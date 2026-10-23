# M6 Quality Flags & Granularity Propagation Audit (v1.0.0)

**Author:** Senior Quantitative Methodology Reviewer & Reproducibility Auditor  
**Date:** 2026-10-23  
**Status:** **PASSED — 100% QUALITY FLAG INTEGRITY VERIFIED**  
**Data Reference:** [occupation_scenario_profiles_v1.json](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json), [skill_scenario_profiles_v1.json](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json)  

---

## 1. Executive Summary & Propagation Mandate

Downstream scenario projections must not obscure data limitations or present synthetic assumptions as verified empirical observations. M6 enforces strict **Quality Flag Inheritance and Attribution Rules**:
1. All quality caveats from frozen M2 v1.1.1 must propagate unbroken.
2. New uncertainty arising from baseline research sparsity or aggregate occupational measurement must be explicitly tagged.
3. Wage granularity rules must strictly prohibit role-specific future salary predictions.

---

## 2. Quality Flag Inventory & Verification Matrix

| Quality Flag | Scope | Applied Count | Trigger Condition | Downstream Guidance for M3 / UI |
| :--- | :---: | :---: | :--- | :--- |
| **`MAJOR_GROUP_WAGE_CONTEXT`** | Occupations | **28 / 28 (100%)** | DOSM formal salaries are reported at 1-digit MASCO Major Group level, not 4-digit title level. | UI must display wage metrics as broad occupational group benchmarks; individual salary estimates are barred. |
| **`NO_ROLE_SPECIFIC_WAGE_DATA`** | Occupations | **28 / 28 (100%)** | No official 4-digit MASCO salary time-series exists in published DOSM releases. | Prohibits role-specific future wage forecasting or salary growth claims. |
| **`AGGREGATE_MAJOR_GROUP`** | Occupations | **8 / 28 (28.6%)** | Records corresponding to Major Groups 1 to 9 (`MAJOR_1` – `MAJOR_9`). | Indicates broad macroeconomic aggregate rather than specific hiring job title. |
| **`LOW_BASE_RESEARCH_SIGNAL`** | Skills | **9 / 16 (56.3%)** | OpenAlex 4-year baseline publication volume $N_{\text{baseline}} < 5$. | Informs candidate that research momentum reflects emerging velocity rather than mature consensus. |
| **`INSUFFICIENT_HISTORICAL_BASELINE`** | Skills | **2 / 16 (12.5%)** | OpenAlex baseline publication volume $N_{\text{baseline}} = 0$ (`human_in_the_loop_qa`, `data_visualization`). | Informs candidate that neutral research score ($50.0$) indicates lack of historical indexing, NOT lack of research interest. |
| **`LOW_SOURCE_COUNT`** | Skills | **2 / 16 (12.5%)** | Inherited from M2 for nascent skills (`prompt_engineering`, `rag_knowledge_systems`). | Highlights narrow primary source breadth. |

---

## 3. Forensic Audit of OpenAlex Sparse-Baseline Rule

### The $N_{\text{baseline}} = 0$ Governance Rule:
In M2 v1.1.1, when OpenAlex bibliometric records have zero publications between 2020 and 2023 ($N_{\text{baseline}} = 0$), the volume reliability weight evaluates to:
$$w_{\text{volume}} = \min\left(1.0, \frac{\ln(1 + 0)}{\ln(26)}\right) = 0.0$$
Consequently, the adjusted growth ratio collapses to $R_{\text{adjusted}} = 1.0$, which maps to the neutral structural baseline score of **`50.0`**.

### Critical M6 Rule:
A score of $50.0$ under $N_{\text{baseline}} = 0$ must **never be interpreted as empirical proof of neutral research momentum**. It is an artifact of low-base shrinkage.

### M6 Propagation Result:
- **`human_in_the_loop_qa`**:
  - Baseline Count: $N_{\text{baseline}} = 0$, $N_{\text{recent}} = 12$
  - Volume Shrinkage Weight: $0.0$
  - Score: $50.0$
  - Flag Attached: **`INSUFFICIENT_HISTORICAL_BASELINE`** (Verified in 3 / 3 scenarios).
- **`data_visualization`**:
  - Baseline Count: $N_{\text{baseline}} = 0$, $N_{\text{recent}} = 4$
  - Volume Shrinkage Weight: $0.0$
  - Score: $50.0$
  - Flag Attached: **`INSUFFICIENT_HISTORICAL_BASELINE`** (Verified in 3 / 3 scenarios).

---

## 4. Wage Granularity Safety Compliance

```
================================================================================
                    WAGE GRANULARITY COMPLIANCE VERIFICATION
================================================================================
  Rule 1: Role-specific future salary numbers?                   -> NONE GENERATED
  Rule 2: Specific salary growth rates forecasted?               -> NONE GENERATED
  Rule 3: Wage context labeled as 1-digit Major Group?          -> 100% LABELED
  Rule 4: NO_ROLE_SPECIFIC_WAGE_DATA flag present on all roles?  -> 28 / 28 (100%)
================================================================================
```

M6 maintains strict separation between macro wage context and occupational foresight, preventing misleading financial guarantees to career-transitioning workers.
