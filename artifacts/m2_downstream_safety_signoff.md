# M2 Downstream Safety Sign-Off: M3 Role Matching & M6 Scenario Engine

**Author:** Independent Senior Quantitative Methodology Reviewer & Systems Architect  
**Date:** 2026-10-23  
**Target Version:** M2 Trend Intelligence v1.1.0  
**Interface Status:** **APPROVED WITH BOUNDARY RESTRICTIONS**

---

## 1. Permitted Downstream Consumption for M3 Role Matching

The M3 Role Matching Engine is authorized to ingest the following fields from M2 v1.1 profiles:
1. **10-Dimensional Component Vector**:
   - `demand_shortage_index`, `demand_momentum_index`, `employment_wage_index`, `research_momentum_index`, `ai_exposure_index`, `automation_index`, `augmentation_index`, `policy_priority_index`.
2. **Categorical & Strategic Metrics**:
   - `overall_outlook`: 5-tier classification (`STRONGLY RISING`, `RISING`, `STABLE`, `DECLINING`, `STRONGLY DECLINING`).
   - `confidence_index` & `confidence_label`: (`HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`).
3. **Traceability & Governance Metadata**:
   - `quality_flags`: `MAJOR_GROUP_WAGE_CONTEXT`, `NO_ROLE_SPECIFIC_WAGE_DATA`, `LOW_SOURCE_COUNT`, `LOW_BASE_RESEARCH_SIGNAL`, `AGING_DATA`.
   - `wage_granularity`, `wage_context_code`, `wage_context_label`, `source_measurement_level`.
   - `top_positive_drivers`, `top_negative_drivers`, `uncertainties`.

---

## 2. Enforced Architectural Prohibitions for M3

To preserve scientific validity and protect candidates, M3 must strictly enforce the following negative constraints:

### Constraint A: Prohibition of Raw Exposure Penalization
- **Violation**: Treating high `ai_exposure_index` as an inherently negative penalty on career viability.
- **Rule**: M3 must evaluate the **Augmentation-to-Automation Ratio**:
  $$R_{\text{aug/auto}} = \frac{\text{Augmentation Potential}}{\text{Automation Potential}}$$
  - If $R_{\text{aug/auto}} \ge 2.0$, AI exposure functions as a positive multiplier of career longevity and talent value (e.g., Software Developers 2512 with $R = 6.75$).
  - Only when $R_{\text{aug/auto}} \le 1.0$ and demand is stagnant (e.g., General Office Clerks 4110) may M3 recommend transition out of the role.

### Constraint B: Prohibition of Salary Inference from Contextual Wage Indices
- **Violation**: Converting `employment_wage_index` into an estimated starting salary or compensation offer.
- **Rule**: M2 wage metrics are derived from **1-digit MASCO Major Groups** (OpenDOSM). M3 is strictly barred from presenting these indices as 4-digit occupational salaries. Wage momentum may only serve as an environmental health factor ($w \le 0.15$).

### Constraint C: Mandatory Exposure of Confidence Limitations
- **Rule**: If a skill carries `confidence_label == "LOW"` or the flag `LOW_BASE_RESEARCH_SIGNAL` (e.g., `prompt_engineering`, `rag_knowledge_systems`), M3 must down-weight its match score contribution by $50\%$ and surface a UI advisory: *"Emerging micro-credential with high research velocity but limited long-term institutional tenure."*

---

## 3. Permitted Interactions for M6 Scenario Engine

1. **Decoupled Scenario Overlays**: M6 may simulate future policy interventions or technological accelerations by modifying scenario assumptions, but must NEVER alter historical baseline observations.
2. **Major Group Shock Propagation**: Macroeconomic wage adjustments during stress tests must propagate at the 1-digit Major Group level, preventing ungrounded role-level salary variance.
3. **Uncertainty Bounds**: M6 workforce projections must incorporate wider confidence intervals ($\pm 25\%$) for any role or skill flagged with `LOW_SOURCE_COUNT` or `LOW_BASE_RESEARCH_SIGNAL`.

---

## 4. Formal Sign-Off

The safety contracts for M3 and M6 are complete, rigorous, and formally approved. Downstream module development may proceed within these boundaries once the targeted OpenAlex formula reconciliation (v1.1.1) is finalized.
