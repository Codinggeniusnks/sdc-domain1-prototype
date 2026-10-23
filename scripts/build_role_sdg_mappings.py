"""
Build Canonical Role SDG Mappings (M5 Stage 13A)
Maps all 20 MASCO 4-digit occupations to UN SDGs and verified targets.
Ensures:
- 100% MASCO coverage (20/20 roles)
- 1-3 primary SDGs per role
- Target-level evidence traceability
- Rigorous mapping types: DIRECT, ENABLING, CONTEXTUAL
- Full consistency with M3 role definitions
"""

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
TARGETS_FILE = ROOT / "data" / "sdg" / "sdg_targets_v1.json"
ROLES_INPUT_FILE = ROOT / "data" / "matching" / "role_requirements_v1_1.json"
OUTPUT_FILE = ROOT / "data" / "sdg" / "role_sdg_mappings_v1.json"

def main():
    with open(TARGETS_FILE, "r", encoding="utf-8") as f:
        targets_data = json.load(f)
    valid_targets = {t["target_id"]: t for t in targets_data["targets"]}

    with open(ROLES_INPUT_FILE, "r", encoding="utf-8") as f:
        roles_data = json.load(f)
    masco_roles = roles_data["roles"]

    # Map of 20 MASCO roles to SDG alignments
    role_mappings = {
        "2512": {
            "masco_code": "2512",
            "role_title": "Software Developers",
            "occupational_group": "Major Group 2: Professionals (ICT)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.5",
                    "target_description": "Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, in particular developing countries, including encouraging innovation and substantially increasing the number of research and development workers.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Software engineers design, code, and deploy enterprise applications, automated testing suites, and digital platforms that upgrade technological capabilities across industrial and services sectors.",
                    "evidence_references": "UN SDG Indicator 9.5.1/9.5.2 meta-framework; TalentCorp Impact Study 2024 Chapter 4; ESCO 2512 technology capability enhancement profile.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation, including through a focus on high-value added and labour-intensive sectors.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Enterprise software development enhances labour productivity, digitises manual operational bottlenecks, and accelerates high-value-added services economic growth.",
                    "evidence_references": "MyCOL 2024/2025 Critical Occupations List; ILO ICT Sector Productivity Framework 2023.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 17,
                    "sdg_name": "Partnerships for the Goals",
                    "target_id": "17.18",
                    "target_description": "Enhance capacity-building support to developing countries to increase significantly the availability of high-quality, timely and reliable data.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Building scalable open APIs and integrated data exchange architectures facilitates multi-stakeholder telemetry and data availability.",
                    "evidence_references": "UN ECOSOC Open Source & Public Goods Guidelines 2023.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED", "GENERAL_PURPOSE_ROLE_RULE_COMPLIANT"],
            "derivation_rules": ["RULE_ROLE_ENABLING_INNOVATION", "RULE_ROLE_PRODUCTIVITY_UPGRADING"]
        },
        "2511": {
            "masco_code": "2511",
            "role_title": "Systems Analysts",
            "occupational_group": "Major Group 2: Professionals (ICT)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.5",
                    "target_description": "Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, in particular developing countries, including encouraging innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Systems analysts assess institutional processes, translate organizational requirements into technical architecture specifications, and steer digital modernization across industrial ecosystems.",
                    "evidence_references": "ESCO 2511 ICT business analysis taxonomy; MASCO 2020 2511 system optimization task requirements.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "System architecture optimization eliminates structural operational friction and drives productivity across enterprise value chains.",
                    "evidence_references": "TalentCorp Impact Study 2024 Chapter 4; ILO Digital Transformation in Services 2023.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_ENABLING_INNOVATION", "RULE_ROLE_PRODUCTIVITY_UPGRADING"]
        },
        "2521": {
            "masco_code": "2521",
            "role_title": "Database Designers and Administrators",
            "occupational_group": "Major Group 2: Professionals (ICT)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.c",
                    "target_description": "Significantly increase access to information and communications technology and strive to provide universal and affordable access to the Internet in least developed countries.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Database architects build reliable, secure, high-concurrency data storage systems that underpin accessible digital public infrastructure and private web applications.",
                    "evidence_references": "ITU Digital Development Report 2023; MASCO 2020 2521 database architecture mandate.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 17,
                    "sdg_name": "Partnerships for the Goals",
                    "target_id": "17.18",
                    "target_description": "Enhance capacity-building support to developing countries to increase significantly the availability of high-quality, timely and reliable data disaggregated by characteristics.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Designing structured, sanitized, high-integrity database repositories directly guarantees the availability and reliability of data pipelines.",
                    "evidence_references": "UN Data Governance Strategy 2024; Cape Town Global Action Plan for Sustainable Development Data.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 16,
                    "sdg_name": "Peace, Justice and Strong Institutions",
                    "target_id": "16.10",
                    "target_description": "Ensure public access to information and protect fundamental freedoms, in accordance with national legislation and international agreements.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Database security enforcement and RBAC architectures protect data confidentiality while ensuring authorized access under data protection regulations.",
                    "evidence_references": "Malaysia PDPA 2010 database security compliance guidelines.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_DATA_INFRASTRUCTURE", "RULE_ROLE_GOVERNANCE_SECURITY"]
        },
        "2529": {
            "masco_code": "2529",
            "role_title": "Database and Network Professionals NEC (AI & Data Science Specialists)",
            "occupational_group": "Major Group 2: Professionals (ICT)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.5",
                    "target_description": "Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, including encouraging innovation and substantially increasing R&D workers.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "AI and data science specialists engineer predictive models, computer vision systems, and automated cognitive pipelines that advance industrial R&D capabilities.",
                    "evidence_references": "National Artificial Intelligence Roadmap 2021-2025 (Malaysia); TalentCorp Impact Study 2024 Chapter 4; ESCO 2529 data science taxonomy.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 17,
                    "sdg_name": "Partnerships for the Goals",
                    "target_id": "17.18",
                    "target_description": "Enhance capacity-building support to increase significantly the availability of high-quality, timely and reliable data.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Advanced statistical modelling, feature engineering, and automated ML pipelines turn raw sensory and operational feeds into decision-grade analytics.",
                    "evidence_references": "UN Big Data Project for Official Statistics; DOSM Open Data Framework.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through technological upgrading and innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Deploying predictive algorithms automates complex operational forecasting and resource optimization.",
                    "evidence_references": "World Economic Forum Future of Jobs Report 2023.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_ENABLING_INNOVATION", "RULE_ROLE_DATA_INFRASTRUCTURE"]
        },
        "2519": {
            "masco_code": "2519",
            "role_title": "Software and Applications Developers NEC (Cloud & Integration Specialists)",
            "occupational_group": "Major Group 2: Professionals (ICT)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.c",
                    "target_description": "Significantly increase access to information and communications technology and strive to provide universal and affordable access to the Internet.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Cloud and microservice integration specialists deploy distributed software services, lowering the infrastructure barriers for digital participation across SMEs.",
                    "evidence_references": "MyDigital Blueprint (Malaysia Digital Economy Blueprint); ITU Cloud Computing Guidelines 2023.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.4",
                    "target_description": "Upgrade infrastructure and retrofit industries to make them sustainable, with increased resource-use efficiency and greater adoption of clean and environmentally sound technologies.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Migrating on-premise legacy compute to energy-efficient hyperscale cloud architectures drastically reduces enterprise data centre carbon footprints.",
                    "evidence_references": "Green Computing / Cloud Sustainability Standard ISO/IEC 30134; TalentCorp 2024.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Cloud automation and DevOps pipelines accelerate time-to-market for digital products.",
                    "evidence_references": "ESCO 2519 cloud architecture competencies.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_ENABLING_INNOVATION", "RULE_ROLE_INFRASTRUCTURE_RETROFIT"]
        },
        "2522": {
            "masco_code": "2522",
            "role_title": "Systems Administrators and Cloud Infrastructure Specialists",
            "occupational_group": "Major Group 2: Professionals (ICT)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.c",
                    "target_description": "Significantly increase access to information and communications technology and strive to provide universal and affordable access to the Internet.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Systems administrators operate and secure server networks, virtual machines, and cloud environments that maintain continuous uptime for public and private web services.",
                    "evidence_references": "ITU Connectivity Benchmarks 2023; MASCO 2020 2522 systems maintenance standards.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Maintaining resilient computing environments prevents costly system outages and preserves enterprise labour productivity.",
                    "evidence_references": "ESCO 2522 systems administration operational guidelines.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_DATA_INFRASTRUCTURE", "RULE_ROLE_PRODUCTIVITY_UPGRADING"]
        },
        "2411": {
            "masco_code": "2411",
            "role_title": "Accountants and Auditors",
            "occupational_group": "Major Group 2: Professionals (Business & Administration)",
            "primary_sdgs": [
                {
                    "sdg_id": 16,
                    "sdg_name": "Peace, Justice and Strong Institutions",
                    "target_id": "16.6",
                    "target_description": "Develop effective, accountable and transparent institutions at all levels.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Accountants and financial auditors verify fiscal compliance, conduct statutory audits, prevent illicit financial flows, and enforce corporate reporting transparency.",
                    "evidence_references": "Malaysian Institute of Accountants (MIA) Standards; International Federation of Accountants (IFAC) SDG Report; MASCO 2020 2411 auditing tasks.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 12,
                    "sdg_name": "Responsible Consumption and Production",
                    "target_id": "12.6",
                    "target_description": "Encourage companies, especially large and transnational companies, to adopt sustainable practices and to integrate sustainability information into their reporting cycle.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Auditors and financial controllers prepare and assure non-financial ESG disclosures, carbon accounting records, and CSRD/Bursa Malaysia sustainability reporting statements.",
                    "evidence_references": "Bursa Malaysia Sustainability Reporting Guide (3rd Edition); ISSB Standards (IFRS S1 & S2); MIA Sustainability Blueprint.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Fiduciary governance and rigorous capital allocation advisory ensure sustainable business investment and economic stability.",
                    "evidence_references": "IFAC Value Creation in Professional Accountancy 2023.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED", "DIRECT_SUSTAINABILITY_ROLE"],
            "derivation_rules": ["RULE_ROLE_GOVERNANCE_SECURITY", "RULE_ROLE_SUSTAINABILITY_REPORTING"]
        },
        "2421": {
            "masco_code": "2421",
            "role_title": "Management and Organization Analysts (Transformation Consultants)",
            "occupational_group": "Major Group 2: Professionals (Business & Administration)",
            "primary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Management consultants guide organizational restructuring, optimize operating models, and champion digital process transformation across domestic enterprises.",
                    "evidence_references": "TalentCorp Impact Study 2024 Chapter 4; MASCO 2020 2421 organization analysis; Productivity Report (Malaysia Productivity Corporation).",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 12,
                    "sdg_name": "Responsible Consumption and Production",
                    "target_id": "12.6",
                    "target_description": "Encourage companies, especially large and transnational companies, to adopt sustainable practices and to integrate sustainability information into their reporting cycle.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Transformation analysts design circular economy business models, sustainable supply chain frameworks, and corporate decarbonization strategies.",
                    "evidence_references": "World Business Council for Sustainable Development (WBCSD) Guidelines; ESCO 2421 management consultancy.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_PRODUCTIVITY_UPGRADING", "RULE_ROLE_SUSTAINABILITY_REPORTING"]
        },
        "2422": {
            "masco_code": "2422",
            "role_title": "Policy and Corporate Planning Professionals (Governance Specialists)",
            "occupational_group": "Major Group 2: Professionals (Business & Administration)",
            "primary_sdgs": [
                {
                    "sdg_id": 16,
                    "sdg_name": "Peace, Justice and Strong Institutions",
                    "target_id": "16.6",
                    "target_description": "Develop effective, accountable and transparent institutions at all levels.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Corporate planning and policy professionals draft ethics frameworks, risk compliance policies, and governance charters that build institutional integrity.",
                    "evidence_references": "OECD Guidelines on Corporate Governance; MASCO 2020 2422 policy analysis; Malaysian Code on Corporate Governance (MCCG).",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 12,
                    "sdg_name": "Responsible Consumption and Production",
                    "target_id": "12.6",
                    "target_description": "Encourage companies, especially large and transnational companies, to adopt sustainable practices and to integrate sustainability information into their reporting cycle.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Corporate strategists formulate organizational Net Zero transition roadmaps, ESG key performance indicators, and responsible procurement policies.",
                    "evidence_references": "UN Global Compact Corporate Sustainability Framework; National Energy Transition Roadmap (NETR).",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 10,
                    "sdg_name": "Reduced Inequalities",
                    "target_id": "10.2",
                    "target_description": "By 2030, empower and promote the social, economic and political inclusion of all, irrespective of age, sex, disability, race, ethnicity, origin, religion or economic or other status.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "LIMITED",
                    "contribution_pathway": "Formulating diversity, equity, and inclusion (DEI) workforce policies in enterprise governance frameworks.",
                    "evidence_references": "ILO Workplace Diversity & Inclusion Policy Guide 2023.",
                    "confidence": "MEDIUM"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_GOVERNANCE_SECURITY", "RULE_ROLE_SUSTAINABILITY_REPORTING"]
        },
        "2151": {
            "masco_code": "2151",
            "role_title": "Electrical Engineers",
            "occupational_group": "Major Group 2: Professionals (Engineering)",
            "primary_sdgs": [
                {
                    "sdg_id": 7,
                    "sdg_name": "Affordable and Clean Energy",
                    "target_id": "7.2",
                    "target_description": "By 2030, increase substantially the share of renewable energy in the global energy mix.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Electrical engineers design, test, and commission solar photovoltaic arrays, grid-scale battery storage, wind converters, and high-voltage transmission interconnectors.",
                    "evidence_references": "National Energy Transition Roadmap (NETR, Malaysia); Suruhanjaya Tenaga (Energy Commission) Grid Codes; Board of Engineers Malaysia (BEM); MASCO 2020 2151.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 7,
                    "sdg_name": "Affordable and Clean Energy",
                    "target_id": "7.3",
                    "target_description": "By 2030, double the global rate of improvement in energy efficiency.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Engineers optimize industrial electrical motors, variable frequency drives, and smart building power distribution to eliminate parasitic transmission losses.",
                    "evidence_references": "Energy Efficiency and Conservation Act (EECA) Malaysia; IEEE Power & Energy Society Sustainability Roadmap.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.4",
                    "target_description": "By 2030, upgrade infrastructure and retrofit industries to make them sustainable, with increased resource-use efficiency and greater adoption of clean and environmentally sound technologies.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Retrofitting legacy power grids with smart distribution automation, IoT sensors, and microgrid controllers.",
                    "evidence_references": "Tenaga Nasional Berhad (TNB) Grid of the Future Masterplan; NIMP 2030 Mission 3.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED", "DIRECT_SUSTAINABILITY_ROLE", "GREEN_ECONOMY_CORE"],
            "derivation_rules": ["RULE_ROLE_CLEAN_ENERGY", "RULE_ROLE_INFRASTRUCTURE_RETROFIT"]
        },
        "2152": {
            "masco_code": "2152",
            "role_title": "Electronic Engineers (Semiconductor / Microelectronics Specialists)",
            "occupational_group": "Major Group 2: Professionals (Engineering)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.5",
                    "target_description": "Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, in particular developing countries, including encouraging innovation.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Electronic engineers spearhead IC design, advanced semiconductor packaging, wafer fabrication testing, and EDA tool validation across Malaysia's electrical & electronics (E&E) export sector.",
                    "evidence_references": "New Industrial Master Plan 2030 (NIMP 2030 Mission 1 & 2); Malaysia Semiconductor Strategy (NSS); MASCO 2020 2152.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 7,
                    "sdg_name": "Affordable and Clean Energy",
                    "target_id": "7.3",
                    "target_description": "By 2030, double the global rate of improvement in energy efficiency.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Developing ultra-low-power microcontrollers, gallium nitride (GaN) and silicon carbide (SiC) wide-bandgap power electronics that maximize electrical vehicle and solar inverter efficiency.",
                    "evidence_references": "Semiconductor Industry Association (SIA) Energy Efficiency Roadmap; IEEE Solid-State Circuits.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Transitioning semiconductor manufacturing into high-complexity front-end design and advanced wafer packaging elevates national manufacturing value-add.",
                    "evidence_references": "MIDA E&E Performance Report 2024; MyCOL 2024/2025.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED", "STRATEGIC_NIMP_2030_ROLE"],
            "derivation_rules": ["RULE_ROLE_ENABLING_INNOVATION", "RULE_ROLE_CLEAN_ENERGY", "RULE_ROLE_PRODUCTIVITY_UPGRADING"]
        },
        "2143": {
            "masco_code": "2143",
            "role_title": "Environmental Engineers",
            "occupational_group": "Major Group 2: Professionals (Engineering)",
            "primary_sdgs": [
                {
                    "sdg_id": 13,
                    "sdg_name": "Climate Action",
                    "target_id": "13.2",
                    "target_description": "Integrate climate change measures into national policies, strategies and planning.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Environmental engineers engineer industrial carbon capture, calculate life-cycle GHG emissions, formulate facility decarbonization roadmaps, and implement climate resilience strategies.",
                    "evidence_references": "Intergovernmental Panel on Climate Change (IPCC) WGIII Assessment; Malaysia National Climate Change Policy 2.0; Board of Engineers Malaysia (BEM); MASCO 2020 2143.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 12,
                    "sdg_name": "Responsible Consumption and Production",
                    "target_id": "12.6",
                    "target_description": "Encourage companies, especially large and transnational companies, to adopt sustainable practices and to integrate sustainability information into their reporting cycle.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Environmental engineers audit industrial effluent, conduct toxic lifecycle impact assessments, and verify technical sustainability disclosures for regulatory bodies.",
                    "evidence_references": "Department of Environment (DOE) Environmental Quality Act 1974; Bursa Malaysia ESG Guide.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 11,
                    "sdg_name": "Sustainable Cities and Communities",
                    "target_id": "11.6",
                    "target_description": "By 2030, reduce the adverse per capita environmental impact of cities, including by paying special attention to air quality and municipal and other waste management.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Design and oversight of municipal wastewater treatment facilities, ambient air quality monitoring arrays, and hazardous waste remediation systems.",
                    "evidence_references": "WHO Air Quality Guidelines; Solid Waste and Public Cleansing Management Act 2007 (Act 672, Malaysia).",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.4",
                    "target_description": "By 2030, upgrade infrastructure and retrofit industries to make them sustainable, with increased resource-use efficiency and greater adoption of clean technologies.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Retrofitting manufacturing plant exhaust scrubbers, zero-liquid-discharge (ZLD) plants, and closed-loop water recirculation systems.",
                    "evidence_references": "Green Technology Master Plan Malaysia 2017-2030.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED", "DIRECT_SUSTAINABILITY_ROLE", "GREEN_ECONOMY_CORE"],
            "derivation_rules": ["RULE_ROLE_CLIMATE_ACTION", "RULE_ROLE_SUSTAINABILITY_REPORTING", "RULE_ROLE_URBAN_SUSTAINABILITY"]
        },
        "2424": {
            "masco_code": "2424",
            "role_title": "Training and Staff Development Professionals (Reskilling Specialists)",
            "occupational_group": "Major Group 2: Professionals (Business & Administration)",
            "primary_sdgs": [
                {
                    "sdg_id": 4,
                    "sdg_name": "Quality Education",
                    "target_id": "4.4",
                    "target_description": "By 2030, substantially increase the number of youth and adults who have relevant skills, including technical and vocational skills, for employment, decent jobs and entrepreneurship.",
                    "mapping_type": "DIRECT",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Corporate trainers, L&D managers, and reskilling instructional designers formulate adult training curricula, deliver technical reskilling interventions, and track workforce competency acquisition.",
                    "evidence_references": "HRD Corp National Training Index (Malaysia); UNESCO-UNEVOC Technical and Vocational Education Guidelines; MASCO 2020 2424 staff development tasks.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.5",
                    "target_description": "By 2030, achieve full and productive employment and decent work for all women and men, including for young people and persons with disabilities, and equal pay for work of equal value.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Reskilling vulnerable and transitioning workers safeguards career longevity, prevents technological displacement, and maintains productive employment.",
                    "evidence_references": "TalentCorp Impact Study 2024 Chapter 5 (Reskilling Roadmap); ILO World Employment and Social Outlook 2023.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 10,
                    "sdg_name": "Reduced Inequalities",
                    "target_id": "10.2",
                    "target_description": "Empower and promote social, economic and political inclusion of all.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Designing inclusive adult learning pathways enables non-traditional and underrepresented worker cohorts to access digital jobs.",
                    "evidence_references": "UNESCO Lifelong Learning Policy Guide 2023.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED", "DIRECT_EDUCATION_RESKILLING_ROLE"],
            "derivation_rules": ["RULE_ROLE_EDUCATION_RESKILLING", "RULE_ROLE_DECENT_WORK"]
        },
        "2166": {
            "masco_code": "2166",
            "role_title": "Graphic and Multimedia Designers (UI/UX Designers)",
            "occupational_group": "Major Group 2: Professionals (Design)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.c",
                    "target_description": "Significantly increase access to information and communications technology and strive to provide universal and affordable access to the Internet.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "UI/UX and multimedia designers build intuitive, WCAG-compliant digital user interfaces that remove usability barriers and enable inclusive public and private web application adoption.",
                    "evidence_references": "W3C Web Content Accessibility Guidelines (WCAG 2.2); ISO 9241-210 Human-centred design; MASCO 2020 2166 multimedia design.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 10,
                    "sdg_name": "Reduced Inequalities",
                    "target_id": "10.2",
                    "target_description": "By 2030, empower and promote the social, economic and political inclusion of all, irrespective of age, sex, disability, race, ethnicity, origin, religion or economic or other status.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Designing accessible interfaces specifically accommodates elderly users, low-literacy populations, and persons with sensory or motor impairments, reducing digital exclusion.",
                    "evidence_references": "UN Enable Digital Inclusion Guidelines; MDeC Digital Accessibility Standard.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through technological upgrading and innovation.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Streamlined user experiences reduce operator cognitive load and transactional error rates in administrative and enterprise software.",
                    "evidence_references": "Nielsen Norman Group Enterprise UX ROI Benchmarks.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_ACCESSIBLE_INFRASTRUCTURE", "RULE_ROLE_SOCIAL_INCLUSION"]
        },
        "1330": {
            "masco_code": "1330",
            "role_title": "Information and Communications Technology Services Managers",
            "occupational_group": "Major Group 1: Managers (ICT)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.5",
                    "target_description": "Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, including encouraging innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "ICT services managers steer technological strategy, allocate R&D budgets, lead enterprise digital architecture transitions, and manage mission-critical technical teams.",
                    "evidence_references": "TalentCorp Impact Study 2024 Chapter 4; MyCOL 2024/2025; MASCO 2020 1330 ICT management functions.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Aligning enterprise information systems with core business operations scales technological efficiency and enables higher-margin digital service delivery.",
                    "evidence_references": "World Bank Digital Development Partnership 2023; ESCO 1330.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.c",
                    "target_description": "Significantly increase access to information and communications technology.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Expanding enterprise network coverage and ensuring high-availability SaaS infrastructure.",
                    "evidence_references": "ITU Telecommunication Management Network Standards.",
                    "confidence": "HIGH"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_ENABLING_INNOVATION", "RULE_ROLE_PRODUCTIVITY_UPGRADING"]
        },
        "3514": {
            "masco_code": "3514",
            "role_title": "Web Technicians and Cloud Operators",
            "occupational_group": "Major Group 3: Technicians and Associate Professionals (ICT)",
            "primary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.c",
                    "target_description": "Significantly increase access to information and communications technology and strive to provide universal and affordable access to the Internet.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Web technicians maintain web servers, handle content management deployment, test responsive browser compatibility, and keep corporate and public portals online.",
                    "evidence_references": "MASCO 2020 3514 web technician duties; ESCO 3514 web operations; MyCOL 2024/2025.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Routine maintenance and automated web testing support stable e-commerce and administrative web transactions.",
                    "evidence_references": "TalentCorp Impact Study 2024 Chapter 4.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_DATA_INFRASTRUCTURE", "RULE_ROLE_PRODUCTIVITY_UPGRADING"]
        },
        "3322": {
            "masco_code": "3322",
            "role_title": "Commercial Sales Representatives",
            "occupational_group": "Major Group 3: Technicians and Associate Professionals (Commercial)",
            "primary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.2",
                    "target_description": "Achieve higher levels of economic productivity through diversification, technological upgrading and innovation.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Commercial representatives match industrial buyers with advanced technological solutions, accelerating enterprise adoption of innovative machinery, software, and services.",
                    "evidence_references": "MASCO 2020 3322 sales representation; ILO Trade and Value Chains Report 2023.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 12,
                    "sdg_name": "Responsible Consumption and Production",
                    "target_id": "12.6",
                    "target_description": "Encourage companies to adopt sustainable practices.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "LIMITED",
                    "contribution_pathway": "Promoting eco-certified and energy-efficient products in commercial procurement contracts.",
                    "evidence_references": "Sustainable Public Procurement (SPP) Guidelines Malaysia.",
                    "confidence": "MEDIUM"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED", "CONTEXTUAL_COMMERCIAL_ROLE"],
            "derivation_rules": ["RULE_ROLE_PRODUCTIVITY_UPGRADING", "RULE_ROLE_CONTEXTUAL_MARKET_LINK"]
        },
        "4311": {
            "masco_code": "4311",
            "role_title": "Accounting and Bookkeeping Clerks",
            "occupational_group": "Major Group 4: Clerical Support Workers (Financial)",
            "primary_sdgs": [
                {
                    "sdg_id": 16,
                    "sdg_name": "Peace, Justice and Strong Institutions",
                    "target_id": "16.6",
                    "target_description": "Develop effective, accountable and transparent institutions at all levels.",
                    "mapping_type": "ENABLING",
                    "alignment_strength": "STRONG",
                    "contribution_pathway": "Bookkeeping clerks verify source receipts, maintain precise general ledgers, reconcile accounts, and support the factual integrity of corporate statutory audits.",
                    "evidence_references": "MASCO 2020 4311 accounting clerk tasks; MIA Bookkeeping Competency Framework.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.5",
                    "target_description": "By 2030, achieve full and productive employment and decent work for all women and men.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Executing day-to-day payroll, invoice processing, and cash reconciliation maintains organizational financial liquidity and administrative employment stability.",
                    "evidence_references": "ILO Global Wage Report 2023; TalentCorp 2024 Chapter 4.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_GOVERNANCE_SECURITY", "RULE_ROLE_DECENT_WORK"]
        },
        "4110": {
            "masco_code": "4110",
            "role_title": "General Office Clerks",
            "occupational_group": "Major Group 4: Clerical Support Workers (General)",
            "primary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.5",
                    "target_description": "By 2030, achieve full and productive employment and decent work for all women and men, including for young people and persons with disabilities.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "General office clerks handle document filing, inter-departmental communications, meeting coordination, and basic data entry, sustaining day-to-day administrative employment.",
                    "evidence_references": "MASCO 2020 4110 general clerical duties; ILO Employment Policy Guidelines.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [
                {
                    "sdg_id": 9,
                    "sdg_name": "Industry, Innovation and Infrastructure",
                    "target_id": "9.c",
                    "target_description": "Significantly increase access to information and communications technology.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "LIMITED",
                    "contribution_pathway": "Operating digital office tools and digitizing physical paperwork supports the digitization of frontline organizational records.",
                    "evidence_references": "Malaysia Digital Economy Corporation (MDEC) Office Digitisation Guidelines.",
                    "confidence": "MEDIUM"
                }
            ],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED", "CONTEXTUAL_CLERICAL_ROLE"],
            "derivation_rules": ["RULE_ROLE_DECENT_WORK", "RULE_ROLE_DATA_INFRASTRUCTURE"]
        },
        "3343": {
            "masco_code": "3343",
            "role_title": "Administrative and Executive Secretaries",
            "occupational_group": "Major Group 3: Technicians and Associate Professionals (Administrative)",
            "primary_sdgs": [
                {
                    "sdg_id": 8,
                    "sdg_name": "Decent Work and Economic Growth",
                    "target_id": "8.5",
                    "target_description": "By 2030, achieve full and productive employment and decent work for all women and men, including equal pay for work of equal value.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Executive secretaries manage senior leadership schedules, organize boardroom governance records, and maintain executive operational workflows, providing essential productivity multiplier support.",
                    "evidence_references": "MASCO 2020 3343 administrative secretary functions; ESCO 3343 executive assistant competencies.",
                    "confidence": "HIGH"
                },
                {
                    "sdg_id": 16,
                    "sdg_name": "Peace, Justice and Strong Institutions",
                    "target_id": "16.6",
                    "target_description": "Develop effective, accountable and transparent institutions at all levels.",
                    "mapping_type": "CONTEXTUAL",
                    "alignment_strength": "MODERATE",
                    "contribution_pathway": "Maintaining official minute archives, statutory board filings, and executive decision registers ensures procedural accountability.",
                    "evidence_references": "Companies Commission of Malaysia (SSM) Secretarial Practice Guide.",
                    "confidence": "HIGH"
                }
            ],
            "secondary_sdgs": [],
            "overall_confidence": "HIGH",
            "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "MASCO_TAXONOMY_GROUNDED"],
            "derivation_rules": ["RULE_ROLE_DECENT_WORK", "RULE_ROLE_GOVERNANCE_SECURITY"]
        }
    }

    # Audit validations
    print("Validating role SDG mappings against official targets...")
    assert len(role_mappings) == 20, f"Expected 20 roles, got {len(role_mappings)}"
    
    # Check that all roles from role_requirements_v1_1 are covered
    masco_codes_in_input = {r.get("masco_code", r.get("role_code")) for r in masco_roles}
    assert masco_codes_in_input == set(role_mappings.keys()), f"Mismatch in MASCO codes: {set(role_mappings.keys()) ^ masco_codes_in_input}"

    for code, role in role_mappings.items():
        assert 1 <= len(role["primary_sdgs"]) <= 3, f"Role {code} primary SDGs out of bounds (1-3): {len(role['primary_sdgs'])}"
        
        # Check all targets are valid
        all_alignments = role["primary_sdgs"] + role["secondary_sdgs"]
        for al in all_alignments:
            t_id = al["target_id"]
            assert t_id in valid_targets, f"Role {code} references invalid target {t_id}"
            assert al["mapping_type"] in ["DIRECT", "ENABLING", "CONTEXTUAL"], f"Invalid mapping_type {al['mapping_type']} in {code}"
            assert al["alignment_strength"] in ["STRONG", "MODERATE", "LIMITED"], f"Invalid alignment_strength in {code}"
            assert al["confidence"] in ["HIGH", "MEDIUM"], f"Invalid confidence in {code}"

    manifest = {
        "version": "1.0.0",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "engine": "M5 SDG Impact Mapping Engine",
        "total_roles_mapped": len(role_mappings),
        "target_reference_file": str(TARGETS_FILE.relative_to(ROOT)),
        "roles_source_file": str(ROLES_INPUT_FILE.relative_to(ROOT)),
        "roles": role_mappings
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated and validated {len(role_mappings)} role SDG mappings at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
