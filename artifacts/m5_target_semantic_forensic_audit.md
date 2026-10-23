# M5 Target Semantic Forensic Audit

**Review Date:** 2026-10-24  
**Auditor:** Independent Senior SDG Methodologist, Sustainability Taxonomy Auditor  
**Artifact Evaluated:** `data/sdg/sdg_targets_v1.json`, `data/sdg/skill_sdg_mappings_v1.json`, `data/sdg/role_sdg_mappings_v1.json`

---

## 1. Forensic Methodology: The 4-Tier Semantic Distance Model

To assess whether entity-to-target relationships are defensible, every mapping is classified into one of four semantic tiers:

1. **DIRECT TARGET FIT (Tier 1):** The core task or competency directly executes the action mandated by the target text with 0 intermediate hops.
2. **PLAUSIBLE ENABLING FIT (Tier 2):** The skill or role produces intermediate outputs, technological tools, or infrastructure directly consumed by actors achieving the target (1 causal hop).
3. **CONTEXTUAL / APPLICATION-DEPENDENT (Tier 3):** The contribution materializes only if the entity is deployed within a specific sector, institutional setting, or policy framework (2 causal hops).
4. **TOO REMOTE (Tier 4):** Requires $>2$ causal hops or unstated speculative assumptions. Prohibited in production.

---

## 2. Target-by-Target Forensic Audit

### Target 9.c: Universal ICT & Affordable Internet Access in LDCs
- **Official Text:** *"Significantly increase access to information and communications technology and strive to provide universal and affordable access to the Internet in least developed countries by 2020."*
- **Indicator:** Indicator 9.c.1 measures the percentage of population covered by a mobile network by technology (2G/3G/4G/5G).
- **Audit of M5 Mappings:**
  - `rag_knowledge_systems`: Classified in v1.0.0 as ENABLING to 9.c. **Finding: TOO REMOTE (Tier 4).** A RAG pipeline retrieves enterprise knowledge chunks; it does not deploy mobile base stations or expand physical internet access.
  - `api_integration`: Classified in v1.0.0 as ENABLING to 9.c. **Finding: TOO REMOTE (Tier 4).** Software APIs connect applications, not physical telecommunications access.
  - `2521` (Database Designers): Classified in v1.0.0 as ENABLING to 9.c. **Finding: TOO REMOTE (Tier 4).**
  - `2166` (UI/UX Designers): Classified in v1.0.0 as ENABLING to 9.c. **Finding: TOO REMOTE (Tier 4).**
  - `3514` (Web Technicians): Classified in v1.0.0 as ENABLING to 9.c. **Finding: CONTEXTUAL (Tier 3).** Web maintenance only supports access if applied to public digital portals.
- **Verdict on Target 9.c:** **OVERSTRETCHED (P1 DEFECT)**. All internal enterprise software applications must be decoupled from Target 9.c.

---

### Target 9.5: Enhance Scientific Research & Industrial Technological Capabilities
- **Official Text:** *"Enhance scientific research, upgrade the technological capabilities of industrial sectors in all countries, in particular developing countries, including, by 2030, encouraging innovation and substantially increasing the number of research and development workers per 1 million people and public and private research and development spending."*
- **Audit of M5 Mappings:**
  - `python_scripting`, `prompt_engineering`, `sql_data_analysis`, `workflow_automation`: Classified as ENABLING. **Finding: PLAUSIBLE ENABLING FIT (Tier 2).** Software languages and automated pipelines are foundational tools for computational industrial R&D.
  - `2512` (Software Developers), `2511` (Systems Analysts), `2529` (AI & Data Science Specialists): Classified as ENABLING. **Finding: PLAUSIBLE ENABLING FIT (Tier 2).** These occupations form the core domestic R&D workforce measured by Indicator 9.5.2.
  - `2152` (Electronic Engineers / Semiconductor): Classified as DIRECT. **Finding: DIRECT TARGET FIT (Tier 1).** Advanced microelectronics IC design directly constitutes high-tech industrial R&D under NIMP 2030.
- **Verdict on Target 9.5:** **VALID**.

---

### Target 8.2: Economic Productivity via Diversification, Innovation & Tech Upgrading
- **Official Text:** *"Achieve higher levels of economic productivity through diversification, technological upgrading and innovation, including through a focus on high-value added and labour-intensive sectors."*
- **Audit of M5 Mappings:**
  - Software & ICT Occupations (`2512`, `2511`, `2529`, `2519`, `1330`): **Finding: PLAUSIBLE ENABLING FIT (Tier 2).** Digital systems automate operational bottlenecks and lift labor productivity.
  - `2421` (Management Analysts): **Finding: PLAUSIBLE ENABLING FIT (Tier 2).** Business process optimization directly drives operational efficiency.
  - `3322` (Commercial Sales Representatives): **Finding: CONTEXTUAL (Tier 3).** Commercial outreach drives market diversification only if selling innovative products.
- **Verdict on Target 8.2:** **VALID**.

---

### Target 8.5: Full & Productive Employment and Decent Work
- **Official Text:** *"By 2030, achieve full and productive employment and decent work for all women and men, including for young people and persons with disabilities, and equal pay for work of equal value."*
- **Audit of M5 Mappings:**
  - `instructional_design` & `2424` (Training Professionals): **Finding: PLAUSIBLE ENABLING FIT (Tier 2).** Reskilling interventions actively preserve employability and career longevity.
  - `4110` (General Office Clerks) & `3343` (Secretaries): Classified as CONTEXTUAL. **Finding: CONTEXTUAL BENEFICIARY (Tier 3).** Being employed is a societal outcome, not an active occupational contribution. Must be clearly qualified.
- **Verdict on Target 8.5:** **VALID WITH QUALIFICATION (P2 DEFECT)**.

---

### Target 16.6: Effective, Accountable and Transparent Institutions
- **Official Text:** *"Develop effective, accountable and transparent institutions at all levels."*
- **Audit of M5 Mappings:**
  - `ai_ethics_governance`: Classified as DIRECT. **Finding: DIRECT TARGET FIT (Tier 1).** Algorithmic auditing directly enforces institutional decision-making transparency.
  - `2411` (Accountants & Auditors): Classified as DIRECT. **Finding: DIRECT TARGET FIT (Tier 1).** Statutory auditing enforces fiduciary integrity and prevents institutional fraud.
  - `2422` (Corporate Governance / Policy): Classified as DIRECT. **Finding: DIRECT TARGET FIT (Tier 1).**
  - `4311` (Accounting Clerks): Classified as ENABLING. **Finding: PLAUSIBLE ENABLING FIT (Tier 2).** Source document verification maintains audit trails.
- **Verdict on Target 16.6:** **HIGHLY ACCURATE & VALID**.

---

### Target 16.10: Public Access to Information & Fundamental Freedoms
- **Official Text:** *"Ensure public access to information and protect fundamental freedoms, in accordance with national legislation and international agreements."*
- **Audit of M5 Mappings:**
  - `data_privacy_pdpa`: Classified as DIRECT to 16.10. **Finding: TOO REMOTE / SEMANTIC MISMATCH (Tier 4).** Malaysia PDPA 2010 regulates commercial privacy; it does NOT grant public access to information. Target 16.10 is a Freedom of Information mandate.
  - `data_visualization`: Classified as ENABLING to 16.10. **Finding: CONTEXTUAL (Tier 3).** Visualization only supports public access if published in open civic dashboards.
- **Verdict on Target 16.10:** **REQUIRES REALLOCATION (P1 DEFECT)**. PDPA belongs under Target 16.6.

---

### Target 12.6: Adopt Sustainable Practices & Corporate Sustainability Reporting
- **Official Text:** *"Encourage companies, especially large and transnational companies, to adopt sustainable practices and to integrate sustainability information into their reporting cycle."*
- **Audit of M5 Mappings:**
  - `esg_sustainability_reporting`: Classified as DIRECT. **Finding: DIRECT TARGET FIT (Tier 1).** 100% literal match with target mandate.
  - `carbon_footprint_analytics`: Classified as DIRECT. **Finding: DIRECT TARGET FIT (Tier 1).** Scope 1/2/3 calculations provide the core quantitative sustainability disclosure.
  - `2411` (Auditors & Accountants): Classified as DIRECT. **Finding: DIRECT TARGET FIT (Tier 1).** Sustainability assurance under Bursa Malaysia ESG standards.
- **Verdict on Target 12.6:** **FLAWLESS & AUTHORITATIVE (Tier 1 Benchmark)**.

---

### Target 13.2: Integrate Climate Change Measures into National Policies & Planning
- **Official Text:** *"Integrate climate change measures into national policies, strategies and planning."*
- **Audit of M5 Mappings:**
  - `2143` (Environmental Engineers): **Finding: DIRECT TARGET FIT (Tier 1).** Environmental engineers model emissions and design national industrial climate strategies.
  - Corporate `carbon_footprint_analytics`: Classified as DIRECT. **Finding: PLAUSIBLE ENABLING FIT (Tier 2).** Corporate carbon data informs national registries, but corporate GHG accounting itself is an enterprise activity under Target 12.6.
- **Verdict on Target 13.2:** **RECLASSIFY CORPORATE CARBON TO ENABLING (P2 DEFECT)**.

---

### Target 17.18: Disaggregated Data for Developing Countries
- **Official Text:** *"By 2020, enhance capacity-building support to developing countries, including for least developed countries and small island developing States, to increase significantly the availability of high-quality, timely and reliable data disaggregated by income, gender, age, race, ethnicity..."*
- **Audit of M5 Mappings:**
  - `sql_data_analysis`: Classified as primary to 17.18. **Finding: TOO REMOTE (Tier 4).** General SQL queries have no intrinsic link to national development statistics.
  - Database Designers (`2521`): **Finding: TOO REMOTE (Tier 4).**
- **Verdict on Target 17.18:** **SEMANTIC MISMATCH (P1 DEFECT)**. Remove as primary target for general SQL and software roles.

---

## 3. Summary of Semantic Classifications

| Target ID | Total Mappings Audited | Direct Fit (Tier 1) | Enabling Fit (Tier 2) | Contextual (Tier 3) | Too Remote (Tier 4) | Defect Identified |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **9.c** | 9 | 0 | 0 | 2 | **7** | **P1 (Overstretch)** |
| **9.5** | 9 | 1 | 8 | 0 | 0 | None (Valid) |
| **8.2** | 17 | 0 | 14 | 3 | 0 | None (Valid) |
| **8.5** | 5 | 0 | 2 | 3 | 0 | P2 (Conflation) |
| **16.6** | 8 | 3 | 5 | 0 | 0 | None (Valid) |
| **16.10** | 4 | 0 | 0 | 2 | **2** | **P1 (Legal Mismatch)** |
| **12.6** | 8 | 5 | 3 | 0 | 0 | None (Valid) |
| **13.2** | 3 | 1 | 2 | 0 | 0 | P2 (Reclassify) |
| **17.18** | 5 | 0 | 1 | 1 | **3** | **P1 (Mismatch)** |
| **All Others** | 9 | 3 | 4 | 2 | 0 | None (Valid) |
| **TOTAL** | **77** | **13** | **39** | **13** | **12** | **3 P1s, 2 P2s** |
