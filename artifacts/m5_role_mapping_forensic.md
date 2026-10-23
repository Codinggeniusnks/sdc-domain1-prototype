# M5 Role SDG Mapping Forensic Evaluation

**Review Date:** 2026-10-24  
**Auditor:** Independent Senior Labour-Market Matching Auditor, Sustainability Taxonomy Reviewer  
**Artifact Evaluated:** `data/sdg/role_sdg_mappings_v1.json`

---

## 1. Forensic Assessment Methodology

Every one of the 20 MASCO 4-digit occupations is scrutinized based on its actual statutory occupational tasks in the **Malaysian Standard Classification of Occupations (MASCO 2020)**.

Assigned Verdicts:
1. `VALID`: Occupational tasks directly substantiate the target relationship.
2. `TOO STRONG`: The claimed mapping type (e.g. `DIRECT`) exceeds the inherent scope of the general 4-digit code.
3. `TOO REMOTE`: Requires $>2$ causal hops.
4. `SECTOR DEPENDENT`: The alignment only holds if the worker is employed in a specific industry branch.
5. `INSUFFICIENT EVIDENCE`: Descriptors do not support the mapping.

---

## 2. Line-by-Line Occupational Forensic Evaluation (20 Roles)

### 1. `2512` (Software Developers)
- **Primary:** SDG 9 (Target 9.5, ENABLING), SDG 8 (Target 8.2, ENABLING)
- **Secondary:** SDG 17 (Target 17.18, ENABLING)
- **MASCO 2020 Task Basis:** Designing, writing, testing, and maintaining software solutions.
- **Forensic Assessment:** Core developer capabilities enable industrial technological upgrading (9.5) and enterprise labor productivity (8.2). Secondary mapping to 17.18 (official census data) is remote unless developing government statistics software.
- **Verdict:** **VALID (Primary confirmed; drop or flag secondary 17.18)**.

### 2. `2511` (Systems Analysts)
- **Primary:** SDG 9 (Target 9.5, ENABLING), SDG 8 (Target 8.2, ENABLING)
- **Secondary:** None
- **MASCO 2020 Task Basis:** Analyzing user requirements, modeling business processes, and recommending software architecture.
- **Forensic Assessment:** System architecture optimization directly enhances technological capability and economic productivity.
- **Verdict:** **VALID**.

### 3. `2521` (Database Designers and Administrators)
- **Primary:** SDG 9 (Target 9.c, ENABLING), SDG 17 (Target 17.18, ENABLING)
- **Secondary:** SDG 16 (Target 16.10, ENABLING)
- **Forensic Assessment:** Mapping database administration to Target 9.c (LDC telecommunications connectivity) and 17.18 (national development census statistics) is an overstretch. Database admins ensure reliable data infrastructure under Target 9.5 or 8.2.
- **Verdict:** **TOO REMOTE ON 9.c and 17.18 (P1 DEFECT)**.

### 4. `2529` (AI & Data Science Specialists)
- **Primary:** SDG 9 (Target 9.5, ENABLING), SDG 17 (Target 17.18, ENABLING)
- **Secondary:** SDG 8 (Target 8.2, ENABLING)
- **Forensic Assessment:** Target 9.5 is a perfect fit (R&D and advanced modeling). Target 17.18 is remote unless working specifically at DOSM on official national statistics.
- **Verdict:** **VALID (Target 9.5 confirmed; Target 17.18 should be secondary contextual)**.

### 5. `2519` (Software and Applications Developers NEC / Cloud)
- **Primary:** SDG 9 (Target 9.c, ENABLING), SDG 9 (Target 9.4, ENABLING)
- **Secondary:** SDG 8 (Target 8.2, ENABLING)
- **Forensic Assessment:** Target 9.c (LDC internet connectivity) is an overstretch for cloud microservices. Target 9.4 (industrial retrofitting via energy-efficient cloud compute) is a valid enabling link.
- **Verdict:** **REALLOCATE 9.c (P1 DEFECT)**.

### 6. `2522` (Systems Administrators and Cloud Infrastructure Specialists)
- **Primary:** SDG 9 (Target 9.c, ENABLING), SDG 8 (Target 8.2, ENABLING)
- **Secondary:** None
- **Forensic Assessment:** Same finding as 2519: sysadmins maintain servers, but do not expand physical internet access to LDCs under Target 9.c.
- **Verdict:** **REALLOCATE 9.c (P1 DEFECT)**.

### 7. `2411` (Accountants and Auditors)
- **Primary:** SDG 16 (Target 16.6, DIRECT), SDG 12 (Target 12.6, DIRECT)
- **Secondary:** SDG 8 (Target 8.2, ENABLING)
- **MASCO 2020 Task Basis:** Examining financial records, conducting audits, ensuring compliance with statutory accounting standards and ESG assurance.
- **Forensic Assessment:** Flawless dual DIRECT alignment to Target 16.6 (fiduciary accountability) and Target 12.6 (sustainability disclosures).
- **Verdict:** **VALID (Exemplary Direct Mapping)**.

### 8. `2421` (Management and Organization Analysts)
- **Primary:** SDG 8 (Target 8.2, ENABLING), SDG 12 (Target 12.6, ENABLING)
- **Secondary:** None
- **Forensic Assessment:** Restructuring enterprise operating models directly drives productivity upgrading (8.2) and assists circular economy adoption (12.6).
- **Verdict:** **VALID**.

### 9. `2422` (Policy and Corporate Planning Professionals)
- **Primary:** SDG 16 (Target 16.6, DIRECT), SDG 12 (Target 12.6, ENABLING)
- **Secondary:** SDG 10 (Target 10.2, CONTEXTUAL)
- **Forensic Assessment:** Drafting corporate governance charters directly enforces institutional transparency (16.6). Formulating sustainability strategies enables corporate disclosures (12.6).
- **Verdict:** **VALID**.

### 10. `2151` (Electrical Engineers)
- **Primary:** SDG 7 (Targets 7.2, 7.3, DIRECT), SDG 9 (Target 9.4, DIRECT)
- **Secondary:** None
- **MASCO 2020 Task Basis:** Conducting research on and advising on, designing, and directing the construction and operation of electrical systems.
- **Forensic Assessment:** While electrical engineers are essential for renewables and grid efficiency, a general electrical engineer may work on diesel generation or basic wiring. An unconditional `DIRECT` mapping overgeneralizes the role.
- **Verdict:** **SECTOR DEPENDENT (P2 DEFECT)**. Requires `SECTOR_DEPENDENT_ALIGNMENT` flag.

### 11. `2152` (Electronic Engineers / Semiconductor)
- **Primary:** SDG 9 (Target 9.5, DIRECT), SDG 7 (Target 7.3, ENABLING)
- **Secondary:** SDG 8 (Target 8.2, ENABLING)
- **Forensic Assessment:** Semiconductor and IC design is the technological centerpiece of Malaysia's NIMP 2030, directly constituting industrial R&D (9.5) and enabling energy-efficient electronics (7.3).
- **Verdict:** **VALID**.

### 12. `2143` (Environmental Engineers)
- **Primary:** SDG 13 (Target 13.2, DIRECT), SDG 12 (Target 12.6, DIRECT), SDG 11 (Target 11.6, DIRECT)
- **Secondary:** SDG 9 (Target 9.4, DIRECT)
- **MASCO 2020 Task Basis:** Investigating environmental impact, designing waste/water treatment, and developing pollution control technologies.
- **Forensic Assessment:** Highly defensible direct alignment to environmental targets, but should include a sector/consultancy deployment flag.
- **Verdict:** **VALID WITH SECTOR FLAG (P2 DEFECT)**.

### 13. `2424` (Training and Staff Development Professionals)
- **Primary:** SDG 4 (Target 4.4, DIRECT), SDG 8 (Target 8.5, ENABLING)
- **Secondary:** SDG 10 (Target 10.2, ENABLING)
- **Forensic Assessment:** Designing and facilitating adult vocational training directly operationalizes Target 4.4 and enables employment longevity under 8.5.
- **Verdict:** **VALID**.

### 14. `2166` (Graphic and Multimedia Designers / UI/UX)
- **Primary:** SDG 9 (Target 9.c, ENABLING), SDG 10 (Target 10.2, ENABLING)
- **Secondary:** SDG 8 (Target 8.2, CONTEXTUAL)
- **Forensic Assessment:** Target 9.c (LDC internet connectivity) is an overstretch for UI design. However, Target 10.2 (accessibility design for elderly and disabled users under WCAG standards) is an outstanding, innovative enabling alignment.
- **Verdict:** **REALLOCATE 9.c; RETAIN 10.2 (P1 DEFECT)**.

### 15. `1330` (ICT Services Managers)
- **Primary:** SDG 9 (Target 9.5, ENABLING), SDG 8 (Target 8.2, ENABLING)
- **Secondary:** SDG 9 (Target 9.c, ENABLING)
- **Forensic Assessment:** Directing enterprise IT departments directly enables technological upgrading (9.5) and operational productivity (8.2). Secondary Target 9.c is remote.
- **Verdict:** **VALID (Primary confirmed; drop secondary 9.c)**.

### 16. `3514` (Web Technicians and Cloud Operators)
- **Primary:** SDG 9 (Target 9.c, ENABLING), SDG 8 (Target 8.2, CONTEXTUAL)
- **Secondary:** None
- **Forensic Assessment:** Maintaining corporate web portals does not expand LDC connectivity under 9.c. Should be reallocated to Target 8.2 (operational productivity).
- **Verdict:** **REALLOCATE 9.c (P1 DEFECT)**.

### 17. `3322` (Commercial Sales Representatives)
- **Primary:** SDG 8 (Target 8.2, CONTEXTUAL)
- **Secondary:** SDG 12 (Target 12.6, CONTEXTUAL)
- **Forensic Assessment:** Correctly classified as CONTEXTUAL. Sales representatives accelerate market adoption of innovative products.
- **Verdict:** **VALID (Contextual confirmed)**.

### 18. `4311` (Accounting and Bookkeeping Clerks)
- **Primary:** SDG 16 (Target 16.6, ENABLING), SDG 8 (Target 8.5, CONTEXTUAL)
- **Secondary:** None
- **Forensic Assessment:** Processing vouchers, ledgers, and reconciliations directly maintains the statutory audit trail required for institutional accountability (16.6).
- **Verdict:** **VALID**.

### 19. `4110` (General Office Clerks)
- **Primary:** SDG 8 (Target 8.5, CONTEXTUAL)
- **Secondary:** SDG 9 (Target 9.c, CONTEXTUAL)
- **Forensic Assessment:** Routine administrative work represents decent employment (8.5), but secondary mapping to 9.c (office digitisation $\to$ LDC internet connectivity) is completely indefensible.
- **Verdict:** **DROP SECONDARY 9.c (P1 DEFECT)**.

### 20. `3343` (Administrative and Executive Secretaries)
- **Primary:** SDG 8 (Target 8.5, CONTEXTUAL), SDG 16 (Target 16.6, CONTEXTUAL)
- **Secondary:** None
- **Forensic Assessment:** Boardroom scheduling and minute archiving support executive governance accountability (16.6) in a contextual capacity.
- **Verdict:** **VALID**.

---

## 3. Summary of Role Forensic Audit

- **VALID:** 13 / 20 (65.0%)
- **P1 Defects (Target 9.c Overstretch / Target 17.18 Mismatch):** 5 roles (`2521`, `2519`, `2522`, `2166`, `3514`)
- **P2 Defects (Missing Sector-Dependent Flag):** 2 roles (`2151`, `2143`)
- **P0 Defects:** 0
