# M2 Sensitivity and Robustness Analysis (v1.1.0)

## Executive Summary

During the Stage 9C Argon Forensic Audit, Defect **P2-2** identified that previous sensitivity analyses collapsed all evaluation into a single generic "stability" figure, concealing the difference between boundary shifts between adjacent tiers and fundamental sign flips or rank inversions.

In M2 v1.1.0, the sensitivity methodology was upgraded to evaluate **three distinct, mathematically rigorous metrics**:
1. **Directional-Sign Stability**: Does the fundamental direction (Positive / Neutral / Negative) remain invariant under $\pm 10\%$ weight and $\pm 5$ pt threshold perturbations?
2. **Exact Outlook Tier Stability**: Do entities retain their identical 5-tier classification (`STRONGLY RISING`, `RISING`, `STABLE`, `DECLINING`, `STRONGLY DECLINING`)?
3. **Relative Rank Stability (Spearman's $\rho$)**: Does the ordinal ranking of skills and occupations remain preserved under parameter shifts?

---

## Sensitivity Audit Results

| Entity Domain | Sample Size ($N$) | Directional-Sign Stability | Exact Tier Stability | Spearman Rank Correlation ($\rho$) | Parameter Margin (Min) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Skills Corpus** | 16 | **100.0%** (16 / 16) | **87.5%** (14 / 16) | **0.9701** ($p < 10^{-8}$) | 5.0 pts |
| **Occupations Corpus** | 20 | **100.0%** (20 / 20) | **45.0%** (9 / 20) | **0.9043** ($p < 10^{-6}$) | 5.0 pts |
| **Combined System** | **36** | **100.0%** (36 / 36) | **63.9%** (23 / 36) | **0.9372** | 5.0 pts |

---

## Analytical Findings & Interpretation

### 1. Invariance of Directional Sign (100.0% Stability)
- Across all 16 skills and all 20 occupations, **not a single entity experienced a sign flip** (e.g., from Rising to Declining, or Declining to Rising).
- Growth skills remained growth skills; declining clerical roles (General Office Clerks 4110, Accounting Clerks 4311) remained negative without exception.
- This proves that M2's macroeconomic conclusions are robust against reasonable weighting uncertainty.

### 2. Distinction Between Sign Stability and Exact Tier Boundary Sensitivity
- For skills, 14 of 16 (87.5%) retained their exact tier. Only `workflow_automation` and `data_privacy_pdpa` shifted from `STRONGLY RISING` to `RISING` when the threshold was raised from +20 to +25.
- For occupations, exact tier retention was 45.0% (9 / 20). 11 occupations cluster near the boundary between `STRONGLY RISING` ($> 20$) and `RISING` ($> 5$). Raising the threshold shifts these 11 roles from `STRONGLY RISING` to `RISING`, but their rank order and positive momentum remain intact.
- **Critical Insight**: This empirical finding explains why reporting a single "stability" metric was misleading in v1.0.0. The clustering near tier boundaries creates apparent tier volatility, yet the underlying ordinal priority and economic signal are exceptionally stable ($\rho = 0.9043$).

### 3. Preservation of Relative Rank Order (Spearman $\rho \ge 0.90$)
- The Spearman rank correlation of **0.9701** for skills and **0.9043** for occupations confirms that downstream consumers (such as M3 Role Matching) will recommend virtually the same prioritized skills and pathways regardless of parameter perturbations within the tested $\pm 10\%$ corridor.

---

## Downstream Implementation Recommendations

1. **Continuous Scoring in M3**: M3 Role Matching should utilize the continuous normalized score ($[-100, +100]$) rather than discrete tier labels to avoid artificial boundary discretization effects.
2. **Confidence Band Visualization**: In UI dashboards, display outlooks with their associated score confidence margins ($score \pm 5.0$) rather than hard categorical boundaries.
