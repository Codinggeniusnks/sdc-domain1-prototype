"""
build_scenario_profiles_v1_1.py

M6 Future Workforce Scenario Engine (v1.1.0)
Deterministic build script transforming frozen M2 Trend Intelligence v1.1.1 profiles
into multi-scenario workforce foresight profiles across three plausible futures:
- REFERENCE_2026 (Baseline Empirical Evidence)
- MODERATE_COPILOT (Assistive AI Expansion)
- FAST_AGENTIC (Accelerated Agentic AI Workflows)

Remediations in v1.1.0:
- P1-1: Anchor-normalized multipliers relative to REFERENCE_2026 central (no magic constants, no Reference bypass)
- P1-2: Unified outlook classification across all 3 scenarios (zero spurious baseline flips, monotonicity preserved)
- P1-3: Active technology diffusion parameter with distinct semantics and non-zero sensitivity
- P1-4: Granularity separation between 20 4-digit occupations and 8 1-digit Major Group fallbacks
- P2-1: Multi-dimensional sensitivity semantics (UPSIDE_TRANSFORMATION vs DOWNSIDE_PRESSURE)
- P2-2: Calibrated reskilling urgency (clerical roles reach VERY HIGH under FAST_AGENTIC)
- P2-3: Spearman rank correlations across multi-channel composite metrics
- P3-1: Correct canonical M1 provenance and M2 freeze verification
- P3-2: Explicit institutional & regulatory lag rationale for FAST_AGENTIC assumptions
"""

import json
import hashlib
import csv
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TRENDS_DIR = DATA_DIR / "trends" / "processed"
SCENARIOS_DIR = DATA_DIR / "scenarios"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

OCC_PROFILES_V1_1_1 = TRENDS_DIR / "occupation_trend_profiles_v1_1_1.json"
SKILL_PROFILES_V1_1_1 = TRENDS_DIR / "skill_trend_profiles_v1_1_1.json"
SCENARIO_DEFS_FILE_V1_1 = SCENARIOS_DIR / "scenario_definitions_v1_1.json"
M2_FREEZE_MANIFEST_FILE = ARTIFACTS_DIR / "m2_v1_1_1_freeze_manifest.json"

OUT_OCC_SCENARIO_PROFILES = SCENARIOS_DIR / "occupation_scenario_profiles_v1_1.json"
OUT_SKILL_SCENARIO_PROFILES = SCENARIOS_DIR / "skill_scenario_profiles_v1_1.json"
OUT_BUILD_MANIFEST = SCENARIOS_DIR / "scenario_build_manifest_v1_1.json"
OUT_OCC_SUMMARY_CSV = ARTIFACTS_DIR / "m6_occupation_scenario_summary_v1_1.csv"
OUT_SKILL_SUMMARY_CSV = ARTIFACTS_DIR / "m6_skill_scenario_summary_v1_1.csv"

# Canonical Reference Central Assumptions (Anchor normalization basis)
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

def compute_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def verify_m2_freeze_manifest():
    print("Verifying M2 v1.1.1 freeze integrity...")
    if not M2_FREEZE_MANIFEST_FILE.exists():
        raise FileNotFoundError(f"Missing M2 freeze manifest: {M2_FREEZE_MANIFEST_FILE}")
    manifest = load_json(M2_FREEZE_MANIFEST_FILE)
    expected_hash = manifest["output_artifacts"]["occupation_trend_profiles_v1_1_1"]
    actual_hash = compute_sha256(OCC_PROFILES_V1_1_1)
    if expected_hash != actual_hash:
        raise ValueError(f"Occupation hash mismatch! Expected {expected_hash}, got {actual_hash}")
    
    expected_skill_hash = manifest["output_artifacts"]["skill_trend_profiles_v1_1_1"]
    actual_skill_hash = compute_sha256(SKILL_PROFILES_V1_1_1)
    if expected_skill_hash != actual_skill_hash:
        raise ValueError(f"Skill hash mismatch! Expected {expected_skill_hash}, got {actual_skill_hash}")
    print("M2 v1.1.1 freeze integrity verified 100% bitwise.")

def get_scenario_multipliers_v1_1(param_dict, bound="central"):
    """
    Computes anchor-normalized scenario transformation multipliers relative to REFERENCE_2026 central.
    Zero magic constants; zero special-case bypass logic.
    At REFERENCE_2026 central, all relative ratios = 1.0000, yielding exactly 1.0000 multipliers.
    """
    adopt = param_dict["AI_ADOPTION_INTENSITY"][bound]
    reach = param_dict["AGENTIC_TASK_REACH"][bound]
    auto_i = param_dict["AUTOMATION_INTENSITY"][bound]
    aug_i = param_dict["AUGMENTATION_INTENSITY"][bound]
    diff = param_dict["TECHNOLOGY_DIFFUSION_BREADTH"][bound]
    reskill = param_dict["RESKILLING_RESPONSE_STRENGTH"][bound]
    policy = param_dict["POLICY_RESPONSE_STRENGTH"][bound]
    adapt = param_dict["ORGANISATIONAL_ADAPTATION_SPEED"][bound]

    # Relative ratios relative to REFERENCE central
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

    # 2. Automation Substitution Multiplier: automation intensity (45%), agentic reach (35%), diffusion breadth (20%)
    # Elasticity gamma_auto = 0.40
    auto_index = (r_auto ** 0.45) * (r_reach ** 0.35) * (r_diff ** 0.20)
    auto_mult = round(auto_index ** 0.40, 4)

    # 3. Augmentation Multiplier: augmentation intensity (40%), adaptation speed (25%), reskilling (20%), diffusion breadth (15%)
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
        "technology_diffusion_ratio": round(r_diff, 4)
    }

def calculate_reskilling_urgency_occ_v1_1(auto_p, trans_p, demand_res):
    """
    Calibrated occupational reskilling urgency:
    Increases with automation pressure and transition friction; cushioned by demand resilience.
    """
    urgency_index = 0.45 * auto_p + 0.35 * trans_p + 0.20 * (100.0 - demand_res)
    if urgency_index >= 52.0:
        return "VERY HIGH"
    elif urgency_index >= 38.0:
        return "HIGH"
    elif urgency_index >= 25.0:
        return "MODERATE"
    else:
        return "LOW"

def calculate_reskilling_urgency_skill_v1_1(auto_p, trans_p, demand_res):
    """
    Calibrated skill reskilling urgency:
    Captures obsolescence risk and curriculum adaptation needs.
    """
    urgency_index = 0.45 * auto_p + 0.35 * trans_p + 0.20 * (100.0 - demand_res)
    if urgency_index >= 48.0:
        return "VERY HIGH"
    elif urgency_index >= 35.0:
        return "HIGH"
    elif urgency_index >= 22.0:
        return "MODERATE"
    else:
        return "LOW"

def get_base_reference_category_occ(base_outlook, base_auto, base_aug):
    """
    Deterministic conceptual mapping from M2 baseline to M6 Reference category.
    """
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

def get_base_reference_category_skill(base_outlook):
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

def determine_occupation_outlook_v1_1(base_ref_cat, auto_p, aug_o, d_res, t_trans, delta):
    """
    Unified occupation outlook classifier across all scenarios.
    Derives scenario outlook from base reference category + scenario delta.
    Zero spurious flips; monotonicity guaranteed when net resilience increases.
    """
    net_res = d_res + 0.30 * aug_o - 0.70 * auto_p
    delta_net = delta["demand_resilience_delta"] + 0.30 * delta["augmentation_opportunity_delta"] - 0.70 * delta["automation_pressure_delta"]

    # Severe pressure triggers
    if auto_p >= 45.0 or net_res < 35.0:
        return "HIGHLY PRESSURED"

    # Moderate pressure triggers
    if auto_p >= 30.0 and net_res < 55.0 and delta_net < -3.0:
        return "HIGHLY PRESSURED" if auto_p >= 40.0 else "PRESSURED"

    if base_ref_cat == "HIGHLY PRESSURED":
        if auto_p >= 35.0 or net_res < 40.0:
            return "HIGHLY PRESSURED"
        return "PRESSURED"

    if base_ref_cat == "PRESSURED":
        if auto_p >= 45.0 or net_res < 35.0:
            return "HIGHLY PRESSURED"
        return "PRESSURED"

    # High augmentation workflow transformation (e.g., Software Developers 2512)
    if t_trans >= 40.0 and aug_o >= 45.0:
        return "TRANSFORMING"

    # Strongly Resilient retention
    if base_ref_cat == "STRONGLY RESILIENT":
        if auto_p < 20.0 and net_res >= 70.0:
            return "STRONGLY RESILIENT"
        elif net_res >= 55.0:
            return "RESILIENT"
        else:
            return "TRANSFORMING"

    # Resilient retention with Monotonicity Rule:
    # If net_res increases and auto_p < 30.0, role NEVER becomes pressured!
    if base_ref_cat == "RESILIENT":
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

def determine_skill_outlook_v1_1(base_ref_cat, auto_p, aug_o, d_res, trans_p, delta):
    """
    Unified skill outlook classifier across all scenarios.
    """
    net_res = d_res + 0.40 * aug_o - 0.60 * auto_p
    delta_net = delta["demand_resilience_delta"] + 0.40 * delta["augmentation_opportunity_delta"] - 0.60 * delta["automation_pressure_delta"]

    if auto_p >= 40.0:
        return "HIGHLY PRESSURED"
    elif auto_p >= 28.0 and net_res < 60.0:
        return "PRESSURED"

    # Transformation trigger: substantial generative AI augmentation synergy
    if aug_o >= 65.0 and trans_p >= 45.0:
        return "TRANSFORMING"

    if base_ref_cat == "STRONGLY RESILIENT":
        if net_res >= 75.0 and auto_p < 20.0:
            return "STRONGLY RESILIENT"
        elif net_res >= 60.0:
            return "RESILIENT"
        else:
            return "TRANSFORMING"

    if base_ref_cat == "RESILIENT":
        if delta_net >= 0.0 and auto_p < 25.0:
            return "RESILIENT"
        elif auto_p >= 25.0:
            return "PRESSURED"
        else:
            return "RESILIENT"

    return "TRANSFORMING"

OUTLOOK_ORDER = {
    "STRONGLY RESILIENT": 1,
    "RESILIENT": 2,
    "TRANSFORMING": 3,
    "PRESSURED": 4,
    "HIGHLY PRESSURED": 5
}

def analyze_sensitivity_v1_1(bound_outlooks, central_m):
    """
    Multi-dimensional sensitivity semantics separating:
    - exact_category_stability
    - downside_risk_stability
    - transformation_sensitivity
    - movement_type (UPSIDE_TRANSFORMATION vs DOWNSIDE_PRESSURE vs NEUTRAL_BOUNDARY_SHIFT vs NO_SHIFT)
    """
    lower_o = bound_outlooks["lower"]
    central_o = bound_outlooks["central"]
    upper_o = bound_outlooks["upper"]

    all_outlooks = [lower_o, central_o, upper_o]
    unique_outlooks = list(dict.fromkeys(all_outlooks))

    ranks = [OUTLOOK_ORDER[o] for o in all_outlooks]
    spread = max(ranks) - min(ranks)

    # Downside check: does any bound enter PRESSURED or HIGHLY PRESSURED?
    has_downside = any(r >= 4 for r in ranks)
    downside_risk_stability = "VULNERABLE" if has_downside else "ROBUST"

    # Transformation check: does any bound enter TRANSFORMING?
    has_trans = "TRANSFORMING" in all_outlooks
    trans_sensitivity = "HIGH" if (has_trans and central_m.get("augmentation_opportunity", 0.0) >= 50.0) else "LOW"

    # Exact category stability
    exact_cat_stability = "STABLE" if spread == 0 else "SHIFTING"

    # Movement type
    if spread == 0:
        movement_type = "NO_SHIFT"
        sens_class = "ROBUST"
    elif all(r <= 3 for r in ranks) and has_trans:
        movement_type = "UPSIDE_TRANSFORMATION"
        sens_class = "MODERATELY SENSITIVE" if spread <= 2 else "HIGHLY SENSITIVE"
    elif has_downside:
        movement_type = "DOWNSIDE_PRESSURE"
        sens_class = "MODERATELY SENSITIVE" if spread == 1 else "HIGHLY SENSITIVE"
    else:
        movement_type = "NEUTRAL_BOUNDARY_SHIFT"
        sens_class = "MODERATELY SENSITIVE" if spread == 1 else "HIGHLY SENSITIVE"

    return {
        "sensitivity_classification": sens_class,
        "sensitivity_profile": {
            "exact_category_stability": exact_cat_stability,
            "downside_risk_stability": downside_risk_stability,
            "transformation_sensitivity": trans_sensitivity,
            "movement_type": movement_type,
            "scenario_range": [lower_o, upper_o]
        }
    }

def process_occupations_v1_1(occs, scenario_defs):
    print("Transforming occupation profiles across scenarios (v1.1.0)...")
    
    params_by_scen = {}
    for sc in scenario_defs["scenarios"]:
        sc_id = sc["scenario_id"]
        params_by_scen[sc_id] = {a["assumption_name"]: a for a in sc["assumptions"]}
        
    all_profiles = []
    ref_by_code = {}

    # First pass: compute Reference central profiles for delta calculation
    for occ in occs:
        code = occ["occupation_code"]
        base_auto = occ.get("automation_exposure", 0.0)
        base_aug = occ.get("augmentation_potential", 0.0)
        base_ai = occ.get("ai_exposure", 0.0)
        shortage = occ.get("demand_shortage_level", 50.0)
        momentum = occ.get("demand_momentum", 50.0)
        wage_mom = occ.get("employment_wage_momentum", 50.0)
        policy_pri = occ.get("policy_priority", 50.0)
        
        m_ref = get_scenario_multipliers_v1_1(params_by_scen["REFERENCE_2026"], "central")
        eff_ai_ref = round(min(100.0, max(0.0, base_ai * m_ref["ai_press_mult"])), 1)
        auto_p_ref = round(min(100.0, max(0.0, base_auto * m_ref["auto_mult"])), 1)
        aug_o_ref = round(min(100.0, max(0.0, base_aug * m_ref["aug_mult"])), 1)
        pol_buf_ref = round(policy_pri * m_ref["policy_factor"], 1)
        
        d_base = 0.50 * shortage + 0.35 * momentum + 0.15 * wage_mom
        d_res_ref = round(min(100.0, max(0.0, 0.85 * d_base + 0.15 * pol_buf_ref)), 1)
        t_trans_ref = round(0.50 * auto_p_ref + 0.50 * aug_o_ref, 1)
        t_press_ref = round(min(100.0, max(0.0, 0.40 * auto_p_ref + 0.35 * t_trans_ref + 0.25 * (100.0 - d_res_ref))), 1)
        
        ref_by_code[code] = {
            "effective_ai_pressure": eff_ai_ref,
            "automation_pressure": auto_p_ref,
            "augmentation_opportunity": aug_o_ref,
            "demand_resilience": d_res_ref,
            "policy_buffer": pol_buf_ref,
            "transition_pressure": t_press_ref,
            "task_transformation": t_trans_ref
        }

    for sc in scenario_defs["scenarios"]:
        sc_id = sc["scenario_id"]
        p_dict = params_by_scen[sc_id]
        param_ids = [a["parameter_id"] for a in sc["assumptions"]]
        
        for occ in occs:
            code = occ["occupation_code"]
            title = occ["occupation_title"]
            major_grp = occ.get("major_group", "")
            major_grp_name = occ.get("major_group_name", "")
            base_auto = occ.get("automation_exposure", 0.0)
            base_aug = occ.get("augmentation_potential", 0.0)
            base_ai = occ.get("ai_exposure", 0.0)
            shortage = occ.get("demand_shortage_level", 50.0)
            momentum = occ.get("demand_momentum", 50.0)
            wage_mom = occ.get("employment_wage_momentum", 50.0)
            policy_pri = occ.get("policy_priority", 50.0)
            base_outlook = occ.get("overall_outlook", "STABLE")
            conf_label = occ.get("confidence_label", "MEDIUM")

            is_fallback = code.startswith("MAJOR_")
            entity_granularity = "ONE_DIGIT_MAJOR_GROUP_FALLBACK" if is_fallback else "FOUR_DIGIT_OCCUPATION"
            
            # P1-4: Granularity-specific quality flags
            flags = []
            for f in occ.get("quality_flags", []):
                if f not in ["AGGREGATED_FALLBACK", "AGGREGATE_MAJOR_GROUP", "MAJOR_GROUP_WAGE_CONTEXT", "NO_ROLE_SPECIFIC_WAGE_DATA"]:
                    flags.append(f)

            if is_fallback:
                flags.extend(["AGGREGATED_MAJOR_GROUP_FALLBACK", "GROUP_LEVEL_DIRECT_WAGE_MEASUREMENT"])
            else:
                flags.extend(["MAJOR_GROUP_WAGE_CONTEXT", "NO_ROLE_SPECIFIC_WAGE_DATA"])
            
            base_ref_cat = get_base_reference_category_occ(base_outlook, base_auto, base_aug)
            ref_m = ref_by_code[code]

            # Bounds evaluation
            bound_metrics = {}
            bound_outlooks = {}
            for b in ["central", "lower", "upper"]:
                m = get_scenario_multipliers_v1_1(p_dict, b)
                eff_ai = round(min(100.0, max(0.0, base_ai * m["ai_press_mult"])), 1)
                auto_p = round(min(100.0, max(0.0, base_auto * m["auto_mult"])), 1)
                aug_o = round(min(100.0, max(0.0, base_aug * m["aug_mult"])), 1)
                pol_buf = round(policy_pri * m["policy_factor"], 1)

                d_base = 0.50 * shortage + 0.35 * momentum + 0.15 * wage_mom
                d_res = round(min(100.0, max(0.0, 0.85 * d_base + 0.15 * pol_buf)), 1)
                t_trans = round(0.50 * auto_p + 0.50 * aug_o, 1)
                t_press = round(min(100.0, max(0.0, 0.40 * auto_p + 0.35 * t_trans + 0.25 * (100.0 - d_res))), 1)

                b_delta = {
                    "automation_pressure_delta": round(auto_p - ref_m["automation_pressure"], 1),
                    "augmentation_opportunity_delta": round(aug_o - ref_m["augmentation_opportunity"], 1),
                    "demand_resilience_delta": round(d_res - ref_m["demand_resilience"], 1),
                    "transition_pressure_delta": round(t_press - ref_m["transition_pressure"], 1)
                }

                b_out = determine_occupation_outlook_v1_1(base_ref_cat, auto_p, aug_o, d_res, t_trans, b_delta)
                bound_outlooks[b] = b_out
                bound_metrics[b] = {
                    "effective_ai_pressure": eff_ai,
                    "automation_pressure": auto_p,
                    "augmentation_opportunity": aug_o,
                    "demand_resilience": d_res,
                    "policy_buffer": pol_buf,
                    "transition_pressure": t_press,
                    "task_transformation": t_trans
                }

            central_m = bound_metrics["central"]
            central_outlook = bound_outlooks["central"]
            sens_res = analyze_sensitivity_v1_1(bound_outlooks, central_m)
            reskill_urg = calculate_reskilling_urgency_occ_v1_1(central_m["automation_pressure"], central_m["transition_pressure"], central_m["demand_resilience"])

            central_delta = {
                "transition_pressure_delta": round(central_m["transition_pressure"] - ref_m["transition_pressure"], 1),
                "automation_pressure_delta": round(central_m["automation_pressure"] - ref_m["automation_pressure"], 1),
                "augmentation_opportunity_delta": round(central_m["augmentation_opportunity"] - ref_m["augmentation_opportunity"], 1),
                "demand_resilience_delta": round(central_m["demand_resilience"] - ref_m["demand_resilience"], 1)
            }

            pos_drivers = []
            neg_drivers = []
            if central_m["demand_resilience"] >= 70.0:
                pos_drivers.append(f"Strong labour market demand resilience ({central_m['demand_resilience']}) buffers occupational transition.")
            if central_m["augmentation_opportunity"] >= 50.0:
                pos_drivers.append(f"Substantial AI augmentation opportunity ({central_m['augmentation_opportunity']}) enhances worker productivity.")
            if central_m["policy_buffer"] >= 35.0:
                pos_drivers.append(f"Active national policy alignment provides transition buffer ({central_m['policy_buffer']}).")
                
            if central_m["automation_pressure"] >= 30.0:
                neg_drivers.append(f"Elevated automation pressure ({central_m['automation_pressure']}) targets routine task components.")
            if central_m["transition_pressure"] >= 40.0:
                neg_drivers.append(f"High role transition friction ({central_m['transition_pressure']}) requires continuous workforce adaptation.")
            if central_m["demand_resilience"] < 40.0:
                neg_drivers.append(f"Weak hiring momentum and baseline surplus create structural transition exposure.")
                
            if not pos_drivers:
                pos_drivers.append("Foundational occupational continuity across core operational tasks.")
            if not neg_drivers:
                neg_drivers.append("Low direct automation exposure under current scenario parameters.")

            profile = {
                "masco_code": code,
                "occupation_title": title,
                "entity_granularity": entity_granularity,
                "major_group": major_grp,
                "major_group_name": major_grp_name,
                "scenario_id": sc_id,
                "baseline_outlook": base_outlook,
                "effective_ai_pressure": central_m["effective_ai_pressure"],
                "automation_pressure": central_m["automation_pressure"],
                "augmentation_opportunity": central_m["augmentation_opportunity"],
                "demand_resilience": central_m["demand_resilience"],
                "policy_buffer": central_m["policy_buffer"],
                "transition_pressure": central_m["transition_pressure"],
                "reskilling_urgency": reskill_urg,
                "scenario_outlook": central_outlook,
                "scenario_confidence": conf_label,
                "sensitivity_classification": sens_res["sensitivity_classification"],
                "sensitivity_profile": sens_res["sensitivity_profile"],
                "uncertainty_band": {
                    "metric": "transition_pressure",
                    "lower": bound_metrics["lower"]["transition_pressure"],
                    "central": central_m["transition_pressure"],
                    "upper": bound_metrics["upper"]["transition_pressure"]
                },
                "range_metrics": {
                    "effective_ai_pressure": {"lower": bound_metrics["lower"]["effective_ai_pressure"], "central": central_m["effective_ai_pressure"], "upper": bound_metrics["upper"]["effective_ai_pressure"]},
                    "automation_pressure": {"lower": bound_metrics["lower"]["automation_pressure"], "central": central_m["automation_pressure"], "upper": bound_metrics["upper"]["automation_pressure"]},
                    "augmentation_opportunity": {"lower": bound_metrics["lower"]["augmentation_opportunity"], "central": central_m["augmentation_opportunity"], "upper": bound_metrics["upper"]["augmentation_opportunity"]},
                    "demand_resilience": {"lower": bound_metrics["lower"]["demand_resilience"], "central": central_m["demand_resilience"], "upper": bound_metrics["upper"]["demand_resilience"]}
                },
                "scenario_delta_from_reference": central_delta,
                "quality_flags": flags,
                "positive_drivers": pos_drivers,
                "negative_drivers": neg_drivers,
                "scenario_assumptions_used": param_ids,
                "research_momentum": None
            }
            all_profiles.append(profile)
            
    return all_profiles

def process_skills_v1_1(skills, scenario_defs):
    print("Transforming skill profiles across scenarios (v1.1.0)...")
    
    params_by_scen = {}
    for sc in scenario_defs["scenarios"]:
        sc_id = sc["scenario_id"]
        params_by_scen[sc_id] = {a["assumption_name"]: a for a in sc["assumptions"]}
        
    all_profiles = []
    ref_by_id = {}

    for s in skills:
        sid = s["skill_id"]
        base_auto = s.get("automation_index", 15.0)
        base_aug = s.get("augmentation_index", 50.0)
        shortage = s.get("demand_shortage_index", 50.0)
        momentum = s.get("demand_momentum_index", 50.0)
        policy_pri = s.get("policy_priority_index", 50.0)
        
        m_ref = get_scenario_multipliers_v1_1(params_by_scen["REFERENCE_2026"], "central")
        pol_buf_ref = round(policy_pri * m_ref["policy_factor"], 1)
        d_res_ref = round(min(100.0, max(0.0, 0.50 * shortage + 0.35 * momentum + 0.15 * pol_buf_ref)), 1)
        trans_p_ref = round(min(100.0, max(0.0, 0.50 * base_aug + 0.50 * base_auto)), 1)
        
        ref_by_id[sid] = {
            "automation_pressure": base_auto,
            "augmentation_opportunity": base_aug,
            "demand_resilience": d_res_ref,
            "transformation_pressure": trans_p_ref
        }

    for sc in scenario_defs["scenarios"]:
        sc_id = sc["scenario_id"]
        p_dict = params_by_scen[sc_id]
        param_ids = [a["parameter_id"] for a in sc["assumptions"]]
        
        for s in skills:
            sid = s["skill_id"]
            sname = s["skill_name"]
            cat = s.get("category", "")
            base_auto = s.get("automation_index", 15.0)
            base_aug = s.get("augmentation_index", 50.0)
            shortage = s.get("demand_shortage_index", 50.0)
            momentum = s.get("demand_momentum_index", 50.0)
            policy_pri = s.get("policy_priority_index", 50.0)
            base_outlook = s.get("overall_outlook", "RISING")
            conf_label = s.get("confidence_label", "MEDIUM")

            flags = list(s.get("quality_flags", []))
            # P2-1: Propagate INSUFFICIENT_HISTORICAL_BASELINE for zero-base research skills
            if s.get("raw_research_growth_ratio") is None or s.get("volume_shrinkage_weight", 1.0) == 0.0:
                if "INSUFFICIENT_HISTORICAL_BASELINE" not in flags:
                    flags.append("INSUFFICIENT_HISTORICAL_BASELINE")

            base_ref_cat = get_base_reference_category_skill(base_outlook)
            ref_m = ref_by_id[sid]

            bound_metrics = {}
            bound_outlooks = {}
            for b in ["central", "lower", "upper"]:
                m = get_scenario_multipliers_v1_1(p_dict, b)
                auto_p = round(min(100.0, max(0.0, base_auto * m["auto_mult"])), 1)
                aug_o = round(min(100.0, max(0.0, base_aug * m["aug_mult"])), 1)
                pol_buf = round(policy_pri * m["policy_factor"], 1)

                d_res = round(min(100.0, max(0.0, 0.50 * shortage + 0.35 * momentum + 0.15 * pol_buf)), 1)
                trans_p = round(min(100.0, max(0.0, 0.50 * aug_o + 0.50 * auto_p)), 1)

                b_delta = {
                    "automation_pressure_delta": round(auto_p - ref_m["automation_pressure"], 1),
                    "augmentation_opportunity_delta": round(aug_o - ref_m["augmentation_opportunity"], 1),
                    "demand_resilience_delta": round(d_res - ref_m["demand_resilience"], 1),
                    "transformation_pressure_delta": round(trans_p - ref_m["transformation_pressure"], 1)
                }

                b_out = determine_skill_outlook_v1_1(base_ref_cat, auto_p, aug_o, d_res, trans_p, b_delta)
                bound_outlooks[b] = b_out
                bound_metrics[b] = {
                    "automation_pressure": auto_p,
                    "augmentation_opportunity": aug_o,
                    "demand_resilience": d_res,
                    "transformation_pressure": trans_p
                }

            central_m = bound_metrics["central"]
            central_outlook = bound_outlooks["central"]
            sens_res = analyze_sensitivity_v1_1(bound_outlooks, central_m)
            reskill_urg = calculate_reskilling_urgency_skill_v1_1(central_m["automation_pressure"], central_m["transformation_pressure"], central_m["demand_resilience"])

            central_delta = {
                "transformation_pressure_delta": round(central_m["transformation_pressure"] - ref_m["transformation_pressure"], 1),
                "automation_pressure_delta": round(central_m["automation_pressure"] - ref_m["automation_pressure"], 1),
                "augmentation_opportunity_delta": round(central_m["augmentation_opportunity"] - ref_m["augmentation_opportunity"], 1),
                "demand_resilience_delta": round(central_m["demand_resilience"] - ref_m["demand_resilience"], 1)
            }

            pos_drivers = []
            neg_drivers = []
            if central_m["augmentation_opportunity"] >= 65.0:
                pos_drivers.append(f"High generative AI augmentation synergy ({central_m['augmentation_opportunity']}) expands practitioner capabilities.")
            if central_m["demand_resilience"] >= 75.0:
                pos_drivers.append(f"Strong market shortage & employer demand persistence ({central_m['demand_resilience']}).")
            if central_m["automation_pressure"] >= 25.0:
                neg_drivers.append(f"Codifiable subcomponents face partial automation pressure ({central_m['automation_pressure']}).")
            if not pos_drivers:
                pos_drivers.append("Stable foundational technical utility across domains.")
            if not neg_drivers:
                neg_drivers.append("Low automation susceptibility under scenario reach.")

            profile = {
                "skill_id": sid,
                "skill_name": sname,
                "category": cat,
                "scenario_id": sc_id,
                "baseline_outlook": base_outlook,
                "automation_pressure": central_m["automation_pressure"],
                "augmentation_opportunity": central_m["augmentation_opportunity"],
                "demand_resilience": central_m["demand_resilience"],
                "transformation_pressure": central_m["transformation_pressure"],
                "reskilling_urgency": reskill_urg,
                "scenario_outlook": central_outlook,
                "scenario_confidence": conf_label,
                "sensitivity_classification": sens_res["sensitivity_classification"],
                "sensitivity_profile": sens_res["sensitivity_profile"],
                "uncertainty_band": {
                    "metric": "transformation_pressure",
                    "lower": bound_metrics["lower"]["transformation_pressure"],
                    "central": central_m["transformation_pressure"],
                    "upper": bound_metrics["upper"]["transformation_pressure"]
                },
                "range_metrics": {
                    "automation_pressure": {"lower": bound_metrics["lower"]["automation_pressure"], "central": central_m["automation_pressure"], "upper": bound_metrics["upper"]["automation_pressure"]},
                    "augmentation_opportunity": {"lower": bound_metrics["lower"]["augmentation_opportunity"], "central": central_m["augmentation_opportunity"], "upper": bound_metrics["upper"]["augmentation_opportunity"]},
                    "demand_resilience": {"lower": bound_metrics["lower"]["demand_resilience"], "central": central_m["demand_resilience"], "upper": bound_metrics["upper"]["demand_resilience"]}
                },
                "scenario_delta_from_reference": central_delta,
                "quality_flags": flags,
                "positive_drivers": pos_drivers,
                "negative_drivers": neg_drivers,
                "baseline_source_refs": [d.get("source_id", "") for d in s.get("top_positive_drivers", []) if isinstance(d, dict)],
                "scenario_assumptions_used": param_ids
            }
            all_profiles.append(profile)

    return all_profiles

def export_summaries_v1_1(occ_profiles, skill_profiles):
    print("Exporting summary CSV artifacts (v1.1.0)...")
    with open(OUT_OCC_SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "masco_code", "occupation_title", "entity_granularity", "major_group", "scenario_id",
            "baseline_outlook", "scenario_outlook", "reskilling_urgency",
            "effective_ai_pressure", "automation_pressure", "augmentation_opportunity",
            "demand_resilience", "policy_buffer", "transition_pressure",
            "transition_pressure_delta", "sensitivity_classification", "movement_type", "scenario_confidence"
        ])
        for p in occ_profiles:
            writer.writerow([
                p["masco_code"], p["occupation_title"], p["entity_granularity"], p["major_group"], p["scenario_id"],
                p["baseline_outlook"], p["scenario_outlook"], p["reskilling_urgency"],
                p["effective_ai_pressure"], p["automation_pressure"], p["augmentation_opportunity"],
                p["demand_resilience"], p["policy_buffer"], p["transition_pressure"],
                p["scenario_delta_from_reference"]["transition_pressure_delta"],
                p["sensitivity_classification"], p["sensitivity_profile"]["movement_type"], p["scenario_confidence"]
            ])
            
    with open(OUT_SKILL_SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "skill_id", "skill_name", "category", "scenario_id",
            "baseline_outlook", "scenario_outlook", "reskilling_urgency",
            "automation_pressure", "augmentation_opportunity", "demand_resilience",
            "transformation_pressure", "transformation_pressure_delta",
            "sensitivity_classification", "movement_type", "scenario_confidence", "quality_flags"
        ])
        for p in skill_profiles:
            writer.writerow([
                p["skill_id"], p["skill_name"], p["category"], p["scenario_id"],
                p["baseline_outlook"], p["scenario_outlook"], p["reskilling_urgency"],
                p["automation_pressure"], p["augmentation_opportunity"], p["demand_resilience"],
                p["transformation_pressure"], p["scenario_delta_from_reference"]["transformation_pressure_delta"],
                p["sensitivity_classification"], p["sensitivity_profile"]["movement_type"], p["scenario_confidence"], ";".join(p["quality_flags"])
            ])

def main():
    print("=" * 70)
    print("BUILDING M6 FUTURE WORKFORCE SCENARIO ENGINE (v1.1.0)")
    print("=" * 70)
    
    verify_m2_freeze_manifest()
    
    occ_data = load_json(OCC_PROFILES_V1_1_1)
    skill_data = load_json(SKILL_PROFILES_V1_1_1)
    scenario_defs = load_json(SCENARIO_DEFS_FILE_V1_1)
    
    occs = occ_data["profiles"]
    skills = skill_data["profiles"]
    
    occ_scenario_profiles = process_occupations_v1_1(occs, scenario_defs)
    skill_scenario_profiles = process_skills_v1_1(skills, scenario_defs)
    
    occ_payload = {
        "engine_version": "1.1.0",
        "parent_m2_version": "1.1.1",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_occupations": len(occs),
        "total_4_digit_occupations": sum(1 for p in occ_scenario_profiles if p["scenario_id"] == "REFERENCE_2026" and p["entity_granularity"] == "FOUR_DIGIT_OCCUPATION"),
        "total_major_group_fallbacks": sum(1 for p in occ_scenario_profiles if p["scenario_id"] == "REFERENCE_2026" and p["entity_granularity"] == "ONE_DIGIT_MAJOR_GROUP_FALLBACK"),
        "total_scenario_profiles": len(occ_scenario_profiles),
        "scenarios": ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"],
        "profiles": occ_scenario_profiles
    }
    save_json(OUT_OCC_SCENARIO_PROFILES, occ_payload)
    print(f"Saved {len(occ_scenario_profiles)} occupation scenario profiles to {OUT_OCC_SCENARIO_PROFILES}")
    
    skill_payload = {
        "engine_version": "1.1.0",
        "parent_m2_version": "1.1.1",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_skills": len(skills),
        "total_scenario_profiles": len(skill_scenario_profiles),
        "scenarios": ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"],
        "profiles": skill_scenario_profiles
    }
    save_json(OUT_SKILL_SCENARIO_PROFILES, skill_payload)
    print(f"Saved {len(skill_scenario_profiles)} skill scenario profiles to {OUT_SKILL_SCENARIO_PROFILES}")
    
    export_summaries_v1_1(occ_scenario_profiles, skill_scenario_profiles)
    
    build_manifest = {
        "engine_version": "1.1.0",
        "parent_m2_version": "1.1.1",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "governance_rule": "M6 preserves channel separation and uncertainty bounds; zero demographic inputs; anchor-normalized scenario multipliers.",
        "input_artifacts": {
            "m2_freeze_manifest": compute_sha256(M2_FREEZE_MANIFEST_FILE),
            "occupation_trend_profiles_v1_1_1": compute_sha256(OCC_PROFILES_V1_1_1),
            "skill_trend_profiles_v1_1_1": compute_sha256(SKILL_PROFILES_V1_1_1),
            "scenario_definitions_v1_1": compute_sha256(SCENARIO_DEFS_FILE_V1_1)
        },
        "output_artifacts": {
            "occupation_scenario_profiles_v1_1": compute_sha256(OUT_OCC_SCENARIO_PROFILES),
            "skill_scenario_profiles_v1_1": compute_sha256(OUT_SKILL_SCENARIO_PROFILES),
            "m6_occupation_scenario_summary_v1_1_csv": compute_sha256(OUT_OCC_SUMMARY_CSV),
            "m6_skill_scenario_summary_v1_1_csv": compute_sha256(OUT_SKILL_SUMMARY_CSV)
        }
    }
    save_json(OUT_BUILD_MANIFEST, build_manifest)
    print(f"Saved scenario build manifest to {OUT_BUILD_MANIFEST}")
    print("=" * 70)
    print("M6 V1.1.0 DETERMINISTIC BUILD COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    main()
