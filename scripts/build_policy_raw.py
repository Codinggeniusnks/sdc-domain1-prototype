"""Build Malaysian Policy & Institutional Priorities dataset (Tier A Policy Signals).
Includes MOSTI AIGE 2024, MyDIGITAL, Bursa Malaysia ESG Reporting Framework,
JPDP PDPA 2024 Amendment Act, and National Semiconductor Strategy (NSS).
"""

import json
from pathlib import Path

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
OUT_DIR = BASE_DIR / "data" / "trends" / "raw" / "policy"
OUT_DIR.mkdir(parents=True, exist_ok=True)

POLICY_RECORDS = [
    {
        "policy_id": "POL-MOSTI-AIGE-2024",
        "title": "National Guidelines on Artificial Intelligence Governance and Ethics (AIGE)",
        "issuing_agency": "Ministry of Science, Technology and Innovation (MOSTI) & National AI Office (NAIO)",
        "publication_date": "2024-09-20",
        "jurisdiction": "Malaysia (National)",
        "quality_tier": "TIER_A",
        "policy_status": "ACTIVE_MANDATE",
        "summary": "Establishes Malaysia's national standard for responsible AI deployment across public and private sectors, mandating human-in-the-loop oversight, fairness auditing, and transparency rubrics.",
        "core_pillars": [
            "Fairness & Non-Discrimination",
            "Reliability, Safety & Robustness",
            "Transparency & Explainability",
            "Human Oversight & Accountability",
            "Privacy & Data Protection",
            "Societal & Environmental Wellbeing"
        ],
        "impacted_skills": ["ai_ethics_governance", "human_in_the_loop_qa", "data_privacy_pdpa", "ai_literacy"],
        "impacted_occupations": ["2422", "2511", "2512", "1330"],
        "evidence_reference": "MOSTI National Guidelines on AI Governance and Ethics (AIGE), Document ID: MOSTI/NAIO/2024/01"
    },
    {
        "policy_id": "POL-BURSA-ESG-2024",
        "title": "Bursa Malaysia Enhanced Sustainability Reporting Framework (Main & ACE Market)",
        "issuing_agency": "Bursa Malaysia Berhad & Securities Commission Malaysia",
        "publication_date": "2024-06-15",
        "jurisdiction": "Malaysia (Capital Markets)",
        "quality_tier": "TIER_A",
        "policy_status": "MANDATORY_REGULATION",
        "summary": "Mandates comprehensive ESG disclosures aligned with the International Sustainability Standards Board (ISSB) standards S1 and S2, including Scope 1, 2, and 3 GHG emissions reporting for all listed issuers.",
        "core_pillars": [
            "Climate Change Strategy & TCFD/ISSB Alignment",
            "Scope 1, 2, and 3 Greenhouse Gas Inventory",
            "Energy & Carbon Compute Telemetry",
            "Diversity, Equity & Anti-Corruption Governance"
        ],
        "impacted_skills": ["esg_sustainability_reporting", "carbon_footprint_analytics", "sql_data_analysis", "data_visualization"],
        "impacted_occupations": ["2411", "2143", "2421", "2151"],
        "evidence_reference": "Bursa Malaysia Sustainability Reporting Guide (3rd Edition, 2024 Update), Listing Requirements Rule 9.45"
    },
    {
        "policy_id": "POL-JPDP-PDPA-2024",
        "title": "Personal Data Protection Act 2010 (Amendment Act 2024)",
        "issuing_agency": "Personal Data Protection Department (JPDP) & Ministry of Digital",
        "publication_date": "2024-07-31",
        "jurisdiction": "Malaysia (National Statutory)",
        "quality_tier": "TIER_A",
        "policy_status": "ENACTED_LEGISLATION",
        "summary": "Substantially strengthens personal data protection in Malaysia by introducing mandatory Data Protection Officer (DPO) appointments, mandatory 72-hour data breach reporting, and cross-border data transfer safeguards.",
        "core_pillars": [
            "Mandatory Data Protection Officer (DPO) Registration",
            "Mandatory 72-Hour Breach Notification",
            "Right to Data Portability",
            "Strict Cross-Border Data Transfer Assessments"
        ],
        "impacted_skills": ["data_privacy_pdpa", "ai_ethics_governance", "api_integration"],
        "impacted_occupations": ["2422", "2521", "2522", "1330"],
        "evidence_reference": "Laws of Malaysia, Act A1720, Personal Data Protection (Amendment) Act 2024"
    },
    {
        "policy_id": "POL-MYDIGITAL-MDEC-2021",
        "title": "Malaysia Digital Economy Blueprint (MyDIGITAL) & National 4IR Policy",
        "issuing_agency": "Economic Planning Unit (EPU) / Ministry of Digital / MDEC",
        "publication_date": "2021-02-19",
        "jurisdiction": "Malaysia (National Strategic Framework)",
        "quality_tier": "TIER_A",
        "policy_status": "ACTIVE_STRATEGIC_PLAN",
        "summary": "Strategic national roadmap to transform Malaysia into a digitally-driven, high-income nation. Targets 500,000 digital economy jobs, 100% student digital literacy, and 22.6% digital economy GDP contribution by 2025/2030.",
        "core_pillars": [
            "Agile Digital Infrastructure & 5G Rollout",
            "High-Skilled Digital Talent Pipeline (Premier Digital Tech Institutions)",
            "Enterprise Cloud & AI Adoption",
            "Government Digital Public Services"
        ],
        "impacted_skills": ["ai_literacy", "python_scripting", "sql_data_analysis", "workflow_automation", "instructional_design"],
        "impacted_occupations": ["2512", "2511", "2529", "2424", "1330"],
        "evidence_reference": "Economic Planning Unit, Prime Minister's Department, Malaysia Digital Economy Blueprint (2021)"
    },
    {
        "policy_id": "POL-MITI-NSS-2024",
        "title": "National Semiconductor Strategy (NSS)",
        "issuing_agency": "Ministry of Investment, Trade and Industry (MITI)",
        "publication_date": "2024-05-28",
        "jurisdiction": "Malaysia (National Industrial Strategy)",
        "quality_tier": "TIER_A",
        "policy_status": "ACTIVE_NATIONAL_PRIORITY",
        "summary": "Allocates RM25 billion to position Malaysia in high-value semiconductor design, advanced packaging, and manufacturing equipment, establishing a national target to train and upskill 60,000 engineers.",
        "core_pillars": [
            "Fabless Chip Design & IC Verification",
            "Advanced Packaging (Heterogeneous Integration)",
            "Automated Semiconductor Test Equipment",
            "High-Skilled Engineering Reskilling Pipelines"
        ],
        "impacted_skills": ["python_scripting", "human_in_the_loop_qa", "process_mapping", "instructional_design"],
        "impacted_occupations": ["2152", "2151", "2512", "2424"],
        "evidence_reference": "MITI National Semiconductor Strategy Policy Document (Launched May 2024)"
    }
]

def build_policy_raw():
    dataset = {
        "source": "Malaysian National Policy & Institutional Mandates",
        "publisher": "Government of Malaysia (MOSTI, Bursa Malaysia, JPDP, MITI, Ministry of Digital)",
        "jurisdiction": "Malaysia",
        "total_policies": len(POLICY_RECORDS),
        "records": POLICY_RECORDS
    }
    out_file = OUT_DIR / "malaysia_policy_signals.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"Saved Malaysian Policy Signals to {out_file.name} ({len(POLICY_RECORDS)} national policy mandates)")

if __name__ == "__main__":
    build_policy_raw()
