import json

with open("data/trends/processed/skill_trend_profiles_v1_1.json", "r", encoding="utf-8") as f:
    sk_data = json.load(f)

profiles = sk_data.get("profiles", [])

print("=== CHECK 2: SKILL CONFIDENCE AUDIT ===")
tiers = {}
for p in profiles:
    lbl = p.get("confidence_label")
    tiers[lbl] = tiers.get(lbl, 0) + 1

print(f"Confidence tiers count: {tiers}")

target_skills = [
    "ai_literacy",
    "data_privacy_pdpa",
    "instructional_design",
    "prompt_engineering",
    "rag_knowledge_systems"
]

print("\n--- Detailed Representative Skills ---")
for p in profiles:
    if p["skill_id"] in target_skills:
        print(f"\nSkill ID: {p['skill_id']} ({p['skill_name']})")
        print(f"  Confidence Score: {p['confidence_index']}")
        print(f"  Confidence Label: {p['confidence_label']}")
        print(f"  Source Count: {p['source_count']}")
        print(f"  Independent Families: {p['independent_evidence_families']}")
        print(f"  Quality Flags: {p['quality_flags']}")
        # Check if ILO or DOSM are in independent_evidence_families
        fams = p['independent_evidence_families']
        has_ilo = "ILO_GENAI_STUDY" in fams
        has_dosm = "DOSM_WAGES" in fams
        print(f"  Contains ILO_GENAI_STUDY? {has_ilo}")
        print(f"  Contains DOSM_WAGES? {has_dosm}")

# Check publisher independence
print("\n--- Publisher Independence in Families ---")
for p in profiles:
    fams = p['independent_evidence_families']
    has_mycol = "TALENTCORP_MYCOL" in fams
    has_impact = "TALENTCORP_IMPACT_STUDY" in fams
    if has_mycol and has_impact:
        print(f"{p['skill_id']}: has BOTH MyCOL and Impact Study (TalentCorp). Listed families count: {len(fams)}")
