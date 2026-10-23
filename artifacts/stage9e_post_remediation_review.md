# Stage 9E Post-Remediation Review: M2 Trend Intelligence v1.1.0

**Reviewer:** Independent Senior Quantitative Methodology Reviewer & Reproducibility Auditor  
**Date:** 2026-10-23  
**Target Engine:** M2 AI Trend Intelligence v1.1.0  
**Audit Scope:** Bounded verification of Stage 9D remediation fixes and mathematical integrity.

---

## 1. Executive Summary & Review Findings

Stage 9D targeted remediation delivered substantial, high-impact improvements to the M2 Trend Intelligence engine. Of the three Priority-1 defects identified during Stage 9C:
- **P1-1 (ILO 2025 Benchmark)**: **CLOSED**. Fully integrated and verified.
- **P1-2 (Confidence Recalibration)**: **CLOSED**. Source bleed eliminated; authentic variation (7 HIGH, 7 MED, 2 LOW) confirmed.
- **P1-3 (Wage Granularity & Context)**: **CLOSED**. 1-digit Major Group context explicitly tagged across all 20 occupations.

However, a mandatory forensic audit of **Check 4 (OpenAlex Damping Arithmetic)** identified a discrepancy between the declared methodology in documentation and the actual implementation in code:
1. **Formula Inconsistency**: The documentation specified a rational shrinkage formula $N_{\text{recent}} / (N_{\text{recent}} + K)$, whereas the code implemented a logarithmic shrinkage on baseline counts $\ln(1 + N_{\text{baseline}}) / \ln(26)$.
2. **Display Format String Bug**: In `scripts/build_trend_scores_v1_1.py` line 623, the raw velocity ratio (`17.1x`) was interpolated into the summary string and erroneously labeled `"volume-damped"`.
3. **Multiplier Saturation**: In line 472, `damped_growth` was scaled by $38.0$, re-saturating `research_momentum` at $95.0$ even after damping.

Because the prompt methodology explicitly dictates: *"If implementation does not match the declared methodology: classify at least as: P1 remediation required before freeze"*, the formal verdict of this review is **`TARGETED M2 V1.1 FIX REQUIRED`**.

---

## 2. Comprehensive Systematic Verification Matrix

| Check ID | Verification Area | Audit Criteria | Empirical Status | Finding / Disposition |
| :---: | :--- | :--- | :---: | :--- |
| **Check 1** | ILO 2025 Integration | WP 140 active; WP 96 historical; same family `ILO_GENAI_STUDY`; 20 roles mapped. | **VERIFIED** | **P1-1 CLOSED**. Active benchmark is WP 140; 0 roles unmapped; longitudinal comparison logic verified. |
| **Check 2** | Confidence Source Bleed | Remove `ILO_GENAI_STUDY` & `DOSM_WAGES` from skills; verify 7/7/2/0 distribution. | **VERIFIED** | **P1-2 CLOSED**. Zero source bleed confirmed across all 16 skills. Distribution derived organically. |
| **Check 2b** | Publisher Independence | Verify TalentCorp MyCOL & Impact Study handling. | **VERIFIED** | TalentCorp capped at 35 pts. Listed families reflect distinct surveys; 3 unique institutional publishers verified for HIGH skills. |
| **Check 3** | Wage Granularity | 20 roles tagged with `MAJOR_GROUP_CONTEXT`, context codes, quality flags; M3 salary inference barred. | **VERIFIED** | **P1-3 CLOSED**. 20/20 roles carry context tags; summary strings declare Major Group context. |
| **Check 4** | OpenAlex Damping Arithmetic | Formula verification against code; determine discrepancies. | **DEFECT FOUND** | **DOCUMENTATION ERROR & FORMAT BUG**. Written formula != code; summary string printed raw ratio as damped. |
| **Check 5** | Low-Base Effect | Material reduction of velocity explosions ($1 \to 18$, $2 \to 22$). | **VERIFIED** | Code's logarithmic formula shrinks excess growth by 78.7% ($17.1 \to 4.4$). Multiplier scaling needs adjustment. |
| **Check 6** | Historical Directional Alignment | Prohibit "accuracy/predictive" terms; benchmark vs 3 naive baselines (+2.5% gain). | **VERIFIED** | Reclassified to "Limited Directional Alignment Check". Honest attribution to persistence confirmed. |
| **Check 7** | No Look-Ahead (Temporal Leakage) | Strict temporal barrier (pre-2024 features predict post-2024 outcomes). | **VERIFIED** | Zero post-2023 leakage in training features. |
| **Check 8** | Sensitivity Claims | 3 metrics evaluated: Sign (100%), Tier (64%), Spearman ($\rho \ge 0.90$). | **VERIFIED** | No generic "100% stable" claim. Tier sensitivity near boundaries accurately disclosed. |
| **Check 9** | Score Saturation | 0 saturated components at 100.0; monotonic soft bounds. | **VERIFIED** | Saturated components reduced from 51 to 0. Soft $\tanh$ transform is strictly monotonic. |
| **Check 10** | Conflict Handling | Distinguish `CROSS_DIMENSION_TENSION` from `WITHIN_DIMENSION_CONFLICT`. | **VERIFIED** | High AI exposure alone does not force decline. Software Devs (2512) confirmed strongly rising via $6.75\times$ augmentation. |
| **Check 11** | M1 Holdout Provenance | Correct historical unsealing statement. | **CORRECTED** | No additional Protocol B/C v2 access occurred during Stage 9A–9E after the approved one-shot Stage 8E evaluation. |
| **Check 12** | Reproducibility | Deterministic hash verification of all inputs and outputs. | **VERIFIED** | All 5 processed outputs match cryptographic hashes in `m2_build_manifest_v1_1.json` (100% deterministic). |
| **Check 13** | Updateability | Verify incremental update pipeline via test fixture. | **VERIFIED** | `tests/test_updateability_fixture.py` passed (OK in 0.003s). |
| **Check 14** | Downstream Safety | Safety contracts for M3 and M6 verified. | **VERIFIED** | M3 barred from salary prediction and raw AI exposure penalization; M6 scenarios decoupled from observations. |

---

## 3. Detailed Audit by Check Section

### Check 1: ILO 2025 Integration (P1-1 CLOSED)
- **Active Benchmark**: ILO Working Paper 140 (May 2025) `SRC-ILO-GENAI-2025`.
- **Historical Reference**: ILO Working Paper 96 (August 2023) `SRC-ILO-GENAI-2023`.
- **Evidence Family**: Both belong strictly to `{'ILO_GENAI_STUDY'}`. They do not count as two independent confirmations.
- **Coverage**: 20 / 20 MASCO 4-digit occupations mapped with explicit task-level augmentation and automation decomposition.

### Check 2: Confidence Recalibration & Publisher Independence (P1-2 CLOSED)
- **Source Bleed**: Verification confirmed that `ILO_GENAI_STUDY` and `DOSM_WAGES` are absent from skill profile evidence families (`False` for all skills).
- **Distribution**: 7 HIGH, 7 MEDIUM, 2 LOW, 0 INSUFFICIENT. Derived organically from signal counts and publisher caps.
- **Publisher Independence**: TalentCorp group score is capped at 35 points. Skills in the HIGH tier possess 3 distinct institutional publishers (TalentCorp, Government Policy, OpenAlex Academic), meeting rigorous independence standards.

### Check 3: Wage Granularity & Attribution (P1-3 CLOSED)
- All 20 four-digit occupations explicitly carry `wage_granularity: "MAJOR_GROUP_CONTEXT"`, context codes (`MAJOR_1` through `MAJOR_4`), and quality flags `MAJOR_GROUP_WAGE_CONTEXT` and `NO_ROLE_SPECIFIC_WAGE_DATA`.
- Citations state `"National formal wage context (Major Group X)"` rather than role-specific wage claims.

### Checks 4 & 5: OpenAlex Damping & Low-Base Effect
- Detailed forensic analysis documented in [m2_v1_1_formula_verification.md](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m2_v1_1_formula_verification.md).
- The code's logarithmic shrinkage on $N_{\text{baseline}}$ successfully reduces small-sample velocity explosions from $17.143 \to 4.434$ ($78.7\%$ reduction).
- However, the documentation formula mismatch, the line 623 format string interpolation bug, and the multiplier ceiling saturation constitute a methodology defect requiring a targeted fix before formal freezing.

### Checks 6 & 7: Historical Alignment & Temporal Integrity
- Terminology reclassified to "Limited Directional Alignment Check". Prohibited terms completely eliminated.
- Incremental gain over naive persistence is $+2.5\%$ (92.5% vs 90.0%), correctly attributed to real-world structural persistence rather than predictive foresight.
- Strict temporal barriers confirmed: features $\le 2023$ evaluate outcomes in 2024–2026.

### Checks 8 & 9: Sensitivity & Score Saturation
- 3 distinct metrics evaluated: Directional sign stability (100.0%), Exact tier stability (87.5% skills, 45.0% occupations), and Spearman rank correlation ($\rho = 0.9701 / 0.9043$).
- Saturated components at 100.0 reduced from 51 in v1.0.0 to 0 in v1.1.0 via monotonic $\tanh$ soft bounds.

### Check 10: Conflict Handling
- Formal 4-tier conflict taxonomy verified. `CROSS_DIMENSION_TENSION` is resolved via the Augmentation-to-Automation ratio.
- Software Developers (2512) correctly retain `STRONGLY RISING` because augmentation ($54.0\%$) outpaces automation ($8.0\%$) by $6.75\times$. High exposure alone does not force a declining outlook.

### Check 11: M1 Holdout Provenance
- Verified and corrected: No additional Protocol B or Protocol C v2 access occurred during Stage 9A–9E after the approved one-shot Stage 8E evaluation.

### Checks 12 & 13: Reproducibility & Updateability
- Cryptographic hash verification confirmed 100% deterministic output matching `data/trends/processed/m2_build_manifest_v1_1.json`.
- `tests/test_updateability_fixture.py` verified that incremental incoming signals update component vectors and confidence cleanly.
