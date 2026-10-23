# M6 Scenario Sensitivity & Parameter Uncertainty Analysis (v1.0.0)

**Author:** Senior Workforce Foresight Engineer & Statistical Reviewer  
**Date:** 2026-10-23  
**Status:** **AUTHORITATIVE UNCERTAINTY AUDIT**  
**Data Reference:** [occupation_scenario_profiles_v1.json](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json), [skill_scenario_profiles_v1.json](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json)  

---

## 1. Executive Summary: Why Scenario Ranges Are Not Confidence Intervals

In traditional econometrics, statistical confidence intervals quantify sampling variance around a known historical distribution. In workforce technology foresight, however:
- **There is no 2030 empirical ground truth.**
- Future outcomes are driven by discretionary corporate adoption choices, technological breakthroughs, and policy interventions.

Therefore, M6 defines deterministic **Scenario Assumption Ranges** across `lower`, `central`, and `upper` parameter bounds. These ranges measure **Sensitivity to Technological Velocity**, not frequentist sampling error.

---

## 2. Sensitivity Classification Framework

Every occupation and skill profile is evaluated across its scenario parameter bounds and assigned one of three sensitivity tiers:
1. **`ROBUST`**: The entity retains the identical scenario outlook tier across all three bounds (`lower`, `central`, `upper`).
2. **`MODERATELY SENSITIVE`**: The entity shifts by at most 1 adjacent outlook tier across bounds (e.g., `STRONGLY RESILIENT` $\leftrightarrow$ `RESILIENT`, or `PRESSURED` $\leftrightarrow$ `HIGHLY PRESSURED`).
3. **`HIGHLY SENSITIVE`**: The entity shifts by $\ge 2$ tiers across bounds (e.g., `RESILIENT` at lower bound $\to$ `TRANSFORMING` at central $\to$ `PRESSURED` at upper bound).

---

## 3. Occupation Sensitivity Distribution Across Scenarios

| Scenario ID | Total Profiles | ROBUST Count (%) | MODERATELY SENSITIVE (%) | HIGHLY SENSITIVE (%) |
| :--- | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | 28 | **28 (100.0%)** | 0 (0.0%) | 0 (0.0%) |
| **`MODERATE_COPILOT`** | 28 | **23 (82.1%)** | 1 (3.6%) | 4 (14.3%) |
| **`FAST_AGENTIC`** | 28 | **20 (71.4%)** | 2 (7.1%) | 6 (21.4%) |

### A. Highly Sensitive Occupations Under `FAST_AGENTIC`
The following 6 occupations exhibit high sensitivity ($\Delta \text{tier} \ge 2$) depending on the exact velocity of agentic tool reach:
1. **MASCO 2512 (Software Developers)**:
   - Lower Bound: `RESILIENT` (Automation pressure 13.9, Augmentation 77.2)
   - Central Bound: `TRANSFORMING` (Automation pressure 15.9, Augmentation 84.0)
   - Upper Bound: `TRANSFORMING` (Automation pressure 18.2, Augmentation 91.5)
   - *Driver*: Extreme sensitivity to the balance between coding agent substitution vs. architectural augmentation leverage.
2. **MASCO 2511 (Systems Analysts)**:
   - Lower Bound: `STRONGLY RESILIENT` $\to$ Central: `TRANSFORMING`.
3. **MASCO 2519 (Software & Applications Developers NEC)**:
   - Shifts between `RESILIENT` and `TRANSFORMING`.
4. **MASCO 2529 (Database & Network Specialists / AI Specialists)**:
   - Shifts between `STRONGLY RESILIENT` and `TRANSFORMING`.
5. **MASCO 2166 (Graphic & Multimedia Designers)**:
   - Lower Bound: `RESILIENT` $\to$ Central: `PRESSURED` $\to$ Upper: `HIGHLY PRESSURED`.
   - *Driver*: Highly vulnerable to generative diffusion breadth and autonomous multi-modal agent capabilities.
6. **MASCO 3514 (Web Technicians & Cloud Application Support)**:
   - Shifts between `RESILIENT` and `PRESSURED`.

### B. Highly Robust Occupations (Invariant Across Bounds)
1. **Physical / Hardware Engineering**:
   - `2151 Electrical Engineers`: Invariant `STRONGLY RESILIENT` across all bounds.
   - `2152 Electronic Engineers (Semiconductor IC Design)`: Invariant `STRONGLY RESILIENT`.
   - `2143 Environmental Engineers & Sustainability`: Invariant `STRONGLY RESILIENT`.
2. **High-Shortage Strategic Governance**:
   - `2411 Accountants & Financial Auditors`: Invariant `STRONGLY RESILIENT` (buffered by $89.6$ shortage level and regulatory compliance requirements).
   - `1330 ICT Services Managers`: Invariant `STRONGLY RESILIENT`.
3. **High-Routine Clerical Roles**:
   - `4110 General Office Clerks`: Invariant `HIGHLY PRESSURED`.
   - `4311 Accounting & Bookkeeping Clerks`: Invariant `HIGHLY PRESSURED`.

---

## 4. Skill Sensitivity Distribution Across Scenarios

| Scenario ID | Total Skills | ROBUST Count (%) | MODERATELY SENSITIVE (%) | HIGHLY SENSITIVE (%) |
| :--- | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | 16 | **16 (100.0%)** | 0 (0.0%) | 0 (0.0%) |
| **`MODERATE_COPILOT`** | 16 | **9 (56.2%)** | 0 (0.0%) | 7 (43.8%) |
| **`FAST_AGENTIC`** | 16 | **7 (43.8%)** | 7 (43.8%) | 2 (12.5%) |

### A. Most Sensitive Skills Under Accelerating AI
- **`sql_data_analysis` & `python_scripting`**: Under Moderate Copilot, these skills receive massive augmentation (`TRANSFORMING`). Under Fast Agentic upper bounds, autonomous code-generation agents substitute routine querying, shifting them toward `PRESSURED`.
- **`ai_literacy` & `prompt_engineering`**: Invariant in their transformation imperative (`TRANSFORMING`), with reskilling urgency remaining `HIGH`.

---

## 5. Audit Conclusion

The sensitivity audit confirms:
- Zero instability in the reference baseline (`100% ROBUST`).
- 71.4% of occupations remain robust under Fast Agentic AI, with sensitivity concentrated precisely in the roles undergoing structural task re-engineering (software development, multimedia design, and junior technical support).
- Uncertainty bounds transparently communicate parameter variance without misleading probability claims.
