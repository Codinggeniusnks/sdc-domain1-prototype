import json
import math
from pathlib import Path

base_dir = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
trends_dir = base_dir / "data" / "trends" / "processed"
scenarios_dir = base_dir / "data" / "scenarios"

with open(trends_dir / "occupation_trend_profiles_v1_1_1.json", "r", encoding="utf-8") as f:
    occs = json.load(f)["profiles"]

with open(trends_dir / "skill_trend_profiles_v1_1_1.json", "r", encoding="utf-8") as f:
    skills = json.load(f)["profiles"]

with open(scenarios_dir / "scenario_definitions_v1.json", "r", encoding="utf-8") as f:
    defs = json.load(f)

REF_CENTRAL = {
    "AI_ADOPTION_INTENSITY": 20.0,
    "AGENTIC_TASK_REACH": 10.0,
    "AUTOMATION_INTENSITY": 20.0,
    "AUGMENTATION_INTENSITY": 30.0,
    "TECHNOLOGY_DIFFUSION_BREADTH": 25.0,
    "RESKILLING_RESPONSE_STRENGTH": 30.0,
    "POLICY_RESPONSE_STRENGTH": 40.0,
    "ORGANISATIONAL_ADAPTATION_SPEED": 25.0
}

params_by_scen = {}
for sc in defs["scenarios"]:
    params_by_scen[sc["scenario_id"]] = {a["assumption_name"]: a for a in sc["assumptions"]}

def get_multipliers_v1_1(param_dict, bound="central"):
    adopt = param_dict["AI_ADOPTION_INTENSITY"][bound]
    reach = param_dict["AGENTIC_TASK_REACH"][bound]
    auto_i = param_dict["AUTOMATION_INTENSITY"][bound]
    aug_i = param_dict["AUGMENTATION_INTENSITY"][bound]
    diff = param_dict["TECHNOLOGY_DIFFUSION_BREADTH"][bound]
    reskill = param_dict["RESKILLING_RESPONSE_STRENGTH"][bound]
    policy = param_dict["POLICY_RESPONSE_STRENGTH"][bound]
    adapt = param_dict["ORGANISATIONAL_ADAPTATION_SPEED"][bound]

    r_adopt = adopt / REF_CENTRAL["AI_ADOPTION_INTENSITY"]
    r_reach = reach / REF_CENTRAL["AGENTIC_TASK_REACH"]
    r_auto = auto_i / REF_CENTRAL["AUTOMATION_INTENSITY"]
    r_aug = aug_i / REF_CENTRAL["AUGMENTATION_INTENSITY"]
    r_diff = diff / REF_CENTRAL["TECHNOLOGY_DIFFUSION_BREADTH"]
    r_reskill = reskill / REF_CENTRAL["RESKILLING_RESPONSE_STRENGTH"]
    r_policy = policy / REF_CENTRAL["POLICY_RESPONSE_STRENGTH"]
    r_adapt = adapt / REF_CENTRAL["ORGANISATIONAL_ADAPTATION_SPEED"]

    ai_index = (r_adopt ** 0.40) * (r_diff ** 0.35) * (r_reach ** 0.25)
    ai_press_mult = round(ai_index ** 0.35, 4)

    auto_index = (r_auto ** 0.45) * (r_reach ** 0.35) * (r_diff ** 0.20)
    auto_mult = round(auto_index ** 0.40, 4)

    aug_index = (r_aug ** 0.40) * (r_adapt ** 0.25) * (r_reskill ** 0.20) * (r_diff ** 0.15)
    aug_mult = round(aug_index ** 0.35, 4)

    policy_factor = round(policy / 100.0, 4)

    return {
        "ai_press_mult": ai_press_mult,
        "auto_mult": auto_mult,
        "aug_mult": aug_mult,
        "policy_factor": policy_factor,
        "diffusion_ratio": round(r_diff, 4)
    }

def get_base_reference_category_occ(base_outlook, base_auto, base_aug):
    # Deterministic mapping from M2 baseline to M6 Reference category
    if base_outlook == "STRONGLY RISING":
        return "STRONGLY RESILIENT"
    elif base_outlook == "RISING":
        return "RESILIENT"
    elif base_outlook == "STABLE":
        t_trans = 0.50 * base_auto + 0.50 * base_aug
        return "TRANSFORMING" if t_trans >= 30.0 else "RESILIENT"
    elif base_outlook == "DECLINING":
        return "PRESSURED"
    elif base_outlook == "STRONGLY DECLINING":
        return "HIGHLY PRESSURED"
    else:
        return "RESILIENT"

def get_base_reference_category_skill(base_outlook, base_auto, base_aug):
    if base_outlook == "STRONGLY RISING":
        return "STRONGLY RESILIENT"
    elif base_outlook == "RISING":
        return "RESILIENT"
    elif base_outlook == "STABLE":
        return "TRANSFORMING"
    elif base_outlook == "DECLINING":
        return "PRESSURED"
    else:
        return "HIGHLY PRESSURED"

def classify_occupation_scenario_unified(base_ref_cat, auto_p, aug_o, d_res, t_trans, delta):
    net_res = d_res + 0.30 * aug_o - 0.70 * auto_p
    delta_net = delta["demand_resilience_delta"] + 0.30 * delta["augmentation_opportunity_delta"] - 0.70 * delta["automation_pressure_delta"]

    # 1. Severe Pressure: auto_p >= 45 or net_res < 35 or (auto_p >= 40 and demand_res < 35)
    if auto_p >= 45.0 or net_res < 35.0:
        return "HIGHLY PRESSURED"

    # 2. Moderate Pressure: auto_p >= 30.0 and net_res < 55.0 and delta_net < 0
    if auto_p >= 30.0 and net_res < 55.0 and delta_net < -3.0:
        return "HIGHLY PRESSURED" if auto_p >= 40.0 else "PRESSURED"

    if base_ref_cat == "HIGHLY PRESSURED":
        if auto_p >= 35.0 or net_res < 40.0:
            return "HIGHLY PRESSURED"
        return "PRESSURED"

    if base_ref_cat == "PRESSURED":
        if auto_p >= 45.0 or net_res < 35.0:
            return "HIGHLY PRESSURED"
        elif delta_net < -5.0 or auto_p >= 35.0:
            return "PRESSURED"
        else:
            return "PRESSURED"

    # 3. Transforming: strong technical / creative role with high workflow augmentation & reorganization
    if t_trans >= 42.0 and aug_o >= 45.0:
        return "TRANSFORMING"

    # 4. Strongly Resilient / Resilient retention
    if base_ref_cat == "STRONGLY RESILIENT":
        if auto_p < 20.0 and net_res >= 70.0:
            return "STRONGLY RESILIENT"
        elif net_res >= 55.0:
            return "RESILIENT"
        else:
            return "TRANSFORMING"

    if base_ref_cat == "RESILIENT":
        # Monotonicity rule: if net_res increases and auto_p < 30.0, role NEVER becomes pressured!
        if delta_net >= 0.0 and auto_p < 30.0:
            return "RESILIENT"
        elif auto_p >= 30.0 or net_res < 50.0:
            return "PRESSURED"
        else:
            return "RESILIENT"

    if base_ref_cat == "TRANSFORMING":
        if auto_p >= 35.0 and net_res < 50.0:
            return "PRESSURED"
        return "TRANSFORMING"

    return "RESILIENT"

# Run simulation
print("\n=== OCCUPATION PROFILES SIMULATION ===")
for sc_id in ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]:
    p_dict = params_by_scen[sc_id]
    m = get_multipliers_v1_1(p_dict, "central")
    
    outlooks_4dig = []
    outlooks_major = []
    
    for occ in occs:
        code = occ["occupation_code"]
        is_fallback = code.startswith("MAJOR_")
        base_auto = occ.get("automation_exposure", 0.0)
        base_aug = occ.get("augmentation_potential", 0.0)
        base_ai = occ.get("ai_exposure", 0.0)
        shortage = occ.get("demand_shortage_level", 50.0)
        momentum = occ.get("demand_momentum", 50.0)
        wage_mom = occ.get("employment_wage_momentum", 50.0)
        policy_pri = occ.get("policy_priority", 50.0)
        base_outlook = occ.get("overall_outlook", "STABLE")

        base_ref_cat = get_base_reference_category_occ(base_outlook, base_auto, base_aug)
        
        # Calculate central metrics
        eff_ai = round(min(100.0, max(0.0, base_ai * m["ai_press_mult"])), 1)
        auto_p = round(min(100.0, max(0.0, base_auto * m["auto_mult"])), 1)
        aug_o = round(min(100.0, max(0.0, base_aug * m["aug_mult"])), 1)
        pol_buf = round(policy_pri * m["policy_factor"], 1)
        d_base = 0.50 * shortage + 0.35 * momentum + 0.15 * wage_mom
        d_res = round(min(100.0, max(0.0, 0.85 * d_base + 0.15 * pol_buf)), 1)
        t_trans = 0.50 * auto_p + 0.50 * aug_o
        t_press = round(min(100.0, max(0.0, 0.40 * auto_p + 0.35 * t_trans + 0.25 * (100.0 - d_res))), 1)

        # Baseline reference metrics (at m = 1.0)
        pol_buf_ref = round(policy_pri * 0.40, 1)
        d_res_ref = round(min(100.0, max(0.0, 0.85 * d_base + 0.15 * pol_buf_ref)), 1)
        t_trans_ref = 0.50 * base_auto + 0.50 * base_aug
        t_press_ref = round(min(100.0, max(0.0, 0.40 * base_auto + 0.35 * t_trans_ref + 0.25 * (100.0 - d_res_ref))), 1)

        delta = {
            "automation_pressure_delta": round(auto_p - base_auto, 1),
            "augmentation_opportunity_delta": round(aug_o - base_aug, 1),
            "demand_resilience_delta": round(d_res - d_res_ref, 1),
            "transition_pressure_delta": round(t_press - t_press_ref, 1)
        }

        sc_outlook = classify_occupation_scenario_unified(base_ref_cat, auto_p, aug_o, d_res, t_trans, delta)
        
        if is_fallback:
            outlooks_major.append(sc_outlook)
        else:
            outlooks_4dig.append(sc_outlook)

    from collections import Counter
    print(f"\n{sc_id}:")
    print(f"  4-Digit Occupations (N=20): {dict(Counter(outlooks_4dig))}")
    print(f"  Major-Group Fallbacks (N=8): {dict(Counter(outlooks_major))}")
