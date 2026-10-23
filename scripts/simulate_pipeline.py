import json
import math

with open("data/trends/processed/skill_trend_profiles_v1_1.json") as f:
    v11 = json.load(f)

for p in v11.get("profiles", []):
    sk_id = p["skill_id"]
    old_res = p["research_momentum_index"]
    old_outlook = p["overall_outlook"]
    old_conf = p["confidence_label"]
    
    # Calculate new research momentum
    # Need r_adj
    # Let's inspect what changes if research_momentum changes
    print(f"{sk_id:25s}: old_res={old_res}, old_outlook={old_outlook}, old_conf={old_conf}")
