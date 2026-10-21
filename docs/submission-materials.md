# Official Submission Materials, Declaration & 5–7 Minute Pitch Outline (Prompt 8 — Synchronized with Audited Codebase)

> [!NOTE]
> **Skill & Audit Status Report (`pdf`, `find-docs`, `playwright-cli`, `code-review`)**:
> - The `pdf` skill is not installed in this Antigravity environment; instead, we extracted the exact text of every page of the official PDF templates in `submission/` (`SDC2026_TeamName_Preliminary.pdf` [14 pages], `SDC2026_TeamName_TechDeclaration.pdf` [16 pages], `SDC2026_TeamName_Replit_POU.pdf` [1 page], and `SDC2026_TeamName_Runpod_POU.pdf` [1 page]) and prepared exact, word-count-verified, field-by-field responses below.
> - The `find-docs` skill (`Context7` MCP `resolve-library-id` & `query-docs`) was executed to verify the arXiv API documentation (`/websites/info_arxiv_help_api`), and `playwright-cli` was executed to verify all 6 browser journeys (`docs/audit-*.png`).
> - All architecture descriptions, signal sources (OpenAlex primary + arXiv secondary + 17-record OpenAlex snapshot), formula terms (`0.55 × Skill Readiness + 0.25 × Research Signal Coverage + 0.20 × Scenario Fit`), test counts (**11 passing tests**), and Antigravity model histories below match commit `a0d710c`.

---

## Part 1: Field-by-Field Text for `submission/SDC2026_TeamName_Preliminary.pdf` (Preliminary Project Proposal)

### Section 1 — Team and Project Overview (Page 2)
- **Team Name**: `[Replace with Your Team Name]`
- **Selected Domain**: `Domain 1 — The Aiversecity Future-Ready Workforce Domain`
- **Selected SDG Track (1–17)**: `SDG 8 (Decent Work and Economic Growth) & SDG 4 (Quality Education)`
- **Project / Solution Name**: `AI Skills Compass`
- **Name (Leader)**: `[Replace with Team Leader Full Name]`
- **Email & Phone (Leader)**: `[Replace with Leader Email & Phone Number]`
- **University Affiliation(s)**: `[Replace with Recognised Malaysian Higher Education Institution(s)]`
- **Number of Team Members**: `[Replace with 1–5]`

---

### Section 2 — Executive Summary & Problem Statement (Pages 3–4)

#### 2.1. The Problem Context *(Word Limit: Maximum 250 words | Actual: 184 words)*
AI is reshaping Malaysia's workforce faster than static university curricula and corporate training calendars can adapt. According to the Hays Asia Salary Guide 2025 (quoted in the SDC 2026 Domain 1 problem brief), 56% of Malaysian professionals already use AI tools at work, yet only 26% have received formal training. Furthermore, the Ministry of Science, Technology and Innovation (MOSTI, also quoted in the Domain 1 brief) projects that more than 600,000 Malaysian workers will require reskilling within the next three to five years.

Working adults in routine operations, quality assurance, and administrative analysis face displacement risk, while fresh graduates and career switchers struggle to identify which emerging technical skills truly lead to resilient roles. Existing career tools fail in three ways: first, they rely on static skill lists that are outdated upon publication; second, generic "upload your CV to a chatbot" wrappers risk exposing personal data and hallucinate unverified courses, statistics, or job guarantees; and third, they ignore how emerging technical roles contribute to global sustainability under the 17 UN Sustainable Development Goals (SDGs).

#### 2.2. The Proposed AI Solution *(Word Limit: Maximum 300 words | Actual: 236 words)*
**AI Skills Compass** is a deployed web application that guides Malaysian workers and graduates from *"who I am today"* to *"where I can be in the AI era"* through an auditable, four-stage pipeline:

1. **Privacy-Safe Skills Profile Intake**: Users select or customize a synthetic skills and interest profile without uploading personally identifiable CVs.
2. **Dated AI Research Signal Layer**: A live signal adapter (`src/signals.py`) queries the public **OpenAlex REST API** (`https://api.openalex.org/works`, CC0 1.0) as the primary live feed and the **arXiv Atom 1.0 API** (`http://export.arxiv.org/api/query`) as the secondary live fallback, backed by an explicitly badged dated snapshot of **17 verbatim OpenAlex scholarly records** (`data/signals_snapshot.json`, generated via `scripts/refresh_snapshot.py`) when offline. The UI explicitly states that these signals measure **scholarly AI research activity**, not employer job postings or vacancy counts. Whole-word regex extraction constrains every signal to our 16-skill catalog (`src/taxonomy.py`) so the system never invents skills or jobs.
3. **Explainable Multi-Scenario Role Matcher**: Roles are ranked via an inspectable formula (`0.55 × Skill Readiness + 0.25 × Research Signal Coverage + 0.20 × Scenario Fit`) across three explicit future scenarios (*Moderate Co-Pilot Adoption*, *Fast Agentic Disruption*, and *Accelerated SDG & Green-Tech Transition*). Sparse profiles or malformed/future-dated/stale signals trigger an honest `"Insufficient Evidence"` guardrail.
4. **Ordered Low-Cost Pathway & SDG Mapping**: Each role generates a step-by-step learning plan citing free public resources (*AI Untuk Rakyat*, *HRD Corp e-LATiH*, *UN CC:e-Learn*, *NIST AI RMF*) or explicit skill objectives, mapped to UN SDG sub-targets (4.3, 4.4, 7.3, 8.2, 8.5, 9.5, 10.3, 13.2, 16.6).

---

### Section 3 — Technical Architecture & Implementation Plan (Pages 5–6)

#### 3.1. Conceptual Tech Stack
- **Frontend**: Responsive, accessible HTML5/CSS3 Data-Dense Dashboard (`Fira Sans` / `Fira Code`, WCAG AA >=4.5:1 contrast, keyboard focus states, reduced-motion support).
- **Backend**: Python 3 Standard Library (`http.server.ThreadingHTTPServer`, `urllib.request`, `xml.etree.ElementTree`, `json`) running on **Replit** (`python src/main.py`).
- **Data & Signal Layer**: Primary live JSON ingestion from the **OpenAlex REST API** (`https://api.openalex.org/works`) + secondary live Atom 1.0 XML fallback from the **arXiv API** (`http://export.arxiv.org/api/query`) + local dated OpenAlex snapshot (`data/signals_snapshot.json`, 17 verbatim DOI records refreshed via `scripts/refresh_snapshot.py`) + constrained 16-skill / 6-role taxonomy (`src/taxonomy.py`).
- **Sponsor-Provided Cloud / Compute**: Hosted and developed on **Replit Core** (official SDC sponsor platform). Optional batch taxonomy-extraction handler prepared in `runpod/handler.py` for **RunPod Serverless** (kept scale-to-zero during Phase 1 because core CPU matching executes in <10ms; `[TEAM CONFIRMATION REQUIRED: Confirm whether your team keeps the CPU-only Phase 1 path or runs a 1-request RunPod Serverless test]`).
- **System Block Diagram**:
  `Synthetic Profile Intake ──► Python Controller (src/main.py) ◄── Signal Adapter (src/signals.py) ◄── 1. Primary Live OpenAlex API / 2. Secondary Live arXiv API / 3. Dated OpenAlex Snapshot Fallback (17 records)`
  `Python Controller ──► Explainable Matcher & Scenario Engine (src/matcher.py) + Constrained Taxonomy (src/taxonomy.py) ──► Ranked Role Cards + Skill Gaps + Ordered Free/Low-Cost Pathway + UN SDG Impact Map`

#### 3.2. Design-Thinking & Deployment Strategy *(Word Limit: Maximum 200 words | Actual: 169 words)*
We structured our prototype around a four-stage design-thinking workflow tailored to Malaysian learners:
1. **Empathize**: Grounded synthetic personas in the 30-percentage-point training gap quoted in the Domain 1 brief (Hays Asia Salary Guide 2025: 56% using AI informally vs. 26% formally trained) across operations, QA, and sustainability roles.
2. **Define**: Framed the core failure mode of career chatbots—false confidence, conflating research buzz with job vacancies, and hallucinating courses—and established strict guardrails: zero real PII, mandatory dated source citations, explicit distinction between research activity and hiring demand, and uncertainty bands.
3. **Ideate & Prototype**: Built a deterministic, zero-secret Python web application for Replit where every score decomposes visibly into Skill Readiness (55%), Research Signal Coverage (25%), and Scenario Fit (20%), backed by a live OpenAlex feed and an automatic 17-record OpenAlex snapshot fallback.
4. **Test & Phase 2 Evolution**: Verified with **11 automated unit and HTTP integration tests** (`tests/test_utils.py`). In Phase 2, we plan to add an Employer/HR cohort skills-gap heatmap.

---

### Section 4 — Preliminary Environmental & SDG Impact Framework (Pages 7–9)

| Metric Category | Your Response |
| :--- | :--- |
| **Target SDG Sub-Target(s)** | • **SDG Target 4.4**: *"By 2030, substantially increase the number of youth and adults who have relevant skills, including technical and vocational skills, for employment, decent jobs and entrepreneurship."*<br>• **SDG Target 4.3**: Equal access to affordable technical and vocational reskilling.<br>• **SDG Target 8.2**: Higher economic productivity through technological upgrading and innovation.<br>• **SDG Target 8.5**: Full and productive employment and decent work for all.<br>• **SDG Target 7.3 & 13.2**: Compute energy efficiency (right-sizing CPU vs. GPU workloads) and ESG telemetry skills. |
| **Current Problem Baseline** | **30 percentage-point formal AI training deficit in Malaysia** (56% of Malaysian professionals use AI tools at work, but only **26%** have received formal training — *Hays Asia Salary Guide 2025*, as quoted in the Domain 1 Brief p. 2) alongside **600,000+ Malaysian workers** projected by MOSTI (quoted in the Domain 1 Brief p. 2) to need reskilling within 3–5 years. Additionally, ungrounded LLM career prompts exhibit high hallucination rates on unverified course URLs and prices. |
| **Core Measurable KPI** | 1. **Citation & Provenance Coverage (%)**: Percentage of role and pathway recommendations backed by a verifiable, dated source URL (resolving OpenAlex DOI or public learning portal) and explicit uncertainty band (Target: **100%**).<br>2. **Time-to-Actionable Reskilling Plan (seconds/minutes)**: End-to-end time for a learner to move from profile intake to a ranked role, skill-gap breakdown, and free/low-cost pathway (< **120 seconds** user journey; < **10 ms** compute latency).<br>3. **Compute Energy Efficiency**: 0 GPU watt-hours consumed for deterministic role matching on Replit CPU. |
| **Phase 2 Impact Target** | • **100% source-citation traceability** (0% fabricated jobs, courses, or statistics across all 16 taxonomy skills and 6 target roles).<br>• **Faster pathway assembly** by consolidating cross-referenced, SDG-mapped, low-cost reskilling steps across public portals (*AI Untuk Rakyat*, *HRD Corp e-LATiH*, *UN CC:e-Learn*, *NIST AI RMF*) into a single inspectable view `[TEAM CONFIRMATION REQUIRED: Confirm whether your team wants to commit to a specific Phase 2 user-testing target]`. |

---

### Section 5 — Eligibility & Readiness Checklist (Page 10)
*`[TEAM CONFIRMATION REQUIRED: Team Leader must verify all 4 checkboxes below before ticking in the final PDF]`*
- [ ] All team members have completed the mandatory GenAI, Database, and Cloud Deployment upskilling workshops.
- [ ] The project concept addresses a verified real-world problem mapped directly to one or more UN SDGs.
- [ ] The proposed solution targets a functional, deployed application rather than a theoretical business case study.
- [ ] All fields in this template have been completed within the word limits stated.

---

### Section 6 — IP & Originality Declaration (Pages 11–13)
*`[TEAM CONFIRMATION REQUIRED: Team Leader must confirm IP and employment-conflict answers below]`*
- **6.1. Pre-Existing / Prior-Owned Work**: `No` *(Built during the official SDC Hackathon 2026 period starting from the official SDC GitHub Submission Template).*
- **6.2. Third-Party Code, Datasets, or Models**: `Yes`
  | Name | Type (code/dataset/model) | License |
  | :--- | :--- | :--- |
  | Official SDC GitHub Submission Template (`michaelzhngg/SDC_Hackathon_Submission_Template`) | Code Template | Apache License 2.0 |
  | Python 3.12 Standard Library (`http.server`, `urllib`, `xml.etree.ElementTree`, `json`, `unittest`) | Code Runtime / Standard Library | PSF License |
  | OpenAlex Public REST API (`https://api.openalex.org/works`) & 17-Record Dated Snapshot (`data/signals_snapshot.json`) | Public Scholarly Research Dataset / Feed | CC0 1.0 Universal Public Domain Dedication |
  | arXiv Public Atom API (`http://export.arxiv.org/api/query`) | Secondary Public Research Feed | arXiv API Terms of Use (Public Metadata Attribution) |
  | Google Fonts (`Fira Sans`, `Fira Code`) | Typography Assets | SIL Open Font License 1.1 |
  | Domain 1 Problem Brief Benchmarks (Hays Asia Salary Guide 2025; MOSTI) & Public Course Portals (AI Untuk Rakyat; HRD Corp e-LATiH; UN CC:e-Learn; NIST AI RMF) | Quoted Context Figures & Linked Public Learning Portals | Public Attribution |
- **6.3. Employment-Related IP Conflicts**: `No`

### Section 7 — Declaration (Page 14)
- **Signature**: `[Replace with Team Leader Signature]`
- **Date**: `[Replace with Submission Date, on or before 25 October 2026, 7:59:59 AM MYT]`

---

## Part 2: Field-by-Field Text for `submission/SDC2026_TeamName_TechDeclaration.pdf` (Technical Tools Declaration)

### Section 1 — Team and Project Overview (Page 2)
- **Team Name**: `[Replace with Your Team Name]`
- **Project / Solution Name**: `AI Skills Compass`
- **Name (Leader)**: `[Replace with Team Leader Full Name]`
- **Email & Phone (Leader)**: `[Replace with Leader Email & Phone Number]`
- **University Affiliation(s)**: `[Replace with Recognised Malaysian Higher Education Institution(s)]`
- **Live Prototype URL**: `[Replace with Live Replit Deployment URL, e.g., https://your-project.replit.app]`
- **Code Repository URL**: `[Replace with Your Team's GitHub Repository URL]`

---

### Section 2 — Architecture & Technology Stack (Pages 3–4)

#### 2.1. System Architecture Overview *(Word Limit: Maximum 200 words | Actual: 174 words)*
**AI Skills Compass** follows a modular, four-layer architecture hosted on Replit:
1. **Presentation Layer (`src/main.py`)**: Serves a server-rendered, accessible HTML5/CSS3 dashboard and JSON REST endpoints (`/api/evaluate`, `/api/signals`, `/api/health`). Users select or customize a synthetic persona, toggle between three future disruption scenarios, and switch signal modes.
2. **Signal Ingestion & Validation Layer (`src/signals.py`)**: Queries the public **OpenAlex REST API** (`https://api.openalex.org/works`, CC0) as the primary live scholarly research feed, with the **arXiv Atom 1.0 API** (`http://export.arxiv.org/api/query`) as a secondary live fallback. If offline, it loads `data/signals_snapshot.json` (17 verbatim OpenAlex DOI records refreshed via `scripts/refresh_snapshot.py`) and badges the UI as fallback data. `validate_signals()` strips malformed, undated, future-dated, or stale records.
3. **Constrained Taxonomy Layer (`src/taxonomy.py`)**: Defines 16 canonical skills (matched via whole-word regex), 6 future roles, free/low-cost learning pathways, and UN SDG sub-target links.
4. **Explainable Matching Engine (`src/matcher.py`)**: Computes deterministic role scores (`0.55 × Skill Readiness + 0.25 × Research Signal Coverage + 0.20 × Scenario Fit`) and halts on sparse evidence.

#### 2.2. Languages, Frameworks & Libraries
| Name & Version | License | Purpose in Project |
| :--- | :--- | :--- |
| Python 3.11 / 3.12 Standard Library (`http.server`, `urllib`, `xml.etree`, `json`, `re`, `unittest`) | PSF License | HTTP web server, OpenAlex JSON & arXiv Atom XML fetching/parsing, whole-word regex extraction, JSON API, and 11-test automated unit/integration test suite |
| Official SDC Submission Template (`SDC_Hackathon_Submission_Template`) | Apache License 2.0 | Base repository directory layout, `.replit` configuration, and utility test harness |
| Google Fonts (`Fira Sans`, `Fira Code`) | SIL Open Font License 1.1 | Accessible dashboard typography and monospace formula/date rendering |
| `runpod` Python SDK (listed in `requirements.txt`) | MIT License | Optional Serverless GPU handler interface in `runpod/handler.py` (not imported by the Replit web server) |

---

### Section 3 — APIs & Cloud Services (Pages 5–6)

#### 3.1. External APIs
| API and Provider | Access Tier (free / paid / sponsor-provided) | Purpose in Project |
| :--- | :--- | :--- |
| OpenAlex REST API (`https://api.openalex.org/works`, OurResearch) | Free (Public unauthenticated REST JSON API, CC0 1.0) | Primary live feed of dated scholarly AI publications (`2026-09-04` to `2026-10-17`) and source of the 17-record dated snapshot (`data/signals_snapshot.json`) used to compute Research Signal Coverage |
| arXiv Public Atom API (`http://export.arxiv.org/api/query`, Cornell University) | Free (Public unauthenticated REST/Atom XML API) | Secondary live fallback feed for dated AI research preprints (`cs.AI`, `cs.CL`, `cs.CY`, `cs.SE`) |
| Google Fonts CSS API (`https://fonts.googleapis.com`) | Free | Loads `Fira Sans` and `Fira Code` web fonts in browser |

#### 3.2. Cloud Platforms & Deployment
| Service & Provider | Plan / Region | Purpose in Project |
| :--- | :--- | :--- |
| Replit (`replit.com`) | Sponsor-Provided Replit Core (US$20 credit) / Global | Primary cloud IDE, runtime environment (`python src/main.py`), Secrets management, and live prototype web hosting |
| GitHub (`github.com`) | Free Tier | Source code version control, continuous commit history, and submission template structure |
| RunPod (`runpod.io` — Optional Serverless Handler) | Sponsor-Provided Credit (US$25 credit preserved) | Optional serverless batch taxonomy extractor (`runpod/handler.py`); not required in critical Replit demo path |

---

### Section 4 — AI Tools, Models & Datasets (Pages 7–10)

#### 4.1. AI Models Used in the Running Solution *(Runtime Application)*
| Model & Version | Source / Provider | License / Terms | Usage (pre-trained / fine-tuned / self-trained) |
| :--- | :--- | :--- | :--- |
| **None embedded in the running application** (Deterministic Whole-Word Regex Taxonomy & Linear Scoring Engine in `src/signals.py` and `src/matcher.py`) | In-house implementation | Apache License 2.0 | No generative AI model is called at runtime. Whole-word regex keyword extraction (`\b...\b`) and weighted linear scoring (`0.55 × Skill Readiness + 0.25 × Research Signal Coverage + 0.20 × Scenario Fit`) guarantee zero hallucinated jobs, courses, or scores |

#### 4.2. Datasets
| Dataset Name | Source / URL | Type (public / private / self-collected / synthetic) | Personal Data? (Y/N) | License |
| :--- | :--- | :--- | :--- | :--- |
| OpenAlex Live & 17-Record Dated Snapshot Signals (`data/signals_snapshot.json`) | `https://api.openalex.org/works` (each record links to its `https://doi.org/...` URL) | Public (Scholarly Research Publications, NOT vacancy data) | N | CC0 1.0 Universal Public Domain Dedication |
| arXiv Live Secondary Fallback Feed | `http://export.arxiv.org/api/query` | Public (Scholarly Preprints, NOT vacancy data) | N | arXiv API Terms of Use (Public Metadata) |
| Synthetic Malaysian Workforce Personas (`SYNTHETIC_PROFILES` in `src/taxonomy.py`) | Created for Domain 1 demo | Synthetic | N | Apache License 2.0 |
| Curated Skills, Roles, Pathways & SDG Catalog (`src/taxonomy.py`) | Grounded in Domain 1 Brief quotes (Hays Asia Salary Guide 2025; MOSTI) and public portals (`ai.gov.my`, HRD Corp e-LATiH, UN CC:e-Learn, NIST AI RMF) | Public / Self-Collected Curated Taxonomy | N | Apache License 2.0 / Public Attribution |

#### 4.3. AI-Assisted Development Tools *(Models Used to Develop & Audit the App — Separate from Runtime)*
- **Did your team use any generative-AI tool to help create code, design, text, or other project material?**: `Yes`
  | Tool & Exact Antigravity Model Display Name | Extent of Use (minor / moderate / major) | Actual Contribution to Project |
  | :--- | :--- | :--- |
  | **Google Antigravity IDE — `Gemini 4 Argon (Medium)`** *(Initial Build Session & Final Release-Doc Sync Session)* | Major | **Session 1 (Prompts 0–8):** Parsed official competition PDFs, authored `docs/competition-requirements.md`, `docs/prototype-spec.md`, `docs/data-sources.md`, `docs/runpod-decision.md`, `docs/judge-audit-report.md`, and `docs/submission-materials.md`; implemented initial `src/taxonomy.py`, `src/signals.py`, `src/matcher.py`, `src/main.py`, `runpod/handler.py`, and 9 unit tests in `tests/test_utils.py`.<br>**Session 3 (Final Sync):** Fixed UI live-signal badge labels (`LIVE RESEARCH API`) in `src/main.py`, executed the 11-test suite, committed audit fixes (`a0d710c`), and synchronized `README.md` and `docs/submission-materials.md` with the audited codebase. |
  | **Google Antigravity IDE — `Claude Opus 5.5 (Medium)`** *(Submission Readiness Audit Session)* | Moderate | **Session 2 (Submission Readiness Audit):** Audited all 29 repository files; identified that the initial 5 snapshot arXiv IDs in `data/signals_snapshot.json` did not match real arXiv titles and wrote `scripts/refresh_snapshot.py` to replace `data/signals_snapshot.json` with 17 verbatim OpenAlex API records; fixed substring false positives (`"rag"` inside `"leverage"`, `"power"` inside `"powered"`) with whole-word regex (`\b...\b`) in `src/signals.py` and refined keywords in `src/taxonomy.py`; added future-date rejection (`age_days < -1`); normalized `Research Signal Coverage` scoring in `src/matcher.py`; replaced unsupported "job-market demand" wording with explicit research-activity vs. vacancy disclosures; added 2 new unit tests (bringing `tests/test_utils.py` to **11 tests**); and ran the 6-route `playwright-cli` judge audit (`docs/audit-*.png`). |
  | **Antigravity Skills & CLI Tools (`find-docs` via Context7 MCP, `ui-ux-pro-max`, `playwright-cli`, plus `get-shit-done`, `code-review`, and `security-audit` checklists)** | Moderate | Verified arXiv API documentation (`Context7` MCP), generated accessible Data-Dense Dashboard design tokens (`ui-ux-pro-max`), and executed headless Chromium browser verification and screenshot capture (`playwright-cli`). |

- **Briefly describe how your team reviewed, tested, and took responsibility for AI-generated output** *(Word Limit: Maximum 100 words | Actual: 95 words)*:
  `[TEAM CONFIRMATION REQUIRED: Before submitting, personally review the files listed below so this statement is 100% true of your team]`
  Our team takes full responsibility for all AI-assisted code and documentation. During the submission readiness audit, we verified that the runtime application embeds zero generative AI models, uses whole-word regex matching against our 16-skill catalog (`src/taxonomy.py`), and populates `data/signals_snapshot.json` verbatim from the live OpenAlex API via `scripts/refresh_snapshot.py`. We verified that all **11 unit and HTTP integration tests** in `tests/test_utils.py` pass (covering sparse profiles, stale/malformed/future-dated signals, and scenario shifts), inspected the live browser journeys, and confirmed that research signals are never misrepresented as job-vacancy counts.

---

### Section 5 — Sponsor-Provided Resources (Pages 11–12)
- **Did your project use any official SDC sponsor-provided resource?**: `Yes`
  | Sponsor | Resource (API / credits / platform / data) | How It Was Used in the Project |
  | :--- | :--- | :--- |
  | Replit | Replit Core (US$20 participant allocation) | Used as the primary hosting and execution platform (`python src/main.py` via `.replit`) and environment variable store |
  | Aiversecity | Domain 1 Problem Statement, Hays 2025 / MOSTI Context Figures & Rubric | Used to structure the 6 must-have features, SDG sub-targets (4.3, 4.4, 8.2, 8.5), and human-in-charge guardrails |
  | RunPod | RunPod Credit (US$25 team allocation — preserved) | Evaluated for GPU necessity (`docs/runpod-decision.md`) and prepared optional serverless handler (`runpod/handler.py`); preserved credit as CPU matching runs in <10ms `[TEAM CONFIRMATION REQUIRED: Confirm whether your team runs a 1-request RunPod test for Runpod_POU.pdf]` |

- **Was the sponsor resource essential to the core functionality of the prototype, or could it be replaced? Explain briefly** *(Word Limit: Maximum 100 words | Actual: 74 words)*:
  Replit provides streamlined cloud hosting, instant webview previews, and Secret management for our live judge demonstration, while Aiversecity's Domain 1 framework shaped our problem definition and guardrails. Because the application is built on portable Python 3 standard libraries with zero proprietary lock-in, the web server can also run on any standard Linux/Windows host, while RunPod Serverless remains an optional accelerator if future corpus volume outgrows CPU matching.

---

### Section 6 — Security, Privacy & Responsible Use (Pages 13–14)

#### 6.1. Data Handling & Privacy *(Word Limit: Maximum 150 words | Actual: 103 words)*
**No user personal data is collected, stored, or transmitted to third-party services.** In strict compliance with Domain 1 Rule §6 (*"Do not use real personal data or real CVs; create sample profiles for your demo"*) and Malaysia's Personal Data Protection Act 2010 (PDPA), AI Skills Compass operates exclusively on pre-built synthetic personas and ephemeral, checkbox-based skill selections held in stateless URL query parameters. No database writes, cookies, or external LLM prompt logs of user inputs occur. Outbound requests fetch only public scholarly metadata from OpenAlex (`api.openalex.org/works`) or arXiv (`export.arxiv.org`). No API keys or secrets are committed to the repository.

#### 6.2. Known Limitations & Risks *(Word Limit: Maximum 150 words | Actual: 132 words)*
1. **Research Activity vs. Local Hiring Demand**: OpenAlex and arXiv publications measure global scholarly AI research activity around technical skills—**not** Malaysian employer job postings, vacancy counts, or salaries. *Mitigation*: Every role card, banner, and documentation file explicitly states this boundary and distinguishes live research signals from the workforce context figures quoted from the Domain 1 brief (Hays 2025, MOSTI).
2. **External API Availability / Rate Limits**: Live requests to OpenAlex or arXiv may fail if a network is offline. *Mitigation*: `fetch_market_signals()` tries OpenAlex first, falls back to arXiv second, and automatically switches to the 17-record verbatim OpenAlex snapshot (`data/signals_snapshot.json`) with an amber `"DATED SNAPSHOT FALLBACK — Not Live"` banner.
3. **Sparse Input Overconfidence**: *Mitigation*: Profiles with `<2` recognized skills or malformed/stale/future-dated signals halt ranking and display `"Insufficient Evidence"`.

---

### Section 7 — Compliance & Readiness Checklist (Page 15)
*`[TEAM CONFIRMATION REQUIRED: Team Leader must verify all 7 checkboxes below before ticking in the final PDF]`*
- [ ] All APIs, cloud services, AI tools, models, and datasets used in the project are declared in this document.
- [ ] All third-party code, datasets, and models are used in accordance with their licenses, and attribution is provided where required.
- [ ] No API keys, passwords, or other credentials are exposed in the code repository, prototype, or this document.
- [ ] Any use of generative-AI tools for development has been disclosed and reviewed by the team.
- [ ] Any use of official SDC sponsor resources has been declared in Section 5.
- [ ] The prototype described here is accessible to judges through the links provided in Section 1.
- [ ] All fields in this template have been completed within the word limits stated.

### Section 8 — Declaration (Page 16)
- **Signature**: `[Replace with Team Leader Signature]`
- **Date**: `[Replace with Submission Date, on or before 25 October 2026, 7:59:59 AM MYT]`

---

## Part 3: 5–7 Minute Preliminary Pitch Outline (Participant Handbook §6.3.5.6)

> [!IMPORTANT]
> **Hard Time Limit**: **5:00 to 7:00 minutes** (YouTube Link). Exceeding 7:00 incurs a penalty of **-1 point per 30 seconds exceeded** (Participant Handbook §6.3.5.6, p. 13). Aim for **6 minutes 15 seconds**.

| Time Window | Segment | Speaker Focus & Live Screen Action | Rubric Criterion Targeted |
| :--- | :--- | :--- | :--- |
| **0:00 – 0:50** *(50s)* | **1. The Malaysian Workforce Gap & Problem Slice** | Quote the Domain 1 brief figures: Hays 2025 (**56% use AI at work, only 26% formally trained**) and MOSTI (**600,000+ workers need reskilling**). Explain why "upload a CV to a chatbot" fails: static lists go stale, and unconstrained LLMs invent jobs, courses, and statistics. Introduce **Aisyah** (synthetic operations coordinator). | **Clarity of Proposal (20%)** & **Innovation (30%)** |
| **0:50 – 2:10** *(80s)* | **2. Live Demo Part A: Synthetic Profile & Dated Research Signal Radar** | Show the running Replit app. Point out the **Data & Privacy Guardrail** and the **Signal Status Banner** (toggle between the 17-record *Reviewed Dated OpenAlex Snapshot* and *Fetch Live Research API Feed (OpenAlex / arXiv)*). Highlight exact ISO publication dates (`2026-09-04` to `2026-10-17`), retrieval dates (`2026-10-21`), resolving `doi.org` links, whole-word taxonomy skill tags, and the explicit notice that these are **research publications, not job vacancy counts**. | **Feasibility of Build (25%)** (Live working core feature) |
| **2:10 – 3:40** *(90s)* | **3. Live Demo Part B: Explainable Matching & Scenario Stress-Testing** | Walk through Rank #1 (*AI Workflow & Operations Specialist — 72.7/100*). Point to the transparent formula (`0.55 × Skill Readiness + 0.25 × Research Signal Coverage + 0.20 × Scenario Fit`), matched skills, and missing skill gaps. Click **Scenario B (Fast Agentic Disruption)** (`75.2/100`) and **Scenario C (SDG Green Push)** (shifts `#1` to *Sustainable AI & Green-Tech Data Analyst*, `74.3/100`) and show the Multi-Scenario Comparison Table updating. | **Innovation & Creativity (30%)** & **Problem-Solution Fit (25%)** |
| **3:40 – 4:45** *(65s)* | **4. Live Demo Part C: Ordered Free/Low-Cost Pathway & Meaningful SDG Links** | Scroll to the ordered pathway steps (Stage 1 → 2 → 3) showing estimated study hours/weeks and free Malaysian/global options (*AI Untuk Rakyat*, *HRD Corp e-LATiH*, *UN CC:e-Learn*, *NIST AI RMF*) or explicit skill objectives. Show the role and skill links to **SDG Targets 4.3, 4.4, 7.3, 8.2, 8.5, 9.5, 10.3, 13.2, and 16.6**. | **Problem-Solution Fit (25%)** (All 6 must-haves) |
| **4:45 – 5:35** *(50s)* | **5. Live Demo Part D: Honest Guardrails (Sparse Profile & Malformed Signals)** | Click **Sparse / Unverified Profile** (`sparse_profile_skills`) and **Simulate Malformed Signal Feed** (`signal_evidence_insufficient`). Show that the app halts and renders `"Insufficient Evidence"` rather than fabricating a confident recommendation. | **Feasibility of Build (25%)** (Hardest risk & fallback) |
| **5:35 – 6:15** *(40s)* | **6. Technical Architecture, Limitations & Phase 2 Roadmap** | Summarize the zero-secret Python architecture on Replit verified by **11 automated unit/integration tests**, why CPU deterministic matching (<10ms) preserves the US$25 RunPod credit (and aligns with SDG 7.3 energy efficiency), reiterate epistemic limits (OpenAlex measures research activity, not DOSM job vacancies), and preview Phase 2 (HR team skills-gap heatmap). | **Clarity (20%)** & **Feasibility (25%)** |
