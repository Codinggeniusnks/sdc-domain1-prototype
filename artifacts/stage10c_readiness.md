# Stage 10C Readiness & Targeted M6 Remediation Plan

**Current Stage**: Stage 10B Concluded  
**Stage 10B Verdict**: **`TARGETED M6 REMEDIATION REQUIRED`**  
**Next Permitted Stage**: **Stage 10C — Bounded M6 v1.1.0 Remediation** (Before M3 Role Matching)

---

## 1. Upstream Freeze Certification (Untouched in Stage 10C)

1. **M1 Skills Extraction (`H_blend_0.70A_0.30C1_W1.0`)**:
   - **Status**: `FROZEN — PROMOTE WITH LIMITATIONS`
   - **Holdout Provenance**: Protocol B and Protocol C v2 were unsealed exactly once during Stage 8E for the approved final frozen M1 evaluation. Zero additional Protocol B or Protocol C v2 access occurred during Stages 9A–10B, and zero access is permitted in Stage 10C.
2. **M2 Trend Intelligence (`M2 v1.1.1`)**:
   - **Status**: `FROZEN` ([`artifacts/m2_v1_1_1_freeze_manifest.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m2_v1_1_1_freeze_manifest.json), SHA-256: `cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542`)
   - **Constraint**: Do NOT modify any M2 data file, source manifest, or `src/trend_engine.py`.

---

## 2. Exact Scope of Stage 10C Remediation (`M6 v1.0.0 -> M6 v1.1.0`)

Stage 10C is strictly bounded to fixing the **4 P1 defects**, **3 P2 issues**, and **2 P3 documentation items** identified in Stage 10B:

### 2.1 P1 Mandatory Fixes (Must Close for M3 Safety)

| Defect ID | Target File(s) | Exact Remediation Specification | Verification Gate |
| :--- | :--- | :--- | :--- |
| **`P1-1`** | [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py) | Replace `if scenario_id == "REFERENCE_2026"` bypass and magic constants (`1.1, 1.2, 1.15`) in `get_scenario_multipliers()` with **anchor-normalized equations relative to `REFERENCE_2026` central parameters** $(\theta_k^{\text{ref}})$: <br>1. At `REFERENCE_2026` central parameters, `ai_press_mult = 1.0`, `auto_mult = 1.0`, `aug_mult = 1.0`, `policy_factor = 0.40` identically from the formula.<br>2. Evaluate `REFERENCE_2026` `lower` and `upper` bounds through the same formula so `REFERENCE_2026` has genuine non-zero `[lower, upper]` intervals.<br>3. Guarantee strict monotonicity across scenarios: `REFERENCE_2026 < MODERATE_COPILOT < FAST_AGENTIC` for `ai_press_mult`, `auto_mult`, and `aug_mult` at all corresponding bounds (`lower`, `central`, `upper`), and ensure `MODERATE_COPILOT` lower-bound `auto_mult >= 1.0`. | Zero `effective_ai_pressure` or `automation_pressure` inversions below `REFERENCE_2026` in `MODERATE_COPILOT` (`central` or `lower`). |
| **`P1-2`** | [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py) | Unify `determine_occupation_outlook()` and `determine_skill_outlook()` across all 3 scenarios so `REFERENCE_2026` is not on a separate regime from `MODERATE_COPILOT` and `FAST_AGENTIC`:<br>1. Anchor scenario outlook transitions to **baseline-relative deltas ($\Delta\text{auto\_p}, \Delta\text{aug\_o}, \Delta\text{task\_trans}, \Delta\text{net\_res}$) combined with the M2 baseline outlook**, OR calibrate unified thresholds that reproduce M2's baseline outlooks at `REFERENCE_2026` central values (`0 / 28` spurious baseline flips).<br>2. Ensure `MAJOR_1..9` do not spuriously flip from `RESILIENT` to `PRESSURED` in `MODERATE_COPILOT` when their `net_resilience` increases. | `0 / 28` occupation and `0 / 16` skill baseline regime discontinuities at `REFERENCE_2026` central parameters. |
| **`P1-3`** | [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py), [`tests/test_scenario_engine.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/tests/test_scenario_engine.py) | Wire `TECHNOLOGY_DIFFUSION_BREADTH` (`diff`) into the active `ai_press_mult`, `auto_mult`, and `aug_mult` equations (e.g., weighting adoption speed and diffusion breadth relative to `REFERENCE_2026` central values `Adopt=20, Diff=25`) and remove dead variable `diffusion_reach`. Add a unit test proving $\partial(\text{auto\_p}, \text{aug\_o}, \text{eff\_ai}) / \partial\text{Diff} > 0$. | All 8 parameters in `scenario_assumptions_v1.json` have non-zero partial derivatives in unit tests. |
| **`P1-4`** | [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py), `artifacts/m6_*.md` | 1. Separate `4_DIGIT_OCCUPATION` ($N=20$) and `1_DIGIT_MAJOR_GROUP_FALLBACK` ($N=8$) summary distributions in JSON metadata and all M6 reports.<br>2. For `MAJOR_1..9`, replace `['AGGREGATED_FALLBACK', 'MAJOR_GROUP_WAGE_CONTEXT', 'NO_ROLE_SPECIFIC_WAGE_DATA', 'AGGREGATE_MAJOR_GROUP']` with `['AGGREGATED_MAJOR_GROUP_FALLBACK', 'GROUP_LEVEL_DIRECT_WAGE_MEASUREMENT']` while keeping `['MAJOR_GROUP_WAGE_CONTEXT', 'NO_ROLE_SPECIFIC_WAGE_DATA']` on all 20 4-digit roles.<br>3. Add the Fallback Neutrality Clause to `m6_m3_consumption_contract.md`. | Clean separation of 20 4-digit vs 8 1-digit fallback metrics and flags. |

---

### 2.2 P2 Quality & Reporting Improvements

| Issue ID | Target File(s) | Exact Remediation Specification |
| :--- | :--- | :--- |
| **`P2-1`** | [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py), [`artifacts/m6_sensitivity_audit.md`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m6_sensitivity_audit.md) | 1. Distinguish **Opportunity/Transformation Sensitivity** (`STRONGLY RESILIENT <-> TRANSFORMING`, where `net_res >= 72.0` holds across all bounds) from **Downside Pressure Sensitivity** (crossing into `PRESSURED` or `HIGHLY PRESSURED`), or refine `OUTLOOK_ORDER` distance so healthy high-augmentation roles are not conflated with downside risk.<br>2. Regenerate all sensitivity and low-base tables directly from JSON so prose matches JSON `100%` (including all 4 `INSUFFICIENT_HISTORICAL_BASELINE` skills: `data_visualization`, `human_in_the_loop_qa`, `api_integration`, `carbon_footprint_analytics`). |
| **`P2-2`** | [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.py) | Refine `reskilling_urgency` thresholds so severely exposed clerical roles (`4110`, `4120`, `4132`) reach `VERY HIGH` under `FAST_AGENTIC`, and adjust skill urgency so high-demand skills (`instructional_design` in `REFERENCE_2026`) are not prematurely flagged `HIGH` at baseline. |
| **`P2-3`** | [`artifacts/m6_sensitivity_audit.md`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m6_sensitivity_audit.md) | Report Spearman $\rho$ on multi-channel composite scores (`transition_pressure`, `demand_resilience`, `net_resilience`) separately for the 20 4-digit roles and 8 Major Groups, and explicitly note that $\rho = 1.0000$ on unclipped `automation_pressure` is structural rank preservation from scalar multiplication. |

---

### 2.3 P3 Documentation Fixes

| Issue ID | Target File(s) | Exact Remediation Specification |
| :--- | :--- | :--- |
| **`P3-1`** | `artifacts/stage10a_m6_scenario_engine_report.md`, `artifacts/stage10b_readiness.md` | Replace "zero holdout access" header shorthand with the exact Stage 8E one-time unsealing statement, and fix the stale `m2_v1_1_1_freeze_manifest.json` SHA-256 string (`9558cf41...` $\to$ `cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542`). |
| **`P3-2`** | [`data/scenarios/scenario_assumptions_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/scenario_assumptions_v1.json), [`artifacts/m6_scenario_assumption_register.md`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m6_scenario_assumption_register.md) | Document the economic rationale (institutional training absorption lag and regulatory adjustment lag relative to rapid agentic deployment) for why `RESKILLING_RESPONSE_STRENGTH` (`60 -> 45`) and `POLICY_RESPONSE_STRENGTH` (`65 -> 60`) are lower in `FAST_AGENTIC` than `MODERATE_COPILOT`. |
