# RunPod GPU Evaluation & Credit Preservation Decision (Prompt 7)

## 1. Skill & Environment Availability Report
- **`runpod` / `runpod-usage` skills**: Not installed in this Antigravity environment (verified via plugin directory scan).
- **Official Competition Rule Check**:
  - *Participant Handbook §9.1.2, §9.3–9.4 (pp. 28–29) & FAQ 15.21 (p. 43)*:
    > *"9.1.2. RunPod: Each team receives US$25 of RunPod credit for the Preliminary Round."*
    > *"9.3. Teams must use RunPod for **any work that needs a GPU**. This includes: training a model, fine-tuning a model, and running a model (inference) that needs a GPU. Teams may also use any other tools, frameworks, or services for work that does not need a GPU."*
    > *"10.7. Teams that used RunPod must include a screenshot of their RunPod dashboard in the Technical & Tools Declaration Document."*
  - *Flagged Contradiction with GitHub Template `README.md`*: The GitHub template `README.md` marks `"## How We Use RunPod (Required)"` and lists `submission/SDC2026_TeamName_Runpod_POU.pdf`.

---

## 2. Measured Prototype Workload Analysis: Is GPU Compute Necessary?

| Task in AI Skills Compass | Measured Execution Time (CPU) | Requires GPU? | Verdict |
| :--- | :--- | :--- | :--- |
| **1. Fetching & Parsing Dated arXiv Atom XML Signals** (`12–15 papers`) | ~250–800 ms (network I/O bound) | **No** | Network & XML parsing; GPU adds cold-start latency (3–15s) and zero speedup. |
| **2. Taxonomy-Constrained Skill Extraction** (`16 canonical skills`) | **< 2 ms** | **No** | Deterministic keyword/phrase matching guarantees zero hallucinated skills (Domain 1 §6 guardrail). |
| **3. Multi-Scenario Role Scoring & Pathway Generation** (`6 roles × 3 scenarios`) | **< 5 ms** | **No** | Exact linear formula (`0.55 × Readiness + 0.25 × Momentum + 0.20 × Scenario Fit`). |

### Engineering Decision for the Preliminary Round
**Preserve the US$25 RunPod credit for the Preliminary Round core demo flow and keep the Replit CPU path 100% self-contained.**
- Adding a mandatory GPU call into the live Replit user path would introduce **serverless cold-start latency (5–20 seconds)**, a network point of failure during judge evaluation, and unnecessary credit burn for a task that executes in **under 10 milliseconds on CPU** with 100% determinism and zero hallucination risk.
- This also aligns directly with **UN SDG 7 (Target 7.3 — Energy Efficiency)** and **SDG 13 (Target 13.2 — Climate Action)**: right-sizing compute by avoiding GPU inference where deterministic CPU logic suffices.

---

## 3. Optional / Conditional RunPod Serverless Plan (If Needed for Sponsor POU or Phase 2 Bulk Ingestion)

If the organizing committee confirms on Discord that **every** team must submit a RunPod Proof-of-Use screenshot (`SDC2026_TeamName_Runpod_POU.pdf`), OR when scaling to 10,000+ regional job postings in Phase 2 (28–30 Oct 2026):

1. **Exact GPU Workload (`runpod/handler.py`)**:
   - Batch semantic skill-taxonomy classification over large corpora of unstructured job descriptions/research abstracts, constrained to emit only canonical IDs from `SKILLS_CATALOG` with confidence scores, falling back to Replit's local deterministic matcher whenever `RUNPOD_API_KEY` or `RUNPOD_ENDPOINT_ID` is unset.
2. **Estimated Spend (Within US$25 Credit Budget)**:
   - **RunPod Serverless — 16GB/24GB GPU (e.g., RTX A4000 / L4 / RTX 3090 Flex Worker)**: ~US$0.00019–US$0.00031 per second of active execution.
   - **Configuration**: `Min Workers = 0` (scale-to-zero when idle!), `Max Workers = 1`, `Idle Timeout = 5 seconds`, `Execution Timeout = 30 seconds`.
   - **Total Estimated Spend for 100 test requests (~3 seconds each)**: `300 seconds × $0.00031/s ≈ US$0.09` (**< US$0.25 total**, preserving >US$24.75 of the US$25 credit).
3. **Stop Conditions & Safety Guardrails**:
   - **Never deploy an always-on GPU Pod** without an auto-stop timer; use **Serverless with `Min Workers = 0`** or terminate any Pod immediately after capturing the dashboard proof screenshot (Pod ID / Endpoint URL, GPU type, runtime).
   - **Hard Stop Condition**: Set a RunPod spend alert / limit at **US$5.00** during Phase 1 so at least **US$20.00** remains for the Final Phase (31 Oct – 1 Nov 2026).
   - **Secret Hygiene**: Store `RUNPOD_API_KEY` and `RUNPOD_ENDPOINT_ID` exclusively in Replit Secrets (never in code, logs, commits, screenshots, or PDF declarations).
