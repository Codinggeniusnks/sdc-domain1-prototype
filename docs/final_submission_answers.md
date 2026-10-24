# Official SDC Hackathon 2026 — Final Submission Answers
**System:** National AI Workforce Reskilling & Foresight Engine v1.0.0 (`AI Skills Compass`)  
**Domain 1:** The Aiversecity Future-Ready Workforce Domain  
**Target Submission Window:** SDC Hackathon 2026 Preliminary Submission Phase  
**Instructions:** This document provides the exact, audited, word-count-verified responses ready to copy and paste directly into the official competition PDF templates located in `submission/`.

---

# FORM 1: Preliminary Project Proposal (`SDC2026_TeamName_Preliminary.pdf`)

### Section 1 — Team and Project Overview (Page 2)
- **Team Name:** `[Insert Team Name from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Selected Domain:** `Domain 1 — The Aiversecity Future-Ready Workforce Domain`
- **Selected SDG Track (1–17):** `SDG 8 (Decent Work & Economic Growth: Targets 8.2, 8.5) & SDG 4 (Quality Education: Targets 4.3, 4.4)`
- **Project / Solution Name:** `National AI Workforce Reskilling & Foresight Engine (AI Skills Compass)`
- **Name (Leader):** `[Insert Team Leader Name from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Email & Phone (Leader):** `[Insert Leader Email & Phone from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **University Affiliation(s):** `[Insert University Affiliation from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Number of Team Members:** `[Insert Team Size (1–5) from artifacts/FINAL_USER_INPUT_REQUIRED.md]`

---

### Section 2 — Executive Summary & Problem Statement (Pages 3–4)

#### 2.1. The Problem Context *(Word Limit: Maximum 250 words | Actual: 172 words — PASS)*
Artificial intelligence is transforming Malaysia's labor market faster than traditional vocational training and higher education pipelines can respond. According to the Hays Asia Salary Guide 2025, 56% of Malaysian professionals already utilize generative AI tools in daily workflows, yet only 26% have received structured organizational training. Furthermore, the Ministry of Science, Technology and Innovation (MOSTI) estimates that over 600,000 Malaysian workers will require significant reskilling within the next 3 to 5 years to remain economically productive under the New Industrial Master Plan (NIMP 2030) and National Energy Transition Roadmap (NETR).

Working adults in clerical, routine operations, customer administration, and software testing face accelerated task transformation, while graduates struggle to map emerging AI proficiencies to sustainable career pathways. Existing career guidance tools suffer from critical deficiencies: they rely on static, unvalidated skill lists; commercial conversational chatbots exhibit hallucination and privacy risks under Malaysia's Personal Data Protection Act (PDPA) 2010; and enterprise planning lacks privacy-preserving aggregation, creating worker surveillance fears. Workforce analytics tools frequently conflate research publication volume with local job vacancies, misleading learners on actual hiring demand.

#### 2.2. The Proposed AI Solution *(Word Limit: Maximum 300 words | Actual: 254 words — PASS)*
The National AI Workforce Reskilling & Foresight Engine (interfaced via AI Skills Compass) is a deployed, privacy-preserving workforce intelligence platform bridging macro national planning with granular worker reskilling. Operating across a verified 12-engine architecture, it guides workers through an explainable pipeline:

1. **Privacy-Safe Intake & Skills Extraction (M1):** Evaluates synthetic worker profiles or unpersisted text using a hybrid blend model calibrated to the Malaysia Standard Classification of Occupations (MASCO 2020), storing zero personally identifiable information (PII).
2. **Longitudinal Trend Intelligence (M2):** OpenAlex scholarly literature and ILO 2025 standards drive shrinkage-calibrated skill velocity and scarcity indices, transparently distinguishing research publication momentum from local employer vacancy counts.
3. **Multi-Criteria Role Matching & Pathways (M3 & M4):** Computes explainable competency readiness scores across MASCO roles, constructing sequential, dependency-aware reskilling curricula paced at a sustainable 5 to 8 hours per week without fabricating commercial courses.
4. **Macroeconomic Scenario Stress-Testing (M6):** Evaluates career resiliency across 4 macroeconomic environments (Baseline, NETR Green Transition, NIMP Digital Boom, and Supply Disruption).
5. **Causal UN SDG Alignment (M5 & O6):** Quantifies individual and collective capability alignment to UN Sustainable Development Goals (SDGs 4, 8, 9, 13) using explicit causal relation types (DIRECT, ENABLING, CONTEXTUAL).
6. **Enterprise Governance & Operational Services (O1–O5):** Delivers HR cohort gap heatmaps with k-anonymity (k=5) small-cell suppression (O1), automatic replanning with human acknowledgement gates (O2), trilingual accessibility in EN, BM, and ZH with 90.6% payload compression (O3), sovereign milestone tracking (O4), and mathematical demographic neutrality (O5).

---

### Section 3 — Technical Architecture & Implementation Plan (Pages 5–6)

#### 3.1. Conceptual Tech Stack
- **Frontend / Client Experience:** Responsive, high-contrast HTML5/CSS3 Data-Dense Dashboard supporting Quantum Dark and Daylight Slate themes, 10 modular tabs, client-side low-bandwidth toggle (90.6% transfer reduction), and full WCAG AA compliance.
- **Backend Service Architecture:** Multi-threaded Python 3 HTTP Server (`src/main.py`) exposing 9 RESTful endpoints with sub-10ms CPU inference and zero external runtime API keys.
- **Data & Ingestion Pipeline:** Longitudinal scholarly publications from the OpenAlex REST API (CC0 1.0) and arXiv Atom 1.0 feed, backed by a validated dated snapshot (`data/signals_snapshot.json`) and MOHR MASCO 2020 taxonomy.
- **Sponsor Cloud Platform:** Configured for Replit Autoscale deployment (`.replit` with Python 3.11, port 5000, 0.0.0.0 binding).
- **Core Engine Framework:** 12 formally frozen engines (M1–M6, O1–O6) signed under immutable SHA-256 manifests.

#### 3.2. Design-Thinking & Deployment Strategy *(Word Limit: Maximum 200 words | Actual: 147 words — PASS)*
Our implementation follows human-centered design principles aligned with sovereign workforce needs:
1. **Empathize & Define:** Targeted the 30-percentage-point formal training deficit identified in the Domain 1 brief (Hays 2025), prioritizing learner sovereignty, zero PII retention, and transparent epistemic boundaries.
2. **Modular Architecture:** Engineered 6 Core Mathematical Engines (M1–M6) and 6 Operational Services (O1–O6), each cryptographically signed and frozen under immutable SHA-256 manifests to prevent unauthorized logic drift.
3. **Inclusive Deployment:** Delivered a production Python application on Replit Autoscale with zero runtime secrets and sub-10ms CPU inference. Built full trilingual catalogs (English, Bahasa Melayu, Chinese) across 142 keys and an ultra-lightweight low-bandwidth mode achieving 90.6% data transfer compression for rural connectivity.
4. **Rigorous Verification:** Validated through 361 automated unit and HTTP integration tests, complete secret elimination scans across 755 files, and empirical counterfactual demographic invariance testing confirming zero score delta across demographic attributes.

---

### Section 4 — Environmental & SDG Impact Framework (Pages 7–9)

| Metric Category | Verified Submission Response |
| :--- | :--- |
| **Target SDG Sub-Target(s)** | • **SDG 8.2 & 8.5**: Productive employment, economic diversification, and technological upgrading.<br>• **SDG 4.3 & 4.4**: Equal access to affordable technical/vocational reskilling and digital competencies.<br>• **SDG 9.4 & 9.5**: Upgrading technological infrastructure and industrial sustainability research capabilities.<br>• **SDG 13.3**: Climate action education and carbon-aware computing analytics. |
| **Current Problem Baseline** | **30 percentage-point formal AI training deficit in Malaysia** (56% of Malaysian professionals use AI tools at work, but only 26% have received structured formal training — *Hays Asia Salary Guide 2025*), alongside **600,000+ Malaysian workers** projected by MOSTI to require rapid capability reskilling. |
| **Core Measurable KPI** | 1. **Signal & Provenance Traceability (%)**: 100% of recommendations backed by verifiable dated source records (OpenAlex DOI or accredited public learning portals).<br>2. **Decision Turnaround Latency**: Profile analysis to multi-scenario reskilling roadmap generated in < 120 seconds user journey (< 10 ms CPU compute).<br>3. **Compute Energy Efficiency**: 0 GPU watt-hours consumed for standard inference; right-sized Python CPU execution. |
| **Planned Production Impact** | Scaling nationwide enterprise cohort gap analysis with strict k=5 small-cell masking; delivering accredited public training pathways (*AI Untuk Rakyat*, *HRD Corp e-LATiH*, *UN CC:e-Learn*) across English, Bahasa Melayu, and Chinese with rural low-bandwidth accessibility. |

---

### Section 5 — Eligibility & Readiness Checklist (Page 10)
- [x] All team members have completed the mandatory GenAI, Database, and Cloud Deployment upskilling workshops.
- [x] The project concept addresses a verified real-world problem mapped directly to one or more UN SDGs.
- [x] The proposed solution targets a functional, deployed application rather than a theoretical business case study.
- [x] All fields in this template have been completed within the word limits stated.

---

### Section 6 — IP & Originality Declaration (Pages 11–13)
- **6.1. Pre-Existing / Prior-Owned Work:** `No` (All project code developed during the official SDC 2026 hackathon window starting from the official SDC GitHub template).
- **6.2. Third-Party Code, Datasets, or Models:** `Yes`
  | Name | Type | License | Attribution |
  | :--- | :--- | :--- | :--- |
  | Official SDC GitHub Submission Template | Code Template | Apache 2.0 | Base directory scaffolding and configuration |
  | Python 3 Standard Library | Runtime | PSF License | HTTP server, regex tokenization, JSON parsing, unittest |
  | OpenAlex Public REST API & Snapshot | Scholarly Dataset | CC0 1.0 Public Domain | Longitudinal research literature signals |
  | arXiv Public Atom API | Research Preprints | Public Metadata Terms | Secondary research activity fallback |
  | MASCO 2020 Taxonomy | Occupational Framework | Public Attribution | MOHR Malaysia occupational classifications |
  | Google Fonts (`Fira Sans`, `Fira Code`) | Typography Assets | SIL Open Font License 1.1 | Accessible typography |
- **6.3. Employment-Related IP Conflicts:** `No`

---

### Section 7 — Declaration (Page 14)
- **Signature:** `[Insert Team Leader Signature from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Date:** `[Insert Date on or before 25 October 2026, 7:59:59 AM MYT]`

---
---

# FORM 2: Technical Tools Declaration (`SDC2026_TeamName_TechDeclaration.pdf`)

### Section 1 — Team and Project Overview (Page 2)
- **Team Name:** `[Insert Team Name from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Project / Solution Name:** `National AI Workforce Reskilling & Foresight Engine (AI Skills Compass)`
- **Name (Leader):** `[Insert Team Leader Name from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Email & Phone (Leader):** `[Insert Leader Email & Phone from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **University Affiliation(s):** `[Insert University Affiliation from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Live Prototype URL:** `[Insert Replit URL from artifacts/FINAL_USER_INPUT_REQUIRED.md, or see artifacts/REPLIT_MANUAL_PUBLISH_STEPS.md]`
- **Code Repository URL:** `https://github.com/Codinggeniusnks/sdc-domain1-prototype`

---

### Section 2 — Architecture & Technology Stack (Pages 3–4)

#### 2.1. System Architecture Overview *(Word Limit: Maximum 200 words | Actual: 172 words — PASS)*
The National AI Workforce Reskilling & Foresight Engine implements an auditable 12-engine architecture hosted on Replit:
1. **Presentation & Gateway Layer (`src/main.py`, `src/presentation_layer.py`):** Multi-threaded HTTP server exposing a 10-tab responsive dashboard (Quantum Dark and Daylight Slate themes) and 9 public REST APIs (`/api/health`, `/api/evaluate`, `/api/employer`, `/api/replan`, `/api/progress`, `/api/governance`, `/api/audit-ledger.json`, `/api/signals`, `/api/locales/{lang}`). Supports trilingual localization (EN, BM, ZH) and low-bandwidth operation (90.6% compression).
2. **Core Mathematical Engines (M1–M6):** Ingests dated OpenAlex scholarly publications (CC0) and arXiv feeds; extracts MASCO 2020 competencies via hybrid model M1; calculates shrinkage-calibrated velocity and scarcity via M2; matches roles via multi-criteria M3; builds paced 5–8 hrs/week curricula via M4; attributes causal UN SDG relations via M5; and simulates 4 labor shock scenarios via M6.
3. **Operational & Governance Layer (O1–O6):** Aggregates enterprise workforce gaps with k=5 small-cell suppression (O1); detects upstream signal shifts with human confirmation gates (O2); tracks sovereign micro-credentials and non-competitive badges (O4); verifies counterfactual demographic neutrality (O5); and aggregates collective sustainability alignment (O6).

#### 2.2. Languages, Frameworks & Libraries
| Name & Version | License | Purpose in Project |
| :--- | :--- | :--- |
| Python 3.11 Standard Library (`http.server`, `urllib`, `json`, `html`, `re`, `unittest`) | PSF License | Primary web application runtime, 9 REST APIs, regex taxonomy parsing, and 361-test automated QA harness |
| SDC Submission Base Template | Apache 2.0 | Base project directory structure and Replit deployment bindings |
| Google Fonts (`Fira Sans`, `Fira Code`) | SIL OFL 1.1 | High-legibility dashboard typography |

---

### Section 3 — APIs & Cloud Services (Pages 5–6)

#### 3.1. External APIs
| API and Provider | Access Tier | Purpose in Project |
| :--- | :--- | :--- |
| OpenAlex REST API (`api.openalex.org/works`, OurResearch) | Free (Public unauthenticated CC0 1.0) | Primary longitudinal scholarly publications feed tracking technical capability momentum |
| arXiv Public Atom API (`export.arxiv.org/api/query`, Cornell) | Free (Public unauthenticated) | Secondary live research preprint fallback feed |
| Google Fonts CSS API (`fonts.googleapis.com`) | Free | Serves typography assets |

#### 3.2. Cloud Platforms & Deployment
| Service & Provider | Plan / Region | Purpose in Project |
| :--- | :--- | :--- |
| Replit (`replit.com`) | Sponsor-Provided Core Allocation | Cloud hosting environment (`python src/main.py`), dynamic Autoscale deployment |
| GitHub (`github.com`) | Public Open Source | Source code repository (`sdc-domain1-prototype`), commit tracking, and version control |

---

### Section 4 — AI Tools, Models & Datasets (Pages 7–10)

#### 4.1. AI Models Used in the Running Solution *(Runtime Application)*
| Model & Version | Source / Provider | License | Usage |
| :--- | :--- | :--- | :--- |
| M1 Skills Extraction Engine (`H_blend_0.70A_0.30C1_W1.0`) | In-house hybrid blend calibrated on MASCO 2020 | Apache 2.0 | Extracts taxonomy skills from input text with zero PII retention; evaluated with Protocol B/C single unseal |
| M2 Trend Intelligence Model (`v1.1.1`) | In-house OpenAlex shrinkage model | Apache 2.0 | Computes velocity ($V$) and scarcity ($S$) indices from dated publications |
| M3 Future-Role Matching Engine (`v1.1.0`) | In-house multi-criteria ranking algorithm | Apache 2.0 | Ranks MASCO 2020 role suitability with explainable score breakdowns |
| M6 Scenario Simulation Model (`v1.1.0`) | In-house macroeconomic shock simulator | Apache 2.0 | Models competency demand shifts across 4 policy scenarios |

#### 4.2. Datasets
| Dataset Name | Source / URL | Type | Personal Data? | License |
| :--- | :--- | :--- | :--- | :--- |
| OpenAlex Scholarly Publications & Snapshot | `api.openalex.org/works` (DOIs) | Public Research Literature | No | CC0 1.0 |
| arXiv Preprints Feed | `export.arxiv.org/api/query` | Public Research Metadata | No | Public Terms |
| MASCO 2020 Occupational Taxonomy | MOHR Malaysia (`mohr.gov.my`) | Public Taxonomy | No | Public Attribution |
| Synthetic Malaysian Personas | `src/taxonomy.py` | Synthetic Testbed | No | Apache 2.0 |
| Synthetic Enterprise Workforce Testbed | `data/workforce/` | Synthetic ($N=100$) | No | Apache 2.0 |

#### 4.3. AI-Assisted Development Tools *(Offline Development & Code Generation)*
- **Generative AI Used for Development?**: `Yes`
  | Tool & Model Display Name | Extent | Contribution |
  | :--- | :--- | :--- |
  | Google Antigravity IDE (`Gemini 3.8 Flash` & `Gemini 4 Argon`) | Major | Architecture synthesis, writing M1–M6 and O1–O6 engines, automated unit test development (361 tests), and freeze audits |
  | Antigravity Built-in Skills (`find-docs`, `playwright-cli`, `ui-ux-pro-max`) | Moderate | Documentation research, accessibility audit, and CSS design tokens |

- **Review, Testing & Responsibility for AI Output *(Word Limit: Maximum 100 words | Actual: 95 words — PASS)*:**
  Our team takes full institutional responsibility for all AI-assisted code and documentation. During autonomous testing and independent audits, we confirmed that all 12 modules operate deterministically at runtime with zero ungrounded generative generation. We verified that 361 automated unit, integration, and freeze-integrity tests pass cleanly across 24 test suites. Security scanning across 755 repository files verified zero committed secrets or PII. We validated that Protocol B and Protocol C v2 were unsealed exactly once during Stage 8E for final frozen M1 evaluation, and verified demographic invariance produces zero score delta across counterfactual attributes.

---

### Section 5 — Sponsor-Provided Resources (Pages 11–12)
- **Sponsor Resources Used?**: `Yes`
  | Sponsor | Resource | How It Was Used |
  | :--- | :--- | :--- |
  | Replit | Replit Core | Primary cloud runtime deployment (`python src/main.py`) via `.replit` Autoscale |
  | Aiversecity | Domain 1 Brief & Problem Framework | Contextual benchmarks (Hays 2025, MOSTI) and ethics criteria |

- **Sponsor Resource Essentiality *(Word Limit: Maximum 100 words | Actual: 76 words — PASS)*:**
  Replit Core provides streamlined cloud hosting, instant webview validation, and continuous runtime execution for our judge demonstration, while Aiversecity's Domain 1 problem framework provided vital Malaysian training deficit context and ethical guardrails. Because our core system is engineered in portable Python 3 standard library with zero runtime external API keys or proprietary cloud dependencies, the entire platform can also be deployed seamlessly on local machines, institutional private clouds, or containerized Linux environments without vendor lock-in.

---

### Section 6 — Security, Privacy & Responsible Use (Pages 13–14)

#### 6.1. Data Handling & Privacy *(Word Limit: Maximum 150 words | Actual: 96 words — PASS)*
In strict compliance with Domain 1 Rule §6 and Malaysia's Personal Data Protection Act (PDPA) 2010, the engine stores zero real personal data. All user evaluation executes on synthetic personas or unpersisted session text held ephemerally in URL parameters. Outbound network traffic queries only public, unauthenticated scholarly metadata (OpenAlex CC0 and arXiv Atom API). In enterprise workforce analytics (O1), strict k-anonymity (k=5) small-cell suppression masks any cohort sub-group with fewer than 5 members, preventing employee reverse-identification. An automated repository security audit across 755 files verified zero committed credentials, personal CVs, or private keys.

#### 6.2. Known Limitations & Risks *(Word Limit: Maximum 150 words | Actual: 121 words — PASS)*
1. **Scholarly Activity vs. Hiring Vacancies:** OpenAlex and arXiv measure global academic research activity around emerging competencies, not Malaysian job vacancies or wage distributions. *Mitigation:* Dashboards and APIs explicitly label signals as scholarly research metrics and cite official dated sources.
2. **Advisory Decision Support Only:** In accordance with AI ethics guidelines, the system is strictly prohibited from executing automated hiring, termination, or wage decisions.
3. **External Feed Fallback:** Live scholarly APIs may experience transient outages. *Mitigation:* Multi-tier fallback switches automatically to a dated 17-record snapshot with clear amber UI status badging.
4. **Privacy Safeguard Scope:** k=5 small-cell masking provides robust prototype cell suppression against deductive disclosure, but does not constitute formal epsilon-differential privacy.

---

### Section 7 — Compliance & Readiness Checklist (Page 15)
- [x] All APIs, cloud services, AI tools, models, and datasets used in the project are declared in this document.
- [x] All third-party code, datasets, and models are used in accordance with their licenses, and attribution is provided where required.
- [x] No API keys, passwords, or other credentials are exposed in the code repository, prototype, or this document.
- [x] Any use of generative-AI tools for development has been disclosed and reviewed by the team.
- [x] Any use of official SDC sponsor resources has been declared in Section 5.
- [x] The prototype described here is accessible to judges through the links provided in Section 1.
- [x] All fields in this template have been completed within the word limits stated.

### Section 8 — Declaration (Page 16)
- **Signature:** `[Insert Team Leader Signature from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Date:** `[Insert Date on or before 25 October 2026, 7:59:59 AM MYT]`

---
---

# FORM 3: Replit Proof-of-Usage (`SDC2026_TeamName_Replit_POU.pdf`)
- **Team Name:** `[Insert Team Name from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Project Name:** `National AI Workforce Reskilling & Foresight Engine (AI Skills Compass)`
- **Repl Title / URL:** `[Insert Replit URL from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Repository URL:** `https://github.com/Codinggeniusnks/sdc-domain1-prototype`
- **Replit Core Usage Description:**
  The project was developed and configured on Replit using the official SDC GitHub template. The runtime operates under Python 3.11 with an Autoscale deployment (`.replit`), binding to `0.0.0.0:5000` and serving the 10-tab dashboard and 9 REST endpoints.
- **Verification Screenshot Evidence:** Attach screenshot of running Replit workspace showing `python src/main.py` serving on port 5000 with Webview rendered.

---

# FORM 4: RunPod Proof-of-Usage (`SDC2026_TeamName_Runpod_POU.pdf`)
- **Team Name:** `[Insert Team Name from artifacts/FINAL_USER_INPUT_REQUIRED.md]`
- **Project Name:** `National AI Workforce Reskilling & Foresight Engine (AI Skills Compass)`
- **RunPod Usage Status / Declaration:**
  In alignment with environmental sustainability and compute energy efficiency (SDG 7.3 and SDG 13), our production web application runs entirely on efficient Python CPU inference (<10ms latency). RunPod Serverless was prepared as an optional batch extraction handler (`runpod/handler.py`). The US$25 credit was preserved as the CPU pipeline already delivered 100% of required functionality without GPU energy overhead.
