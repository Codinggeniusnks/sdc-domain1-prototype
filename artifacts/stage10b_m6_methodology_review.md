# Stage 10B Independent Methodology Review: M6 Future Workforce Scenario Engine (v1.0.0)

**Reviewer Role:** Independent Senior Workforce-Foresight Methodologist, Labour-Economics Reviewer, Quantitative Scenario-Modelling Auditor & Explainable-AI Architect  
**Date:** 2026-10-23  
**Reviewed Engine:** M6 Future Workforce Scenario Engine v1.0.0  
**Upstream Baselines:**  
- **M1 Skills Extraction**: `H_blend_0.70A_0.30C1_W1.0` (Frozen after Stage 8E; Protocol B and Protocol C v2 were unsealed exactly once during Stage 8E for the approved final frozen M1 evaluation; no additional Protocol B or Protocol C v2 access occurred during Stages 9A onward).  
- **M2 AI Trend Intelligence**: `M2 v1.1.1` (Formally frozen in `artifacts/m2_v1_1_1_freeze_manifest.json`, SHA-256: `cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542`; verified read-only).  
**Final Audit Verdict:** **`TARGETED M6 REMEDIATION REQUIRED`**

---

## 1. Executive Summary & Overall Assessment

We conducted a rigorous, code-and-data-first forensic audit of **M6 Future Workforce Scenario Engine v1.0.0** across all 33 audit dimensions, inspecting [`scripts/build_scenario_profiles.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/build_scenario_profiles.json), [`src/scenario_engine.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/src/scenario_engine.py), [`data/scenarios/scenario_definitions_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/scenario_definitions_v1.json), [`data/scenarios/occupation_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1.json), and [`data/scenarios/skill_scenario_profiles_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/skill_scenario_profiles_v1.json) rather than relying on Stage 10A summary prose.

### Key Strengths Confirmed
1. **Strict Upstream Integrity (Zero P0 Defects)**: M6 is completely decoupled from M1 and M2. Frozen M2 v1.1.1 hashes are verified prior to execution and never mutated.
2. **Explicit Assumption Governance**: All 24 parameter entries (8 parameters $\times$ 3 scenarios) carry `assumption_status = "SCENARIO_ASSUMPTION"`, qualitative bands (`LOW`, `MODERATE`, `HIGH`, `VERY HIGH`), and `[lower, central, upper]` ranges. Zero fake probabilities or 2030 forecast accuracy claims exist.
3. **Multi-Channel Architecture**: Automation pressure, augmentation opportunity, demand resilience, policy buffer, and transition pressure are modeled as distinct, inspectable channels. High AI exposure with dominant augmentation (`2512 Software Developers`) remains resilient/transforming while clerical roles (`4110 General Office Clerks`) face high pressure from structural evidence.
4. **Fairness & Reproducibility**: Zero demographic attributes are used or accepted (`ValueError` enforced). All build outputs match `data/scenarios/scenario_build_manifest_v1.json` bitwise.

### Why Targeted Remediation (Stage 10C) Is Required Before M3
Despite a sound architectural foundation, forensic code inspection uncovered **4 P1 defects**, **3 P2 issues**, and **2 P3 documentation discrepancies** that must be remediated in a bounded Stage 10C pass before M6 outputs can safely influence M3 Role Matching:
- **P1-1 (Non-Monotonic Multiplier Anchor & Magic Constants)**: Because `get_scenario_multipliers()` hardcodes `1.0` for `REFERENCE_2026` but divides by `50.0` (with undocumented `1.1`, `1.2`, `1.15` scalars) for non-reference scenarios, `MODERATE_COPILOT` central `effective_ai_pressure` (`ai_press_mult = 0.9605`) is **lower** than `REFERENCE_2026` for all 28 occupations (`2512` drops from `62.0` to `59.6`), and `MODERATE_COPILOT` lower-bound `automation_pressure` (`auto_mult = 0.8017`) drops 20% below `REFERENCE_2026` despite strictly higher scenario assumptions.
- **P1-2 (Bifurcated Outlook Classification Regime)**: `determine_occupation_outlook()` and `determine_skill_outlook()` use a string lookup from M2 `overall_outlook` when `scenario_id == "REFERENCE_2026"`, but switch to a numerical threshold formula (`net_res < 55.0`, etc.) for `MODERATE_COPILOT` and `FAST_AGENTIC`. Evaluating the threshold formula on `REFERENCE_2026` numbers produces a **different category for 15/28 occupations and 5/16 skills**. Notably, all 8 Major Groups (`MAJOR_1..9`) flip from `RESILIENT` (`REFERENCE_2026`) to `PRESSURED` (`MODERATE_COPILOT`) even though their `net_res` **increased** in `MODERATE_COPILOT`!
- **P1-3 (Dead Parameter `TECHNOLOGY_DIFFUSION_BREADTH`)**: `get_scenario_multipliers()` computes `diffusion_reach`, but neither `process_occupations()` nor `process_skills()` ever reads it. `TECHNOLOGY_DIFFUSION_BREADTH` has a $0.0$ derivative across the entire engine while being cited in `scenario_assumptions_used`.
- **P1-4 (Granularity Mixing & Misattributed Wage Flags on Major Groups)**: Aggregate occupation distributions mix 20 4-digit occupations with 8 1-digit Major Group fallbacks (8 of the 10 `PRESSURED` roles in `MODERATE_COPILOT` and `FAST_AGENTIC` are `MAJOR_1..9`). Moreover, `MAJOR_1..9` are tagged with `MAJOR_GROUP_WAGE_CONTEXT` and `NO_ROLE_SPECIFIC_WAGE_DATA` alongside duplicate flags `AGGREGATED_FALLBACK` and `AGGREGATE_MAJOR_GROUP`, even though 1-digit DOSM wages are direct group-level measurements for `MAJOR_1..9`.

---

## 2. Summary Audit Table (Audits 1–33)

| Audit # | Audit Dimension | Status | Defect Severity | Key Forensic Finding |
| :---: | :--- | :---: | :---: | :--- |
| **1** | Scenario Assumption Status | **VALID** | None | 24/24 parameters labeled `SCENARIO_ASSUMPTION`; never `OBSERVED_EVIDENCE` or `PROBABILITY`. |
| **2** | Assumption Justification | **VALID** | None | Ordinal bands (`20=LOW`, `55=MODERATE`, `85=VERY HIGH`), bounds, and rationales coherent. |
| **3** | Reference Scenario Identity | **NEEDS FIX** | **P1-1, P1-2** | Central numbers match M2 ($\Delta=0$), but achieved via `if/else` bypass that masks formula mismatch on 15/28 roles and collapses Reference lower/upper ranges. |
| **4** | Automation Formula | **NEEDS FIX** | **P1-1, P1-3** | `FAST >= MODERATE >= REF` holds at central bound, but `MOD_COPILOT` lower bound (`0.8017x`) < `REF` (`1.0x`), `eff_ai` (`0.9605x`) < `REF`, magic constants `1.1/1.2`, and `TECHNOLOGY_DIFFUSION_BREADTH` is unused. |
| **5** | Augmentation Formula | **VALID** | **P1-1** (minor) | Independently modeled via `aug_i`, `adapt`, `reskill`; allows simultaneous high auto & high aug. Uses magic constant `1.15`. |
| **6** | Demand Resilience | **VALID** | None | Driven by M2 shortage (50%), momentum (35%), wage context (15%) + policy buffer (15%); completely independent of AI exposure. |
| **7** | Transition Pressure | **VALID** | None | Combines `auto_p` (40%), `task_trans` (35%), and demand deficit `100 - demand_res` (25%). Properly distinguishes workflow change from career decline. |
| **8** | Reskilling Urgency | **NEEDS FIX** | **P2-2** | Skill urgency uses `0.40*(100 - demand_res)`, penalizing high-demand skills and giving `instructional_design` `HIGH` urgency in `REFERENCE_2026`. `0/28` roles and `0/16` skills ever reach `VERY HIGH`. |
| **9** | Outlook Taxonomy | **VALID** | None | 5-tier resilience/transformation taxonomy is conceptually superior to `RISING/DECLINING`. |
| **10** | Scenario Formula Traceability | **NEEDS FIX** | **P1-1, P1-3** | All 5 occupations & 5 skills reconstructed to 0.1 precision; exposes `eff_ai` drop in `MODERATE_COPILOT` and unused `diffusion_reach`. |
| **11** | Software Developers Case (2512) | **VALID** | **P2-1** (prose) | Augmentation grows $54.0 \to 77.2 \to 84.0$; demand resilience $75.5 \to 78.9 \to 78.2$; outlook `TRANSFORMING`. (Prose misstated sensitivity tier in Fast Agentic). |
| **12** | Clerical Cases (4110, 4311, 3343) | **VALID** | None | High pressure in `FAST_AGENTIC` (`59.7, 57.7, 49.8` auto; `55.0, 54.5, 51.0` trans_p) emerges organically from high baseline automation + low shortage (`20.0`). |
| **13** | Engineering Resilience (2151, 2152, 2143) | **VALID** | None | `STRONGLY RESILIENT` requires `net_res >= 75.0` AND `auto_p < 20.0`; driven by high shortage (`89.6`) + low baseline auto (`3.0–4.0`), not low auto alone. |
| **14** | Policy Buffer | **VALID** | None | Capped at $15\%$ weight of `demand_resilience` (`max +15.0` pts); cannot make a low-demand role resilient (`4110` stays at `25.8`). |
| **15** | Confidence Propagation | **VALID** | None | 100% invariant with M2 (`19 HIGH, 9 MEDIUM` occupations; `7 HIGH, 7 MEDIUM, 2 LOW` skills). All M2 flags preserved. |
| **16** | $N=0$ OpenAlex Baseline | **VALID** | **P2-1** (prose) | Code properly flags all 4 skills with `w_vol == 0.0` (`data_visualization`, `human_in_the_loop_qa`, `api_integration`, `carbon_footprint_analytics`) with `INSUFFICIENT_HISTORICAL_BASELINE` (prose undercounted as 2). |
| **17** | Major-Group Fallback Profiles | **NEEDS FIX** | **P1-4** | Summary counts mix 20 4-digit roles and 8 `MAJOR_*` fallbacks; 8 of 10 `PRESSURED` roles are `MAJOR_*`. M3 contract must segregate them. |
| **18** | Wage Quality Flags | **NEEDS FIX** | **P1-4** | `MAJOR_1..9` are tagged with `MAJOR_GROUP_WAGE_CONTEXT` and `NO_ROLE_SPECIFIC_WAGE_DATA` plus duplicate `AGGREGATED_FALLBACK` / `AGGREGATE_MAJOR_GROUP`. |
| **19** | Scenario Sensitivity | **NEEDS FIX** | **P1-1, P2-1** | `lower/central/upper` recompute in Mod/Fast, but `MOD_COPILOT` lower bound drops below Reference, and `STRONGLY RESILIENT -> TRANSFORMING` is misclassified as a 2-tier jump (`HIGHLY SENSITIVE`). |
| **20** | Highly Uncertain Outputs | **NEEDS FIX** | **P2-1** | JSON has 6 `HIGHLY SENSITIVE` occupations and 2 skills in `FAST_AGENTIC`, but Stage 10A prose listed the wrong occupations (`2512, 2166, 3514` instead of `2521, 2411, 2421`) and wrong skills (`process_mapping, instructional_design` instead of `esg, carbon`). |
| **21** | Rank Stability | **NEEDS FIX** | **P2-3** | Spearman $\rho = 1.00$ on `automation_pressure` is trivial structural rank preservation from uniform scalar multiplication. `transition_pressure` ($\rho=0.9880$) and `net_resilience` ($\rho=0.9895$) provide genuine multi-channel rank checks. |
| **22** | Category Thresholds | **NEEDS FIX** | **P1-2, P2-1** | `net_res < 55.0` threshold places all 8 `MAJOR_*` fallbacks and 3 `STABLE` roles into `PRESSURED` immediately upon leaving `REFERENCE_2026`. |
| **23** | Scenario Ordering Invariants | **NEEDS FIX** | **P1-1** | Central `FAST >= MOD >= REF` holds for automation, augmentation, and transition pressure, but `effective_ai_pressure` violates `MOD >= REF` (`0.9605x`). |
| **24** | Reskilling Response Assumption | **VALID** | **P3-2** | `MODERATE_COPILOT (60) > FAST_AGENTIC (45)` reflects institutional training lag under rapid shock; needs explicit methodology prominence. |
| **25** | Policy Response Assumption | **VALID** | **P3-2** | `MODERATE_COPILOT (65) > FAST_AGENTIC (60)` reflects regulatory lag behind rapid agentic deployment; needs explicit methodology prominence. |
| **26** | Uncertainty Terminology | **VALID** | None | Strictly labeled as `SCENARIO ASSUMPTION RANGES` and `uncertainty_band`; never `95% CI` or `prediction interval`. |
| **27** | No Future-Accuracy Claims | **VALID** | None | Zero claims of `forecast accuracy`, `prediction accuracy`, or `2030 probability`. |
| **28** | M3 Consumption Contract | **NEEDS FIX** | **P1-4, P2-1** | Must expand contract so M3 consumes decomposed channels, sensitivity warnings, and `evidence_granularity` (`4_DIGIT_OCCUPATION` vs `MAJOR_GROUP_FALLBACK`), never `scenario_outlook` alone. |
| **39** | M3 Ranking Safety | **VALID** | None | Safeguards defined: M6 is context; skill fit remains primary; `PRESSURED` roles can rank if fit + reskilling path exist; `STRONGLY RESILIENT` roles cannot rank with poor fit. |
| **30** | M4 Safety | **VALID** | None | `reskilling_urgency` informs pathway priority only; course selection requires actual candidate skill gaps. |
| **31** | Fairness | **VALID** | None | Zero demographic attributes in formulas; `ScenarioEngine` rejects `age, gender, ethnicity, race, religion, socioeconomic_background`. |
| **32** | Reproducibility | **VALID** | **P3-1** | All JSON/CSV hashes match `scenario_build_manifest_v1.json`. (`stage10b_readiness.md` table had a stale hash string for `m2_v1_1_1_freeze_manifest.json`). |
| **33** | M1 Holdout Provenance | **VALID** | **P3-1** | `m2_v1_1_1_freeze_manifest.json` has exact canonical wording; Stage 10A response header used "zero holdout access" shorthand and is corrected here. |

---

## 3. Complete Defect Ledger (`P0`, `P1`, `P2`, `P3`)

- **P0 Count**: **0**
- **P1 Count**: **4** (`P1-1`, `P1-2`, `P1-3`, `P1-4`)
- **P2 Count**: **3** (`P2-1`, `P2-2`, `P2-3`)
- **P3 Count**: **2** (`P3-1`, `P3-2`)

### Detailed Remediation Scope for Stage 10C
1. **Fix `P1-1` (Anchor Scenario Multipliers to `REFERENCE_2026` & Remove Magic Constants)**:
   - Express `auto_mult`, `aug_mult`, and `ai_press_mult` as ratios anchored directly to the `REFERENCE_2026` central parameters:
     $$\mu_{\text{auto}}(s, b) = \left(\frac{\text{Adopt}_{s,b}}{\text{Adopt}_{\text{ref}}}\right)^{\alpha_1} \left(\frac{\text{Reach}_{s,b}}{\text{Reach}_{\text{ref}}}\right)^{\alpha_2} \left(\frac{\text{Auto}_{s,b}}{\text{Auto}_{\text{ref}}}\right)^{\alpha_3}$$
     where $\text{Adopt}_{\text{ref}}=20, \text{Reach}_{\text{ref}}=10, \text{Auto}_{\text{ref}}=20$ (with exponents calibrated so `REFERENCE_2026` central equals $1.0000$ organically without an `if/else` bypass or magic multipliers `1.1, 1.2, 1.15`, and `MODERATE_COPILOT` lower and central bounds are strictly $> 1.0$).
2. **Fix `P1-2` (Unify Outlook Classification Rule Across All Scenarios)**:
   - Remove `if scenario_id == "REFERENCE_2026"` string-lookup branching in `determine_occupation_outlook()` and `determine_skill_outlook()`. Calibrate the unified continuous threshold function so that `REFERENCE_2026` reproduces baseline M2 outlooks organically via the exact same mathematical rule used in `MODERATE_COPILOT` and `FAST_AGENTIC`.
3. **Fix `P1-3` (Wire `TECHNOLOGY_DIFFUSION_BREADTH` into M6 Equations)**:
   - Incorporate `TECHNOLOGY_DIFFUSION_BREADTH` into `effective_ai_pressure` (e.g., $\mu_{\text{ai}} = (\text{Adopt}/\text{Adopt}_{\text{ref}})^{0.60} (\text{Diff}/\text{Diff}_{\text{ref}})^{0.40}$) and `task_transformation` / `skill_change_needed` so all 8 declared parameters have non-zero, traceable partial derivatives.
4. **Fix `P1-4` (Segregate 4-Digit Occupations from 1-Digit Major Groups & Correct Wage Flags)**:
   - Add explicit `entity_granularity`: `"OCCUPATION_4_DIGIT"` (20 roles) vs `"MAJOR_GROUP_FALLBACK"` (8 groups).
   - Tag `MAJOR_1..9` with `GROUP_LEVEL_DIRECT_WAGE_MEASUREMENT` instead of `MAJOR_GROUP_WAGE_CONTEXT` / `NO_ROLE_SPECIFIC_WAGE_DATA`, and deduplicate `AGGREGATED_FALLBACK` vs `AGGREGATE_MAJOR_GROUP`.
   - Report 4-digit occupation distributions ($N=20$) separately from Major Group fallbacks ($N=8$).
5. **Fix `P2-1`, `P2-2`, `P2-3`, `P3-1`, `P3-2`**:
   - Separate resilience tier order from `TRANSFORMING` flag in sensitivity classification (`P2-1`), reconcile all prose tables with exact JSON outputs (`P2-1`), remove `(100 - demand_resilience)` from skill reskilling urgency (`P2-2`), report `transition_pressure` and `net_resilience` rank correlations alongside structural rank preservation (`P2-3`), and update documentation/provenance strings (`P3-1, P3-2`).

---

## 4. Final Review Gate Verdict

```
TARGETED M6 REMEDIATION REQUIRED
```
*(Do NOT build M3. Do NOT build M4. Do NOT modify frozen M1 or M2. Proceed to bounded Stage 10C remediation).*
