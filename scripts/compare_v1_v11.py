import json

with open("data/trends/processed/skill_trend_profiles_v1.json", "r", encoding="utf-8") as f:
    v1_sk = {p["skill_id"]: p for p in json.load(f)["profiles"]}
with open("data/trends/processed/skill_trend_profiles_v1_1.json", "r", encoding="utf-8") as f:
    v11_sk = {p["skill_id"]: p for p in json.load(f)["profiles"]}

print("=== SKILL COMPARISON (v1 vs v1.1) ===")
for sid in v1_sk:
    p1 = v1_sk[sid]
    p11 = v11_sk[sid]
    out_chg = f"{p1['overall_outlook']} -> {p11['overall_outlook']}" if p1["overall_outlook"] != p11["overall_outlook"] else f"SAME ({p1['overall_outlook']})"
    conf_chg = f"{p1['confidence_label']} ({p1['confidence_index']}) -> {p11['confidence_label']} ({p11['confidence_index']})"
    print(f"{sid:<30} | Outlook: {out_chg:<30} | Conf: {conf_chg}")

with open("data/trends/processed/occupation_trend_profiles_v1.json", "r", encoding="utf-8") as f:
    v1_occ = {p["occupation_code"]: p for p in json.load(f)["profiles"]}
with open("data/trends/processed/occupation_trend_profiles_v1_1.json", "r", encoding="utf-8") as f:
    v11_occ = {p["occupation_code"]: p for p in json.load(f)["profiles"]}

print("\n=== OCCUPATION COMPARISON (v1 vs v1.1) ===")
for oid in v1_occ:
    if oid.startswith("MAJOR_"):
        continue
    p1 = v1_occ[oid]
    p11 = v11_occ[oid]
    out_chg = f"{p1['overall_outlook']} -> {p11['overall_outlook']}" if p1["overall_outlook"] != p11["overall_outlook"] else f"SAME ({p1['overall_outlook']})"
    conf_chg = f"{p1['confidence_label']} ({p1['confidence_index']}) -> {p11['confidence_label']} ({p11['confidence_index']})"
    exp_chg = f"AI Exp: {p1['ai_exposure']} -> {p11['ai_exposure']} (Auto: {p1['automation_exposure']}->{p11['automation_exposure']}, Aug: {p1['augmentation_potential']}->{p11['augmentation_potential']})"
    print(f"{oid:<6} {p1['occupation_title'][:25]:<25} | Out: {out_chg:<25} | {exp_chg}")
