# M3 Weight Sensitivity Analysis & Robustness Report

**Engine Version**: M3 v1.0.0  
**Evaluator**: Senior Recommender-Systems Engineer & Methodology Auditor  
**Date**: 2026-10-23  
**Data Reference**: [`data/matching/m3_benchmark_results_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/matching/m3_benchmark_results_v1.json)  

---

## 1. Executive Summary

A core methodological requirement of Stage 11A is verifying that M3 recommendations do not behave erratically under small perturbations in weight configurations, while simultaneously ensuring that no optimization occurred against synthetic persona answers.

We evaluated all 8 synthetic benchmark personas across three distinct weighting regimes:
1. **Balanced Baseline**: $w_{\text{M1}} = 60\%, w_{\text{M2}} = 25\%, w_{\text{M6}} = 15\%$
2. **Skill-Heavy**: $w_{\text{M1}} = 75\%, w_{\text{M2}} = 15\%, w_{\text{M6}} = 10\%$
3. **Scenario-Aware**: $w_{\text{M1}} = 55\%, w_{\text{M2}} = 30\%, w_{\text{M6}} = 15\%$

All three regimes strictly satisfy the M6 Downstream Safety Contract ($w_{\text{M1}} \ge 55\%$, $w_{\text{M2}} \le 30\%$, $w_{\text{M6}} \le 15\%$).

---

## 2. Aggregate Stability Metrics

| Metric | Measured Value | Minimum Target Threshold | Status | Interpretation |
|:---|:---:|:---:|:---:|:---|
| **Top-1 Weight Stability** | **75.0%** | $\ge 60.0\%$ | **PASS** | 6 of 8 personas maintain identical #1 recommended role across all 3 regimes |
| **Top-3 Overlap (Jaccard)** | **0.938** | $\ge 0.800$ | **PASS** | 93.8% overlap in top-3 recommendation sets between regimes |
| **Average Spearman Rank Correlation** | **0.987** | $\ge 0.900$ | **PASS** | Exceptionally high overall rank order stability across all 20 candidate roles |
| **Total Weight-Sensitive Roles** | **18** | Documented & Flagged | **AUDITED** | Roles shifting by $\ge 2$ ranks across regimes flagged with `WEIGHT_SENSITIVE_RECOMMENDATION` |

---

## 3. Persona-by-Persona Sensitivity Breakdown

| Persona ID | Primary Domain | Top-1 Role (Balanced) | Top-1 Role (Skill-Heavy) | Top-1 Role (Scenario-Aware) | Top-1 Stable? | Top-3 Overlap | Spearman $\rho$ |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | Data / Analytics | 2521 (Database Admin) | 2521 (Database Admin) | 2521 (Database Admin) | **YES** | 1.000 | 0.995 |
| **P2** | Software / Automation | 2512 (Software Dev) | 2512 (Software Dev) | 2512 (Software Dev) | **YES** | 1.000 | 0.998 |
| **P3** | Business Operations | 2511 (Systems Analyst) | 2511 (Systems Analyst) | 2511 (Systems Analyst) | **YES** | 1.000 | 0.994 |
| **P4** | Governance / Privacy | 2422 (Policy Specialist) | 2422 (Policy Specialist) | 2422 (Policy Specialist) | **YES** | 1.000 | 0.994 |
| **P5** | Sustainability / ESG | 2143 (Environmental Eng) | 2143 (Environmental Eng) | 2143 (Environmental Eng) | **YES** | 1.000 | 0.997 |
| **P6** | Instructional / Comm | 2424 (Training Specialist) | 2424 (Training Specialist) | 2424 (Training Specialist) | **YES** | 1.000 | 0.988 |
| **P7** | Clerical Transition | 4110 (Office Clerk) | 4110 (Office Clerk) | 2511 (Systems Analyst) | **NO** | 0.750 | 0.965 |
| **P8** | Sparse Early-Career | 4110 (Office Clerk) | 3322 (Sales Rep) | 4110 (Office Clerk) | **NO** | 0.750 | 0.965 |

### Analysis of Non-Identical Top-1 Personas:
1. **Persona 7 (Clerical Transition)**:
   - Under `balanced_baseline` and `skill_heavy`, the candidate ranks `4110 General Office Clerks` as #1 due to near-complete core skill fit (process mapping + AI literacy).
   - Under `scenario_aware` ($w_{\text{M2}}=30\%, w_{\text{M6}}=15\%$), `2511 Systems Analysts` edges into #1 because 2511 has massive demand shortage (89.6) and high augmentation potential (85.0), whereas 4110 suffers high routine automation exposure.
   - **Methodological Significance**: This illustrates that the Scenario-Aware model surfaces high-leverage transition targets when labor context is prioritized, while Balanced keeps immediate skill readiness top.
2. **Persona 8 (Sparse Early-Career)**:
   - With only foundational `ai_literacy`, top candidate roles cluster closely between 4110 and 3322. Because skill fit is low across all roles, small weight differences naturally shift the top recommendation.

---

## 4. Scenario Weight Dominance Verification

A critical test is checking whether increasing the M6 Scenario weight from $10\%$ (`skill_heavy`) to the ceiling of $15\%$ (`balanced_baseline` and `scenario_aware`) allows scenario foresight to overpower skill fit.

**Finding**:
- Across all 8 personas, zero roles with low skill fit overtook high skill fit roles.
- Role 2512 (Software Developers, with highest scenario resilience of 92.5) remained ranked in the bottom quartile for Personas 5 (Sustainability) and 6 (Instructional Design) because their skill overlap is near zero ($< 15.0$ Match Index).
- The **Scenario Dominance Guardrail** ($\Delta \text{fit} > 20\%$) and **Zero-Overlap Clamping** ($\le 15.0$) successfully prevented scenario score leakage.

---

## 5. Non-Optimization Statement

As required by competition standards:
- The weighting configurations ($60/25/15$, $75/15/10$, $55/30/15$) were established a priori derived from the M6 Downstream Safety Contract bounds.
- **Weights were NOT tuned or fitted to optimize synthetic persona ranks or preferred occupations.**
