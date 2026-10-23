import json

with open("data/trends/processed/skill_trend_profiles_v1_1.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for p in d["profiles"]:
    print(f"{p['skill_id']:<30} | {p['confidence_label']:<8} | Score: {p['confidence_index']:<5} | Fams: {p['independent_evidence_families']}")
