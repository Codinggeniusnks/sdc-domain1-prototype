"""
Benchmark Suite for O4 Learning Progress & Milestone Tracking Engine
Runs benchmarks BM01 through BM08 and saves execution manifests.
"""

import sys
import os
import json
import time
import hashlib

# Ensure UTF-8 output encoding for Windows compatibility
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.progress_engine import ProgressEngine


def run_benchmarks():
    print("=" * 65)
    print("O4 Learning Progress & Milestone Tracking Engine v1.0.0 Benchmarks")
    print("=" * 65)

    engine = ProgressEngine()
    results = {}
    all_passed = True

    sample_pathway = {
        "target_role": "2512",
        "milestones": [
            {"milestone_id": "M1", "title": "Programming Basics", "skills": ["python", "git"]},
            {"milestone_id": "M2", "title": "Data Structures", "skills": ["algorithms", "sql"]},
            {"milestone_id": "M3", "title": "Advanced Frameworks", "skills": ["fastapi", "docker"]}
        ]
    }

    # BM01: Initial progress ledger instantiation
    print("\nRunning BM01: Initial Progress Ledger Instantiation...")
    rec = engine.initialize_progress("BENCH_USER_001", sample_pathway)
    bm01_pass = (rec["profile_id"] == "BENCH_USER_001") and (rec["total_milestones"] == 3) and (rec["overall_completion_pct"] == 0.0)
    results["BM01"] = {
        "title": "Initial Progress Ledger Instantiation",
        "passed": bm01_pass,
        "total_milestones": rec["total_milestones"]
    }
    print(f"BM01 Outcome: {'PASSED' if bm01_pass else 'FAILED'}")
    all_passed = all_passed and bm01_pass

    # BM02: State transition lifecycle
    print("\nRunning BM02: Complete State Transition Lifecycle...")
    rec1, ok1, _ = engine.update_milestone_progress(rec, "M1", "IN_PROGRESS", 50.0)
    rec2, ok2, _ = engine.update_milestone_progress(rec1, "M1", "COMPLETED_SELF_REPORTED", 100.0)
    valid_ev = {
        "credential_id": "CERT-BM02-001",
        "issuer": "National Digital Academy",
        "issue_date": "2026-06-01",
        "sha256": "c" * 64
    }
    rec3, ok3, _ = engine.update_milestone_progress(
        rec2, "M1", "COMPLETED_VERIFIED", 100.0, evidence=valid_ev, verified_skills=["python", "git"]
    )
    rec4, ok4, _ = engine.update_milestone_progress(
        rec3, "M1", "SKILL_EVIDENCE_UPDATED", 100.0
    )
    bm02_pass = ok1 and ok2 and ok3 and ok4 and (rec4["milestones_progress"]["M1"]["status"] == "SKILL_EVIDENCE_UPDATED")
    results["BM02"] = {
        "title": "State Transition Lifecycle",
        "passed": bm02_pass,
        "final_status": rec4["milestones_progress"]["M1"]["status"]
    }
    print(f"BM02 Outcome: {'PASSED' if bm02_pass else 'FAILED'}")
    all_passed = all_passed and bm02_pass

    # BM03: Illegal state transition gate
    print("\nRunning BM03: Illegal State Transition Rejection...")
    fresh_rec = engine.initialize_progress("BENCH_USER_002", sample_pathway)
    _, bad_ok, bad_msg = engine.update_milestone_progress(fresh_rec, "M1", "SKILL_EVIDENCE_UPDATED", 100.0)
    bm03_pass = (bad_ok is False) and ("Illegal state transition" in bad_msg)
    results["BM03"] = {
        "title": "Illegal State Transition Rejection",
        "passed": bm03_pass,
        "rejection_message": bad_msg
    }
    print(f"BM03 Outcome: {'PASSED' if bm03_pass else 'FAILED'}")
    all_passed = all_passed and bm03_pass

    # BM04: Cryptographic credential evidence verification
    print("\nRunning BM04: Credential Evidence Verification...")
    good_ev = {"credential_id": "CR-01", "issuer": "MDEC", "issue_date": "2026-01-01", "sha256": "d" * 64}
    bad_sha = {"credential_id": "CR-01", "issuer": "MDEC", "issue_date": "2026-01-01", "sha256": "short-hash"}
    v_good, _ = engine.verify_credential_evidence(good_ev)
    v_bad, _ = engine.verify_credential_evidence(bad_sha)
    bm04_pass = v_good and (not v_bad)
    results["BM04"] = {
        "title": "Credential Evidence Verification",
        "passed": bm04_pass
    }
    print(f"BM04 Outcome: {'PASSED' if bm04_pass else 'FAILED'}")
    all_passed = all_passed and bm04_pass

    # BM05: Non-competitive recognition badges
    print("\nRunning BM05: Non-Competitive Recognition Badges...")
    badges = rec4.get("earned_badges", [])
    bm05_pass = ("FIRST_STEP_TAKEN" in badges) and ("VERIFIED_CREDENTIAL_EARNED" in badges)
    results["BM05"] = {
        "title": "Non-Competitive Recognition Badges",
        "passed": bm05_pass,
        "earned_badges": badges
    }
    print(f"BM05 Outcome: {'PASSED' if bm05_pass else 'FAILED'} (Badges: {badges})")
    all_passed = all_passed and bm05_pass

    # BM06: Verified skills delta production
    print("\nRunning BM06: Verified Skills Delta Production for O2...")
    delta = engine.generate_verified_skills_delta(rec4)
    bm06_pass = (delta["verified_skills_count"] == 2) and (delta["trigger_replan_event"] is True)
    results["BM06"] = {
        "title": "Verified Skills Delta for O2 Replanning",
        "passed": bm06_pass,
        "verified_skills": delta["verified_skills"]
    }
    print(f"BM06 Outcome: {'PASSED' if bm06_pass else 'FAILED'}")
    all_passed = all_passed and bm06_pass

    # BM07: Cohort progress aggregation under small-cell privacy (k=5)
    print("\nRunning BM07: Cohort Progress Aggregation Privacy (k=5)...")
    cohort = []
    for i in range(12):
        c_rec = engine.initialize_progress(f"USER_{i:03d}", sample_pathway)
        if i < 7:
            c_rec["milestones_progress"]["M1"]["completion_pct"] = 100.0
        if i < 4:
            c_rec["milestones_progress"]["M2"]["completion_pct"] = 100.0
        cohort.append(c_rec)
    agg = engine.aggregate_cohort_progress(cohort, min_k=5)
    # M1 has 7 completions (reportable), M2 has 4 completions (suppressed to '<5')
    bm07_pass = (agg["milestone_completion_rates"]["M1"]["completed_count"] == 7) and \
                (agg["milestone_completion_rates"]["M2"]["completed_count_display"] == "<5") and \
                (agg["milestone_completion_rates"]["M2"]["suppressed"] is True)
    results["BM07"] = {
        "title": "Cohort Progress Privacy Preservation (k=5)",
        "passed": bm07_pass,
        "m1_reportable_count": agg["milestone_completion_rates"]["M1"]["completed_count"],
        "m2_suppressed_display": agg["milestone_completion_rates"]["M2"]["completed_count_display"]
    }
    print(f"BM07 Outcome: {'PASSED' if bm07_pass else 'FAILED'}")
    all_passed = all_passed and bm07_pass

    # BM08: Responsible-AI employment disclaimer persistence
    print("\nRunning BM08: Responsible-AI Employment Disclaimer...")
    disc = engine.get_employment_disclaimer()
    bm08_pass = ("Official Notice" in disc) and ("does not constitute an automated guarantee" in disc)
    results["BM08"] = {
        "title": "Responsible-AI Employment Disclaimer Persistence",
        "passed": bm08_pass,
        "disclaimer_text": disc
    }
    print(f"BM08 Outcome: {'PASSED' if bm08_pass else 'FAILED'}")
    all_passed = all_passed and bm08_pass

    print("\n" + "=" * 65)
    print(f"BENCHMARK SUMMARY: {'ALL 8 PASSED' if all_passed else 'SOME FAILED'}")
    print("=" * 65)

    # Save benchmark outputs
    out_dir = os.path.join("data", "progress")
    os.makedirs(out_dir, exist_ok=True)
    results_path = os.path.join(out_dir, "o4_benchmark_results_v1.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved benchmark results to {results_path}")

    # Build manifest
    manifest = {
        "engine": "O4 Learning Progress & Milestone Tracking Engine",
        "version": "v1.0.0",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "BUILD_VERIFIED",
        "all_benchmarks_passed": all_passed,
        "total_benchmarks": 8,
        "passed_benchmarks": sum(1 for v in results.values() if v["passed"]),
        "files": {}
    }
    tracked_files = [
        "src/progress_engine.py",
        "data/progress/o4_config_v1.json",
        "data/progress/synthetic_learner_progress_v1.json",
        "scripts/run_o4_benchmarks.py",
        "tests/test_progress_engine.py"
    ]
    for tf in tracked_files:
        if os.path.exists(tf):
            with open(tf, "rb") as fp:
                manifest["files"][tf] = hashlib.sha256(fp.read()).hexdigest()

    manifest_path = os.path.join(out_dir, "o4_build_manifest_v1.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Saved build manifest to {manifest_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_benchmarks())
