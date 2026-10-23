# M6 Occupational Granularity & Wage Quality Flag Report (v1.1.0)

**Audit Subject**: P1-4 Resolution — Granularity Separation & Wage Flag Cleanup  
**Engine Version**: M6 v1.1.0  
**Target Output**: [`occupation_scenario_profiles_v1_1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1_1.json)

---

## 1. Problem Statement: Granularity Conflation in v1.0.0

In M6 v1.0.0:
- 20 specific 4-digit occupations and 8 one-digit Major Group fallback entities were combined into a single pooled $N=28$ distribution table.
- This masked the fact that **8 out of the 10 `PRESSURED` occupations** in `MODERATE_COPILOT` and `FAST_AGENTIC` were actually 1-digit fallback entities (`MAJOR_1` through `MAJOR_9`), rather than specific career roles.
- Furthermore, 1-digit Major Group entities incorrectly inherited 4-digit role flags:
  - `MAJOR_GROUP_WAGE_CONTEXT`
  - `NO_ROLE_SPECIFIC_WAGE_DATA`
  - Duplicate `AGGREGATED_FALLBACK` / `AGGREGATE_MAJOR_GROUP` flags.

---

## 2. Stage 10C Granularity Architectural Standard

In M6 v1.1.0, every occupational record explicitly carries the `entity_granularity` field:
- **`FOUR_DIGIT_OCCUPATION`** ($N=20$): Granular occupational entities corresponding to MASCO 4-digit codes (e.g., `2512 Software Developers`, `4110 General Office Clerks`, `2151 Electrical Engineers`).
- **`ONE_DIGIT_MAJOR_GROUP_FALLBACK`** ($N=8$): High-level MASCO Major Group aggregate profiles (`MAJOR_1` to `MAJOR_9`).

### Quality Flag Cleanup:
- **For `FOUR_DIGIT_OCCUPATION`**:
  - `quality_flags`: `["MAJOR_GROUP_WAGE_CONTEXT", "NO_ROLE_SPECIFIC_WAGE_DATA"]` (plus proxy crosswalk flags where applicable). Accurately warns downstream consumers that wage momentum is inherited from the 1-digit Major Group.
- **For `ONE_DIGIT_MAJOR_GROUP_FALLBACK`**:
  - `quality_flags`: `["AGGREGATED_MAJOR_GROUP_FALLBACK", "GROUP_LEVEL_DIRECT_WAGE_MEASUREMENT"]`.
  - Removed misleading `NO_ROLE_SPECIFIC_WAGE_DATA` (since DOSM wage data is measured directly at the 1-digit Major Group level) and eliminated duplicate fallback flags.

---

## 3. Disaggregated Scenario Outlook Distributions (M6 v1.1.0)

| Scenario | Granularity Tier | Total | `STRONGLY RESILIENT` | `RESILIENT` | `TRANSFORMING` | `PRESSURED` | `HIGHLY PRESSURED` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | **4-Digit Occupations** | **20** | **11** | **6** | **0** | **0** | **3** |
| **`REFERENCE_2026`** | **Major-Group Fallbacks** | **8** | **0** | **8** | **0** | **0** | **0** |
| *`REFERENCE_2026`* | *Combined System Total* | *28* | *11* | *14* | *0* | *0* | *3* |
| **`MODERATE_COPILOT`** | **4-Digit Occupations** | **20** | **9** | **4** | **2** | **2** | **3** |
| **`MODERATE_COPILOT`** | **Major-Group Fallbacks** | **8** | **0** | **8** | **0** | **0** | **0** |
| *`MODERATE_COPILOT`* | *Combined System Total* | *28* | *9* | *12* | *2* | *2* | *3* |
| **`FAST_AGENTIC`** | **4-Digit Occupations** | **20** | **7** | **4** | **4** | **2** | **3** |
| **`FAST_AGENTIC`** | **Major-Group Fallbacks** | **8** | **0** | **0** | **0** | **8** | **0** |
| *`FAST_AGENTIC`* | *Combined System Total* | *28* | *7* | *4* | *4* | *10* | *3* |

---

## 4. Downstream M3 Fallback Neutrality Contract

1. **Primary Candidate Pool**: M3 Role Matching must rank candidate occupations strictly from the `FOUR_DIGIT_OCCUPATION` pool ($N=20$).
2. **Exclusion of Fallbacks from Direct Competition**: `ONE_DIGIT_MAJOR_GROUP_FALLBACK` entities ($N=8$) must **never compete** as standard candidate recommendations alongside specific occupations.
3. **Restricted Use Cases for Fallbacks**:
   - Fallback profiles may be used only when a worker's target role has no direct 4-digit mapping in the system.
   - When a fallback profile is referenced, its scenario adjustment modifier is dampened by $0.5\times$ and flagged with `AGGREGATED_MAJOR_GROUP_FALLBACK`.
