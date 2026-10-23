"""
scripts/run_requirement_sensitivity.py

Evaluates M3 v1.1.0 sensitivity to borderline requirement tier classifications:
Perturbs borderline requirements (e.g. IMPORTANT <-> SUPPORTING or borderline CORE emerging)
while keeping clear authoritative core requirements intact.
Reports:
- Top-1 stability
- Top-3 overlap
- Spearman rank correlation
"""

import copy
import json
from pathlib import Path
import sys

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
sys.path.insert(0, str(BASE_DIR))

from src.role_matching_engine import RoleMatchingEngine

def compute_spearman(ranks1, ranks2):
    n = len(ranks1)
    if n <= 1:
        return 1.0
    d_sq = sum((r1 - r2) ** 2 for r1, r2 in zip(ranks1, ranks2))
    return round(1.0 - (6.0 * d_sq) / (n * (n ** 2 - 1)), 3)

def main():
    engine_base = RoleMatchingEngine()
    
    # Load personas
    with open(BASE_DIR / "data" / "matching" / "synthetic_personas_v1_1.json", "r", encoding="utf-8") as f:
        personas = json.load(f)["personas"]

    # Perturbed catalog: perturb borderline emerging skills in select roles
    # E.g. in 2529, rag_knowledge_systems perturbed from CORE (weight 1.0) to IMPORTANT (0.6)
    # in 2512, workflow_automation perturbed from IMPORTANT (0.6) to SUPPORTING (0.3)
    # in 2411, process_mapping perturbed from IMPORTANT (0.6) to SUPPORTING (0.3)
    perturbed_catalog = copy.deepcopy(engine_base.role_catalog)
    for r in perturbed_catalog["roles"]:
        if r["masco_code"] == "2512":
            r["skill_requirement_strength"]["workflow_automation"] = "SUPPORTING"
        elif r["masco_code"] == "2411":
            r["skill_requirement_strength"]["process_mapping"] = "SUPPORTING"
        elif r["masco_code"] == "2152":
            r["skill_requirement_strength"]["process_mapping"] = "SUPPORTING"
        elif r["masco_code"] == "2166":
            r["skill_requirement_strength"]["stakeholder_communication"] = "SUPPORTING"

    engine_perturbed = RoleMatchingEngine()
    engine_perturbed.roles = {}
    for r in perturbed_catalog.get("roles", []):
        code = str(r["masco_code"])
        if r.get("entity_granularity") == "FOUR_DIGIT_OCCUPATION" and not code.startswith("MAJOR_"):
            engine_perturbed.roles[code] = r

    top1_matches = 0
    top3_jaccards = []
    correlations = []

    for p in personas:
        rank_base = engine_base.rank_roles(p)
        rank_pert = engine_perturbed.rank_roles(p)

        b_top1 = rank_base[0]["masco_code"]
        p_top1 = rank_pert[0]["masco_code"]
        if b_top1 == p_top1:
            top1_matches += 1

        b_top3 = {r["masco_code"] for r in rank_base[:3]}
        p_top3 = {r["masco_code"] for r in rank_pert[:3]}
        jaccard = len(b_top3 & p_top3) / len(b_top3 | p_top3)
        top3_jaccards.append(jaccard)

        codes = sorted([r["masco_code"] for r in rank_base])
        b_ranks = {r["masco_code"]: r["rank"] for r in rank_base}
        p_ranks = {r["masco_code"]: r["rank"] for r in rank_pert}

        b_list = [b_ranks[c] for c in codes]
        p_list = [p_ranks[c] for c in codes]
        correlations.append(compute_spearman(b_list, p_list))

    top1_pct = round(top1_matches / len(personas) * 100.0, 1)
    avg_top3 = round(sum(top3_jaccards) / len(top3_jaccards), 3)
    avg_corr = round(sum(correlations) / len(correlations), 3)

    print("=" * 60)
    print("M3 v1.1.0 REQUIREMENT TIER SENSITIVITY RESULTS")
    print("=" * 60)
    print(f"Top-1 Recommendation Stability: {top1_pct}%")
    print(f"Average Top-3 Overlap (Jaccard): {avg_top3}")
    print(f"Average Spearman Rank Correlation: {avg_corr}")
    print("=" * 60)

if __name__ == "__main__":
    main()
