# Stage 9F Remediation Report: OpenAlex Damping & Multiplier Reconciliation (v1.1.1)

**Author:** Senior Quantitative Engineer & Reproducibility Auditor  
**Date:** 2026-10-23  
**Stage:** Stage 9F Targeted Remediation  
**Release Target:** M2 Trend Intelligence v1.1.1 (Engine Release Candidate)

---

## 1. Executive Summary & Defect Remediation Scope

Following the Stage 9E Post-Remediation Review, which issued the verdict **`TARGETED M2 V1.1 FIX REQUIRED`**, Stage 9F was executed with a strict, bounded mandate:
1. **Fix the Format String Defect in Explanation Strings**: Eliminate the interpolation of raw velocity ratios (`growth_rate_ratio`) mislabeled as "volume-damped".
2. **Reconcile Documentation with Canonical Implementation**: Formally retire the obsolete draft formula $N_{\text{recent}} / (N_{\text{recent}} + K)$ and document the canonical logarithmic baseline-volume shrinkage formula $w_{\text{vol}} = \min(1.0, \ln(1 + N_{\text{base}})/\ln(26))$.
3. **Upgrade Research Momentum Mapping to Ensure Material Component Separation**: Replace the linear multiplier (`damped_growth * 38.0`) that caused saturation at 95.0 with a smooth, monotonic asymptotic transform ($50.0 + 44.0 \cdot (1 - e^{-(R_{\text{adj}}-1)/4.0})$), ensuring that low-base emerging topics are cleanly differentiated from mature, high-volume literature.
4. **Preserve Complete Methodological Integrity**: Leave ILO 2025 benchmarks, wage granularity metadata, confidence distributions (7 HIGH, 7 MEDIUM, 2 LOW), conflict taxonomy, and frozen M1 holdouts completely untouched.

All 4 remediation objectives were successfully implemented, verified through automated unit tests (42/42 passing), and packaged under version **1.1.1**.

---

## 2. Detailed Technical Fixes Implemented

### Issue 1: Explanation String Generator Patch
- **Defect in v1.1.0**: In `scripts/build_trend_scores_v1_1.py` line 623, the summary string interpolated `srm.get('growth_rate_ratio')` (the raw ratio, e.g., 17.143 $\to$ 17.1x) and appended the text `", volume-damped"`.
- **Fix in v1.1.1**: The explanation generator in [build_trend_scores_v1_1_1.py](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_trend_scores_v1_1_1.py#L265-L278) now explicitly distinguishes between raw publication growth and adjusted momentum:
  - *Low-Base Skills* ($N_{\text{baseline}} < 5$):
    > `"Raw publication growth: 17.1x; low-base adjusted research momentum ratio: 4.4x; based on 1 baseline publication and 18 recent publications."`
  - *Mature / High-Volume Skills* ($N_{\text{baseline}} \ge 5$):
    > `"Raw publication growth: 11.2x; volume-adjusted research momentum ratio: 9.5x; based on 14 baseline publications and 121 recent publications."`
- **Audit Verification**: Verified via `test_explanation_distinguishes_raw_and_adjusted` in [test_trend_scoring_engine_v1_1_1.py](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/tests/test_trend_scoring_engine_v1_1_1.py).

### Issue 2: Documentation Formula Reconciliation
- **Obsolete Draft Formula**: $R_{\text{damped}} = 1.0 + (R_{\text{raw}} - 1.0) \cdot \frac{N_{\text{recent}}}{N_{\text{recent}} + 10}$ is formally classified as a **REJECTED STAGE 9D DRAFT**.
- **Canonical v1.1.1 Formula**:
  $$w_{\text{volume}} = \min\left(1.0, \frac{\ln(1 + N_{\text{baseline}})}{\ln(26)}\right)$$
  $$R_{\text{adjusted}} = 1.0 + (R_{\text{raw}} - 1.0) \cdot w_{\text{volume}}$$
- **Empirical Justification**: In scientometrics, spurious growth rate explosions are caused by near-zero denominators ($N_{\text{baseline}} \le 2$). The logarithmic shrinkage on baseline volume shrinks small-sample noise while approaching 1.0 as the baseline body of literature reaches 25 publications ($\ln(26)$).

### Issue 3: Monotonic Asymptotic Score Transform
- **Defect in v1.1.0**: Multiplying `damped_growth * 38.0` pushed both `prompt_engineering` ($4.434 \times 38 = 168.5$) and `ai_literacy` ($9.481 \times 38 = 360.3$) into the hard 95.0 ceiling, erasing the effect of damping.
- **Fix in v1.1.1**: Replaced linear multiplier with monotonic asymptotic transform:
  $$\text{research\_momentum\_index} = 50.0 + 44.0 \cdot \left(1.0 - \exp\left(-\frac{R_{\text{adjusted}} - 1.0}{4.0}\right)\right)$$
- **Operational Effect**:
  - `prompt_engineering` ($R_{\text{adj}} = 4.434$) score drops from **95.0 $\to$ 75.4**.
  - `rag_knowledge_systems` ($R_{\text{adj}} = 6.866$) score drops from **95.0 $\to$ 83.8**.
  - `ai_literacy` ($R_{\text{adj}} = 9.481$) score drops moderately from **95.0 $\to$ 88.7**.
  - Creates a **13.3 point operational gap** between low-base emerging topics and mature high-volume topics, completely eliminating false ceiling saturation.

---

## 3. Regression Verification & Test Results

All regression gates passed with 100% compliance:
- **ILO 2025 Benchmark**: Remains active (`ILO_WP140_2025`).
- **Confidence Distribution**: Remains **7 HIGH, 7 MEDIUM, 2 LOW, 0 INSUFFICIENT**.
- **Wage Granularity**: All 20 MASCO 4-digit roles retain `wage_granularity = "MAJOR_GROUP_CONTEXT"` and quality flags.
- **Saturation at 100.0**: Exactly **0** components saturated across all skills and occupations.
- **Automated Test Suites**: **42 / 42 PASSED** (0.651s).
