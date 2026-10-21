# Judge Demo Walkthrough, Code Review & Security Audit Report (Prompt 6)

## 1. Skills & Tools Verification Report
- **`playwright-cli` (`C:\Users\LENOVO\AppData\Roaming\npm\playwright-cli.cmd`)**: **Installed and Executed.** Used to automate Chromium browser navigation across normal synthetic profiles, live OpenAlex API mode, scenario switches, and sparse/malformed guardrail states, inspecting console logs, accessibility snapshots, and viewport screenshots.
- **`code-review` (`CodeRabbit CLI`)**: `SKILL.md` read; the `coderabbit` binary is not installed on this Windows host (`where.exe coderabbit` returned empty), so we performed the structured diff and logic review directly per Prompt 4 & Prompt 6 instructions.
- **`security-audit` (`skills/security-audit/SKILL.md`)**: **Guidance mode applied.** Audited all trust boundaries, user inputs, outbound HTTP calls, environment variable handling, and personal-data guardrails.

---

## 2. First-Time Judge Walkthrough Checklist (Verified Live at `http://127.0.0.1:5000`)

| Judge Inspection Item | Normal Profile (`aisyah_ops` & `priya_esg`) | Sparse Profile (`sparse_edge_case`) & Malformed Feed (`malformed_test`) | Verdict |
| :--- | :--- | :--- | :--- |
| **Source Dates & Attribution** | Every signal in the Role Cards and Step 4 Radar Table shows ISO-8601 `Pub: YYYY-MM-DD`, `Ret: YYYY-MM-DD`, attributed source name (`OpenAlex Live API` or `arXiv API`), and a clickable `https://` link (`target="_blank" rel="noopener noreferrer"`). | When `malformed_test` is clicked, signals missing valid ISO dates or `http/https` URLs are rejected and listed in the audit warning log. | **PASS** |
| **Live vs. Fallback Status Visibility** | Amber top banner (`[DATED SNAPSHOT FALLBACK (NOT LIVE)]`) when using snapshot; green top banner (`[LIVE PUBLIC FEED (OpenAlex / arXiv API)]`) when live mode succeeds. Never disguises snapshot data as live. | Guardrail test mode displays a red top banner (`[GUARDRAIL TEST: MALFORMED / EMPTY SIGNALS]`). | **PASS** |
| **Explainable Role Ranking & Skill Gaps** | Displays `Rank #1` (`AI Workflow & Operations Specialist — 72.7/100` for Aisyah; `Sustainable AI & ESG Telemetry Analyst` for Priya under Scenario C), exact formula breakdown (`0.55 × Readiness + 0.25 × Momentum + 0.20 × Scenario Fit`), green matched required skills, and red missing skill gaps. | Ranking halts (`ranked_roles = []`) and displays `Insufficient Evidence — Honest Guardrail Triggered` (`sparse_profile_skills` or `signal_evidence_insufficient`). | **PASS** |
| **Ordered Reskilling Pathway** | Ordered `Step 1 · Stage 1` → `Stage 2` → `Stage 3` cards with estimated hours/weeks, cost tier (`Free`), and verified public Malaysian/global platforms (`AI Untuk Rakyat`, `HRD Corp e-LATiH`, `UN CC:e-Learn`, `NIST AI RMF`). Zero invented course prices. | Halted safely when evidence is insufficient. | **PASS** |
| **Meaningful UN SDG Explanation** | Each role and pathway step maps to specific UN SDG targets (`Target 4.3`, `4.4`, `7.3`, `8.2`, `8.5`, `9.5`, `10.3`, `13.2`, `16.6`) with a plain-English explanation of how the career path advances the goal. | Visible in header and across all matched roles. | **PASS** |
| **Multiple Future Scenarios & Uncertainty** | 3 interactive scenario tabs (*Scenario A: Moderate Co-Pilot*, *Scenario B: Fast Agentic Disruption*, *Scenario C: Accelerated SDG & Green-Tech Transition*) plus a side-by-side **Multi-Scenario Uncertainty Comparison Table** showing how #1 and #2 roles shift. | Scenario selector remains accessible so the user can return to a normal profile at any time. | **PASS** |

---

## 3. Ranked Findings List, Fixes Applied & Re-Verification

| Priority | Finding ID & Summary | Trust Boundary / Impact | Fix Applied | Re-Verification Result |
| :--- | :--- | :--- | :--- | :--- |
| **1 — HIGH (Blocking Live Demo Reliability)** | **F-01: Live `export.arxiv.org` Boolean Category Query Timed Out (>8s)** | Outbound network dependency: During live testing on `2026-10-21`, querying `export.arxiv.org/api/query` with a 4-category boolean `OR` timed out after 8 seconds, forcing `mode="live"` to always fall back to the snapshot. | Added **OpenAlex Public REST API (`https://api.openalex.org/works`)** (CC0 license, <600ms response time, daily dated scholarly works) as the primary live source in `src/signals.py`, retaining `export.arxiv.org` as secondary and `data/signals_snapshot.json` as tertiary fallback. | **FIXED & VERIFIED**: `fetch_market_signals(mode="live")` returned 18 valid dated works (`2026-10-19` / `2026-10-21`) in <1s with `is_fallback: False`. |
| **2 — MEDIUM (UX / Judge Discoverability)** | **F-02: Sparse-Profile Guardrail Alert Rendered Below the Fold in Step 3** | Judge UX: On a 1280×720 viewport, clicking `"Sparse / Unverified Profile (Guardrail Demo)"` rendered the red `Insufficient Evidence` alert inside Step 3 below the fold, requiring scrolling to notice that ranking had halted. | Updated `render_dashboard_html()` in `src/main.py` to surface the red `Insufficient Evidence` alert banner immediately above Step 1 whenever `ev["status"] != "ok"`, and added a **Quick Judge Navigation** bar. | **FIXED & VERIFIED**: Playwright screenshot `docs/screenshot-sparse-guardrail.png` confirms the red `Insufficient Evidence` alert is immediately visible above the fold. |
| **3 — LOW (Browser Console Cleanliness)** | **F-03: Browser Logged 1 Console Error (`GET /favicon.ico 404`)** | First-time judge inspecting DevTools console saw `1 error` due to missing `/favicon.ico` route in `CompassRequestHandler`. | Added an explicit `/favicon.ico` `204 No Content` handler in `src/main.py`. | **FIXED & VERIFIED**: Re-running `playwright-cli` reported `0 errors, 0 warnings` in the browser console. |
| **4 — INFO (Security & Privacy Review)** | **F-04: XSS, SSRF, Secret Exposure & PDPA Audit** | Checked all query parameters (`profile_id`, `scenario_id`, `signal_mode`, `skills`, `custom_name`) and external signal fields rendered in HTML. | Every dynamic value in `src/main.py` is escaped via `html.escape()` (`esc()`), outbound URLs in `src/signals.py` are hardcoded constants (`OPENALEX_QUERY_URL`, `ARXIV_QUERY_URL` — zero user-controlled SSRF), no PII is stored, and zero secrets exist in git history. | **PASS (Clean)** |

---

## 4. What Remains for Phase 2 (Post-Preliminary Ambitions)
- All **Preliminary Round** requirements and all 6 Domain 1 Must-Have features are implemented, tested (9/9 unit tests passing), and verified in a live browser.
- Deferred intentionally to Phase 2 (28–30 Oct 2026): Employer/HR multi-employee cohort heatmap and Bahasa Malaysia / Chinese UI translation toggles.
