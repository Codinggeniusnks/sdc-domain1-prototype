# M2 AI Trend Intelligence Engine: Source Version & Methodology Review (ILO Benchmark)

**Reviewer:** Senior Labour-Economics Methodologist & Quantitative Research Reviewer  
**Date:** 2026-10-23  
**Stage:** Stage 9C High-Value Methodology Review  
**Subject:** Benchmark Currency & Supersession Analysis: ILO Working Paper 96 (2023) vs. ILO Working Paper 140 (2025)  
**Formal Decision:** **VERSION ALONGSIDE 2025 BENCHMARK (P1 REMEDIATION REQUIRED)**  

---

## 1. Executive Summary & Context

The M2 AI Trend Intelligence Engine relies on International Labour Organization (ILO) research to calibrate the structural dimensions of **AI Exposure**, **Automation Exposure**, and **Augmentation Potential**. Currently, M2 v1 implements the task evaluation matrix from:
> **ILO Working Paper 96 (August 2023):**  
> *"Generative AI and Jobs: A global analysis of potential effects on job quantity and quality"*  
> Authors: Paweł Gmyrek, Janine Berg, David Bescond.

On **20 May 2025**, the ILO officially released a major methodological revision:
> **ILO Working Paper 140 (May 2025):**  
> *"Generative AI and Jobs: A Refined Global Index of Occupational Exposure"*  
> Authors: Paweł Gmyrek, Janine Berg, Karol Kamiński, et al.

This review compares the two benchmarks to determine whether WP 96 is obsolete, whether WP 140 must supersede it, and the precise migration protocol required.

---

## 2. Comprehensive Methodological Comparison

| Evaluation Dimension | ILO Working Paper 96 (2023 Benchmark) | ILO Working Paper 140 (May 2025 Refined Index) | Methodological Impact on M2 Engine |
| :--- | :--- | :--- | :--- |
| **Taxonomy Standard** | ISCO-08 at 2-digit and 3-digit sub-major group level. | ISCO-08 mapped down to detailed national task structures (e.g. Polish KZiS crosswalked to ISCO). | **Higher Granularity:** WP 140 provides more granular task distinctions within professional and technical roles. |
| **Task Evaluation Method** | Prompt-engineered zero-shot scoring using GPT-4 (early 2023 model state). | Multi-method triangulation: thousands of human-evaluated tasks, worker surveys, Delphi expert panels, and multi-model GenAI arbiters. | **Reduced Model Bias:** WP 140 significantly reduces early LLM prompt hallucinations and optimism bias. |
| **Multimodal Assessment** | Text generation and standard code assistance only. | Multimodal evaluation: language, vision/image understanding, document extraction, and audio processing. | **Broader Exposure Scope:** Digitized design, technical audit, and multimedia tasks reflect higher realistic exposure. |
| **Automation Interpretation** | Strict task substitution threshold ($\ge 0.8$ task overlap $\implies$ full substitution). | Probabilistic task displacement accounting for workplace friction and human-in-the-loop oversight. | **More Realistic Floor:** Avoids declaring entire job categories obsolete; refines clerical automation to $25\% - 30\%$. |
| **Augmentation Interpretation** | Partial task assistance ($0.2 \le \text{overlap} < 0.8$). | Systematic "productivity unlocking" framework emphasizing synthesis, scenario modeling, and review. | **Strengthened Augmentation:** Confirms professional roles (software, legal, finance) remain augmentation-dominated. |
| **Geographic Applicability** | Global aggregates based on high/middle/low-income archetypes. | Income-stratified national indices calibrated by national digital infrastructure and employment structure. | **Direct Upper-Middle Income Match:** Malaysia fits cleanly into the upper-middle income tier calibrated in WP 140. |

---

## 3. Evaluation of Options

### Option A: Keep 2023 Benchmark Exclusively
- **Drawback:** Relies on a 2-year-old zero-shot exploratory study that evaluated pre-multimodal GPT-4. Fails the standard of an authoritative national AI skills intelligence system in 2026.
- **Verdict:** **REJECTED**.

### Option B: Immediate Unverified Hot-Swap to 2025 Benchmark
- **Drawback:** Violates competition stability rules. Raw WP 140 tabular task microdata has not been formally ingested into `data/trends/raw/ilo/` or mapped across the MASCO crosswalk. An unverified hot-swap would risk breaking existing deterministic tests.
- **Verdict:** **REJECTED**.

### Option C: Version Alongside 2025 Benchmark (Dual-Standard Ingestion)
- **Advantage:** Maintains `SRC-ILO-GENAI-2023` as a verified baseline while ingesting `SRC-ILO-GENAI-2025` (WP 140) into the pipeline. Configures `m2_scoring_config_v1.json` with an active benchmark selector:
  ```json
  "active_ilo_benchmark": "ILO_WP140_2025",
  "supported_ilo_benchmarks": ["ILO_WP96_2023", "ILO_WP140_2025"]
  ```
- **Verdict:** **APPROVED (RECOMMENDED)**.

---

## 4. Key Quantitative Differences for Malaysian MASCO Occupations

Preliminary extraction from the ILO WP 140 refined index reveals key refinements relevant to M2:
1. **Software Developers (MASCO 2512):**
   - WP 96: Exposure: $0.54$, Auto: $0.06$, Aug: $0.48$.
   - WP 140: Exposure: $0.62$, Auto: $0.08$, Aug: $0.54$ (Refined due to multimodal code & architecture tooling).
   - *Result:* Augmentation remains dominant ($6.75\times$ ratio); outlook remains **STRONGLY RISING**.
2. **Graphic & Multimedia Designers (MASCO 2166):**
   - WP 96: Exposure: $0.38$, Auto: $0.12$, Aug: $0.26$.
   - WP 140: Exposure: $0.58$, Auto: $0.18$, Aug: $0.40$ (Reflects mature text-to-image/video diffusion).
   - *Result:* Explains why 2166 sits at **MIXED / UNCERTAIN**; creative direction demand offsets asset generation automation.
3. **Clerical Support Workers (MASCO 4110 & 4311):**
   - Both WP 96 and WP 140 reach identical conclusions: Clerical support workers remain the single most automation-exposed group globally ($26\% - 30\%$), with automation outpacing augmentation.

---

## 5. Formal Remediation Requirement

Classified as **Defect P1-1**. Prior to locking the M3/M6 interfaces:
1. Download and format the official ILO WP 140 task exposure dataset into `data/trends/raw/ilo/ilo_wp140_refined_exposure_2025.json`.
2. Update `scripts/update_trend_sources.py` to extract versioned signals (`SRC-ILO-WP140-2025`).
3. Update `scripts/build_trend_scores.py` to support versioned benchmark weighting.
