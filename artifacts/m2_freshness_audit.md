# M2 AI Trend Intelligence Engine: Source Freshness Audit

**Author:** Senior Labour-Market Data Engineer & ML Systems Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9B Explainable M2 Trend Scoring Engine  
**Reference Date:** 2026-10-23  
**Source Manifest:** `data/trends/manifests/trend_source_manifest.json`  

---

## 1. Freshness Policy & Signal-Type Awareness

A critical defect identified in naive trend monitoring systems is applying a single, uncalibrated age threshold to all labour-market data. Stage 9B enforces **signal-type aware freshness**:

1. **Dynamic High-Frequency Data (Macro / Wages / Vacancies):**
   - Expected update cadence: Monthly, quarterly, or annual.
   - Status:
     - `FRESH`: Age $\le 730$ days (covers latest annual national surveys, e.g. MyCOL 2024/2025).
     - `AGING`: Age $731 - 1095$ days ($2 - 3$ years without update).
     - `STALE`: Age $> 1095$ days ($> 3$ years). Incurs a 15-point confidence penalty.
     - `MISSING_EXPECTED_UPDATE`: When a known statutory annual cycle fails to publish.

2. **Structural & Methodological Benchmarks (Task Exposure / Taxonomies):**
   - Expected update cadence: Multi-year or decennial (e.g., ILO Working Paper 96, MASCO 2020, ESCO v1.1).
   - Status:
     - `CURRENT_STANDARD`: The currently active multilateral reference standard.
     - `ARCHIVAL_VALID`: Sound methodology remaining valid until formally superseded.
     - `SUPERSEDED`: Formally replaced by a newer standard (deprecated).
   - *Rule:* Structural benchmarks are **never** penalized as "stale" simply because their publication date is $>2$ years old, provided no newer revision has been issued.

---

## 2. Source-by-Source Freshness Audit Table

| Source ID | Source Name | Source Type | Publication Date | Latest Observation Date | Age (Days) | Freshness Category | Engine Validity Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `SRC-MYCOL-2024` | TalentCorp Malaysia Critical Occupations List | Annual / Multi-Year Report | 2024-11-01 | 2024-11-01 | 721 | `FRESH` | `VALID_FOR_M2` |
| `SRC-TALENTCORP-IMPACT-2024` | Impact Study of AI, Digital & Green Economy | Statutory Workforce Study | 2024-11-18 | 2024-11-18 | 704 | `FRESH` | `VALID_FOR_M2` |
| `SRC-OPENDOSM-LIVE` | OpenDOSM Salaries & Wages Snapshot | Annual National Survey | 2024-01-01 | 2025-05-01 (Latest series) | 540 | `FRESH` | `VALID_FOR_M2` |
| `SRC-ILO-GENAI-2023` | ILO Working Paper 96: Generative AI and Jobs | Multilateral Benchmark | 2023-08-21 | 2023-08-21 | 1,159 | `CURRENT_STANDARD` | `VALID_FOR_M2` |
| `SRC-OPENALEX-TEMPORAL` | OpenAlex Scholarly AI Research Corpus | Scholarly API Stream | 2026-10-21 | 2026-10-21 | 2 | `FRESH` | `VALID_FOR_M2` |
| `SRC-MYS-POLICY-2024` | Malaysian National Policies (MOSTI, Bursa, JPDP, MITI) | Statutory Mandates | 2024-09-20 | 2024-09-20 | 763 | `CURRENT_STANDARD` | `VALID_FOR_M2` |

---

## 3. Freshness Corrections Made in Stage 9B

1. **Distinction Between Publication Age and Observation Age:**
   - In Stage 9A, `SRC-OPENDOSM-LIVE` was provisionally tagged with `age_days: 1026` based on a 2024 portal metadata date, triggering a misleading `STALE` label.
   - Stage 9B verified the actual observation records in `data/trends/raw/opendosm/wages_occupation_snapshot.json`, which contain full annual series through 2025. The latest observation age is 540 days, correctly reclassifying it as `FRESH`.
2. **Reclassification of ILO Working Paper 96:**
   - In Stage 9A, the ILO Working Paper was marked `ACCEPTABLE` with an age of 1,159 days. Stage 9B corrected the taxonomy to designate it `CURRENT_STANDARD` under the structural benchmark track, ensuring it remains valid without incurring false staleness penalties.
3. **No Fake Real-Time Claims:**
   - The engine explicitly documents that macroeconomic and statutory survey data update on an annual or multi-year basis. Real-time claims are avoided, in strict accordance with Section 26.
