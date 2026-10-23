import json
import math

with open("data/trends/raw/openalex/openalex_temporal_momentum.json") as f:
    d = json.load(f)
srm = d.get('skill_research_momentum', {})

skills = [
    ("prompt_engineering", 1, 18, 17.143),
    ("rag_knowledge_systems", 1, 30, 28.571),
    ("ai_literacy", 14, 121, 11.204),
    ("instructional_design", 15, 97, 8.398),
    ("ai_ethics_governance", 8, 79, 12.54),
    ("workflow_automation", 2, 33, 18.333),
    ("data_privacy_pdpa", 3, 25, 9.80),
    ("stakeholder_communication", 11, 57, 6.67),
    ("python_scripting", 5, 22, 5.432),
    ("sql_data_analysis", 5, 18, 4.444),
    ("human_in_the_loop_qa", 0, 15, 50.0),
    ("data_visualization", 0, 6, 20.0),
]

print(f"{'Skill':25s} | {'Base':4s} | {'Rec':4s} | {'Raw':6s} | {'w_vol':5s} | {'R_adj':6s}")
for sk, base, rec, raw in skills:
    w_vol = min(1.0, math.log(1.0 + base) / math.log(26.0))
    r_adj = 1.0 + (raw - 1.0) * w_vol
    print(f"{sk:25s} | {base:4d} | {rec:4d} | {raw:6.2f} | {w_vol:5.3f} | {r_adj:6.2f}")

print("\n--- Candidate Mappings ---")
# Candidate 1: Log-scaled growth from baseline 50
# score = 50.0 + 35.0 * (1 - exp(-(R_adj - 1.0) / tau)) with tau = 3.5 -> bounded [50, 85]
# Or tau = 4.0, max = 92.0:
# score = 50.0 + (92.0 - 50.0) * (1 - math.exp(-(r_adj - 1.0) / 4.0))

# Candidate 2: Continuous smooth transform:
# Base 45.0 for r_adj=1.0. As r_adj increases, asymptotically approaches 94.0.
# score = 45.0 + 48.0 * (1.0 - math.exp(-(r_adj - 1.0) / 3.5))

# Candidate 3: Power / Logarithmic scaling:
# score = 50.0 + 20.0 * math.log2(r_adj) capped at 94.0 (r_adj=1 -> 50, r_adj=2 -> 70, r_adj=4.4 -> 82, r_adj=9.5 -> 94)

for cand_name, func in [
    ("Candidate A (Asymptotic tau=3.5, base=45, max=92)", lambda r: 45.0 + 47.0 * (1.0 - math.exp(-(r - 1.0) / 3.5))),
    ("Candidate B (Asymptotic tau=4.0, base=50, max=94)", lambda r: 50.0 + 44.0 * (1.0 - math.exp(-(r - 1.0) / 4.0))),
    ("Candidate C (Log2 base=50, scale=14.0, max=94)", lambda r: min(94.0, 50.0 + 14.0 * math.log2(r) if r >= 1.0 else 50.0)),
    ("Candidate D (Linear ramp + soft bound above 75)", lambda r: 45.0 + (r - 1.0) * 8.0 if 45.0 + (r-1)*8.0 <= 75 else 75.0 + 19.0 * math.tanh((45.0 + (r-1)*8.0 - 75.0) / 15.0)),
]:
    print(f"\n{cand_name}:")
    for sk, base, rec, raw in skills:
        w_vol = min(1.0, math.log(1.0 + base) / math.log(26.0))
        r_adj = 1.0 + (raw - 1.0) * w_vol
        sc = round(func(r_adj), 1)
        print(f"  {sk:25s}: r_adj={r_adj:5.2f} -> score = {sc:4.1f}")
