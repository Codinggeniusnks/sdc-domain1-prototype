"""Build OpenAlex temporal research momentum dataset from the 208-record evidence corpus.
Strictly decoupled from M1 supervised training.
Computes temporal research indicators: publication counts by year and skill, growth momentum,
citation impact velocity, and topic emergence.
"""

import json
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
CORPUS_PATH = BASE_DIR / "data" / "processed" / "openalex_trend_evidence_corpus.json"
OUT_DIR = BASE_DIR / "data" / "trends" / "raw" / "openalex"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def build_openalex_raw():
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    print(f"Loaded {len(corpus)} records from openalex_trend_evidence_corpus.json")

    # Group by year
    by_year = defaultdict(int)
    by_skill_by_year = defaultdict(lambda: defaultdict(int))
    citations_by_skill = defaultdict(list)
    skill_counts = defaultdict(int)

    for item in corpus:
        raw_year = item.get("publication_year")
        year = int(raw_year) if raw_year is not None else 2023
        raw_cits = item.get("cited_by_count")
        citations = int(raw_cits) if raw_cits is not None else 0
        by_year[year] += 1
        
        skills = item.get("extracted_taxonomy_skills", [])
        for s in skills:
            skill_counts[s] += 1
            by_skill_by_year[s][year] += 1
            citations_by_skill[s].append(citations)

    # Calculate momentum per skill
    skill_momentum = {}
    for skill, total_count in skill_counts.items():
        year_dist = dict(by_skill_by_year[skill])
        # Recent: 2024, 2025, 2026
        recent_count = sum(year_dist.get(y, 0) for y in [2024, 2025, 2026])
        baseline_count = sum(year_dist.get(y, 0) for y in [2020, 2021, 2022, 2023])
        recent_share = round(recent_count / total_count, 4) if total_count > 0 else 0.0
        
        # Growth velocity
        growth_rate = round((recent_count / 3.0) / ((baseline_count / 4.0) + 0.1), 3)
        cits = citations_by_skill[skill]
        mean_citations = round(sum(cits) / len(cits), 2) if cits else 0.0
        
        # Emergence tag
        emergence = "SURGING_MOMENTUM" if recent_share >= 0.50 and growth_rate >= 1.5 else (
            "STEADY_GROWTH" if recent_share >= 0.30 else "ESTABLISHED_BASELINE"
        )

        skill_momentum[skill] = {
            "total_publications": total_count,
            "publications_by_year": {str(y): year_dist.get(y, 0) for y in sorted(list(set(by_year.keys())))},
            "recent_count_2024_2026": recent_count,
            "baseline_count_2020_2023": baseline_count,
            "recent_publication_share": recent_share,
            "growth_rate_ratio": growth_rate,
            "mean_citations": mean_citations,
            "emergence_category": emergence
        }

    dataset = {
        "source": "OpenAlex Scholarly Works Corpus",
        "publisher": "OurResearch (OpenAlex API, CC0)",
        "retrieval_date": "2026-10-21",
        "total_works": len(corpus),
        "corpus_temporal_span": {
            "min_year": min(by_year.keys()),
            "max_year": max(by_year.keys()),
            "publications_by_year": {str(y): by_year[y] for y in sorted(by_year.keys())}
        },
        "skill_research_momentum": skill_momentum,
        "sample_works": corpus[:5]
    }

    out_file = OUT_DIR / "openalex_temporal_momentum.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"Saved OpenAlex temporal research momentum to {out_file.name} ({len(skill_momentum)} skills analyzed)")

if __name__ == "__main__":
    build_openalex_raw()
