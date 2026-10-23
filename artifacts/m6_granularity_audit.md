# M6 Granularity, Confidence & Low-Base Audit Report (Audits 15–18)

**Audit Stage**: Stage 10B — M6 Future Workforce Scenario Engine v1.0.0 Methodology Review  
**Target Outputs**: [`occupation_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json), [`skill_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json)

---

## 1. Audit 15 — Confidence Preservation Audit (`VALID`)

Forensic check across all $28 \times 3 = 84$ occupation-scenario records and $16 \times 3 = 48$ skill-scenario records against frozen M2 v1.1.1 ([`occupation_trend_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/trends/processed/occupation_trend_profiles_v1.json) and [`skill_trend_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/trends/processed/skill_trend_profiles_v1.json)):

- **Occupation Confidence**:
  - `m2_evidence_confidence_score` and `m2_evidence_confidence_Level` match M2 v1.1.1 identically (`0` mismatches).
  - Distribution preserved across every scenario: **`15 HIGH` (`70.0–90.0`), `13 MEDIUM` (`60.0`), `0 LOW`**.
  - Specifically, all 8 `MAJOR_1..9` fallback profiles and all 5 proxy-crosswalked 4-digit occupations (`2411, 2421, 2422, 2423, 2424`) remain capped at **`MEDIUM (60.0)`** (`P1-2` from Stage 9D/9E preserved).
- **Skill Confidence**:
  - `m2_evidence_confidence_score` and `m2_evidence_confidence_level` match M2 v1.1.1 identically (`0` mismatches).
  - Distribution preserved across every scenario: **`12 HIGH` (`80.0`), `3 MEDIUM` (`60.0`), `1 LOW` (`40.0` — `prompt_engineering`)**.
- **Confidence Separation**:
  - M6 exposes `m2_evidence_confidence_score` (empirical M2 signal quality) and `scenario_sensitivity_band` (`ROBUST`, `MODERATELY SENSITIVE`, `HIGHLY SENSITIVE` under assumption bounds) as two distinct fields and never averages or conflates them.

---

## 2. Audit 16 — OpenAlex Low-Base Flag Propagation (`P2-1` Prose Discrepancy)

Forensic check of `quality_flags` in [`skill_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json) vs [`skill_trend_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/trends/processed/skill_trend_profiles_v1.json):

| Skill ID | M2 `research_momentum` | M2 OpenAlex $N_{\text{base}}$ | M2 `quality_flags` | M6 `quality_flags` in `skill_scenario_profiles_v1.json` | Mentioned in Stage 10A Prose? |
| :--- | :---: | :---: | :--- | :--- | :---: |
| `human_in_the_loop_qa` | `50.0` (neutral fallback) | `0` | `['LOW_SAMPLE_SIZE', 'INSUFFICIENT_HISTORICAL_BASELINE']` | `['LOW_SAMPLE_SIZE', 'INSUFFICIENT_HISTORICAL_BASELINE']` | Yes |
| `carbon_footprint_analytics` | `78.9` | `0` | `['INSUFFICIENT_HISTORICAL_BASELINE']` | `['INSUFFICIENT_HISTORICAL_BASELINE']` | Yes |
| `data_visualization` | `78.5` | `0` | `['INSUFFICIENT_HISTORICAL_BASELINE']` | `['INSUFFICIENT_HISTORICAL_BASELINE']` | **No (Omitted in prose)** |
| `api_integration` | `83.2` | `0` | `['INSUFFICIENT_HISTORICAL_BASELINE']` | `['INSUFFICIENT_HISTORICAL_BASELINE']` | **No (Omitted in prose)** |

- **Finding**:
  - The JSON data in [`skill_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json) is **100% faithful** to M2 v1.1.1: all **4 / 16 skills** with $N_{\text{base}} = 0$ (`w_vol = 0.0`) carry `INSUFFICIENT_HISTORICAL_BASELINE`, and `human_in_the_loop_qa` (`research_momentum == 50.0`) uses the neutral-fallback weight adjustment.
  - However, Stage 10A narrative reports ([`stage10a_m6_scenario_engine_report.md`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/stage10a_m6_scenario_engine_report.md)) stated that only 2 skills carried `INSUFFICIENT_HISTORICAL_BASELINE`.
  - **Stage 10C Action (`P2-1`)**: Update all M6 narrative documentation to list all 4 skills (`data_visualization`, `human_in_the_loop_qa`, `api_integration`, `carbon_footprint_analytics`).

---

## 3. Audit 17 — 4-Digit Occupations vs 1-Digit Major Group Fallbacks (`P1-4`)

### 3.1 Granularity-Separated Outlook Distributions
In [`occupation_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json), the 28 occupational entities consist of **20 specific 4-digit MASCO occupations** and **8 1-digit Major Group fallback aggregates (`MAJOR_1`–`MAJOR_9`)**. Stage 10A summary tables pooled all 28 entities together. Separating them reveals a major structural distortion:

| Scenario | Entity Granularity Tier | `STRONGLY RESILIENT` | `RESILIENT` | `TRANSFORMING` | `PRESSURED` | `HIGHLY PRESSURED` | Total |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | **4-Digit Specific Occupations** | 12 | 5 | 0 | 1 | 2 | **20** |
| **`REFERENCE_2026`** | **1-Digit Major Group Fallbacks** | 0 | **8** | 0 | 0 | 0 | **8** |
| **`REFERENCE_2026`** | *Pooled Total (Reported in 10A)* | *12* | *13* | *0* | *1* | *2* | *28* |
| **`MODERATE_COPILOT`** | **4-Digit Specific Occupations** | 10 | 3 | 2 | **2** | 3 | **20** |
| **`MODERATE_COPILOT`** | **1-Digit Major Group Fallbacks** | 0 | 0 | 0 | **8** | 0 | **8** |
| **`MODERATE_COPILOT`** | *Pooled Total (Reported in 10A)* | *10* | *3* | *2* | *10* | *3* | *28* |
| **`FAST_AGENTIC`** | **4-Digit Specific Occupations** | 7 | 2 | 6 | **2** | 3 | **20** |
| **`FAST_AGENTIC`** | **1-Digit Major Group Fallbacks** | 0 | 0 | 0 | **8** | 0 | **8** |
| **`FAST_AGENTIC`** | *Pooled Total (Reported in 10A)* | *7* | *2* | *6* | *10* | *3* | *28* |

### 3.2 Why Pooling Distorts Scenario Interpretation (`P1-4` + `P1-2`)
1. **80% of `PRESSURED` Occupations Are Major Group Fallbacks**: In both `MODERATE_COPILOT` and `FAST_AGENTIC`, 8 out of the 10 `PRESSURED` entities are `MAJOR_1` through `MAJOR_9`. Only 2 specific 4-digit roles (`2166 Graphic Designers` and `3514 Web Technicians`) are `PRESSURED`.
2. **Spurious Regime Flip on Major Groups**: As proven in [`m6_formula_audit.md`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m6_formula_audit.md), all 8 Major Groups have `net_res` between `42.6` and `52.3` in `REFERENCE_2026` (where M2 labels them `RESILIENT`) and between `47.5` and `53.8` in `MODERATE_COPILOT` (where M6's `net_res < 55.0` threshold labels them `PRESSURED`). Thus their `net_resilience` **increased** in `MODERATE_COPILOT`, yet their outlook degraded from `RESILIENT` to `PRESSURED`.
3. **Downstream M3 Risk**: If M3 applies a `PRESSURED` penalty to any role falling back to `MAJOR_1` (Managers) or `MAJOR_2` (Professionals), fallback roles will be systematically down-ranked compared to 4-digit roles in the same Major Group.

---

## 4. Audit 18 — Wage Granularity Flag Audit (`P1-4`)

Inspection of `quality_flags` and `granularity_flags` in [`occupation_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json):

| Entity Cohort | Count | Current `quality_flags` in M6 v1.0.0 | Current `granularity_flags` in M6 v1.0.0 | Audit Verdict |
| :--- | :---: | :--- | :--- | :--- |
| **4-Digit Specific Roles (Direct Crosswalk)** | 15 | `['MAJOR_GROUP_WAGE_CONTEXT', 'NO_ROLE_SPECIFIC_WAGE_DATA']` | `['4_DIGIT_OCCUPATION']` | **`VALID`**: Accurately warns M3 that DOSM wage signals are inherited from 1-digit MASCO Major Group. |
| **4-Digit Specific Roles (Proxy Crosswalk: `2411, 2421, 2422, 2423, 2424`)** | 5 | `['PROXY_OCCUPATION_CROSSWALK', 'MAJOR_GROUP_WAGE_CONTEXT', 'NO_ROLE_SPECIFIC_WAGE_DATA']` | `['4_DIGIT_OCCUPATION']` | **`VALID`**: Accurately flags both proxy crosswalk and 1-digit wage inheritance. |
| **1-Digit Major Group Fallbacks (`MAJOR_1..9`)** | 8 | `['AGGREGATED_FALLBACK', 'MAJOR_GROUP_WAGE_CONTEXT', 'NO_ROLE_SPECIFIC_WAGE_DATA', 'AGGREGATE_MAJOR_GROUP']` | `['1_DIGIT_MAJOR_GROUP_FALLBACK']` | **`DEFECT (P1-4)`**: Misattributes role-level wage flags to group-level entities and duplicates `AGGREGATED_FALLBACK` / `AGGREGATE_MAJOR_GROUP`. |

### Stage 10C Remediation Specification for `P1-4`
1. **Separate Reporting Tables**: All M6 summary artifacts and metadata must report `4_DIGIT_OCCUPATION` ($N=20$) and `1_DIGIT_MAJOR_GROUP_FALLBACK` ($N=8$) distributions in separate tables.
2. **Clean Up Major Group Quality Flags**:
   - For `MAJOR_1..9` (`is_fallback == True`), replace `MAJOR_GROUP_WAGE_CONTEXT` and `NO_ROLE_SPECIFIC_WAGE_DATA` with `GROUP_LEVEL_DIRECT_WAGE_MEASUREMENT` (since 1-digit DOSM MASCO wage statistics are direct measurements for 1-digit Major Groups, while remaining coarse for any individual 4-digit occupation mapped to that fallback), and deduplicate `AGGREGATED_FALLBACK` / `AGGREGATE_MAJOR_GROUP` into a single canonical flag `AGGREGATED_MAJOR_GROUP_FALLBACK`.
   - Retain `['MAJOR_GROUP_WAGE_CONTEXT', 'NO_ROLE_SPECIFIC_WAGE_DATA']` on all 20 4-digit occupations.
