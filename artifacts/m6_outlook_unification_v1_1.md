# M6 Unified Scenario Outlook Classification Report (v1.1.0)

**Audit Subject**: P1-2 Resolution — Unified Outlook Classification  
**Engine Version**: M6 v1.1.0  
**Target Code**: [`scripts/build_scenario_profiles_v1_1.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles_v1_1.py#L170-L245)

---

## 1. Problem Statement: Regime Switching in v1.0.0

In M6 v1.0.0:
- `REFERENCE_2026` simply copied M2 `overall_outlook` strings (`STRONGLY RISING -> STRONGLY RESILIENT`, `STABLE -> RESILIENT`).
- `MODERATE_COPILOT` and `FAST_AGENTIC` used an independent threshold classifier (`net_res < 55.0 -> PRESSURED`).
- This created an artificial regime discontinuity: evaluating the threshold classifier on `REFERENCE_2026` values disagreed with **15 / 28 occupations** and **5 / 16 skills**.
- Most egregiously, all 8 `MAJOR_1..9` fallback profiles were mapped to `RESILIENT` in `REFERENCE_2026` (via `base_outlook == STABLE`), but flipped to `PRESSURED` in `MODERATE_COPILOT` even though their `net_resilience` **increased** by `+4.0` to `+5.0` points.

---

## 2. Stage 10C Unified Classification Framework

Instead of bifurcated string-lookup vs threshold logic, M6 v1.1.0 uses a **two-stage anchor-and-delta classification framework** evaluated identically across all scenarios:

### Step 1: Deterministic Reference Anchor Mapping
Every entity has an unambiguous reference category $C_0$ derived from its frozen M2 baseline state:
- `STRONGLY RISING` $\to$ `STRONGLY RESILIENT`
- `RISING` $\to$ `RESILIENT`
- `STABLE` $\to$ `TRANSFORMING` if baseline task transition $\ge 30.0$ else `RESILIENT`
- `DECLINING` $\to$ `PRESSURED`
- `STRONGLY DECLINING` $\to$ `HIGHLY PRESSURED`

### Step 2: Unified Scenario Delta Shift Rules
A scenario outlook is evaluated based on $C_0$ plus scenario pressure deltas ($\Delta\text{auto\_p}, \Delta\text{aug\_o}, \Delta\text{net\_res}, \Delta\text{trans\_p}$):
1. **Severe Automation Downgrade**: If $\text{auto\_p} \ge 45.0$ or $\text{net\_res} < 35.0$, the outlook degrades to `HIGHLY PRESSURED`.
2. **Moderate Pressure Downgrade**: If $\text{auto\_p} \ge 30.0$, $\text{net\_res} < 55.0$, and $\Delta\text{net\_res} < -3.0$, the role becomes `PRESSURED`.
3. **Monotonicity Invariant (P1-2 Core)**: If an entity had $C_0 = \text{RESILIENT}$, and under the scenario $\Delta\text{net\_res} \ge 0$ (net resilience increased or stayed constant) and $\text{auto\_p} < 30.0$, the entity is **guaranteed to remain `RESILIENT`**.
4. **Upside Transformation Shift**: If a role has strong demand resilience ($\ge 60.0$) and undergoes massive augmentation workflow reorganization ($\text{task\_trans} \ge 40.0$, $\text{aug\_o} \ge 45.0$), it shifts to `TRANSFORMING` (e.g. `2512 Software Developers`).
5. **Reference Identity Preservation**: In `REFERENCE_2026` central, all scenario deltas are identically `0.0`, ensuring the unified classifier reproduces $C_0$ with **`0` spurious baseline flips**.

---

## 3. Verified Scenario Outlook Distributions (M6 v1.1.0)

### 3.1 4-Digit Specific Occupations ($N=20$)
| Scenario | `STRONGLY RESILIENT` | `RESILIENT` | `TRANSFORMING` | `PRESSURED` | `HIGHLY PRESSURED` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | 11 | 6 | 0 | 0 | 3 |
| **`MODERATE_COPILOT`** | 9 | 4 | 2 | 2 | 3 |
| **`FAST_AGENTIC`** | 7 | 4 | 4 | 2 | 3 |

*Notes on 4-Digit Shifts*:
- In `MODERATE_COPILOT`, 2 high-augmentation roles (`2512 Software Developers`, `2519 Software & Applications Developers NEC`) shift to `TRANSFORMING` (`UPSIDE_TRANSFORMATION`).
- In `FAST_AGENTIC`, 2 additional technical roles (`2511 Systems Analysts`, `2529 Database & Network Professionals`) shift to `TRANSFORMING`.
- 3 routine clerical roles (`4110 General Office Clerks`, `4311 Accounting Clerks`, `3343 Administrative Secretaries`) remain consistently in `HIGHLY PRESSURED`.

### 3.2 1-Digit Major Group Fallbacks ($N=8$)
| Scenario | `STRONGLY RESILIENT` | `RESILIENT` | `TRANSFORMING` | `PRESSURED` | `HIGHLY PRESSURED` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | 0 | **8** | 0 | 0 | 0 |
| **`MODERATE_COPILOT`** | 0 | **8** | 0 | 0 | 0 |
| **`FAST_AGENTIC`** | 0 | 0 | 0 | **8** | 0 |

*Remediation Impact*:
- In `MODERATE_COPILOT`, all 8 Major Groups remain `RESILIENT` (zero spurious flips to `PRESSURED`, eliminating the defect where higher resilience caused worse category classification).
- In `FAST_AGENTIC`, when broad agentic substitution shock hits ($1.905\times$), the fallback aggregates transition to `PRESSURED`.
