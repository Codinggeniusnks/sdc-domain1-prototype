import json

with open("data/reskilling/learning_resources_v1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for r in data["resources"]:
    print(f"{r['resource_id']}|{r['provider']}|{r['official_url']}|{r['cost_status']}|{r['access_model']}|{r['language']}|{r['learning_level']}")
