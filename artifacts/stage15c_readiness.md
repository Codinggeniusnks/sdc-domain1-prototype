# Stage 15C Readiness & Remediation Specification: O1 v1.1.0

**Module:** O1 Employer / HR Workforce Planning Layer  
**Audit Source:** Stage 15B Independent Methodology Review  
**Date:** 2026-10-24  
**Target Candidate:** O1 Employer Workforce Gap & Cohort Reskilling Engine v1.1.0  

---

## 1. Remediation Backlog & Action Items

| Defect ID | Severity | Target File / Module | Action Item Description |
| :---: | :---: | :--- | :--- |
| **P1-01** | **P1** | `src/workforce_gap_engine.py` | Enforce $k=5$ threshold or mask counts (`"<5"`) in `identify_shared_learning_opportunities`. |
| **P1-02** | **P1** | `src/workforce_gap_engine.py` | Apply small-cell count masking (`transition_volume_display: "<5"`) in `build_role_gap_summary`. |
| **P1-03** | **P1** | `src/workforce_gap_engine.py` | Mask `affected_profile_count` to `"<5"` in `rank_workforce_reskilling_priorities` when $0 < N < 5$. |
| **P2-01** | **P2** | `artifacts/o1_*methodology.md` | Rephrase CORE-first documentation: state "weighted preference only", strike "structural guarantee". |
| **P2-02** | **P2** | `data/aggregation/` | Enhance synthetic benchmark with fractional proficiency to demonstrate continuous deficit variance. |
| **P2-03** | **P2** | `src/workforce_gap_engine.py` | Port O6 complementary suppression to role-family and partition analytics. |
| **P2-04** | **P2** | `src/workforce_gap_engine.py` | Add `SMALL_CELL_ESTIMATE` flag and prevalence masking to heatmap cells where gapped count $< 5$. |
| **P3-01** | **P3** | `tests/test_workforce_gap_engine.py` | Add unit tests for small-cell privacy, counterexamples, weight sensitivity, and fractional deficits. |
| **P3-02** | **P3** | `artifacts/o1_workforce_gap_methodology.md` | Add explicit disclaimers: role transition pressure $\ne$ employee displacement probability. |
| **P3-03** | **P3** | `artifacts/o1_cohort_reskilling_methodology.md` | Emphasize calendar duration vs aggregate learner-hours distinction in scheduling guidelines. |

---

## 2. Non-Negotiable Invariants for Stage 15C

1. **Frozen Upstream Models:** Do NOT modify M1, M2 v1.1.1, M6 v1.1.0, M3 v1.1.0, M4 v1.1.0, M5 v1.1.0, or O6 v1.1.0.
2. **Zero Employee Ranking:** Maintain absolute prohibition of individual worker performance scoring or ranking.
3. **No UI Building:** Do not construct frontend web components or dashboards in Stage 15C.
4. **Deterministic Versioning:** Bump candidate version to `O1 Employer Workforce Gap Engine v1.1.0`.
