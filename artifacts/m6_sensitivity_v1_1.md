# M6 Sensitivity Semantics & Rank Stability Report (v1.1.0)

**Audit Subject**: P2-1 & P2-3 Resolution — Multi-Dimensional Sensitivity & Multi-Channel Rank Stability  
**Engine Version**: M6 v1.1.0  
**Target Code**: [`scripts/build_scenario_profiles_v1_1.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles_v1_1.py#L250-L300)

---

## 1. Problem Statement: 1D Ordinal Flaw & Misleading $\rho = 1.0$ in v1.0.0

In M6 v1.0.0:
- Categorical sensitivity was calculated by ordinal distance in `[STRONGLY RESILIENT, RESILIENT, TRANSFORMING, PRESSURED, HIGHLY PRESSURED]`.
- As a result, when a strong technical role (`2512 Software Developers`) moved from `STRONGLY RESILIENT` (`1`) to `TRANSFORMING` (`3`), its spread of 2 caused it to be labeled `HIGHLY SENSITIVE`, falsely conflating high productivity augmentation with downside vulnerability!
- Furthermore, Stage 10A reported Spearman rank correlation $\rho = 1.0000$ on `automation_pressure` as evidence of robust ranking, which is mathematically trivial scalar multiplication ($x \cdot c$).

---

## 2. Stage 10C Multi-Dimensional Sensitivity Semantics

In M6 v1.1.0, every profile carries a detailed `sensitivity_profile` object with 4 independent dimensions:

1. **`exact_category_stability`**: `"STABLE"` if outlook is identical across `[lower, central, upper]` bounds; else `"SHIFTING"`.
2. **`downside_risk_stability`**: `"ROBUST"` if no bound enters `PRESSURED` or `HIGHLY PRESSURED`; `"VULNERABLE"` if downside risk is present.
3. **`transformation_sensitivity`**: `"HIGH"` if augmentation expands workflow into `TRANSFORMING`; else `"LOW"`.
4. **`movement_type`**:
   - **`NO_SHIFT`**: Outlook is invariant across bounds.
   - **`UPSIDE_TRANSFORMATION`**: Role shifts between `STRONGLY RESILIENT` / `RESILIENT` and `TRANSFORMING` while demand resilience remains strong ($\ge 60.0$) and automation risk remains low ($< 30.0$).
   - **`DOWNSIDE_PRESSURE`**: Bounds enter `PRESSURED` or `HIGHLY PRESSURED`.
   - **`NEUTRAL_BOUNDARY_SHIFT`**: Minor boundary movement between adjacent non-pressured states.

---

## 3. Verified Sensitivity Distribution Across Scenarios (M6 v1.1.0)

All statistics below were generated directly from canonical JSON data:

| Scenario ID ($N=28$) | Exact Category Stable | Downside Risk Robust | High Transformation Sensitivity | Movement Types Observed |
| :--- | :---: | :---: | :---: | :--- |
| **`REFERENCE_2026`** | 20 / 28 | 17 / 28 | 0 / 28 | `NO_SHIFT`: 20, `DOWNSIDE_PRESSURE`: 8 |
| **`MODERATE_COPILOT`** | 23 / 28 | **23 / 28** | 4 / 28 | `NO_SHIFT`: 23, `UPSIDE_TRANSFORMATION`: 3, `DOWNSIDE_PRESSURE`: 1, `NEUTRAL_BOUNDARY_SHIFT`: 1 |
| **`FAST_AGENTIC`** | 27 / 28 | 15 / 28 | 4 / 28 | `NO_SHIFT`: 27, `UPSIDE_TRANSFORMATION`: 1 |

*Note on Software Developers `2512`*:
- Under `MODERATE_COPILOT` and `FAST_AGENTIC`, `2512` is classified with `downside_risk_stability = "ROBUST"` and `movement_type = "UPSIDE_TRANSFORMATION"`. Downstream systems (M3) know that its transformation reflects generative AI tool adoption, not employment replacement risk.

---

## 4. Multi-Channel Spearman Rank Stability Analysis (P2-3)

Rather than citing trivial $\rho = 1.0$ on unclipped scalar metrics, M6 v1.1.0 evaluates genuine composite multi-channel indices:

### 4.1 4-Digit Specific Occupations ($N=20$)
| Multi-Channel Metric | `REFERENCE` vs `COPILOT` | `REFERENCE` vs `FAST_AGENTIC` | `COPILOT` vs `FAST_AGENTIC` | Methodological Evaluation |
| :--- | :---: | :---: | :---: | :--- |
| **`transition_pressure`** | **0.9992** | **0.9925** | **0.9947** | High structural stability across scenarios. |
| **`net_resilience`** | **0.9970** | **0.9910** | **0.9940** | Meaningful cross-scenario re-ordering without rank churn. |
| **`demand_resilience`** | **0.9970** | **0.9970** | **1.0000** | High persistence of macro labor shortage signals. |
| *`automation_pressure`* | *1.0000* | *1.0000* | *1.0000* | *Structural rank preservation from monotonic multiplier scaling.* |

### 4.2 Core Skills ($N=16$)
| Multi-Channel Metric | `REFERENCE` vs `COPILOT` | `REFERENCE` vs `FAST_AGENTIC` | `COPILOT` vs `FAST_AGENTIC` | Methodological Evaluation |
| :--- | :---: | :---: | :---: | :--- |
| **`transformation_pressure`** | **1.0000** | **0.8710** | **0.8710** | Significant differentiation as agentic workflows accelerate. |
| **`net_resilience`** | **0.9948** | **0.9698** | **0.9765** | Robust preservation of relative skill endurance. |
| **`demand_resilience`** | **0.9853** | **0.9853** | **1.0000** | Stable policy and shortage prioritization. |

---

## 5. Canonical Zero-Base Research Skills Verification (4 Skills)
Extracted directly from [`skill_scenario_profiles_v1_1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1_1.json):
- Total count: **4 / 16 skills** carry `INSUFFICIENT_HISTORICAL_BASELINE`:
  1. `data_visualization`
  2. `human_in_the_loop_qa`
  3. `api_integration`
  4. `carbon_footprint_analytics`
- All 4 skills maintain their baseline warning flags across all 3 scenarios.
