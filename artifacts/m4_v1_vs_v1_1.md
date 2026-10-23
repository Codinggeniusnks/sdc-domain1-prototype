# M4 Architectural Comparison: v1.0.0 vs v1.1.0

**Reference Milestone**: Stage 12C Remediation Summary  
**Module**: M4 Personalised Reskilling Pathway Engine  
**Status**: COMPLETE & VERIFIED

---

## 1. Overview of Changes

M4 v1.1.0 represents a bounded, robust remediation of M4 v1.0.0. It resolves 1 P1 defect, 3 P2 defects, and 2 P3 defects identified during the independent Stage 12B methodology review, with zero changes to upstream frozen models (M1, M2 v1.1.1, M6 v1.1.0, M3 v1.1.0) and zero forward expansion into M5.

---

## 2. Side-by-Side Comparison Matrix

| Architectural Dimension | M4 Engine v1.0.0 | M4 Engine v1.1.0 | Remediation Rationale & Impact |
|:---|:---|:---|:---|
| **Pathway Evidence Confidence** | Fixed static score of `94.5` across all 8 personas. Heuristic blend lacking pathway sensitivity. | Dynamic aggregation across 4 dimensions: Gap Evidence (0.30), Prerequisite Quality (0.25), Resource Verification (0.25), Resource Freshness (0.20). Min=91.3, Max=93.6, Mean=92.54, Std=0.86. | **M4-P1-01 Resolved**. Eliminates static saturation. Accurately reflects variations in curriculum mapping, resource verification, and catalog age. |
| **Provider Taxonomy** | 27 raw, un-grouped provider strings (e.g., Coursera variants, Kaggle vs Google). | Dual-layer taxonomy: 27 raw `provider_display_name` strings mapped to 21 normalized `provider_group_id` parent institutions. | **M4-P2-01 Resolved**. Enables institutional diversity filtering and macro-level workforce analytics. |
| **Production Resource Catalog** | 38 resources total, including 2 synthetic benchmark fixtures (`RES_LOWCOST_01`, `RES_VAR_01`). | Exactly 36 verified live resources. 0 synthetic fixtures. Test fixtures relocated to `tests/fixtures/m4_resource_pricing_fixtures.json` (`test_only = true`). | **M4-P2-02 Resolved**. Strict separation of production data from test fixtures. Catalog truthfulness restored. |
| **Effort Multiplier Floor** | Hardcoded `0.50` floor buried in Python engine code. Rationale undocumented. | Config-driven (`min_multiplier_floor = 0.50`). Documented pedagogical rationale for fixed setup/assessment overhead. Proven invariant across 0.35, 0.50, and 0.65. | **M4-P2-03 Resolved**. Clean configuration decoupling and pedagogical grounding. |
| **Low-Cost Threshold & Disclaimer** | Implicit numeric threshold. No socioeconomic policy disclaimer. | Explicit config entry `low_cost_threshold_myr: 150.0`. Mandatory operational disclaimer attached to every pathway output. | **M4-P3-01 Resolved**. Prevents misinterpretation of "low cost" as a normative affordability claim. |
| **Weekly Study Hours Labeling** | Completion weeks presented without qualification, implying clinical prediction. | Benchmark schedules labeled `"TEST ASSUMPTION: 10 STUDY HOURS/WEEK"`. Live API requires explicit `hours_per_week` parameter. | **M4-P3-02 Resolved**. Eliminates misleading pacing expectations for working adult learners. |
| **Zero-Deficit Edge Case** | Could generate redundant steps if a worker was already fully qualified. | Explicit short-circuit returning `total_pathway_steps: 0`, 0 hours, and status `NO_RESKILLING_REQUIRED`. | Hardens edge-case handling for workers seeking lateral roles within their existing skill envelope. |
| **Resource Failure Fallback** | Hardcoded fallback strings. | Config-driven failure independence ensuring structural pathway validity even if external resources are temporarily offline. | Prevents API crashes when third-party course URLs or metadata are missing. |

---

## 3. Data File and Schema Evolution

```
data/reskilling/
├── [MODIFIED] learning_resources_v1_1.json      <- 36 live resources, 21 provider groups, 0 fixtures
├── [MODIFIED] m4_scoring_config_v1_1.json       <- Dynamic confidence weights, effort floor, cost policy
├── [MODIFIED] skill_prerequisites_v1_1.json     <- Formalized mapping confidence (0.90 - 0.98)
├── [NEW]      m4_benchmark_results_v1_1.json    <- Full benchmark results with dynamic confidence
└── [NEW]      m4_build_manifest_v1_1.json       <- Build SHA-256 integrity manifest

tests/fixtures/
└── [NEW]      m4_resource_pricing_fixtures.json <- Isolated synthetic test fixtures (test_only = true)
```

---

## 4. Contract Stability & Invariance

1. **M3 Interface**: M4 v1.1.0 consumes the exact frozen M3 Role Match payload (`masco_code`, `gaps`, `missing_core_skills`, `transition_distance`, `evidence_confidence_index`). Zero modifications to M3.
2. **Deterministic Reproducibility**: Given identical input profiles and scenario IDs, M4 v1.1.0 produces 100% byte-for-byte identical outputs across Python runs.
3. **Downstream Readiness**: Outputs provide clean, typed fields for future M5 SDG Impact consumption without speculative M5 dependencies.
