import json
from collections import Counter

with open("data/reskilling/learning_resources_v1.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

resources = catalog["resources"]
print(f"Total resources: {len(resources)}")

# Cost / Access model counts
access_counts = Counter(r.get("access_model") for r in resources)
cost_status_counts = Counter(r.get("cost_status") for r in resources)
print("Access models:", dict(access_counts))
print("Cost statuses:", dict(cost_status_counts))

# Providers
providers = [r["provider"] for r in resources]
print(f"Raw providers count: {len(set(providers))}")

# Check languages
languages = Counter(r.get("language") for r in resources)
print("Languages:", dict(languages))

# Check levels
levels = Counter(r.get("learning_level") for r in resources)
print("Levels:", dict(levels))

# Check alignment
alignments = Counter(r.get("skill_alignment") for r in resources)
print("Alignments:", dict(alignments))

# Check URLs and verification dates
urls = [r["official_url"] for r in resources]
verif_dates = Counter(r.get("last_verified_date") for r in resources)
print("Verification dates:", dict(verif_dates))

print("\nNon-FREE or special resources:")
for r in resources:
    if r.get("access_model") != "FREE" or r.get("cost_status") != "FREE":
        print(f"ID: {r['resource_id']}, Title: {r['title']}, Provider: {r['provider']}, Access: {r.get('access_model')}, CostStatus: {r.get('cost_status')}, Amount: {r.get('cost_amount_if_verified')} {r.get('currency_if_verified')}, CertCost: {r.get('certificate_cost_if_verified')}")

print("\nAll 38 resources summary:")
for i, r in enumerate(resources, 1):
    print(f"{i:02d}. [{r['resource_id']}] {r['provider']} - {r['title']} ({r.get('access_model')}, {r.get('cost_status')}, {r.get('learning_level')}) -> Skills: {r.get('skill_ids')}")
