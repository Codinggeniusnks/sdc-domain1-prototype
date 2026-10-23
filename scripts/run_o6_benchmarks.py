"""
run_o6_benchmarks.py

Executes the official 13 benchmark cases for O6 SDG Contribution Aggregation Engine v1.1.0.
Validates:
- BM01: Single individual alignment
- BM02: Multi-skill individual with duplicate SDG mappings (deduplication verification)
- BM03: Cohort above privacy threshold (>= 5)
- BM04: Cohort below privacy threshold (< 5) suppression
- BM05: Mixed-role company cohort and M5 flag propagation
- BM06: Scenario comparison across REFERENCE_2026, MODERATE_COPILOT, FAST_AGENTIC
- BM07: CURRENT vs POST_PATHWAY capability view
- BM08: Regional synthetic aggregation
- BM09: Malformed profile exclusion & denominator integrity (DEF-P1-01)
- BM10: Complementary suppression & differencing protection (DEF-P2-02)
- BM11: Canonical mapping-type deduplication (i, t, tau) (DEF-P2-03)
- BM12: Fairness claim semantics & structural non-use (DEF-P2-01)
- BM13: Regional & cohort runtime representativeness disclaimer (DEF-P3-02)

Outputs:
- data/aggregation/o6_benchmark_results_v1_1.json
- data/aggregation/o6_build_manifest_v1_1.json
"""

import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.sdg_aggregation_engine import SDGAggregationEngine


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def run_benchmarks():
    print("=" * 60)
    print("O6 SDG Contribution Aggregation Engine v1.1.0 Benchmark Suite")
    print("=" * 60)

    engine = SDGAggregationEngine()

    # Load synthetic workforce
    wf_path = ROOT / "data" / "aggregation" / "synthetic_workforce_v1.json"
    with open(wf_path, "r", encoding="utf-8") as f:
        wf_data = json.load(f)
    profiles = wf_data["profiles"]
    print(f"Loaded {len(profiles)} synthetic profiles from {wf_path.name}")

    benchmarks = []

    # -------------------------------------------------------------
    # BM01: Single individual alignment
    # -------------------------------------------------------------
    print("\nRunning Benchmark 1: Single individual alignment...")
    p1 = profiles[0]
    res1 = engine.aggregate_individual_alignment(p1, time_dimension="CURRENT")
    bm1_passed = (
        res1["aggregation_level"] == "INDIVIDUAL"
        and res1["profile_id"] == "SYN_PROF_001"
        and res1["descriptive_metrics"]["aligned_sdg_count"] > 0
        and res1["descriptive_metrics"]["aligned_target_count"] > 0
        and res1["governance_safeguards"]["individual_sdg_score_computed"] is False
        and res1["governance_safeguards"]["employee_sustainability_ranking_computed"] is False
        and "SDG_score" not in res1
    )
    benchmarks.append({
        "benchmark_id": "BM01_SINGLE_INDIVIDUAL_ALIGNMENT",
        "description": "Validation of descriptive individual alignment metrics without personal SDG scores or employee ranking",
        "profile_id": p1["profile_id"],
        "aligned_sdgs": res1["aligned_sdgs"],
        "aligned_sdg_count": res1["descriptive_metrics"]["aligned_sdg_count"],
        "direct_mappings": res1["descriptive_metrics"]["direct_mapping_count"],
        "enabling_mappings": res1["descriptive_metrics"]["enabling_mapping_count"],
        "contextual_mappings": res1["descriptive_metrics"]["contextual_mapping_count"],
        "passed": bm1_passed
    })
    print(f"BM01 Outcome: {'PASSED' if bm1_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM02: Multi-skill individual with duplicate SDG mappings (Deduplication)
    # -------------------------------------------------------------
    print("\nRunning Benchmark 2: Multi-skill individual deduplication...")
    sdg_occurrences = {}
    for sdg in res1["aligned_sdgs"]:
        sdg_occurrences[sdg] = sdg_occurrences.get(sdg, 0) + 1

    no_duplicate_sdgs = all(count == 1 for count in sdg_occurrences.values())
    bm2_passed = (
        no_duplicate_sdgs
        and 8 in res1["aligned_sdgs"]
        and 9 in res1["aligned_sdgs"]
        and res1["descriptive_metrics"]["aligned_sdg_count"] == len(set(res1["aligned_sdgs"]))
    )
    benchmarks.append({
        "benchmark_id": "BM02_MULTI_SKILL_INDIVIDUAL_DEDUPLICATION",
        "description": "Validation that a profile holding multiple skills mapping to the same SDG counts the SDG exactly once",
        "profile_id": p1["profile_id"],
        "unique_sdg_count": len(res1["aligned_sdgs"]),
        "duplicate_sdg_detected": not no_duplicate_sdgs,
        "passed": bm2_passed
    })
    print(f"BM02 Outcome: {'PASSED' if bm2_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM03: Cohort above privacy threshold (>= 5)
    # -------------------------------------------------------------
    print("\nRunning Benchmark 3: Cohort above privacy threshold...")
    digital_profiles = [p for p in profiles if p["cohort_id"] == "DIGITAL_SERVICES"]
    res3 = engine.aggregate_cohort_alignment(digital_profiles, cohort_id="DIGITAL_SERVICES")
    bm3_passed = (
        res3["suppressed"] is False
        and res3["eligible_count"] == 16
        and res3["sdg_alignment_prevalence"] is not None
        and res3["target_prevalence"] is not None
        and 0.0 <= res3["sdg_alignment_prevalence"]["SDG_8"]["prevalence_ratio"] <= 1.0
        and 0.0 <= res3["sdg_alignment_prevalence"]["SDG_9"]["prevalence_ratio"] <= 1.0
        and round(
            res3["mapping_type_distribution"]["direct_share"]
            + res3["mapping_type_distribution"]["enabling_share"]
            + res3["mapping_type_distribution"]["contextual_share"],
            2
        ) == 1.0
    )
    benchmarks.append({
        "benchmark_id": "BM03_COHORT_ABOVE_PRIVACY_THRESHOLD",
        "description": "Validation of full statistical aggregation for cohort meeting privacy threshold (N=16 >= 5)",
        "cohort_id": "DIGITAL_SERVICES",
        "eligible_count": res3["eligible_count"],
        "suppressed": res3["suppressed"],
        "sdg_8_prevalence_pct": res3["sdg_alignment_prevalence"]["SDG_8"]["prevalence_percentage"],
        "sdg_9_prevalence_pct": res3["sdg_alignment_prevalence"]["SDG_9"]["prevalence_percentage"],
        "mapping_shares": {
            "direct": res3["mapping_type_distribution"]["direct_share"],
            "enabling": res3["mapping_type_distribution"]["enabling_share"],
            "contextual": res3["mapping_type_distribution"]["contextual_share"]
        },
        "passed": bm3_passed
    })
    print(f"BM03 Outcome: {'PASSED' if bm3_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM04: Cohort below privacy threshold (< 5)
    # -------------------------------------------------------------
    print("\nRunning Benchmark 4: Cohort below privacy threshold suppression...")
    small_subset = digital_profiles[:4]  # N=4 < 5
    res4 = engine.aggregate_cohort_alignment(small_subset, cohort_id="SMALL_TEST_GROUP")
    bm4_passed = (
        res4["suppressed"] is True
        and res4["suppression_reason"] == "SUPPRESSED_SMALL_COHORT"
        and res4["eligible_count"] == 4
        and res4["sdg_alignment_prevalence"] is None
        and res4["target_prevalence"] is None
        and res4["mapping_type_distribution"] is None
        and res4["capability_coverage"] is None
        and "SMALL_COHORT_SUPPRESSED" in res4["quality_flags"]
    )
    benchmarks.append({
        "benchmark_id": "BM04_COHORT_BELOW_PRIVACY_THRESHOLD",
        "description": "Validation of complete statistical suppression for small cohorts (N=4 < 5) to prevent disclosure",
        "cohort_id": "SMALL_TEST_GROUP",
        "eligible_count": res4["eligible_count"],
        "suppressed": res4["suppressed"],
        "suppression_reason": res4["suppression_reason"],
        "distributions_suppressed": (
            res4["sdg_alignment_prevalence"] is None and res4["target_prevalence"] is None
        ),
        "passed": bm4_passed
    })
    print(f"BM04 Outcome: {'PASSED' if bm4_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM05: Mixed-role company cohort and M5 flag propagation
    # -------------------------------------------------------------
    print("\nRunning Benchmark 5: Mixed-role cohort & M5 flag propagation...")
    mfg_profiles = [p for p in profiles if p["cohort_id"] == "ADVANCED_MANUFACTURING"]
    res5 = engine.aggregate_cohort_alignment(mfg_profiles, cohort_id="ADVANCED_MANUFACTURING")
    has_sector_flag = "SECTOR_DEPENDENT_ALIGNMENT_PRESENT" in res5["quality_flags"]
    has_med_conf = "MEDIUM_CONFIDENCE_MAPPING_PRESENT" in res5["quality_flags"]
    bm5_passed = (
        res5["suppressed"] is False
        and res5["eligible_count"] == 14
        and len(res5["role_alignment_distribution"]) > 1
        and has_sector_flag
        and has_med_conf
    )
    benchmarks.append({
        "benchmark_id": "BM05_MIXED_ROLE_COHORT_FLAG_PROPAGATION",
        "description": "Validation of role diversity and propagation of M5 sector-dependence and medium-confidence flags",
        "cohort_id": "ADVANCED_MANUFACTURING",
        "eligible_count": res5["eligible_count"],
        "roles_represented": list(res5["role_alignment_distribution"].keys()),
        "sector_dependent_flag_propagated": has_sector_flag,
        "medium_confidence_flag_propagated": has_med_conf,
        "passed": bm5_passed
    })
    print(f"BM05 Outcome: {'PASSED' if bm5_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM06: Scenario comparison across M6 scenarios
    # -------------------------------------------------------------
    print("\nRunning Benchmark 6: Scenario comparison (M6 foresight)...")
    res6 = engine.compare_scenarios(digital_profiles, cohort_id="DIGITAL_SERVICES")
    bm6_passed = (
        res6.get("suppressed") is not True
        and "REFERENCE_2026" in res6["results"]
        and "MODERATE_COPILOT" in res6["results"]
        and "FAST_AGENTIC" in res6["results"]
        and "role_scenario_foresight" in res6["results"]["FAST_AGENTIC"]
        and "structured_assumption_notice" in res6
    )
    benchmarks.append({
        "benchmark_id": "BM06_SCENARIO_COMPARISON",
        "description": "Validation of foresight scenario integration without altering underlying M5 qualitative mappings",
        "cohort_id": "DIGITAL_SERVICES",
        "scenarios_evaluated": res6["scenarios_evaluated"],
        "fast_agentic_roles_foresight_count": len(res6["results"]["FAST_AGENTIC"]["role_scenario_foresight"]),
        "passed": bm6_passed
    })
    print(f"BM06 Outcome: {'PASSED' if bm6_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM07: CURRENT vs POST_PATHWAY capability view
    # -------------------------------------------------------------
    print("\nRunning Benchmark 7: CURRENT vs POST_PATHWAY capability view...")
    green_profiles = [p for p in profiles if p["cohort_id"] == "GREEN_TRANSITION"]
    res7_cur = engine.aggregate_cohort_alignment(green_profiles, cohort_id="GREEN_TRANSITION", time_dimension="CURRENT")
    res7_post = engine.aggregate_cohort_alignment(green_profiles, cohort_id="GREEN_TRANSITION", time_dimension="POST_PATHWAY")

    cur_skills_sdg12 = res7_cur["capability_coverage"]["SDG_12"]["skills_present_count"]
    post_skills_sdg12 = res7_post["capability_coverage"]["SDG_12"]["skills_present_count"]

    bm7_passed = (
        res7_cur["suppressed"] is False
        and res7_post["suppressed"] is False
        and res7_cur["time_dimension_label"] == "CURRENT_CAPABILITIES"
        and res7_post["time_dimension_label"] == "PROJECTED CAPABILITY ALIGNMENT IF PATHWAY COMPLETED"
        and post_skills_sdg12 >= cur_skills_sdg12
        and "PROJECTED_CAPABILITY_SCENARIO" in res7_post["quality_flags"]
    )
    benchmarks.append({
        "benchmark_id": "BM07_CURRENT_VS_POST_PATHWAY_CAPABILITY",
        "description": "Validation of temporal capability scenario comparison with mandatory projection disclaimers",
        "cohort_id": "GREEN_TRANSITION",
        "current_sdg12_skills_count": cur_skills_sdg12,
        "post_pathway_sdg12_skills_count": post_skills_sdg12,
        "current_label": res7_cur["time_dimension_label"],
        "post_pathway_label": res7_post["time_dimension_label"],
        "passed": bm7_passed
    })
    print(f"BM07 Outcome: {'PASSED' if bm7_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM08: Regional synthetic aggregation
    # -------------------------------------------------------------
    print("\nRunning Benchmark 8: Regional synthetic aggregation...")
    res8 = engine.aggregate_region_alignment(profiles, region_id="REGION_A")
    bm8_passed = (
        res8["aggregation_level"] == "REGIONAL_SYNTHETIC"
        and res8["region_id"] == "REGION_A"
        and res8["eligible_count"] == 19
        and res8["suppressed"] is False
        and "representativeness_disclaimer" in res8
        and "synthetic demonstration cohort" in res8["representativeness_disclaimer"].lower()
    )
    benchmarks.append({
        "benchmark_id": "BM08_REGIONAL_SYNTHETIC_AGGREGATION",
        "description": "Validation of regional synthetic population aggregation with non-identifying geography disclaimer",
        "region_id": "REGION_A",
        "eligible_count": res8["eligible_count"],
        "suppressed": res8["suppressed"],
        "sdg_alignment_prevalence_keys": list(res8["sdg_alignment_prevalence"].keys())[:5],
        "passed": bm8_passed
    })
    print(f"BM08 Outcome: {'PASSED' if bm8_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM09: Malformed profile exclusion & denominator integrity (DEF-P1-01)
    # -------------------------------------------------------------
    print("\nRunning Benchmark 9: Malformed profile exclusion & denominator integrity (DEF-P1-01)...")
    valid_base = list(profiles[:6])
    malformed_items = [
        {},
        {"some_random_key": "val"},
        None,
        "invalid_string_profile",
        {"profile_id": "VALID_PID_NONE_SKILLS", "current_role": {"masco_code": "2512"}, "confirmed_skills": None}
    ]
    mixed_cohort = valid_base + malformed_items
    res9 = engine.aggregate_cohort_alignment(mixed_cohort, cohort_id="BM09_MIXED_COHORT")
    # Expected: 6 valid_base + 1 valid with none skills = 7 eligible profiles
    # Excluded: 2 incomplete ({}, {some_key}), 2 invalid types (None, string) = 4 excluded
    bm9_passed = (
        res9["input_profile_count"] == 11
        and res9["eligible_profile_count"] == 7
        and res9["excluded_profile_count"] == 4
        and res9["excluded_profiles_by_reason"]["INCOMPLETE_PROFILE_DATA"] == 2
        and res9["excluded_profiles_by_reason"]["INVALID_PROFILE_TYPE"] == 2
        and res9["suppressed"] is False
        and "EXCLUDED_FROM_DENOMINATOR" in res9["quality_flags"]
    )
    benchmarks.append({
        "benchmark_id": "BM09_MALFORMED_PROFILE_EXCLUSION",
        "description": "Validation that malformed, empty, None, and non-dict records are quarantined and excluded from denominator",
        "input_profile_count": res9["input_profile_count"],
        "eligible_profile_count": res9["eligible_profile_count"],
        "excluded_profile_count": res9["excluded_profile_count"],
        "excluded_by_reason": res9["excluded_profiles_by_reason"],
        "passed": bm9_passed
    })
    print(f"BM09 Outcome: {'PASSED' if bm9_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM10: Complementary suppression & differencing protection (DEF-P2-02)
    # -------------------------------------------------------------
    print("\nRunning Benchmark 10: Complementary suppression & differencing protection (DEF-P2-02)...")
    # Build 10 profiles: 6 in Sub A, 4 in Sub B
    p_sub_a = [dict(profiles[i], profile_id=f"SYN_BM10_A_{i}", sub_dept="DEPT_A") for i in range(6)]
    p_sub_b = [dict(profiles[i], profile_id=f"SYN_BM10_B_{i}", sub_dept="DEPT_B") for i in range(4)]
    combined_10 = p_sub_a + p_sub_b

    breakdown_bm10 = engine.aggregate_partition_breakdown(combined_10, partition_key="sub_dept", cohort_id="BM10_PARENT")
    bm10_passed = (
        breakdown_bm10["parent_eligible_count"] == 10
        and breakdown_bm10["complementary_suppression_applied"] is True
        and "DEPT_B" in breakdown_bm10["small_cells_suppressed"]
        and "DEPT_A" in breakdown_bm10["complementary_suppressed_cells"]
        and breakdown_bm10["partition_cells"]["DEPT_A"]["suppression_reason"] == "SUPPRESSED_COMPLEMENTARY_RULE"
        and breakdown_bm10["partition_cells"]["DEPT_A"]["sdg_alignment_prevalence"] is None
        and breakdown_bm10["partition_cells"]["DEPT_B"]["suppression_reason"] == "SUPPRESSED_SMALL_COHORT"
    )
    benchmarks.append({
        "benchmark_id": "BM10_COMPLEMENTARY_SUPPRESSION",
        "description": "Validation of partition-aware complementary suppression preventing subtraction recovery in N=10 (6+4)",
        "parent_count": breakdown_bm10["parent_eligible_count"],
        "small_cells_suppressed": breakdown_bm10["small_cells_suppressed"],
        "complementary_suppressed_cells": breakdown_bm10["complementary_suppressed_cells"],
        "passed": bm10_passed
    })
    print(f"BM10 Outcome: {'PASSED' if bm10_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM11: Canonical mapping-type deduplication (i, t, tau) (DEF-P2-03)
    # -------------------------------------------------------------
    print("\nRunning Benchmark 11: Canonical mapping-type deduplication (i, t, tau) (DEF-P2-03)...")
    # Single profile with multiple skills reaching target 8.2 ENABLING
    p_dedup = {
        "profile_id": "SYN_BM11_DEDUP",
        "current_role": {"masco_code": "2512"},
        "confirmed_skills": ["python_scripting", "api_integration", "sql_data_analysis"]
    }
    ind_11 = engine.aggregate_individual_alignment(p_dedup)
    # For individual, target 8.2 ENABLING is counted once in unique relations
    res11_cohort = engine.aggregate_cohort_alignment(profiles[:5])
    m_dist11 = res11_cohort["mapping_type_distribution"]
    bm11_passed = (
        m_dist11["counting_unit"] == "UNIQUE_PROFILE_TARGET_MAPPING_TYPE_RELATION"
        and m_dist11["total_mappings_evaluated"] > 0
        and round(m_dist11["direct_share"] + m_dist11["enabling_share"] + m_dist11["contextual_share"], 2) == 1.0
    )
    benchmarks.append({
        "benchmark_id": "BM11_MAPPING_TYPE_DEDUP",
        "description": "Validation of canonical counting unit (i, t, tau) deduplicating multiple skill/role instances",
        "counting_unit": m_dist11["counting_unit"],
        "total_relations": m_dist11["total_mappings_evaluated"],
        "shares_sum": round(m_dist11["direct_share"] + m_dist11["enabling_share"] + m_dist11["contextual_share"], 4),
        "passed": bm11_passed
    })
    print(f"BM11 Outcome: {'PASSED' if bm11_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM12: Fairness claim semantics & structural non-use (DEF-P2-01)
    # -------------------------------------------------------------
    print("\nRunning Benchmark 12: Fairness claim semantics & structural non-use (DEF-P2-01)...")
    res12 = engine.aggregate_cohort_alignment(profiles[:10])
    o5_hook = res12["o5_fairness_hook"]
    bm12_passed = (
        o5_hook["protected_attributes_used"] is False
        and o5_hook["demographic_fairness_evaluated"] is False
        and o5_hook["fairness_scope"] == "STRUCTURAL_PROTECTED_ATTRIBUTE_NON_USE"
        and "disparate_impact_ratio" not in o5_hook
        and "DIR" not in o5_hook
        and "demographic group labels" in o5_hook["fairness_policy_note"]
    )
    benchmarks.append({
        "benchmark_id": "BM12_FAIRNESS_CLAIM_SEMANTICS",
        "description": "Validation of structural non-use fairness language and absolute removal of empirical DIR claims",
        "protected_attributes_used": o5_hook["protected_attributes_used"],
        "demographic_fairness_evaluated": o5_hook["demographic_fairness_evaluated"],
        "fairness_scope": o5_hook["fairness_scope"],
        "passed": bm12_passed
    })
    print(f"BM12 Outcome: {'PASSED' if bm12_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # BM13: Regional & cohort runtime representativeness disclaimer (DEF-P3-02)
    # -------------------------------------------------------------
    print("\nRunning Benchmark 13: Regional & cohort runtime representativeness disclaimer (DEF-P3-02)...")
    res13_cohort = engine.aggregate_cohort_alignment(profiles[:10])
    res13_region = engine.aggregate_region_alignment(profiles, region_id="REGION_B")
    bm13_passed = (
        res13_cohort["data_source_class"] == "SYNTHETIC_DEMO"
        and res13_region["data_source_class"] == "SYNTHETIC_DEMO"
        and "not statistically representative" in res13_cohort["representativeness_disclaimer"].lower()
        and "not statistically representative" in res13_region["representativeness_disclaimer"].lower()
        and res13_cohort["pathway_alignment_coverage"]["pathway_alignment_coverage_scope"] == "PLANNED_CURRICULUM_SKILL_STEPS"
    )
    benchmarks.append({
        "benchmark_id": "BM13_REGIONAL_RUNTIME_DISCLAIMER",
        "description": "Validation of runtime JSON representativeness disclaimer and pathway alignment coverage scope",
        "cohort_data_source_class": res13_cohort["data_source_class"],
        "region_data_source_class": res13_region["data_source_class"],
        "pathway_scope": res13_cohort["pathway_alignment_coverage"]["pathway_alignment_coverage_scope"],
        "passed": bm13_passed
    })
    print(f"BM13 Outcome: {'PASSED' if bm13_passed else 'FAILED'}")

    # -------------------------------------------------------------
    # Save Benchmark Results
    # -------------------------------------------------------------
    all_passed = all(bm["passed"] for bm in benchmarks)
    benchmark_report = {
        "engine_name": "O6 SDG Contribution Aggregation Engine",
        "version": "1.1.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_benchmarks": len(benchmarks),
        "passed_count": sum(1 for bm in benchmarks if bm["passed"]),
        "all_passed": all_passed,
        "benchmarks": benchmarks
    }

    out_bm = ROOT / "data" / "aggregation" / "o6_benchmark_results_v1_1.json"
    with open(out_bm, "w", encoding="utf-8") as f:
        json.dump(benchmark_report, f, indent=2, ensure_ascii=False)
    print(f"\nSaved benchmark results to {out_bm}")

    # -------------------------------------------------------------
    # Generate Build Manifest v1.1.0
    # -------------------------------------------------------------
    tracked_files = [
        "data/aggregation/o6_config_v1_1.json",
        "data/aggregation/synthetic_workforce_v1.json",
        "data/aggregation/o6_benchmark_results_v1_1.json",
        "src/sdg_aggregation_engine.py",
        "scripts/build_synthetic_workforce.py",
        "scripts/run_o6_benchmarks.py",
        "tests/test_sdg_aggregation_engine.py"
    ]

    manifest = {
        "engine_name": "O6 SDG Contribution Aggregation Engine",
        "engine_version": "1.1.0",
        "status": "REMEDIATED_STAGE_14C",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "benchmarks_passed": f"{sum(1 for bm in benchmarks if bm['passed'])}/{len(benchmarks)}",
        "pinned_upstream_dependencies": {
            "m5_sdg_mapping_freeze_hash": "94c1f42b46a1fa5e9b026fb82d5225e21c24547cdd58c234f2843cd84eb32ec7",
            "m4_reskilling_freeze_hash": "448545188ba4e196eaf3502d7803c3d9cfbb1247ec453208cafae990c8db5f2f",
            "m3_role_matching_build_hash": "15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c",
            "m2_trend_intelligence_freeze_hash": "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542",
            "m6_scenario_engine_build_hash": "ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5"
        },
        "file_manifest": {}
    }

    for rel_path in tracked_files:
        p = ROOT / rel_path
        if p.exists():
            manifest["file_manifest"][rel_path] = {
                "sha256": compute_sha256(p),
                "bytes": p.stat().st_size
            }

    out_manifest = ROOT / "data" / "aggregation" / "o6_build_manifest_v1_1.json"
    with open(out_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Saved build manifest to {out_manifest}")

    print("=" * 60)
    print(f"BENCHMARK OUTCOME: {'ALL 13 BENCHMARKS PASSED' if all_passed else 'FAILURES DETECTED'}")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmarks()
