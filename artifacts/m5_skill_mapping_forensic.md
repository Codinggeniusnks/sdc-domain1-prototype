# M5 Skill SDG Mapping Forensic Evaluation

**Review Date:** 2026-10-24  
**Auditor:** Independent Senior SDG Methodologist, Evidence-Grounding Reviewer  
**Artifact Evaluated:** `data/sdg/skill_sdg_mappings_v1.json`

---

## 1. Forensic Assessment Methodology

Every one of the 16 canonical skills is individually scrutinized against its primary and secondary SDG alignments. The reviewer assigns one of five definitive verdicts:
1. `VALID`: The causal mechanism is defensible, evidence-grounded, and correctly typed.
2. `TOO STRONG`: The claimed mapping type (e.g. `DIRECT`) exceeds the actual causal influence of the skill.
3. `TOO REMOTE`: The causal chain involves $>2$ intermediate hops or unsupportable extrapolation.
4. `CONTEXT DEPENDENT`: The alignment depends entirely on enterprise sector or deployment setting without appropriate flags.
5. `INSUFFICIENT EVIDENCE`: The cited sources do not substantiate the claim.

---

## 2. Line-by-Line Forensic Evaluation of the 16 Canonical Skills

### 1. `ai_literacy` (AI Literacy & Principles)
- **Claimed Primary:** SDG 4 (Target 4.4, ENABLING)
- **Claimed Secondary:** SDG 8 (Target 8.2, ENABLING)
- **Forensic Review:** Foundational digital and AI literacy enables adult workers to remain employable in tech-enabled workplaces (Target 4.4) and adapt to productive workflow tools (Target 8.2). Causal link is 1 hop.
- **Verdict:** **VALID**.

### 2. `prompt_engineering` (Prompt Engineering & Synthesis)
- **Claimed Primary:** SDG 8 (Target 8.2, ENABLING)
- **Claimed Secondary:** SDG 9 (Target 9.5, ENABLING)
- **Forensic Review:** Optimizing LLM interaction directly increases labor productivity and knowledge synthesis in enterprise services (Target 8.2). Secondary mapping to Target 9.5 (industrial R&D) is plausible when assisting technical coders.
- **Verdict:** **VALID**.

### 3. `process_mapping` (Business Process Mapping)
- **Claimed Primary:** SDG 8 (Target 8.2, ENABLING)
- **Claimed Secondary:** SDG 12 (Target 12.6, ENABLING)
- **Forensic Review:** Identifying operational bottlenecks drives productivity upgrading (Target 8.2). Mapping workflows for resource efficiency supports corporate sustainability disclosures (Target 12.6).
- **Verdict:** **VALID**.

### 4. `sql_data_analysis` (SQL Data Extraction & Analysis)
- **Claimed Primary:** SDG 17 (Target 17.18, ENABLING)
- **Claimed Secondary:** SDG 9 (Target 9.5, ENABLING)
- **Forensic Review:** Target 17.18 is international statistical capacity building for developing country demographic census disaggregation. General SQL querying on corporate business data is far removed from official UN statistical capacity. Primary mapping should be Target 9.5 or 8.2.
- **Verdict:** **TOO REMOTE (P1 DEFECT)**.

### 5. `python_scripting` (Python Scripting & Automation)
- **Claimed Primary:** SDG 9 (Target 9.5, ENABLING)
- **Claimed Secondary:** SDG 8 (Target 8.2, ENABLING)
- **Forensic Review:** Python is the premier language of industrial R&D, data science, and scientific computing (Target 9.5). Automation scripts eliminate manual processing friction, lifting labor productivity (Target 8.2). Strictly non-DIRECT.
- **Verdict:** **VALID**.

### 6. `data_visualization` (Data Visualization & Dashboarding)
- **Claimed Primary:** SDG 16 (Target 16.10, ENABLING)
- **Claimed Secondary:** SDG 17 (Target 17.18, ENABLING)
- **Forensic Review:** Mapping data visualization to Target 16.10 (*public access to information*) is context-dependent. Dashboards built for internal corporate management do not provide public access to information. It should be contextualized or mapped to operational decision-making.
- **Verdict:** **CONTEXT DEPENDENT (P2 DEFECT)**.

### 7. `workflow_automation` (Workflow & Integration Automation)
- **Claimed Primary:** SDG 8 (Target 8.2, ENABLING)
- **Claimed Secondary:** SDG 9 (Target 9.5, ENABLING)
- **Forensic Review:** Automating repetitive cross-system workflows directly accelerates economic productivity through technological upgrading (Target 8.2).
- **Verdict:** **VALID**.

### 8. `human_in_the_loop_qa` (Human-in-the-Loop Quality Assurance)
- **Claimed Primary:** SDG 8 (Target 8.8, ENABLING)
- **Claimed Secondary:** SDG 16 (Target 16.6, ENABLING)
- **Forensic Review:** Auditing AI outputs for hallucinations, safety hazards, and errors protects safe working environments (Target 8.8) and reinforces institutional decision accuracy (Target 16.6).
- **Verdict:** **VALID**.

### 9. `rag_knowledge_systems` (Retrieval-Augmented Generation)
- **Claimed Primary:** SDG 9 (Target 9.c, ENABLING)
- **Claimed Secondary:** SDG 16 (Target 16.10, ENABLING)
- **Forensic Review:** Target 9.c mandates universal and affordable access to the Internet in LDCs. A vector database retrieving enterprise PDF chunks has zero relationship to telecommunications access in LDCs. Primary mapping must be reallocated to Target 9.5 (technological capabilities).
- **Verdict:** **TOO REMOTE (P1 DEFECT)**.

### 10. `api_integration` (API Integration & Orchestration)
- **Claimed Primary:** SDG 9 (Target 9.c, ENABLING)
- **Claimed Secondary:** SDG 8 (Target 8.2, ENABLING)
- **Forensic Review:** Same defect as RAG: connecting REST endpoints in enterprise cloud systems does not provide physical internet access in least developed countries. Primary mapping must be Target 9.5 or 8.2.
- **Verdict:** **TOO REMOTE (P1 DEFECT)**.

### 11. `ai_ethics_governance` (AI Ethics & Algorithmic Governance)
- **Claimed Primary:** SDG 16 (Target 16.6, DIRECT)
- **Claimed Secondary:** SDG 10 (Target 10.2, ENABLING)
- **Forensic Review:** Preventing algorithmic discrimination directly enforces effective, accountable institutions (Target 16.6) and protects demographic inclusion (Target 10.2).
- **Verdict:** **VALID**.

### 12. `data_privacy_pdpa` (Data Privacy & PDPA Compliance)
- **Claimed Primary:** SDG 16 (Target 16.10, DIRECT)
- **Claimed Secondary:** SDG 16 (Target 16.6, DIRECT)
- **Forensic Review:** Target 16.10 is Freedom of Information (public access to government information). Malaysia PDPA 2010 regulates commercial privacy and restricts unauthorized disclosure. It belongs directly under Target 16.6 (institutional compliance and rule of law).
- **Verdict:** **TOO STRONG / MISCLASSIFIED (P1 DEFECT)**.

### 13. `esg_sustainability_reporting` (ESG & Corporate Sustainability Reporting)
- **Claimed Primary:** SDG 12 (Target 12.6, DIRECT)
- **Claimed Secondary:** SDG 13 (Target 13.2, DIRECT)
- **Forensic Review:** Flawless alignment to Target 12.6 (*encourage companies to adopt sustainable practices and integrate sustainability information into their reporting cycle*). Secondary mapping to Target 13.2 should be ENABLING.
- **Verdict:** **VALID**.

### 14. `carbon_footprint_analytics` (Carbon Footprint Analytics & Accounting)
- **Claimed Primary:** SDG 13 (Target 13.2, DIRECT)
- **Claimed Secondary:** SDG 12 (Target 12.6, DIRECT), SDG 13 (Target 13.3, DIRECT)
- **Forensic Review:** Calculating Scope 1/2/3 carbon emissions directly satisfies corporate reporting under Target 12.6. Target 13.2 is national government policy planning, where corporate carbon data acts as an ENABLING feed.
- **Verdict:** **TOO STRONG ON 13.2 (P2 DEFECT)**.

### 15. `stakeholder_communication` (Cross-Functional Stakeholder Communication)
- **Claimed Primary:** SDG 17 (Target 17.16, ENABLING)
- **Claimed Secondary:** SDG 16 (Target 16.6, CONTEXTUAL)
- **Forensic Review:** Routine enterprise communication is not equivalent to international multi-stakeholder sustainable development partnerships (Target 17.16). It is an essential administrative enabler, but its SDG 17 link is contextual.
- **Verdict:** **CONTEXT DEPENDENT (P2 DEFECT)**.

### 16. `instructional_design` (Instructional Design & Workforce Reskilling)
- **Claimed Primary:** SDG 4 (Target 4.4, DIRECT)
- **Claimed Secondary:** SDG 8 (Target 8.5, DIRECT), SDG 4 (Target 4.7, DIRECT)
- **Forensic Review:** Designing adult technical upskilling directly executes Target 4.4. Secondary mapping to Target 4.7 (sustainability education) should only apply if courses teach sustainability; generic instructional design is Target 4.4.
- **Verdict:** **VALID (Target 4.4 confirmed; 4.7 requires qualification)**.

---

## 3. Summary of Skill Forensic Audit

- **VALID:** 10 / 16 (62.5%)
- **P1 Defects (Too Remote / Misclassified):** 3 (`sql_data_analysis`, `rag_knowledge_systems`, `api_integration`, `data_privacy_pdpa`)
- **P2 Defects (Too Strong / Context Dependent):** 3 (`data_visualization`, `carbon_footprint_analytics`, `stakeholder_communication`)
- **P0 Defects:** 0
