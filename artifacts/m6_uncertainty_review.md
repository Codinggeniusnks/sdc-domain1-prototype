# M6 Uncertainty, Sensitivity & Rank-Stability Review (Audits 19–21, 26)

**Audit Stage**: Stage 10B — M6 Future Workforce Scenario Engine v1.0.0 Methodology Review  
**Target Files**: [`m6_sensitivity_audit.md`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m6_sensitivity_audit.md), [`occupation_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json), [`skill_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json)

---

## 1. Audit 19 — Lower / Central / Upper Bound Monotonicity Audit

Forensic check across all $28 \times 3 = 84$ occupation records and $16 \times 3 = 48$ skill records:

### 1.1 Within-Scenario Bound Ordering (`lower <= central <= upper`)
- **Occupations (`84 / 84` pass)**:
  - `automation_pressure_range`: `lower <= central <= upper` holds for all 84 records (`0` inversions).
  - `augmentation_opportunity_range`: `lower <= central <= upper` holds for all 84 records (`0` inversions).
  - `demand_resilience_range`: `lower <= central <= upper` holds for all 84 records (`0` inversions).
  - `transition_pressure_range`: `lower <= central <= upper` holds for all 84 records (`0` inversions).
- **Skills (`48 / 48` pass)**:
  - All 4 range fields satisfy `lower <= central <= upper` across all 48 records (`0` inversions).

### 1.2 Two Structural Defects in Range Construction (`P1-1` & Zero-Width `REFERENCE_2026`)
1. **Collapsed Zero-Width Intervals in `REFERENCE_2026`**:
   - Because [`get_scenario_multipliers()`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L59-L68) hardcodes `1.0` and `policy_factor = 0.40` whenever `scenario_id == "REFERENCE_2026"`, ignoring the `lower` (`[15, 5, 15, 20, 15, 20, 30]`) and `upper` (`[25, 15, 25, 40, 35, 40, 50]`) parameter bounds in [`scenario_assumptions_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/scenario_assumptions_v1.json), every single `REFERENCE_2026` range has **zero width** (`lower == central == upper`, e.g., `2512` `trans_p = [20.2, 20.2, 20.2]`).
2. **Cross-Scenario Lower-Bound Inversion (`P1-1`)**:
   - In `MODERATE_COPILOT`, `lower` bound has `auto_mult = 0.8017` and `ai_press_mult = 0.7349`. As a result, `MODERATE_COPILOT` lower-bound `automation_pressure` is **20% lower than `REFERENCE_2026`** across all 28 occupations and 16 skills (e.g., `4110` `auto_p` is `30.0` in `REFERENCE_2026` but `[24.1, 31.4, 38.7]` in `MODERATE_COPILOT`).

---

## 2. Audit 20 — Sensitivity Band Classification & Prose-vs-JSON Verification (`P2-1`)

### 2.1 Why High-Resilience Technical Roles Are Flagged `HIGHLY SENSITIVE`
In [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L38-L44):
```python
OUTLOOK_ORDER = {
    "STRONGLY RESILIENT": 1,
    "RESILIENT": 2,
    "TRANSFORMING": 3,
    "PRESSURED": 4,
    "HIGHLY PRESSURED": 5
}
```
And in [`determine_occupation_outlook()`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L99-L115), the `TRANSFORMING` check (`if task_trans >= 42.0 and aug_o >= 45.0: return "TRANSFORMING"`) executes **before** the `STRONGLY RESILIENT` check (`if net_res >= 75.0 and auto_p < 20.0: return "STRONGLY RESILIENT"`).
- Consequently, when a strong technical role (`2511, 2512, 2519, 2521, 2529, 2411, 2421`) has `net_res >= 75.0` and `auto_p < 20.0`, it is `STRONGLY RESILIENT` (`1`) whenever `task_trans < 42.0` (at the lower bound) and jumps to `TRANSFORMING` (`3`) as soon as `task_trans >= 42.0` (at the central or upper bound).
- Because `|3 - 1| = 2`, [`compute_sensitivity()`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L135-L143) classifies any transition between `STRONGLY RESILIENT` and `TRANSFORMING` as **`HIGHLY SENSITIVE`**, even though the role is never at risk of becoming `PRESSURED` (`4`) or `HIGHLY PRESSURED` (`5`).

### 2.2 Complete Verified Table of Non-`ROBUST` Entities (JSON Truth vs Stage 10A Prose Errors)

Forensic comparison of the actual JSON records against [`artifacts/m6_sensitivity_audit.md`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m6_sensitivity_audit.md) revealed that while the **aggregate counts** in Stage 10A were right (`23/4/1` and `20/2/6` for occupations; `14/0/2` and `7/7/2` for skills), the **specific entity names cited in the Stage 10A prose for `FAST_AGENTIC` were wrong**:

#### A. Occupations — Non-`ROBUST` Entities in JSON
| Scenario | Code | Title | `L` Outlook | `C` Outlook | `U` Outlook | JSON `sensitivity_band` | Stage 10A Prose Claim in `m6_sensitivity_audit.md` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MODERATE_COPILOT` | `2512` | Software Developers | `STRONGLY RESILIENT` | `TRANSFORMING` | `TRANSFORMING` | `HIGHLY SENSITIVE` | Listed correctly |
| `MODERATE_COPILOT` | `2511` | Systems Analysts | `STRONGLY RESILIENT` | `STRONGLY RESILIENT` | `TRANSFORMING` | `HIGHLY SENSITIVE` | Listed correctly |
| `MODERATE_COPILOT` | `2529` | Database & Network Profs | `STRONGLY RESILIENT` | `STRONGLY RESILIENT` | `TRANSFORMING` | `HIGHLY SENSITIVE` | Listed correctly |
| `MODERATE_COPILOT` | `2519` | Software & App Dev NEC | `STRONGLY RESILIENT` | `STRONGLY RESILIENT` | `TRANSFORMING` | `HIGHLY SENSITIVE` | Listed correctly |
| `MODERATE_COPILOT` | `2424` | Training & Staff Dev Profs | `RESILIENT` | `RESILIENT` | `TRANSFORMING` | `MODERATELY SENSITIVE` | Listed correctly |
| `FAST_AGENTIC` | `2511` | Systems Analysts | `STRONGLY RESILIENT` | `TRANSFORMING` | `TRANSFORMING` | **`HIGHLY SENSITIVE`** | **Omitted in prose** |
| `FAST_AGENTIC` | `2521` | Database Designers & Admins | `STRONGLY RESILIENT` | `TRANSFORMING` | `TRANSFORMING` | **`HIGHLY SENSITIVE`** | **Omitted in prose** |
| `FAST_AGENTIC` | `2529` | Database & Network Profs | `STRONGLY RESILIENT` | `TRANSFORMING` | `TRANSFORMING` | **`HIGHLY SENSITIVE`** | Listed |
| `FAST_AGENTIC` | `2519` | Software & App Dev NEC | `STRONGLY RESILIENT` | `TRANSFORMING` | `TRANSFORMING` | **`HIGHLY SENSITIVE`** | **Omitted in prose** |
| `FAST_AGENTIC` | `2411` | Accountants & Auditors | `STRONGLY RESILIENT` | `TRANSFORMING` | `TRANSFORMING` | **`HIGHLY SENSITIVE`** | Listed |
| `FAST_AGENTIC` | `2421` | Management & Org Analysts | `STRONGLY RESILIENT` | `STRONGLY RESILIENT` | `TRANSFORMING` | **`HIGHLY SENSITIVE`** | Listed |
| `FAST_AGENTIC` | `2422` | Policy Admin Professionals | `RESILIENT` | `RESILIENT` | `TRANSFORMING` | **`MODERATELY SENSITIVE`** | **Omitted in prose** |
| `FAST_AGENTIC` | `2424` | Training & Staff Dev Profs | `RESILIENT` | `TRANSFORMING` | `TRANSFORMING` | **`MODERATELY SENSITIVE`** | **Omitted in prose** |

> [!WARNING]
> Stage 10A [`m6_sensitivity_audit.md`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m6_sensitivity_audit.md) falsely listed `2512 Software Developers`, `2166 Graphic Designers`, and `3514 Web Technicians` as `HIGHLY SENSITIVE` in `FAST_AGENTIC`. In the actual JSON, `2512` (`L/C/U = TRANSFORMING`), `2166` (`L/C/U = PRESSURED`), and `3514` (`L/C/U = PRESSURED`) are all **`ROBUST`** in `FAST_AGENTIC`!

#### B. Skills — Non-`ROBUST` Entities in JSON
| Scenario | Skill ID | `L` Outlook | `C` Outlook | `U` Outlook | JSON `sensitivity_band` | Stage 10A Prose Claim in `m6_sensitivity_audit.md` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MODERATE_COPILOT` | `human_in_the_loop_qa` | `STRONGLY RESILIENT` | `TRANSFORMING` | `TRANSFORMING` | `HIGHLY SENSITIVE` | Listed correctly |
| `MODERATE_COPILOT` | `instructional_design` | `STRONGLY RESILIENT` | `STRONGLY RESILIENT` | `PRESSURED` | `HIGHLY SENSITIVE` | Listed correctly |
| `FAST_AGENTIC` | `esg_sustainability_reporting` | `STRONGLY RESILIENT` | `STRONGLY RESILIENT` | `TRANSFORMING` | **`HIGHLY SENSITIVE`** | **Omitted in prose** |
| `FAST_AGENTIC` | `carbon_footprint_analytics` | `STRONGLY RESILIENT` | `STRONGLY RESILIENT` | `TRANSFORMING` | **`HIGHLY SENSITIVE`** | **Omitted in prose** |
| `FAST_AGENTIC` | `ai_literacy` | `TRANSFORMING` | `TRANSFORMING` | `PRESSURED` | `MODERATELY SENSITIVE` | Omitted in prose |
| `FAST_AGENTIC` | `prompt_engineering` | `TRANSFORMING` | `TRANSFORMING` | `PRESSURED` | `MODERATELY SENSITIVE` | Omitted in prose |
| `FAST_AGENTIC` | `process_mapping` | `TRANSFORMING` | `TRANSFORMING` | `PRESSURED` | **`MODERATELY SENSITIVE`** | **Falsely claimed `HIGHLY SENSITIVE` in prose** |
| `FAST_AGENTIC` | `data_visualization` | `TRANSFORMING` | `PRESSURED` | `PRESSURED` | `MODERATELY SENSITIVE` | Omitted in prose |
| `FAST_AGENTIC` | `workflow_automation` | `TRANSFORMING` | `TRANSFORMING` | `PRESSURED` | `MODERATELY SENSITIVE` | Omitted in prose |
| `FAST_AGENTIC` | `stakeholder_communication` | `STRONGLY RESILIENT` | `RESILIENT` | `RESILIENT` | `MODERATELY SENSITIVE` | Omitted in prose |
| `FAST_AGENTIC` | `instructional_design` | `TRANSFORMING` | `PRESSURED` | `PRESSURED` | **`MODERATELY SENSITIVE`** | **Falsely claimed `HIGHLY SENSITIVE` in prose** |

---

## 3. Audit 21 — Spearman Rank-Correlation Audit (`P2-3`)

Exact Spearman rank correlations ($\rho$) computed across scenarios:

| Entity Cohort | Metric | `Ref` vs `Copilot` | `Ref` vs `Fast Agentic` | `Copilot` vs `Fast Agentic` | Methodological Interpretation |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **All 28 Occupations** | `automation_pressure` | `1.0000` | `1.0000` | `1.0000` | **Trivial scalar multiplication**: $x_i \cdot c$ preserves rank order identically when no saturation occurs. |
| **All 28 Occupations** | `augmentation_opportunity` | `1.0000` | `1.0000` | `1.0000` | **Trivial scalar multiplication**: $y_i \cdot c$ preserves rank order identically when no saturation occurs. |
| **All 28 Occupations** | `demand_resilience` | `0.9964` | `0.9968` | `0.9999` | Genuine multi-channel stability (`shortage + momentum + wage + policy * factor`). |
| **All 28 Occupations** | `transition_pressure` | `0.9799` | `0.9888` | `0.9859` | Genuine cross-scenario rank differentiation as high-augmentation roles rise in `task_trans`. |
| **All 28 Occupations** | `net_resilience` | `0.9877` | `0.9896` | `0.9856` | Genuine resilience re-ordering under agentic automation shock. |
| **20 4-Digit Occupations Only** | `demand_resilience` | `0.9967` | `0.9970` | `0.9999` | High structural stability among specific 4-digit roles. |
| **20 4-Digit Occupations Only** | `transition_pressure` | `0.9721` | `0.9880` | `0.9868` | Meaningful rank shift between copilot and agentic futures. |
| **20 4-Digit Occupations Only** | `net_resilience` | `0.9876` | `0.9895` | `0.9865` | Meaningful rank shift without chaotic rank inversion. |
| **All 16 Skills** | `automation_pressure` | `1.0000` | `1.0000` | `1.0000` | Trivial scalar multiplication (max skill `auto_p` is `35.8 < 100`). |
| **All 16 Skills** | `augmentation_opportunity` | `0.9993` | `0.9803` | `0.9830` | Slight rank compression at top due to `100.0` ceiling clipping on 8 skills. |
| **All 16 Skills** | `demand_resilience` | `0.9874` | `0.9903` | `0.9993` | Genuine multi-channel stability. |
| **All 16 Skills** | `transition_pressure` | `0.9867` | `0.9785` | `0.9623` | Genuine rank differentiation across scenarios. |
| **All 16 Skills** | `net_resilience` | `0.9897` | `0.9661` | `0.9617` | Genuine rank differentiation (`0.9617` Copilot vs Fast). |

- **Stage 10C Reporting Requirement (`P2-3`)**: Do not cite $\rho = 1.0000$ on `automation_pressure` or `augmentation_opportunity` as empirical validation of rank stability; report the multi-channel `transition_pressure` ($\rho = 0.962–0.989$) and `net_resilience` ($\rho = 0.962–0.990$) correlations instead, separated by 4-digit vs 1-digit granularity.
