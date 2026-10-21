> [!IMPORTANT]
> ## 📁 Submission Documents & Templates
> **All required submission templates are in the Google Drive folder below. Download them before you start.**
>
> ### 👉 [**OPEN THE GOOGLE DRIVE FOLDER**](https://drive.google.com/drive/folders/1xw7c2aN8N-at8hPEULzkcU76e_FFb0Ef) 👈

---

# AI Skills Compass

> An explainable, signal-grounded career and reskilling compass for Malaysian workers and graduates that connects dated AI research and workforce trends to future roles, skill gaps, low-cost learning pathways, alternative future scenarios, and the 17 UN Sustainable Development Goals—without inventing jobs, courses, or statistics.

---

## Team Information

| Field                  | Details                                                                                   |
| ---------------------- | ----------------------------------------------------------------------------------------- |
| **Team Name**          | `[Replace with Your Team Name]`                                                           |
| **Team Domain**        | **Domain 1 — The Aiversecity Future-Ready Workforce Domain**                              |
| **SDG Track (1–17)**   | **SDG 8** (Decent Work & Economic Growth: 8.2, 8.5) & **SDG 4** (Quality Education: 4.3, 4.4) |
| **Team Leader**        | `[Replace with Team Leader Name]`                                                         |
| **University**         | `[Replace with Recognised Malaysian Higher Education Institution(s)]`                     |
| **Number of Members**  | `[Replace with 1–5]`                                                                      |

## Links

| Resource          | Link                                                         |
| ----------------- | ------------------------------------------------------------ |
| GitHub Repository | `https://github.com/your-username/your-project`              |
| Replit Project    | `https://replit.com/@your-username/your-project`             |
| Live Demo         | `https://your-project.replit.app`                            |
| RunPod Endpoint   | Optional (`runpod/handler.py` — see [docs/runpod-decision.md](docs/runpod-decision.md)) |
| Slide Deck        | `https://example.com/slides`                                 |
| Demo Video        | `https://example.com/demo-video` *(5–7 min YouTube link)*    |

---

## Overview

### Problem

AI is reshaping jobs faster than static training programmes can be updated. According to the **Hays Asia Salary Guide 2025** (cited in the Domain 1 brief), **56%** of Malaysian professionals already use AI tools at work, yet only **26%** have received formal training, while **MOSTI** projects over **600,000 Malaysian workers** will need reskilling within 3–5 years. Existing "upload your CV to a chatbot" wrappers rely on static lists, risk exposing personal data, and hallucinate unverified courses, job openings, or guaranteed outcomes.

### Solution

**AI Skills Compass** guides a learner from *"who I am today"* to *"where I can be in the AI era"* through an auditable, human-in-charge pipeline:
1. **Privacy-Safe Synthetic Profile Intake** (4 pre-loaded Malaysian personas + 16-skill customizer; zero real PII collected).
2. **Dated AI & Market Signal Layer** (fetches live Atom 1.0 XML preprints from the public **arXiv API** across `cs.AI`, `cs.CL`, `cs.CY`, `cs.SE`, paired with cited Malaysian workforce benchmarks and an explicitly labeled dated snapshot fallback in `data/signals_snapshot.json`).
3. **Explainable, Deterministic Role Matcher** (`Total Score = 0.55 × Skill Readiness + 0.25 × Dated Signal Momentum + 0.20 × Scenario Fit`), constrained strictly to our reviewed taxonomy (`src/taxonomy.py`) so it never invents jobs, courses, or statistics.
4. **Honest Guardrails**: Sparse profiles (<2 recognized skills) or malformed/empty signal feeds halt ranking and display `"Insufficient Evidence"` rather than a false-confidence prediction.

### Key Features (All 6 Domain 1 Must-Haves)

- **1. Skills Profile Intake (`Must-Have #1`)** — Pre-built synthetic Malaysian worker personas (*Aisyah — Operations*, *Wei Jie — QA*, *Priya — ESG*, plus a *Sparse Profile Guardrail Demo*) and interactive skill checkboxes.
- **2. Dated AI-Trend Signal Layer (`Must-Have #2`)** — Live `export.arxiv.org` API ingestion with publication date, retrieval date, source URL, and taxonomy-constrained skill tags, plus an explicitly badged dated snapshot fallback (`DATED SNAPSHOT FALLBACK — Not Live`).
- **3. Explainable Future-Role Matching (`Must-Have #3`)** — Transparent score breakdown, `"Why This Role Ranks #X"` narrative, matched profile skills, and missing required/supporting skill gaps.
- **4. Ordered Low-Cost Reskilling Pathway (`Must-Have #4`)** — Step-by-step learning plan (`Stage 1 → 2 → 3`) with estimated study hours/weeks and verified free public resources (*AI Untuk Rakyat*, *HRD Corp e-LATiH*, *UN CC:e-Learn*, *NIST AI RMF*, *Green Software Foundation*) or honest skill objectives.
- **5. Meaningful UN SDG Mapping (`Must-Have #5`)** — Every recommended role and skill is mapped to specific UN SDG targets (`Target 4.3`, `4.4`, `7.3`, `8.2`, `8.5`, `9.5`, `10.3`, `13.2`, `16.6`).
- **6. Multi-Scenario Uncertainty Handling (`Must-Have #6`)** — Interactive comparison across 3 explicit future scenarios (*Scenario A: Moderate Co-Pilot Adoption*, *Scenario B: Fast Agentic Disruption*, *Scenario C: Accelerated SDG & Green-Tech Transition*) with explicit assumptions and uncertainty bands.

### Tech Stack

| Layer         | Technology                                                                 |
| ------------- | -------------------------------------------------------------------------- |
| Frontend      | Semantic HTML5, CSS3 Data-Dense Dashboard (`Fira Sans` / `Fira Code`, WCAG AA) |
| Backend       | Python 3 Standard Library (`http.server.ThreadingHTTPServer`, `urllib`, `xml.etree`) |
| Data / State  | Live arXiv Atom 1.0 API + Reviewed Dated JSON Snapshot (`data/signals_snapshot.json`) |
| AI / Compute  | Deterministic Taxonomy & Linear Scoring Engine on Replit CPU (<10ms); Optional RunPod Serverless (`runpod/handler.py`) |
| Hosting / Dev | Replit Core (`.replit` configured to run `python src/main.py`)             |

---

## Project Structure

```text
.
├── data/
│   └── signals_snapshot.json    # Reviewed dated snapshot fallback (clearly labeled in UI)
├── docs/
│   ├── competition-requirements.md  # Prompt 0: Verified rules, rubric, contradictions & checklist
│   ├── prototype-spec.md            # Prompt 1: Concept debate, architecture & acceptance criteria
│   ├── data-sources.md              # Prompt 2: Signal source verification & epistemic boundaries
│   ├── judge-audit-report.md        # Prompt 6: End-to-end judge walkthrough, Playwright & security audit
│   ├── runpod-decision.md           # Prompt 7: Measured workload analysis & US$25 credit preservation
│   └── submission-materials.md      # Prompt 8: Exact field-by-field PDF answers & 5–7 min pitch outline
├── runpod/
│   └── handler.py               # Optional RunPod serverless batch taxonomy extractor
├── src/
│   ├── main.py                  # Web server, HTML dashboard renderer, JSON API & CLI self-check
│   ├── matcher.py               # Explainable role scorer, pathway builder & scenario comparator
│   ├── signals.py               # Live arXiv Atom XML fetcher, schema validator & snapshot fallback
│   ├── taxonomy.py              # Reviewed catalog of 16 skills, 6 roles, SDGs, scenarios & personas
│   └── utils.py                 # Core summary utilities
├── submission/                  # Required submission documents
│   ├── SDC2026_TeamName_Preliminary.pdf      # Preliminary submission template
│   ├── SDC2026_TeamName_TechDeclaration.pdf  # Technology declaration template
│   ├── SDC2026_TeamName_Replit_POU.pdf       # Replit proof of use
│   └── SDC2026_TeamName_Runpod_POU.pdf       # RunPod proof of use
├── tests/
│   └── test_utils.py            # 9 automated unit & HTTP integration tests
├── .env.example                 # Example environment variables
├── .replit                      # Replit run configuration (`python src/main.py`)
├── LICENSE                      # Apache License 2.0
├── requirements.txt             # Python dependencies
└── README.md
```

### Architecture

```text
Synthetic Profile / Scenario Selection ──► Replit Web Server (src/main.py)
                                                 │
        ┌────────────────────────────────────────┼────────────────────────────────────────┐
        ▼                                        ▼                                        ▼
Signal Adapter (src/signals.py)      Reviewed Taxonomy (src/taxonomy.py)     Explainable Matcher (src/matcher.py)
├─ Live arXiv API (export.arxiv.org) ├─ 16 Canonical Skills & Keywords       ├─ 0.55 Readiness + 0.25 Signal Momentum
├─ Schema & Staleness Validator      ├─ 6 Future Roles & UN SDG Sub-Targets  │  + 0.20 Scenario Fit
└─ Dated Snapshot Fallback           └─ Verified Free/Low-Cost Pathways      └─ Sparse/Malformed Guardrail
```

---

## How to Run

### Option 1 — Run on Replit (Recommended)

1. Import this repository into Replit via **Create Repl → Import from GitHub**.
2. *(Optional)* Open **Secrets** (🔒) to set `PORT=5000` or `PROJECT_NAME="AI Skills Compass"`. (No paid API keys are required for the core application!).
3. Click **Run**. Replit executes `python src/main.py` (configured in `.replit`), runs the startup self-check, and serves the interactive web dashboard on `http://0.0.0.0:5000`.

### Option 2 — Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/your-username/your-project.git
cd your-project

# 2. Run the startup self-check
python src/main.py --self-check

# 3. Start the web server (defaults to http://127.0.0.1:5000)
python src/main.py
```

### Run Automated Tests

```bash
python -m unittest discover -s tests -v
```

---

## Judge 2-Minute Demo Walkthrough

1. **Open the Dashboard (`http://127.0.0.1:5000/`)**: Observe the **Synthetic Data Guardrail** and the **Signal Status Banner** (`DATED SNAPSHOT FALLBACK` vs. `LIVE PUBLIC FEED`).
2. **Test a Normal Persona**: Click **Aisyah Rahman (Operations)** or **Priya Nair (ESG)**. Inspect **Rank #1**, the transparent formula breakdown, matched skills, missing skill gaps, cited dated signals, ordered free/low-cost pathway, and UN SDG targets.
3. **Test Multi-Scenario Uncertainty**: Switch between **Scenario A (Moderate Co-Pilot)**, **Scenario B (Fast Agentic Disruption)**, and **Scenario C (Accelerated SDG & Green-Tech Transition)** and watch the rankings and **Multi-Scenario Comparison Table** update.
4. **Test Honest Guardrails**:
   - Click **Sparse / Unverified Profile (Guardrail Demo)** → verify the app halts ranking and shows `Insufficient Evidence (sparse_profile_skills)`.
   - Click **Simulate Malformed Signal Feed (Guardrail Check)** in Step 4 → verify invalid/unattributed signals are stripped and the app halts with `Insufficient Evidence (signal_evidence_insufficient)`.

---

## How We Use Replit *(Required)*

- **Development & Hosting:** The web application (`src/main.py`) is built to run natively on Replit via `.replit` (`run = "python src/main.py"`), serving both the interactive HTML dashboard and JSON endpoints (`/api/evaluate`, `/api/signals`, `/api/health`).
- **Secrets:** Environment variables (`PROJECT_NAME`, `PORT`, and optional `RUNPOD_*` keys) are read via `os.getenv()` from Replit Secrets and never hardcoded.

📄 Proof of use: [`submission/SDC2026_TeamName_Replit_POU.pdf`](submission/SDC2026_TeamName_Replit_POU.pdf)

## How We Use RunPod *(Evaluated & Documented per Participant Handbook §9.3)*

- **Measured Engineering Decision:** Per Participant Handbook §9.3–9.4 (pp. 28–29), RunPod is required *"for any work that needs a GPU."* Our benchmarked taxonomy-constrained signal extraction and 6-role × 3-scenario scoring run in **< 10 ms on Replit CPU**, ensuring zero hallucination risk, zero cold-start latency during live judging, and alignment with **SDG 7.3 (Energy Efficiency)** while preserving our **US$25 RunPod credit**.
- **Optional Serverless GPU Handler:** `runpod/handler.py` provides a ready-to-deploy RunPod Serverless batch taxonomy extractor (`Min Workers = 0`, estimated spend < US$0.25) for bulk Phase 2 corpus ingestion or sponsor Proof-of-Use verification. Full details and cost math are in [`docs/runpod-decision.md`](docs/runpod-decision.md).

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
