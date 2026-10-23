"""
Benchmark Suite for O2 Automatic Replanning & Change Detection Engine v1.0.0
Runs 14 mandated benchmarks (BM01 - BM14) covering:
  - Identical state detection
  - Minor M2 trend score movement
  - Top-role re-ranking materiality
  - CORE gap additions and resolutions
  - IMPORTANT gap adjustments
  - Pathway step reordering
  - Scenario change attribution
  - Duplicate event rejection
  - Stale/out-of-order event rejection
  - Unsupported version handling
  - Privacy-safe diff transitions (4->5, 5->4, <5-><5)

Saves results to: data/replanning/o2_benchmark_results_v1.json
Saves build manifest to: data/replanning/o2_build_manifest_v1.json
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.replanning_engine import ReplanningEngine


def compute_file_sha256(path: Path) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_benchmarks():
    print("=" * 65)
    print("O2 Automatic Replanning & Change Detection Engine v1.0.0 Benchmarks")
    print("=" * 65)

    engine = ReplanningEngine()
    results = []

    # Load synthetic M2 snapshots
    with open(ROOT / "data" / "replanning" / "synthetic_m2_snapshots_v1.json", "r", encoding="utf-8") as f:
        m2_snaps = json.load(f)

    # Base profile fixtures
    base_profile = {
        "profile_id": "P_O2_BM_001",
        "skills": {
            "python_scripting": "USER_CONFIRMED",
            "data_visualization": "USER_CONFIRMED",
            "sql_data_analysis": "USER_CONFIRMED"
        }
    }

    # -------------------------------------------------------------
    # BM01: Identical State (No Semantic Change)
    # -------------------------------------------------------------
    print("\nRunning BM01: Identical state re-evaluation...")
    s1 = engine.build_state_snapshot(
        profile_snapshot=base_profile,
        m2_snapshot_id="M2_SNAP_BASELINE_2026Q1",
        m2_snapshot_data=m2_snaps["SNAPSHOT_A_BASELINE"],
        scenario_id="REFERENCE_2026",
        m3_output=[{"masco_code": "2511", "occupation_title": "Systems Analysts", "role_match_index": 82.5}],
        m4_output={"pathway_steps": [{"skill_id": "ai_literacy", "requirement_tier": "CORE"}], "total_estimated_hours_high": 120.0},
        state_id="STATE_BM01_PREV"
    )
    s2 = engine.build_state_snapshot(
        profile_snapshot=base_profile,
        m2_snapshot_id="M2_SNAP_BASELINE_2026Q1",
        m2_snapshot_data=m2_snaps["SNAPSHOT_A_BASELINE"],
        scenario_id="REFERENCE_2026",
        m3_output=[{"masco_code": "2511", "occupation_title": "Systems Analysts", "role_match_index": 82.5}],
        m4_output={"pathway_steps": [{"skill_id": "ai_literacy", "requirement_tier": "CORE"}], "total_estimated_hours_high": 120.0},
        state_id="STATE_BM01_NEW"
    )
    evt01 = {
        "event_id": "EVT_BM01_IDENTICAL",
        "trigger_type": "MANUAL_REPLAN_REQUESTED",
        "timestamp": "2026-10-24T05:00:00Z"
    }
    replan01 = engine.execute_candidate_replan(s1, evt01, s2)
    passed01 = (
        not replan01["state_changed"]
        and replan01["materiality"] == "NONE"
        and "NO_SEMANTIC_CHANGE" in replan01["quality_flags"]
        and replan01["publication_status"] == "CURRENT_ACCEPTED"
    )
    print(f"BM01 Outcome: {'PASSED' if passed01 else 'FAILED'} (Materiality: {replan01['materiality']})")
    results.append({
        "benchmark_id": "BM01_IDENTICAL_STATE",
        "description": "Validation that identical state produces NO_SEMANTIC_CHANGE and materiality NONE",
        "passed": passed01
    })

    # -------------------------------------------------------------
    # BM02: Minor M2 Change (Score Movement with Stable Ranks)
    # -------------------------------------------------------------
    print("\nRunning BM02: Minor M2 trend score movement...")
    s_m3_prev = [{"masco_code": "2511", "occupation_title": "Systems Analysts", "role_match_index": 82.5, "evidence_confidence_index": 80.0}]
    s_m3_new_minor = [{"masco_code": "2511", "occupation_title": "Systems Analysts", "role_match_index": 83.2, "evidence_confidence_index": 80.5}]
    
    s_prev_bm02 = engine.build_state_snapshot(
        profile_snapshot=base_profile,
        m2_snapshot_id="M2_SNAP_BASELINE_2026Q1",
        m2_snapshot_data=m2_snaps["SNAPSHOT_A_BASELINE"],
        m3_output=s_m3_prev,
        state_id="STATE_BM02_PREV"
    )
    s_new_bm02 = engine.build_state_snapshot(
        profile_snapshot=base_profile,
        m2_snapshot_id="M2_SNAP_MINOR_2026Q2",
        m2_snapshot_data=m2_snaps["SNAPSHOT_B_MINOR_CHANGE"],
        m3_output=s_m3_new_minor,
        state_id="STATE_BM02_NEW"
    )
    evt02 = {
        "event_id": "EVT_BM02_MINOR_M2",
        "trigger_type": "M2_TREND_SNAPSHOT_UPDATED",
        "timestamp": "2026-10-24T05:01:00Z"
    }
    replan02 = engine.execute_candidate_replan(s_prev_bm02, evt02, s_new_bm02)
    passed02 = (
        replan02["state_changed"]
        and replan02["materiality"] == "MINOR"
        and "MINOR_SCORE_MOVEMENT_ONLY" in replan02["quality_flags"]
        and replan02["publication_status"] == "CURRENT_ACCEPTED"
    )
    print(f"BM02 Outcome: {'PASSED' if passed02 else 'FAILED'} (Materiality: {replan02['materiality']})")
    results.append({
        "benchmark_id": "BM02_MINOR_M2_CHANGE",
        "description": "Validation that minor trend score movement with stable ranking yields MINOR materiality",
        "passed": passed02
    })

    # -------------------------------------------------------------
    # BM03: Top Role Change (Structural Material Shift)
    # -------------------------------------------------------------
    print("\nRunning BM03: Top recommended role change...")
    s_m3_prev_role = [
        {"masco_code": "2511", "occupation_title": "Systems Analysts", "role_match_index": 84.0},
        {"masco_code": "2529", "occupation_title": "Database & AI Engineers", "role_match_index": 81.0}
    ]
    s_m3_new_role = [
        {"masco_code": "2529", "occupation_title": "Database & AI Engineers", "role_match_index": 92.5},
        {"masco_code": "2511", "occupation_title": "Systems Analysts", "role_match_index": 79.0}
    ]
    s_prev_bm03 = engine.build_state_snapshot(
        profile_snapshot=base_profile,
        m2_snapshot_id="M2_SNAP_BASELINE_2026Q1",
        m2_snapshot_data=m2_snaps["SNAPSHOT_A_BASELINE"],
        m3_output=s_m3_prev_role,
        state_id="STATE_BM03_PREV"
    )
    s_new_bm03 = engine.build_state_snapshot(
        profile_snapshot=base_profile,
        m2_snapshot_id="M2_SNAP_MATERIAL_2026Q3",
        m2_snapshot_data=m2_snaps["SNAPSHOT_C_MATERIAL_TREND_CHANGE"],
        m3_output=s_m3_new_role,
        state_id="STATE_BM03_NEW"
    )
    evt03 = {
        "event_id": "EVT_BM03_TOP_ROLE",
        "trigger_type": "M2_TREND_SNAPSHOT_UPDATED",
        "timestamp": "2026-10-24T05:02:00Z"
    }
    replan03 = engine.execute_candidate_replan(s_prev_bm03, evt03, s_new_bm03)
    passed03 = (
        replan03["materiality"] == "HIGH_MATERIALITY"
        and replan03["changes"]["M3"]["top_recommended_role_changed"]
        and replan03["publication_status"] == "CANDIDATE_REQUIRES_ACKNOWLEDGEMENT"
        and "MATERIAL_ROLE_CHANGE" in replan03["quality_flags"]
    )
    print(f"BM03 Outcome: {'PASSED' if passed03 else 'FAILED'} (Materiality: {replan03['materiality']}, PubStatus: {replan03['publication_status']})")
    results.append({
        "benchmark_id": "BM03_TOP_ROLE_CHANGE",
        "description": "Validation that top recommended role change triggers HIGH_MATERIALITY and requires acknowledgement",
        "passed": passed03
    })

    # -------------------------------------------------------------
    # BM04: CORE Gap Added
    # -------------------------------------------------------------
    print("\nRunning BM04: CORE skill gap added...")
    m4_prev_core = {"pathway_steps": [{"skill_id": "sql_data_analysis", "requirement_tier": "CORE"}]}
    m4_new_core = {"pathway_steps": [
        {"skill_id": "sql_data_analysis", "requirement_tier": "CORE"},
        {"skill_id": "ai_literacy", "requirement_tier": "CORE"}
    ]}
    s_prev_bm04 = engine.build_state_snapshot(profile_snapshot=base_profile, m4_output=m4_prev_core, state_id="STATE_BM04_PREV")
    s_new_bm04 = engine.build_state_snapshot(profile_snapshot=base_profile, m4_output=m4_new_core, state_id="STATE_BM04_NEW")
    evt04 = {"event_id": "EVT_BM04_CORE_ADDED", "trigger_type": "PROFILE_SKILL_STATE_UPDATED", "timestamp": "2026-10-24T05:03:00Z"}
    replan04 = engine.execute_candidate_replan(s_prev_bm04, evt04, s_new_bm04)
    passed04 = (
        replan04["materiality"] == "HIGH_MATERIALITY"
        and "ai_literacy" in replan04["changes"]["M4"]["core_gaps_added"]
        and replan04["publication_status"] == "CANDIDATE_REQUIRES_ACKNOWLEDGEMENT"
    )
    print(f"BM04 Outcome: {'PASSED' if passed04 else 'FAILED'} (Materiality: {replan04['materiality']}, Added: {replan04['changes']['M4']['core_gaps_added']})")
    results.append({
        "benchmark_id": "BM04_CORE_GAP_ADDED",
        "description": "Validation that newly identified CORE gap triggers HIGH_MATERIALITY",
        "passed": passed04
    })

    # -------------------------------------------------------------
    # BM05: CORE Gap Resolved
    # -------------------------------------------------------------
    print("\nRunning BM05: CORE skill gap resolved...")
    s_prev_bm05 = engine.build_state_snapshot(profile_snapshot=base_profile, m4_output=m4_new_core, state_id="STATE_BM05_PREV")
    s_new_bm05 = engine.build_state_snapshot(profile_snapshot=base_profile, m4_output=m4_prev_core, state_id="STATE_BM05_NEW")
    evt05 = {"event_id": "EVT_BM05_CORE_RESOLVED", "trigger_type": "PROFILE_SKILL_STATE_UPDATED", "timestamp": "2026-10-24T05:04:00Z"}
    replan05 = engine.execute_candidate_replan(s_prev_bm05, evt05, s_new_bm05)
    passed05 = (
        replan05["materiality"] == "HIGH_MATERIALITY"
        and "ai_literacy" in replan05["changes"]["M4"]["core_gaps_removed"]
    )
    print(f"BM05 Outcome: {'PASSED' if passed05 else 'FAILED'} (Materiality: {replan05['materiality']}, Removed: {replan05['changes']['M4']['core_gaps_removed']})")
    results.append({
        "benchmark_id": "BM05_CORE_GAP_RESOLVED",
        "description": "Validation that resolving a CORE gap triggers HIGH_MATERIALITY",
        "passed": passed05
    })

    # -------------------------------------------------------------
    # BM06: IMPORTANT Gap Change
    # -------------------------------------------------------------
    print("\nRunning BM06: IMPORTANT skill gap change...")
    m4_prev_imp = {"pathway_steps": [
        {"skill_id": "sql_data_analysis", "requirement_tier": "CORE"},
        {"skill_id": "data_visualization", "requirement_tier": "IMPORTANT"}
    ]}
    m4_new_imp = {"pathway_steps": [
        {"skill_id": "sql_data_analysis", "requirement_tier": "CORE"},
        {"skill_id": "workflow_automation", "requirement_tier": "IMPORTANT"}
    ]}
    s_prev_bm06 = engine.build_state_snapshot(profile_snapshot=base_profile, m4_output=m4_prev_imp, state_id="STATE_BM06_PREV")
    s_new_bm06 = engine.build_state_snapshot(profile_snapshot=base_profile, m4_output=m4_new_imp, state_id="STATE_BM06_NEW")
    evt06 = {"event_id": "EVT_BM06_IMP_GAP", "trigger_type": "PROFILE_SKILL_STATE_UPDATED", "timestamp": "2026-10-24T05:05:00Z"}
    replan06 = engine.execute_candidate_replan(s_prev_bm06, evt06, s_new_bm06)
    passed06 = (
        replan06["materiality"] == "MATERIAL"
        and "workflow_automation" in replan06["changes"]["M4"]["important_gaps_added"]
        and "data_visualization" in replan06["changes"]["M4"]["important_gaps_removed"]
    )
    print(f"BM06 Outcome: {'PASSED' if passed06 else 'FAILED'} (Materiality: {replan06['materiality']})")
    results.append({
        "benchmark_id": "BM06_IMPORTANT_GAP_CHANGE",
        "description": "Validation that changes to IMPORTANT gaps produce MATERIAL classification",
        "passed": passed06
    })

    # -------------------------------------------------------------
    # BM07: Pathway Order Change
    # -------------------------------------------------------------
    print("\nRunning BM07: Pathway step ordering change...")
    m4_order_a = {"pathway_steps": [
        {"skill_id": "sql_data_analysis", "requirement_tier": "CORE"},
        {"skill_id": "python_scripting", "requirement_tier": "CORE"}
    ]}
    m4_order_b = {"pathway_steps": [
        {"skill_id": "python_scripting", "requirement_tier": "CORE"},
        {"skill_id": "sql_data_analysis", "requirement_tier": "CORE"}
    ]}
    s_prev_bm07 = engine.build_state_snapshot(profile_snapshot=base_profile, m4_output=m4_order_a, state_id="STATE_BM07_PREV")
    s_new_bm07 = engine.build_state_snapshot(profile_snapshot=base_profile, m4_output=m4_order_b, state_id="STATE_BM07_NEW")
    evt07 = {"event_id": "EVT_BM07_PATHWAY_ORDER", "trigger_type": "PROFILE_SKILL_STATE_UPDATED", "timestamp": "2026-10-24T05:06:00Z"}
    replan07 = engine.execute_candidate_replan(s_prev_bm07, evt07, s_new_bm07)
    passed07 = (
        replan07["materiality"] == "MATERIAL"
        and replan07["changes"]["M4"]["pathway_order_changed"]
    )
    print(f"BM07 Outcome: {'PASSED' if passed07 else 'FAILED'} (Materiality: {replan07['materiality']}, OrderChanged: {replan07['changes']['M4']['pathway_order_changed']})")
    results.append({
        "benchmark_id": "BM07_PATHWAY_ORDER_CHANGE",
        "description": "Validation that reordering pathway steps triggers MATERIAL classification",
        "passed": passed07
    })

    # -------------------------------------------------------------
    # BM08: Scenario Change
    # -------------------------------------------------------------
    print("\nRunning BM08: Scenario change attribution...")
    s_prev_bm08 = engine.build_state_snapshot(profile_snapshot=base_profile, scenario_id="REFERENCE_2026", state_id="STATE_BM08_PREV")
    s_new_bm08 = engine.build_state_snapshot(profile_snapshot=base_profile, scenario_id="FAST_AGENTIC", state_id="STATE_BM08_NEW")
    evt08 = {"event_id": "EVT_BM08_SCENARIO", "trigger_type": "M6_SCENARIO_CHANGED", "timestamp": "2026-10-24T05:07:00Z"}
    replan08 = engine.execute_candidate_replan(s_prev_bm08, evt08, s_new_bm08)
    passed08 = (
        "SCENARIO_CHANGE" in replan08["root_causes"]
        and "SCENARIO_ASSUMPTION_CHANGE" in replan08["quality_flags"]
        and "M6_SCENARIO" in replan08["explanation"]["summary_narrative"] or "scenario" in replan08["explanation"]["summary_narrative"].lower()
    )
    print(f"BM08 Outcome: {'PASSED' if passed08 else 'FAILED'} (RootCauses: {replan08['root_causes']})")
    results.append({
        "benchmark_id": "BM08_SCENARIO_CHANGE",
        "description": "Validation that scenario change is correctly attributed without implying labor market shifted",
        "passed": passed08
    })

    # -------------------------------------------------------------
    # BM09: Duplicate Event Rejection
    # -------------------------------------------------------------
    print("\nRunning BM09: Duplicate event handling...")
    evt09 = {"event_id": "EVT_BM09_DUP_TEST", "trigger_type": "MANUAL_REPLAN_REQUESTED", "timestamp": "2026-10-24T05:08:00Z"}
    r1 = engine.execute_candidate_replan(s1, evt09, s2)
    r2 = engine.execute_candidate_replan(s1, evt09, s2)
    passed09 = (
        r2["publication_status"] == "DUPLICATE_EVENT"
        and "DUPLICATE_EVENT" in r2["quality_flags"]
        and r2["rollback_reference"] == s1["state_id"]
    )
    print(f"BM09 Outcome: {'PASSED' if passed09 else 'FAILED'} (Second PubStatus: {r2['publication_status']})")
    results.append({
        "benchmark_id": "BM09_DUPLICATE_EVENT",
        "description": "Validation that duplicate event ID is rejected and does not mutate state",
        "passed": passed09
    })

    # -------------------------------------------------------------
    # BM10: Stale Event Rejection
    # -------------------------------------------------------------
    print("\nRunning BM10: Stale event handling...")
    evt10 = {"event_id": "EVT_BM10_STALE", "trigger_type": "MANUAL_REPLAN_REQUESTED", "timestamp": "2024-01-01T00:00:00Z"}
    replan10 = engine.execute_candidate_replan(s1, evt10, s2)
    passed10 = (
        replan10["publication_status"] == "STALE_EVENT"
        and "STALE_EVENT" in replan10["quality_flags"]
    )
    print(f"BM10 Outcome: {'PASSED' if passed10 else 'FAILED'} (PubStatus: {replan10['publication_status']})")
    results.append({
        "benchmark_id": "BM10_STALE_EVENT",
        "description": "Validation that stale event with older timestamp is rejected",
        "passed": passed10
    })

    # -------------------------------------------------------------
    # BM11: Unsupported Upstream Version
    # -------------------------------------------------------------
    print("\nRunning BM11: Unsupported upstream version rejection...")
    evt11 = {
        "event_id": "EVT_BM11_UNSUPPORTED",
        "trigger_type": "M2_TREND_SNAPSHOT_UPDATED",
        "source_versions": {"M2": "2.0.0"},
        "timestamp": "2026-10-24T05:09:00Z"
    }
    replan11 = engine.execute_candidate_replan(s1, evt11, s2)
    passed11 = (
        replan11["publication_status"] == "UNSUPPORTED_UPSTREAM_VERSION"
        and "UNSUPPORTED_UPSTREAM_VERSION" in replan11["quality_flags"]
    )
    print(f"BM11 Outcome: {'PASSED' if passed11 else 'FAILED'} (PubStatus: {replan11['publication_status']})")
    results.append({
        "benchmark_id": "BM11_UNSUPPORTED_VERSION",
        "description": "Validation that unsupported upstream version triggers immediate rejection",
        "passed": passed11
    })

    # -------------------------------------------------------------
    # BM12: Privacy Diff: Small Cell 4 to 5
    # -------------------------------------------------------------
    print("\nRunning BM12: Small cell transition 4 -> 5...")
    msg12 = engine.build_privacy_safe_diff(prev_val="<5", new_val="5", prev_count=4, new_count=5)
    passed12 = (
        msg12 == "Previously suppressed; now above reporting threshold."
        and "4" not in msg12
    )
    print(f"BM12 Outcome: {'PASSED' if passed12 else 'FAILED'} (Diff: '{msg12}')")
    results.append({
        "benchmark_id": "BM12_SMALL_CELL_4_TO_5",
        "description": "Validation of privacy-safe transition when small cell crosses 4 to 5",
        "passed": passed12,
        "diff_message": msg12
    })

    # -------------------------------------------------------------
    # BM13: Privacy Diff: Small Cell 5 to 4
    # -------------------------------------------------------------
    print("\nRunning BM13: Small cell transition 5 -> 4...")
    msg13 = engine.build_privacy_safe_diff(prev_val="5", new_val="<5", prev_count=5, new_count=4)
    passed13 = (
        msg13 == "Previously reportable; now below reporting threshold."
        and "4" not in msg13
    )
    print(f"BM13 Outcome: {'PASSED' if passed13 else 'FAILED'} (Diff: '{msg13}')")
    results.append({
        "benchmark_id": "BM13_SMALL_CELL_5_TO_4",
        "description": "Validation of privacy-safe transition when cell drops below threshold from 5 to 4",
        "passed": passed13,
        "diff_message": msg13
    })

    # -------------------------------------------------------------
    # BM14: Privacy Diff: Suppressed to Suppressed
    # -------------------------------------------------------------
    print("\nRunning BM14: Suppressed to suppressed...")
    msg14 = engine.build_privacy_safe_diff(prev_val="<5", new_val="<5", prev_count=2, new_count=3)
    passed14 = (
        msg14 == "SUPPRESSED → SUPPRESSED"
    )
    print(f"BM14 Outcome: {'PASSED' if passed14 else 'FAILED'} (Diff: '{msg14}')")
    results.append({
        "benchmark_id": "BM14_SUPPRESSED_TO_SUPPRESSED",
        "description": "Validation of privacy-safe transition between two small counts (<5 to <5)",
        "passed": passed14,
        "diff_message": msg14
    })

    # -------------------------------------------------------------
    # Summary & Manifest Generation
    # -------------------------------------------------------------
    all_passed = all(r["passed"] for r in results)
    print("\n" + "=" * 65)
    print(f"BENCHMARK SUMMARY: {'ALL 14 PASSED' if all_passed else 'FAILURES DETECTED'}")
    print("=" * 65)

    benchmark_summary = {
        "engine_name": "O2 Automatic Replanning & Change Detection Engine",
        "engine_version": "1.0.0",
        "execution_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_benchmarks": len(results),
        "passed_benchmarks": sum(1 for r in results if r["passed"]),
        "all_passed": all_passed,
        "results": results
    }

    out_bench_path = ROOT / "data" / "replanning" / "o2_benchmark_results_v1.json"
    with open(out_bench_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_summary, f, indent=2)
    print(f"Saved benchmark results to {out_bench_path}")

    # Build manifest
    build_manifest = {
        "engine_name": "O2 Automatic Replanning & Change Detection Engine",
        "engine_version": "1.0.0",
        "status": "STAGE_16A_CANDIDATE_READY_FOR_METHODOLOGY_REVIEW",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "files": {
            "engine_source": {
                "path": "src/replanning_engine.py",
                "sha256": compute_file_sha256(ROOT / "src" / "replanning_engine.py")
            },
            "configuration": {
                "path": "data/replanning/o2_config_v1.json",
                "sha256": compute_file_sha256(ROOT / "data" / "replanning" / "o2_config_v1.json")
            },
            "synthetic_m2_snapshots": {
                "path": "data/replanning/synthetic_m2_snapshots_v1.json",
                "sha256": compute_file_sha256(ROOT / "data" / "replanning" / "synthetic_m2_snapshots_v1.json")
            },
            "synthetic_replan_events": {
                "path": "data/replanning/synthetic_replan_events_v1.json",
                "sha256": compute_file_sha256(ROOT / "data" / "replanning" / "synthetic_replan_events_v1.json")
            },
            "benchmark_results": {
                "path": "data/replanning/o2_benchmark_results_v1.json",
                "sha256": compute_file_sha256(out_bench_path)
            }
        },
        "pinned_upstream_baseline": engine.PINNED_VERSIONS,
        "verification_summary": {
            "benchmarks_passed": f"{sum(1 for r in results if r['passed'])}/{len(results)}"
        }
    }

    out_man_path = ROOT / "data" / "replanning" / "o2_build_manifest_v1.json"
    with open(out_man_path, "w", encoding="utf-8") as f:
        json.dump(build_manifest, f, indent=2)
    print(f"Saved build manifest to {out_man_path}")

    return all_passed


if __name__ == "__main__":
    success = run_benchmarks()
    if not success:
        exit(1)
