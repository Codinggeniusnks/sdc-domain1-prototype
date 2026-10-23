import os
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import json
from src.workforce_gap_engine import WorkforceGapEngine

engine = WorkforceGapEngine()
with open("data/aggregation/synthetic_workforce_v1.json") as f:
    profiles = json.load(f)["profiles"]

res = engine.analyse_workforce_gaps(profiles)
print("Suppressed:", res.get("suppressed"))
print("Eligible count:", res.get("eligible_profile_count"))
print("Priority skills count:", len(res.get("priority_skills", [])))
print("\nTop 5 Priority Skills:")
for item in res.get("priority_skills", [])[:5]:
    print(f"  Rank {item['priority_rank']}: {item['skill_id']} -> Index: {item['priority_index']}")
    print(f"    Components: {item['components']}")
    print(f"    Weighted Contributions: {item['weighted_contributions']}")

print("\nExecutive Summary:")
print(json.dumps(res.get("executive_summary"), indent=2))

print("\nShared Learning Opportunities (Top 3):")
for item in res.get("shared_learning_opportunities", [])[:3]:
    print(f"  Shared: {item['shared_skill']} (Affected: {item['profiles_affected']}) - Session: {item['shared_curriculum_hours_range']}h, Aggregate: {item['aggregate_learner_hours_range']}h")
