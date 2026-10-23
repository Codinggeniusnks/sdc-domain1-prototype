# Statistical Comparison & Significance Audit: M6 Candidate vs M5 Baseline

**Auditor**: Independent Statistical Reviewer & Technical Judge  
**Date**: October 22, 2026  
**Methodology**: Paired Record-Level Bootstrap, Paired Grouped/Cluster Bootstrap (3,000 resamples), Paired Permutation Test, and McNemar Disagreement Counting on Identical Test Samples.

---

## 1. Executive Statistical Finding

The reported gains of M6 over M5 (+0.0221 Skills Macro F1 on Protocol B and +0.0151 on Protocol C) are **statistically indistinguishable from noise**. Every 95% confidence interval for the delta spans zero, and paired permutation test p-values are high ($p = 0.28$ to $0.43$).

The apparent improvement is driven by a net gain of **only two correct binary decisions** across the entire 63-sample evaluation suite.

---

## 2. Paired Analysis on Protocol B ($N = 63$, Clusters = 32)

Evaluating M6 and M5 on the exact same 63 holdout records:

| Metric | M5 Baseline | M6 Candidate | Observed Delta ($\Delta$) | Paired 95% Bootstrap CI (Record) | Paired 95% Bootstrap CI (Cluster) | $P(\text{M6} > \text{M5})$ | Paired Permutation $p$-value | Statistically Significant? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Skills Macro F1** | 0.6928 | **0.7149** | **+0.0221** | `[-0.0151, +0.0631]` | `[-0.0223, +0.0633]` | 85.3% | **$p = 0.2842$** | **NO** |
| **Skills Micro F1** | 0.6612 | **0.6824** | **+0.0212** | `[-0.0174, +0.0625]` | `[-0.0272, +0.0577]` | 82.8% | **$p = 0.3662$** | **NO** |
| **Demand Macro F1** | 0.7407 | **0.7644** | **+0.0237** | `[-0.0813, +0.1261]` | `[-0.0681, +0.1514]` | 63.6% | **$p = 0.6928$** | **NO** |
| **Demand ROC AUC** | **0.8617** | 0.8379 | **-0.0238** | `[-0.0839, +0.0309]` | `[-0.0830, +0.0336]` | 21.1% | **$p = 0.4125$** | **NO (Degraded)** |
| **Demand Brier Score** | **0.1635** | 0.1668 | **+0.0033** | `[-0.0127, +0.0190]` | `[-0.0169, +0.0250]` | 36.9% | **$p = 0.6891$** | **NO (Degraded)** |

### Granular Contingency Analysis on Protocol B
- **Multi-Label Skill Decision Matrix ($63 \times 16 = 1,008$ binary cells)**:
  - Cells correctly fixed by M6: **15 cells**.
  - Cells broken by M6 (correct in M5, wrong in M6): **13 cells**.
  - **Net Gain**: **+2 cells out of 1,008 total decisions (+0.20%)**.
- **Demand Classification ($N = 63$ records)**:
  - M6 correct, M5 wrong: **6 records**.
  - M6 wrong, M5 correct: **4 records**.
  - **Net Gain**: **+2 records out of 63 (+3.17%)**.

---

## 3. Paired Analysis on Protocol C ($N = 25$, Clusters = 12)

| Metric | M5 Baseline | M6 Candidate | Observed Delta ($\Delta$) | Paired 95% Bootstrap CI (Record) | Paired 95% Bootstrap CI (Cluster) | $P(\text{M6} > \text{M5})$ | Paired Permutation $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Skills Macro F1** | 0.6045 | **0.6196** | **+0.0151** | `[-0.0212, +0.0581]` | `[-0.0192, +0.0551]` | 81.2% | **$p = 0.4335$** |
| **Skills Micro F1** | 0.6377 | **0.6712** | **+0.0336** | `[-0.0207, +0.0950]` | `[-0.0259, +0.0813]` | 88.4% | **$p = 0.1989$** |
| **Demand Macro F1** | **0.5660** | 0.5098 | **-0.0562** | `[-0.3014, +0.1872]` | `[-0.2889, +0.1778]` | 35.8% | **$p = 0.5621$** |
| **Demand ROC AUC** | **0.6500** | 0.6200 | **-0.0300** | `[-0.2818, +0.2222]` | `[-0.2667, +0.2000]` | 41.5% | **$p = 0.8120$** |

---

## 4. Methodological Review of the Bootstrap

The previous developer reported independent 1,000-iteration bootstrap confidence intervals for M6 alone (e.g., `[0.5466, 0.7726]`).
1. **Flaw of Independent CIs**: Independent intervals do not measure whether M6 is better than M5 because they ignore sample-level correlation. On small paired samples, a paired delta test is mandatory.
2. **Cluster Grouping Effect**: Because multiple records share occupational unit groups (32 clusters across 63 records in Protocol B), ordinary i.i.d. bootstrap artificially underestimates variance. Grouped/cluster bootstrap expands the lower bound of the delta to **-0.0223**, demonstrating that the probability of zero or negative improvement is approximately **15%**.

---

## 5. Statistical Conclusion

The claimed improvement from $F_1 = 0.6928$ to $0.7149$ cannot be scientifically cited as a verified capability breakthrough. It represents an incremental shift of 2 decisions within standard sampling error, accompanied by a genuine degradation in calibrated demand probability.
