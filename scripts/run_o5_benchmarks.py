"""
Benchmark Suite for O5 Responsible-AI & Invariance Governance Audit Layer
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

from src.governance_engine import GovernanceEngine


def run_benchmarks():
    print("=" * 65)
    print("O5 Responsible-AI & Invariance Governance Audit Layer v1.0.0 Benchmarks")
    print("=" * 65)

    engine = GovernanceEngine()
    results = {}
    all_passed = True

    # BM01: Freeze integrity verification
    print("\nRunning BM01: Upstream Freeze Integrity Verification...")
    freeze_ok, freeze_report = engine.verify_freeze_integrity()
    bm01_pass = freeze_ok and (freeze_report["modules_checked"] >= 9)
    results["BM01"] = {
        "title": "Upstream Freeze Integrity Verification",
        "passed": bm01_pass,
        "modules_checked": freeze_report["modules_checked"],
        "manifest_details": freeze_report["manifest_details"]
    }
    print(f"BM01 Outcome: {'PASSED' if bm01_pass else 'FAILED'} (Checked: {freeze_report['modules_checked']} modules)")
    all_passed = all_passed and bm01_pass

    # BM02: Clean dataset proxy exclusion
    print("\nRunning BM02: Clean Dataset Proxy Attribute Exclusion...")
    clean_sample = {
        "profile_id": "SYNTH_001",
        "skills": ["python", "machine_learning", "data_engineering"],
        "target_occupation": "2511",
        "weekly_hours": 8
    }
    is_clean, clean_viols = engine.audit_proxy_field_exclusion(clean_sample)
    bm02_pass = is_clean and (len(clean_viols) == 0)
    results["BM02"] = {
        "title": "Clean Dataset Proxy Attribute Exclusion",
        "passed": bm02_pass
    }
    print(f"BM02 Outcome: {'PASSED' if bm02_pass else 'FAILED'}")
    all_passed = all_passed and bm02_pass

    # BM03: Adversarial proxy detection
    print("\nRunning BM03: Adversarial Demographic Proxy Detection...")
    adversarial_sample = {
        "candidate": {
            "name": "Synthetic Candidate",
            "gender": "Female",
            "ethnicity": "Malay",
            "age": 29,
            "skills": ["python"]
        }
    }
    is_adv_clean, adv_viols = engine.audit_proxy_field_exclusion(adversarial_sample)
    bm03_pass = (not is_adv_clean) and (len(adv_viols) == 3)
    results["BM03"] = {
        "title": "Adversarial Demographic Proxy Detection",
        "passed": bm03_pass,
        "violations_detected": len(adv_viols)
    }
    print(f"BM03 Outcome: {'PASSED' if bm03_pass else 'FAILED'} (Caught {len(adv_viols)} violations)")
    all_passed = all_passed and bm03_pass

    # BM04: Counterfactual demographic invariance audit
    print("\nRunning BM04: Counterfactual Demographic Invariance Audit...")
    testbed_path = os.path.join("data", "governance", "synthetic_perturbation_testbed_v1.json")
    with open(testbed_path, "r", encoding="utf-8") as f:
        testbed = json.load(f)
    pairs = testbed.get("pairs", [])

    # Canonical evaluation function that strictly ignores demographics
    def sanitized_evaluator(p):
        skills_cnt = len(p.get("confirmed_skills", []))
        return {
            "career_readiness_score": round(skills_cnt * 25.0, 2),
            "target": p.get("target_occupation")
        }

    pair_results = []
    bm04_pass = True
    for p in pairs:
        p_ok, p_det = engine.run_counterfactual_invariance_test(
            p["base_profile"], p["perturbed_profile"], sanitized_evaluator
        )
        pair_results.append({"pair_id": p["pair_id"], "passed": p_ok})
        if not p_ok:
            bm04_pass = False

    results["BM04"] = {
        "title": "Counterfactual Demographic Invariance Audit",
        "passed": bm04_pass,
        "pairs_tested": len(pairs),
        "pair_results": pair_results
    }
    print(f"BM04 Outcome: {'PASSED' if bm04_pass else 'FAILED'} (Tested {len(pairs)} pairs)")
    all_passed = all_passed and bm04_pass

    # BM05: Counterfactual bias detection gate
    print("\nRunning BM05: Counterfactual Bias Detection Gate...")
    def biased_evaluator(p):
        penalty = 15.0 if "synthetic_injected_gender" in p else 0.0
        return {"score": 85.0 - penalty}

    bias_caught, bias_det = engine.run_counterfactual_invariance_test(
        pairs[0]["base_profile"], pairs[0]["perturbed_profile"], biased_evaluator
    )
    bm05_pass = (bias_caught is False) and (bias_det["violations_count"] > 0)
    results["BM05"] = {
        "title": "Counterfactual Bias Detection Gate",
        "passed": bm05_pass,
        "bias_detected_correctly": bm05_pass
    }
    print(f"BM05 Outcome: {'PASSED' if bm05_pass else 'FAILED'}")
    all_passed = all_passed and bm05_pass

    # BM06: Small-cell privacy clean verification
    print("\nRunning BM06: Small-Cell Privacy Clean Verification...")
    clean_k5_payload = {
        "cohort_summary": {
            "role_2512": {"profiles_count": 14, "suppressed": False},
            "role_2511": {"profiles_count": None, "display": "<5", "suppressed": True}
        }
    }
    k5_ok, k5_viols = engine.verify_small_cell_privacy(clean_k5_payload, min_k=5)
    bm06_pass = k5_ok and (len(k5_viols) == 0)
    results["BM06"] = {
        "title": "Small-Cell Privacy Clean Verification (k=5)",
        "passed": bm06_pass
    }
    print(f"BM06 Outcome: {'PASSED' if bm06_pass else 'FAILED'}")
    all_passed = all_passed and bm06_pass

    # BM07: Small-cell privacy leak detection gate
    print("\nRunning BM07: Small-Cell Privacy Leak Detection Gate...")
    leaky_k5_payload = {
        "cohort_summary": {
            "role_2512": {"profiles_count": 14},
            "role_2511": {"profiles_count": 2}  # Exposed raw count < 5!
        }
    }
    leak_ok, leak_viols = engine.verify_small_cell_privacy(leaky_k5_payload, min_k=5)
    bm07_pass = (not leak_ok) and (len(leak_viols) > 0)
    results["BM07"] = {
        "title": "Small-Cell Privacy Leak Detection Gate",
        "passed": bm07_pass,
        "leaks_caught": len(leak_viols)
    }
    print(f"BM07 Outcome: {'PASSED' if bm07_pass else 'FAILED'} (Caught {len(leak_viols)} leaks)")
    all_passed = all_passed and bm07_pass

    # BM08: Comprehensive audit ledger generation
    print("\nRunning BM08: Comprehensive Audit Ledger Generation...")
    ledger = engine.generate_comprehensive_audit_ledger()
    bm08_pass = (ledger["overall_governance_verdict"] == "APPROVED_RESPONSIBLE_AI_COMPLIANT")
    results["BM08"] = {
        "title": "Comprehensive Audit Ledger Generation",
        "passed": bm08_pass,
        "verdict": ledger["overall_governance_verdict"]
    }
    print(f"BM08 Outcome: {'PASSED' if bm08_pass else 'FAILED'} (Verdict: {ledger['overall_governance_verdict']})")
    all_passed = all_passed and bm08_pass

    print("\n" + "=" * 65)
    print(f"BENCHMARK SUMMARY: {'ALL 8 PASSED' if all_passed else 'SOME FAILED'}")
    print("=" * 65)

    # Save benchmark outputs
    out_dir = os.path.join("data", "governance")
    os.makedirs(out_dir, exist_ok=True)
    results_path = os.path.join(out_dir, "o5_benchmark_results_v1.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved benchmark results to {results_path}")

    # Build manifest
    manifest = {
        "engine": "O5 Responsible-AI & Invariance Governance Audit Layer",
        "version": "v1.0.0",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "BUILD_VERIFIED",
        "all_benchmarks_passed": all_passed,
        "total_benchmarks": 8,
        "passed_benchmarks": sum(1 for v in results.values() if v["passed"]),
        "files": {}
    }
    tracked_files = [
        "src/governance_engine.py",
        "data/governance/o5_config_v1.json",
        "data/governance/synthetic_perturbation_testbed_v1.json",
        "scripts/run_o5_benchmarks.py",
        "tests/test_governance_engine.py"
    ]
    for tf in tracked_files:
        if os.path.exists(tf):
            with open(tf, "rb") as fp:
                manifest["files"][tf] = hashlib.sha256(fp.read()).hexdigest()

    manifest_path = os.path.join(out_dir, "o5_build_manifest_v1.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Saved build manifest to {manifest_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_benchmarks())
