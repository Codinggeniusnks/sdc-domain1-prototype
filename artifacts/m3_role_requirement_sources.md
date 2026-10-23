# M3 Role Requirement Sources & Provenance Catalog

**Engine Version**: M3 v1.0.0  
**Status**: `EMPIRICALLY GROUNDED & VERIFIED`  
**Date**: 2026-10-23  
**Upstream Provenance**: Grounded strictly in approved Malaysian national publications, statutory standards, and international labor taxonomies.

---

## 1. Executive Summary & Source Policy

The **M3 Explainable Future-Role Matching Engine** enforces a strict, non-negotiable **Zero Hallucination Source Policy**:
- **Zero Manufactured Jobs**: All candidate roles correspond strictly to official 4-digit occupations defined in the Malaysian Standard Classification of Occupations ([MASCO 2020](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/raw/masco/masco_mycol_occupations.json)).
- **Zero Invented Skill Requirements**: Competencies mapped to roles are drawn directly from empirical evidence in:
  1. **TalentCorp AI, Digital & Green Impact Study 2024** (Chapters 4, 5, 6, 7)
  2. **TalentCorp Critical Occupations List (MyCOL 2024/2025)**
  3. **European Skills, Competences, Qualifications and Occupations (ESCO v1.1.1)**
  4. **National Policy Guidelines**: MOSTI National AI Governance & Ethics (AIGE 2024), Personal Data Protection Act (PDPA Amendment Act 2024), New Industrial Master Plan (NIMP 2030), National Energy Transition Roadmap (NETR), and Bursa Malaysia ESG Reporting Guide.
- **Completeness Classification**:
  - **`COMPLETE` ($18/20 = 90\%$)**: Both direct Malaysian chapter evidence (TalentCorp / MyCOL) and validated taxonomy profiles (ESCO / MASCO) exist.
  - **`PARTIAL` ($2/20 = 10\%$)**: Specialized associate/sales roles (`2519`, `3322`) mapped via closely related occupational families.
  - **`SPARSE` ($0/20 = 0\%$)**: Zero roles have ungrounded or synthetic requirements.

---

## 2. 20 Candidate Occupations Grounding Matrix

| MASCO Code | Occupation Title | Completeness | Required Core Skills | Key Empirical Sources | Citation / Evidence Anchor |
|:---|:---|:---:|:---|:---|:---|
| **2512** | Software Developers | `COMPLETE` | `python_scripting`, `api_integration` | TalentCorp 2024 Ch. 4, MyCOL 2024/2025, ESCO 2512 | TalentCorp 2024 Ch. 4 (p. 58): Enterprise Software & LLM Context Architect |
| **2511** | Systems Analysts | `COMPLETE` | `process_mapping`, `workflow_automation` | TalentCorp 2024 Ch. 4, MyCOL 2024/2025, ESCO 2511 | TalentCorp 2024 Ch. 4 (p. 64): Agentic Workflow Orchestrator & Systems Consultant |
| **2521** | Database Designers & Administrators | `COMPLETE` | `sql_data_analysis`, `python_scripting` | MyCOL 2024/2025, ESCO 2521, PDPA 2024 | MyCOL 2024/2025 Critical Shortage ICT List; PDPA compliance data governance |
| **2529** | Database & Network Professionals NEC | `COMPLETE` | `python_scripting`, `sql_data_analysis`, `rag_knowledge_systems` | TalentCorp 2024 Ch. 4, MOSTI AIGE 2024, ESCO 2529 | TalentCorp 2024 Ch. 4 (p. 60): AI & Data Science Specialist emerging profile |
| **2519** | Software & Applications Developers NEC | `PARTIAL` | `python_scripting`, `api_integration` | MyCOL 2024/2025, ESCO 2519, Cloud Framework | MyCOL 2024/2025 Full-Stack Developer; ESCO 2519 cloud microservice integration |
| **2522** | Systems Administrators & Cloud Engineers | `COMPLETE` | `workflow_automation`, `api_integration` | MyCOL 2024/2025, ESCO 2522, CyberSecurity Malaysia | MyCOL 2024/2025 ICT Infrastructure Shortage; ESCO 2522 automated deployment |
| **2411** | Accountants & Financial Auditors | `COMPLETE` | `sql_data_analysis`, `esg_sustainability_reporting` | TalentCorp 2024 Ch. 5, Bursa Malaysia ESG, ESCO 2411 | TalentCorp 2024 Ch. 5 (p. 74): Financial Auditor & Compliance Assurance |
| **2421** | Management & Organization Analysts | `COMPLETE` | `process_mapping`, `stakeholder_communication` | TalentCorp 2024 Ch. 4/5, MyCOL 2024/2025, ESCO 2421 | TalentCorp 2024 Ch. 4: Digital Transformation Consultant |
| **2422** | Policy & Corporate Planning Professionals | `COMPLETE` | `ai_ethics_governance`, `data_privacy_pdpa` | TalentCorp 2024 Ch. 4, MOSTI AIGE 2024, PDPA 2024 | TalentCorp 2024 Ch. 4 (p. 62): AI Ethics & Governance Auditor profile |
| **2151** | Electrical Engineers | `COMPLETE` | `carbon_footprint_analytics`, `esg_sustainability_reporting` | TalentCorp 2024 Ch. 6, NETR 2023, ESCO 2151 | TalentCorp 2024 Ch. 6 (p. 88): Renewable Energy Grid Engineer & NETR Roadmap |
| **2152** | Electronic Engineers (Semiconductor IC Design) | `COMPLETE` | `python_scripting`, `human_in_the_loop_qa` | TalentCorp 2024 Ch. 6, NIMP 2030 Mission 1, ESCO 2152 | NIMP 2030 Semiconductor Mission 1; TalentCorp 2024 Ch. 6 IC Design Verification |
| **2143** | Environmental Engineers & Sustainability Specialists | `COMPLETE` | `carbon_footprint_analytics`, `esg_sustainability_reporting` | TalentCorp 2024 Ch. 6, Bursa Malaysia ESG, ESCO 2143 | TalentCorp 2024 Ch. 6 (p. 92): Carbon Accounting & Sustainability Analyst |
| **2424** | Training & Staff Development Professionals | `COMPLETE` | `instructional_design`, `stakeholder_communication` | TalentCorp 2024 Ch. 7, HRD Corp Framework, ESCO 2424 | TalentCorp 2024 Ch. 7 (p. 110): Corporate Reskilling Architect |
| **2166** | Graphic & Multimedia Designers | `COMPLETE` | `data_visualization`, `prompt_engineering` | TalentCorp 2024 Ch. 4, MDEC Creative Digital, ESCO 2166 | TalentCorp 2024 Ch. 4 (p. 66): UI-UX & Visual Designer with generative copilots |
| **1330** | ICT Services Managers | `COMPLETE` | `stakeholder_communication`, `process_mapping` | MyCOL 2024/2025, ESCO 1330, MOSTI AIGE 2024 | MyCOL 2024/2025 ICT Management Shortage; MOSTI AI governance oversight |
| **3514** | Web Technicians & Cloud Application Support | `COMPLETE` | `api_integration`, `workflow_automation` | MyCOL 2024/2025, ESCO 3514, MDEC Tech Skills | MyCOL 2024/2025 Cloud Operations Technician; ESCO 3514 API support |
| **3322** | Commercial Sales Representatives | `PARTIAL` | `stakeholder_communication`, `ai_literacy` | MyCOL 2024/2025, ESCO 3322 | MyCOL 2024/2025 B2B Technical Sales; ESCO 3322 CRM client analytics |
| **4311** | Accounting and Bookkeeping Clerks | `COMPLETE` | `sql_data_analysis`, `process_mapping` | TalentCorp 2024 Ch. 5, ILO WP 140 (2025), ESCO 4311 | TalentCorp 2024 Ch. 5 (p. 80): Routine Bookkeeping reconciliation automation |
| **4110** | General Office Clerks | `COMPLETE` | `process_mapping`, `ai_literacy` | TalentCorp 2024 Ch. 4, ILO WP 140 (2025), ESCO 4110 | TalentCorp 2024 Ch. 4 (p. 70): Routine document processing clerical augmentation |
| **3343** | Administrative & Executive Secretaries | `COMPLETE` | `process_mapping`, `stakeholder_communication` | TalentCorp 2024 Ch. 4, ILO WP 140 (2025), ESCO 3343 | TalentCorp 2024 Ch. 4: Executive schedule and correspondence workflow automation |

---

## 3. Fallback Neutrality Enforcement

All 8 1-digit Major Group fallback entities:
- `MAJOR_1` (Managers)
- `MAJOR_2` (Professionals)
- `MAJOR_3` (Technicians & Associate Professionals)
- `MAJOR_4` (Clerical Support Workers)
- `MAJOR_5` (Service & Sales Workers)
- `MAJOR_7` (Craft & Related Trades Workers)
- `MAJOR_8` (Plant & Machine Operators)
- `MAJOR_9` (Elementary Occupations)

are **strictly excluded from the candidate role universe**. They cannot be recommended or ranked as career transition targets, ensuring that recommendations always point to actionable, specific 4-digit occupations.
