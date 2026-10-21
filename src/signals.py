"""Market and research signal adapter with live OpenAlex + arXiv fetching, schema validation, and dated snapshot fallback.

Guarantees:
1. Every valid signal stores: id, title, published_date, retrieved_date, source_name, source_url,
   extracted_skills (constrained strictly to SKILLS_CATALOG), related_roles (constrained strictly
   to ROLES_CATALOG), and is_fallback (boolean).
2. Malformed, undated, unattributed, or zero-skill signals are rejected by validate_signals().
3. If live fetching fails or is disabled, the reviewed snapshot is returned with explicit fallback
   metadata so the UI never presents fallback data as live.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from taxonomy import ROLES_CATALOG, SKILLS_CATALOG

SNAPSHOT_PATH = Path(__file__).resolve().parent.parent / "data" / "signals_snapshot.json"
OPENALEX_QUERY_URL = (
    "https://api.openalex.org/works?"
    "search=artificial+intelligence+llm+workflow+evaluation+governance+sustainability+sql+python"
    "&per-page=18&sort=publication_date:desc"
)
ARXIV_QUERY_URL = (
    "http://export.arxiv.org/api/query?"
    "search_query=cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.CY+OR+cat:cs.SE"
    "&sortBy=submittedDate&sortOrder=descending&max_results=12"
)
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def extract_taxonomy_entities(text: str) -> tuple[list[str], list[str]]:
    """Extract only reviewed skills and roles matched in the text (never invents new skills/roles)."""
    if not text or not isinstance(text, str):
        return [], []
    lowered = text.lower()
    matched_skills: list[str] = []
    for skill_id, skill_info in SKILLS_CATALOG.items():
        if any(kw.lower() in lowered for kw in skill_info.get("keywords", [])):
            matched_skills.append(skill_id)

    matched_roles: list[str] = []
    if matched_skills:
        skill_set = set(matched_skills)
        for role_id, role_info in ROLES_CATALOG.items():
            req = set(role_info.get("required_skills", []))
            sup = set(role_info.get("supporting_skills", []))
            if len(skill_set & (req | sup)) >= 2:
                matched_roles.append(role_id)

    return matched_skills, matched_roles


def validate_signals(
    raw_signals: list[dict] | None,
    reference_date: str | None = None,
    max_age_days: int = 730,
) -> dict:
    """Validate signal records and strip malformed, undated, stale, or unconstrained items."""
    if not isinstance(raw_signals, list) or len(raw_signals) == 0:
        return {
            "valid_signals": [],
            "rejected_count": 0 if not raw_signals else len(raw_signals),
            "status": "insufficient_evidence",
            "warnings": ["No market signal records were provided or available."],
        }

    ref_dt = dt.date.fromisoformat(reference_date) if reference_date else dt.date.today()
    valid: list[dict] = []
    rejected = 0
    warnings: list[str] = []

    for idx, item in enumerate(raw_signals):
        if not isinstance(item, dict):
            rejected += 1
            warnings.append(f"Signal #{idx + 1} rejected: record is not an object.")
            continue

        title = str(item.get("title") or "").strip()
        pub_date = str(item.get("published_date") or "").strip()[:10]
        ret_date = str(item.get("retrieved_date") or "").strip()[:10]
        source_url = str(item.get("source_url") or "").strip()
        source_name = str(item.get("source_name") or "OpenAlex / arXiv API").strip()

        if not title or len(title) < 5:
            rejected += 1
            warnings.append(f"Signal #{idx + 1} rejected: missing or invalid title.")
            continue
        if not ISO_DATE_RE.match(pub_date) or not ISO_DATE_RE.match(ret_date):
            rejected += 1
            warnings.append(f"Signal '{title[:40]}' rejected: invalid ISO date format.")
            continue
        if not (source_url.startswith("http://") or source_url.startswith("https://")):
            rejected += 1
            warnings.append(f"Signal '{title[:40]}' rejected: missing http/https source_url.")
            continue

        try:
            pub_dt = dt.date.fromisoformat(pub_date)
            dt.date.fromisoformat(ret_date)
        except ValueError:
            rejected += 1
            warnings.append(f"Signal '{title[:40]}' rejected: unparseable calendar date.")
            continue

        age_days = (ref_dt - pub_dt).days
        if age_days > max_age_days:
            rejected += 1
            warnings.append(
                f"Signal '{title[:40]}' rejected: stale signal ({age_days} days old > {max_age_days} day limit)."
            )
            continue

        raw_skills = item.get("extracted_skills")
        if isinstance(raw_skills, list) and raw_skills:
            clean_skills = [s for s in raw_skills if s in SKILLS_CATALOG]
        else:
            clean_skills, _ = extract_taxonomy_entities(f"{title} {item.get('summary', '')}")

        if not clean_skills:
            rejected += 1
            warnings.append(
                f"Signal '{title[:40]}' rejected: zero reviewed taxonomy skills matched."
            )
            continue

        raw_roles = item.get("related_roles")
        if isinstance(raw_roles, list) and raw_roles:
            clean_roles = [r for r in raw_roles if r in ROLES_CATALOG]
        else:
            _, clean_roles = extract_taxonomy_entities(
                " ".join(SKILLS_CATALOG[s]["name"] for s in clean_skills)
            )
            if not clean_roles:
                skill_set = set(clean_skills)
                clean_roles = [
                    r_id
                    for r_id, r_info in ROLES_CATALOG.items()
                    if skill_set & (set(r_info["required_skills"]) | set(r_info["supporting_skills"]))
                ]

        valid.append(
            {
                "id": str(item.get("id") or f"sig-{idx + 1}"),
                "title": " ".join(title.split()),
                "published_date": pub_date,
                "retrieved_date": ret_date,
                "source_name": source_name,
                "source_url": source_url,
                "summary": str(item.get("summary") or "").strip(),
                "extracted_skills": clean_skills,
                "related_roles": clean_roles,
                "is_fallback": bool(item.get("is_fallback", False)),
            }
        )

    status = "ok" if len(valid) > 0 else "insufficient_evidence"
    if status != "ok" and not warnings:
        warnings.append("Zero valid signals remained after validation.")

    return {
        "valid_signals": valid,
        "rejected_count": rejected,
        "status": status,
        "warnings": warnings,
    }


def _reconstruct_inverted_abstract(inv: dict | None) -> str:
    if not isinstance(inv, dict) or not inv:
        return ""
    pairs: list[tuple[int, str]] = []
    for word, positions in inv.items():
        if isinstance(positions, list):
            for pos in positions:
                if isinstance(pos, int):
                    pairs.append((pos, str(word)))
    pairs.sort(key=lambda x: x[0])
    return " ".join(w for _, w in pairs[:80])


def parse_openalex_json(json_text: str, retrieved_date: str | None = None) -> list[dict]:
    """Parse OpenAlex /works JSON response into candidate signal dictionaries."""
    if not json_text or not json_text.strip():
        return []
    ret_date = retrieved_date or dt.date.today().isoformat()
    try:
        payload = json.loads(json_text)
    except ValueError:
        return []

    records: list[dict] = []
    for work in payload.get("results", []):
        if not isinstance(work, dict):
            continue
        title = str(work.get("title") or "").strip()
        pub_date = str(work.get("publication_date") or "").strip()[:10]
        work_id = str(work.get("id") or "").strip()
        doi = str(work.get("doi") or "").strip()
        source_url = doi if doi.startswith("http") else work_id
        abstract_text = _reconstruct_inverted_abstract(work.get("abstract_inverted_index"))
        concepts_text = " ".join(
            str(c.get("display_name") or "")
            for c in (work.get("concepts") or [])
            if isinstance(c, dict)
        )
        combined_text = f"{title} {abstract_text} {concepts_text}"
        skills, roles = extract_taxonomy_entities(combined_text)
        if not skills:
            continue

        summary = abstract_text if abstract_text else f"Key concepts: {concepts_text[:200]}"
        records.append(
            {
                "id": work_id.split("/")[-1] if "/" in work_id else (work_id or "openalex-work"),
                "title": title,
                "published_date": pub_date,
                "retrieved_date": ret_date,
                "source_name": "OpenAlex Live API (CC0 Scholarly Feed)",
                "source_url": source_url,
                "summary": summary[:300] + ("..." if len(summary) > 300 else ""),
                "extracted_skills": skills,
                "related_roles": roles,
                "is_fallback": False,
            }
        )
    return records


def parse_arxiv_atom_xml(xml_text: str, retrieved_date: str | None = None) -> list[dict]:
    """Parse arXiv Atom 1.0 XML feed into candidate signal dictionaries."""
    if not xml_text or not xml_text.strip():
        return []
    ret_date = retrieved_date or dt.date.today().isoformat()
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    records: list[dict] = []
    for entry in root.findall("atom:entry", ns):
        entry_id = (entry.findtext("atom:id", default="", namespaces=ns) or "").strip()
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split())
        published = (entry.findtext("atom:published", default="", namespaces=ns) or "").strip()[:10]
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ns) or "").split())

        skills, roles = extract_taxonomy_entities(f"{title} {summary}")
        if not skills:
            continue

        records.append(
            {
                "id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                "title": title,
                "published_date": published,
                "retrieved_date": ret_date,
                "source_name": "arXiv Live API (cs.AI / cs.CL / cs.CY)",
                "source_url": entry_id.replace("http://", "https://"),
                "summary": summary[:320] + ("..." if len(summary) > 320 else ""),
                "extracted_skills": skills,
                "related_roles": roles,
                "is_fallback": False,
            }
        )
    return records


def load_snapshot_signals(snapshot_path: Path = SNAPSHOT_PATH) -> dict:
    """Load the reviewed dated snapshot fallback from disk and validate it."""
    if not snapshot_path.exists():
        return {
            "source_mode": "error_no_snapshot",
            "is_fallback": True,
            "banner_label": "ERROR: Snapshot file missing and live feed unavailable.",
            "signals": [],
            "validation": validate_signals([]),
        }
    raw_data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    raw_list = raw_data.get("signals", [])
    for s in raw_list:
        s["is_fallback"] = True
    validation = validate_signals(raw_list)
    created_date = raw_data.get("snapshot_metadata", {}).get("created_date", "2026-10-20")
    return {
        "source_mode": "fallback_snapshot",
        "is_fallback": True,
        "snapshot_date": created_date,
        "banner_label": (
            f"DATED SNAPSHOT FALLBACK (Snapshot Date: {created_date}) — "
            "Not Live. Displayed transparently so offline demos never fabricate live status."
        ),
        "signals": validation["valid_signals"],
        "validation": validation,
    }


def fetch_market_signals(mode: str = "auto", timeout_sec: float = 5.0) -> dict:
    """Fetch dated AI/job-market signals in 'live', 'auto', 'fallback', or 'malformed_test' mode."""
    if mode == "malformed_test":
        malformed_payload = [
            {"title": "Bad Signal Without URL or Date", "published_date": "invalid-date"},
            {
                "title": "Unrelated Paper With Zero Taxonomy Skills",
                "published_date": "2026-10-18",
                "retrieved_date": "2026-10-20",
                "source_url": "https://arxiv.org/abs/0000.0000",
                "extracted_skills": ["made_up_hallucinated_skill"],
            },
        ]
        validation = validate_signals(malformed_payload)
        return {
            "source_mode": "malformed_test",
            "is_fallback": True,
            "banner_label": "GUARDRAIL TEST MODE: Simulated Malformed / Unverified Signal Feed (All invalid records stripped).",
            "signals": validation["valid_signals"],
            "validation": validation,
        }

    if mode == "fallback":
        return load_snapshot_signals()

    today_str = dt.date.today().isoformat()
    headers = {"User-Agent": "AISkillsCompass-SDCHackathon2026/1.0 (mailto:sdc.xmumhack@gmail.com)"}

    # 1. Primary Live Fetch: OpenAlex REST API (fast, CC0, dated)
    try:
        req = urllib.request.Request(OPENALEX_QUERY_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            json_text = resp.read().decode("utf-8", errors="ignore")
        live_candidates = parse_openalex_json(json_text, retrieved_date=today_str)
        validation = validate_signals(live_candidates)
        if validation["status"] == "ok" and len(validation["valid_signals"]) >= 2:
            return {
                "source_mode": "live_feed",
                "is_fallback": False,
                "banner_label": (
                    f"LIVE SIGNAL FEED — Retrieved from OpenAlex API on {today_str} "
                    f"({len(validation['valid_signals'])} dated works matched reviewed taxonomy)."
                ),
                "signals": validation["valid_signals"],
                "validation": validation,
            }
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        pass

    # 2. Secondary Live Fetch: arXiv Atom API
    try:
        req = urllib.request.Request(ARXIV_QUERY_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            xml_text = resp.read().decode("utf-8", errors="ignore")
        live_candidates = parse_arxiv_atom_xml(xml_text, retrieved_date=today_str)
        validation = validate_signals(live_candidates)
        if validation["status"] == "ok" and len(validation["valid_signals"]) >= 2:
            return {
                "source_mode": "live_feed",
                "is_fallback": False,
                "banner_label": (
                    f"LIVE SIGNAL FEED — Retrieved from arXiv API on {today_str} "
                    f"({len(validation['valid_signals'])} dated papers matched reviewed taxonomy)."
                ),
                "signals": validation["valid_signals"],
                "validation": validation,
            }
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        pass

    fallback = load_snapshot_signals()
    if mode == "live":
        fallback["banner_label"] = (
            "LIVE FETCH UNAVAILABLE (Network/Rate-Limit) — Automatically switched to "
            + fallback["banner_label"]
        )
    return fallback
