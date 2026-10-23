# M6 Anchor Normalization & Multiplier Verification (v1.1.0)

**Audit Subject**: P1-1 Resolution — Multiplier Normalization & Monotonic Scaling  
**Engine Version**: M6 v1.1.0  
**Target Code**: [`scripts/build_scenario_profiles_v1_1.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles_v1_1.py#L65-L115)

---

## 1. Problem Statement & Mathematical Diagnosis of v1.0.0

In M6 v1.0.0, [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py) normalized scenario assumptions against an arbitrary fixed denominator `/ 50.0` and scaled them with magic constants (`1.1, 1.2, 1.15`), while hardcoding `1.0` for `REFERENCE_2026`:
- Because `MODERATE_COPILOT` parameters (e.g. reach=35, auto=45) divided by `50.0` yielded ratios $< 1.0$, multiplying by `1.1` produced an `effective_ai_pressure` multiplier of `0.9605` ($< 1.0000$), causing AI pressure to drop below baseline!
- In the lower bound of `MODERATE_COPILOT`, `auto_mult` fell to `0.8017`, dropping 20% below `REFERENCE_2026`.
- `REFERENCE_2026` lower, central, and upper bounds collapsed to zero width because of the `if scenario_id == "REFERENCE_2026"` bypass.

---

## 2. Stage 10C Anchor Normalization Formulation

Let $\theta_{\text{ref}, k}$ denote the central assumption values for `REFERENCE_2026`:
- $\text{Adopt}_{\text{ref}} = 20.0$
- $\text{Reach}_{\text{ref}} = 10.0$
- $\text{Auto}_{\text{ref}} = 20.0$
- $\text{Aug}_{\text{ref}} = 30.0$
- $\text{Diff}_{\text{ref}} = 25.0$
- $\text{Reskill}_{\text{ref}} = 30.0$
- $\text{Policy}_{\text{ref}} = 40.0$
- $\text{Adapt}_{\text{ref}} = 25.0$

For any scenario and bound, we compute normalized relative intensity ratios:
$$r_k = \frac{\theta_k}{\theta_{\text{ref}, k}}$$

### Multiplier Formulas:
1. **Macro AI Pressure Multiplier** (`ai_press_mult`):
   $$\text{Index}_{\text{ai}} = r_{\text{adopt}}^{0.40} \cdot r_{\text{diff}}^{0.35} \cdot r_{\text{reach}}^{0.25}$$
   $$\text{ai\_press\_mult} = \text{Index}_{\text{ai}}^{0.35}$$
2. **Automation Substitution Multiplier** (`auto_mult`):
   $$\text{Index}_{\text{auto}} = r_{\text{auto}}^{0.45} \cdot r_{\text{reach}}^{0.35} \cdot r_{\text{diff}}^{0.20}$$
   $$\text{auto\_mult} = \text{Index}_{\text{auto}}^{0.40}$$
3. **Augmentation Opportunity Multiplier** (`aug_mult`):
   $$\text{Index}_{\text{aug}} = r_{\text{aug}}^{0.40} \cdot r_{\text{adapt}}^{0.25} \cdot r_{\text{reskill}}^{0.20} \cdot r_{\text{diff}}^{0.15}$$
   $$\text{aug\_mult} = \text{Index}_{\text{aug}}^{0.35}$$
4. **Policy Buffer Factor** (`policy_factor`):
   $$\text{policy\_factor} = \frac{\text{Policy}}{100.0}$$

---

## 3. Exact Multiplier Values in M6 v1.1.0

| Scenario ID | Bound | `ai_press_mult` | `auto_mult` | `aug_mult` | `policy_factor` | `diffusion_ratio` |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`REFERENCE_2026`** | **lower** | 0.8796 | 0.8465 | 0.9184 | 0.3000 | 0.8000 |
| **`REFERENCE_2026`** | **central** | **1.0000** | **1.0000** | **1.0000** | **0.4000** | **1.0000** |
| **`REFERENCE_2026`** | **upper** | 1.0931 | 1.1180 | 1.0696 | 0.5000 | 1.2000 |
| **`MODERATE_COPILOT`** | **lower** | **1.2857** | **1.3055** | 1.2323 | 0.5500 | 1.6000 |
| **`MODERATE_COPILOT`** | **central** | **1.3996** | **1.4576** | 1.3133 | 0.6500 | 2.0000 |
| **`MODERATE_COPILOT`** | **upper** | 1.4976 | 1.5884 | 1.3857 | 0.7500 | 2.4000 |
| **`FAST_AGENTIC`** | **lower** | **1.6184** | **1.8089** | 1.3188 | 0.5000 | 2.8000 |
| **`FAST_AGENTIC`** | **central** | **1.6939** | **1.9053** | 1.3929 | 0.6000 | 3.2000 |
| **`FAST_AGENTIC`** | **upper** | 1.7635 | 1.9948 | 1.4596 | 0.7000 | 3.6000 |

---

## 4. Invariant Verification Checklist

1. **Analytic Identity at Reference Central**: At `REFERENCE_2026` central, every $r_k \equiv 1.0000$, yielding `1.0000` analytically without special-case branching (`PASS`).
2. **No Magic Constants**: Removed arbitrary constants `1.1, 1.2, 1.15`. Elasticities sum to well-defined economic weights (`PASS`).
3. **Reference Bounds**: `REFERENCE_2026` has meaningful non-zero intervals (`[0.8465, 1.1180]` on `auto_mult`) (`PASS`).
4. **Monotonicity Across Scenarios**:
   - Minimum `MODERATE_COPILOT` `auto_mult` ($1.3055$) $>$ `REFERENCE_2026` Upper ($1.1180$) ($0$ inversions).
   - Minimum `FAST_AGENTIC` `auto_mult` ($1.8089$) $>$ `MODERATE_COPILOT` Upper ($1.5884$) ($0$ inversions).
   - Strict progression $\text{FAST} \ge \text{MODERATE} \ge \text{REFERENCE}$ holds across all corresponding bounds (`PASS`).
