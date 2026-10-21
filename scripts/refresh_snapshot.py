"""Rebuild data/signals_snapshot.json from a real OpenAlex API response.

Usage: python scripts/refresh_snapshot.py
Every record written here comes verbatim (title, date, DOI/URL) from the API; review the
diff before committing. Records are research publications, not vacancy data.
"""

import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from signals import OPENALEX_QUERY_URL, SNAPSHOT_PATH, parse_openalex_json, validate_signals  # noqa: E402

today = dt.date.today().isoformat()
req = urllib.request.Request(OPENALEX_QUERY_URL, headers={"User-Agent": "AISkillsCompass-snapshot/1.0"})
with urllib.request.urlopen(req, timeout=20) as resp:
    records = parse_openalex_json(resp.read().decode("utf-8"), retrieved_date=today)
valid = validate_signals(records)["valid_signals"]
if len(valid) < 2:
    sys.exit(f"Refusing to write snapshot: only {len(valid)} valid records.")
for s in valid:
    s["source_name"] = "OpenAlex API (CC0) — dated snapshot"
    s["is_fallback"] = True
SNAPSHOT_PATH.write_text(
    json.dumps(
        {
            "snapshot_metadata": {
                "snapshot_id": f"openalex-{today}",
                "created_date": today,
                "query_url": OPENALEX_QUERY_URL,
                "description": (
                    "Dated snapshot of scholarly AI publications retrieved from the OpenAlex API (CC0). "
                    "Research-activity signals only; NOT job postings, vacancy counts, or hiring data."
                ),
                "is_fallback": True,
            },
            "signals": valid,
        },
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)
print(f"Wrote {len(valid)} records to {SNAPSHOT_PATH}")
