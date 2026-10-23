"""
build_scenario_profiles.py

M6 Future Workforce Scenario Engine (v1.0.0)
Deterministic build script transforming frozen M2 Trend Intelligence v1.1.1 profiles
into multi-scenario workforce foresight profiles across three plausible futures:
- REFERENCE_2026 (Baseline Empirical Evidence)
- MODERATE_COPILOT (Assistive AI Expansion)
- FAST_AGENTIC (Accelerated Agentic AI Workflows)

Preserves channel separation (Automation vs Augmentation vs Demand Resilience),
propagates quality flags, prohibits role-specific wage forecasting, and handles uncertainty
without fake probabilities.
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
SCENARIO_DEFS_FILE = SCENARIOS_DIR / "scenario_definitions_v1.json"
M2_FREEZE_MANIFEST_FILE = ARTIFACTS_DIR / "m2_v1_1_1_freeze_manifest.json"

OUT_OCC_SCENARIO_PROFILES = SCENARIOS_DIR / "occupation_scenario_profiles_v1.json"
OUT_SKILL_SCENARIO_PROFILES = SCENARIOS_DIR / "skill_scenario_profiles_v1.json"
OUT_BUILD_MANIFEST = SCENARIOS_DIR / "scenario_build_manifest_v1.json"
OUT_OCC_SUMMARY_CSV = ARTIFACTS_DIR / "m6_occupation_scenario_summary.csv"
OUT_SKILL_SUMMARY_CSV = ARTIFACTS_DIR / "m6_skill_scenario_summary.csv"

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

def get_scenario_multipliers(param_dict, scenario_id, bound="central"):
    """
    Computes transparent, bounded multipliers for scenario transformation.
    In REFERENCE_2026, multipliers are strictly 1.0 (zero shock).
    """
    if scenario_id == "REFERENCE_2026":
        return {
            "ai_press_mult": 1.0,
            "auto_mult": 1.0,
            "aug_mult": 1.0,
            "policy_factor": 0.40,
            "diffusion_reach": 0.175
        }
    
    adopt = param_dict["AI_ADOPTION_INTENSITY"][bound]
    reach = param_dict["AGENTIC_TASK_REACH"][bound]
    auto_i = param_dict["AUTOMATION_INTENSITY"][bound]
    aug_i = param_dict["AUGMENTATION_INTENSITY"][bound]
    diff = param_dict["TECHNOLOGY_DIFFUSION_BREADTH"][bound]
    reskill = param_dict["RESKILLING_RESPONSE_STRENGTH"][bound]
    policy = param_dict["POLICY_RESPONSE_STRENGTH"][bound]
    adapt = param_dict["ORGANISATIONAL_ADAPTATION_SPEED"][bound]

    # Automation shock compounding adoption, task reach, and substitution intensity
    auto_scale = ((adopt / 50.0) ** 0.35) * ((reach / 50.0) ** 0.40) * ((auto_i / 50.0) ** 0.25)
    
    # Augmentation shock compounding augmentation intensity, organisational adaptation, reskilling
    aug_scale = ((aug_i / 50.0) ** 0.40) * ((adapt / 50.0) ** 0.30) * ((reskill / 50.0) ** 0.30)
    
    return {
        "ai_press_mult": round(max(0.5, auto_scale * 1.1), 4),
        "auto_mult": round(max(0.5, auto_scale * 1.2), 4),
        "aug_mult": round(max(0.5, aug_scale * 1.15), 4),
        "policy_factor": round(policy / 100.0, 4),
        "diffusion_reach": round((diff + reach) / 200.0, 4)
    }

def calculate_reskilling_urgency(task_trans, trans_p):
    urgency_index = 0.55 * task_trans + 0.45 * trans_p
    if urgency_index >= 55.0:
        return "VERY HIGH"
    elif urgency_index >= 40.0:
        return "HIGH"
    elif urgency_index >= 25.0:
        return "MODERATE"
    else:
        return "LOW"

def determine_occupation_outlook(scenario_id, base_outlook, auto_p, aug_o, demand_res, task_trans):
    net_res = demand_res + 0.30 * aug_o - 0.70 * auto_p
    
    if scenario_id == "REFERENCE_2026":
        if base_outlook == "STRONGLY RISING":
            return "STRONGLY RESILIENT"
        elif base_outlook == "RISING":
            return "RESILIENT"
        elif base_outlook == "STABLE":
            return "TRANSFORMING" if task_trans >= 30.0 else "RESILIENT"
        elif base_outlook == "DECLINING":
            return "PRESSURED"
        elif base_outlook == "STRONGLY DECLINING":
            return "HIGHLY PRESSURED"
        else:
            return "TRANSFORMING"
    else:
        if auto_p >= 45.0 or net_res < 35.0:
            return "HIGHLY PRESSURED"
        elif auto_p >= 30.0 or net_res < 55.0:
            return "PRESSURED"
        elif task_trans >= 42.0 and aug_o >= 45.0:
            return "TRANSFORMING"
        elif net_res >= 75.0 and auto_p < 20.0:
            return "STRONGLY RESILIENT"
        elif net_res >= 60.0:
            return "RESILIENT"
        else:
            return "TRANSFORMING"

def determine_skill_outlook(scenario_id, base_outlook, auto_p, aug_o, demand_res, trans_p):
    net_res = demand_res + 0.40 * aug_o - 0.60 * auto_p
    
    if scenario_id == "REFERENCE_2026":
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
    else:
        if auto_p >= 40.0:
            return "HIGHLY PRESSURED"
        elif auto_p >= 25.0:
            return "PRESSURED"
        elif trans_p >= 45.0 and aug_o >= 55.0:
            return "TRANSFORMING"
        elif net_res >= 80.0:
            return "STRONGLY RESILIENT"
        elif net_res >= 60.0:
            return "RESILIENT"
        else:
            return "TRANSFORMING"

OUTLOOK_ORDER = {
    "STRONGLY RESILIENT": 1,
    "RESILIENT": 2,
    "TRANSFORMING": 3,
    "PRESSURED": 4,
    "HIGHLY PRESSURED": 5
}

def classify_sensitivity(outlooks):
    ranks = [OUTLOOK_ORDER[o] for o in outlooks]
    spread = max(ranks) - min(ranks)
    if spread == 0:
        return "ROBUST"
    elif spread == 1:
        return "MODERATELY SENSITIVE"
    else:
        return "HIGHLY SENSITIVE"

def process_occupations(occs, scenario_defs):
    print("Transforming occupation profiles across scenarios...")
    
    # Pre-parse scenario definitions parameters
    params_by_scen = {}
    for sc in scenario_defs["scenarios"]:
        sc_id = sc["scenario_id"]
        params_by_scen[sc_id] = {
            a["assumption_name"]: a for a in sc["assumptions"]
        }
        
    all_profiles = []
    
    # First pass: compute reference profiles for delta calculation
    ref_by_code = {}
    
    for occ in occs:
        code = occ["occupation_code"]
        base_auto = occ.get("automation_exposure", 0.0)
        base_aug = occ.get("augmentation_potential", 0.0)
        base_ai = occ.get("ai_exposure", 0.0)
        shortage = occ.get("demand_shortage_level", 50.0)
        momentum = occ.get("demand_momentum", 50.0)
        wage_mom = occ.get("employment_wage_momentum", 50.0)
        policy_pri = occ.get("policy_priority", 50.0)
        base_outlook = occ.get("overall_outlook", "STABLE")
        
        m_ref = get_scenario_multipliers(params_by_scen["REFERENCE_2026"], "REFERENCE_2026", "central")
        pol_buf_ref = round(policy_pri * m_ref["policy_factor"], 1)
        d_base = 0.50 * shortage + 0.35 * momentum + 0.15 * wage_mom
        d_res_ref = round(min(100.0, max(0.0, 0.85 * d_base + 0.15 * pol_buf_ref)), 1)
        t_trans_ref = 0.50 * base_auto + 0.50 * base_aug
        t_press_ref = round(min(100.0, max(0.0, 0.40 * base_auto + 0.35 * t_trans_ref + 0.25 * (100.0 - d_res_ref))), 1)
        
        ref_by_code[code] = {
            "effective_ai_pressure": base_ai,
            "automation_pressure": base_auto,
            "augmentation_opportunity": base_aug,
            "demand_resilience": d_res_ref,
            "transition_pressure": t_press_ref
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
            
            # Quality flags
            flags = list(occ.get("quality_flags", []))
            if "MAJOR_GROUP_WAGE_CONTEXT" not in flags:
                flags.append("MAJOR_GROUP_WAGE_CONTEXT")
            if "NO_ROLE_SPECIFIC_WAGE_DATA" not in flags:
                flags.append("NO_ROLE_SPECIFIC_WAGE_DATA")
            if code.startswith("MAJOR_") and "AGGREGATE_MAJOR_GROUP" not in flags:
                flags.append("AGGREGATE_MAJOR_GROUP")
                
            # Bounds evaluation (central, lower, upper)
            bound_metrics = {}
            bound_outlooks = {}
            for b in ["central", "lower", "upper"]:
                m = get_scenario_multipliers(p_dict, sc_id, b)
                if sc_id == "REFERENCE_2026":
                    eff_ai = base_ai
                    auto_p = base_auto
                    aug_o = base_aug
                else:
                    eff_ai = round(min(100.0, max(0.0, base_ai * m["ai_press_mult"])), 1)
                    auto_p = round(min(100.0, max(0.0, base_auto * m["auto_mult"])), 1)
                    aug_o = round(min(100.0, max(0.0, base_aug * m["aug_mult"])), 1)
                
                pol_buf = round(policy_pri * m["policy_factor"], 1)
                d_base = 0.50 * shortage + 0.35 * momentum + 0.15 * wage_mom
                d_res = round(min(100.0, max(0.0, 0.85 * d_base + 0.15 * pol_buf)), 1)
                t_trans = 0.50 * auto_p + 0.50 * aug_o
                t_press = round(min(100.0, max(0.0, 0.40 * auto_p + 0.35 * t_trans + 0.25 * (100.0 - d_res))), 1)
                
                b_out = determine_occupation_outlook(sc_id, base_outlook, auto_p, aug_o, d_res, t_trans)
                bound_outlooks[b] = b_out
                bound_metrics[b] = {
                    "effective_ai_pressure": eff_ai,
                    "automation_pressure": auto_p,
                    "augmentation_opportunity": aug_o,
                    "demand_resilience": d_res,
                    "policy_buffer": pol_buf,
                    "transition_pressure": t_press,
                    "task_transformation": round(t_trans, 1)
                }
                
            central_m = bound_metrics["central"]
            central_outlook = bound_outlooks["central"]
            sens_class = classify_sensitivity(list(bound_outlooks.values()))
            reskill_urg = calculate_reskilling_urgency(central_m["task_transformation"], central_m["transition_pressure"])
            
            # Deltas from reference
            ref_m = ref_by_code[code]
            delta = {
                "transition_pressure_delta": round(central_m["transition_pressure"] - ref_m["transition_pressure"], 1),
                "automation_pressure_delta": round(central_m["automation_pressure"] - ref_m["automation_pressure"], 1),
                "augmentation_opportunity_delta": round(central_m["augmentation_opportunity"] - ref_m["augmentation_opportunity"], 1),
                "demand_resilience_delta": round(central_m["demand_resilience"] - ref_m["demand_resilience"], 1)
            }
            
            # Drivers
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
                "sensitivity_classification": sens_class,
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
                "scenario_delta_from_reference": delta,
                "quality_flags": flags,
                "positive_drivers": pos_drivers,
                "negative_drivers": neg_drivers,
                "scenario_assumptions_used": param_ids,
                "research_momentum": None # Preserved strictly null as in M2
            }
            all_profiles.append(profile)
            
    return all_profiles

def process_skills(skills, scenario_defs):
    print("Transforming skill profiles across scenarios...")
    
    params_by_scen = {}
    for sc in scenario_defs["scenarios"]:
        sc_id = sc["scenario_id"]
        params_by_scen[sc_id] = {
            a["assumption_name"]: a for a in sc["assumptions"]
        }
        
    all_profiles = []
    ref_by_id = {}
    
    for s in skills:
        sid = s["skill_id"]
        base_auto = s.get("automation_index", 15.0)
        base_aug = s.get("augmentation_index", 50.0)
        shortage = s.get("demand_shortage_index", 50.0)
        momentum = s.get("demand_momentum_index", 50.0)
        policy_pri = s.get("policy_priority_index", 50.0)
        
        m_ref = get_scenario_multipliers(params_by_scen["REFERENCE_2026"], "REFERENCE_2026", "central")
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
            if s.get("raw_research_growth_ratio") is None or s.get("volume_shrinkage_weight", 1.0) == 0.0:
                if "INSUFFICIENT_HISTORICAL_BASELINE" not in flags:
                    flags.append("INSUFFICIENT_HISTORICAL_BASELINE")
                    
            bound_metrics = {}
            bound_outlooks = {}
            for b in ["central", "lower", "upper"]:
                m = get_scenario_multipliers(p_dict, sc_id, b)
                if sc_id == "REFERENCE_2026":
                    auto_p = base_auto
                    aug_o = base_aug
                else:
                    auto_p = round(min(100.0, max(0.0, base_auto * m["auto_mult"])), 1)
                    aug_o = round(min(100.0, max(0.0, base_aug * m["aug_mult"])), 1)
                    
                pol_buf = round(policy_pri * m["policy_factor"], 1)
                d_res = round(min(100.0, max(0.0, 0.50 * shortage + 0.35 * momentum + 0.15 * pol_buf)), 1)
                trans_p = round(min(100.0, max(0.0, 0.50 * aug_o + 0.50 * auto_p)), 1)
                b_out = determine_skill_outlook(sc_id, base_outlook, auto_p, aug_o, d_res, trans_p)
                bound_outlooks[b] = b_out
                bound_metrics[b] = {
                    "automation_pressure": auto_p,
                    "augmentation_opportunity": aug_o,
                    "demand_resilience": d_res,
                    "transformation_pressure": trans_p
                }
                
            central_m = bound_metrics["central"]
            central_outlook = bound_outlooks["central"]
            sens_class = classify_sensitivity(list(bound_outlooks.values()))
            
            # Skill reskilling urgency
            urgency_val = 0.60 * central_m["transformation_pressure"] + 0.40 * (100.0 - central_m["demand_resilience"])
            if urgency_val >= 50.0:
                reskill_urg = "VERY HIGH"
            elif urgency_val >= 35.0:
                reskill_urg = "HIGH"
            elif urgency_val >= 20.0:
                reskill_urg = "MODERATE"
            else:
                reskill_urg = "LOW"
                
            ref_m = ref_by_id[sid]
            delta = {
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
                "sensitivity_classification": sens_class,
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
                "scenario_delta_from_reference": delta,
                "quality_flags": flags,
                "positive_drivers": pos_drivers,
                "negative_drivers": neg_drivers,
                "baseline_source_refs": [d.get("source_id", "") for d in s.get("top_positive_drivers", []) if isinstance(d, dict)],
                "scenario_assumptions_used": param_ids
            }
            all_profiles.append(profile)
            
    return all_profiles

def export_summaries(occ_profiles, skill_profiles):
    print("Exporting summary CSV artifacts...")
    # Occupation summary CSV
    with open(OUT_OCC_SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "masco_code", "occupation_title", "major_group", "scenario_id",
            "baseline_outlook", "scenario_outlook", "reskilling_urgency",
            "effective_ai_pressure", "automation_pressure", "augmentation_opportunity",
            "demand_resilience", "policy_buffer", "transition_pressure",
            "transition_pressure_delta", "sensitivity_classification", "scenario_confidence"
        ])
        for p in occ_profiles:
            writer.writerow([
                p["masco_code"], p["occupation_title"], p["major_group"], p["scenario_id"],
                p["baseline_outlook"], p["scenario_outlook"], p["reskilling_urgency"],
                p["effective_ai_pressure"], p["automation_pressure"], p["augmentation_opportunity"],
                p["demand_resilience"], p["policy_buffer"], p["transition_pressure"],
                p["scenario_delta_from_reference"]["transition_pressure_delta"],
                p["sensitivity_classification"], p["scenario_confidence"]
            ])
            
    # Skill summary CSV
    with open(OUT_SKILL_SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "skill_id", "skill_name", "category", "scenario_id",
            "baseline_outlook", "scenario_outlook", "reskilling_urgency",
            "automation_pressure", "augmentation_opportunity", "demand_resilience",
            "transformation_pressure", "transformation_pressure_delta",
            "sensitivity_classification", "scenario_confidence", "quality_flags"
        ])
        for p in skill_profiles:
            writer.writerow([
                p["skill_id"], p["skill_name"], p["category"], p["scenario_id"],
                p["baseline_outlook"], p["scenario_outlook"], p["reskilling_urgency"],
                p["automation_pressure"], p["augmentation_opportunity"], p["demand_resilience"],
                p["transformation_pressure"], p["scenario_delta_from_reference"]["transformation_pressure_delta"],
                p["sensitivity_classification"], p["scenario_confidence"], ";".join(p["quality_flags"])
            ])

def main():
    print("=" * 70)
    print("BUILDING M6 FUTURE WORKFORCE SCENARIO ENGINE (v1.0.0)")
    print("=" * 70)
    
    verify_m2_freeze_manifest()
    
    occ_data = load_json(OCC_PROFILES_V1_1_1)
    skill_data = load_json(SKILL_PROFILES_V1_1_1)
    scenario_defs = load_json(SCENARIO_DEFS_FILE)
    
    occs = occ_data["profiles"]
    skills = skill_data["profiles"]
    
    occ_scenario_profiles = process_occupations(occs, scenario_defs)
    skill_scenario_profiles = process_skills(skills, scenario_defs)
    
    # Save JSON profiles
    occ_payload = {
        "engine_version": "1.0.0",
        "parent_m2_version": "1.1.1",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_occupations": len(occs),
        "total_scenario_profiles": len(occ_scenario_profiles),
        "scenarios": ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"],
        "profiles": occ_scenario_profiles
    }
    save_json(OUT_OCC_SCENARIO_PROFILES, occ_payload)
    print(f"Saved {len(occ_scenario_profiles)} occupation scenario profiles to {OUT_OCC_SCENARIO_PROFILES}")
    
    skill_payload = {
        "engine_version": "1.0.0",
        "parent_m2_version": "1.1.1",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_skills": len(skills),
        "total_scenario_profiles": len(skill_scenario_profiles),
        "scenarios": ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"],
        "profiles": skill_scenario_profiles
    }
    save_json(OUT_SKILL_SCENARIO_PROFILES, skill_payload)
    print(f"Saved {len(skill_scenario_profiles)} skill scenario profiles to {OUT_SKILL_SCENARIO_PROFILES}")
    
    export_summaries(occ_scenario_profiles, skill_scenario_profiles)
    
    # Generate build manifest
    build_manifest = {
        "engine_version": "1.0.0",
        "parent_m2_version": "1.1.1",
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "governance_rule": "M6 preserves channel separation and uncertainty bounds; zero demographic inputs.",
        "input_artifacts": {
            "m2_freeze_manifest": compute_sha256(M2_FREEZE_MANIFEST_FILE),
            "occupation_trend_profiles_v1_1_1": compute_sha256(OCC_PROFILES_V1_1_1),
            "skill_trend_profiles_v1_1_1": compute_sha256(SKILL_PROFILES_V1_1_1),
            "scenario_definitions_v1": compute_sha256(SCENARIO_DEFS_FILE)
        },
        "output_artifacts": {
            "occupation_scenario_profiles_v1": compute_sha256(OUT_OCC_SCENARIO_PROFILES),
            "skill_scenario_profiles_v1": compute_sha256(OUT_SKILL_SCENARIO_PROFILES),
            "m6_occupation_scenario_summary_csv": compute_sha256(OUT_OCC_SUMMARY_CSV),
            "m6_skill_scenario_summary_csv": compute_sha256(OUT_SKILL_SUMMARY_CSV)
        }
    }
    save_json(OUT_BUILD_MANIFEST, build_manifest)
    print(f"Saved scenario build manifest to {OUT_BUILD_MANIFEST}")
    print("=" * 70)
    print("M6 DETERMINISTIC BUILD COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    main()
