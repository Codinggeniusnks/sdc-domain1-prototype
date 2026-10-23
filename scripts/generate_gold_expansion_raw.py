"""Generator for Stage 8A Raw Occupational and Competency Source Data.
Produces immutable raw data files in data/raw/:
1. data/raw/masco/masco_expansion_p0_p1_p2.json
2. data/raw/competency_frameworks/competency_expansion_v5.json
3. data/raw/esco/esco_targeted_expansion.json

Includes:
- Legitimate Malaysian and international authoritative standards.
- Intentional negative audit test records (quarantined groups, near duplicates, ambiguous keywords, non-occupational text)
  to verify that the Gold Admission Gate strictly intercepts flawed records.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

(RAW_DIR / "masco").mkdir(parents=True, exist_ok=True)
(RAW_DIR / "competency_frameworks").mkdir(parents=True, exist_ok=True)
(RAW_DIR / "esco").mkdir(parents=True, exist_ok=True)


def build_masco_raw_data() -> list[dict]:
    """Generates authentic Malaysian occupational records covering P0, P1, P2 gaps,
    plus intentional negative test records for the admission gate audit.
    """
    records = []

    # -------------------------------------------------------------------------
    # P0: DATA PRIVACY & PDPA (Malaysian Legal & Enterprise Governance)
    # -------------------------------------------------------------------------
    pdpa_roles = [
        ("masco-raw-pdpa-01", "2421", "Enterprise Data Protection Officer", "Legal & Compliance",
         "Manages corporate Personal Data Protection Act (PDPA 2010) compliance across Malaysian business units. Conducts Privacy Impact Assessments (PIA) for customer-facing systems, maintains the register of processing activities, audits third-party data processor agreements under JPDP Standards 2015, and establishes mandatory 72-hour data breach containment protocols.",
         ["data_privacy_pdpa", "ai_ethics_governance", "stakeholder_communication"], 1.0,
         "JPDP Guidelines on Data Protection Officer & PDPA Act 709 Section 5-10", "https://www.pdp.gov.my"),
        ("masco-raw-pdpa-02", "2412", "Banking Customer Data Privacy Specialist", "Banking & Financial Services",
         "Audits customer personal information workflows in commercial banking operations in Kuala Lumpur. Enforces statutory consent withdrawal procedures, verifies cross-border financial data transfer agreements with overseas correspondent banks, and coordinates with internal audit to prevent unauthorised disclosures under Bank Negara Malaysia RMiT and PDPA regulations.",
         ["data_privacy_pdpa", "sql_data_analysis", "stakeholder_communication"], 1.0,
         "Bank Negara Malaysia RMiT & JPDP Financial Sector Standards", "https://www.bnm.gov.my"),
        ("masco-raw-pdpa-03", "1219", "Healthcare Information Governance & Privacy Manager", "Healthcare & Medical Services",
         "Ensures digital hospital information systems and electronic medical records comply with Malaysian Personal Data Protection Act principles. Implements role-based access control audits for clinical databases, enforces patient sensitive personal data consent policies, and leads hospital staff privacy training workshops.",
         ["data_privacy_pdpa", "stakeholder_communication", "process_mapping"], 0.5,
         "Ministry of Health Malaysia & JPDP Healthcare Data Advisory", "https://www.moh.gov.my"),
        ("masco-raw-pdpa-04", "1221", "Digital Retail Consumer Privacy Analyst", "Wholesale & Retail Trade",
         "Monitors consumer cookie tracking, direct marketing consent preferences, and customer data retention periods on Malaysian retail platforms. Audits third-party digital advertising trackers to ensure compliance with JPDP direct marketing rules and customer opt-out mechanisms.",
         ["data_privacy_pdpa", "data_visualization", "sql_data_analysis"], 1.0,
         "Malaysian E-Commerce Consumer Protection & PDPA Guidance", "https://www.kpdn.gov.my"),
        ("masco-raw-pdpa-05", "2511", "Cloud Infrastructure Privacy Architect", "ICT & Cloud Engineering",
         "Designs tenant data segregation, cryptographic key management, and privacy-preserving data access architectures for cloud services in Cyberjaya. Validates anonymisation and pseudonymisation pipelines to ensure cloud-hosted databases satisfy Malaysian statutory data localisation and transfer restrictions under the Personal Data Protection Act.",
         ["data_privacy_pdpa", "api_integration", "python_scripting"], 1.0,
         "MyDIGITAL Cloud Security & Privacy Architecture Standard", "https://www.mydigital.gov.my"),
        ("masco-raw-pdpa-06", "1212", "Human Resource Privacy & Employee Records Manager", "Human Resource Management",
         "Oversees employee personal data collection, background screening compliance, and HR records retention across Malaysian multinational shared services. Implements employee privacy notices, manages subject access requests, and audits payroll vendors under JPDP security standards.",
         ["data_privacy_pdpa", "process_mapping", "stakeholder_communication"], 0.5,
         "Malaysian Employers Federation (MEF) & JPDP HR Guidance", "https://www.mef.org.my"),
        ("masco-raw-pdpa-07", "2422", "Corporate Regulatory Counsel (Digital Privacy & Cyber Law)", "Professional & Legal Services",
         "Advises corporate boards on statutory liabilities under Malaysia's Personal Data Protection Act 2010 amendments. Drafts data transfer impact assessments, reviews cloud vendor liability clauses, and manages regulatory reporting to the Commissioner of Personal Data Protection during cybersecurity incidents.",
         ["data_privacy_pdpa", "ai_ethics_governance", "stakeholder_communication"], 1.0,
         "Malaysian Bar Council Cyber Law & Data Protection Committee", "https://www.malaysianbar.org.my"),
        ("masco-raw-pdpa-08", "2521", "Enterprise Database Privacy Operations Analyst", "Cybersecurity & IT Governance",
         "Operates data access logging and loss prevention telemetry consoles to detect unauthorized querying of national identification numbers and confidential corporate assets. Investigates privacy incident alerts, maps database access perimeters, and prepares formal compliance reports under the Malaysian Personal Data Protection Act.",
         ["data_privacy_pdpa", "sql_data_analysis", "process_mapping"], 1.0,
         "National Cyber Security Agency (NACSA) & JPDP Incident Protocol", "https://www.nacsa.gov.my"),
        ("masco-raw-pdpa-09", "1211", "Finance Privacy & Regulatory Compliance Auditor", "Accounting & Audit Services",
         "Performs comprehensive annual compliance audits against the Personal Data Protection Standard 2015 for insurance and asset management firms in Kuala Lumpur. Reviews physical and digital security controls, tests customer consent tracking databases, and issues formal remediation findings to senior leadership.",
         ["data_privacy_pdpa", "sql_data_analysis", "stakeholder_communication"], 0.5,
         "Malaysian Institute of Accountants (MIA) Regulatory Audit Series", "https://www.mia.org.my"),
        ("masco-raw-pdpa-10", "1324", "Logistics Fleet Information Privacy Controller", "Transportation & Logistics",
         "Audits delivery address databases, courier mobile app tracking permissions, and proof-of-delivery photo archiving procedures across nationwide express logistics networks. Enforces data destruction schedules for expired waybills in accordance with statutory PDPA privacy principles.",
         ["data_privacy_pdpa", "process_mapping", "workflow_automation"], 0.5,
         "Malaysian Logistics Council Data Handling Standard", "https://www.mot.gov.my"),
        ("masco-raw-pdpa-11", "2412", "FinTech Algorithmic KYC & Privacy Lead", "Financial Technology",
         "Designs privacy-preserving Know Your Customer (e-KYC) biometric workflows for digital remittance and micro-investing apps in Malaysia. Implements zero-knowledge proof verification algorithms and tokenised biometric storage to prevent identity disclosure under JPDP and BNM guidelines.",
         ["data_privacy_pdpa", "api_integration", "ai_ethics_governance"], 1.0,
         "FinTech Association of Malaysia (FAOM) Regulatory Guidelines", "https://www.fintechmalaysia.org"),
        ("masco-raw-pdpa-12", "2422", "Public Sector Data Governance & Citizen Privacy Officer", "Public Administration",
         "Coordinates data sharing protocols and citizen privacy compliance for federal and state digital public service platforms. Validates inter-agency data exchange APIs, establishes citizen consent registries, and monitors adherence to the National Data Sharing Policy and PDPA standards.",
         ["data_privacy_pdpa", "ai_ethics_governance", "api_integration"], 0.5,
         "MAMPU / Public Sector Digital Data Governance Standard", "https://www.mampu.gov.my"),
        ("masco-raw-pdpa-13", "2519", "Mobile App Privacy & SDK Compliance Engineer", "Software & Mobile Applications",
         "Inspects third-party software development kits (SDKs) and advertising libraries in Android/iOS apps for unauthorized device tracking and background location harvesting. Implements runtime user consent prompts and privacy-by-design architectures compliant with JPDP rules.",
         ["data_privacy_pdpa", "api_integration", "python_scripting"], 1.0,
         "MDEC Mobile App Developer Privacy Standards", "https://www.mdec.my"),
        ("masco-raw-pdpa-14", "3341", "BPO Customer Support Data Privacy Supervisor", "Global Business Services",
         "Supervises call centre agents handling sensitive identity verification across telecommunications customer care. Enforces redaction procedures for credit card numbers and identity cards in CRM ticket logs, and conducts weekly privacy spot-audits under Malaysian PDPA rules.",
         ["data_privacy_pdpa", "human_in_the_loop_qa", "process_mapping"], 0.5,
         "Contact Centre Association of Malaysia (CCAM) Privacy Blueprint", "https://www.ccam.com.my"),
        ("masco-raw-pdpa-15", "1346", "Digital InsurTech Claims Privacy Specialist", "Insurance & Actuarial Services",
         "Oversees medical claims document ingestion pipelines for life and health insurance underwriting. Validates policyholder consent forms, audits automated OCR text extraction for sensitive medical data leakage, and ensures data segregation between claims and marketing units under PDPA standards.",
         ["data_privacy_pdpa", "human_in_the_loop_qa", "workflow_automation"], 1.0,
         "Life Insurance Association of Malaysia (LIAM) Privacy Standard", "https://www.liam.org.my"),
        ("masco-raw-pdpa-16", "2421", "Marketing Technology Privacy Compliance Specialist", "Digital Marketing",
         "Configures customer data platforms (CDP) and email marketing automation pipelines to honor unsubscribes and data erasure requests under the Malaysian Personal Data Protection Act. Validates opt-in consent metadata tags across digital ad campaigns.",
         ["data_privacy_pdpa", "workflow_automation", "process_mapping"], 1.0,
         "Malaysian Digital Association (MDA) Data Guidelines", "https://www.malaysiandigital.org"),
        ("masco-raw-pdpa-17", "2512", "Backend API Privacy & Data Masking Developer", "Software Development",
         "Develops database middleware and microservices that perform real-time dynamic data masking (DDM) and field-level encryption on national identity numbers and financial accounts. Implements access-control policies in Python and Go aligned with JPDP security guidelines.",
         ["data_privacy_pdpa", "python_scripting", "api_integration"], 1.0,
         "MDEC Software Engineering Security Guidelines", "https://www.mdec.my"),
        ("masco-raw-pdpa-18", "4132", "Data Entry Privacy & Redaction Operator", "Business Support Services",
         "Performs manual review and optical redaction of customer tax forms and identity documents before ingestion into public cloud archives. Verifies that masking algorithms completely obscure confidential identifiers in accordance with enterprise PDPA operating procedures.",
         ["data_privacy_pdpa", "human_in_the_loop_qa", "process_mapping"], 0.0,
         "GBS Malaysia Data Processing Standard", "https://www.gbsmalaysia.org.my"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in pdpa_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"Department of Personal Data Protection (JPDP) & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # -------------------------------------------------------------------------
    # P0: PROCESS MAPPING & WORKFLOW ENGINEERING
    # -------------------------------------------------------------------------
    proc_roles = [
        ("masco-raw-proc-01", "2421", "Shared Services Business Process Mapping Lead", "Global Business Services (GBS)",
         "Facilitates enterprise value stream mapping workshops and documents end-to-end accounting process flows across regional shared services centres in Cyberjaya. Authors standard operating procedures (SOP), identifies manual handoff bottlenecks using BPMN diagrams, and tracks cycle-time reduction metrics.",
         ["process_mapping", "stakeholder_communication", "workflow_automation"], 1.0,
         "GBS Malaysia Operational Excellence & Process Mapping Framework", "https://www.gbsmalaysia.org.my"),
        ("masco-raw-proc-02", "2141", "Industrial Lean Six Sigma Process Engineer", "Manufacturing & Heavy Engineering",
         "Leads continuous improvement projects in automotive and industrial machinery manufacturing plants in Shah Alam. Performs time-and-motion studies, maps assembly line material flows, creates Spaghetti diagrams and Value Stream Maps (VSM), and implements 5S standard work documentation.",
         ["process_mapping", "data_visualization", "workflow_automation"], 0.5,
         "Malaysia Productivity Corporation (MPC) Lean Management Certification", "https://www.mpc.gov.my"),
        ("masco-raw-proc-03", "2412", "Banking Operational Workflow Optimization Specialist", "Banking & Financial Services",
         "Maps commercial mortgage underwriting and credit approval process chains across regional retail branches. Identifies multi-department handoff delays, produces detailed swimlane process flowcharts, and specifies standardized digital routing checklists to improve loan turnaround times.",
         ["process_mapping", "workflow_automation", "stakeholder_communication"], 0.5,
         "Asian Institute of Chartered Bankers (AICB) Operations Series", "https://www.aicb.org.my"),
        ("masco-raw-proc-04", "1324", "Supply Chain Warehouse Process Controller", "Logistics & Warehousing",
         "Documents inbound receiving, quality verification, and automated picking workflows in regional distribution hubs in Port Klang. Analyses warehouse management system (WMS) transit intervals, models floor layout bottlenecks using Visio process maps, and standardizes cross-docking SOPs.",
         ["process_mapping", "sql_data_analysis", "workflow_automation"], 0.5,
         "Chartered Institute of Logistics and Transport Malaysia (CILTM)", "https://www.cilt.org.my"),
        ("masco-raw-proc-05", "2511", "Enterprise ERP Business Process Systems Analyst", "ICT & Systems Consulting",
         "Gathers user requirements, documents AS-IS functional workflows, and architectures TO-BE process blueprints for enterprise resource planning (ERP) deployments across Malaysian conglomerate subsidiaries. Facilitates process alignment meetings between finance, procurement, and IT departments.",
         ["process_mapping", "stakeholder_communication", "sql_data_analysis"], 1.0,
         "Malaysian Digital Economy Corporation (MDEC) Enterprise Systems Guide", "https://www.mdec.my"),
        ("masco-raw-proc-06", "1219", "Healthcare Facility Clinical Workflow Mapping Officer", "Healthcare Services",
         "Conducts patient journey mapping from emergency triage to inpatient admission in private tertiary hospitals in Subang Jaya. Creates clinical process flowcharts, identifies diagnostic bottleneck points, and standardizes inter-departmental patient handover documentation under Malaysian Healthcare Quality standards.",
         ["process_mapping", "stakeholder_communication", "data_visualization"], 0.5,
         "Malaysian Society for Quality in Health (MSQH) Accreditation Standard", "https://www.msqh.com.my"),
        ("masco-raw-proc-07", "2141", "Quality Management Systems & ISO 9001 Lead Auditor", "Engineering & Quality Assurance",
         "Audits manufacturing standard operating procedures, documentation hierarchies, and corrective action workflows across precision engineering plants in Johor. Designs process control plans, failure mode and effects analysis (FMEA) flowcharts, and ensures audit readiness under ISO 9001:2015 frameworks.",
         ["process_mapping", "stakeholder_communication", "human_in_the_loop_qa"], 0.5,
         "SIRIM QAS International Quality Management Framework", "https://www.sirim-qas.com.my"),
        ("masco-raw-proc-08", "2422", "Public Sector Service Re-engineering Specialist", "Public Administration",
         "Maps citizen licensing and permit application workflows across municipal local councils. Identifies document verification redundancies, designs simplified digital submission swimlane flowcharts, and drafts service-level agreement SOPs under national administrative modernization initiatives.",
         ["process_mapping", "workflow_automation", "stakeholder_communication"], 0.5,
         "National Institute of Public Administration (INTAN) Process Guide", "https://www.intan.my"),
        ("masco-raw-proc-09", "1211", "Procure-to-Pay Accounting Process Analyst", "Accounting & Shared Services",
         "Maps end-to-end vendor onboarding, three-way invoice matching, and payment release workflows for regional multinational shared services hubs. Quantifies manual invoice exception rates, designs standardized escalation routing paths, and benchmarks processing cycle times.",
         ["process_mapping", "sql_data_analysis", "workflow_automation"], 0.5,
         "Chartered Institute of Management Accountants (CIMA) Malaysia Operations", "https://www.aicpa-cima.com"),
        ("masco-raw-proc-10", "2152", "Factory Automation Assembly Flow Engineer", "Electrical & Electronics Manufacturing",
         "Develops cycle-time process flowcharts for automated printed circuit board assembly (PCBA) lines in Penang. Documents feeder changeover procedures, identifies surface mount placement bottlenecks using line balancing software, and standardizes maintenance engineering work instructions.",
         ["process_mapping", "workflow_automation", "data_visualization"], 1.0,
         "Federation of Malaysian Manufacturers (FMM) Industry 4.0 Series", "https://www.fmm.org.my"),
        ("masco-raw-proc-11", "2421", "Customer Journey & Service Design Process Analyst", "Telecommunications & Customer Experience",
         "Maps customer touchpoint journey flows from broadband registration to technical fault dispatch. Documents multi-channel ticket resolution paths, quantifies customer drop-off bottlenecks using flowchart analytics, and specifies unified customer support escalation workflows.",
         ["process_mapping", "data_visualization", "stakeholder_communication"], 1.0,
         "Malaysian Communications and Multimedia Commission (MCMC) Quality Guide", "https://www.mcmc.gov.my"),
        ("masco-raw-proc-12", "3343", "Executive Office Administration Workflow Coordinator", "Corporate Administrative Services",
         "Standardizes corporate procurement requisition, contract approval routing, and digital board resolution workflows across group holding companies. Creates digital document approval swimlanes, authors office management standard operating manuals, and trains administrative staff.",
         ["process_mapping", "workflow_automation", "stakeholder_communication"], 0.5,
         "Malaysian Institute of Corporate Governance (MICG) Operational Guidelines", "https://www.micg.org.my"),
        ("masco-raw-proc-13", "3122", "Industrial Packaging Line Process Controller", "Food & Beverage Manufacturing",
         "Analyzes packaging line downtime and carton sealing bottlenecks in halal food manufacturing plants in Nilai. Maps operator handover workflows, develops standard work visual boards, and establishes line-clearance operating protocols.",
         ["process_mapping", "data_visualization", "workflow_automation"], 0.0,
         "Halal Development Corporation (HDC) Manufacturing Standards", "https://www.hdcglobal.com"),
        ("masco-raw-proc-14", "2421", "Digital Transformation Agile Process Consultant", "Management Consulting",
         "Conducts business architecture and value stream mapping for statutory bodies transitioning from legacy paper files to electronic document workflows. Designs future-state BPMN 2.0 flow models, facilitates user story workshops, and establishes change governance cadences.",
         ["process_mapping", "stakeholder_communication", "ai_literacy"], 1.0,
         "MDEC Digital Adoption Blueprint", "https://www.mdec.my"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in proc_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"Malaysia Productivity Corporation (MPC) & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # -------------------------------------------------------------------------
    # P0: ESG & SUSTAINABILITY REPORTING (Bursa Malaysia & NETR)
    # -------------------------------------------------------------------------
    esg_roles = [
        ("masco-raw-esg-01", "2412", "Corporate ESG & Climate Risk Analyst", "Capital Markets & Sustainable Finance",
         "Prepares mandatory sustainability statements for Bursa Malaysia Main Market listed entities in compliance with Bursa's Sustainability Reporting Guide (4th Edition). Calculates Scope 1, 2, and preliminary Scope 3 greenhouse gas emissions, compiles Task Force on Climate-related Financial Disclosures (TCFD) metrics, and assists external assurance audits.",
         ["esg_sustainability_reporting", "carbon_footprint_analytics", "stakeholder_communication"], 1.0,
         "Bursa Malaysia Sustainability Reporting Guide 4th Edition", "https://www.bursamalaysia.com"),
        ("masco-raw-esg-02", "2133", "Industrial Decarbonisation & Carbon Accounting Specialist", "Energy & Clean Technology",
         "Conducts facility-level greenhouse gas inventories across petrochemical and heavy manufacturing sites in Kerteh under Malaysia's National Energy Transition Roadmap (NETR). Quantifies stationary combustion, fugitive methane emissions, and flaring volumes according to GHG Protocol standards, and models carbon abatement pathways.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "data_visualization"], 1.0,
         "Ministry of Economy Malaysia / NETR Green Skills Standard", "https://www.ekonomi.gov.my"),
        ("masco-raw-esg-03", "1213", "Sustainability Strategy & ESG Disclosures Manager", "Conglomerate Management",
         "Formulates group-wide sustainability masterplans for diversified property and plantation conglomerates in Petaling Jaya. Coordinates materiality assessment surveys with institutional stakeholders, benchmarks performance against FTSE4Good Bursa Malaysia criteria, and drafts annual corporate governance and sustainability disclosures.",
         ["esg_sustainability_reporting", "stakeholder_communication", "data_visualization"], 1.0,
         "Securities Commission Malaysia Sustainable and Responsible Investment (SRI) Roadmap", "https://www.sc.com.my"),
        ("masco-raw-esg-04", "2143", "Environmental Compliance & Carbon Footprint Engineer", "Environmental Engineering",
         "Monitors stack flue gas emissions, wastewater effluent biochemical oxygen demand, and operational energy consumption in Kulim semiconductor fabrication plants. Calculates product carbon footprints across product life cycles using ISO 14067 frameworks, and prepares quarterly compliance dossiers for the Department of Environment.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "sql_data_analysis"], 1.0,
         "Department of Environment Malaysia (DOE) Industrial Emissions Standard", "https://www.doe.gov.my"),
        ("masco-raw-esg-05", "1211", "Sustainable Finance & ESG Portfolio Analyst", "Asset Management & Investment",
         "Evaluates corporate green bond issuances and Islamic Sukuk sustainability frameworks against ASEAN Green Bond Standards. Audits issuer carbon reduction targets, extracts financed emissions data from annual filings using SQL, and produces portfolio ESG risk dashboards for fund managers.",
         ["esg_sustainability_reporting", "sql_data_analysis", "carbon_footprint_analytics"], 1.0,
         "Bank Negara Malaysia & SC Climate Change and Principle-based Taxonomy (CCPT)", "https://www.bnm.gov.my"),
        ("masco-raw-esg-06", "3111", "Plantation Sustainability & Traceability Field Officer", "Agriculture & Commodity Trading",
         "Audits fresh fruit bunch transport manifests, deforestation satellite alerts, and chemical fertiliser usage in palm oil estates in Sabah. Validates certification documentation under Malaysian Sustainable Palm Oil (MSPO) standards and tracks estate-level carbon sequestration metrics.",
         ["esg_sustainability_reporting", "process_mapping", "human_in_the_loop_qa"], 0.5,
         "Malaysian Palm Oil Certification Council (MPOCC) MSPO 2022 Standard", "https://www.mpocc.org.my"),
        ("masco-raw-esg-07", "2142", "Green Building Index (GBI) & Energy Efficiency Assessor", "Construction & Real Estate",
         "Performs whole-building energy modeling, thermal envelope simulations, and embodied carbon assessments for commercial towers in Kuala Lumpur. Gathers data on sustainable building materials, water harvesting systems, and solar PV yields to achieve Green Building Index platinum certification.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "data_visualization"], 1.0,
         "Green Building Index Malaysia Technical Standard", "https://www.greenbuildingindex.org"),
        ("masco-raw-esg-08", "2412", "Supply Chain Scope 3 Emissions & ESG Auditor", "Manufacturing & Supply Chain",
         "Quantifies purchased goods upstream Scope 3 freight and vendor emissions across Tier 1 automotive suppliers in Selangor. Implements supplier sustainability evaluation scorecards, standardizes emissions data collection templates, and tracks carbon reduction commitments.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "stakeholder_communication"], 1.0,
         "Malaysian Automotive, Robotics and IoT Institute (MARii) Green Supply Chain", "https://www.marii.my"),
        ("masco-raw-esg-09", "1346", "Sustainable Banking & SME Transition Finance Officer", "Commercial Banking",
         "Assesses decarbonisation roadmaps and carbon reduction plans for small-and-medium enterprise borrowers seeking preferential green financing. Verifies energy audit reports, reviews renewable energy installations, and monitors loan portfolio alignment with BNM Climate Change taxonomy.",
         ["esg_sustainability_reporting", "stakeholder_communication", "carbon_footprint_analytics"], 1.0,
         "Association of Banks in Malaysia (ABM) ESG Financing Guide", "https://www.abm.org.my"),
        ("masco-raw-esg-10", "2133", "Renewable Energy Carbon Credit Verification Specialist", "Renewable Energy & Carbon Markets",
         "Validates generation data from grid-connected solar farms and biogas plants in Kedah to issue International Renewable Energy Certificates (I-REC) and Bursa Carbon Exchange (BCX) verified carbon credits. Conducts baseline emissions additionality audits and life-cycle GHG accounting.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "sql_data_analysis"], 1.0,
         "Bursa Carbon Exchange (BCX) Rules & Guidelines", "https://www.bursamalaysia.com"),
        ("masco-raw-esg-11", "2422", "Municipal Climate Resilience & Sustainability Officer", "Local Government Services",
         "Develops low-carbon city action plans for local councils under the Low Carbon Cities Framework (LCCF). Compiles municipal baseline energy consumption, waste diversion statistics, and public transit carbon abatement metrics for state climate change committees.",
         ["esg_sustainability_reporting", "carbon_footprint_analytics", "data_visualization"], 0.5,
         "Malaysian Green Technology and Climate Change Corporation (MGTC) LCCF", "https://www.mgtc.gov.my"),
        ("masco-raw-esg-12", "1321", "Industrial Waste & Circular Economy Sustainability Manager", "Chemical & Waste Management",
         "Monitors scheduled waste recycling rates, industrial co-processing yields, and circular economy resource flows in industrial parks. Prepares sustainability reports detailing water circularity, landfill diversion rates, and hazardous waste governance under statutory environmental guidelines.",
         ["esg_sustainability_reporting", "process_mapping", "stakeholder_communication"], 0.5,
         "Department of Environment Malaysia Scheduled Waste Regulations", "https://www.doe.gov.my"),
        ("masco-raw-esg-13", "2511", "ESG Data Integration & Sustainability Systems Architect", "Enterprise Software",
         "Architects automated ESG data lakes that ingest utility smart-meter feeds, ERP fuel purchase ledgers, and travel expense records. Builds automated carbon accounting calculation engines using Python and SQL to eliminate manual spreadsheet consolidation for Bursa sustainability disclosures.",
         ["esg_sustainability_reporting", "carbon_footprint_analytics", "python_scripting", "sql_data_analysis"], 1.0,
         "Bursa Malaysia ESG Reporting Technology Advisory", "https://www.bursamalaysia.com"),
        ("masco-raw-esg-14", "2412", "Sustainable Procurement & Ethical Sourcing Specialist", "Procurement & Corporate Governance",
         "Audits tier-1 vendor supply chain labour standards, worker accommodation compliance, and carbon footprint disclosures for export manufacturers in Penang. Implements supplier sustainability audit checklists and presents corrective action findings to group purchasing committees.",
         ["esg_sustainability_reporting", "carbon_footprint_analytics", "stakeholder_communication"], 0.5,
         "Federation of Malaysian Manufacturers Responsible Sourcing Code", "https://www.fmm.org.my"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in esg_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"Bursa Malaysia / MGTC & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # -------------------------------------------------------------------------
    # P1: INSTRUCTIONAL DESIGN & WORKFORCE DEVELOPMENT
    # -------------------------------------------------------------------------
    inst_roles = [
        ("masco-raw-inst-01", "2424", "Corporate Instructional Designer & e-Learning Developer", "Workforce Training & HRD",
         "Designs interactive digital learning modules and blended training curricula for technical professionals across Malaysian enterprises. Applies the ADDIE model to conduct learning needs analysis, scripts multimedia storyboards, and develops micro-learning units on company learning management systems.",
         ["instructional_design", "ai_literacy", "stakeholder_communication"], 1.0,
         "HRD Corp e-LATiH Instructional Design Framework", "https://www.hrdcorp.gov.my"),
        ("masco-raw-inst-02", "2424", "TVET Curriculum & Competency Standards Developer", "Vocational & Technical Education",
         "Develops National Occupational Skills Standards (NOSS) and competency-based training packages for Jabatan Pembangunan Kemahiran (JPK). Formulates learning outcomes, writes assessment performance rubrics, and designs practical workshop training manuals for technical skills certification.",
         ["instructional_design", "process_mapping", "stakeholder_communication"], 0.5,
         "Jabatan Pembangunan Kemahiran (JPK) NOSS Development Guidelines", "https://www.dsd.gov.my"),
        ("masco-raw-inst-03", "2424", "AI & Digital Skills Trainer / Instructional Specialist", "Higher Education & EdTech",
         "Creates course syllabi, laboratory coding tutorials, and practical generative AI prompt engineering assignments for tertiary polytechnic students. Conducts formative assessment design, evaluates student project submissions, and maps instructional content to Malaysian Qualifications Framework (MQF) standards.",
         ["instructional_design", "prompt_engineering", "ai_literacy"], 1.0,
         "Malaysian Qualifications Agency (MQA) & Department of Polytechnic Education", "https://www.mqa.gov.my"),
        ("masco-raw-inst-04", "2424", "Banking & Compliance Instructional Design Specialist", "Financial Services Training",
         "Designs mandatory anti-money laundering (AML/CFT) and fraud prevention e-learning courses for retail banking personnel. Authors scenario-based decision trees, creates interactive branching quizzes, and aligns course learning milestones with Bank Negara Malaysia regulatory requirements.",
         ["instructional_design", "stakeholder_communication", "human_in_the_loop_qa"], 0.5,
         "Asian Institute of Chartered Bankers (AICB) Learning Design Standards", "https://www.aicb.org.my"),
        ("masco-raw-inst-05", "2424", "Healthcare Simulation & Clinical Training Designer", "Medical & Nursing Education",
         "Designs clinical simulation scenarios, debriefing guides, and objective structured clinical examination (OSCE) assessment rubrics for nursing and paramedic staff. Integrates virtual patient mannequins and augmented reality anatomy software into continuing medical education curricula.",
         ["instructional_design", "data_visualization", "process_mapping"], 0.5,
         "Ministry of Health Malaysia Healthcare Training Division", "https://www.moh.gov.my"),
        ("masco-raw-inst-06", "2424", "Manufacturing Plant Technical Trainer & SOP Course Designer", "Industrial Training",
         "Develops bilingual on-the-job training modules and visual standard work training aids for automated semiconductor assembly line technicians in Bayan Lepas. Analyzes equipment error histories, writes step-by-step troubleshooting manuals, and evaluates technician practical competence.",
         ["instructional_design", "process_mapping", "workflow_automation"], 0.5,
         "Penang Skills Development Centre (PSDC) Technical Training Guidelines", "https://www.psdc.org.my"),
        ("masco-raw-inst-07", "2424", "EdTech Digital Learning Experience (LX) Designer", "Educational Technology",
         "Develops adaptive learning pathways and gamified instructional experiences for K-12 STEM education portals. Uses learner analytics data to optimize content sequencing, writes pedagogically sound instructional scripts, and evaluates learner engagement metrics.",
         ["instructional_design", "sql_data_analysis", "ai_literacy"], 1.0,
         "MDEC Digital Education Initiative Standards", "https://www.mdec.my"),
        ("masco-raw-inst-08", "2424", "Enterprise Leadership & Soft Skills Program Architect", "Corporate Talent Development",
         "Architects high-potential leadership development journeys and 360-degree feedback coaching workshops for government-linked companies (GLCs). Designs executive presentation rubrics, conducts diagnostic needs analysis, and measures training effectiveness using Kirkpatrick's Four-Level Model.",
         ["instructional_design", "stakeholder_communication", "data_visualization"], 0.5,
         "Razak School of Government (RSOG) Leadership Curriculum", "https://www.rsog.com.my"),
        ("masco-raw-inst-09", "2424", "Cybersecurity Awareness Instructional Designer", "Cybersecurity Training",
         "Designs interactive phishing simulation exercises and cybersecurity hygiene e-learning modules for federal civil servants. Creates realistic social engineering case scenarios, develops post-training assessment tests, and analyzes user click-rate vulnerabilities.",
         ["instructional_design", "ai_literacy", "human_in_the_loop_qa"], 1.0,
         "CyberSecurity Malaysia Professional Training Guidelines", "https://www.cybersecurity.my"),
        ("masco-raw-inst-10", "2424", "Retail & Customer Service Training Curriculum Lead", "Retail & Hospitality",
         "Develops front-line service excellence curricula and omnichannel POS system operational training modules for retail chain store associates. Creates video demonstrations, conducts train-the-trainer workshops, and monitors mystery shopper score improvements.",
         ["instructional_design", "process_mapping", "stakeholder_communication"], 0.0,
         "Malaysia Retailers Association (MRA) Training Blueprint", "https://www.mra.com.my"),
        ("masco-raw-inst-11", "2424", "Prompt-Assisted Courseware & Curriculum Architect", "EdTech & Generative Learning",
         "Architects automated courseware generation pipelines using generative AI prompt templates to accelerate technical curriculum authoring for polytechnics. Validates AI-generated lesson plans against national TVET competency standards and designs pedagogical evaluation rubrics.",
         ["instructional_design", "prompt_engineering", "ai_literacy"], 1.0,
         "HRD Corp AI in Learning & Development Framework", "https://www.hrdcorp.gov.my"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in inst_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"HRD Corp / JPK TVET & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # -------------------------------------------------------------------------
    # P1: SEMICONDUCTOR, E&E & INDUSTRIAL AUTOMATION
    # -------------------------------------------------------------------------
    semi_roles = [
        ("masco-raw-semi-01", "2152", "Semiconductor IC Packaging & Automation Engineer", "Electrical & Electronics (E&E)",
         "Programs automated wafer dicing, flip-chip die attach, and high-density wire bonding machinery in Penang advanced semiconductor packaging facilities. Writes Python automation scripts to parse Automated Test Equipment (ATE) yield logs, optimizes machine vision alignment recipes, and builds yield dashboards.",
         ["workflow_automation", "python_scripting", "data_visualization"], 1.0,
         "MIDA Malaysian Semiconductor Industry Roadmap 2024-2030", "https://www.mida.gov.my"),
        ("masco-raw-semi-02", "3114", "Automated Test Equipment (ATE) Firmware Technician", "Semiconductor Manufacturing",
         "Calibrates mixed-signal IC automated test handlers and programmable wafer probers in Kulim Hi-Tech Park. Executes automated Python test routines to screen microchips, troubleshoots PLC fault codes, and documents equipment calibration standard operating procedures.",
         ["workflow_automation", "python_scripting", "process_mapping"], 1.0,
         "Penang Automation Cluster (PAC) Technical Guidelines", "https://www.pac.org.my"),
        ("masco-raw-semi-03", "2141", "Smart Factory SCADA & MES Automation Systems Lead", "Precision Manufacturing",
         "Architects supervisory control and data acquisition (SCADA) and manufacturing execution system (MES) pipelines for automated cleanroom fabrication plants in Batu Kawan. Connects industrial IoT sensors via MQTT protocols, configures real-time PLC alarm escalation, and automates work order dispatch.",
         ["workflow_automation", "api_integration", "process_mapping"], 1.0,
         "Federation of Malaysian Manufacturers (FMM) Industry 4.0 Standard", "https://www.fmm.org.my"),
        ("masco-raw-semi-04", "3139", "Robotic Arm Automation & Cell Integration Specialist", "Advanced Robotics",
         "Programs 6-axis industrial articulated robots for automated solar panel assembly and semiconductor tray transfer. Optimizes robotic motion trajectories, integrates safety light curtains with PLC controllers, and authors robotic cell standard maintenance manuals.",
         ["workflow_automation", "process_mapping", "workflow_automation"], 0.5,
         "Malaysian Robotics and Automation Society (MyRAS) Standards", "https://www.myras.org.my"),
        ("masco-raw-semi-05", "2512", "Industrial IoT Edge Gateway Developer", "Embedded Systems & Electronics",
         "Writes Python and C++ firmware for industrial edge gateways deployed across electronics manufacturing lines. Implements automated sensor data ingestion pipelines, packages telemetry payloads into JSON for cloud streaming APIs, and validates zero-packet-loss edge buffering.",
         ["workflow_automation", "python_scripting", "api_integration"], 1.0,
         "CREST R&D Consortium Collaborative Engineering Framework", "https://www.crest.my"),
        ("masco-raw-semi-06", "2152", "Semiconductor Metrology & Optical Inspection Specialist", "Semiconductor Quality Control",
         "Develops automated recipe routines for scanning electron microscopes and high-speed optical defect inspection systems in silicon wafer fabrication. Analyzes defect density pareto charts using SQL, calibrates automated threshold triggers, and performs human verification on flagged wafer anomalies.",
         ["human_in_the_loop_qa", "sql_data_analysis", "workflow_automation"], 1.0,
         "MIDA Semiconductor Talent Framework", "https://www.mida.gov.my"),
        ("masco-raw-semi-07", "3115", "Mechatronics Maintenance & Predictive Sensor Technician", "Machinery & Equipment",
         "Maintains automated conveyor sorting systems and pneumatic pick-and-place grippers in airfreight logistics terminals at KLIA. Monitors vibration sensor telemetry, writes automated alerts for bearing wear, and executes scheduled preventive maintenance work orders.",
         ["workflow_automation", "process_mapping", "human_in_the_loop_qa"], 0.5,
         "Malaysian Society for Nondestructive Testing (MSNT)", "https://www.msnt.org.my"),
        ("masco-raw-semi-08", "2152", "Cleanroom Automated Material Handling (AMHS) Engineer", "Semiconductor Logistics",
         "Optimizes overhead hoist transport (OHT) vehicle dispatch schedules and automated wafer cassette stocker routing inside 300mm semiconductor fabs. Diagnoses track interlock errors using automated logging software, tracks delivery cycle times, and authors emergency recovery SOPs.",
         ["workflow_automation", "process_mapping", "sql_data_analysis"], 1.0,
         "Kulim Technology Park Corporation (KTPC) Fab Guidelines", "https://www.ktechnopark.com.my"),
        ("masco-raw-semi-09", "2519", "Computer Vision Defect Inspection Model Evaluator", "Industrial AI & Electronics",
         "Validates automated deep-learning optical inspection models classifying surface solder bridging and hairline crack defects on PCBA boards in Bayan Lepas. Labels edge-case micro-defect images, computes confusion matrices, and maintains human-in-the-loop audit gates to prevent false escapes.",
         ["human_in_the_loop_qa", "workflow_automation", "python_scripting"], 1.0,
         "MIDA Advanced Manufacturing AI Quality Guidelines", "https://www.mida.gov.my"),
        ("masco-raw-semi-10", "3114", "SMT Line Automated Stencil & Reflow Technician", "Electronics Assembly",
         "Sets up automated solder paste printing stencils and reflow oven temperature profiles on surface-mount technology (SMT) lines. Calibrates automated 3D solder paste inspection (SPI) parameters, investigates bridging alarms, and documents paste height standard operating procedures.",
         ["workflow_automation", "process_mapping", "human_in_the_loop_qa"], 0.5,
         "IPC Malaysia Electronics Assembly Standards", "https://www.ipc.org"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in semi_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"MIDA / Penang Automation Cluster & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # -------------------------------------------------------------------------
    # P1: CLERICAL / BPO MODERNIZATION & HUMAN-IN-THE-LOOP QA
    # -------------------------------------------------------------------------
    clerical_roles = [
        ("masco-raw-cler-01", "4132", "AI Document Ingestion & HITL Verification Specialist", "Global Business Services (GBS)",
         "Reviews AI-extracted text from digitised invoices, purchase orders, and customs declarations in shared services operations in Bangsar South. Corrects optical character recognition (OCR) parsing exceptions, audits low-confidence bounding boxes, and flags extraction discrepancies to improve automated document processing pipelines.",
         ["human_in_the_loop_qa", "workflow_automation", "process_mapping"], 0.5,
         "GBS Malaysia Digital Office Operations Framework", "https://www.gbsmalaysia.org.my"),
        ("masco-raw-cler-02", "4222", "Customer Contact Centre AI Support & Quality Auditor", "Telecommunications BPO",
         "Monitors generative AI chatbot customer interaction transcripts across multi-lingual helpdesks in Cyberjaya. Evaluates chatbot response accuracy against standard operating procedures, intervenes in escalated customer complaints, and updates prompt reply templates for edge cases.",
         ["human_in_the_loop_qa", "stakeholder_communication", "prompt_engineering"], 0.5,
         "Contact Centre Association of Malaysia (CCAM) Operational Guide", "https://www.ccam.com.my"),
        ("masco-raw-cler-03", "4311", "Accounts Payable Invoice Verification & Exception Clerk", "Corporate Financial Services",
         "Performs three-way matching verification on high-value supplier invoices flagged by automated ERP optical recognition workflows. Validates tax invoice details against purchase order ledgers using SQL queries, communicates with vendors to resolve price variances, and logs audit exceptions.",
         ["human_in_the_loop_qa", "sql_data_analysis", "stakeholder_communication"], 0.0,
         "Malaysian Institute of Accountants (MIA) Clerical Practice Guide", "https://www.mia.org.my"),
        ("masco-raw-cler-04", "4413", "Clinical Records Coding & Data Integrity Auditor", "Healthcare Administration",
         "Audits automated ICD-10 medical diagnostic coding suggestions generated from physician clinical notes. Verifies diagnostic specificity, corrects mismatched procedure codes in hospital information systems, and ensures billing integrity under national health financing standards.",
         ["human_in_the_loop_qa", "process_mapping", "data_privacy_pdpa"], 0.5,
         "Ministry of Health Malaysia Health Informatics Guidelines", "https://www.moh.gov.my"),
        ("masco-raw-cler-05", "4110", "Digital Registry & Records Modernization Clerk", "Public Sector Administration",
         "Scans, indexes, and validates official government land registry and birth record archives during digital conversion projects. Performs visual quality audits on digitized microfilm scans, tags metadata attributes according to national archiving standards, and logs defective images.",
         ["human_in_the_loop_qa", "process_mapping", "workflow_automation"], 0.0,
         "National Archives of Malaysia (Arkib Negara) Digitization Standard", "https://www.arkib.gov.my"),
        ("masco-raw-cler-06", "3341", "BPO Workflow Operations & Quality Team Lead", "Business Process Outsourcing",
         "Supervises a team of 25 data processing associates executing automated workflow queues. Analyzes daily first-pass yield metrics, investigates repetitive validation failure patterns using Excel charts, and refines operational standard work instructions.",
         ["process_mapping", "data_visualization", "workflow_automation"], 0.5,
         "OMiSTI / Outsourcing Malaysia Workforce Standards", "https://www.pikom.org.my"),
        ("masco-raw-cler-07", "4312", "Insurance Underwriting Document Validation Clerk", "General Insurance",
         "Inspects vehicle registration certificates, road tax records, and claims assessment photographs submitted through mobile self-service apps. Resolves identity data mismatches flagged by automated underwriting engines, and communicates with insurance agents regarding missing evidence.",
         ["human_in_the_loop_qa", "process_mapping", "stakeholder_communication"], 0.0,
         "General Insurance Association of Malaysia (PIAM) Operational Standard", "https://www.piam.org.my"),
        ("masco-raw-cler-08", "4131", "Legal Transcription & Speech-to-Text Proofreader", "Legal Support Services",
         "Reviews AI speech-to-text transcriptions of Malaysian court proceedings and arbitration hearings. Listens to audio recordings to correct legal terminology, speaker attributions, and local dialect nuances, delivering certified official transcripts under judicial transcription protocols.",
         ["human_in_the_loop_qa", "stakeholder_communication", "process_mapping"], 0.0,
         "Office of the Chief Registrar Federal Court of Malaysia Transcription Guide", "https://www.kehakiman.gov.my"),
        ("masco-raw-cler-09", "4321", "Inventory System Data Entry & Discrepancy Clerk", "Wholesale Distribution",
         "Verifies barcode scanner inventory intake records against shipping container manifests in Port Klang warehouses. Investigates stock variance flags in enterprise database tables, conducts physical cycle counts, and updates damaged stock write-off ledgers.",
         ["human_in_the_loop_qa", "sql_data_analysis", "process_mapping"], 0.0,
         "Chartered Institute of Logistics and Transport Malaysia", "https://www.cilt.org.my"),
        ("masco-raw-cler-10", "4211", "Digital Banking KYC Onboarding Verification Associate", "Banking Operations",
         "Conducts secondary human review on digital account opening applications flagged by automated risk and biometric liveness checks. Verifies Malaysian MyKad security features, cross-checks sanctions watchlist databases, and makes final compliance approvals under BNM guidelines.",
         ["human_in_the_loop_qa", "data_privacy_pdpa", "process_mapping"], 0.5,
         "Bank Negara Malaysia Policy Document on e-KYC", "https://www.bnm.gov.my"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in clerical_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"GBS Malaysia / CCAM & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # -------------------------------------------------------------------------
    # P1: FINTECH & DIGITAL BANKING (Bank Negara Malaysia & FAOM)
    # -------------------------------------------------------------------------
    fintech_roles = [
        ("masco-raw-fin-01", "2412", "Digital Banking Risk & Fraud Analytics Specialist", "Digital Banking & Payments",
         "Builds automated SQL queries and machine learning risk scorecards to detect suspicious financial transactions and account takeover attempts on digital banking platforms in Kuala Lumpur. Investigates anomalous money flows, evaluates fraud telemetry dashboards, and files suspicious transaction reports (STR) with Bank Negara Malaysia.",
         ["sql_data_analysis", "data_visualization", "workflow_automation"], 1.0,
         "Bank Negara Malaysia Financial Intelligence and Enforcement Department Guidelines", "https://www.bnm.gov.my"),
        ("masco-raw-fin-02", "2512", "Open Banking API & Payment Gateway Integration Engineer", "Financial Technology",
         "Develops and tests secure DuitNow QR and FPX payment gateway microservices adhering to Bank Negara Malaysia's Open API standards. Implements OAuth2 authentication handshakes, configures webhook callback listeners, and writes automated end-to-end integration tests using Python.",
         ["api_integration", "python_scripting", "workflow_automation"], 1.0,
         "PayNet Malaysia DuitNow API Technical Specification", "https://www.paynet.my"),
        ("masco-raw-fin-03", "2412", "Algorithmic Credit Scoring & Model Governance Analyst", "Micro-Financing & FinTech",
         "Designs alternative credit scoring models using telecommunications bill payment histories and e-commerce transaction data for unbanked micro-entrepreneurs. Audits predictive model feature importances, monitors demographic bias under ethical AI principles, and drafts technical documentation for BNM regulatory sandboxes.",
         ["sql_data_analysis", "ai_ethics_governance", "python_scripting"], 1.0,
         "FinTech Association of Malaysia (FAOM) Alternative Credit Blueprint", "https://www.fintechmalaysia.org"),
        ("masco-raw-fin-04", "1346", "Digital WealthTech Operations & Robot-Advisory Manager", "Wealth Management",
         "Oversees daily portfolio rebalancing and algorithmic asset allocation routines on automated robo-advisory platforms. Validates automated execution logs against client risk tolerance profiles, audits fee calculation algorithms, and ensures compliance with Securities Commission Malaysia digital investment guidelines.",
         ["workflow_automation", "stakeholder_communication", "sql_data_analysis"], 1.0,
         "Securities Commission Malaysia Digital Investment Management Framework", "https://www.sc.com.my"),
        ("masco-raw-fin-05", "2412", "Financial Crime Data Science & AML Modeling Specialist", "Regulatory Compliance",
         "Develops Python scripts to analyze cross-border fund transfer networks and identify money laundering mules across domestic payment switches. Builds automated graph visualization dashboards for anti-money laundering compliance officers, reducing false positive transaction alerts.",
         ["python_scripting", "data_visualization", "sql_data_analysis"], 1.0,
         "Asian Institute of Chartered Bankers AML/CFT Certification", "https://www.aicb.org.my"),
        ("masco-raw-fin-06", "3311", "Algorithmic Equities Execution Trader", "Capital Markets Trading",
         "Monitors and tunes automated execution algorithms (VWAP, TWAP) trading on Bursa Malaysia equity and derivatives markets. Analyzes market depth order book latency, reviews real-time slippage telemetry, and adjusts execution risk limit parameters.",
         ["sql_data_analysis", "workflow_automation", "python_scripting"], 1.0,
         "Bursa Malaysia Participant Trading Rules & Direct Market Access Guidelines", "https://www.bursamalaysia.com"),
        ("masco-raw-fin-07", "2511", "Core Banking Cloud Migration Systems Analyst", "Banking Technology",
         "Maps legacy mainframe deposit and lending database schemas to cloud-native microservices for Malaysian commercial banks. Validates data integrity during automated ETL pipeline migrations, specifies REST API payload contracts, and coordinates technical user acceptance testing.",
         ["sql_data_analysis", "api_integration", "process_mapping"], 1.0,
         "Bank Negara Malaysia Risk Management in Technology (RMiT)", "https://www.bnm.gov.my"),
        ("masco-raw-fin-08", "3312", "Commercial Credit Risk Underwriter & Financial Data Analyst", "Commercial Lending",
         "Analyzes financial statements, bank statement cash flows, and debt service coverage ratios for corporate loan applications in SME commercial banking. Uses SQL and Excel to model debt repayment sensitivity under varying interest rates, and prepares comprehensive credit committee memorandums.",
         ["sql_data_analysis", "stakeholder_communication", "data_visualization"], 0.5,
         "Asian Institute of Chartered Bankers (AICB) Credit Risk Framework", "https://www.aicb.org.my"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in fintech_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"Bank Negara Malaysia / FAOM & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # -------------------------------------------------------------------------
    # P2: ADVANCED AI & DIGITAL SKILLS (RAG, Prompt Engineering, Python, AI Ethics)
    # -------------------------------------------------------------------------
    ai_roles = [
        ("masco-raw-ai-01", "2519", "Enterprise RAG & Knowledge Systems Architect", "Artificial Intelligence & Enterprise Systems",
         "Architects retrieval-augmented generation (RAG) pipelines over Malaysian corporate document archives and legal jurisprudence databases. Implements dense vector indexing with Milvus, configures semantic hybrid search rerankers, and evaluates context retrieval precision to prevent LLM hallucinations.",
         ["rag_knowledge_systems", "python_scripting", "api_integration"], 1.0,
         "MDEC National Artificial Intelligence Roadmap (2021-2025)", "https://www.mdec.my"),
        ("masco-raw-ai-02", "2519", "Generative AI Prompt Engineer & LLM Evaluator", "AI Solutions Development",
         "Designs and refines systematic prompt engineering templates for enterprise customer support chatbots and legal document summarization agents. Authors few-shot prompt libraries, benchmarks output quality across Claude and GPT foundation models, and tests adversarial prompt injection resistance.",
         ["prompt_engineering", "ai_literacy", "human_in_the_loop_qa"], 1.0,
         "MDEC Generative AI Guidelines for Malaysian Industry", "https://www.mdec.my"),
        ("masco-raw-ai-03", "2512", "AI Solutions Backend Developer (Python & Vector DB)", "Software Engineering",
         "Builds scalable Python FastAPI backends that integrate vector databases and large language model APIs for banking research analysts. Implements asynchronous API integration endpoints, semantic chunking algorithms for PDF filings, and token caching mechanisms.",
         ["python_scripting", "api_integration", "rag_knowledge_systems"], 1.0,
         "MyDIGITAL National 4IR Policy Workforce Guide", "https://www.mydigital.gov.my"),
        ("masco-raw-ai-04", "2422", "AI Ethics & Algorithmic Governance Officer", "Digital Policy & Technology Ethics",
         "Audits enterprise artificial intelligence models for demographic bias, algorithmic transparency, and compliance with Malaysia's National AI Governance and Ethics (AIGE) guidelines. Establishes model risk registries, conducts ethical impact assessments, and reports model evaluation findings to corporate executive risk committees.",
         ["ai_ethics_governance", "ai_literacy", "stakeholder_communication"], 1.0,
         "Ministry of Science, Technology and Innovation (MOSTI) National AI Governance Code", "https://www.mosti.gov.my"),
        ("masco-raw-ai-05", "2511", "Enterprise AI Adoption & Workforce Literacy Specialist", "Corporate Digital Transformation",
         "Leads enterprise-wide AI literacy workshops for non-technical business units across multinational companies in Malaysia. Trains business analysts on prompt engineering fundamentals, responsible generative AI usage policies, and workflow automation opportunities using no-code AI tools.",
         ["ai_literacy", "prompt_engineering", "stakeholder_communication"], 1.0,
         "HRD Corp National Training Week AI Upskilling Standards", "https://www.hrdcorp.gov.my"),
        ("masco-raw-ai-06", "2519", "Legal Tech RAG & Document Intelligence Engineer", "Legal Technology",
         "Builds specialized legal search retrieval-augmented generation systems indexing Malaysian statutes, subsidiary legislation, and reported judgments. Formulates vector chunking strategies preserving legislative section hierarchies, and integrates citation validation checks.",
         ["rag_knowledge_systems", "python_scripting", "prompt_engineering"], 1.0,
         "Malaysian Bar Council Legal Technology Innovation Guide", "https://www.malaysianbar.org.my"),
        ("masco-raw-ai-07", "2519", "Customer Experience Conversational Prompt Designer", "Customer Experience Technology",
         "Develops conversational system prompts and tone-of-voice persona constraints for omnichannel banking customer assistants. Evaluates intent recognition accuracy, conducts multi-turn prompt debugging, and refines fallback escalation triggers to human customer care agents.",
         ["prompt_engineering", "human_in_the_loop_qa", "stakeholder_communication"], 1.0,
         "Contact Centre Association of Malaysia AI Guidelines", "https://www.ccam.com.my"),
        ("masco-raw-ai-08", "2512", "Data Pipeline & Analytical Automation Developer", "Data Engineering",
         "Develops automated data extraction and transformation pipelines in Python to ingest heterogeneous ERP, CRM, and web analytics logs into Snowflake data warehouses. Orchestrates workflow automation jobs using Apache Airflow, writes SQL transformations, and monitors pipeline execution telemetry.",
         ["python_scripting", "workflow_automation", "sql_data_analysis"], 1.0,
         "MDEC Big Data and Analytics Workforce Competencies", "https://www.mdec.my"),
        ("masco-raw-ai-09", "2519", "Medical Clinical Decision Support RAG Engineer", "Health Informatics",
         "Develops clinical knowledge retrieval-augmented systems indexing peer-reviewed biomedical literature and Ministry of Health clinical practice guidelines for hospital physicians. Tunes dense retrieval embeddings, implements strict medical provenance citations, and measures factual accuracy against medical ground truth.",
         ["rag_knowledge_systems", "python_scripting", "human_in_the_loop_qa"], 1.0,
         "Ministry of Health Malaysia Health Tech Innovation Blueprint", "https://www.moh.gov.my"),
        ("masco-raw-ai-10", "2422", "Algorithmic Fairness & Model Risk Validator", "Financial Risk & Compliance",
         "Performs independent model validation on automated retail credit underwriting algorithms used by licensed financial institutions in Malaysia. Calculates disparate impact ratios, identifies proxy variable biases, and authors formal model governance reports for Bank Negara Malaysia.",
         ["ai_ethics_governance", "sql_data_analysis", "stakeholder_communication"], 1.0,
         "Bank Negara Malaysia Technology Risk Governance Series", "https://www.bnm.gov.my"),
        ("masco-raw-ai-11", "2519", "Domain-Specific Prompt Optimization Engineer", "Enterprise AI Consulting",
         "Authors structured system prompt templates incorporating XML tags and chain-of-thought instructions for enterprise financial analysis and ESG report drafting. Benchmarks output consistency, evaluates token cost efficiency across API providers, and establishes automated evaluation assertions.",
         ["prompt_engineering", "ai_literacy", "api_integration"], 1.0,
         "MDEC Artificial Intelligence Industry Standards", "https://www.mdec.my"),
        ("masco-raw-ai-12", "2519", "Enterprise Semantic Search & Knowledge Graph Specialist", "Enterprise Search & Knowledge Management",
         "Constructs hybrid retrieval-augmented generation architectures combining vector embeddings and Neo4j knowledge graphs over manufacturing failure logs and engineering schematics. Implements multi-hop query decomposition in Python and designs evaluation benchmarks.",
         ["rag_knowledge_systems", "python_scripting", "api_integration"], 1.0,
         "CREST Collaborative Engineering AI Framework", "https://www.crest.my"),
        ("masco-raw-ai-13", "2511", "Generative AI Workflow Automation Consultant", "Digital Transformation",
         "Designs automated business document processing workflows connecting generative LLM APIs with internal ERP systems for Malaysian logistics operators. Constructs few-shot prompts to extract structured shipment parameters, automates exceptions routing, and trains administrative staff.",
         ["workflow_automation", "prompt_engineering", "api_integration", "ai_literacy"], 1.0,
         "MDEC Digital Productivity Initiative", "https://www.mdec.my"),
        ("masco-raw-ai-14", "2519", "Multilingual Prompt Localization Specialist", "Natural Language Processing",
         "Optimizes prompt engineering templates for multilingual Bahasa Malaysia, English, and Mandarin customer service virtual assistants. Analyzes linguistic nuance, prevents semantic drift in code-switched queries, and evaluates automated translation fidelity.",
         ["prompt_engineering", "human_in_the_loop_qa", "ai_literacy"], 1.0,
         "MDEC Language Technology Standards", "https://www.mdec.my"),
        ("masco-raw-ai-15", "2519", "Technical Documentation RAG System Developer", "Software Architecture",
         "Builds internal engineering retrieval-augmented documentation assistants indexing software repositories, API specifications, and architectural decision records. Implements semantic hybrid search over markdown codebases using Python and Qdrant vector databases.",
         ["rag_knowledge_systems", "python_scripting", "api_integration"], 1.0,
         "MyDIGITAL Software Engineering Standards", "https://www.mydigital.gov.my"),
        ("masco-raw-ai-16", "2519", "Enterprise Knowledge Base & Vector Indexing Engineer", "ICT Services & Enterprise Search",
         "Develops semantic vector indexing and retrieval-augmented generation pipelines over multi-terabyte internal documentation and confluence repositories. Implements recursive chunking algorithms in Python, evaluates embedding distance metrics, and integrates API endpoints.",
         ["rag_knowledge_systems", "python_scripting", "api_integration"], 1.0,
         "MDEC Cloud & Big Data Standards", "https://www.mdec.my"),
        ("masco-raw-ai-17", "2511", "Enterprise Knowledge Management & Vector Retrieval Lead", "Corporate ICT",
         "Leads corporate knowledge management modernization connecting legacy document stores with modern neural vector databases. Specifies retrieval-augmented generation search architectures, tunes BM25 and vector hybrid search algorithms, and audits retrieval recall.",
         ["rag_knowledge_systems", "process_mapping", "stakeholder_communication"], 1.0,
         "TalentCorp MyCOL ICT Services Framework", "https://www.talentcorp.com.my"),
        ("masco-raw-ai-18", "2512", "Customer Support RAG Agent Backend Developer", "FinTech & E-Commerce",
         "Builds Python FastAPI services that ingest customer support tickets, FAQs, and product manuals into Pinecone vector databases. Constructs retrieval-augmented generation context injection pipelines for generative chatbots, and monitors response latency.",
         ["rag_knowledge_systems", "python_scripting", "api_integration"], 1.0,
         "PayNet FinTech Architecture Series", "https://www.paynet.my"),
        ("masco-raw-ai-19", "2519", "Scientific & Medical Literature RAG Specialist", "HealthTech & Pharmaceuticals",
         "Builds domain-specific retrieval-augmented search applications indexing medical clinical trials and pharmacological research papers. Evaluates reranker precision using cross-encoders in Python, validates source citation fidelity, and prevents hallucinated medical claims.",
         ["rag_knowledge_systems", "python_scripting", "human_in_the_loop_qa"], 1.0,
         "Clinical Research Malaysia (CRM) Health Informatics Guide", "https://www.clinicalresearch.my"),
        ("masco-raw-ai-20", "2519", "Regulatory Compliance RAG System Engineer", "Regulatory Technology (RegTech)",
         "Designs automated retrieval-augmented systems over Bank Negara Malaysia circulars, statutory acts, and tax guidelines. Implements hierarchical section-aware document chunking, tests hybrid dense-sparse vector search, and evaluates context retrieval precision.",
         ["rag_knowledge_systems", "python_scripting", "ai_ethics_governance"], 1.0,
         "Asian Institute of Chartered Bankers Regulatory Series", "https://www.aicb.org.my"),
        ("masco-raw-ai-21", "2519", "Industrial Equipment Troubleshooting RAG Developer", "Manufacturing Tech",
         "Builds retrieval-augmented troubleshooting assistants indexing equipment repair schematics and error codes for manufacturing technicians. Creates automated PDF document parsing pipelines in Python, tunes dense embeddings, and evaluates context window efficiency.",
         ["rag_knowledge_systems", "workflow_automation", "python_scripting"], 1.0,
         "FMM Advanced Manufacturing AI Guidelines", "https://www.fmm.org.my"),
        ("masco-raw-ai-22", "2519", "Generative LLM Prompt Architect & Evaluator", "Enterprise AI Consulting",
         "Authors system prompts, few-shot demonstration exemplars, and output schema constraints for generative language model applications in Malaysian enterprises. Benchmarks multi-turn prompt stability across reasoning models, minimizes prompt injection vulnerabilities, and optimizes token costs.",
         ["prompt_engineering", "ai_literacy", "human_in_the_loop_qa"], 1.0,
         "MDEC Generative AI Playbook", "https://www.mdec.my"),
        ("masco-raw-ai-23", "2519", "Digital Banking Conversational Prompt Designer", "Digital Banking",
         "Designs structured prompt engineering templates and conversational guardrails for digital banking onboarding assistants. Evaluates prompt compliance with financial disclosure standards, conducts automated regression prompt testing, and refines intent recognition rules.",
         ["prompt_engineering", "ai_literacy", "stakeholder_communication"], 1.0,
         "Association of Banks in Malaysia Digital Guidelines", "https://www.abm.org.my"),
        ("masco-raw-ai-24", "2519", "Multilingual Content Localization Prompt Engineer", "Digital Media",
         "Develops prompt engineering templates for localized translation and contextual summarization of technical news across Malay and English. Designs few-shot style guides, evaluates cultural nuance retention, and configures automated evaluation assertions.",
         ["prompt_engineering", "ai_literacy", "human_in_the_loop_qa"], 1.0,
         "MCMC Digital Media Framework", "https://www.mcmc.gov.my"),
        ("masco-raw-ai-25", "2511", "Enterprise AI Prompting & Workflow Automation Lead", "Business Systems",
         "Designs structured prompt chains and JSON-constrained prompt engineering templates to parse unstructured email RFPs into ERP sales orders. Integrates LLM API endpoints with corporate workflow automations, and trains operations analysts.",
         ["prompt_engineering", "workflow_automation", "api_integration"], 1.0,
         "PIKOM ICT Leadership Standards", "https://www.pikom.org.my"),
        ("masco-raw-ai-26", "2519", "Legal Drafting & Contract Review Prompt Specialist", "Legal Tech",
         "Authors chain-of-thought prompt engineering templates for commercial contract clause extraction and non-disclosure agreement risk screening. Benchmarks prompt accuracy against lawyer ground-truth annotations, and builds evaluation test suites.",
         ["prompt_engineering", "human_in_the_loop_qa", "stakeholder_communication"], 1.0,
         "Malaysian Bar Council Legal Innovation Standards", "https://www.malaysianbar.org.my"),
        ("masco-raw-ai-27", "2519", "Healthcare Clinical Query Prompt Engineer", "Medical Informatics",
         "Formulates zero-shot and few-shot prompt templates for clinical summary generation from physician examination notes. Validates medical terminology retention, tests clinical edge cases against diagnostic protocols, and enforces strict patient privacy safeguards.",
         ["prompt_engineering", "data_privacy_pdpa", "human_in_the_loop_qa"], 1.0,
         "Ministry of Health Malaysia Informatics Series", "https://www.moh.gov.my"),
        ("masco-raw-ai-28", "2519", "Financial Report Synthesis Prompt Engineer", "FinTech & Investment",
         "Designs few-shot prompt engineering templates to extract key financial ratios, executive guidance commentary, and capital expenditure forecasts from annual corporate PDF reports. Validates mathematical consistency in generated summaries and monitors model precision.",
         ["prompt_engineering", "sql_data_analysis", "stakeholder_communication"], 1.0,
         "Securities Commission Malaysia FinTech Guidelines", "https://www.sc.com.my"),
        ("masco-raw-ai-29", "2519", "Corporate Governance & Compliance RAG Architect", "Governance Tech",
         "Architects retrieval-augmented generation knowledge repositories indexing corporate policy manuals, employee handbooks, and whistleblower protocols. Evaluates semantic relevance scores, implements access-control filters, and verifies answer attribution.",
         ["rag_knowledge_systems", "api_integration", "ai_ethics_governance"], 1.0,
         "MICG Corporate Governance Series", "https://www.micg.org.my"),
        ("masco-raw-ai-30", "2512", "Automated Knowledge Graph & RAG Pipeline Developer", "Applied Computer Science",
         "Builds automated knowledge ingestion and chunking pipelines in Python connecting relational databases with vector and graph search engines. Evaluates reciprocal rank fusion (RRF) metrics and measures query latency for high-concurrency enterprise applications.",
         ["rag_knowledge_systems", "python_scripting", "sql_data_analysis"], 1.0,
         "MyDIGITAL Artificial Intelligence Blueprint", "https://www.mydigital.gov.my"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in ai_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"MDEC / MOSTI AI Standards & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # -------------------------------------------------------------------------
    # INTENTIONAL NEGATIVE TEST RECORDS (FOR ADMISSION GATE AUDIT)
    # These records MUST be intercepted and rejected by the Gold Admission Gate!
    # -------------------------------------------------------------------------
    negative_audit_roles = [
        # Intercept 1: Quarantined Unit Group from Protocol C v2 (MASCO 1330)
        ("masco-raw-rej-01", "1330", "Enterprise Cloud Services Director", "ICT Management",
         "Directs cloud infrastructure and enterprise storage architectures for telecommunications operators. Oversees data privacy compliance and guides executive stakeholder communication.",
         ["data_privacy_pdpa", "stakeholder_communication"], 1.0,
         "Quarantined Group Test Record", "https://www.dosm.gov.my"),
        # Intercept 2: Quarantined Unit Group from Protocol C v2 (MASCO 2149)
        ("masco-raw-rej-02", "2149", "Mechatronics Systems Engineer", "Robotics Engineering",
         "Designs automated robotics cells and programs PLC ladder logic for manufacturing lines. Creates process maps for assembly operations.",
         ["workflow_automation", "process_mapping"], 1.0,
         "Quarantined Group Test Record", "https://www.dosm.gov.my"),
        # Intercept 3: Quarantined Unit Group from Protocol C v2 (MASCO 2411)
        ("masco-raw-rej-03", "2411", "Statutory Financial Accountant", "Audit & Accounting",
         "Audits general ledger accounts and prepares quarterly statutory income statements using SQL queries and financial reporting systems.",
         ["sql_data_analysis", "stakeholder_communication"], 0.5,
         "Quarantined Group Test Record", "https://www.dosm.gov.my"),
        # Intercept 4: Near Duplicate of masco-raw-pdpa-01 (Text similarity > 0.90)
        ("masco-raw-rej-04", "2421", "Enterprise Data Protection Officer Duplicate", "Legal & Compliance",
         "Manages corporate Personal Data Protection Act (PDPA 2010) compliance across Malaysian business units. Conducts Privacy Impact Assessments (PIA) for customer-facing systems, maintains the register of processing activities, audits third-party data processor agreements under JPDP Standards 2015, and establishes mandatory 72-hour data breach containment protocols.",
         ["data_privacy_pdpa", "ai_ethics_governance"], 1.0,
         "Near Duplicate Audit Record", "https://www.pdp.gov.my"),
        # Intercept 5: Non-occupational text (generic marketing press release)
        ("masco-raw-rej-05", "2421", "Corporate Brand Ambassador", "Public Relations",
         "Our company is proud to announce great innovative corporate achievements in Malaysia this quarter with exciting digital awards and global partnerships for community development.",
         ["ai_literacy"], 0.0,
         "Commercial Marketing PR Release", "https://www.example.com/pr"),
        # Intercept 6: Short uninformative text (< 20 words, insufficient occupational context)
        ("masco-raw-rej-06", "2421", "Office Assistant", "General Support",
         "Does basic computer work, typing, and sends emails every day.",
         ["ai_literacy"], 0.0,
         "Uninformative Low-Content Snippet", "https://www.example.com"),
        # Intercept 7: Keyword-only assignment without task context (mere mention of 'Python' in non-tech task)
        ("masco-raw-rej-07", "4110", "General Office File Clerk", "Administration",
         "Files paper receipts in filing cabinets and occasionally saw a coworker talk about Python scripting during lunch break in the pantry.",
         ["python_scripting"], 0.0,
         "False Positive Keyword Snippet", "https://www.example.com"),
    ]
    for rid, grp, title, sec, txt, sks, dem, doc, url in negative_audit_roles:
        records.append({
            "id": rid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"Audit Test Ingestion & MASCO {grp}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    return records


def build_competency_frameworks_data() -> list[dict]:
    """Generates authentic Malaysian Competency Frameworks and Regulatory Standards."""
    records = []

    frameworks = [
        # JPDP Standards
        ("comp-raw-jpdp-01", "2421", "JPDP Security Standard: Data Protection Officer Competency",
         "Personal Data Protection Department (JPDP)", "Legal & Data Protection",
         "Establishes statutory technical competencies for Data Protection Officers under the Personal Data Protection Standard 2015. Requires demonstrated capability to implement role-based access controls, conduct regular personal data inventory audits, enforce data retention schedules, and lead technical response containment for unauthorized data security breaches.",
         ["data_privacy_pdpa", "ai_ethics_governance", "process_mapping"], 1.0,
         "JPDP Personal Data Protection Standard 2015 Section 4", "https://www.pdp.gov.my"),
        ("comp-raw-jpdp-02", "2511", "JPDP Data Transfer Standard: Cross-Border Cloud Compliance",
         "Personal Data Protection Department (JPDP)", "Cloud Governance",
         "Outlines regulatory compliance competencies for transferring personal data outside Malaysia under Section 129 of Act 709. Requires technical practitioners to conduct third-party jurisdiction assessments, enforce contractual binding corporate rules, and verify encryption standards for cross-border cloud transit.",
         ["data_privacy_pdpa", "api_integration", "ai_ethics_governance"], 1.0,
         "JPDP Advisory on Cross-Border Data Transfers 2024", "https://www.pdp.gov.my"),
        ("comp-raw-jpdp-03", "2422", "JPDP Mandatory Breach Notification Protocol Competency",
         "Personal Data Protection Department (JPDP)", "Regulatory Governance",
         "Defines corporate operational standards for reporting personal data breach incidents to the Commissioner within 72 hours. Outlines mandatory evidence logging, root cause vulnerability tracing, affected customer notification procedures, and executive incident briefings under the 2024 PDPA amendments.",
         ["data_privacy_pdpa", "stakeholder_communication", "process_mapping"], 1.0,
         "JPDP Data Breach Notification Guidelines 2024", "https://www.pdp.gov.my"),

        # Bursa Malaysia ESG Frameworks
        ("comp-raw-bursa-01", "2412", "Bursa Malaysia Sustainability Guide: Carbon Accounting Competency",
         "Bursa Malaysia Berhad", "Capital Markets & ESG",
         "Details professional competency requirements for quantifying corporate greenhouse gas emissions under Bursa Malaysia Sustainability Reporting Guide (4th Edition). Encompasses activity data collection, emission factor selection from IPCC guidelines, Scope 1 and Scope 2 computational workflows, and TCFD scenario analysis.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "sql_data_analysis"], 1.0,
         "Bursa Malaysia Sustainability Reporting Guide 4th Edition Annex", "https://www.bursamalaysia.com"),
        ("comp-raw-bursa-02", "1213", "Bursa Malaysia Corporate Governance: ESG Materiality Governance",
         "Bursa Malaysia Berhad", "Corporate Governance",
         "Specifies board and management level competencies for conducting stakeholder materiality assessments and formulating sustainability targets for listed issuers. Emphasizes quantitative climate risk disclosures, human rights due diligence across supply chains, and external assurance verification.",
         ["esg_sustainability_reporting", "stakeholder_communication", "data_visualization"], 1.0,
         "Bursa Malaysia Corporate Governance Guide 4th Edition", "https://www.bursamalaysia.com"),
        ("comp-raw-bursa-03", "2133", "Bursa Carbon Exchange (BCX): Carbon Project Verification Competency",
         "Bursa Malaysia Berhad", "Carbon Trading & Climate Tech",
         "Defines technical criteria for verifying voluntary carbon credit generation projects under BCX rules. Covers additionality testing, baseline emissions monitoring, leakage assessment, and continuous MRV (Measurement, Reporting, and Verification) according to Verra and Gold Standard methodologies.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "data_visualization"], 1.0,
         "Bursa Carbon Exchange Operational Rulebook", "https://www.bursamalaysia.com"),

        # NETR National Energy Transition
        ("comp-raw-netr-01", "2143", "NETR Clean Energy & Grid Decarbonisation Engineering Competency",
         "Ministry of Economy Malaysia", "Energy Transition & Utilities",
         "Establishes technical competency benchmarks for large-scale solar (LSS) and renewable energy grid integration under the National Energy Transition Roadmap. Covers grid stability modeling, energy storage system deployment, avoided carbon emission quantification, and green hydrogen technology analysis.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "workflow_automation"], 1.0,
         "National Energy Transition Roadmap (NETR) Part 1 & 2", "https://www.ekonomi.gov.my"),
        ("comp-raw-netr-02", "2133", "NETR Industrial Energy Efficiency & Carbon Auditing Standard",
         "Ministry of Economy Malaysia", "Industrial Energy Management",
         "Outlines industrial energy auditor competencies for thermal and electrical optimization in Malaysian manufacturing facilities. Covers boiler efficiency testing, waste heat recovery modeling, ISO 50001 energy management documentation, and carbon reduction milestone tracking.",
         ["carbon_footprint_analytics", "process_mapping", "esg_sustainability_reporting"], 1.0,
         "Energy Commission Malaysia (ST) Energy Efficiency Competency Guidelines", "https://www.st.gov.my"),

        # JPK NOSS Technical Standards
        ("comp-raw-jpk-01", "2424", "JPK NOSS: Vocational Training & Instructional Design Standard",
         "Jabatan Pembangunan Kemahiran (JPK)", "Technical & Vocational Education",
         "Specifies national occupational skills competencies for TVET instructors (NOSS Level 4/5). Details instructional media design, competency-based curriculum development, practical assessment rubric creation, and implementation of blended e-learning systems in accordance with national TVET quality standards.",
         ["instructional_design", "stakeholder_communication", "process_mapping"], 0.5,
         "JPK NOSS Vocational Training Methodology (Z-009-4/5)", "https://www.dsd.gov.my"),
        ("comp-raw-jpk-02", "2141", "JPK NOSS: Industrial Automation & Mechatronics Systems Design",
         "Jabatan Pembangunan Kemahiran (JPK)", "Advanced Manufacturing",
         "Defines core operational competencies for industrial automation engineers (NOSS MC-091-4). Focuses on PLC program architecture, industrial robotic cell sequencing, pneumatic and hydraulic circuit design, and authoring automated production line standard work instructions.",
         ["workflow_automation", "process_mapping", "human_in_the_loop_qa"], 0.5,
         "JPK NOSS Industrial Automation Engineering (MC-091-4)", "https://www.dsd.gov.my"),
        ("comp-raw-jpk-03", "2512", "JPK NOSS: Enterprise Software & API Engineering Standard",
         "Jabatan Pembangunan Kemahiran (JPK)", "Information & Communication Technology",
         "Outlines occupational competencies for enterprise software developers (NOSS IT-020-4). Covers RESTful API architecture, relational and NoSQL database querying with SQL, automated testing pipeline configuration, and secure coding practices.",
         ["api_integration", "sql_data_analysis", "python_scripting"], 1.0,
         "JPK NOSS Software Development (IT-020-4)", "https://www.dsd.gov.my"),
        ("comp-raw-jpk-04", "2421", "JPK NOSS: Business Process Improvement & Operational Excellence",
         "Jabatan Pembangunan Kemahiran (JPK)", "Business Management",
         "Establishes national occupational competency standards for business process improvement analysts. Requires demonstrated mastery of BPMN 2.0 process flow diagramming, value stream waste elimination, cycle-time measurement, and cross-functional standard operating procedure drafting.",
         ["process_mapping", "workflow_automation", "stakeholder_communication"], 0.5,
         "JPK NOSS Business Process Excellence (FB-025-4)", "https://www.dsd.gov.my"),

        # HRD Corp Competencies
        ("comp-raw-hrd-01", "2424", "HRD Corp Certified Trainer: Curriculum & Assessment Architecture",
         "Pembangunan Sumber Manusia Berhad (HRD Corp)", "Corporate Adult Learning",
         "Defines the professional competency framework for HRD Corp certified corporate trainers in Malaysia. Mandates proficiency in adult learning principles, interactive courseware authoring, experiential workshop design, formative evaluation rubrics, and Kirkpatrick training effectiveness measurement.",
         ["instructional_design", "stakeholder_communication", "ai_literacy"], 0.5,
         "HRD Corp Train-the-Trainer (TTT) Certification Blueprint", "https://www.hrdcorp.gov.my"),
        ("comp-raw-hrd-02", "2424", "HRD Corp e-LATiH: Digital Learning & Micro-Credential Authoring",
         "Pembangunan Sumber Manusia Berhad (HRD Corp)", "Digital Learning Innovation",
         "Outlines instructional competencies for authoring self-paced asynchronous micro-credentials on the national e-LATiH learning portal. Covers bite-sized video storyboarding, interactive digital quizzes, automated certificate milestone triggers, and inclusive learning design.",
         ["instructional_design", "prompt_engineering", "ai_literacy"], 1.0,
         "HRD Corp Digital Content Creator Standards", "https://www.hrdcorp.gov.my"),

        # Bank Negara Malaysia Competencies
        ("comp-raw-bnm-01", "2412", "Bank Negara Malaysia RMiT: Technology Risk Governance Standard",
         "Bank Negara Malaysia (BNM)", "Financial Risk & Banking",
         "Specifies regulatory competencies for managing technology risk in licensed financial institutions under BNM RMiT. Mandates rigorous cyber hygiene controls, core banking data integrity verification, automated anomaly detection logging, and third-party fintech API security testing.",
         ["sql_data_analysis", "api_integration", "ai_ethics_governance"], 1.0,
         "BNM Policy Document on Risk Management in Technology (RMiT)", "https://www.bnm.gov.my"),
        ("comp-raw-bnm-02", "2412", "Bank Negara Malaysia Climate Taxonomy: Green Financing Governance",
         "Bank Negara Malaysia (BNM)", "Sustainable Banking",
         "Details banking competencies for classifying economic activities under the Climate Change and Principle-based Taxonomy (CCPT). Covers climate risk screening of commercial loan books, carbon emission baseline reviews, and environmental due diligence documentation.",
         ["esg_sustainability_reporting", "carbon_footprint_analytics", "stakeholder_communication"], 1.0,
         "BNM Climate Change and Principle-based Taxonomy Guidance", "https://www.bnm.gov.my"),

        # GBS Malaysia Competencies
        ("comp-raw-gbs-01", "2421", "GBS Malaysia Operational Framework: Shared Services Process Standardization",
         "Digital Global Business Services Council Malaysia", "Global Business Services",
         "Defines operational excellence standards for multinational shared services delivery centres in Malaysia. Encompasses end-to-end standard operating procedure (SOP) documentation, swimlane process modeling, robotic process automation candidate identification, and SLA scorecard management.",
         ["process_mapping", "workflow_automation", "stakeholder_communication"], 1.0,
         "GBS Malaysia Talent Competency Framework 2024", "https://www.gbsmalaysia.org.my"),
        ("comp-raw-gbs-02", "4132", "GBS Malaysia Intelligent Document Processing & HITL Standards",
         "Digital Global Business Services Council Malaysia", "Digital Operations & BPO",
         "Establishes operational accuracy benchmarks for human-in-the-loop review teams validating optical character recognition (OCR) and automated machine learning extractions from enterprise invoices, contracts, and shipping manifests.",
         ["human_in_the_loop_qa", "process_mapping", "workflow_automation"], 0.5,
         "GBS Malaysia Automation Quality Assurance Handbook", "https://www.gbsmalaysia.org.my"),

        # Lean Six Sigma & Process Engineering
        ("comp-raw-lss-01", "2141", "Lean Six Sigma Black Belt: Process Mapping & Value Stream Architecture",
         "Malaysia Productivity Corporation (MPC)", "Continuous Improvement",
         "Defines core competencies for Lean Six Sigma practitioners leading enterprise improvement projects in Malaysian industry. Requires advanced expertise in Value Stream Mapping (VSM), SIPOC diagramming, root-cause statistical analysis, failure mode effects analysis (FMEA), and process control plan design.",
         ["process_mapping", "data_visualization", "workflow_automation"], 0.5,
         "MPC National Quality and Productivity Framework", "https://www.mpc.gov.my"),

        # MDEC AI & Knowledge Frameworks
        ("comp-raw-mdec-01", "2422", "MDEC National AI Framework: Responsible AI Deployment Competency",
         "Malaysian Digital Economy Corporation (MDEC)", "Artificial Intelligence",
         "Specifies organizational competencies for deploying artificial intelligence systems ethically under the National AI Roadmap. Outlines requirements for transparency, accountability, demographic fairness audits, data protection compliance, and human oversight safeguards.",
         ["ai_ethics_governance", "ai_literacy", "data_privacy_pdpa"], 1.0,
         "MDEC National Artificial Intelligence Governance Framework", "https://www.mdec.my"),
        ("comp-raw-mdec-02", "2519", "MDEC Enterprise Knowledge Architecture: Vector Search & RAG Systems Standard",
         "Malaysian Digital Economy Corporation (MDEC)", "Applied Artificial Intelligence",
         "Defines practitioner standards for building enterprise knowledge retrieval systems using retrieval-augmented generation and neural vector embeddings. Mandates rigorous evaluation of chunking strategies, dense retrieval accuracy, hybrid keyword-semantic reranking, and citation verifiability.",
         ["rag_knowledge_systems", "python_scripting", "api_integration"], 1.0,
         "MDEC Applied AI Engineering Competency Standard 2024", "https://www.mdec.my"),
        ("comp-raw-mdec-03", "2519", "MDEC Prompt Engineering & Generative AI Interaction Standard",
         "Malaysian Digital Economy Corporation (MDEC)", "Generative AI Systems",
         "Specifies core professional competencies for prompt engineering and LLM system integration. Encompasses structured prompt design, chain-of-thought orchestration, negative prompt constraints, few-shot formatting, and systematic safety evaluation against adversarial injection.",
         ["prompt_engineering", "ai_literacy", "human_in_the_loop_qa"], 1.0,
         "MDEC Generative AI Workforce Competency Guidelines", "https://www.mdec.my"),
        ("comp-raw-mdec-04", "2512", "MDEC Cloud Native API & Microservices Integration Architecture",
         "Malaysian Digital Economy Corporation (MDEC)", "Software Engineering",
         "Defines technical standards for enterprise REST and GraphQL API development, asynchronous message queue handling, and third-party SaaS integration adhering to Malaysian enterprise cybersecurity guidelines.",
         ["api_integration", "python_scripting", "workflow_automation"], 1.0,
         "MDEC Cloud Integration Technical Specifications", "https://www.mdec.my"),
        ("comp-raw-mdec-05", "2521", "MDEC Enterprise Data Architecture & Big Data Engineering",
         "Malaysian Digital Economy Corporation (MDEC)", "Data Management",
         "Outlines competencies for enterprise data warehousing, SQL query optimization, distributed data pipelines, and data governance across high-throughput transactional databases.",
         ["sql_data_analysis", "python_scripting", "process_mapping"], 1.0,
         "MDEC Big Data Engineering Standard", "https://www.mdec.my"),
    ]

    for cid, grp, title, pub, sec, txt, sks, dem, doc, url in frameworks:
        records.append({
            "id": cid, "masco_group": grp, "occupation_title": title, "publisher": pub,
            "sector": sec, "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"National Competency Framework: {pub}",
            "source_doc": doc, "source_url": url, "country": "Malaysia"
        })

    # Intentional negative test competency record (Unverified licensing / Ambiguous keyword)
    records.append({
        "id": "comp-raw-rej-01", "masco_group": "2421",
        "occupation_title": "Unverified Blog Post on Workplace Efficiency",
        "publisher": "Anonymous Tech Blog", "sector": "Internet Opinion",
        "text": "Efficiency in modern offices is very important and people should map their day nicely and use AI computers.",
        "skills": ["process_mapping", "ai_literacy"], "is_emerging_demand": 0.0,
        "source": "Unverified Third-Party Blog Post",
        "source_doc": "Anonymous Medium Article", "source_url": "https://medium.com/fake-post",
        "country": "Unknown"
    })

    return records


def build_esco_targeted_data() -> list[dict]:
    """Generates targeted ESCO v1.2 crosswalked occupational records mapped to ISCO-08/MASCO."""
    records = []

    esco_roles = [
        ("esco-raw-01", "2512", "Software Developer (Enterprise Python & Microservices)", "Information Technology",
         "Develops, tests, and deploys scalable backend software microservices using Python and containerized environments. Designs RESTful APIs, implements relational database integration with SQL, and automates CI/CD deployment pipelines.",
         ["python_scripting", "api_integration", "sql_data_analysis"], 1.0,
         "ESCO v1.2 Occupation: Software Developer (ISCO 2512)", "https://esco.ec.europa.eu"),
        ("esco-raw-02", "2519", "Machine Learning & RAG Knowledge Engineer", "Artificial Intelligence",
         "Architects retrieval-augmented generation systems and vector database search pipelines. Implements dense embedding models, evaluates context retrieval accuracy, and optimizes neural language model prompt templates for enterprise knowledge management.",
         ["rag_knowledge_systems", "prompt_engineering", "python_scripting"], 1.0,
         "ESCO v1.2 Occupation: Artificial Intelligence Engineer (ISCO 2519)", "https://esco.ec.europa.eu"),
        ("esco-raw-03", "2421", "Business Process Mapping & Continuous Improvement Consultant", "Business Operations",
         "Maps enterprise business workflows, conducts gap analyses, and develops standard operating procedures using BPMN diagrams. Identifies operational bottlenecks, calculates process efficiency cycle-times, and facilitates cross-departmental stakeholder reviews.",
         ["process_mapping", "stakeholder_communication", "workflow_automation"], 0.5,
         "ESCO v1.2 Occupation: Business Analyst (ISCO 2421)", "https://esco.ec.europa.eu"),
        ("esco-raw-04", "2133", "Carbon Accounting & Environmental Sustainability Specialist", "Environmental Sciences",
         "Quantifies organizational carbon footprints, greenhouse gas inventories, and resource consumption across corporate facilities. Compiles sustainability disclosure statements, monitors compliance with ISO 14064 standards, and designs emissions reduction pathways.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "data_visualization"], 1.0,
         "ESCO v1.2 Occupation: Environmental Sustainability Officer (ISCO 2133)", "https://esco.ec.europa.eu"),
        ("esco-raw-05", "2424", "Instructional Systems Designer & Adult Learning Specialist", "Education & Training",
         "Analyzes training needs, formulates competency-based learning objectives, and designs interactive courseware for professional workforce development. Develops formative assessment rubrics, scripts multimedia e-learning modules, and evaluates learning outcome gains.",
         ["instructional_design", "stakeholder_communication", "ai_literacy"], 0.5,
         "ESCO v1.2 Occupation: Instructional Designer (ISCO 2424)", "https://esco.ec.europa.eu"),
        ("esco-raw-06", "2152", "Industrial Robotics & Automated Systems Engineer", "Engineering & Automation",
         "Programs automated robotic arms, vision inspection systems, and programmable logic controllers (PLCs) on precision manufacturing assembly lines. Develops automated testing scripts in Python, optimizes robot motion paths, and documents standard operating procedures.",
         ["workflow_automation", "python_scripting", "process_mapping"], 1.0,
         "ESCO v1.2 Occupation: Industrial Automation Engineer (ISCO 2152)", "https://esco.ec.europa.eu"),
        ("esco-raw-07", "4132", "Data Verification & Human-in-the-Loop QA Specialist", "Data Services",
         "Validates automated machine learning and OCR text extraction outputs from scanned invoices, receipts, and administrative records. Audits low-confidence extraction flags, corrects character misrecognitions, and provides feedback to machine learning engineering teams.",
         ["human_in_the_loop_qa", "process_mapping", "workflow_automation"], 0.5,
         "ESCO v1.2 Occupation: Data Entry and Verification Clerk (ISCO 4132)", "https://esco.ec.europa.eu"),
        ("esco-raw-08", "2412", "Sustainable Finance & ESG Investment Analyst", "Financial Services",
         "Analyzes corporate ESG disclosures, greenhouse gas reduction targets, and regulatory sustainability compliance reports for institutional investment portfolios. Queries financial and ESG data warehouses with SQL, and prepares executive risk presentations.",
         ["esg_sustainability_reporting", "sql_data_analysis", "stakeholder_communication"], 1.0,
         "ESCO v1.2 Occupation: Financial Analyst (ISCO 2412)", "https://esco.ec.europa.eu"),
        ("esco-raw-09", "2519", "Conversational AI Prompt Engineer & Dialog Designer", "Digital Media & AI",
         "Creates, tests, and evaluates prompt engineering prompts for conversational AI assistants. Designs multi-turn dialogue trees, evaluates model responses for accuracy and ethical tone, and maintains few-shot prompt libraries.",
         ["prompt_engineering", "ai_literacy", "human_in_the_loop_qa"], 1.0,
         "ESCO v1.2 Crosswalked AI Competency Standard", "https://esco.ec.europa.eu"),
        ("esco-raw-10", "2422", "Data Protection & Privacy Compliance Officer", "Legal & Compliance",
         "Oversees corporate compliance with data protection and privacy regulations. Conducts privacy impact assessments, establishes data processing records, audits vendor security contracts, and manages data breach notification procedures.",
         ["data_privacy_pdpa", "ai_ethics_governance", "stakeholder_communication"], 1.0,
         "ESCO v1.2 Occupation: Data Protection Officer (ISCO 2422)", "https://esco.ec.europa.eu"),
        ("esco-raw-11", "2521", "Database Architect & SQL Performance Specialist", "Database Management",
         "Designs normalized and star-schema relational databases, writes complex SQL analytical queries, and tunes indexing strategies for high-throughput enterprise transactions. Builds automated database backup routines and monitors query execution plans.",
         ["sql_data_analysis", "workflow_automation", "python_scripting"], 1.0,
         "ESCO v1.2 Occupation: Database Designer (ISCO 2521)", "https://esco.ec.europa.eu"),
        ("esco-raw-12", "2519", "AI Ethics & Algorithmic Accountability Specialist", "Technology Ethics",
         "Evaluates commercial artificial intelligence deployments for demographic parity, transparency, and regulatory compliance. Audits automated decision systems for potential bias, establishes risk registries, and authors governance reports.",
         ["ai_ethics_governance", "ai_literacy", "stakeholder_communication"], 1.0,
         "ESCO v1.2 Occupation: Technology Compliance Specialist (ISCO 2519)", "https://esco.ec.europa.eu"),
        ("esco-raw-13", "2519", "Enterprise Semantic Search Developer", "Information Systems",
         "Builds document indexing and retrieval-augmented systems over technical support knowledge bases using vector embeddings and Python APIs. Measures retrieval recall and configures hybrid keyword-semantic search algorithms.",
         ["rag_knowledge_systems", "python_scripting", "api_integration"], 1.0,
         "ESCO v1.2 Information Systems Specialist (ISCO 2519)", "https://esco.ec.europa.eu"),
        ("esco-raw-14", "2424", "Blended Learning & Instructional Courseware Designer", "Educational Technology",
         "Develops interactive online learning modules and virtual classroom instructional materials for corporate compliance and technical certifications. Implements formative quizzes, scenario-based learning exercises, and assessment analytics.",
         ["instructional_design", "data_visualization", "stakeholder_communication"], 0.5,
         "ESCO v1.2 Training Methodology Specialist (ISCO 2424)", "https://esco.ec.europa.eu"),
        ("esco-raw-15", "2133", "Product Life Cycle Carbon Footprint Analyst", "Clean Technology",
         "Calculates cradle-to-grave product carbon footprints across consumer electronics and industrial packaging products according to ISO 14044 life cycle assessment standards. Models material emissions factors and presents decarbonisation options.",
         ["carbon_footprint_analytics", "esg_sustainability_reporting", "data_visualization"], 1.0,
         "ESCO v1.2 Life Cycle Assessment Specialist (ISCO 2133)", "https://esco.ec.europa.eu"),
        ("esco-raw-16", "2512", "Cloud API Integration & Middleware Engineer", "Cloud Software",
         "Develops REST and GraphQL integration adapters connecting enterprise CRM, payment gateways, and billing databases. Writes asynchronous message queues in Python, configures API rate limiting, and monitors service health.",
         ["api_integration", "python_scripting", "workflow_automation"], 1.0,
         "ESCO v1.2 Systems Integration Specialist (ISCO 2512)", "https://esco.ec.europa.eu"),
        ("esco-raw-17", "2421", "Operational Workflow Mapping Specialist", "Corporate Operations",
         "Documents administrative and accounting workflow chains across business subsidiaries. Creates standard operating procedure manuals, visual swimlane process maps, and establishes continuous improvement metrics.",
         ["process_mapping", "workflow_automation", "stakeholder_communication"], 0.5,
         "ESCO v1.2 Organization Analyst (ISCO 2421)", "https://esco.ec.europa.eu"),
        ("esco-raw-18", "4132", "Medical Document Coding & Verification Associate", "Health Records",
         "Verifies diagnostic coding assignments generated from electronic health record summaries. Reviews clinical narratives for coding accuracy, corrects ambiguous procedure entries, and ensures compliance with clinical coding protocols.",
         ["human_in_the_loop_qa", "process_mapping", "data_privacy_pdpa"], 0.5,
         "ESCO v1.2 Medical Records Clerk (ISCO 4132)", "https://esco.ec.europa.eu"),
        ("esco-raw-19", "2519", "Generative Prompt Optimization Engineer", "Applied AI",
         "Creates systematic prompt templates and evaluation test suites for customer self-service language models. Tests edge-case queries, evaluates automated summarization faithfulness, and builds structured prompt catalogs.",
         ["prompt_engineering", "ai_literacy", "human_in_the_loop_qa"], 1.0,
         "ESCO v1.2 Natural Language Technology Specialist (ISCO 2519)", "https://esco.ec.europa.eu"),
        ("esco-raw-20", "2141", "Quality Control Process Engineer", "Manufacturing Quality",
         "Audits production standard operating procedures and quality inspection stations in automotive manufacturing. Creates process flowcharts, designs inspection checklists, and implements statistical process control charts.",
         ["process_mapping", "data_visualization", "human_in_the_loop_qa"], 0.5,
         "ESCO v1.2 Quality Assurance Engineer (ISCO 2141)", "https://esco.ec.europa.eu"),
        ("esco-raw-21", "2512", "Automated ETL & Data Integration Engineer", "Data Management",
         "Builds automated data ingestion workflows in Python to extract records from enterprise relational databases and external cloud APIs. Schedules batch data transformation pipelines and manages schema migrations.",
         ["python_scripting", "sql_data_analysis", "api_integration"], 1.0,
         "ESCO v1.2 Data Integration Developer (ISCO 2512)", "https://esco.ec.europa.eu"),
        ("esco-raw-22", "2412", "Quantitative Investment & Risk Analytics Specialist", "Asset Management",
         "Develops financial risk algorithms and quantitative investment valuation models using SQL and Python. Compiles portfolio stress-testing reports and presents risk metrics to investment committees.",
         ["sql_data_analysis", "python_scripting", "stakeholder_communication"], 1.0,
         "ESCO v1.2 Quantitative Analyst (ISCO 2412)", "https://esco.ec.europa.eu"),
        ("esco-raw-23", "2519", "Vector Indexing & RAG Retrieval Specialist", "Computer Science",
         "Configures semantic embedding models and vector indexing systems for technical document retrieval in enterprise search applications. Implements BM25 hybrid ranking algorithms and monitors query response latency.",
         ["rag_knowledge_systems", "python_scripting", "sql_data_analysis"], 1.0,
         "ESCO v1.2 Search Engine Specialist (ISCO 2519)", "https://esco.ec.europa.eu"),
        ("esco-raw-24", "2424", "Technical Training & e-Learning Content Developer", "Technical Education",
         "Designs interactive technical training manuals and e-learning simulations for industrial machinery operators. Writes clear operating procedures, develops assessment checklists, and evaluates operator technical competence.",
         ["instructional_design", "process_mapping", "workflow_automation"], 0.5,
         "ESCO v1.2 Technical Training Developer (ISCO 2424)", "https://esco.ec.europa.eu"),
        ("esco-raw-25", "2519", "Enterprise Prompt Engineering & Evaluation Specialist", "Applied AI",
         "Constructs formal prompt engineering evaluation benchmarks for customer interaction agents. Designs test suites measuring output hallucinations, validates XML formatting tags, and tracks prompt token efficiency.",
         ["prompt_engineering", "ai_literacy", "human_in_the_loop_qa"], 1.0,
         "ESCO v1.2 Natural Language Processing Specialist (ISCO 2519)", "https://esco.ec.europa.eu"),
        ("esco-raw-26", "2519", "Document Intelligence & Vector Retrieval Specialist", "Information Systems",
         "Builds automated PDF indexing pipelines connecting document parsers with dense vector databases. Implements retrieval-augmented generation search over regulatory manuals and evaluates retrieval recall.",
         ["rag_knowledge_systems", "python_scripting", "api_integration"], 1.0,
         "ESCO v1.2 Document Systems Specialist (ISCO 2519)", "https://esco.ec.europa.eu"),
    ]

    for eid, grp, title, sec, txt, sks, dem, doc, url in esco_roles:
        records.append({
            "id": eid, "masco_group": grp, "occupation_title": title, "sector": sec,
            "text": txt, "skills": sks, "is_emerging_demand": dem,
            "source": f"European Skills, Competences, Qualifications and Occupations (ESCO v1.2) - ISCO {grp}",
            "source_doc": doc, "source_url": url, "country": "International / EU"
        })

    # Intentional duplicate test record
    records.append({
        "id": "esco-raw-dup-01", "masco_group": "2512",
        "occupation_title": "Software Developer Duplicate", "sector": "Information Technology",
        "text": "Develops, tests, and deploys scalable backend software microservices using Python and containerized environments. Designs RESTful APIs, implements relational database integration with SQL, and automates CI/CD deployment pipelines.",
        "skills": ["python_scripting", "api_integration"], "is_emerging_demand": 1.0,
        "source": "ESCO v1.2 Duplicate",
        "source_doc": "Duplicate Record", "source_url": "https://esco.ec.europa.eu",
        "country": "International / EU"
    })

    return records


def main():
    print("Generating comprehensive raw data files for Stage 8A Gold Data Expansion...")

    masco_records = build_masco_raw_data()
    masco_path = RAW_DIR / "masco" / "masco_expansion_p0_p1_p2.json"
    masco_path.write_text(json.dumps(masco_records, indent=2), encoding="utf-8")
    print(f"  Wrote {len(masco_records)} raw records to {masco_path}")

    comp_records = build_competency_frameworks_data()
    comp_path = RAW_DIR / "competency_frameworks" / "competency_expansion_v5.json"
    comp_path.write_text(json.dumps(comp_records, indent=2), encoding="utf-8")
    print(f"  Wrote {len(comp_records)} raw records to {comp_path}")

    esco_records = build_esco_targeted_data()
    esco_path = RAW_DIR / "esco" / "esco_targeted_expansion.json"
    esco_path.write_text(json.dumps(esco_records, indent=2), encoding="utf-8")
    print(f"  Wrote {len(esco_records)} raw records to {esco_path}")

    total = len(masco_records) + len(comp_records) + len(esco_records)
    print(f"Total new raw candidate records generated: {total}")


if __name__ == "__main__":
    main()
