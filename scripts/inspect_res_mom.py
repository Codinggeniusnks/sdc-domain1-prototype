import json

with open("data/trends/processed/skill_trend_profiles_v1_1.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for p in d.get("profiles", []):
    print(f"{p['skill_id']:30s}: research_momentum_index = {p.get('research_momentum_index')}")
