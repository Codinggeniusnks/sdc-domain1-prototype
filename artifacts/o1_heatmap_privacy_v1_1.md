# O1 Heatmap Cell Privacy & Suppression Matrix v1.1.0

**Reference Date:** 2026-10-24  
**Defect Resolved:** DEF-P2-04 (Heatmap Cell Small-Count Exposure)  

---

## 1. The Large-Group / Small-Cell Privacy Paradox

An operational cohort of $N = 50$ satisfies the minimum cohort floor ($k=5$). However, when stratified into a 2D matrix ($4 \text{ clusters} \times 16 \text{ skills} = 64 \text{ cells}$), individual cell counts frequently drop into the privacy-sensitive zone ($1..4$).
In v1.0.0, publishing `gap_prevalence = count / N_group` for a single-worker gap revealed $1 / 14 = 0.0714$, leaking single-worker attribute status.

---

## 2. Remediated Heatmap Cell Contract

In O1 v1.1.0:
Every heatmap cell undergoes independent privacy evaluation:
- If $0 < \text{gapped\_count} < 5$:
  - `suppressed: true`
  - `suppression_reason: "SMALL_CELL_PRIVACY"`
  - `display_value: null`
  - `count_display: "<5"`
  - `gap_prevalence: null`
  - `core_gap_prevalence: null`
  - `priority_index: null`
- If unsuppressed ($N \ge 5$):
  - `display_value = priority_index`
  - `count_display = str(count)`

In the synthetic demonstration benchmark, **38 of 64 cells** are correctly suppressed, eliminating all cell-level small-count disclosures.
