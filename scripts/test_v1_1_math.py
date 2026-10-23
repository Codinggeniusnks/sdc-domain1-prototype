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

# Reference Central Assumptions:
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

    # Normalized relative ratios:
    r_adopt = adopt / REF_CENTRAL["AI_ADOPTION_INTENSITY"]
    r_reach = reach / REF_CENTRAL["AGENTIC_TASK_REACH"]
    r_auto = auto_i / REF_CENTRAL["AUTOMATION_INTENSITY"]
    r_aug = aug_i / REF_CENTRAL["AUGMENTATION_INTENSITY"]
    r_diff = diff / REF_CENTRAL["TECHNOLOGY_DIFFUSION_BREADTH"]
    r_reskill = reskill / REF_CENTRAL["RESKILLING_RESPONSE_STRENGTH"]
    r_policy = policy / REF_CENTRAL["POLICY_RESPONSE_STRENGTH"]
    r_adapt = adapt / REF_CENTRAL["ORGANISATIONAL_ADAPTATION_SPEED"]

    # 1. Macro AI Pressure: adoption intensity (40%), diffusion breadth (35%), agentic reach (25%)
    # Elasticity gamma_ai = 0.35
    ai_index = (r_adopt ** 0.40) * (r_diff ** 0.35) * (r_reach ** 0.25)
    ai_press_mult = round(ai_index ** 0.35, 4)

    # 2. Automation Multiplier: automation intensity (45%), agentic reach (35%), diffusion breadth (20%)
    # Elasticity gamma_auto = 0.40
    auto_index = (r_auto ** 0.45) * (r_reach ** 0.35) * (r_diff ** 0.20)
    auto_mult = round(auto_index ** 0.40, 4)

    # 3. Augmentation Multiplier: augmentation intensity (40%), adaptation speed (25%), reskilling (20%), diffusion (15%)
    # Elasticity gamma_aug = 0.35
    aug_index = (r_aug ** 0.40) * (r_adapt ** 0.25) * (r_reskill ** 0.20) * (r_diff ** 0.15)
    aug_mult = round(aug_index ** 0.35, 4)

    # 4. Policy Factor: policy index / 100
    policy_factor = round(policy / 100.0, 4)

    return {
        "ai_press_mult": ai_press_mult,
        "auto_mult": auto_mult,
        "aug_mult": aug_mult,
        "policy_factor": policy_factor,
        "diffusion_ratio": round(r_diff, 4)
    }

print("=== SCENARIO MULTIPLIERS V1.1 ===")
for sc_id in ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]:
    p_dict = params_by_scen[sc_id]
    for b in ["lower", "central", "upper"]:
        m = get_multipliers_v1_1(p_dict, b)
        print(f"{sc_id:<16} {b:<8}: ai_mult={m['ai_press_mult']:.4f}, auto_mult={m['auto_mult']:.4f}, aug_mult={m['aug_mult']:.4f}, pol={m['policy_factor']:.4f}")
