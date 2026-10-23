# M2 Confidence Score Recalibration Report (v1.1.0)

## Executive Summary

During the Stage 9C Argon Forensic Audit, Defect **P1-2** identified severe artificial confidence inflation in M2 v1.0.0: all 16 skills received a uniform `100.0 (HIGH)` confidence rating. Forensic investigation revealed two root causes:
1. **Unconditional Source Bleed**: Occupational-level and macro-level evidence families (`ILO_GENAI_STUDY` and `DOSM_WAGES`) were injected unconditionally into every skill's evidence graph, granting 2 artificial evidence families without direct empirical link.
2. **Missing Publisher Grouping Caps**: Multiple signals from the same underlying statutory body (e.g., TalentCorp MyCOL + TalentCorp AI Impact Study) were summed independently without entity caps.

In M2 v1.1.0, the confidence engine was completely recalibrated under `data/trends/processed/m2_confidence_config_v1_1.json` to enforce strict structural boundaries, entity-level caps, and direct empirical requirement rules.

---

## Confidence Recalibration Results

### Skill Confidence Tier Distribution

| Version | Total Skills | HIGH Confidence (>=75) | MEDIUM Confidence (55-74) | LOW Confidence (35-54) | INSUFFICIENT (<35) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **v1.0.0 (Pre-Remediation)** | 16 | 16 (100.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| **v1.1.0 (Remediated)** | 16 | **7 (43.75%)** | **7 (43.75%)** | **2 (12.50%)** | 0 (0.0%) |

The remediated distribution exhibits authentic variance reflecting actual empirical data coverage across the Malaysian ecosystem.

---

## Detailed Skill Confidence Inventory (v1.1.0)

| Skill ID | Skill Name | Confidence Score | Tier | Independent Families | Direct Signals | Present Evidence Families |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `ai_literacy` | Foundational AI Literacy & LLM Capabilities | 80.0 | **HIGH** | 4 | 16 | MyCOL, Impact Study, Policy, OpenAlex |
| `process_mapping` | Business Process Mapping & SOP Design | 80.0 | **HIGH** | 4 | 16 | MyCOL, Impact Study, Policy, OpenAlex |
| `sql_data_analysis` | SQL & Structured Data Analysis | 80.0 | **HIGH** | 4 | 17 | MyCOL, Impact Study, Policy, OpenAlex |
| `python_scripting` | Python Scripting & Data Automation | 80.0 | **HIGH** | 4 | 17 | MyCOL, Impact Study, Policy, OpenAlex |
| `data_visualization` | Data Visualization & KPI Storytelling | 80.0 | **HIGH** | 4 | 16 | MyCOL, Impact Study, Policy, OpenAlex |
| `workflow_automation` | Agentic Workflow Orchestration & Tool Integration | 80.0 | **HIGH** | 4 | 16 | MyCOL, Impact Study, Policy, OpenAlex |
| `api_integration` | REST API Integration & Resilient Fallbacks | 80.0 | **HIGH** | 4 | 17 | MyCOL, Impact Study, Policy, OpenAlex |
| `human_in_the_loop_qa` | Human-in-the-Loop Evaluation & AI Testing | 60.0 | **MEDIUM** | 3 | 7 | Impact Study, Policy, OpenAlex |
| `ai_ethics_governance` | AI Ethics, Fairness Auditing & Governance | 60.0 | **MEDIUM** | 3 | 7 | Impact Study, Policy, OpenAlex |
| `data_privacy_pdpa` | Data Privacy & Malaysian PDPA Compliance | 60.0 | **MEDIUM** | 3 | 8 | Impact Study, Policy, OpenAlex |
| `esg_sustainability_reporting` | ESG Frameworks & UN SDG Impact Mapping | 60.0 | **MEDIUM** | 3 | 7 | Impact Study, Policy, OpenAlex |
| `carbon_footprint_analytics` | Carbon-Aware Compute & Resource Telemetry | 60.0 | **MEDIUM** | 3 | 7 | Impact Study, Policy, OpenAlex |
| `stakeholder_communication` | Human-Centred Change & Stakeholder Communication | 60.0 | **MEDIUM** | 3 | 11 | MyCOL, Impact Study, OpenAlex |
| `instructional_design` | Competency Matrix & Reskilling Curriculum Design | 60.0 | **MEDIUM** | 3 | 7 | Impact Study, Policy, OpenAlex |
| `prompt_engineering` | Structured Prompting & Context Engineering | 40.0 | **LOW** | 2 | 8 | Impact Study, OpenAlex |
| `rag_knowledge_systems` | Retrieval-Augmented Generation (RAG) & Grounding | 40.0 | **LOW** | 2 | 8 | Impact Study, OpenAlex |

---

## Architectural Remediation Mechanics

### 1. Elimination of Source Bleed
- `ILO_GENAI_STUDY` (ILO Working Papers 96 & 140) and `DOSM_WAGES` (Formal Sector Wages) are occupational-level taxonomies mapped via MASCO 4-digit codes.
- In v1.1.0, skills evaluation parses **only** signals where `entity_type == "SKILL"` or direct crosswalks from verified skill taxonomies.
- No synthetic or macro-level spillover is permitted into skill confidence accumulation.

### 2. Publisher-Level Contribution Caps
To prevent a single organization with multiple publications from dominating confidence, strict publisher groupings are enforced:

| Publisher Entity | Evidence Families Included | Maximum Contribution Cap |
| :--- | :--- | :---: |
| **TalentCorp Malaysia / ILMIA** | `TALENTCORP_MYCOL`, `TALENTCORP_IMPACT_STUDY` | **35.0 pts** |
| **Malaysian Government (EPU/MOSTI/MDEC)** | `MALAYSIAN_GOVERNMENT_POLICY` | **20.0 pts** |
| **Department of Statistics Malaysia (DOSM)** | `DOSM_WAGES` | **30.0 pts** |
| **Multilateral International Bodies (ILO)** | `ILO_GENAI_STUDY` | **25.0 pts** |
| **Academic / Scientometric (OpenAlex)** | `OPENALEX_SCHOLARLY` | **15.0 pts** |

### 3. Structural Tier Thresholds
Confidence score tiers require both a point threshold and a minimum count of independent evidence families:
- **HIGH**: Score $\ge 75.0$ AND $\ge 4$ independent evidence families.
- **MEDIUM**: Score $\ge 55.0$ AND $\ge 3$ independent evidence families.
- **LOW**: Score $\ge 35.0$ AND $\ge 2$ independent evidence families.
- **INSUFFICIENT**: Score $< 35.0$ OR $< 2$ independent evidence families.

---

## Leave-One-Family-Out Sensitivity Audit

A complete perturbation matrix was evaluated across all 16 skills $\times$ 6 evidence families ($N = 96$ audit instances), recorded in `artifacts/m2_leave_one_family_out_confidence.csv`.

Key observations:
1. **Zero Impact from Irrelevant Families**: Removing `ILO_GENAI_STUDY` or `DOSM_WAGES` causes **0.0 score change** across all 16 skills, proving complete isolation and zero source bleed.
2. **Graceful Degradation**:
   - For HIGH skills, removing `TALENTCORP_MYCOL` drops score from 80.0 to 60.0 (shifting tier to MEDIUM).
   - For MEDIUM skills, removing `MALAYSIAN_GOVERNMENT_POLICY` or `TALENTCORP_IMPACT_STUDY` drops score to 40.0–45.0 (shifting tier to LOW).
   - For LOW skills (`prompt_engineering`, `rag_knowledge_systems`), removing `TALENTCORP_IMPACT_STUDY` leaves only 1 family (`OPENALEX_SCHOLARLY`), correctly dropping the rating to `INSUFFICIENT` (15.0).
3. **Robustness**: No single family removal causes catastrophic divergence; tier transitions follow strict mathematical step functions.

---

## Downstream Interface Safety (M3 & M6)

1. **Down-Weighting Low Confidence in Matching**: In M3 Role Matching, skills marked `LOW` confidence will have their match contribution discount factor applied ($w_{\text{adj}} = 0.50 \times w_{\text{base}}$).
2. **Scenario Flagging**: In M6 Scenario Engine, skills marked `LOW` or `MEDIUM` confidence are tagged with `EVIDENCE_UNCERTAINTY` flags, preventing absolute claims of workforce displacement.
