import json
import math

with open("data/trends/raw/openalex/openalex_temporal_momentum.json", "r") as f:
    oalex = json.load(f)

srm = oalex.get("skill_research_momentum", {})

print("=== RAW OPENALEX JSON DATA ===")
for sk in ["prompt_engineering", "rag_knowledge_systems", "ai_literacy", "workflow_automation", "sql_data_analysis", "python_scripting"]:
    rec = srm.get(sk, {})
    print(f"Skill: {sk}")
    print(f"  baseline: {rec.get('baseline_count_2020_2023')}")
    print(f"  recent: {rec.get('recent_count_2024_2026')}")
    print(f"  raw growth_rate_ratio in JSON: {rec.get('growth_rate_ratio')}")

print("\n=== CODE IMPLEMENTATION IN build_trend_scores_v1_1.py ===")
# Line 470 in scripts/build_trend_scores_v1_1.py:
# vol_weight = min(1.0, math.log(1.0 + base_count) / math.log(1.0 + 25.0))
# damped_growth = 1.0 + (raw_growth - 1.0) * vol_weight
# research_momentum = round(max(10.0, min(95.0, damped_growth * 38.0)), 1)
for sk in ["prompt_engineering", "rag_knowledge_systems", "ai_literacy", "workflow_automation", "sql_data_analysis", "python_scripting"]:
    rec = srm.get(sk, {})
    base = rec.get('baseline_count_2020_2023', 0)
    raw = rec.get('growth_rate_ratio', 1.0)
    vol_weight = min(1.0, math.log(1.0 + base) / math.log(1.0 + 25.0))
    damped_code = 1.0 + (raw - 1.0) * vol_weight
    res_mom = round(max(10.0, min(95.0, damped_code * 38.0)), 1)
    print(f"{sk}: base={base}, raw={raw:.3f}, vol_weight={vol_weight:.4f}, damped_code={damped_code:.3f}, res_mom={res_mom}")

print("\n=== DOCUMENTED FORMULA IN m2_openalex_low_base_audit.md ===")
# Formula: R_damped = 1.0 + (R_raw - 1.0) * (N_recent / (N_recent + K)) with K = 10.0
for sk in ["prompt_engineering", "rag_knowledge_systems", "ai_literacy", "workflow_automation", "sql_data_analysis", "python_scripting"]:
    rec = srm.get(sk, {})
    recent = rec.get('recent_count_2024_2026', 0)
    base = rec.get('baseline_count_2020_2023', 0)
    raw = rec.get('growth_rate_ratio', 1.0)
    k = 10.0
    factor = recent / (recent + k) if (recent + k) > 0 else 1.0
    damped_doc_formula = 1.0 + (raw - 1.0) * factor
    print(f"{sk}: recent={recent}, raw={raw:.3f}, factor={factor:.4f}, damped_doc_formula={damped_doc_formula:.3f}")
