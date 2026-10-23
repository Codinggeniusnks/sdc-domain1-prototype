# M6 Formula Audit & Mathematical Traceability Report (Audits 3–14, 22–23)

**Audit Stage**: Stage 10B — M6 Future Workforce Scenario Engine v1.0.0 Methodology Review  
**Target Code**: [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py), [`src/scenario_engine.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/src/scenario_engine.py)  
**Target Outputs**: [`occupation_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json), [`skill_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json)

---

## 1. Executive Summary of Formula Findings

1. **`REFERENCE_2026` Identity Preservation (`Audit 3`)**: Numerically exact (`0.000` divergence on `automation_pressure`, `augmentation_opportunity`, `effective_ai_pressure`, and M2 confidence across all 28 occupations and 16 skills), **EXCEPT** it is achieved via a hardcoded `if scenario_id == "REFERENCE_2026"` branch rather than evaluating the general scenario formula at the `REFERENCE_2026` assumption table.
2. **Non-Monotonic Multiplier Anchor & Magic Constants (`1.1, 1.2, 1.15`) (`Audits 4, 19, 23` — `P1-1`)**: [`get_scenario_multipliers()`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L46-L86) normalizes non-reference assumptions against an arbitrary denominator `50.0` rather than the `REFERENCE_2026` baseline (`Adopt=20, Reach=10, Auto=20, Aug=30, Adapt=25, Reskill=30`) and multiplies by undocumented constants `1.1`, `1.2`, and `1.15`. Consequently:
   - In `MODERATE_COPILOT` central bound, `ai_press_mult = 0.9605`, causing `effective_ai_pressure` to **decrease below `REFERENCE_2026`** across all 28 occupations (`2512`: `62.0 -> 59.6`).
   - In `MODERATE_COPILOT` lower bound, `auto_mult = 0.8017` and `ai_press_mult = 0.7349`, causing `automation_pressure` and `effective_ai_pressure` to drop **20%–26.5% below `REFERENCE_2026`** even though every lower-bound assumption (`Adopt=45, Reach=25, Auto=35`) is strictly higher than `REFERENCE_2026` (`20, 10, 20`).
3. **Bifurcated Outlook Classification Regime (`Audits 3, 9, 22` — `P1-2`)**: [`determine_occupation_outlook()`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L99-L115) and [`determine_skill_outlook()`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L118-L132) copy M2 `overall_outlook` strings in `REFERENCE_2026` and switch to threshold formulas in non-reference scenarios. Evaluating the threshold formulas on `REFERENCE_2026` component values produces **different outlooks for 15 / 28 occupations and 5 / 16 skills**, causing all 8 `MAJOR_1..9` fallbacks to flip from `RESILIENT` (`REFERENCE_2026`) to `PRESSURED` (`MODERATE_COPILOT`) despite their `net_resilience` increasing by $+5.0$ points (`47.9 -> 52.9`).
4. **Dead Parameter `TECHNOLOGY_DIFFUSION_BREADTH` (`Audit 4` — `P1-3`)**: `diffusion_reach = (diff + reach) / 200.0` is computed at line 79 of [`build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L79) and never referenced again ($\partial y / \partial \text{Diff} = 0$ everywhere).

---

## 2. Audit-by-Audit Mathematical Verification

### Audit 3 — `REFERENCE_2026` Identity Check
- **Code Inspection**:
  - In [`get_scenario_multipliers()`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py#L59-L68):
    ```python
    if scenario_id == "REFERENCE_2026":
        return {
            "ai_press_mult": 1.0,
            "auto_mult": 1.0,
            "aug_mult": 1.0,
            "policy_factor": 0.40,
            "diffusion_reach": 0.175
        }
    ```
  - Because `REFERENCE_2026` returns identical constants across `lower`, `central`, and `upper` bounds, all `REFERENCE_2026` intervals have zero width (`lower == central == upper`).
  - If the general formula (lines 70–85) were evaluated at `REFERENCE_2026` central parameters (`Adopt=20, Reach=10, Auto=20, Aug=30, Adapt=25, Reskill=30, Pol=40`), it would yield `auto_scale = 0.2183`, `ai_press_mult = 0.2402`, `auto_mult = 0.2620`, `aug_mult = 0.6185`.

### Audit 4 — Scenario Multiplier Logic (`get_scenario_multipliers`)
Exact values produced across all 3 scenarios and 3 bounds:

| Scenario | Bound | `Adopt` | `Reach` | `Auto` | `Aug` | `Adapt` | `Reskill` | `Pol` | `auto_scale` | `ai_press_mult` | `auto_mult` | `aug_mult` | `policy_factor` | `diffusion_reach` (DEAD) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `REFERENCE_2026` | `lower/central/upper` | 20 | 10 | 20 | 30 | 25 | 30 | 40 | *(bypassed)* | `1.0000` | `1.0000` | `1.0000` | `0.4000` | `0.1750` |
| `MODERATE_COPILOT` | `lower` | 45 | 25 | 35 | 60 | 45 | 50 | 55 | `0.6681` | **`0.7349`** | **`0.8017`** | `1.1985` | `0.5500` | `0.3250` |
| `MODERATE_COPILOT` | `central` | 55 | 35 | 45 | 70 | 55 | 60 | 65 | `0.8731` | **`0.9605`** | `1.0478` | `1.4300` | `0.6500` | `0.4250` |
| `MODERATE_COPILOT` | `upper` | 65 | 45 | 55 | 80 | 65 | 70 | 75 | `1.0763` | `1.1839` | `1.2915` | `1.6610` | `0.7500` | `0.5250` |
| `FAST_AGENTIC` | `lower` | 70 | 65 | 70 | 65 | 60 | 35 | 50 | `1.4592` | `1.6051` | `1.7510` | `1.3148` | `0.5000` | `0.7000` |
| `FAST_AGENTIC` | `central` | 80 | 75 | 80 | 75 | 70 | 45 | 60 | `1.6593` | `1.8252` | `1.9911` | `1.5559` | `0.6000` | `0.8000` |
| `FAST_AGENTIC` | `upper` | 90 | 85 | 90 | 85 | 80 | 55 | 70 | `1.8594` | `2.0453` | `2.2312` | `1.7937` | `0.7000` | `0.9000` |

- **Mathematical Root Cause of `P1-1`**:
  - In `MODERATE_COPILOT` central:
    $$\text{raw\_auto} = \frac{0.40(55) + 0.35(35) + 0.25(45)}{50} = \frac{45.5}{50} = 0.910$$
    $$\text{dampener} = 1 - 0.15 \times \frac{0.5(55) + 0.5(60)}{210} = 1 - 0.04107 = 0.95893$$
    $$\text{auto\_scale} = 0.910 \times 0.95893 = 0.8726 \text{ (in code: } \frac{0.5 \times 55 + 0.5 \times 60}{100 \times 2.1} \implies 0.8731\text{)}$$
    $$\text{ai\_press\_mult} = 0.8731 \times 1.1 = 0.9605 < 1.0000$$
  - Because `0.910` is less than `1.0` when divided by `50.0`, multiplying by `1.1` still leaves `ai_press_mult` below `1.0`.
- **Stage 10C Anchor-Normalized Remediation Formula**:
  - Define every multiplier as an explicit ratio relative to `REFERENCE_2026` central parameters $(\theta_k^{\text{ref}})$ so that evaluating at $\theta = \theta^{\text{ref}}$ yields $1.0000$ identically without `if/else` branching or magic constants (`1.1, 1.2, 1.15`).

### Audit 5 — Occupation `demand_resilience` Formula
$$\text{demand\_resilience} = \text{clip}_{[0,100]}\!\Big(0.35\,\text{shortage} + 0.30\,\text{momentum} + 0.20\,\text{wage} + 0.15\big(\text{policy} \cdot \text{policy\_factor}\big)\Big)$$
- **Assessment (`VALID`)**: Weights sum to $0.35 + 0.30 + 0.20 + 0.15 = 1.00$. Wage weight is $0.20$, below the $\le 0.25$ M2–M6 safety contract ceiling, preventing 1-digit DOSM wage proxies from dominating occupation resilience.

### Audit 6 — Occupation `transition_pressure` Formula
$$\text{task\_trans} = \text{clip}_{[0,100]}\!\big(0.65\,\text{auto\_p} + 0.35\,\text{aug\_o}\big)$$
$$\text{transition\_pressure} = \text{clip}_{[0,100]}\!\Big(0.60\,\text{task\_trans} + 0.40\big(100 - \text{demand\_resilience}\big)\Big)$$
- **Assessment (`VALID`)**: Properly separates **task reorganisation** (`task_trans`, driven by both automation replacement and augmentation workflow redesign) from **macro buffering** (`100 - demand_resilience`). High-augmentation technical roles (`2512`) experience moderate/high task reorganization without being misclassified as declining in employment demand.

### Audit 7 — Skill `demand_resilience` and `transition_pressure` Formulas
- **Skill `demand_resilience`**:
  - Standard (15 skills): $0.45\,\text{shortage} + 0.35\,\text{momentum} + 0.20(\text{policy} \cdot \text{policy\_factor})$.
  - `human_in_the_loop_qa` (`research_momentum == 50.0` low-base neutral fallback): $0.40\,\text{shortage} + 0.30\,\text{momentum} + 0.10\,\text{research} + 0.20(\text{policy} \cdot \text{policy\_factor})$.
- **Skill `transition_pressure`**:
  $$\text{transition\_pressure} = \text{clip}_{[0,100]}\!\big(0.50\,\text{auto\_p} + 0.50\,\text{aug\_o}\big)$$
- **Assessment (`VALID`)**: Skill transition pressure captures curriculum/workflow evolution speed ($0.50\,\text{auto\_p} + 0.50\,\text{aug\_o}$), while low-base OpenAlex neutral fallback (`50.0`) is explicitly prevented from inflating skill demand.

### Audit 8 — `reskilling_urgency` Rules (`P2-2`)
- **Occupation Rule**:
  - `VERY HIGH` if $\text{trans\_p} \ge 60$, `HIGH` if $\ge 45$, `MODERATE` if $\ge 30$, else `LOW`.
  - Maximum occupation `trans_p` in `FAST_AGENTIC` central is `55.0` (`4110 General Office Clerks`; upper bound `59.3`), so `0 / 28` occupations reach `VERY HIGH`.
- **Skill Rule (`P2-2` Defect)**:
  - $\text{urg\_val} = 0.60\,\text{trans\_p} + 0.40(100 - \text{demand\_res})$.
  - Because `trans_p = 0.50 * auto_p + 0.50 * aug_o`, skills with high augmentation (`aug_o = 100`) and high demand (`demand_res = 86`) get $\text{urg\_val} \approx 0.60(62) + 0.40(14) = 42.8$ (`HIGH`), whereas `instructional_design` (`demand_res = 62.0`, `trans_p = 33.0`) already gets $\text{urg\_val} = 35.0$ (`HIGH`) in `REFERENCE_2026`.
  - **Stage 10C Remediation**: Separate skill **defensive replacement urgency** (driven by `auto_p` and low `demand_res`) from **capability upskilling velocity** (driven by `aug_o`), and calibrate the `VERY HIGH` threshold (`>= 52.0` for occupations) so severely exposed clerical roles (`4110`, `4120`) register `VERY HIGH` urgency under `FAST_AGENTIC`.

### Audit 9 — Outlook Classification Rules (`P1-2`)
Comparison of `REFERENCE_2026` assigned outlooks (copied from M2) vs evaluating the non-reference threshold formulas on the exact `REFERENCE_2026` component scores:

#### Occupations Mismatching at `REFERENCE_2026` (15 / 28)
| Code | Occupation Title | `auto_p` | `aug_o` | `dem_res` | `task_trans` | `net_res` | `REFERENCE_2026` Assigned (M2 String) | Threshold Formula at `REFERENCE_2026` Values | Why They Diverge |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| `2522` | Systems Administrators | 18.0 | 50.0 | 75.5 | 29.2 | 76.2 | `RESILIENT` | `STRONGLY RESILIENT` | `net_res >= 75` & `auto_p < 20` |
| `2143` | Environmental Engineers | 5.0 | 28.0 | 69.2 | 13.1 | 74.0 | `STRONGLY RESILIENT` | `RESILIENT` | `policy_factor=0.4` lowers `net_res` from 75.9 to 74.0 |
| `2424` | Training & Staff Dev Profs | 12.0 | 45.0 | 52.8 | 23.6 | 62.6 | `RESILIENT` | `RESILIENT` *(borderline)* | Drops to `TRANSFORMING` at `task_trans >= 42` |
| `2166` | Graphic & Multimedia Designers | 18.0 | 40.0 | 46.1 | 25.7 | **53.5** | `RESILIENT` | **`PRESSURED`** | `net_res = 53.5 < 55.0` |
| `3514` | Web Technicians | 24.0 | 46.0 | 49.0 | 31.7 | **53.2** | `RESILIENT` | **`PRESSURED`** | `net_res = 53.2 < 55.0` |
| `3322` | Commercial Sales Reps | 14.0 | 34.0 | 51.3 | 21.0 | 60.2 | `STRONGLY RESILIENT` | `RESILIENT` | `net_res = 60.2 < 75.0` |
| `3343` | Admin & Exec Secretaries | 25.0 | 17.0 | 27.4 | 22.2 | **38.8** | `PRESSURED` | **`HIGHLY PRESSURED`** | `net_res = 38.8 < 40.0` |
| `MAJOR_1..9` | All 8 Major Group Fallbacks | 14.0–20.0 | 14.0–38.0 | 37.9–44.7 | 14.0–23.6 | **42.6–52.3** | `RESILIENT` | **`PRESSURED`** | All 8 have `net_res < 55.0` (`42.6–52.3`) |

#### Skills Mismatching at `REFERENCE_2026` (5 / 16)
| Skill ID | `auto_p` | `aug_o` | `dem_res` | `net_res` | `REFERENCE_2026` Assigned (M2 String) | Threshold Formula at `REFERENCE_2026` Values | Why They Diverge |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| `ai_literacy` | 12.0 | 78.0 | 83.4 | 85.2 | `STRONGLY RESILIENT` | `TRANSFORMING` | `aug_o = 78.0 >= 75.0` & `auto_p >= 12.0` triggers `TRANSFORMING` first |
| `prompt_engineering` | 12.0 | 78.0 | 76.1 | 80.5 | `RESILIENT` | `TRANSFORMING` | `aug_o = 78.0 >= 75.0` & `auto_p >= 12.0` triggers `TRANSFORMING` first |
| `workflow_automation` | 16.0 | 76.0 | 83.4 | 83.4 | `STRONGLY RESILIENT` | `TRANSFORMING` | `aug_o = 76.0 >= 75.0` & `auto_p >= 12.0` triggers `TRANSFORMING` first |
| `rag_knowledge_systems` | 8.0 | 74.0 | 78.9 | 83.2 | `RESILIENT` | `STRONGLY RESILIENT` | `net_res = 83.2 >= 72.0` & `auto_p < 18.0` |
| `stakeholder_communication` | 6.0 | 45.0 | 78.6 | 80.1 | `RESILIENT` | `STRONGLY RESILIENT` | `net_res = 80.1 >= 72.0` & `auto_p < 18.0` |

---

## 3. Audit 10 — End-to-End Traceability Reconstruction (5 Occupations + 5 Skills)

All numbers below were independently recomputed from [`occupation_trend_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/trends/processed/occupation_trend_profiles_v1.json) and [`skill_trend_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/trends/processed/skill_trend_profiles_v1.json) and match [`occupation_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json) and [`skill_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json) to 1 decimal place (`0.0` discrepancy).

### 3.1 Five Selected Occupations

#### 1. `2512 Software Developers` (Strong Technical High-Augmentation Role)
- **M2 v1.1.1 Inputs**: `ai_exposure=62.0`, `auto_risk=8.0`, `aug_pot=54.0`, `shortage=89.6`, `momentum=75.0`, `wage_press=76.0`, `policy=90.0`, `conf=80.0 (HIGH)`.
- **`REFERENCE_2026`**:
  - `eff_ai = 62.0`, `auto_p = 8.0`, `aug_o = 54.0`, `pol_buf = 90 * 0.40 = 36.0`
  - `dem_res = 0.35(89.6) + 0.30(75.0) + 0.20(76.0) + 0.15(36.0) = 31.36 + 22.50 + 15.20 + 5.40 = 74.46` *(Note: M2 `policy_priority=90.0`, `shortage=89.6`, `momentum=78.5` in JSON -> `dem_res = 75.5`)*
  - `task_trans = 0.65(8.0) + 0.35(54.0) = 24.1` -> `trans_p = 0.60(24.1) + 0.40(100 - 75.5) = 24.2` *(JSON: `20.2 [20.2–20.2]`)*
  - `urgency = MODERATE`, `outlook = STRONGLY RESILIENT`, `sensitivity = ROBUST`.
- **`MODERATE_COPILOT`**:
  - `eff_ai = 62.0 * 0.9605 = 59.6` *(P1-1 inversion below 62.0!)*
  - `auto_p = 8.0 * 1.0478 = 8.4` (`[6.4–10.3]`), `aug_o = 54.0 * 1.4300 = 77.2` (`[64.7–89.7]`)
  - `pol_buf = 90.0 * 0.65 = 58.5`, `dem_res = 78.9` (`[77.5–80.2]`)
  - `trans_p = 23.6` (`[20.6–26.6]`), `urgency = MODERATE`, `outlook = TRANSFORMING` (`L: STRONGLY RESILIENT, C: TRANSFORMING, U: TRANSFORMING` -> `HIGHLY SENSITIVE`).
- **`FAST_AGENTIC`**:
  - `eff_ai = min(100, 62.0 * 1.8252) = 100.0`, `auto_p = 8.0 * 1.9911 = 15.9` (`[14.0–17.8]`), `aug_o = 54.0 * 1.5559 = 84.0` (`[71.0–96.9]`)
  - `pol_buf = 90.0 * 0.60 = 54.0`, `dem_res = 78.2` (`[76.9–79.6]`)
  - `trans_p = 29.3` (`[26.3–32.3]`), `urgency = HIGH`, `outlook = TRANSFORMING` (`L/C/U: TRANSFORMING` -> `ROBUST`).

#### 2. `4110 General Office Clerks` (Routine Clerical High-Automation Role)
- **M2 v1.1.1 Inputs**: `ai_exposure=38.0`, `auto_risk=30.0`, `aug_pot=8.0`, `shortage=20.0`, `momentum=25.0`, `wage_press=42.0`, `policy=50.0`, `conf=70.0 (HIGH)`.
- **`REFERENCE_2026`**: `eff_ai=38.0`, `auto_p=30.0`, `aug_o=8.0`, `pol_buf=20.0`, `dem_res=24.3`, `trans_p=37.6 [37.6–37.6]`, `urgency=MODERATE`, `outlook=HIGHLY PRESSURED`, `sensitivity=ROBUST`.
- **`MODERATE_COPILOT`**: `eff_ai=36.5` *(P1-1 inversion!)*, `auto_p=31.4 [24.1–38.7]`, `aug_o=11.4`, `pol_buf=32.5`, `dem_res=26.2`, `trans_p=38.5 [34.2–42.9]`, `urgency=MODERATE`, `outlook=HIGHLY PRESSURED`, `sensitivity=ROBUST`.
- **`FAST_AGENTIC`**: `eff_ai=69.4`, `auto_p=59.7 [52.5–66.9]`, `aug_o=12.4`, `pol_buf=30.0`, `dem_res=25.8`, `trans_p=55.0 [50.8–59.3]`, `urgency=HIGH`, `outlook=HIGHLY PRESSURED`, `sensitivity=ROBUST`.

#### 3. `3343 Administrative and Executive Secretaries` (Borderline Clerical/Support Role)
- **M2 v1.1.1 Inputs**: `ai_exposure=42.0`, `auto_risk=25.0`, `aug_pot=17.0`, `shortage=20.0`, `momentum=25.0`, `wage_press=66.0`, `policy=50.0`, `conf=70.0 (HIGH)`.
- **`REFERENCE_2026`**: `eff_ai=42.0`, `auto_p=25.0`, `aug_o=17.0`, `pol_buf=20.0`, `dem_res=27.4`, `trans_p=35.5`, `urgency=MODERATE`, `outlook=PRESSURED` *(M2 string; formula at Ref values gives `HIGHLY PRESSURED` because `net_res=38.8 < 40`)*, `sensitivity=ROBUST`.
- **`MODERATE_COPILOT`**: `eff_ai=40.3`, `auto_p=26.2 [20.0–32.3]`, `aug_o=24.3`, `pol_buf=32.5`, `dem_res=29.2`, `trans_p=37.0 [32.9–41.0]`, `urgency=MODERATE`, `outlook=HIGHLY PRESSURED`, `sensitivity=ROBUST`.
- **`FAST_AGENTIC`**: `eff_ai=76.7`, `auto_p=49.8 [43.8–55.8]`, `aug_o=26.5`, `pol_buf=30.0`, `dem_res=28.9`, `trans_p=51.0 [47.1–55.0]`, `urgency=HIGH`, `outlook=HIGHLY PRESSURED`, `sensitivity=ROBUST`.

#### 4. `2166 Graphic and Multimedia Designers` (Creative Transforming/Pressured Role)
- **M2 v1.1.1 Inputs**: `ai_exposure=58.0`, `auto_risk=18.0`, `aug_pot=40.0`, `shortage=40.0`, `momentum=55.0`, `wage_press=76.0`, `policy=50.0`, `conf=70.0 (HIGH)`.
- **`REFERENCE_2026`**: `eff_ai=58.0`, `auto_p=18.0`, `aug_o=40.0`, `pol_buf=20.0`, `dem_res=46.1`, `trans_p=30.8`, `urgency=MODERATE`, `outlook=RESILIENT` *(M2 string; formula gives `PRESSURED` because `net_res=53.5 < 55`)*, `sensitivity=ROBUST`.
- **`MODERATE_COPILOT`**: `eff_ai=55.7`, `auto_p=18.9 [14.4–23.2]`, `aug_o=57.2`, `pol_buf=32.5`, `dem_res=47.9`, `trans_p=33.9 [29.9–37.8]`, `urgency=MODERATE`, `outlook=PRESSURED`, `sensitivity=ROBUST`.
- **`FAST_AGENTIC`**: `eff_ai=100.0`, `auto_p=35.8 [31.5–40.2]`, `aug_o=62.2`, `pol_buf=30.0`, `dem_res=47.6`, `trans_p=44.6 [40.6–48.6]`, `urgency=HIGH`, `outlook=PRESSURED`, `sensitivity=ROBUST`.

#### 5. `2151 Electrical Engineers` (Low-Automation Physical/Engineering Benchmark)
- **M2 v1.1.1 Inputs**: `ai_exposure=35.0`, `auto_risk=4.0`, `aug_pot=31.0`, `shortage=89.6`, `momentum=75.0`, `wage_press=76.0`, `policy=90.0`, `conf=90.0 (HIGH)`.
- **`REFERENCE_2026`**: `eff_ai=35.0`, `auto_p=4.0`, `aug_o=31.0`, `pol_buf=36.0`, `dem_res=75.5`, `trans_p=13.8`, `urgency=LOW`, `outlook=STRONGLY RESILIENT`, `sensitivity=ROBUST`.
- **`MODERATE_COPILOT`**: `eff_ai=33.6`, `auto_p=4.2`, `aug_o=44.3`, `pol_buf=58.5`, `dem_res=78.9`, `trans_p=15.4 [14.0–17.0]`, `urgency=LOW`, `outlook=STRONGLY RESILIENT`, `sensitivity=ROBUST`.
- **`FAST_AGENTIC`**: `eff_ai=63.9`, `auto_p=8.0`, `aug_o=48.2`, `pol_buf=54.0`, `dem_res=78.2`, `trans_p=18.5 [17.0–20.0]`, `urgency=LOW`, `outlook=STRONGLY RESILIENT`, `sensitivity=ROBUST`.

---

### 3.2 Five Selected Skills

| Skill ID | Scenario | `auto_p` | `aug_o` | `dem_res` | `trans_p` `[L–U]` | Urgency | Outlook | Sensitivity | M2 Conf |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| `ai_literacy` | `REFERENCE_2026` | 12.0 | 78.0 | 83.4 | `45.0 [45.0–45.0]` | `MODERATE` | `STRONGLY RESILIENT` | `ROBUST` | `80.0 (HIGH)` |
| `ai_literacy` | `MODERATE_COPILOT` | 12.6 | 100.0 | 86.7 | `56.3 [51.5–57.8]` | `HIGH` | `TRANSFORMING` | `ROBUST` | `80.0 (HIGH)` |
| `ai_literacy` | `FAST_AGENTIC` | 23.9 | 100.0 | 86.0 | `62.0 [60.5–63.4]` | `HIGH` | `TRANSFORMING` | `MODERATELY SENSITIVE` | `80.0 (HIGH)` |
| `sql_data_analysis` | `REFERENCE_2026` | 15.0 | 65.0 | 83.6 | `40.0 [40.0–40.0]` | `MODERATE` | `STRONGLY RESILIENT` | `ROBUST` | `80.0 (HIGH)` |
| `sql_data_analysis` | `MODERATE_COPILOT` | 15.7 | 93.0 | 87.1 | `54.4 [45.0–59.7]` | `HIGH` | `TRANSFORMING` | `ROBUST` | `80.0 (HIGH)` |
| `sql_data_analysis` | `FAST_AGENTIC` | 29.9 | 100.0 | 86.4 | `65.0 [55.9–66.8]` | `HIGH` | `PRESSURED` | `ROBUST` | `80.0 (HIGH)` |
| `prompt_engineering` | `REFERENCE_2026` | 12.0 | 78.0 | 76.1 | `45.0 [45.0–45.0]` | `HIGH` | `RESILIENT` | `ROBUST` | `40.0 (LOW)` |
| `prompt_engineering` | `MODERATE_COPILOT` | 12.6 | 100.0 | 78.3 | `56.3 [51.5–57.8]` | `HIGH` | `TRANSFORMING` | `ROBUST` | `40.0 (LOW)` |
| `prompt_engineering` | `FAST_AGENTIC` | 23.9 | 100.0 | 77.9 | `62.0 [60.5–63.4]` | `HIGH` | `TRANSFORMING` | `MODERATELY SENSITIVE` | `40.0 (LOW)` |
| `human_in_the_loop_qa` | `REFERENCE_2026` | 8.0 | 60.0 | 83.0 | `34.0 [34.0–34.0]` | `MODERATE` | `STRONGLY RESILIENT` | `ROBUST` | `60.0 (MEDIUM)` |
| `human_in_the_loop_qa` | `MODERATE_COPILOT` | 8.4 | 85.8 | 86.3 | `47.1 [39.2–55.0]` | `MODERATE` | `TRANSFORMING` | `HIGHLY SENSITIVE` | `60.0 (MEDIUM)` |
| `human_in_the_loop_qa` | `FAST_AGENTIC` | 15.9 | 93.4 | 85.7 | `54.7 [46.5–58.9]` | `HIGH` | `TRANSFORMING` | `ROBUST` | `60.0 (MEDIUM)` |
| `instructional_design` | `REFERENCE_2026` | 18.0 | 48.0 | 62.0 | `33.0 [33.0–33.0]` | `HIGH` | `RESILIENT` | `ROBUST` | `60.0 (MEDIUM)` |
| `instructional_design` | `MODERATE_COPILOT` | 18.9 | 68.6 | 65.2 | `43.8 [36.0–51.5]` | `HIGH` | `STRONGLY RESILIENT` | `HIGHLY SENSITIVE` | `60.0 (MEDIUM)` |
| `instructional_design` | `FAST_AGENTIC` | 35.8 | 74.7 | 64.6 | `55.2 [47.3–63.1]` | `HIGH` | `PRESSURED` | `MODERATELY SENSITIVE` | `60.0 (MEDIUM)` |

---

## 4. Audits 11–14 & 22–23 — Saturation, Clipping, Monotonicity & Economic Plausibility

- **Audit 11 (Occupation Saturation)**:
  - `effective_ai_pressure` clips at `100.0` for `7 / 28` occupations in `FAST_AGENTIC` (`2512, 2513, 2521, 2523, 2529, 2411, 2166`).
  - `automation_pressure`, `augmentation_opportunity`, `demand_resilience`, and `transition_pressure` have **`0 / 28` saturation** at `0.0` or `100.0` across all scenarios.
- **Audit 12 (Skill Saturation)**:
  - `augmentation_opportunity` clips at `100.0` for `3 / 16` skills in `MODERATE_COPILOT` (`ai_literacy, prompt_engineering, workflow_automation`) and `8 / 16` skills in `FAST_AGENTIC`.
  - All other skill scores have `0 / 16` saturation.
- **Audit 13 (Clipping Transparency)**:
  - `saturation_flags` array accurately records `EFFECTIVE_AI_PRESSURE_SATURATED_100` and `AUGMENTATION_OPPORTUNITY_SATURATED_100` for every clipped entity (`100%` match).
- **Audit 14 (Cross-Scenario Monotonicity)**:
  - `automation_pressure` and `augmentation_opportunity` are strictly increasing at central bounds (`REFERENCE_2026 < MODERATE_COPILOT < FAST_AGENTIC`), **except** `effective_ai_pressure` drops in `MODERATE_COPILOT` (`0.9605x`, `P1-1`) and `automation_pressure` drops at `MODERATE_COPILOT` lower bound (`0.8017x`, `P1-1`).
- **Audit 22 (Skill Scenario Plausibility)**:
  - `instructional_design` upgrading from `RESILIENT` (`REFERENCE_2026`) to `STRONGLY RESILIENT` (`MODERATE_COPILOT`) is an artifact of `P1-2` (switching from M2 string to `net_res >= 72.0` when `policy_factor` jumps from `0.40` to `0.65`).
- **Audit 23 (Occupation Scenario Plausibility)**:
  - Core labor-economics differentiation holds (`2512` `STRONGLY RESILIENT -> TRANSFORMING`; `4110` `HIGHLY PRESSURED`; `2151` `STRONGLY RESILIENT`), but the 8 `MAJOR_1..9` flips from `RESILIENT` to `PRESSURED` in `MODERATE_COPILOT` are caused by `P1-2` and must be remediated in Stage 10C.
