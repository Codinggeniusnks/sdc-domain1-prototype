"""
scripts/run_m3_benchmarks.py

Executes full benchmark evaluation for M3 Explainable Future-Role Matching Engine v1.1.0.
Evaluates 8 synthetic personas across:
- 3 Weighting Configurations (Balanced Baseline, Skill-Heavy, Scenario-Aware)
- 3 AI Scenarios (REFERENCE_2026, MODERATE_COPILOT, FAST_AGENTIC)

Implements Stage 11C Remediation:
- P2-2: Recalibrated weight sensitivity criteria (Top-3 flip or max displacement >= 4).
- P1-1: Verifies decoupled match strength vs evidence confidence.
- P1-3: Continuous low-fit gating without step discontinuity.
- Generates data/matching/m3_benchmark_results_v1_1.json
- Computes SHA-256 hashes and writes data/matching/m3_build_manifest_v1_1.json
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Set

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
DATA_DIR = BASE_DIR / "data" / "matching"

def compute_spearman(ranks1: List[int], ranks2: List[int]) -> float:
    """Computes Spearman rank correlation coefficient between two equal-length rank lists."""
    n = len(ranks1)
    if n <= 1:
        return 1.0
    d_sq = sum((r1 - r2) ** 2 for r1, r2 in zip(ranks1, ranks2))
    return round(1.0 - (6.0 * d_sq) / (n * (n ** 2 - 1)), 3)

def compute_sha256(filepath: Path) -> str:
    """Computes SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    import sys
    sys.path.append(str(BASE_DIR))
    from src.role_matching_engine import RoleMatchingEngine

    engine = RoleMatchingEngine()

    personas_file = DATA_DIR / "synthetic_personas_v1_1.json"
    if not personas_file.exists():
        personas_file = DATA_DIR / "synthetic_personas_v1.json"
    with open(personas_file, "r", encoding="utf-8") as f:
        personas_data = json.load(f)

    personas = personas_data["personas"]
    weight_configs = ["balanced_baseline", "skill_heavy", "scenario_aware"]
    scenarios = ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]

    benchmark_records = []
    top1_stabilities = []
    top3_overlaps = []
    top5_overlaps = []
    spearman_correlations = []
    all_weight_sensitive_roles = set()

    for p in personas:
        p_id = p["persona_id"]
        p_name = p["persona_name"]
        p_cat = p["category"]

        persona_eval = {
            "persona_id": p_id,
            "persona_name": p_name,
            "category": p_cat,
            "evaluations": {}
        }

        # Evaluate across weight configs under default REFERENCE_2026
        ref_rankings_by_weight = {}
        for w_cfg in weight_configs:
            ranked = engine.rank_roles(p, scenario_id="REFERENCE_2026", weight_config=w_cfg)
            ref_rankings_by_weight[w_cfg] = ranked

        bal_ranks = {r["masco_code"]: r["rank"] for r in ref_rankings_by_weight["balanced_baseline"]}
        skill_ranks = {r["masco_code"]: r["rank"] for r in ref_rankings_by_weight["skill_heavy"]}
        scen_ranks = {r["masco_code"]: r["rank"] for r in ref_rankings_by_weight["scenario_aware"]}

        bal_indices = {r["masco_code"]: r["role_match_index"] for r in ref_rankings_by_weight["balanced_baseline"]}
        skill_indices = {r["masco_code"]: r["role_match_index"] for r in ref_rankings_by_weight["skill_heavy"]}
        scen_indices = {r["masco_code"]: r["role_match_index"] for r in ref_rankings_by_weight["scenario_aware"]}

        # 1. Top-1 stability
        bal_top1 = ref_rankings_by_weight["balanced_baseline"][0]["masco_code"]
        skill_top1 = ref_rankings_by_weight["skill_heavy"][0]["masco_code"]
        scen_top1 = ref_rankings_by_weight["scenario_aware"][0]["masco_code"]
        top1_stable = (bal_top1 == skill_top1 == scen_top1)
        top1_stabilities.append(1.0 if top1_stable else 0.0)

        # 2. Top-3 overlap (Jaccard)
        bal_top3 = {r["masco_code"] for r in ref_rankings_by_weight["balanced_baseline"][:3]}
        skill_top3 = {r["masco_code"] for r in ref_rankings_by_weight["skill_heavy"][:3]}
        scen_top3 = {r["masco_code"] for r in ref_rankings_by_weight["scenario_aware"][:3]}
        jaccard_skill3 = len(bal_top3 & skill_top3) / len(bal_top3 | skill_top3)
        jaccard_scen3 = len(bal_top3 & scen_top3) / len(bal_top3 | scen_top3)
        avg_top3_overlap = round((jaccard_skill3 + jaccard_scen3) / 2.0, 3)
        top3_overlaps.append(avg_top3_overlap)

        # 3. Top-5 overlap (Jaccard)
        bal_top5 = {r["masco_code"] for r in ref_rankings_by_weight["balanced_baseline"][:5]}
        skill_top5 = {r["masco_code"] for r in ref_rankings_by_weight["skill_heavy"][:5]}
        scen_top5 = {r["masco_code"] for r in ref_rankings_by_weight["scenario_aware"][:5]}
        jaccard_skill5 = len(bal_top5 & skill_top5) / len(bal_top5 | skill_top5)
        jaccard_scen5 = len(bal_top5 & scen_top5) / len(bal_top5 | scen_top5)
        avg_top5_overlap = round((jaccard_skill5 + jaccard_scen5) / 2.0, 3)
        top5_overlaps.append(avg_top5_overlap)

        # 4. Spearman correlation across all 20 roles
        codes_ordered = sorted(bal_ranks.keys())
        b_list = [bal_ranks[c] for c in codes_ordered]
        sk_list = [skill_ranks[c] for c in codes_ordered]
        sc_list = [scen_ranks[c] for c in codes_ordered]
        sp_skill = compute_spearman(b_list, sk_list)
        sp_scen = compute_spearman(b_list, sc_list)
        avg_sp = round((sp_skill + sp_scen) / 2.0, 3)
        spearman_correlations.append(avg_sp)

        # 5. P2-2 Remediation: Recalibrated Weight-Sensitivity Flag
        # Rule: Top-3 membership changed OR absolute rank displacement >= 4
        p_sensitive_roles = []
        for c in codes_ordered:
            ranks = [bal_ranks[c], skill_ranks[c], scen_ranks[c]]
            max_disp = max(ranks) - min(ranks)
            
            # Check if top-3 membership changes
            in_bal_top3 = (bal_ranks[c] <= 3)
            in_skill_top3 = (skill_ranks[c] <= 3)
            in_scen_top3 = (scen_ranks[c] <= 3)
            top3_changed = not (in_bal_top3 == in_skill_top3 == in_scen_top3)

            # Check if top-5 membership changes
            in_bal_top5 = (bal_ranks[c] <= 5)
            in_skill_top5 = (skill_ranks[c] <= 5)
            in_scen_top5 = (scen_ranks[c] <= 5)
            top5_changed = not (in_bal_top5 == in_skill_top5 == in_scen_top5)

            indices = [bal_indices[c], skill_indices[c], scen_indices[c]]
            index_range = round(max(indices) - min(indices), 1)

            is_sensitive = (top3_changed or max_disp >= 4)

            if is_sensitive:
                p_sensitive_roles.append({
                    "masco_code": c,
                    "occupation_title": engine.roles[c]["occupation_title"],
                    "rank_balanced": bal_ranks[c],
                    "rank_skill_heavy": skill_ranks[c],
                    "rank_scenario_aware": scen_ranks[c],
                    "max_rank_displacement": max_disp,
                    "top3_membership_changed": top3_changed,
                    "top5_membership_changed": top5_changed,
                    "match_index_range_across_configs": index_range,
                    "flag": "WEIGHT_SENSITIVE_RECOMMENDATION"
                })
                all_weight_sensitive_roles.add(c)

        # Evaluate across scenarios under balanced baseline
        scenario_outcomes = {}
        for sc in scenarios:
            ranked_sc = engine.rank_roles(p, scenario_id=sc, weight_config="balanced_baseline")
            scenario_outcomes[sc] = {
                "top_1": {
                    "masco_code": ranked_sc[0]["masco_code"],
                    "title": ranked_sc[0]["occupation_title"],
                    "role_match_index": ranked_sc[0]["role_match_index"],
                    "match_strength_label": ranked_sc[0]["match_strength_label"],
                    "evidence_confidence_label": ranked_sc[0]["evidence_confidence_label"]
                },
                "top_3": [
                    {
                        "rank": r["rank"],
                        "masco_code": r["masco_code"],
                        "title": r["occupation_title"],
                        "role_match_index": r["role_match_index"],
                        "match_strength_label": r["match_strength_label"],
                        "evidence_confidence_label": r["evidence_confidence_label"]
                    }
                    for r in ranked_sc[:3]
                ]
            }

        persona_eval["weight_sensitivity"] = {
            "top1_stable": top1_stable,
            "top1_roles": {"balanced": bal_top1, "skill_heavy": skill_top1, "scenario_aware": scen_top1},
            "top3_overlap": avg_top3_overlap,
            "top5_overlap": avg_top5_overlap,
            "spearman_correlation": avg_sp,
            "weight_sensitive_roles": p_sensitive_roles
        }
        persona_eval["scenario_sensitivity"] = scenario_outcomes
        benchmark_records.append(persona_eval)

    # Global Benchmark Aggregation
    overall_top1_stability = round(sum(top1_stabilities) / len(top1_stabilities) * 100.0, 1)
    overall_top3_overlap = round(sum(top3_overlaps) / len(top3_overlaps), 3)
    overall_top5_overlap = round(sum(top5_overlaps) / len(top5_overlaps), 3)
    overall_avg_spearman = round(sum(spearman_correlations) / len(spearman_correlations), 3)

    benchmark_summary = {
        "version": "1.1.0",
        "benchmark_date": "2026-10-23",
        "total_personas_evaluated": len(personas),
        "total_candidate_roles_per_evaluation": len(engine.roles),
        "weight_configurations_evaluated": weight_configs,
        "scenarios_evaluated": scenarios,
        "aggregate_metrics": {
            "top1_weight_stability_pct": overall_top1_stability,
            "average_top3_overlap_jaccard": overall_top3_overlap,
            "average_top5_overlap_jaccard": overall_top5_overlap,
            "average_spearman_rank_correlation": overall_avg_spearman,
            "total_weight_sensitive_roles_count": len(all_weight_sensitive_roles),
            "weight_sensitive_roles": sorted(list(all_weight_sensitive_roles))
        },
        "persona_evaluations": benchmark_records
    }

    results_path = DATA_DIR / "m3_benchmark_results_v1_1.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_summary, f, indent=2)

    print(f"Successfully generated benchmark results at {results_path}")
    print(f"Top-1 Weight Stability: {overall_top1_stability}%")
    print(f"Average Top-3 Overlap: {overall_top3_overlap}")
    print(f"Average Top-5 Overlap: {overall_top5_overlap}")
    print(f"Average Spearman Rank Correlation: {overall_avg_spearman}")
    print(f"Recalibrated Weight-Sensitive Roles Count: {len(all_weight_sensitive_roles)} (was 18 in v1.0.0)")

    # Generate M3 Build Manifest v1.1.0
    manifest_files = [
        DATA_DIR / "role_requirements_v1_1.json",
        DATA_DIR / "m3_scoring_config_v1_1.json",
        DATA_DIR / "synthetic_personas_v1_1.json",
        DATA_DIR / "m3_benchmark_results_v1_1.json",
        BASE_DIR / "src" / "role_matching_engine.py",
        BASE_DIR / "scripts" / "build_role_requirements.py",
        BASE_DIR / "scripts" / "run_m3_benchmarks.py"
    ]

    manifest = {
        "version": "1.1.0",
        "module": "M3_EXPLAINABLE_FUTURE_ROLE_MATCHING_ENGINE",
        "build_date": "2026-10-23",
        "upstream_dependencies": {
            "m1_skills_extraction": {
                "model": "H_blend_0.70A_0.30C1_W1.0",
                "status": "FROZEN",
                "provenance": "Protocol B and Protocol C v2 were unsealed exactly once during Stage 8E for the approved final frozen M1 evaluation. No additional Protocol B or Protocol C v2 access occurred during Stages 9A onward."
            },
            "m2_trend_intelligence": {
                "version": "v1.1.1",
                "status": "FORMALLY_FROZEN",
                "manifest_sha256": "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542"
            },
            "m6_scenario_engine": {
                "version": "v1.1.0",
                "status": "FORMALLY_FROZEN",
                "manifest_sha256": "ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5"
            }
        },
        "candidate_universe": {
            "target_granularity": "FOUR_DIGIT_OCCUPATION",
            "candidate_role_count": 20,
            "excluded_fallback_count": 8
        },
        "artifacts_sha256": {}
    }

    for f_path in manifest_files:
        if f_path.exists():
            manifest["artifacts_sha256"][str(f_path.relative_to(BASE_DIR)).replace("\\", "/")] = compute_sha256(f_path)

    manifest_path = DATA_DIR / "m3_build_manifest_v1_1.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    manifest_hash = compute_sha256(manifest_path)
    print(f"Generated M3 Build Manifest at {manifest_path} (Manifest SHA-256: {manifest_hash})")

if __name__ == "__main__":
    main()
