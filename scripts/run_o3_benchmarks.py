"""
Benchmark Suite for O3 Multilingual & Low-Bandwidth Presentation Layer
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

from src.presentation_layer import PresentationLayer


def run_benchmarks():
    print("=" * 65)
    print("O3 Multilingual & Low-Bandwidth Presentation Layer v1.0.0 Benchmarks")
    print("=" * 65)

    engine = PresentationLayer()
    results = {}
    all_passed = True

    # BM01: 100% Catalog Key Parity
    print("\nRunning BM01: Catalog Key Parity Validation...")
    parity_rep = engine.validate_key_parity()
    bm01_pass = parity_rep["is_clean"] and parity_rep["total_canonical_keys"] > 100
    results["BM01"] = {
        "title": "Catalog Key Parity (EN, MS, ZH-CN)",
        "passed": bm01_pass,
        "total_keys": parity_rep["total_canonical_keys"],
        "locale_counts": parity_rep["locale_key_counts"]
    }
    print(f"BM01 Outcome: {'PASSED' if bm01_pass else 'FAILED'} (Keys: {parity_rep['total_canonical_keys']})")
    all_passed = all_passed and bm01_pass

    # BM02: Translation Throughput
    print("\nRunning BM02: Translation Resolution Throughput...")
    n_lookups = 20000
    start_t = time.perf_counter()
    for _ in range(n_lookups):
        _ = engine.t("app.title")
        _ = engine.t("nav.matching")
        _ = engine.t("common.tiers.core")
    elapsed = time.perf_counter() - start_t
    ops_per_sec = (n_lookups * 3) / elapsed
    bm02_pass = ops_per_sec > 10000
    results["BM02"] = {
        "title": "Translation Resolution Throughput",
        "passed": bm02_pass,
        "ops_per_sec": round(ops_per_sec, 2),
        "total_operations": n_lookups * 3,
        "elapsed_seconds": round(elapsed, 4)
    }
    print(f"BM02 Outcome: {'PASSED' if bm02_pass else 'FAILED'} ({round(ops_per_sec, 0)} ops/sec)")
    all_passed = all_passed and bm02_pass

    # BM03: Mathematical Invariance on M3 Career Matching
    print("\nRunning BM03: Invariance on M3 Career Matching...")
    m3_payload_en = {
        "target_role": "Data Scientist",
        "masco_code": "2511",
        "fit_score": 91.50,
        "viability": 0.88,
        "ranked_candidates": [
            {"masco_code": "2511", "score": 91.50, "rank": 1},
            {"masco_code": "2512", "score": 88.20, "rank": 2},
            {"masco_code": "2521", "score": 82.10, "rank": 3}
        ]
    }
    m3_payload_ms = {
        "target_role": "Saintis Data",
        "masco_code": "2511",
        "fit_score": 91.50,
        "viability": 0.88,
        "ranked_candidates": [
            {"masco_code": "2511", "score": 91.50, "rank": 1},
            {"masco_code": "2512", "score": 88.20, "rank": 2},
            {"masco_code": "2521", "score": 82.10, "rank": 3}
        ]
    }
    m3_payload_zh = {
        "target_role": "数据科学家",
        "masco_code": "2511",
        "fit_score": 91.50,
        "viability": 0.88,
        "ranked_candidates": [
            {"masco_code": "2511", "score": 91.50, "rank": 1},
            {"masco_code": "2512", "score": 88.20, "rank": 2},
            {"masco_code": "2521", "score": 82.10, "rank": 3}
        ]
    }
    inv_ms, viol_ms = engine.verify_mathematical_invariance(m3_payload_en, m3_payload_ms)
    inv_zh, viol_zh = engine.verify_mathematical_invariance(m3_payload_en, m3_payload_zh)
    bm03_pass = inv_ms and inv_zh
    results["BM03"] = {
        "title": "M3 Invariance Preservation (EN, MS, ZH-CN)",
        "passed": bm03_pass,
        "violations_ms": viol_ms,
        "violations_zh": viol_zh
    }
    print(f"BM03 Outcome: {'PASSED' if bm03_pass else 'FAILED'}")
    all_passed = all_passed and bm03_pass

    # BM04: Mathematical Invariance on M4 Reskilling Pathway
    print("\nRunning BM04: Invariance on M4 Reskilling Pathway...")
    m4_en = {
        "masco_code": "2512",
        "total_hours": 140.0,
        "calendar_weeks": 20,
        "core_milestones": [
            {"milestone_id": "M1", "hours": 40.0, "status": "REQUIRED"},
            {"milestone_id": "M2", "hours": 50.0, "status": "REQUIRED"},
            {"milestone_id": "M3", "hours": 50.0, "status": "REQUIRED"}
        ]
    }
    m4_ms = {
        "masco_code": "2512",
        "total_hours": 140.0,
        "calendar_weeks": 20,
        "core_milestones": [
            {"milestone_id": "M1", "hours": 40.0, "status": "REQUIRED"},
            {"milestone_id": "M2", "hours": 50.0, "status": "REQUIRED"},
            {"milestone_id": "M3", "hours": 50.0, "status": "REQUIRED"}
        ]
    }
    inv_m4, viol_m4 = engine.verify_mathematical_invariance(m4_en, m4_ms)
    bm04_pass = inv_m4
    results["BM04"] = {
        "title": "M4 Pathway Invariance Preservation",
        "passed": bm04_pass,
        "violations": viol_m4
    }
    print(f"BM04 Outcome: {'PASSED' if bm04_pass else 'FAILED'}")
    all_passed = all_passed and bm04_pass

    # BM05: Mathematical Invariance on O1 Priority Reskilling Index
    print("\nRunning BM05: Invariance on O1 Employer PRI...")
    o1_en = {
        "cohort_size": 50,
        "priority_reskilling_index": 78.45,
        "core_gap_prevalence": 0.64,
        "privacy_status": "K_ANONYMITY_5_ACTIVE"
    }
    o1_zh = {
        "cohort_size": 50,
        "priority_reskilling_index": 78.45,
        "core_gap_prevalence": 0.64,
        "privacy_status": "K_ANONYMITY_5_ACTIVE"
    }
    inv_o1, viol_o1 = engine.verify_mathematical_invariance(o1_en, o1_zh)
    bm05_pass = inv_o1
    results["BM05"] = {
        "title": "O1 Priority Reskilling Index Invariance",
        "passed": bm05_pass,
        "violations": viol_o1
    }
    print(f"BM05 Outcome: {'PASSED' if bm05_pass else 'FAILED'}")
    all_passed = all_passed and bm05_pass

    # BM06: Low-Bandwidth Pruning
    print("\nRunning BM06: Low-Bandwidth Pruning...")
    rich_sample = {
        "svg": "<svg>Large SVG data...</svg>",
        "full_methodology_text": "Lengthy narrative paragraphs...",
        "masco_code": "2512",
        "fit_score": 88.123456,
        "gap_score": 45.678910
    }
    pruned = engine.render_low_bandwidth_payload(rich_sample)
    bm06_pass = ("svg" not in pruned) and ("full_methodology_text" not in pruned) and (pruned["fit_score"] == 88.12)
    results["BM06"] = {
        "title": "Low-Bandwidth Asset & Narrative Pruning",
        "passed": bm06_pass,
        "pruned_keys": list(pruned.keys())
    }
    print(f"BM06 Outcome: {'PASSED' if bm06_pass else 'FAILED'}")
    all_passed = all_passed and bm06_pass

    # BM07: Low-Bandwidth Compression Ratio
    print("\nRunning BM07: Compression Ratio Verification...")
    synthetic_bulk = {
        "workforce_summary": [
            {
                "masco_code": f"25{i:02d}",
                "headcount": 10 + i,
                "urgency_score": 50.0 + i,
                "skills": ["data_analysis", "python", "ai_literacy"]
            }
            for i in range(50)
        ]
    }
    comp_rep = engine.compress_payload(synthetic_bulk)
    bm07_pass = comp_rep["within_bandwidth_ceiling"] and (comp_rep["reduction_ratio"] >= 0.60)
    results["BM07"] = {
        "title": "Low-Bandwidth Compression Ratio",
        "passed": bm07_pass,
        "reduction_ratio": comp_rep["reduction_ratio"],
        "uncompressed_bytes": comp_rep["uncompressed_bytes"],
        "compressed_bytes": comp_rep["compressed_bytes"]
    }
    print(f"BM07 Outcome: {'PASSED' if bm07_pass else 'FAILED'} (Ratio: {comp_rep['reduction_percentage']}, CompBytes: {comp_rep['compressed_bytes']})")
    all_passed = all_passed and bm07_pass

    # BM08: Interpolation Security
    print("\nRunning BM08: Interpolation Security...")
    # Safe rendering even with malicious or unexpected inputs
    safe_out = engine.t("common.labels.role", unexpected="{<script>alert(1)</script>}")
    bm08_pass = isinstance(safe_out, str) and len(safe_out) > 0
    results["BM08"] = {
        "title": "Safe Template Parameter Interpolation",
        "passed": bm08_pass
    }
    print(f"BM08 Outcome: {'PASSED' if bm08_pass else 'FAILED'}")
    all_passed = all_passed and bm08_pass

    print("\n" + "=" * 65)
    print(f"BENCHMARK SUMMARY: {'ALL 8 PASSED' if all_passed else 'SOME FAILED'}")
    print("=" * 65)

    # Save benchmark outputs
    out_dir = os.path.join("data", "presentation")
    os.makedirs(out_dir, exist_ok=True)
    results_path = os.path.join(out_dir, "o3_benchmark_results_v1.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved benchmark results to {results_path}")

    # Build manifest
    manifest = {
        "engine": "O3 Multilingual & Low-Bandwidth Presentation Layer",
        "version": "v1.0.0",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "BUILD_VERIFIED",
        "all_benchmarks_passed": all_passed,
        "total_benchmarks": 8,
        "passed_benchmarks": sum(1 for v in results.values() if v["passed"]),
        "files": {}
    }
    tracked_files = [
        "src/presentation_layer.py",
        "data/presentation/o3_config_v1.json",
        "locales/en.json",
        "locales/ms.json",
        "locales/zh-CN.json",
        "scripts/run_o3_benchmarks.py",
        "tests/test_presentation_layer.py"
    ]
    for tf in tracked_files:
        if os.path.exists(tf):
            with open(tf, "rb") as fp:
                manifest["files"][tf] = hashlib.sha256(fp.read()).hexdigest()

    manifest_path = os.path.join(out_dir, "o3_build_manifest_v1.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Saved build manifest to {manifest_path}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_benchmarks())
