"""
build_synthetic_workforce.py

Generates a deterministic, privacy-safe synthetic workforce dataset (50 profiles)
for O6 SDG Contribution Aggregation Engine v1.0.0.

Adheres to:
1. Zero demographic attributes (no age, gender, race, religion, income, location).
2. Purely technical and occupational attributes (current role, current skills, target role, pathway skills).
3. 4 neutral synthetic cohorts: DIGITAL_SERVICES, ADVANCED_MANUFACTURING, GREEN_TRANSITION, BUSINESS_SERVICES.
4. 3 neutral synthetic demo regions: REGION_A, REGION_B, REGION_C.
5. Realistic distribution across 20 MASCO 4-digit occupations and 16 canonical M5 skills.
6. Deterministic generation with fixed seed.
"""

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "data" / "aggregation" / "synthetic_workforce_v1.json"

# Canonical Skills (16)
CANONICAL_SKILLS = [
    "ai_literacy", "prompt_engineering", "process_mapping", "sql_data_analysis",
    "python_scripting", "data_visualization", "workflow_automation", "human_in_the_loop_qa",
    "rag_knowledge_systems", "api_integration", "ai_ethics_governance", "data_privacy_pdpa",
    "esg_sustainability_reporting", "carbon_footprint_analytics", "stakeholder_communication",
    "instructional_design"
]

# Canonical Roles (20)
ROLE_TITLES = {
    "2512": "Software Developers",
    "2511": "Systems Analysts",
    "2521": "Database Designers and Administrators",
    "2529": "Database and Network Professionals NEC (AI & Data Science Specialists)",
    "2519": "Software and Applications Developers NEC (Cloud & Integration Specialists)",
    "2522": "Systems Administrators and Cloud Infrastructure Specialists",
    "2411": "Accountants and Auditors",
    "2421": "Management and Organization Analysts (Transformation Consultants)",
    "2422": "Policy and Corporate Planning Professionals (Governance Specialists)",
    "2151": "Electrical Engineers",
    "2152": "Electronic Engineers (Semiconductor / Microelectronics Specialists)",
    "2143": "Environmental Engineers",
    "2424": "Training and Staff Development Professionals (Reskilling Specialists)",
    "2166": "Graphic and Multimedia Designers (UI/UX Designers)",
    "1330": "Information and Communications Technology Services Managers",
    "3514": "Web Technicians and Cloud Operators",
    "3322": "Commercial Sales Representatives",
    "4311": "Accounting and Bookkeeping Clerks",
    "4110": "General Office Clerks",
    "3343": "Administrative and Executive Secretaries"
}

# 50 Detailed Profile Templates
PROFILE_SPECS = [
    # -------------------------------------------------------------
    # COHORT 1: DIGITAL_SERVICES (16 Profiles)
    # Focus: Software, Data, AI, Cloud, Product
    # -------------------------------------------------------------
    {"id": "SYN_PROF_001", "cohort": "DIGITAL_SERVICES", "region": "REGION_A", "cur_role": "2512", "cur_skills": ["python_scripting", "api_integration", "sql_data_analysis"], "target_role": "2529", "pathway": ["rag_knowledge_systems", "prompt_engineering", "ai_ethics_governance"], "core_gaps": ["rag_knowledge_systems", "ai_ethics_governance"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_002", "cohort": "DIGITAL_SERVICES", "region": "REGION_A", "cur_role": "3514", "cur_skills": ["api_integration", "workflow_automation"], "target_role": "2512", "pathway": ["python_scripting", "sql_data_analysis", "prompt_engineering"], "core_gaps": ["python_scripting", "sql_data_analysis"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_003", "cohort": "DIGITAL_SERVICES", "region": "REGION_B", "cur_role": "2521", "cur_skills": ["sql_data_analysis", "data_visualization"], "target_role": "2529", "pathway": ["python_scripting", "rag_knowledge_systems", "data_privacy_pdpa"], "core_gaps": ["rag_knowledge_systems"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_004", "cohort": "DIGITAL_SERVICES", "region": "REGION_A", "cur_role": "2511", "cur_skills": ["process_mapping", "sql_data_analysis", "stakeholder_communication"], "target_role": "2529", "pathway": ["ai_literacy", "prompt_engineering", "ai_ethics_governance"], "core_gaps": ["ai_ethics_governance", "prompt_engineering"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_005", "cohort": "DIGITAL_SERVICES", "region": "REGION_C", "cur_role": "2166", "cur_skills": ["stakeholder_communication", "ai_literacy"], "target_role": "2512", "pathway": ["prompt_engineering", "workflow_automation", "human_in_the_loop_qa"], "core_gaps": ["workflow_automation"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_006", "cohort": "DIGITAL_SERVICES", "region": "REGION_A", "cur_role": "2522", "cur_skills": ["workflow_automation", "api_integration"], "target_role": "2519", "pathway": ["python_scripting", "data_privacy_pdpa", "human_in_the_loop_qa"], "core_gaps": ["data_privacy_pdpa"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_007", "cohort": "DIGITAL_SERVICES", "region": "REGION_B", "cur_role": "1330", "cur_skills": ["stakeholder_communication", "process_mapping", "ai_literacy"], "target_role": "1330", "pathway": ["ai_ethics_governance", "data_privacy_pdpa", "esg_sustainability_reporting"], "core_gaps": ["ai_ethics_governance", "esg_sustainability_reporting"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_008", "cohort": "DIGITAL_SERVICES", "region": "REGION_A", "cur_role": "2519", "cur_skills": ["python_scripting", "api_integration"], "target_role": "2519", "pathway": ["workflow_automation", "rag_knowledge_systems", "prompt_engineering"], "core_gaps": ["rag_knowledge_systems"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_009", "cohort": "DIGITAL_SERVICES", "region": "REGION_B", "cur_role": "2512", "cur_skills": ["python_scripting", "sql_data_analysis"], "target_role": "2512", "pathway": ["human_in_the_loop_qa", "prompt_engineering", "ai_ethics_governance"], "core_gaps": ["human_in_the_loop_qa"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_010", "cohort": "DIGITAL_SERVICES", "region": "REGION_C", "cur_role": "3514", "cur_skills": ["workflow_automation", "process_mapping"], "target_role": "2522", "pathway": ["api_integration", "python_scripting", "data_privacy_pdpa"], "core_gaps": ["api_integration"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_011", "cohort": "DIGITAL_SERVICES", "region": "REGION_A", "cur_role": "2529", "cur_skills": ["python_scripting", "sql_data_analysis", "rag_knowledge_systems"], "target_role": "2529", "pathway": ["ai_ethics_governance", "data_privacy_pdpa", "carbon_footprint_analytics"], "core_gaps": ["carbon_footprint_analytics"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_012", "cohort": "DIGITAL_SERVICES", "region": "REGION_B", "cur_role": "2166", "cur_skills": ["ai_literacy", "stakeholder_communication"], "target_role": "2166", "pathway": ["prompt_engineering", "human_in_the_loop_qa", "instructional_design"], "core_gaps": ["prompt_engineering"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_013", "cohort": "DIGITAL_SERVICES", "region": "REGION_A", "cur_role": "2511", "cur_skills": ["sql_data_analysis", "process_mapping"], "target_role": "2421", "pathway": ["ai_literacy", "data_visualization", "esg_sustainability_reporting"], "core_gaps": ["esg_sustainability_reporting"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_014", "cohort": "DIGITAL_SERVICES", "region": "REGION_C", "cur_role": "2512", "cur_skills": ["python_scripting", "api_integration"], "target_role": "2529", "pathway": ["prompt_engineering", "rag_knowledge_systems", "human_in_the_loop_qa"], "core_gaps": ["rag_knowledge_systems"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_015", "cohort": "DIGITAL_SERVICES", "region": "REGION_B", "cur_role": "2521", "cur_skills": ["sql_data_analysis", "data_visualization"], "target_role": "2521", "pathway": ["data_privacy_pdpa", "workflow_automation"], "core_gaps": ["data_privacy_pdpa"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_016", "cohort": "DIGITAL_SERVICES", "region": "REGION_A", "cur_role": "3514", "cur_skills": ["process_mapping"], "target_role": "2519", "pathway": ["python_scripting", "api_integration", "workflow_automation"], "core_gaps": ["python_scripting", "api_integration"], "scenario": "REFERENCE_2026"},

    # -------------------------------------------------------------
    # COHORT 2: ADVANCED_MANUFACTURING (14 Profiles)
    # Focus: Engineering, Automation, Systems, Electronics
    # -------------------------------------------------------------
    {"id": "SYN_PROF_017", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_B", "cur_role": "2151", "cur_skills": ["process_mapping", "workflow_automation"], "target_role": "2151", "pathway": ["carbon_footprint_analytics", "python_scripting", "data_visualization"], "core_gaps": ["carbon_footprint_analytics"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_018", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_B", "cur_role": "2152", "cur_skills": ["python_scripting", "process_mapping"], "target_role": "2152", "pathway": ["workflow_automation", "prompt_engineering", "ai_literacy"], "core_gaps": ["workflow_automation"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_019", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_A", "cur_role": "2511", "cur_skills": ["sql_data_analysis", "process_mapping"], "target_role": "2421", "pathway": ["workflow_automation", "data_visualization", "esg_sustainability_reporting"], "core_gaps": ["esg_sustainability_reporting"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_020", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_B", "cur_role": "2151", "cur_skills": ["process_mapping", "stakeholder_communication"], "target_role": "2151", "pathway": ["python_scripting", "workflow_automation", "carbon_footprint_analytics"], "core_gaps": ["carbon_footprint_analytics"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_021", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_C", "cur_role": "3514", "cur_skills": ["workflow_automation"], "target_role": "2522", "pathway": ["python_scripting", "api_integration", "data_privacy_pdpa"], "core_gaps": ["python_scripting", "data_privacy_pdpa"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_022", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_B", "cur_role": "2152", "cur_skills": ["python_scripting", "api_integration"], "target_role": "2152", "pathway": ["prompt_engineering", "human_in_the_loop_qa", "rag_knowledge_systems"], "core_gaps": ["human_in_the_loop_qa"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_023", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_A", "cur_role": "2424", "cur_skills": ["instructional_design", "stakeholder_communication"], "target_role": "2424", "pathway": ["ai_literacy", "prompt_engineering", "human_in_the_loop_qa"], "core_gaps": ["ai_literacy", "prompt_engineering"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_024", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_B", "cur_role": "2151", "cur_skills": ["process_mapping"], "target_role": "2143", "pathway": ["carbon_footprint_analytics", "esg_sustainability_reporting", "data_visualization"], "core_gaps": ["carbon_footprint_analytics", "esg_sustainability_reporting"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_025", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_C", "cur_role": "2512", "cur_skills": ["python_scripting", "sql_data_analysis"], "target_role": "2519", "pathway": ["workflow_automation", "api_integration", "prompt_engineering"], "core_gaps": ["workflow_automation"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_026", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_B", "cur_role": "2152", "cur_skills": ["process_mapping", "workflow_automation"], "target_role": "2152", "pathway": ["python_scripting", "sql_data_analysis", "data_visualization"], "core_gaps": ["python_scripting"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_027", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_A", "cur_role": "1330", "cur_skills": ["stakeholder_communication", "process_mapping"], "target_role": "1330", "pathway": ["ai_ethics_governance", "workflow_automation", "esg_sustainability_reporting"], "core_gaps": ["esg_sustainability_reporting"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_028", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_B", "cur_role": "2522", "cur_skills": ["workflow_automation", "api_integration"], "target_role": "2522", "pathway": ["data_privacy_pdpa", "prompt_engineering"], "core_gaps": ["data_privacy_pdpa"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_029", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_C", "cur_role": "3514", "cur_skills": ["process_mapping"], "target_role": "2512", "pathway": ["python_scripting", "sql_data_analysis", "api_integration"], "core_gaps": ["python_scripting", "sql_data_analysis"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_030", "cohort": "ADVANCED_MANUFACTURING", "region": "REGION_B", "cur_role": "2151", "cur_skills": ["process_mapping", "workflow_automation"], "target_role": "2151", "pathway": ["carbon_footprint_analytics", "esg_sustainability_reporting"], "core_gaps": ["carbon_footprint_analytics"], "scenario": "MODERATE_COPILOT"},

    # -------------------------------------------------------------
    # COHORT 3: GREEN_TRANSITION (12 Profiles)
    # Focus: Environmental, ESG, Sustainability, Policy
    # -------------------------------------------------------------
    {"id": "SYN_PROF_031", "cohort": "GREEN_TRANSITION", "region": "REGION_C", "cur_role": "2143", "cur_skills": ["carbon_footprint_analytics", "esg_sustainability_reporting", "data_visualization"], "target_role": "2143", "pathway": ["python_scripting", "sql_data_analysis", "workflow_automation"], "core_gaps": ["python_scripting", "sql_data_analysis"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_032", "cohort": "GREEN_TRANSITION", "region": "REGION_C", "cur_role": "2422", "cur_skills": ["stakeholder_communication", "process_mapping", "data_privacy_pdpa"], "target_role": "2422", "pathway": ["esg_sustainability_reporting", "ai_ethics_governance", "carbon_footprint_analytics"], "core_gaps": ["esg_sustainability_reporting", "carbon_footprint_analytics"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_033", "cohort": "GREEN_TRANSITION", "region": "REGION_A", "cur_role": "2411", "cur_skills": ["sql_data_analysis", "process_mapping"], "target_role": "2411", "pathway": ["esg_sustainability_reporting", "carbon_footprint_analytics", "data_visualization"], "core_gaps": ["esg_sustainability_reporting", "carbon_footprint_analytics"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_034", "cohort": "GREEN_TRANSITION", "region": "REGION_C", "cur_role": "2143", "cur_skills": ["carbon_footprint_analytics", "process_mapping"], "target_role": "2143", "pathway": ["esg_sustainability_reporting", "rag_knowledge_systems", "prompt_engineering"], "core_gaps": ["esg_sustainability_reporting"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_035", "cohort": "GREEN_TRANSITION", "region": "REGION_B", "cur_role": "2151", "cur_skills": ["process_mapping", "python_scripting"], "target_role": "2143", "pathway": ["carbon_footprint_analytics", "esg_sustainability_reporting", "sql_data_analysis"], "core_gaps": ["carbon_footprint_analytics", "esg_sustainability_reporting"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_036", "cohort": "GREEN_TRANSITION", "region": "REGION_C", "cur_role": "2421", "cur_skills": ["process_mapping", "stakeholder_communication", "data_visualization"], "target_role": "2421", "pathway": ["esg_sustainability_reporting", "carbon_footprint_analytics", "workflow_automation"], "core_gaps": ["esg_sustainability_reporting"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_037", "cohort": "GREEN_TRANSITION", "region": "REGION_A", "cur_role": "2424", "cur_skills": ["instructional_design", "stakeholder_communication"], "target_role": "2424", "pathway": ["esg_sustainability_reporting", "ai_literacy", "prompt_engineering"], "core_gaps": ["esg_sustainability_reporting"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_038", "cohort": "GREEN_TRANSITION", "region": "REGION_C", "cur_role": "2143", "cur_skills": ["carbon_footprint_analytics", "esg_sustainability_reporting"], "target_role": "2143", "pathway": ["workflow_automation", "api_integration", "python_scripting"], "core_gaps": ["workflow_automation"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_039", "cohort": "GREEN_TRANSITION", "region": "REGION_B", "cur_role": "2422", "cur_skills": ["stakeholder_communication", "ai_ethics_governance"], "target_role": "2422", "pathway": ["esg_sustainability_reporting", "data_privacy_pdpa", "carbon_footprint_analytics"], "core_gaps": ["esg_sustainability_reporting", "carbon_footprint_analytics"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_040", "cohort": "GREEN_TRANSITION", "region": "REGION_C", "cur_role": "2411", "cur_skills": ["sql_data_analysis", "data_visualization"], "target_role": "2411", "pathway": ["esg_sustainability_reporting", "carbon_footprint_analytics"], "core_gaps": ["esg_sustainability_reporting"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_041", "cohort": "GREEN_TRANSITION", "region": "REGION_A", "cur_role": "2151", "cur_skills": ["process_mapping", "workflow_automation"], "target_role": "2151", "pathway": ["carbon_footprint_analytics", "data_visualization"], "core_gaps": ["carbon_footprint_analytics"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_042", "cohort": "GREEN_TRANSITION", "region": "REGION_C", "cur_role": "2143", "cur_skills": ["carbon_footprint_analytics"], "target_role": "2143", "pathway": ["esg_sustainability_reporting", "sql_data_analysis", "python_scripting"], "core_gaps": ["esg_sustainability_reporting", "sql_data_analysis"], "scenario": "FAST_AGENTIC"},

    # -------------------------------------------------------------
    # COHORT 4: BUSINESS_SERVICES (8 Profiles)
    # Focus: Clerical, Finance, Administration, Operations
    # -------------------------------------------------------------
    {"id": "SYN_PROF_043", "cohort": "BUSINESS_SERVICES", "region": "REGION_A", "cur_role": "4110", "cur_skills": ["stakeholder_communication"], "target_role": "3343", "pathway": ["workflow_automation", "process_mapping", "ai_literacy"], "core_gaps": ["workflow_automation", "process_mapping"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_044", "cohort": "BUSINESS_SERVICES", "region": "REGION_A", "cur_role": "4311", "cur_skills": ["sql_data_analysis"], "target_role": "2411", "pathway": ["python_scripting", "workflow_automation", "data_visualization"], "core_gaps": ["python_scripting", "data_visualization"], "scenario": "FAST_AGENTIC"},
    {"id": "SYN_PROF_045", "cohort": "BUSINESS_SERVICES", "region": "REGION_B", "cur_role": "3343", "cur_skills": ["stakeholder_communication", "process_mapping"], "target_role": "2421", "pathway": ["ai_literacy", "prompt_engineering", "workflow_automation"], "core_gaps": ["ai_literacy", "workflow_automation"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_046", "cohort": "BUSINESS_SERVICES", "region": "REGION_A", "cur_role": "3322", "cur_skills": ["stakeholder_communication"], "target_role": "3322", "pathway": ["ai_literacy", "prompt_engineering", "data_visualization"], "core_gaps": ["ai_literacy", "prompt_engineering"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_047", "cohort": "BUSINESS_SERVICES", "region": "REGION_C", "cur_role": "4110", "cur_skills": ["stakeholder_communication"], "target_role": "4110", "pathway": ["prompt_engineering", "ai_literacy", "workflow_automation"], "core_gaps": ["ai_literacy", "prompt_engineering"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_048", "cohort": "BUSINESS_SERVICES", "region": "REGION_A", "cur_role": "4311", "cur_skills": ["sql_data_analysis", "process_mapping"], "target_role": "4311", "pathway": ["workflow_automation", "data_privacy_pdpa", "prompt_engineering"], "core_gaps": ["workflow_automation"], "scenario": "REFERENCE_2026"},
    {"id": "SYN_PROF_049", "cohort": "BUSINESS_SERVICES", "region": "REGION_B", "cur_role": "3343", "cur_skills": ["stakeholder_communication"], "target_role": "3343", "pathway": ["prompt_engineering", "workflow_automation", "data_privacy_pdpa"], "core_gaps": ["workflow_automation", "data_privacy_pdpa"], "scenario": "MODERATE_COPILOT"},
    {"id": "SYN_PROF_050", "cohort": "BUSINESS_SERVICES", "region": "REGION_A", "cur_role": "3322", "cur_skills": ["stakeholder_communication", "data_visualization"], "target_role": "2421", "pathway": ["process_mapping", "workflow_automation", "prompt_engineering"], "core_gaps": ["process_mapping", "workflow_automation"], "scenario": "FAST_AGENTIC"}
]


def build_workforce():
    profiles = []
    cohort_counts = {}
    region_counts = {}

    for spec in PROFILE_SPECS:
        pid = spec["id"]
        cid = spec["cohort"]
        rid = spec["region"]
        cur_r = spec["cur_role"]
        tgt_r = spec["target_role"]

        cohort_counts[cid] = cohort_counts.get(cid, 0) + 1
        region_counts[rid] = region_counts.get(rid, 0) + 1

        rec = {
            "profile_id": pid,
            "cohort_id": cid,
            "region_id": rid,
            "current_role": {
                "masco_code": cur_r,
                "role_title": ROLE_TITLES.get(cur_r, "Unknown Role")
            },
            "confirmed_skills": spec["cur_skills"],
            "target_role": {
                "masco_code": tgt_r,
                "role_title": ROLE_TITLES.get(tgt_r, "Unknown Role")
            },
            "reskilling_pathway": {
                "planned_skills": spec["pathway"],
                "core_gaps": spec["core_gaps"],
                "important_gaps": [s for s in spec["pathway"] if s not in spec["core_gaps"]]
            },
            "scenario_context": {
                "assigned_scenario": spec["scenario"]
            },
            "data_classification": "SYNTHETIC_DEMO_NON_PII"
        }
        profiles.append(rec)

    dataset = {
        "dataset_name": "Synthetic Workforce Intelligence Profiles v1.0",
        "dataset_version": "1.0.0",
        "total_profiles": len(profiles),
        "synthetic_cohorts": [
            {"cohort_id": k, "profile_count": v} for k, v in sorted(cohort_counts.items())
        ],
        "synthetic_regions": [
            {"region_id": k, "profile_count": v} for k, v in sorted(region_counts.items())
        ],
        "demographic_fields_present": False,
        "pii_present": False,
        "purpose": "O6 SDG Contribution Aggregation Engine Development and Testing",
        "profiles": profiles
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(profiles)} synthetic profiles in {OUTPUT_FILE}")
    print(f"Cohorts: {cohort_counts}")
    print(f"Regions: {region_counts}")


if __name__ == "__main__":
    build_workforce()
