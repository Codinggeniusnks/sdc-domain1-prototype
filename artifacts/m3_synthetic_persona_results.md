# M3 Synthetic Benchmark Persona Evaluation Results

**Engine Version**: M3 v1.0.0  
**Status**: `BENCHMARK VERIFIED & REPRODUCIBLE`  
**Date**: 2026-10-23  
**Data Reference**: [`data/matching/synthetic_personas_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/matching/synthetic_personas_v1.json)  

---

## 1. Overview of Synthetic Personas

The 8 synthetic personas represent archetypal Malaysian workforce profiles designed to test recommender sanity, guardrails, and explainability without utilizing private personal CV data.

---

## 2. Persona Results Across Scenarios (Balanced Baseline Weighting)

### Persona 1: Senior Tabular Data Analyst (Data / Analytics-Oriented)
- **Profile Skills**: `sql_data_analysis` (CONFIRMED), `python_scripting` (CONFIRMED), `data_visualization` (CONFIRMED), `workflow_automation` (M1 SUGGESTED).
- **Match Results**:

| Rank | MASCO | Occupation Title | Reference Index | Moderate Copilot | Fast Agentic | Confidence Tier | Transition Distance |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **#1** | **2521** | Database Designers & Administrators | **72.6** | 73.1 | 73.8 | `MODERATE FIT WITH GAP` | SHORT TRANSITION |
| **#2** | **2512** | Software Developers | **58.7** | 59.4 | 60.1 | `MODERATE FIT WITH GAP` | MODERATE TRANSITION |
| **#3** | **2529** | Database & Network NEC (AI & Data Science) | **57.6** | 58.5 | 59.4 | `MODERATE FIT WITH GAP` | MODERATE TRANSITION |

- **Sanity Invariant**: Correctly prioritizes database and analytical roles; non-data engineering roles (e.g., 2151 Electrical, 2166 Multimedia) rank in the bottom tier.

---

### Persona 2: Full-Stack Software & Systems Developer (Software / Automation-Oriented)
- **Profile Skills**: `python_scripting` (CONFIRMED), `api_integration` (CONFIRMED), `workflow_automation` (CONFIRMED), `rag_knowledge_systems` (USER ADDED).
- **Match Results**:

| Rank | MASCO | Occupation Title | Reference Index | Moderate Copilot | Fast Agentic | Confidence Tier | Transition Distance |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **#1** | **2512** | Software Developers | **85.3** | 86.0 | 86.8 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |
| **#2** | **2519** | Software & Applications Developers NEC | **78.2** | 78.9 | 79.5 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |
| **#3** | **2522** | Systems Administrators & Cloud Engineers | **70.4** | 71.0 | 71.7 | `MODERATE FIT WITH GAP` | SHORT TRANSITION |

- **Sanity Invariant**: High confidence alignment with enterprise software development and cloud operations.

---

### Persona 3: Operations & Transformation Lead (Business Process / Operations-Oriented)
- **Profile Skills**: `process_mapping` (CONFIRMED), `workflow_automation` (CONFIRMED), `stakeholder_communication` (CONFIRMED), `ai_literacy` (M1 SUGGESTED).
- **Match Results**:

| Rank | MASCO | Occupation Title | Reference Index | Moderate Copilot | Fast Agentic | Confidence Tier | Transition Distance |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **#1** | **2511** | Systems Analysts | **84.6** | 85.3 | 86.1 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |
| **#2** | **2421** | Management & Organization Analysts | **80.5** | 81.2 | 82.0 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |
| **#3** | **1330** | ICT Services Managers | **75.1** | 75.8 | 76.5 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |

- **Sanity Invariant**: Seamlessly bridges process engineering and corporate operational management.

---

### Persona 4: Data Privacy & AI Governance Specialist (Governance / Privacy-Oriented)
- **Profile Skills**: `ai_ethics_governance` (CONFIRMED), `data_privacy_pdpa` (CONFIRMED), `stakeholder_communication` (CONFIRMED), `human_in_the_loop_qa` (M1 CORE).
- **Match Results**:

| Rank | MASCO | Occupation Title | Reference Index | Moderate Copilot | Fast Agentic | Confidence Tier | Transition Distance |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **#1** | **2422** | Policy & Corporate Planning Professionals | **80.9** | 81.6 | 82.3 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |
| **#2** | **1330** | ICT Services Managers | **62.4** | 63.1 | 63.8 | `MODERATE FIT WITH GAP` | MODERATE TRANSITION |
| **#3** | **2421** | Management & Organization Analysts | **59.8** | 60.5 | 61.2 | `MODERATE FIT WITH GAP` | MODERATE TRANSITION |

- **Sanity Invariant**: Accurately maps MOSTI AIGE and PDPA governance skills to corporate policy planning.

---

### Persona 5: Environmental & Carbon Accounting Analyst (Sustainability-Oriented)
- **Profile Skills**: `esg_sustainability_reporting` (CONFIRMED), `carbon_footprint_analytics` (CONFIRMED), `sql_data_analysis` (CONFIRMED), `process_mapping` (M1 SUGGESTED).
- **Match Results**:

| Rank | MASCO | Occupation Title | Reference Index | Moderate Copilot | Fast Agentic | Confidence Tier | Transition Distance |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **#1** | **2143** | Environmental Engineers & Sustainability Specialists | **81.4** | 82.1 | 82.9 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |
| **#2** | **2151** | Electrical Engineers | **79.8** | 80.5 | 81.2 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |
| **#3** | **2411** | Accountants & Financial Auditors | **62.7** | 63.3 | 64.0 | `MODERATE FIT WITH GAP` | MODERATE TRANSITION |

- **Sanity Invariant**: Correctly pairs green engineering with Bursa ESG reporting; software development is clamped to zero overlap.

---

### Persona 6: Corporate Learning & Instructional Designer (Communication / Instructional-Oriented)
- **Profile Skills**: `instructional_design` (CONFIRMED), `stakeholder_communication` (CONFIRMED), `ai_literacy` (CONFIRMED), `prompt_engineering` (M1 SUGGESTED).
- **Match Results**:

| Rank | MASCO | Occupation Title | Reference Index | Moderate Copilot | Fast Agentic | Confidence Tier | Transition Distance |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **#1** | **2424** | Training & Staff Development Professionals | **83.1** | 83.7 | 84.4 | `HIGH CONFIDENCE FIT` | SHORT TRANSITION |
| **#2** | **2421** | Management & Organization Analysts | **55.3** | 56.0 | 56.7 | `MODERATE FIT WITH GAP` | MODERATE TRANSITION |
| **#3** | **3322** | Commercial Sales Representatives | **54.2** | 54.8 | 55.4 | `MODERATE FIT WITH GAP` | MODERATE TRANSITION |

- **Sanity Invariant**: Dominant fit for HRD Corp reskilling architecture; technical IC design ranks near zero.

---

### Persona 7: Administrative Assistant in Digital Upskilling (Clerical Transition-Oriented)
- **Profile Skills**: `process_mapping` (CONFIRMED), `ai_literacy` (CONFIRMED), `workflow_automation` (USER ADDED), `sql_data_analysis` (M1 SUGGESTED).
- **Match Results**:

| Rank | MASCO | Occupation Title | Reference Index | Moderate Copilot | Fast Agentic | Confidence Tier | Transition Distance |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **#1** | **4110** | General Office Clerks | **72.1** | 71.8 | 71.4 | `MODERATE FIT WITH GAP` | SHORT TRANSITION |
| **#2** | **4311** | Accounting and Bookkeeping Clerks | **69.8** | 69.5 | 69.1 | `MODERATE FIT WITH GAP` | SHORT TRANSITION |
| **#3** | **2511** | Systems Analysts | **68.4** | 69.1 | 69.9 | `MODERATE FIT WITH GAP` | MODERATE TRANSITION |

- **Sanity Invariant & Non-Punitive Semantics**: Under FAST_AGENTIC, 2511 rises to 69.9 while 4110 drops to 71.4. The engine highlights 2511 as a high-growth transition target rather than presenting clerical work as an unviable dead end.

---

### Persona 8: Recent Graduate (Sparse Early-Career Profile)
- **Profile Skills**: `ai_literacy` (CONFIRMED), `prompt_engineering` (M1 SUGGESTED).
- **Match Results**:

| Rank | MASCO | Occupation Title | Reference Index | Moderate Copilot | Fast Agentic | Confidence Tier | Transition Distance |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|
| **#1** | **4110** | General Office Clerks | **42.3** | 42.1 | 41.8 | `DEVELOPING TRANSITION TARGET` | SUBSTANTIAL TRANSITION |
| **#2** | **3322** | Commercial Sales Representatives | **40.1** | 40.0 | 39.8 | `DEVELOPING TRANSITION TARGET` | SUBSTANTIAL TRANSITION |
| **#3** | **3343** | Administrative & Executive Secretaries | **38.9** | 38.7 | 38.5 | `DEVELOPING TRANSITION TARGET` | SUBSTANTIAL TRANSITION |

- **Sanity Invariant**: Correctly assigns `DEVELOPING TRANSITION TARGET` (Index 30–50) with substantial transition distance, preventing premature high-confidence matching for sparse profiles.
