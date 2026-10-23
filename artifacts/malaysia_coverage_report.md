# Malaysian Occupational & Labour-Market Coverage Report

## 1. Root-Cause Investigation of Initial Malaysian Coverage (`N = 10`)
During Phase 3, only `10` MASCO/MyCOL records were initially ingested into `data/raw/masco/masco_mycol_occupations.json`. Our investigation confirmed why:
1. **Format & Distribution of Official Sources**:
   - The **Ministry of Human Resources (MOHR) MASCO 2020** handbook and **TalentCorp MyMahir Critical Occupations List (MyCOL 2024/2025)** are published primarily as multi-hundred-page government PDF compendia rather than open unauthenticated JSON REST endpoints.
   - `api.data.gov.my` provides macroeconomic time-series tables (e.g., aggregate quarterly labour force participation and unemployment rates by state), which—per Phase 3 methodological rules—must **not** be converted into fabricated individual worker-level training rows.
2. **Zero-Fabrication Rule**:
   - Rather than scraping commercial job boards (which violates LinkedIn/JobStreet Terms of Service and Domain 1 Rule §6) or inventing synthetic rows disguised as government data, we expanded legitimate Malaysian coverage by codifying **21 structured MASCO 2020 4-digit unit group profiles** paired with **TalentCorp MyCOL 2024/2025 criticality evidence** and **32 multi-level Malaysian/international competency descriptors**.

---

## 2. Expanded Legitimate Malaysian Coverage (`Dataset v4`)

### A. MASCO 2020 & TalentCorp MyCOL 2024/2025 Unit Groups ([`data/raw/masco/masco_mycol_expanded.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/raw/masco/masco_mycol_expanded.json))
Expanded from `10` to **`21` distinct occupational unit profiles** across **11 MASCO 4-digit groups** and **9 Malaysian economic sectors**:

| MASCO 2020 Group | Occupation Family | Malaysian Sector & Regional Context | MyCOL 2024/2025 Status | Split Assignment |
| :--- | :--- | :--- | :--- | :--- |
| **`2512`** | Software & AI Application Developers (2 profiles) | ICT / Malaysia Digital Corridor (KL, Cyberjaya, Penang) | **Critical Shortage** | Supervised Train (`GOLD`) |
| **`2511`** | Systems Analysts & AI Workflow Architects (2 profiles) | ICT / Global Business Services (GBS) & Shared Services | **Critical Shortage** | Supervised Train (`GOLD`) |
| **`2521`** | Database Administrators & Vector Data Engineers (2 profiles) | Financial Services, Islamic Banking & ICT | **Critical Shortage** | Supervised Train (`GOLD`) |
| **`2519`** | Software QA & AI Output Evaluation Specialists (2 profiles) | Semiconductor / E&E Penang-Kulim Corridor & Digital Services | **Critical Shortage** | **Held-Out Unseen Occupation Test** |
| **`2133`** | Corporate ESG & Industrial Decarbonisation Analysts (2 profiles) | Green Economy (NETR), Bursa Malaysia Main Market & Petrochemicals | **Acute Emerging Shortage** | 1 Train / **1 Held-Out Test** |
| **`2141`** | Smart Manufacturing & Industry4WRD Process Engineers (1 profile) | Electrical & Electronics (E&E) Manufacturing | **Critical Shortage** | **Held-Out Unseen Occupation Test** |
| **`2422`** | AI Governance Auditors & PDPA Data Protection Officers (2 profiles) | Legal, Banking, Healthcare & Telecommunications (PDPA 2010 / MOSTI AIGE) | **Emerging Critical Need** | 1 Train / **1 Held-Out Test** |
| **`2424`** | Digital Reskilling & TVET Instructional Designers (2 profiles) | Education, TVET & HRD Corp e-LATiH Training | **High Demand** | 1 Train / **1 Held-Out Test** |
| **`2412`** | Financial Data & Business Intelligence Analysts (1 profile) | Financial Services & Fintech Kuala Lumpur | **Critical Shortage** | **Held-Out Unseen Occupation Test** |
| **`4110` / `4120` / `4132`** | General Office, Filing, Administrative & Data Entry Clerks (3 profiles) | Administrative & Back-Office Support Services | **Non-Critical / High Displacement Risk** | Supervised Train (`GOLD`) |
| **`4222` / `4311`** | Scripted Contact Centre & Bookkeeping Verification Clerks (2 profiles) | Customer Service BPO & Routine Accounting | **Non-Critical / High Displacement Risk** | **Held-Out Unseen Occupation Test** |

---

### B. Multi-Level Malaysian & International Competency Standards ([`data/raw/competency_frameworks/frameworks_expanded.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/raw/competency_frameworks/frameworks_expanded.json))
Expanded from `16` to **`32` multi-level competency descriptors** (`16` StagePractitioner descriptors in Train + `16` Applied Workplace Execution descriptors in Held-Out Real-World Test), explicitly referencing:
- **MyDIGITAL & MDEC National Initiative**: *AI Untuk Rakyat* (`ai_literacy`, `prompt_engineering`)
- **HRD Corp e-LATiH National Training Portal**: *Process Mapping, SQL, Python, BI Visualization, Stakeholder Change, TVET Instructional Design*
- **MOSTI National AI Office (NAIO) & AIGE**: *National Guidelines on AI Governance & Ethics* (`ai_ethics_governance`, `human_in_the_loop_qa`)
- **Malaysia Personal Data Protection Act (PDPA 2010 / 2024 Amendment)**: *Data Privacy & Redaction Guardrails* (`data_privacy_pdpa`)
- **Bursa Malaysia Sustainability Reporting Guide & NETR**: *ESG & GHG Scope 1–3 Carbon Analytics* (`esg_sustainability_reporting`, `carbon_footprint_analytics`)

---

### C. Crosswalked ESCO Occupational Profiles (`104` Occupations)
All `104` European Commission ESCO v1.1 occupations were mapped via `map_esco_to_malaysian_demand()` onto MASCO 2020 unit groups (`2133`, `2422`, `2424`, `2511`, `2512`, `2519`, `2521`, `4110`, `4132`, `4222`, `4311`) so that European task/skill descriptions enrich vocabulary while **Malaysian MyCOL criticality determines the target demand label**.
