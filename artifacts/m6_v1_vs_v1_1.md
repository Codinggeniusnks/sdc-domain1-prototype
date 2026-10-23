# M6 Architecture & Output Comparison: v1.0.0 vs v1.1.0

**Audit Subject**: Side-by-Side Comparison of M6 Scenario Engine v1.0.0 vs v1.1.0  
**Date**: 2026-10-23  
**Stage**: Stage 10C Verification

---

## 1. Architectural & Formula Differences

| Dimension | M6 v1.0.0 (Legacy Prototype) | M6 v1.1.0 (Remediated Production Gate) | Remediation Impact |
| :--- | :--- | :--- | :--- |
| **Scenario Multipliers** | Hardcoded `1.0` bypass for `REFERENCE_2026`; non-reference normalized by `/ 50.0` with arbitrary constants `1.1, 1.2, 1.15`. | Analytically anchor-normalized relative to `REFERENCE_2026` central parameters; zero magic constants; zero bypass logic. | Completely eliminates `MODERATE_COPILOT` baseline inversions (`0.9605x` $\to$ `1.3996x`). Strict monotonicity across all bounds. |
| **Reference Uncertainty** | Ranges collapsed to zero width (`lower == central == upper`). | Meaningful non-zero intervals evaluated through the unified formula (`auto_mult`: `[0.8465, 1.0000, 1.1180]`). | Real baseline sensitivity ranges without altering central M2 identity. |
| **Outlook Classification** | Bifurcated regimes: string lookup in `REFERENCE_2026` vs independent threshold classifier in non-reference. | Unified two-stage anchor-and-delta classification framework across all scenarios. | Zero spurious baseline flips. Preserves `RESILIENT` status for Major Groups in `MODERATE_COPILOT` where net resilience rises. |
| **Technology Diffusion** | Dead parameter (`diffusion_reach` computed but never used, $\partial y / \partial \text{diff} = 0$). | Actively wired into `ai_press_mult` ($35\%$), `auto_mult` ($20\%$), and `aug_mult` ($15\%$) with distinct semantics. | All 8 scenario parameters have verified non-zero, interpretable partial derivatives ($\partial > 0$). |
| **Occupational Granularity** | 20 4-digit occupations and 8 1-digit Major Group fallbacks pooled into single $N=28$ table. | Explicit `entity_granularity` (`FOUR_DIGIT_OCCUPATION` vs `ONE_DIGIT_MAJOR_GROUP_FALLBACK`) reported separately. | Downstream M3 knows fallbacks are aggregate benchmarks, not peer candidate roles. |
| **Major Group Wage Flags** | Major Groups carried invalid role-level flags: `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA`. | Major Groups carry: `AGGREGATED_MAJOR_GROUP_FALLBACK`, `GROUP_LEVEL_DIRECT_WAGE_MEASUREMENT`. | Clean, deduplicated wage flags aligned to direct DOSM measurement level. |
| **Sensitivity Semantics** | 1D ordinal distance labeled high-augmentation roles (`2512`) as `HIGHLY SENSITIVE`. | Multi-dimensional `sensitivity_profile` separating `downside_risk_stability` from `transformation_sensitivity`. | Software Developers recognized as `ROBUST` against downside risk with `UPSIDE_TRANSFORMATION`. |
| **Reskilling Urgency** | Clustered at `MODERATE`/`HIGH`; 0 occupations reached `VERY HIGH` in `FAST_AGENTIC`. | Calibrated 3-channel urgency index ($\text{auto\_p}$, $\text{trans\_p}$, $100 - \text{demand\_res}$). | Clerical roles (`4110`, `4311`, `3343`) correctly reach `VERY HIGH` under `FAST_AGENTIC`; baseline skills not over-penalized. |
| **Historical Baseline Flags** | Stage 10A text reported only 2 zero-base skills. | Canonical propagation across all 4 zero-base skills (`data_visualization`, `human_in_the_loop_qa`, `api_integration`, `carbon_footprint_analytics`). | 100% agreement between JSON data and report narrative. |

---

## 2. Numerical Trajectory Comparison on Core Benchmark Entities

### 2.1 Software Developers (`2512`) — Strong Augmentation Benchmark
| Scenario | Metric | M6 v1.0.0 (Legacy) | M6 v1.1.0 (Remediated) | Key Change |
| :--- | :--- | :---: | :---: | :--- |
| **`REFERENCE_2026`** | `eff_ai` / `auto_p` / `aug_o` | 62.0 / 8.0 / 54.0 | 62.0 / 8.0 / 54.0 | Exact baseline identity preserved. |
| **`REFERENCE_2026`** | `auto_p` range `[L, C, U]` | `[8.0, 8.0, 8.0]` (collapsed) | **`[6.8, 8.0, 8.9]`** | Meaningful non-zero uncertainty interval. |
| **`MODERATE_COPILOT`** | `eff_ai` | **59.6** (INVERTED BELOW BASELINE!) | **86.8** | P1-1 defect resolved. |
| **`MODERATE_COPILOT`** | `auto_p` / `aug_o` | 8.4 / 77.2 | 11.7 / 70.9 | Realistic expansion of task exposures. |
| **`MODERATE_COPILOT`** | `scenario_outlook` | `TRANSFORMING` | `TRANSFORMING` | Consistent upside workflow evolution. |
| **`MODERATE_COPILOT`** | `sensitivity` | `HIGHLY SENSITIVE` (spurious) | `ROBUST` (`UPSIDE_TRANSFORMATION`) | P2-1 defect resolved. |
| **`FAST_AGENTIC`** | `eff_ai` / `auto_p` / `aug_o` | 100.0 / 15.9 / 84.0 | 100.0 / 15.2 / 75.2 | High AI pressure with controlled automation. |
| **`FAST_AGENTIC`** | `reskilling_urgency` | `HIGH` | `MODERATE` | Reflects high demand resilience (78.2). |

### 2.2 General Office Clerks (`4110`) — Severe Automation Benchmark
| Scenario | Metric | M6 v1.0.0 (Legacy) | M6 v1.1.0 (Remediated) | Key Change |
| :--- | :--- | :---: | :---: | :--- |
| **`REFERENCE_2026`** | `eff_ai` / `auto_p` / `aug_o` | 38.0 / 30.0 / 8.0 | 38.0 / 30.0 / 8.0 | Exact baseline identity preserved. |
| **`MODERATE_COPILOT`** | `eff_ai` | **36.5** (INVERTED!) | **53.2** | P1-1 defect resolved. |
| **`MODERATE_COPILOT`** | `auto_p` (lower bound) | **24.1** (INVERTED BELOW REF 30.0!) | **39.2** ($> 30.0$) | Monotonic scaling across all bounds. |
| **`FAST_AGENTIC`** | `auto_p` | 59.7 | 57.2 | Substantial substitution shock. |
| **`FAST_AGENTIC`** | `reskilling_urgency` | **`HIGH`** (failed to reach VERY HIGH) | **`VERY HIGH`** | P2-2 defect resolved. |
| **`FAST_AGENTIC`** | `scenario_outlook` | `HIGHLY PRESSURED` | `HIGHLY PRESSURED` | Stable, robust identification of displacement exposure. |

### 2.3 Major Group 2: Professionals (`MAJOR_2`) — Fallback Benchmark
| Scenario | Metric | M6 v1.0.0 (Legacy) | M6 v1.1.0 (Remediated) | Key Change |
| :--- | :--- | :---: | :---: | :--- |
| **`REFERENCE_2026`** | `scenario_outlook` | `RESILIENT` | `RESILIENT` | Baseline identity preserved. |
| **`MODERATE_COPILOT`** | `net_resilience` | 52.9 ($> 47.9$ Ref) | 52.8 ($> 48.0$ Ref) | Net resilience increases under Copilot. |
| **`MODERATE_COPILOT`** | `scenario_outlook` | **`PRESSURED`** (SPURIOUS FLIP!) | **`RESILIENT`** | P1-2 defect resolved; monotonicity holds. |
| **`FAST_AGENTIC`** | `scenario_outlook` | `PRESSURED` | `PRESSURED` | Genuine degradation under severe agentic shock. |
| **All Scenarios** | `quality_flags` | `['AGGREGATED_FALLBACK', 'MAJOR_GROUP_WAGE_CONTEXT', 'NO_ROLE_SPECIFIC_WAGE_DATA']` | `['AGGREGATED_MAJOR_GROUP_FALLBACK', 'GROUP_LEVEL_DIRECT_WAGE_MEASUREMENT']` | P1-4 wage flag cleanup resolved. |

---

## 3. Cryptographic Output Artifact Hashes (M6 v1.1.0)

| Artifact File | SHA-256 Checksum |
| :--- | :--- |
| `data/scenarios/scenario_definitions_v1_1.json` | `5c61d564cf94d87aa1bc19e7a8e53d5a57a070e62ae4be6a32d184cf4682fb06` |
| `data/scenarios/occupation_scenario_profiles_v1_1.json` | `64ea6ff91896d9e034078a6cb8250000a6f4e1f7601f7869389e0237b78bb4a2` |
| `data/scenarios/skill_scenario_profiles_v1_1.json` | `432dbb13beea5098ff99c8bf27514a348ea3c489c72e27b409ffaa53cb09f874` |
| `data/scenarios/scenario_build_manifest_v1_1.json` | `f28a95c3ae8f73111812bb3e9aaeb567be569300301389e47514a383d4677764` |
| `artifacts/m6_occupation_scenario_summary_v1_1.csv` | `05b4e724eaae0b4907db1aa2580ce6b09315d18d451244e8bc1bfa4439c1b48b` |
| `artifacts/m6_skill_scenario_summary_v1_1.csv` | `6ae9a9cbaea5a9d2c206f6b5bfe3e390c5fa6261555fe82d5a2d1d07c34b6b69` |
