"""Script to fetch machine-readable labour market data from api.data.gov.my / OpenDOSM.
Preserves raw snapshots with retrieval timestamp, license, and dataset metadata.
"""

import json
import urllib.request
import datetime as dt
import os
from pathlib import Path

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
OUT_DIR = BASE_DIR / "data" / "trends" / "raw" / "opendosm"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CATALOGUE_IDS = [
    ("lfs_month", "Monthly Labour Force Statistics", "https://api.data.gov.my/data-catalogue?id=lfs_month&limit=1000"),
    ("lfs_qtr", "Quarterly Labour Force Statistics", "https://api.data.gov.my/data-catalogue?id=lfs_qtr&limit=500"),
    ("wages_occupation", "Salaries & Wages by Occupation (Annual)", "https://api.data.gov.my/data-catalogue?id=wages_occupation&limit=1000"),
    ("wages_skill", "Salaries & Wages by Skill Level (Annual)", "https://api.data.gov.my/data-catalogue?id=wages_skill&limit=1000"),
    ("employment_sector", "Employment by Economic Sector (Annual)", "https://api.data.gov.my/data-catalogue?id=employment_sector&limit=1000"),
    ("wages_industry", "Salaries & Wages by Industry Section (Annual)", "https://api.data.gov.my/data-catalogue?id=wages_industry&limit=1000")
]

def fetch_and_save():
    retrieval_time = dt.datetime.now(dt.timezone.utc).isoformat()
    manifest_records = []

    for cid, title, url in CATALOGUE_IDS:
        print(f"Fetching {cid} ({title})...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SDC-M2-Research/1.0 (Government Open Data Ingestion)"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                
                snapshot = {
                    "dataset_id": cid,
                    "title": title,
                    "source_url": url,
                    "publisher": "Department of Statistics Malaysia (DOSM) / OpenDOSM",
                    "portal": "data.gov.my",
                    "licence": "Open Data Commons Open Database License (ODbL) / Creative Commons Attribution 4.0",
                    "retrieved_at": retrieval_time,
                    "record_count": len(data),
                    "data": data
                }
                
                out_path = OUT_DIR / f"{cid}_snapshot.json"
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(snapshot, f, indent=2)
                
                print(f"  Saved {len(data)} records to {out_path.name}")
                manifest_records.append({
                    "dataset_id": cid,
                    "title": title,
                    "status": "LIVE_INGESTED",
                    "record_count": len(data),
                    "file": str(out_path.name),
                    "retrieved_at": retrieval_time
                })
        except Exception as e:
            print(f"  ERROR fetching {cid}: {e}")
            manifest_records.append({
                "dataset_id": cid,
                "title": title,
                "status": "FAILED",
                "error": str(e)
            })

    # Save metadata summary
    summary_path = OUT_DIR / "opendosm_ingestion_manifest.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({"retrieved_at": retrieval_time, "datasets": manifest_records}, f, indent=2)
    print("OpenDOSM ingestion complete!")

if __name__ == "__main__":
    fetch_and_save()
