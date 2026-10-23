import json
from pathlib import Path
from collections import Counter
import scipy.stats as stats

base_dir = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
scenarios_dir = base_dir / "data" / "scenarios"

with open(scenarios_dir / "occupation_scenario_profiles_v1_1.json", "r", encoding="utf-8") as f:
    occ_data = json.load(f)["profiles"]

with open(scenarios_dir / "skill_scenario_profiles_v1_1.json", "r", encoding="utf-8") as f:
    skill_data = json.load(f)["profiles"]

print("=== 1. SCENARIO OUTLOOK DISTRIBUTIONS ===")
for sc in ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]:
    four_d = [p["scenario_outlook"] for p in occ_data if p["scenario_id"] == sc and p["entity_granularity"] == "FOUR_DIGIT_OCCUPATION"]
    major = [p["scenario_outlook"] for p in occ_data if p["scenario_id"] == sc and p["entity_granularity"] == "ONE_DIGIT_MAJOR_GROUP_FALLBACK"]
    sk = [p["scenario_outlook"] for p in skill_data if p["scenario_id"] == sc]
    print(f"\nScenario: {sc}")
    print(f"  4-Digit Occupations (N=20): {dict(Counter(four_d))}")
    print(f"  Major-Group Fallbacks (N=8): {dict(Counter(major))}")
    print(f"  Skills (N=16): {dict(Counter(sk))}")

print("\n=== 2. RESKILLING URGENCY DISTRIBUTIONS ===")
for sc in ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]:
    four_d_urg = [p["reskilling_urgency"] for p in occ_data if p["scenario_id"] == sc and p["entity_granularity"] == "FOUR_DIGIT_OCCUPATION"]
    major_urg = [p["reskilling_urgency"] for p in occ_data if p["scenario_id"] == sc and p["entity_granularity"] == "ONE_DIGIT_MAJOR_GROUP_FALLBACK"]
    sk_urg = [p["reskilling_urgency"] for p in skill_data if p["scenario_id"] == sc]
    print(f"\nScenario: {sc}")
    print(f"  4-Digit Occupations: {dict(Counter(four_d_urg))}")
    print(f"  Major-Group Fallbacks: {dict(Counter(major_urg))}")
    print(f"  Combined Occupations: {dict(Counter([p['reskilling_urgency'] for p in occ_data if p['scenario_id'] == sc]))}")
    print(f"  Skills: {dict(Counter(sk_urg))}")

print("\n=== 3. VERY HIGH URGENCY OCCUPATIONS UNDER FAST_AGENTIC ===")
very_high_fast = [f"{p['masco_code']} - {p['occupation_title']}" for p in occ_data if p["scenario_id"] == "FAST_AGENTIC" and p["reskilling_urgency"] == "VERY HIGH"]
print(f"Count: {len(very_high_fast)}")
for v in very_high_fast:
    print(f"  {v}")

print("\n=== 4. SENSITIVITY SEMANTICS (ACROSS UNCERTAINTY BOUNDS) ===")
for sc in ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]:
    sc_occs = [p for p in occ_data if p["scenario_id"] == sc]
    exact_stable = sum(1 for p in sc_occs if p["sensitivity_profile"]["exact_category_stability"] == "STABLE")
    downside_robust = sum(1 for p in sc_occs if p["sensitivity_profile"]["downside_risk_stability"] == "ROBUST")
    trans_high = sum(1 for p in sc_occs if p["sensitivity_profile"]["transformation_sensitivity"] == "HIGH")
    movements = Counter(p["sensitivity_profile"]["movement_type"] for p in sc_occs)
    print(f"\nScenario {sc} (N=28):")
    print(f"  Exact category stable: {exact_stable} / 28")
    print(f"  Downside risk robust: {downside_robust} / 28")
    print(f"  Transformation sensitivity high: {trans_high} / 28")
    print(f"  Movement types: {dict(movements)}")

print("\n=== 5. SPEARMAN RANK CORRELATIONS ===")
# Separate 4-digit occupations vs Major Group fallbacks
four_digit_codes = sorted(list({p["masco_code"] for p in occ_data if p["entity_granularity"] == "FOUR_DIGIT_OCCUPATION"}))
major_codes = sorted(list({p["masco_code"] for p in occ_data if p["entity_granularity"] == "ONE_DIGIT_MAJOR_GROUP_FALLBACK"}))
skill_ids = sorted(list({p["skill_id"] for p in skill_data}))

def get_ranks(metric, codes, dataset, id_key):
    by_sc = {"REFERENCE_2026": [], "MODERATE_COPILOT": [], "FAST_AGENTIC": []}
    for c in codes:
        p_ref = next(p for p in dataset if p[id_key] == c and p["scenario_id"] == "REFERENCE_2026")
        p_cop = next(p for p in dataset if p[id_key] == c and p["scenario_id"] == "MODERATE_COPILOT")
        p_age = next(p for p in dataset if p[id_key] == c and p["scenario_id"] == "FAST_AGENTIC")
        by_sc["REFERENCE_2026"].append(p_ref[metric])
        by_sc["MODERATE_COPILOT"].append(p_cop[metric])
        by_sc["FAST_AGENTIC"].append(p_age[metric])
    
    r_cop, _ = stats.spearmanr(by_sc["REFERENCE_2026"], by_sc["MODERATE_COPILOT"])
    r_age, _ = stats.spearmanr(by_sc["REFERENCE_2026"], by_sc["FAST_AGENTIC"])
    r_cop_age, _ = stats.spearmanr(by_sc["MODERATE_COPILOT"], by_sc["FAST_AGENTIC"])
    return r_cop, r_age, r_cop_age

print("4-Digit Occupations (N=20):")
for m in ["transition_pressure", "demand_resilience", "automation_pressure"]:
    rc, ra, rca = get_ranks(m, four_digit_codes, occ_data, "masco_code")
    print(f"  {m:<22}: Ref vs Cop = {rc:.4f}, Ref vs Fast = {ra:.4f}, Cop vs Fast = {rca:.4f}")

# Net resilience for occupations: demand_res + 0.3*aug - 0.7*auto
def get_net_res_ranks(codes, dataset, id_key, aug_w, auto_w):
    by_sc = {"REFERENCE_2026": [], "MODERATE_COPILOT": [], "FAST_AGENTIC": []}
    for c in codes:
        for sc in ["REFERENCE_2026", "MODERATE_COPILOT", "FAST_AGENTIC"]:
            p = next(x for x in dataset if x[id_key] == c and x["scenario_id"] == sc)
            net_r = p["demand_resilience"] + aug_w * p["augmentation_opportunity"] - auto_w * p["automation_pressure"]
            by_sc[sc].append(net_r)
    rc, _ = stats.spearmanr(by_sc["REFERENCE_2026"], by_sc["MODERATE_COPILOT"])
    ra, _ = stats.spearmanr(by_sc["REFERENCE_2026"], by_sc["FAST_AGENTIC"])
    rca, _ = stats.spearmanr(by_sc["MODERATE_COPILOT"], by_sc["FAST_AGENTIC"])
    return rc, ra, rca

rc, ra, rca = get_net_res_ranks(four_digit_codes, occ_data, "masco_code", 0.30, 0.70)
print(f"  {'net_resilience':<22}: Ref vs Cop = {rc:.4f}, Ref vs Fast = {ra:.4f}, Cop vs Fast = {rca:.4f}")

print("\nSkills (N=16):")
for m in ["transformation_pressure", "demand_resilience", "automation_pressure"]:
    rc, ra, rca = get_ranks(m, skill_ids, skill_data, "skill_id")
    print(f"  {m:<24}: Ref vs Cop = {rc:.4f}, Ref vs Fast = {ra:.4f}, Cop vs Fast = {rca:.4f}")
rc, ra, rca = get_net_res_ranks(skill_ids, skill_data, "skill_id", 0.40, 0.60)
print(f"  {'net_resilience':<24}: Ref vs Cop = {rc:.4f}, Ref vs Fast = {ra:.4f}, Cop vs Fast = {rca:.4f}")

print("\n=== 6. ZERO-BASE RESEARCH SKILLS ===")
zero_base = [p["skill_id"] for p in skill_data if p["scenario_id"] == "REFERENCE_2026" and "INSUFFICIENT_HISTORICAL_BASELINE" in p["quality_flags"]]
print(f"Count: {len(zero_base)}")
print(f"IDs: {zero_base}")
