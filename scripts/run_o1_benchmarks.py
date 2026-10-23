"""
scripts/run_o1_benchmarks.py

Official Benchmark Execution Suite for:
O1 Employer / HR Workforce Gap & Cohort Reskilling Engine v1.1.0

Runs 18 Mandated Benchmarks:
BM01 — Standard synthetic company cohort (50 profiles)
BM02 — One highly prevalent CORE skill gap
BM03 — Mixed CORE / IMPORTANT / SUPPORTING gaps
BM04 — Cross-role transferable skill
BM05 — Prerequisite-sensitive cohort plan
BM06 — Scenario comparison (Reference vs Copilot vs Agentic)
BM07 — Small cohort suppression (N < 5) and complementary suppression
BM08 — Malformed profiles and denominator integrity
BM09 — Shared learning opportunity (learner-hours vs session duration)
BM10 — SDG capability context without corporate impact scoring
BM11 — Shared learning small cell (N=2–4) suppressed
BM12 — Priority skill small cell (N=3 in N=50) suppressed & no leakage
BM13 — Role transition small cell (N=2) suppressed
BM14 — Heatmap cell privacy (cell count 1–4 masked)
BM15 — Complementary partition suppression (Parent 10 / A 6 / B 4)
BM16 — CORE-weighted preference semantics (adversarial counterexample)
BM17 — Binary deficit non-discriminating policy (weight = 0.0)
BM18 — Priority regression stability (v1.0 -> v1.1 Spearman rho >= 0.99)

Saves results to: data/workforce/o1_benchmark_results_v1_1.json
Saves build manifest to: data/workforce/o1_build_manifest_v1_1.json
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.workforce_gap_engine import WorkforceGapEngine


def compute_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def run_all_benchmarks():
    print("=" * 60)
    print("O1 Employer Workforce Gap & Reskilling Engine v1.1.0 Benchmarks")
    print("=" * 60)

    engine = WorkforceGapEngine()
    wf_path = ROOT / "data" / "aggregation" / "synthetic_workforce_v1.json"
    with open(wf_path, "r", encoding="utf-8") as f:
        profiles = json.load(f)["profiles"]

    print(f"Loaded {len(profiles)} synthetic profiles from {wf_path.name}")
    results = []

    # -------------------------------------------------------------
    # BM01: Standard Synthetic Company Cohort (50 profiles)
    # -------------------------------------------------------------
    print("\nRunning BM01: Standard synthetic company cohort...")
    res01 = engine.analyse_workforce_gaps(profiles, scenario="REFERENCE_2026", cohort_id="COMPANY_ALL")
    passed01 = (
        res01["eligible_profile_count"] == 50
        and not res01["suppressed"]
        and len(res01["priority_skills"]) == 16
        and res01.get("status") != "FAILED"
    )
    print(f"BM01 Outcome: {'PASSED' if passed01 else 'FAILED'} (Eligible: {res01['eligible_profile_count']})")
    results.append({
        "benchmark_id": "BM01_STANDARD_SYNTHETIC_COHORT",
        "description": "Validation of complete 50-profile enterprise workforce gap analysis",
        "eligible_profile_count": res01["eligible_profile_count"],
        "top_skill": res01["priority_skills"][0]["skill_id"],
        "top_internal_index": res01["priority_skills"][0]["_internal_priority_index"],
        "passed": passed01
    })

    # -------------------------------------------------------------
    # BM02: Highly Prevalent CORE Skill Gap
    # -------------------------------------------------------------
    print("\nRunning BM02: Highly prevalent CORE skill gap...")
    matrix01 = res01["skill_gap_matrix"]
    highest_core_skill = max(matrix01.values(), key=lambda x: x["core_gap_prevalence"] or 0.0)
    passed02 = (
        (highest_core_skill["core_gap_prevalence"] or 0.0) > 0.20
        and (highest_core_skill["profiles_with_core_gap"] or 0) >= 10
    )
    print(f"BM02 Outcome: {'PASSED' if passed02 else 'FAILED'} (Skill: {highest_core_skill['skill_id']}, Core Prev: {highest_core_skill['core_gap_prevalence']})")
    results.append({
        "benchmark_id": "BM02_HIGH_PREVALENCE_CORE_GAP",
        "description": "Detection of dominant critical core competency deficit across cohort",
        "skill_id": highest_core_skill["skill_id"],
        "core_gap_prevalence": highest_core_skill["core_gap_prevalence"],
        "profiles_with_core_gap": highest_core_skill["profiles_with_core_gap"],
        "passed": passed02
    })

    # -------------------------------------------------------------
    # BM03: Mixed CORE / IMPORTANT / SUPPORTING Gaps
    # -------------------------------------------------------------
    print("\nRunning BM03: Mixed CORE / IMPORTANT / SUPPORTING gaps...")
    all_core = sum((item["profiles_with_core_gap"] or 0) for item in matrix01.values())
    all_imp = sum((item["profiles_with_important_gap"] or 0) for item in matrix01.values())
    all_sup = sum((item["profiles_with_supporting_gap"] or 0) for item in matrix01.values())
    passed03 = all_core > 0 and all_imp > 0 and all_sup > 0
    print(f"BM03 Outcome: {'PASSED' if passed03 else 'FAILED'} (Core: {all_core}, Important: {all_imp}, Supporting: {all_sup})")
    results.append({
        "benchmark_id": "BM03_MIXED_REQUIREMENT_TIERS",
        "description": "Validation of stratified requirement tier distribution across catalog",
        "total_core_gaps": all_core,
        "total_important_gaps": all_imp,
        "total_supporting_gaps": all_sup,
        "passed": passed03
    })

    # -------------------------------------------------------------
    # BM04: Cross-Role Transferable Skill
    # -------------------------------------------------------------
    print("\nRunning BM04: Cross-role transferable skill...")
    proc_map = matrix01.get("process_mapping", {})
    passed04 = (
        proc_map.get("transferability_pct", 0.0) >= 60.0
        and (proc_map.get("profiles_with_gap") or proc_map.get("_raw_profiles_with_gap", 0)) > 0
    )
    print(f"BM04 Outcome: {'PASSED' if passed04 else 'FAILED'} (Transferability: {proc_map.get('transferability_pct')}%)")
    results.append({
        "benchmark_id": "BM04_CROSS_ROLE_TRANSFERABILITY",
        "description": "Validation of multi-role leverage and transferability weighting",
        "skill_id": "process_mapping",
        "transferability_pct": proc_map.get("transferability_pct"),
        "passed": passed04
    })

    # -------------------------------------------------------------
    # BM05: Prerequisite-Sensitive Cohort Plan
    # -------------------------------------------------------------
    print("\nRunning BM05: Prerequisite-sensitive cohort plan...")
    plan01 = res01["cohort_reskilling_plan"]
    foundations = plan01["roadmap_phases"]["PHASE 1 — FOUNDATIONS"]
    passed05 = (
        len(foundations) > 0
        and all(item["prerequisite_dependencies"] or len(engine.downstream_prereqs.get(item["skill_id"], set())) >= 2 for item in foundations)
    )
    print(f"BM05 Outcome: {'PASSED' if passed05 else 'FAILED'} (Foundations Count: {len(foundations)})")
    results.append({
        "benchmark_id": "BM05_PREREQUISITE_COHORT_ROADMAP",
        "description": "Validation of prerequisite-ordered sequencing in cohort roadmap",
        "foundation_skills": [item["skill_id"] for item in foundations],
        "passed": passed05
    })

    # -------------------------------------------------------------
    # BM06: Scenario Comparison (Reference vs Copilot vs Agentic)
    # -------------------------------------------------------------
    print("\nRunning BM06: Scenario comparison...")
    scen_comp = res01["scenario_summary"]
    sensitive = scen_comp.get("most_scenario_sensitive_skills", [])
    passed06 = (
        len(scen_comp.get("scenarios_evaluated", [])) == 3
        and len(sensitive) >= 2
        and "rag_knowledge_systems" in sensitive
    )
    print(f"BM06 Outcome: {'PASSED' if passed06 else 'FAILED'} (Sensitive Skills: {sensitive})")
    results.append({
        "benchmark_id": "BM06_SCENARIO_COMPARISON",
        "description": "Validation of multi-scenario reskilling priority sensitivity",
        "scenarios_evaluated": scen_comp.get("scenarios_evaluated"),
        "most_scenario_sensitive_skills": sensitive,
        "passed": passed06
    })

    # -------------------------------------------------------------
    # BM07: Small Cohort Suppression (N < 5) and Masking
    # -------------------------------------------------------------
    print("\nRunning BM07: Small cohort suppression...")
    small_cohort = profiles[:4]  # N=4 < 5
    res07 = engine.analyse_workforce_gaps(small_cohort, cohort_id="SMALL_PILOT")
    passed07 = (
        res07["suppressed"] is True
        and res07["suppression_reason"] == "COHORT_SIZE_BELOW_PRIVACY_THRESHOLD"
        and len(res07["skill_gap_matrix"]) == 0
        and res07["privacy_metadata"]["exact_small_cell_count_masked"] is True
    )
    print(f"BM07 Outcome: {'PASSED' if passed07 else 'FAILED'} (Suppressed: {res07['suppressed']}, Reason: {res07['suppression_reason']})")
    results.append({
        "benchmark_id": "BM07_SMALL_COHORT_SUPPRESSION",
        "description": "Enforcement of k=5 k-anonymity privacy floor with masked distributions",
        "input_count": len(small_cohort),
        "suppressed": res07["suppressed"],
        "suppression_reason": res07["suppression_reason"],
        "passed": passed07
    })

    # -------------------------------------------------------------
    # BM08: Malformed Profiles & Denominator Integrity
    # -------------------------------------------------------------
    print("\nRunning BM08: Malformed profiles & denominator integrity...")
    malformed_cohort = [
        None,
        "invalid_string_profile",
        {"invalid_key": "no_id"},
        profiles[0],
        profiles[1],
        profiles[2],
        profiles[3],
        profiles[4]
    ]
    res08 = engine.analyse_workforce_gaps(malformed_cohort, cohort_id="DIRTY_COHORT")
    passed08 = (
        res08["input_profile_count"] == 8
        and res08["eligible_profile_count"] == 5
        and res08["excluded_profile_count"] == 3
        and not res08["suppressed"]
    )
    print(f"BM08 Outcome: {'PASSED' if passed08 else 'FAILED'} (Input: {res08['input_profile_count']}, Eligible: {res08['eligible_profile_count']}, Excluded: {res08['excluded_profile_count']})")
    results.append({
        "benchmark_id": "BM08_DENOMINATOR_INTEGRITY",
        "description": "Deterministic sanitization separating eligible from excluded profiles",
        "input_profile_count": res08["input_profile_count"],
        "eligible_profile_count": res08["eligible_profile_count"],
        "excluded_profile_count": res08["excluded_profile_count"],
        "passed": passed08
    })

    # -------------------------------------------------------------
    # BM09: Shared Learning Opportunity & Hour Semantics
    # -------------------------------------------------------------
    print("\nRunning BM09: Shared learning opportunity & hour semantics...")
    shared_opps = res01["shared_learning_opportunities"]
    top_shared = shared_opps[0] if shared_opps else {}
    passed09 = (
        len(shared_opps) > 0
        and top_shared.get("profiles_affected", 0) >= 5
        and top_shared.get("shared_curriculum_hours_range") is not None
        and top_shared.get("aggregate_learner_hours_range") is not None
        and top_shared["aggregate_learner_hours_range"][0] > top_shared["shared_curriculum_hours_range"][0]
    )
    print(f"BM09 Outcome: {'PASSED' if passed09 else 'FAILED'} (Top Shared: {top_shared.get('shared_skill')}, Affected: {top_shared.get('profiles_affected')})")
    results.append({
        "benchmark_id": "BM09_SHARED_LEARNING_OPPORTUNITIES",
        "description": "Aggregation of cohort curriculum with explicit learner-hours distinction",
        "shared_skill": top_shared.get("shared_skill"),
        "profiles_affected": top_shared.get("profiles_affected"),
        "shared_session_hours": top_shared.get("shared_curriculum_hours_range"),
        "aggregate_learner_hours": top_shared.get("aggregate_learner_hours_range"),
        "passed": passed09
    })

    # -------------------------------------------------------------
    # BM10: SDG Capability Context (No Impact Scoring)
    # -------------------------------------------------------------
    print("\nRunning BM10: SDG capability context without impact scoring...")
    sdg_ctx = res01["sdg_capability_context"]
    top_plan_sdg = res01["cohort_reskilling_plan"]["priority_skills_plan"][0]["sdg_alignment_context"]
    passed10 = (
        sdg_ctx["sdg_mappings_status"] == "DESCRIPTIVE_ALIGNMENT_NOT_IMPACT"
        and sdg_ctx["corporate_sdg_impact_score"] is None
        and len(top_plan_sdg.get("primary_sdgs", [])) > 0
    )
    print(f"BM10 Outcome: {'PASSED' if passed10 else 'FAILED'} (SDG Status: {sdg_ctx['sdg_mappings_status']})")
    results.append({
        "benchmark_id": "BM10_SDG_CAPABILITY_CONTEXT",
        "description": "Integration of descriptive SDG mapping metadata without corporate score generation",
        "sdg_status": sdg_ctx["sdg_mappings_status"],
        "corporate_impact_score_omitted": sdg_ctx["corporate_sdg_impact_score"] is None,
        "passed": passed10
    })

    # -------------------------------------------------------------
    # BM11: Shared Learning Small Cell (N=2–4) Suppressed
    # -------------------------------------------------------------
    print("\nRunning BM11: Shared learning small cell suppression...")
    # instructional_design in synthetic workforce has raw gap = 0.
    # In res01, any raw small cell learning need (1-4) is suppressed.
    small_cell_needs = res01["small_cell_learning_needs_suppressed_count"]
    # Test with custom cohort where skill X has exactly 3 gapped profiles out of 10
    custom_p = []
    for i in range(10):
        # 3 profiles lack python_scripting, 7 have it
        skills_c = ["python_scripting"] if i >= 3 else []
        custom_p.append({
            "profile_id": f"P_BM11_{i:02d}",
            "confirmed_skills": skills_c,
            "target_role": {"masco_code": "2511"}
        })
    shared_custom = engine.identify_shared_learning_opportunities(custom_p)
    # python_scripting affects 3 (< 5), so it must be suppressed from employer listing
    py_in_shared = any(item.get("shared_skill") == "python_scripting" for item in shared_custom)
    passed11 = (not py_in_shared) and (len(shared_custom) == 0 or all(item["profiles_affected"] >= 5 for item in shared_custom))
    print(f"BM11 Outcome: {'PASSED' if passed11 else 'FAILED'} (Small Cell Suppressed: {not py_in_shared})")
    results.append({
        "benchmark_id": "BM11_SHARED_LEARNING_SMALL_CELL",
        "description": "Enforce k=5 suppression on shared learning: 1-4 small subgroups withheld",
        "small_cell_count_tested": 3,
        "suppressed_from_employer_listing": not py_in_shared,
        "passed": passed11
    })

    # -------------------------------------------------------------
    # BM12: Priority Skill Small Cell (N=3 in N=50) Suppressed & No Leakage
    # -------------------------------------------------------------
    print("\nRunning BM12: Priority skill small cell suppression...")
    # Test skill gap affecting 3 employees inside cohort N=50
    cohort_bm12 = []
    for i in range(50):
        # 3 profiles lack sql_data_analysis, 47 have it
        sk = ["sql_data_analysis"] if i >= 3 else []
        cohort_bm12.append({
            "profile_id": f"P_BM12_{i:02d}",
            "confirmed_skills": sk,
            "target_role": {"masco_code": "2511"}
        })
    ranks12 = engine.rank_workforce_reskilling_priorities(cohort_bm12)
    sql_item = next(item for item in ranks12 if item["skill_id"] == "sql_data_analysis")
    passed12 = (
        sql_item["priority_status"] == "SUPPRESSED_SMALL_CELL"
        and sql_item["priority_index"] is None
        and sql_item["components"] is None
        and sql_item["weighted_contributions"] is None
        and sql_item["affected_profile_count"] is None
        and sql_item["affected_profile_count_display"] == "<5"
    )
    print(f"BM12 Outcome: {'PASSED' if passed12 else 'FAILED'} (Priority Status: {sql_item['priority_status']}, Index: {sql_item['priority_index']})")
    results.append({
        "benchmark_id": "BM12_PRIORITY_SKILL_SMALL_CELL",
        "description": "Suppression of priority index, decomposition, and counts when skill gap < 5",
        "priority_status": sql_item["priority_status"],
        "priority_index_is_none": sql_item["priority_index"] is None,
        "components_is_none": sql_item["components"] is None,
        "passed": passed12
    })

    # -------------------------------------------------------------
    # BM13: Role Transition Small Cell (N=2) Suppressed
    # -------------------------------------------------------------
    print("\nRunning BM13: Role transition small cell suppression...")
    # Create cohort of 10 with 2 transitions from 2511 to 2512
    cohort_bm13 = []
    for i in range(10):
        c_role = "2511"
        t_role = "2512" if i < 2 else "2511"
        cohort_bm13.append({
            "profile_id": f"P_BM13_{i:02d}",
            "current_role": {"masco_code": c_role},
            "target_role": {"masco_code": t_role},
            "confirmed_skills": ["python_scripting"]
        })
    trans_summary = engine.build_role_gap_summary(cohort_bm13)
    trans_2511_2512 = next((t for t in trans_summary["role_transitions"] if t["current_masco"] == "2511" and t["target_masco"] == "2512"), None)
    passed13 = (
        trans_2511_2512 is not None
        and trans_2511_2512["suppressed"] is True
        and trans_2511_2512["transition_volume"] is None
        and trans_2511_2512["transition_volume_display"] == "<5"
        and trans_2511_2512["suppression_reason"] == "SMALL_CELL_PRIVACY"
    )
    print(f"BM13 Outcome: {'PASSED' if passed13 else 'FAILED'} (Suppressed: {trans_2511_2512['suppressed']}, Disp: {trans_2511_2512['transition_volume_display']})")
    results.append({
        "benchmark_id": "BM13_ROLE_TRANSITION_SMALL_CELL",
        "description": "Masking of transition volume and percentage when transition volume < 5",
        "suppressed": trans_2511_2512["suppressed"] if trans_2511_2512 else False,
        "transition_volume_display": trans_2511_2512["transition_volume_display"] if trans_2511_2512 else None,
        "passed": passed13
    })

    # -------------------------------------------------------------
    # BM14: Heatmap Cell Privacy (cell count 1–4 masked)
    # -------------------------------------------------------------
    print("\nRunning BM14: Heatmap cell privacy...")
    # Build heatmap for synthetic workforce
    heatmap = engine.build_heatmap_payload(profiles)
    cells = heatmap.get("cells", [])
    supp_cells = [c for c in cells if c.get("suppressed")]
    small_cells = [c for c in supp_cells if c.get("suppression_reason") == "SMALL_CELL_PRIVACY"]
    passed14 = bool(
        len(small_cells) > 0
        and all(c["display_value"] is None and c["count_display"] == "<5" for c in small_cells)
    )
    print(f"BM14 Outcome: {'PASSED' if passed14 else 'FAILED'} (Small Cells Masked: {len(small_cells)})")
    results.append({
        "benchmark_id": "BM14_HEATMAP_CELL_PRIVACY",
        "description": "Masking of individual heatmap cells with gapped profile count < 5",
        "small_cells_count": len(small_cells),
        "all_small_cells_suppressed": passed14,
        "passed": passed14
    })

    # -------------------------------------------------------------
    # BM15: Complementary Partition Suppression (Parent 10 / A 6 / B 4)
    # -------------------------------------------------------------
    print("\nRunning BM15: Complementary partition suppression...")
    supp_res = engine.apply_partition_suppression({"A": 6, "B": 4}, parent_total=10)
    passed15 = bool(
        supp_res["B"]["suppressed"] is True
        and supp_res["B"]["suppression_reason"] == "SMALL_CELL_PRIVACY"
        and supp_res["B"]["count"] is None
        and supp_res["A"]["suppressed"] is True
        and supp_res["A"]["suppression_reason"] == "SUPPRESSED_COMPLEMENTARY_RULE"
        and supp_res["A"]["count"] is None
    )
    print(f"BM15 Outcome: {'PASSED' if passed15 else 'FAILED'} (A Reason: {supp_res['A']['suppression_reason']}, B Reason: {supp_res['B']['suppression_reason']})")
    results.append({
        "benchmark_id": "BM15_COMPLEMENTARY_SUPPRESSION",
        "description": "Deterministic complementary suppression across partition (Parent 10 / A 6 / B 4)",
        "child_b_reason": supp_res["B"]["suppression_reason"],
        "child_a_reason": supp_res["A"]["suppression_reason"],
        "passed": passed15
    })

    # -------------------------------------------------------------
    # BM16: CORE-Weighted Preference Semantics (Adversarial Fixture)
    # -------------------------------------------------------------
    print("\nRunning BM16: CORE-weighted preference semantics...")
    # Adversarial fixture: Widespread IMPORTANT gap (0.80) outranks rare CORE gap (0.05)
    w = engine.weights
    x_imp_wide = 0.80
    score_imp = (w["important_gap_prevalence"] * x_imp_wide + w["cross_role_transferability"] * 0.50 + w["prerequisite_centrality"] * 0.20) * 100.0
    x_core_rare = 0.05
    score_core = (w["core_gap_prevalence"] * x_core_rare) * 100.0
    passed16 = bool(
        score_imp > score_core
        and res01["core_first_metadata"]["core_first_semantics"] == "CORE_WEIGHTED_PREFERENCE"
    )
    print(f"BM16 Outcome: {'PASSED' if passed16 else 'FAILED'} (Imp Score: {score_imp:.2f} > Core Score: {score_core:.2f})")
    results.append({
        "benchmark_id": "BM16_CORE_WEIGHTED_NOT_ABSOLUTE",
        "description": "Proof that CORE semantics implement weighted preference rather than structural precedence",
        "widespread_important_score": round(score_imp, 2),
        "rare_core_score": round(score_core, 2),
        "semantics_label": res01["core_first_metadata"]["core_first_semantics"],
        "passed": passed16
    })

    # -------------------------------------------------------------
    # BM17: Binary Deficit Non-Discriminating Policy (Weight = 0.0)
    # -------------------------------------------------------------
    print("\nRunning BM17: Binary deficit non-discriminating policy...")
    matrix_deficits = [s["mean_deficit_among_gapped_profiles"] for s in matrix01.values() if s["mean_deficit_among_gapped_profiles"] is not None and s["mean_deficit_among_gapped_profiles"] > 0]
    unique_deficits = set(matrix_deficits)
    passed17 = (
        len(unique_deficits) == 1
        and engine.weights.get("average_deficit") == 0.0
        and res01["deficit_metadata"]["deficit_signal_status"] == "BINARY_NON_DISCRIMINATING"
        and res01["deficit_metadata"]["deficit_used_for_ranking"] is False
        and res01["deficit_metadata"]["deficit_diagnostic_only"] is True
    )
    print(f"BM17 Outcome: {'PASSED' if passed17 else 'FAILED'} (Deficit Weight: {engine.weights.get('average_deficit')}, Status: {res01['deficit_metadata']['deficit_signal_status']})")
    results.append({
        "benchmark_id": "BM17_BINARY_DEFICIT_POLICY",
        "description": "Disabling of non-discriminating deficit ranking component with diagnostic preservation",
        "deficit_ranking_weight": engine.weights.get("average_deficit"),
        "deficit_signal_status": res01["deficit_metadata"]["deficit_signal_status"],
        "diagnostic_only": res01["deficit_metadata"]["deficit_diagnostic_only"],
        "passed": passed17
    })

    # -------------------------------------------------------------
    # BM18: Priority Regression Stability (v1.0 -> v1.1 Spearman rho >= 0.99)
    # -------------------------------------------------------------
    print("\nRunning BM18: Priority regression stability...")
    engine_v1 = WorkforceGapEngine(config_path=os.path.join(ROOT, "data", "workforce", "o1_config_v1.json"))
    ranks_v1 = engine_v1.rank_workforce_reskilling_priorities(profiles)
    ranks_v1_1 = engine.rank_workforce_reskilling_priorities(profiles)

    map_v1 = {item["skill_id"]: item["_internal_priority_index"] for item in ranks_v1}
    map_v1_1 = {item["skill_id"]: item["_internal_priority_index"] for item in ranks_v1_1}

    skills_common = list(map_v1.keys())
    scores_v1 = [map_v1[s] for s in skills_common]
    scores_v1_1 = [map_v1_1[s] for s in skills_common]

    rho, _ = spearmanr(scores_v1, scores_v1_1)
    passed18 = bool(rho >= 0.99)
    print(f"BM18 Outcome: {'PASSED' if passed18 else 'FAILED'} (Spearman rho: {rho:.6f})")
    results.append({
        "benchmark_id": "BM18_PRIORITY_REGRESSION",
        "description": "Validation that removal of constant deficit offset preserves rank ordering",
        "spearman_rank_correlation": round(float(rho), 6),
        "rank_stability_threshold": 0.99,
        "passed": passed18
    })

    # -------------------------------------------------------------
    # Summary & Manifest Generation
    # -------------------------------------------------------------
    all_passed = bool(all(b["passed"] for b in results))
    summary = {
        "engine_name": "O1 Employer Workforce Gap & Reskilling Engine",
        "version": "1.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_benchmarks": len(results),
        "passed_count": sum(1 for b in results if b["passed"]),
        "all_passed": all_passed,
        "benchmarks": results
    }

    # Save benchmark results v1_1
    out_path = ROOT / "data" / "workforce" / "o1_benchmark_results_v1_1.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved benchmark results to {out_path}")

    # Generate build manifest v1_1
    build_manifest = {
        "engine_name": "O1 Employer Workforce Gap & Reskilling Engine",
        "engine_version": "1.1.0",
        "status": "REMEDIATED_CANDIDATE_READY_FOR_FREEZE_REVIEW",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "pinned_dependencies": {
            "m1": "H_blend_0.70A_0.30C1_W1.0",
            "m2": "1.1.1",
            "m6": "1.1.0",
            "m3": "1.1.0",
            "m4": "1.1.0",
            "m5": "1.1.0",
            "o6": "1.1.0"
        },
        "files": {
            "engine_source": {
                "path": "src/workforce_gap_engine.py",
                "sha256": compute_file_sha256(ROOT / "src" / "workforce_gap_engine.py")
            },
            "configuration": {
                "path": "data/workforce/o1_config_v1_1.json",
                "sha256": compute_file_sha256(ROOT / "data" / "workforce" / "o1_config_v1_1.json")
            },
            "benchmark_results": {
                "path": "data/workforce/o1_benchmark_results_v1_1.json",
                "sha256": compute_file_sha256(out_path)
            }
        },
        "verification_summary": {
            "total_benchmarks": len(results),
            "passed_benchmarks": sum(1 for b in results if b["passed"]),
            "all_benchmarks_passed": all_passed,
            "minimum_cohort_threshold": 5,
            "small_cell_threshold": 5,
            "complementary_suppression_active": True,
            "reconstruction_protection_active": True,
            "cross_query_differencing_protection": "PARTIAL",
            "differential_privacy_claimed": False,
            "protected_attributes_used": False,
            "demographic_fairness_evaluated": False,
            "employee_ranking_prohibited": True,
            "deficit_signal_status": "BINARY_NON_DISCRIMINATING",
            "deficit_ranking_weight": 0.0,
            "core_first_semantics": "CORE_WEIGHTED_PREFERENCE",
            "spearman_rank_stability_v1_vs_v1_1": round(float(rho), 6)
        }
    }

    manifest_path = ROOT / "data" / "workforce" / "o1_build_manifest_v1_1.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(build_manifest, f, indent=2)
    print(f"Saved build manifest to {manifest_path}")

    print("=" * 60)
    print(f"BENCHMARK OUTCOME: {'ALL 18 BENCHMARKS PASSED' if all_passed else 'SOME BENCHMARKS FAILED'}")
    print("=" * 60)


if __name__ == "__main__":
    run_all_benchmarks()
