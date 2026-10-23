# M6–M3 Downstream Safety & Consumption Contract (v1.1.0)

**Governing Purpose**: Bounded, safe consumption of M6 Future Workforce Scenario Engine intelligence by future M3 Role Matching  
**Contract Status**: **`APPROVED & SAFE FOR M3 CONSUMPTION`**  
**Version**: 1.1.0  
**Effective Date**: 2026-10-23  

---

## 1. Upstream Freeze & Architectural Boundaries

1. **M1 Skills Extraction**: `H_blend_0.70A_0.30C1_W1.0` is permanently frozen. Protocol B and Protocol C v2 were unsealed exactly once during Stage 8E for the approved final frozen M1 evaluation. No additional Protocol B or Protocol C v2 access occurred during Stages 9A onward.
2. **M2 Trend Intelligence**: `M2 v1.1.1` is permanently frozen (SHA-256: `cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542`).
3. **M6 Scenario Engine**: `M6 v1.1.0` provides scenario-adjusted foresight inputs. M6 does NOT perform personalized candidate matching; it produces macro and occupational scenario projections to contextualize M3.

---

## 2. Mandatory Downstream Consumption Rules for M3

### Rule 1: Bounded Composite Weight ($\le 15\%$)
In M3 composite scoring:
$$\text{Score}_{\text{composite}} = w_{\text{M1}}\,\text{SkillMatch} + w_{\text{M2}}\,\text{BaselineTrend} + w_{\text{M6}}\,\text{ScenarioModifier}$$
- $w_{\text{M1}} \ge 0.55$: Current demonstrable skills match must always constitute the primary matching anchor.
- $w_{\text{M2}} \le 0.30$: Empirical labor-market demand trend.
- **$w_{\text{M6}} \le 0.15$**: M6 scenario foresight adjustment is strictly bounded to a maximum of $15\%$. Exploratory future scenarios must never overturn strong current skill alignment.

### Rule 2: Fallback Neutrality Clause (P1-4 Enforcement)
- **Primary Ranking Pool**: M3 must rank candidate roles strictly from the 20 four-digit occupations (`entity_granularity == "FOUR_DIGIT_OCCUPATION"`).
- **Fallback Exclusion**: `ONE_DIGIT_MAJOR_GROUP_FALLBACK` entities ($N=8$) must **never be recommended as primary career targets** or ranked directly against 4-digit occupations.
- **Fallback Usage**: If a worker's target role lacks 4-digit crosswalk coverage and falls back to a Major Group profile, M3 must apply a $0.5\times$ attenuation to the scenario modifier and display the `AGGREGATED_MAJOR_GROUP_FALLBACK` warning.

### Rule 3: Zero Demographic Inputs Guarantee
- M3 must never pass demographic variables (`age`, `gender`, `race`, `ethnicity`, `religion`, `marital_status`, `nationality`, `disability`, `socioeconomic_background`) to M6 runtime interfaces. The `ScenarioEngine` enforces this programmatically via strict keyword rejection.

### Rule 4: Confidence & Uncertainty Damping
- Roles carrying `scenario_confidence == "MEDIUM"` (e.g. proxy-crosswalked roles `2411, 2421, 2422, 2423, 2424` or Major Group fallbacks) must have their M6 scenario adjustment damped by $0.80\times$ in M3 ranking.
- Roles exhibiting `downside_risk_stability == "VULNERABLE"` must display an explicit uncertainty warning banner rather than being silently filtered out.

### Rule 5: Non-Punitive Clerical Reskilling Recommendations (M4 Pathway)
- For roles classified as `HIGHLY PRESSURED` with `reskilling_urgency == "VERY HIGH"` (such as `4110 General Office Clerks` or `4311 Accounting Clerks`), M3 must not simply present dead-end scores.
- M3 must automatically bridge to M4 course recommendations by identifying high-augmentation, high-demand adjacent skills (`ai_literacy`, `workflow_automation`, `process_mapping`, `data_privacy_pdpa`) to support active career transition.

---

## 3. Query Interface Signoff

The following methods in [`src/scenario_engine.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/src/scenario_engine.py) are certified for M3 runtime consumption:
- `engine.get_role_scenario(masco_code, scenario_id)`
- `engine.get_skill_scenario(skill_id, scenario_id)`
- `engine.compare_role_scenarios(masco_code)`
- `engine.get_scenario_delta(masco_code, scenario_id)`
- `engine.get_all_role_scenarios(scenario_id, granularity="FOUR_DIGIT_OCCUPATION")`
- `engine.explain_role_scenario(masco_code, scenario_id)`
