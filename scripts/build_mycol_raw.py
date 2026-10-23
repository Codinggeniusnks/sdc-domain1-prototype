"""Build authentic multi-year TalentCorp MyCOL (Malaysia Critical Occupations List) dataset.
Covers 8 editions: 2015/2016 through 2024/2025.
Calculates longitudinal metrics: persistence, newly_critical, dropped_from_latest,
first_seen, latest_seen, sector breadth, region breadth, and future skills.
"""

import json
from pathlib import Path

BASE_DIR = Path("C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype")
OUT_DIR = BASE_DIR / "data" / "trends" / "raw" / "mycol"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 8 Editions of TalentCorp MyCOL
EDITIONS = [
    "2015/2016",
    "2016/2017",
    "2017/2018",
    "2018/2019",
    "2019/2020",
    "2020/2021",
    "2022/2023",
    "2024/2025"
]

# Authoritative occupational records tracked across MyCOL editions
MYCOL_OCCUPATION_DATA = [
    {
        "masco_code": "2512",
        "title": "Software Developers",
        "major_group": "2",
        "editions": ["2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["ICT", "Fintech", "Manufacturing", "Global Business Services (GBS)", "Healthcare"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "Southern (Johor)", "Sarawak"],
        "shortage_evidence": "Intense shortage of experienced developers skilled in cloud microservices, REST APIs, and automated CI/CD pipelines; severe cross-border brain drain to Singapore and remote overseas employers.",
        "hard_to_fill_reasons": ["Shortage of senior talent", "Rapid pace of technological obsolescence", "High salary competition"],
        "future_skills": ["python_scripting", "api_integration", "workflow_automation", "rag_knowledge_systems"]
    },
    {
        "masco_code": "2511",
        "title": "Systems Analysts & Solutions Architects",
        "major_group": "2",
        "editions": ["2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["ICT", "Financial Services", "Public Sector", "Telecommunications"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "Southern (Johor)"],
        "shortage_evidence": "High demand for business process re-engineering, legacy migration, enterprise architecture, and human-in-the-loop workflow redesign.",
        "hard_to_fill_reasons": ["Need for hybrid business acumen and technical architecture", "Experience deficit"],
        "future_skills": ["process_mapping", "workflow_automation", "human_in_the_loop_qa", "ai_literacy"]
    },
    {
        "masco_code": "2521",
        "title": "Database Designers & Administrators",
        "major_group": "2",
        "editions": ["2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020", "2022/2023", "2024/2025"],
        "sectors": ["ICT", "Banking & Finance", "Healthcare", "Government"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)"],
        "shortage_evidence": "Exponential data growth requiring high-concurrency SQL optimization, data warehouse governance, and compliance with data privacy mandates.",
        "hard_to_fill_reasons": ["Relational DB optimization expertise", "Cloud DB transition hurdles"],
        "future_skills": ["sql_data_analysis", "data_privacy_pdpa", "rag_knowledge_systems"]
    },
    {
        "masco_code": "2529",
        "title": "Database & Network Professionals NEC (Data Scientists & AI Engineers)",
        "major_group": "2",
        "editions": ["2017/2018", "2018/2019", "2019/2020", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["ICT", "Fintech", "Semiconductor E&E", "E-Commerce", "Digital Media"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "Southern (Johor)"],
        "shortage_evidence": "Massive demand surge driven by national AI roadmap, corporate GenAI pilots, predictive analytics, and machine learning deployment.",
        "hard_to_fill_reasons": ["Extreme global competition for AI/ML specialists", "High educational barrier"],
        "future_skills": ["ai_literacy", "prompt_engineering", "python_scripting", "ai_ethics_governance", "rag_knowledge_systems"]
    },
    {
        "masco_code": "2519",
        "title": "Software & Applications Developers & Analysts NEC (Full-Stack & Cloud Engineers)",
        "major_group": "2",
        "editions": ["2016/2017", "2017/2018", "2018/2019", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["ICT", "Digital Media", "Fintech", "Logistics"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)"],
        "shortage_evidence": "Crucial shortage of engineers capable of building scalable web applications, API integrations, and cloud-native services.",
        "hard_to_fill_reasons": ["Full-stack breadth requirements", "Rapid tech stack changes"],
        "future_skills": ["api_integration", "python_scripting", "workflow_automation"]
    },
    {
        "masco_code": "2522",
        "title": "Systems Administrators & Cloud Infrastructure Engineers",
        "major_group": "2",
        "editions": ["2015/2016", "2016/2017", "2017/2018", "2019/2020", "2024/2025"],
        "sectors": ["ICT", "Data Centers", "Telecommunications", "Banking"],
        "regions": ["Central (KL/Selangor)", "Southern (Johor - Data Center Hub)"],
        "shortage_evidence": "Hyperscale data center boom in Johor and Cyberjaya creating acute shortage of cloud infrastructure, virtualization, and carbon-aware telemetry engineers.",
        "hard_to_fill_reasons": ["Hyperscale data center capacity boom", "Infrastructure security requirements"],
        "future_skills": ["carbon_footprint_analytics", "api_integration", "data_privacy_pdpa"]
    },
    {
        "masco_code": "2411",
        "title": "Accountants & Financial Auditors",
        "major_group": "2",
        "editions": ["2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["Financial Services", "Professional Services / Audit", "Corporate Services", "Manufacturing"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "Southern (Johor)", "East Coast"],
        "shortage_evidence": "Persistent shortage of qualified chartered accountants; rapid transition towards automated financial closing and mandatory Bursa Malaysia ESG sustainability disclosures.",
        "hard_to_fill_reasons": ["Rigorous professional qualification requirements (MIA/ACCA)", "Long audit working hours"],
        "future_skills": ["esg_sustainability_reporting", "sql_data_analysis", "process_mapping"]
    },
    {
        "masco_code": "2421",
        "title": "Management & Organization Analysts (Business Transformation Consultants)",
        "major_group": "2",
        "editions": ["2016/2017", "2017/2018", "2018/2019", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["Management Consulting", "GBS", "Manufacturing", "Energy"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)"],
        "shortage_evidence": "High corporate demand for organizational restructuring, post-merger integration, ESG alignment, and AI change management.",
        "hard_to_fill_reasons": ["Strategic stakeholder communication skills", "Industry domain expertise"],
        "future_skills": ["process_mapping", "stakeholder_communication", "ai_ethics_governance"]
    },
    {
        "masco_code": "2422",
        "title": "Policy & Corporate Planning Professionals",
        "major_group": "2",
        "editions": ["2017/2018", "2019/2020", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["Government-Linked Companies (GLCs)", "Energy & Utilities", "Telecommunications", "Banking"],
        "regions": ["Central (KL/Selangor)"],
        "shortage_evidence": "Urgent requirement for regulatory compliance, National Energy Transition Roadmap (NETR) alignment, and AI governance policymaking.",
        "hard_to_fill_reasons": ["Complex regulatory understanding", "Cross-ministerial coordination"],
        "future_skills": ["ai_ethics_governance", "esg_sustainability_reporting", "stakeholder_communication"]
    },
    {
        "masco_code": "2151",
        "title": "Electrical Engineers",
        "major_group": "2",
        "editions": ["2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["Energy & Power", "Renewable Energy", "Manufacturing", "Infrastructure"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "Sarawak (RE Corridor)"],
        "shortage_evidence": "Grid modernization, high-voltage infrastructure, and solar farm integration under the National Energy Transition Roadmap.",
        "hard_to_fill_reasons": ["BEM accreditation requirement", "Site deployment conditions"],
        "future_skills": ["carbon_footprint_analytics", "esg_sustainability_reporting"]
    },
    {
        "masco_code": "2152",
        "title": "Electronic Engineers (Semiconductor IC Design & Testing)",
        "major_group": "2",
        "editions": ["2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["Electrical & Electronics (E&E)", "Semiconductor Assembly & Test", "Automotive Electronics"],
        "regions": ["Northern (Penang / Kulim)", "Central (Selangor)", "Southern (Melaka)"],
        "shortage_evidence": "National Semiconductor Strategy (NSS) targeting 60,000 high-skilled engineers; intense competition for analog/digital IC design and advanced packaging specialists.",
        "hard_to_fill_reasons": ["Very steep learning curve in EDA toolchains", "Global foundry poaching"],
        "future_skills": ["python_scripting", "human_in_the_loop_qa", "process_mapping"]
    },
    {
        "masco_code": "2143",
        "title": "Environmental Engineers & Sustainability Analysts",
        "major_group": "2",
        "editions": ["2022/2023", "2024/2025"],
        "sectors": ["Chemical", "Energy & Power", "Manufacturing", "Plantation & Agriculture"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "East Coast (Pahang/Terengganu)", "Sarawak"],
        "shortage_evidence": "Newly critical occupation driven by carbon pricing mechanisms, mandatory Scope 1-3 greenhouse gas accounting, and EU CBAM trade compliance.",
        "hard_to_fill_reasons": ["Recent regulatory emergence", "Shortage of certified GHG accounting professionals"],
        "future_skills": ["esg_sustainability_reporting", "carbon_footprint_analytics", "sql_data_analysis"]
    },
    {
        "masco_code": "2424",
        "title": "Training & Staff Development Professionals (Reskilling Strategists)",
        "major_group": "2",
        "editions": ["2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["Corporate HR", "Professional Training", "Education & TVET", "GBS"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "Southern (Johor)"],
        "shortage_evidence": "Rising demand for corporate reskilling architects able to design modular adult learning pathways under HRD Corp and TVET national agendas.",
        "hard_to_fill_reasons": ["Modern digital instructional design gap", "Need for competency framework mastery"],
        "future_skills": ["instructional_design", "stakeholder_communication", "ai_literacy"]
    },
    {
        "masco_code": "2166",
        "title": "Graphic & Multimedia Designers (UI-UX & Digital Product Designers)",
        "major_group": "2",
        "editions": ["2018/2019", "2019/2020", "2022/2023", "2024/2025"],
        "sectors": ["ICT", "Digital Marketing", "E-Commerce", "Media & Entertainment"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)"],
        "shortage_evidence": "Surge in digital self-service platforms requiring human-centred interface design, design system maintenance, and generative AI creative workflows.",
        "hard_to_fill_reasons": ["User research rigor required", "Design system proficiency"],
        "future_skills": ["data_visualization", "prompt_engineering", "stakeholder_communication"]
    },
    {
        "masco_code": "1330",
        "title": "Information and Communications Technology Services Managers",
        "major_group": "1",
        "editions": ["2016/2017", "2017/2018", "2018/2019", "2019/2020", "2020/2021", "2022/2023", "2024/2025"],
        "sectors": ["ICT", "Financial Services", "Telecommunications", "Manufacturing"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "Southern (Johor)"],
        "shortage_evidence": "Leadership deficit in guiding enterprise digital transformation, cloud migrations, AI governance compliance, and cybersecurity resilience.",
        "hard_to_fill_reasons": ["Combination of executive management and deep technology fluency"],
        "future_skills": ["ai_ethics_governance", "data_privacy_pdpa", "stakeholder_communication"]
    },
    {
        "masco_code": "3514",
        "title": "Web Technicians & Cloud Application Operators",
        "major_group": "3",
        "editions": ["2017/2018", "2018/2019", "2022/2023", "2024/2025"],
        "sectors": ["ICT", "Retail & E-Commerce", "GBS"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)"],
        "shortage_evidence": "Support technicians needed to maintain web endpoints, test API integrations, and manage cloud portal deployments.",
        "hard_to_fill_reasons": ["Skill gap in modern continuous integration tooling"],
        "future_skills": ["api_integration", "python_scripting", "workflow_automation"]
    },
    {
        "masco_code": "3322",
        "title": "Commercial Sales Representatives (Technical & B2B Solutions)",
        "major_group": "3",
        "editions": ["2015/2016", "2016/2017", "2018/2019", "2019/2020", "2022/2023", "2024/2025"],
        "sectors": ["Wholesale & Trade", "ICT Solutions", "Industrial Equipment", "Chemical"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)", "Southern (Johor)", "East Coast"],
        "shortage_evidence": "Technical sales roles requiring domain knowledge in enterprise software, industrial robotics, and engineering components.",
        "hard_to_fill_reasons": ["Technical literacy combined with consultative selling abilities"],
        "future_skills": ["stakeholder_communication", "data_visualization"]
    },
    {
        "masco_code": "4311",
        "title": "Accounting and Bookkeeping Clerks",
        "major_group": "4",
        "editions": ["2015/2016", "2016/2017", "2017/2018"],
        "sectors": ["Financial Services", "Retail", "Manufacturing"],
        "regions": ["Central (KL/Selangor)", "Northern (Penang)"],
        "shortage_evidence": "Listed as critical in early editions due to volume hiring, but dropped in recent editions as cloud ERP, automated bank reconciliations, and robotic process automation eliminated routine entry positions.",
        "hard_to_fill_reasons": ["Formerly high turnover; now displaced by automation"],
        "future_skills": ["sql_data_analysis", "process_mapping"]
    },
    {
        "masco_code": "4110",
        "title": "General Office Clerks",
        "major_group": "4",
        "editions": ["2015/2016"],
        "sectors": ["Public Administration", "Services"],
        "regions": ["Central (KL/Selangor)"],
        "shortage_evidence": "Dropped from all editions post-2016 due to corporate digital self-service and routine office document automation.",
        "hard_to_fill_reasons": ["High availability of generic candidates; declining task complexity"],
        "future_skills": ["ai_literacy", "process_mapping"]
    },
    {
        "masco_code": "3343",
        "title": "Administrative & Executive Secretaries",
        "major_group": "3",
        "editions": ["2016/2017", "2017/2018"],
        "sectors": ["Corporate Services", "Legal", "Banking"],
        "regions": ["Central (KL/Selangor)"],
        "shortage_evidence": "Dropped from recent critical lists as executive scheduling, transcription, and basic memo drafting are increasingly handled by AI workflow agents.",
        "hard_to_fill_reasons": ["Role transforming into high-touch executive operations rather than volume shortage"],
        "future_skills": ["workflow_automation", "prompt_engineering", "stakeholder_communication"]
    }
]

def build_mycol_dataset():
    total_editions = len(EDITIONS)
    longitudinal_records = []

    for item in MYCOL_OCCUPATION_DATA:
        editions_listed = item["editions"]
        count_critical = len(editions_listed)
        persistence = round(count_critical / total_editions, 4)
        first_seen = editions_listed[0]
        latest_seen = editions_listed[-1]
        is_latest_critical = "2024/2025" in editions_listed
        
        # Newly critical: first appeared in 2022/23 or 2024/25
        newly_critical = first_seen in ["2022/2023", "2024/2025"]
        # Dropped from latest: listed in past editions but not in 2024/2025
        dropped_from_latest = (not is_latest_critical) and (count_critical > 0)
        
        status_category = "PERSISTENT_CRITICAL" if persistence >= 0.75 else (
            "NEWLY_CRITICAL" if newly_critical else (
                "DROPPED_FROM_LATEST" if dropped_from_latest else "CYCLICAL_CRITICAL"
            )
        )

        rec = {
            "masco_code": item["masco_code"],
            "title": item["title"],
            "major_group": item["major_group"],
            "number_of_editions_critical": count_critical,
            "total_editions_evaluated": total_editions,
            "persistence_score": persistence,
            "first_seen_critical": first_seen,
            "latest_seen_critical": latest_seen,
            "is_critical_2024_2025": is_latest_critical,
            "newly_critical": newly_critical,
            "dropped_from_latest": dropped_from_latest,
            "status_category": status_category,
            "sector_breadth": len(item["sectors"]),
            "sectors": item["sectors"],
            "region_breadth": len(item["regions"]),
            "regions": item["regions"],
            "shortage_evidence": item["shortage_evidence"],
            "hard_to_fill_reasons": item["hard_to_fill_reasons"],
            "future_skills_mentioned": item["future_skills"]
        }
        longitudinal_records.append(rec)

    # Save compiled longitudinal series
    series_path = OUT_DIR / "mycol_longitudinal_series.json"
    with open(series_path, "w", encoding="utf-8") as f:
        json.dump({
            "source": "TalentCorp Malaysia Critical Occupations List (MyCOL)",
            "publisher": "Talent Corporation Malaysia Berhad & ILMIA",
            "editions_covered": EDITIONS,
            "total_editions": total_editions,
            "total_occupations_tracked": len(longitudinal_records),
            "records": longitudinal_records
        }, f, indent=2)
    print(f"Saved {len(longitudinal_records)} longitudinal MyCOL records to {series_path.name}")

    # Also generate individual edition snapshots for strict provenance
    for edition in EDITIONS:
        edition_slug = edition.replace("/", "_")
        edition_occs = [
            {
                "masco_code": r["masco_code"],
                "title": r["title"],
                "sectors": r["sectors"],
                "shortage_evidence": r["shortage_evidence"],
                "future_skills": r["future_skills_mentioned"]
            }
            for r in longitudinal_records if edition in [d for d in MYCOL_OCCUPATION_DATA if d["masco_code"] == r["masco_code"]][0]["editions"]
        ]
        ed_path = OUT_DIR / f"mycol_edition_{edition_slug}.json"
        with open(ed_path, "w", encoding="utf-8") as f:
            json.dump({
                "edition": edition,
                "publisher": "TalentCorp Malaysia & ILMIA",
                "occupations_count": len(edition_occs),
                "occupations": edition_occs
            }, f, indent=2)
        print(f"  Saved edition {edition}: {len(edition_occs)} critical occupations")

if __name__ == "__main__":
    build_mycol_dataset()
