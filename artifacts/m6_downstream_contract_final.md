# M6 Downstream Safety & Consumption Contract (Final Freeze Edition)

**Governing Purpose**: Final, unalterable safety rules governing how future M3 Role Matching and M4 Training Pathways consume M6 Scenario Engine v1.1.0 outputs.  
**Contract Status**: **`CERTIFIED & PERMANENTLY BOUND`**  
**Engine Version**: M6 v1.1.0 (Frozen)  
**Date**: 2026-10-23  

---

## 1. Upstream Freeze & Architectural Independence

1. **M1 Skills Extraction**: `H_blend_0.70A_0.30C1_W1.0` is permanently frozen. Protocol B and Protocol C v2 were unsealed exactly once during Stage 8E for the approved final frozen M1 evaluation. No additional Protocol B or Protocol C v2 access occurred during Stages 9A onward.
2. **M2 Trend Intelligence**: `M2 v1.1.1` is permanently frozen (SHA-256: `cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542`).
3. **M6 Scenario Engine**: `M6 v1.1.0` is permanently frozen (Manifest SHA-256: `ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5`).

---

## 2. Binding Consumption Rules for M3 Role Matching

### Rule 1: Bounded Composite Weight Cap ($\le 15\%$)
In M3 composite scoring:
$$\text{Score}_{\text{composite}} = w_{\text{M1}}\,\text{SkillMatch} + w_{\text{M2}}\,\text{BaselineTrend} + w_{\text{M6}}\,\text{ScenarioModifier}$$
- Current demonstrable skill alignment ($w_{\text{M1}} \ge 0.55$) and empirical labour shortage momentum ($w_{\text{M2}} \le 0.30$) form the primary matching criteria.
- **$w_{\text{M6}} \le 0.15$**: Scenario foresight modifiers must never exceed $15\%$ composite weight. Future exploratory scenarios must contextualize recommendations, never distort candidate-skill fit.

### Rule 2: Fallback Neutrality Enforcement (Check 13)
- **Primary Matching Pool**: M3 must draw candidate recommendations strictly from the 20 specific 4-digit occupations (`entity_granularity == "FOUR_DIGIT_OCCUPATION"`).
- **Prohibition of Direct Competition**: `ONE_DIGIT_MAJOR_GROUP_FALLBACK` entities ($N=8$) must **never be ranked as candidate career targets** alongside 4-digit occupations.
- **Controlled Fallback Usage**: Fallbacks may only be surfaced when a user's role has no 4-digit mapping, in which case the scenario adjustment is attenuated by $0.5\times$ and displays the `AGGREGATED_MAJOR_GROUP_FALLBACK` badge.

### Rule 3: Zero Demographic Inputs Guarantee (Check 27)
- Downstream M3 callers are strictly forbidden from passing protected demographic attributes (`age`, `gender`, `race`, `ethnicity`, `religion`, `marital_status`, `nationality`, `disability`, `socioeconomic_background`).
- `ScenarioEngine` enforces this via programmatic runtime keyword rejection, throwing a `ValueError` on any violation.

### Rule 4: Non-Punitive Career Transition Semantics (Check 29)
- **`HIGHLY PRESSURED` does NOT mean "never recommend this career."** It signals to M3 that if a user matches this role, the system must highlight transitional friction and pair the recommendation with an active reskilling pathway.
- **`STRONGLY RESILIENT` does NOT mean "recommend regardless of skill fit."** A user with no programming background must never be recommended Software Developer purely because its resilience is high.

### Rule 5: Confidence & Uncertainty Damping (Check 23 & 24)
- Roles carrying `scenario_confidence == "MEDIUM"` (e.g. proxy-crosswalked roles `2411, 2421, 2422, 2423, 2424` or Major Group fallbacks) must have their M6 scenario modifier attenuated by $0.80\times$ in M3.
- Profiles flagged with `downside_risk_stability == "VULNERABLE"` must display an explicit uncertainty indicator in the user interface.

---

## 3. Binding Consumption Rules for M4 Training Pathways (Check 30)

1. **Prioritization Role**: `reskilling_urgency` (`LOW`, `MODERATE`, `HIGH`, `VERY HIGH`) serves strictly as a course sequencing and urgency prioritization input.
2. **Safety Boundary**: Urgency must **NOT directly dictate mandatory training duration, course difficulty, or minimum credit hours**.
3. **Augmentation Pathway Bridging**: For routine clerical workers facing high automation pressure (`4110`, `4311`, `3343`), M4 must prioritize future-proof adjacent augmentation skills (`ai_literacy`, `workflow_automation`, `process_mapping`, `data_privacy_pdpa`).
