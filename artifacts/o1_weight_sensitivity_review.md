# Empirical Audit: Priority Weight Sensitivity & Robustness

**Module:** O1 Employer / HR Workforce Planning Layer  
**Engine:** `src/workforce_gap_engine.py`  
**Date:** 2026-10-24  
**Audit Finding:** RANKINGS ARE ROBUST (AUDIT 18 & 19: PASS)  

---

## 1. Methodology for Weight Perturbation

To test whether the Workforce Reskilling Priority Index is excessively fragile to minor product-policy adjustments, we conducted a systematic perturbation study around the baseline weights:
- Baseline Weights: `core` = 0.35, `important` = 0.20, `deficit` = 0.15, `transferability` = 0.15, `scenario` = 0.10, `prerequisite` = 0.05.
- Evaluated on the canonical 50-profile synthetic workforce cohort (`synthetic_workforce_v1.json`).
- Applied $\pm 0.05$ shifts to paired components with renormalization to $\sum w_k = 1.00$.
- Computed Spearman rank correlation $\rho$, Top-5 skill overlap, and count of skills shifting by $\ge 3$ rank positions.

---

## 2. Sensitivity Analysis Results

| Experiment ID | Weight Perturbation Description | Re-normalized Weights | Spearman Rank Correlation $\rho$ | Top-5 Overlap | Skills Shifting $\ge 3$ Ranks |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **BASE** | Baseline Policy Config | 0.35 / 0.20 / 0.15 / 0.15 / 0.10 / 0.05 | 1.0000 | 5/5 | 0 |
| **PERT-01** | +0.05 CORE, -0.05 IMPORTANT | 0.40 / 0.15 / 0.15 / 0.15 / 0.10 / 0.05 | **0.9824** | 4/5 | 0 |
| **PERT-02** | -0.05 CORE, +0.05 IMPORTANT | 0.30 / 0.25 / 0.15 / 0.15 / 0.10 / 0.05 | **1.0000** | 5/5 | 0 |
| **PERT-03** | +0.05 Transferability, -0.05 Deficit | 0.35 / 0.20 / 0.10 / 0.20 / 0.10 / 0.05 | **0.9941** | 5/5 | 0 |
| **PERT-04** | +0.05 Scenario, -0.05 CORE | 0.30 / 0.20 / 0.15 / 0.15 / 0.15 / 0.05 | **0.9853** | 4/5 | 0 |
| **PERT-05** | +0.05 Prerequisite, -0.05 Scenario | 0.35 / 0.20 / 0.15 / 0.15 / 0.05 / 0.10 | **0.9765** | 5/5 | 0 |

---

## 3. Analysis & Robustness Classification

1. **Rank Correlation:** The Spearman rank correlation across all perturbations ranges from **0.9765** to **1.0000**, with a mean correlation of **0.9877**.
2. **Top-Tier Stability:** The Top-5 skills maintain an overlap of at least 4 out of 5 (80%) in all perturbations, with 3 out of 5 perturbations preserving 100% Top-5 membership.
3. **Absence of Violent Swings:** Across all 16 canonical skills, **zero** skills shifted by $\ge 3$ positions under any tested perturbation. Shifts were confined to local adjacent ties (e.g. ranks 4 and 5 swapping).
4. **Policy Parameter Declaration:** The weights are properly documented in `o1_config_v1.json` as configurable product-policy parameters rather than universal scientific constants.

### Official Robustness Classification:
**`ROBUST`**
