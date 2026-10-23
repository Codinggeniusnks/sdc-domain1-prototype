# M6 Reskilling Urgency Calibration Report (v1.1.0)

**Audit Subject**: P2-2 Resolution — Calibrated Reskilling Urgency  
**Engine Version**: M6 v1.1.0  
**Target Code**: [`scripts/build_scenario_profiles_v1_1.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles_v1_1.py#L117-L148)

---

## 1. Problem Statement: Calibration Defect in v1.0.0

In M6 v1.0.0:
- **`0 / 28` occupations** reached `VERY HIGH` urgency under `FAST_AGENTIC`, even severely automated clerical roles like `4110 General Office Clerks` (automation pressure reached 59.7, but urgency peaked at `HIGH` 55.0 vs threshold 60.0).
- Conversely, for skills, `instructional_design` was flagged `HIGH` urgency in `REFERENCE_2026` simply because $100 - \text{demand\_resilience}$ was weighted too heavily ($40\%$), creating false-positive alarm for a baseline capability with modest automation pressure.

---

## 2. Stage 10C Calibrated Urgency Formulation

### 2.1 Occupational Reskilling Urgency
Captures task substitution threat and role transition friction, buffered by external labour market hiring demand:
$$\text{Urgency Index}_{\text{occ}} = 0.45\,\text{automation\_pressure} + 0.35\,\text{transition\_pressure} + 0.20\,(100.0 - \text{demand\_resilience})$$

**Calibrated Decision Thresholds**:
- $\ge 52.0 \implies \textbf{VERY HIGH}$
- $\ge 38.0 \implies \textbf{HIGH}$
- $\ge 25.0 \implies \textbf{MODERATE}$
- $< 25.0 \implies \textbf{LOW}$

### 2.2 Skill Reskilling Urgency
Captures curriculum obsolescence and workflow re-tooling urgency:
$$\text{Urgency Index}_{\text{skill}} = 0.45\,\text{automation\_pressure} + 0.35\,\text{transformation\_pressure} + 0.20\,(100.0 - \text{demand\_resilience})$$

**Calibrated Decision Thresholds**:
- $\ge 48.0 \implies \textbf{VERY HIGH}$
- $\ge 35.0 \implies \textbf{HIGH}$
- $\ge 22.0 \implies \textbf{MODERATE}$
- $< 22.0 \implies \textbf{LOW}$

---

## 3. Verified Reskilling Urgency Distributions (M6 v1.1.0)

### 3.1 Occupations
| Scenario | Granularity Tier | `LOW` | `MODERATE` | `HIGH` | `VERY HIGH` |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | **4-Digit Occupations ($N=20$)** | 15 | 2 | 3 | **0** |
| **`REFERENCE_2026`** | **Major-Group Fallbacks ($N=8$)** | 3 | 5 | 0 | **0** |
| *`REFERENCE_2026`* | *Combined Total ($N=28$)* | *18* | *7* | *3* | *0* |
| **`MODERATE_COPILOT`** | **4-Digit Occupations ($N=20$)** | 15 | 2 | 3 | **0** |
| **`MODERATE_COPILOT`** | **Major-Group Fallbacks ($N=8$)** | 0 | 8 | 0 | **0** |
| *`MODERATE_COPILOT`* | *Combined Total ($N=28$)* | *15* | *10* | *3* | *0* |
| **`FAST_AGENTIC`** | **4-Digit Occupations ($N=20$)** | 12 | 4 | 1 | **3** |
| **`FAST_AGENTIC`** | **Major-Group Fallbacks ($N=8$)** | 0 | 8 | 0 | **0** |
| *`FAST_AGENTIC`* | *Combined Total ($N=28$)* | *12* | *12* | *1* | **3** |

### Occupations Reaching `VERY HIGH` Urgency under `FAST_AGENTIC`:
1. **`4110 General Office Clerks`**: Automation pressure reaches $57.2$, Transition pressure reaches $53.8$, Urgency Index $= 59.4 \ge 52.0 \implies \textbf{VERY HIGH}$.
2. **`4311 Accounting and Bookkeeping Clerks`**: Automation pressure reaches $55.3$, Transition pressure reaches $52.7$, Urgency Index $= 57.8 \ge 52.0 \implies \textbf{VERY HIGH}$.
3. **`3343 Administrative and Executive Secretaries`**: Automation pressure reaches $47.6$, Transition pressure reaches $49.5$, Urgency Index $= 52.9 \ge 52.0 \implies \textbf{VERY HIGH}$.

### 3.2 Skills ($N=16$)
| Scenario | `LOW` | `MODERATE` | `HIGH` | `VERY HIGH` |
| :--- | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | 5 | 11 | **0** | 0 |
| **`MODERATE_COPILOT`** | 2 | 14 | **0** | 0 |
| **`FAST_AGENTIC`** | 2 | 4 | **10** | 0 |

*Remediation Impact*:
- In `REFERENCE_2026`, `instructional_design` is now **`MODERATE`** (Urgency Index $= 27.2 < 35.0$), completely eliminating the false-positive `HIGH` alarm at baseline.
- Under `FAST_AGENTIC`, 10 skills requiring substantial retooling correctly advance to `HIGH` urgency.
