# O1 Version Changelog: v1.0.0 vs v1.1.0

**Reference Date:** 2026-10-24  

---

## Summary of Key Differences

| Dimension | O1 v1.0.0 | O1 v1.1.0 |
| :--- | :--- | :--- |
| **Shared Learning Threshold** | $N \ge 2$ (Disclosed counts 2–4) | $N \ge 5$ (Counts 1–4 suppressed) |
| **Role Transition Masking** | Exact volumes 1–4 published | Volumes 1–4 masked to `'<5'`, `null` |
| **Priority Skills Small Cell** | Exact affected count published | Masked to `null` and `'<5'` |
| **Priority Index Suppression** | Always published | Suppressed if subcell reconstructable |
| **Complementary Suppression** | Missing in role family partitions | Fully active (reusing frozen O6 logic) |
| **Heatmap Cell Privacy** | Prevalences published for small cells | Cell prevalence masked to `null` |
| **CORE Semantics** | Claimed 'structurally prioritised' | Rephrased to `CORE_WEIGHTED_PREFERENCE` |
| **Deficit Ranking Weight** | $0.15$ (non-discriminating) | $0.00$ (diagnostic only, renormalized) |
| **Automated Tests** | 43 unit tests | 65 unit tests (100% pass) |
| **Benchmark Suite** | 10 benchmarks | 18 benchmarks (100% pass) |
