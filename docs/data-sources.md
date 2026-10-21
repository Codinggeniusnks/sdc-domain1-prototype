# Evidence & Data Sources Specification (Prompt 2)

## 1. Selected Signal Sources & Verification

### Primary Live Source: OpenAlex Public REST API (`api.openalex.org/works`)
- **Endpoint**: `https://api.openalex.org/works?search=artificial+intelligence+llm+workflow+evaluation+governance+sustainability+sql+python&per-page=18&sort=publication_date:desc`
- **Access Method**: Standard unauthenticated HTTP `GET` returning JSON (`application/json`) with polite `User-Agent` header (`mailto:sdc.xmumhack@gmail.com`). Uses Python's standard library (`urllib.request` + `json`), requiring zero secret API keys.
- **Usage Terms & Attribution Requirements**:
  - Dedicated to the public domain under **CC0 1.0 Universal (CC0)** ([OpenAlex Terms](https://docs.openalex.org/)).
  - Free for public, commercial, and academic hackathon use; polite pool allows 10 requests/second and 100,000 requests/day. Every signal displays its canonical DOI / OpenAlex URL (`https://openalex.org/W...` or `https://doi.org/...`), publication date, and retrieval date.
- **Update Frequency**: Daily continuous ingestion of global scholarly works, preprints, and conference proceedings.
- **Available Fields Used**:
  - `title`: Work title
  - `publication_date`: Exact ISO-8601 publication date (`YYYY-MM-DD`)
  - `doi` / `id`: Canonical clickable source URL
  - `abstract_inverted_index` & `concepts`: Reconstructed abstract and concept terms, scanned **strictly** against our reviewed canonical skill taxonomy (`SKILLS_CATALOG`)—never used to invent unconstrained skills or jobs.
- **Live Demo Suitability**: **Yes (Verified < 1s response time).** Tested live on `2026-10-21`, returning 12+ valid dated works matched to our taxonomy in under 600ms.

### Secondary Live Source: arXiv Public Atom API (`export.arxiv.org/api/query`)
- **Endpoint**: `http://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.CY+OR+cat:cs.SE&sortBy=submittedDate&sortOrder=descending&max_results=12`
- **Documentation Verified via `find-docs` (`Context7` MCP `/websites/info_arxiv_help_api`)**: Queries `cs.AI`, `cs.CL`, `cs.CY`, and `cs.SE` sorted by `submittedDate` and parses `<entry>`, `<title>`, `<published>`, `<id>`, and `<summary>`.
- **Role in Adapter**: Automatic secondary live feed if OpenAlex is unreachable, before falling back to our local snapshot (`data/signals_snapshot.json`). Note: During live testing on `2026-10-21`, `export.arxiv.org` experienced >8s read timeouts on multi-category boolean queries, confirming why our multi-tier adapter (OpenAlex Live → arXiv Live → Reviewed Snapshot Fallback) is essential for demo reliability.

### Grounding Benchmark Context (Cited Policy & Workforce Baselines)
To connect leading AI technical signals to the Malaysian workforce context highlighted in the Domain 1 Problem Statement (p. 3), each role and pathway also cites published benchmark reports:
1. **Hays Asia Salary Guide 2025 (Malaysia)**: 56% of Malaysian professionals use AI tools at work, while only 26% have received formal training.
2. **Ministry of Science, Technology and Innovation (MOSTI) Malaysia Workforce Projection**: Over 600,000 Malaysian workers require reskilling within 3–5 years.
3. **National Free Upskilling Benchmarks**: Malaysia *AI Untuk Rakyat* (`https://www.ai.gov.my/`, MyDIGITAL / MDEC) and *HRD Corp e-LATiH* (`https://elatih.hrdcorp.gov.my/`) free public learning modules.

---

## 2. Honest Epistemic Boundaries: What the Data Does and Does Not Support

| What This Data **DOES** Support | What This Data **DOES NOT** Support (Explicitly Disclosed in UI) |
| :--- | :--- |
| • Identifying which **technical AI capabilities and workflow patterns** (e.g., RAG, agentic evaluation, AI governance, prompt engineering, carbon-aware ML, SQL/Python data analysis) are actively surging in current dated literature.<br>• Showing **transparent provenance**: every signal displays its exact publication date, retrieval timestamp, source URL, and the exact taxonomy keywords matched in its title/abstract.<br>• Demonstrating **dynamic sensitivity**: switching between Live Feed and Snapshot Fallback, or switching scenarios, visibly recalculates role momentum scores. | • **Not a census of Malaysian job vacancies**: OpenAlex and arXiv measure global AI capability & research momentum, not local employer job openings in Kuala Lumpur, Penang, or Johor.<br>• **Not a guarantee of salary or hiring**: A high match or momentum score indicates skill alignment and emerging technical relevance, not a guaranteed job offer.<br>• **No unconstrained AI hallucination**: `extract_taxonomy_entities()` only tags skills that exist in the reviewed taxonomy (`src/taxonomy.py`); it cannot invent unverified job titles or courses. |

---

## 3. Signal Schema & Fallback Labeling Contract

Every signal processed by `src/signals.py` conforms to a strict dictionary schema validated by `validate_signals()`:

```json
{
  "id": "W7222873672",
  "title": "AI as Co-Designer and Feedback Partner: Enhancing Human Judgment",
  "published_date": "2026-10-19",
  "retrieved_date": "2026-10-21",
  "source_name": "OpenAlex Live API (CC0 Scholarly Feed)",
  "source_url": "https://openalex.org/W7222873672",
  "extracted_skills": ["ai_literacy", "human_in_the_loop_qa", "stakeholder_communication"],
  "related_roles": ["ai_workflow_specialist", "ai_governance_auditor"],
  "is_fallback": false
}
```

### Guardrails Enforced in Code (`src/signals.py` & `src/matcher.py`)
1. **Explicit Fallback Badging**: When `mode="fallback"` is selected or live network requests fail, `fetch_market_signals()` returns records from `data/signals_snapshot.json` with `source_mode = "fallback_snapshot"` and `is_fallback = True`. The UI renders an amber warning banner (`DATED SNAPSHOT FALLBACK — Not Live`) so judges are never misled.
2. **Malformed / Empty Signal Rejection (`test_malformed_or_empty_signals_rejected`)**: `validate_signals(raw_signals)` strips any record missing `title`, `published_date` (`YYYY-MM-DD`), `source_url` (`http://` or `https://`), `retrieved_date`, or valid taxonomy skills. If zero valid signals remain after validation, `rank_roles_for_profile()` sets `status = "insufficient_evidence"` and refuses to produce confident role rankings.
