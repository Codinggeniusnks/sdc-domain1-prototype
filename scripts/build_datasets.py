"""Pipeline for cleaning, standardizing, and assembling multi-source datasets."""

import json
import hashlib
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))
from taxonomy import SKILLS_CATALOG

SKILL_KEYS = list(SKILLS_CATALOG.keys())

def extract_skills_from_text(text: str) -> tuple[list[str], list[float]]:
    t_lower = text.lower()
    matched = []
    labels = []
    for k, v in SKILLS_CATALOG.items():
        kw_list = v.get("keywords", [])
        has_kw = False
        for kw in kw_list:
            pattern = r"\b" + re.escape(kw.lower()) + r"\b"
            if re.search(pattern, t_lower):
                has_kw = True
                break
        if has_kw:
            matched.append(k)
            labels.append(1.0)
        else:
            labels.append(0.0)
    return matched, labels

def main():
    openalex_path = BASE_DIR / "data" / "raw" / "openalex" / "openalex_works.json"
    esco_path = BASE_DIR / "data" / "raw" / "esco" / "esco_occupations.json"
    masco_path = BASE_DIR / "data" / "raw" / "masco" / "masco_mycol_occupations.json"
    synth_path = BASE_DIR / "data" / "training_dataset.json"
    test_manifest_path = BASE_DIR / "data" / "splits" / "frozen_test_manifest.json"

    openalex_raw = json.loads(openalex_path.read_text(encoding="utf-8"))
    esco_raw = json.loads(esco_path.read_text(encoding="utf-8"))
    masco_raw = json.loads(masco_path.read_text(encoding="utf-8"))
    synth_raw = json.loads(synth_path.read_text(encoding="utf-8"))
    test_hashes = set(json.loads(test_manifest_path.read_text(encoding="utf-8"))["record_hashes"])

    processed_records = []
    seen_hashes = set()
    exact_duplicates = 0

    # 1. OpenAlex
    for w in openalex_raw:
        full_text = f"{w['title']}. {w['abstract']}".strip()
        if len(full_text) < 40:
            continue
        h = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
        if h in seen_hashes or h in test_hashes:
            exact_duplicates += 1
            continue
        seen_hashes.add(h)
        skills, labels = extract_skills_from_text(full_text)
        is_emerging = 1.0 if (len(skills) > 0 or any(c in str(w.get("concepts", [])).lower() for c in ["artificial intelligence", "machine learning", "reskilling"])) else 0.0
        
        processed_records.append({
            "id": f"openalex-{w['openalex_id'].split('/')[-1]}",
            "source": "OpenAlex CC0 Scholarly Literature",
            "source_tier": "GOLD",
            "text": full_text,
            "skills": skills,
            "labels": labels,
            "is_emerging_demand": float(is_emerging),
            "doi": w.get("doi"),
            "year": w.get("publication_year")
        })

    # 2. ESCO
    for occ in esco_raw:
        tasks_text = "; ".join(occ.get("essential_skills", [])[:8])
        full_text = f"{occ['title']}. {occ['description']} Key competencies: {tasks_text}".strip()
        h = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
        if h in seen_hashes or h in test_hashes:
            exact_duplicates += 1
            continue
        seen_hashes.add(h)
        skills, labels = extract_skills_from_text(full_text)
        title_l = occ["title"].lower()
        is_routine = any(r in title_l for r in ["clerk", "clerical", "assistant", "data entry", "manual", "sorter", "typist"])
        is_emerging = 0.0 if is_routine else (1.0 if len(skills) > 0 else 0.5)

        uri_hash = hashlib.md5(occ["esco_uri"].encode()).hexdigest()[:8]
        processed_records.append({
            "id": f"esco-{uri_hash}",
            "source": "European Skills, Competences and Occupations (ESCO)",
            "source_tier": "GOLD",
            "text": full_text,
            "skills": skills,
            "labels": labels,
            "is_emerging_demand": float(is_emerging),
            "esco_uri": occ.get("esco_uri")
        })

    # 3. MASCO / MyCOL
    for m in masco_raw:
        full_text = f"MASCO {m['masco_code']}: {m['title']} ({m['sector']}). {m['description']} Key Tasks: {m['tasks']}. Evidence: {m['mycol_evidence']}"
        h = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
        if h in seen_hashes or h in test_hashes:
            exact_duplicates += 1
            continue
        seen_hashes.add(h)
        skills, labels = extract_skills_from_text(full_text)
        is_emerging = 1.0 if m["mycol_critical"] else 0.0
        processed_records.append({
            "id": f"masco-{m['masco_code']}",
            "source": "Malaysia Standard Classification of Occupations (MASCO/MyCOL)",
            "source_tier": "GOLD",
            "text": full_text,
            "skills": skills,
            "labels": labels,
            "is_emerging_demand": float(is_emerging),
            "masco_code": m["masco_code"]
        })

    real_count = len(processed_records)
    print(f"Processed {real_count} real-world records.")

    # 4. Filter Synthetic Training Set (First 1200 only, strict leakage check against test set)
    synth_retained = []
    for s in synth_raw[:1200]:
        t = s["text"]
        h = hashlib.sha256(t.encode("utf-8")).hexdigest()
        if h in test_hashes or h in seen_hashes:
            exact_duplicates += 1
            continue
        seen_hashes.add(h)
        synth_retained.append({
            "id": s["id"],
            "source": "Synthetic Malaysian Worker Task Profile",
            "source_tier": "BRONZE",
            "text": t,
            "skills": s.get("skills", []),
            "labels": s.get("labels", []),
            "is_emerging_demand": float(s.get("is_emerging_demand", 0.0))
        })

    print(f"Retained {len(synth_retained)} unique synthetic training records. Exact duplicates filtered: {exact_duplicates}")

    # Build Dataset v2: Real sources only
    v2_path = BASE_DIR / "data" / "processed" / "dataset_v2_real_sources.json"
    v2_path.write_text(json.dumps(processed_records, indent=2), encoding="utf-8")

    # Build Dataset v3: High-Quality Balanced Real + Controlled Synthetic (1:2 ratio)
    balanced_synth = synth_retained[:640]
    v3_corpus = processed_records + balanced_synth
    v3_path = BASE_DIR / "data" / "processed" / "dataset_v3_real_plus_synthetic.json"
    v3_path.write_text(json.dumps(v3_corpus, indent=2), encoding="utf-8")

    # Dedup & Data Quality Report
    report = {
        "total_records_processed": len(v3_corpus),
        "real_records": real_count,
        "synthetic_records_retained": len(balanced_synth),
        "synthetic_records_original": len(synth_raw[:1200]),
        "duplicates_filtered": exact_duplicates,
        "breakdown_by_source": {
            "OpenAlex CC0 Scholarly Literature": sum(1 for r in v3_corpus if "OpenAlex" in r["source"]),
            "European Skills, Competences and Occupations (ESCO)": sum(1 for r in v3_corpus if "ESCO" in r["source"]),
            "Malaysia Standard Classification of Occupations (MASCO/MyCOL)": sum(1 for r in v3_corpus if "MASCO" in r["source"]),
            "Synthetic Malaysian Worker Task Profile": sum(1 for r in v3_corpus if "Synthetic" in r["source"])
        },
        "quality_tiers": {
            "GOLD": sum(1 for r in v3_corpus if r.get("source_tier") == "GOLD"),
            "BRONZE": sum(1 for r in v3_corpus if r.get("source_tier") == "BRONZE")
        }
    }
    report_path = BASE_DIR / "data" / "manifests" / "data_quality_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Data quality report saved to {report_path}")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
