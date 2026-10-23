import json
from pathlib import Path

p = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/occupation_scenario_profiles_v1_1.json")
with open(p, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"{'Code':<5} | {'Title':<35} | {'Outlook':<18} | {'Conf':<6} | {'SensClass':<15} | {'DownsideStab':<12} | {'CatStab':<8}")
print("-" * 115)

for prof in data["profiles"]:
    if prof["scenario_id"] == "REFERENCE_2026":
        sp = prof.get("sensitivity_profile", {})
        print(f"{prof['masco_code']:<5} | {prof['occupation_title'][:35]:<35} | {prof['scenario_outlook']:<18} | {prof['scenario_confidence']:<6} | {str(prof.get('sensitivity_classification')):<15} | {str(sp.get('downside_risk_stability')):<12} | {str(sp.get('exact_category_stability')):<8}")
