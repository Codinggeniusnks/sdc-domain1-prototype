# M2 AI Trend Intelligence Engine: Freshness & Staleness Policy

**Author:** Senior Labour-Market Data Engineer, AI Trend Research Engineer & ML Systems Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9A Data Foundation & Evidence Architecture  
**Reference Date:** 2026-10-23  

---

## 1. Architectural Philosophy

In labour-market and technological trend forecasting, a rigid "one-size-fits-all" expiration window is fundamentally flawed:
- A high-frequency indicator (such as monthly national unemployment) becomes obsolete after 90 days.
- An occupational classification standard (such as MASCO 2020 or ISCO-08) or a deep econometric research benchmark (such as ILO Working Paper 96) remains structurally valid and authoritative for 3 to 7 years.
- Longitudinal shortage series (such as TalentCorp MyCOL 2015–2025) derive their primary predictive power specifically from their multi-year historical depth.

Therefore, M2 implements a **Signal-Type Aware Freshness Engine**.

---

## 2. Freshness Mathematical Model

Given the dataset's publication or observation date $D_{\text{source}}$ and the engine's frozen reference date $D_{\text{ref}} = \text{2026-10-23}$:
$$\text{AgeDays} = D_{\text{ref}} - D_{\text{source}}$$

Each source category is governed by explicit freshness bounds $(\tau_{\text{fresh}}, \tau_{\text{acceptable}})$:

$$\text{FreshnessCategory}(\text{AgeDays}) = \begin{cases}
\text{FRESH} & \text{if } \text{AgeDays} \le \tau_{\text{fresh}} \\
\text{ACCEPTABLE} & \text{if } \tau_{\text{fresh}} < \text{AgeDays} \le \tau_{\text{acceptable}} \\
\text{ARCHIVAL\_VALID} & \text{if } \text{AgeDays} > \tau_{\text{acceptable}} \text{ and Category} \in \{\text{MULTI\_YEAR\_REPORT}, \text{BENCHMARK\_STANDARD}\} \\
\text{STALE} & \text{otherwise}
\end{cases}$$

---

## 3. Freshness Policy Matrix

| Cadence Type | Representative Sources | Fresh Threshold ($\tau_{\text{fresh}}$) | Acceptable Threshold ($\tau_{\text{acceptable}}$) | Max Archival Validity | Expiration Action |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`MONTHLY_MACRO`** | OpenDOSM `lfs_month` | 60 days | 180 days | None (Macro data expires) | Flag as STALE; trigger API fetch. |
| **`QUARTERLY_SURVEY`** | OpenDOSM `lfs_qtr` | 120 days | 365 days | None | Flag as STALE; trigger API fetch. |
| **`ANNUAL_SURVEY`** | OpenDOSM `wages_occupation`, `wages_skill` | 365 days (1 yr) | 730 days (2 yrs) | 1,825 days (5 yrs) | Downweight confidence by $10\%$ per year past acceptable. |
| **`MULTI_YEAR_REPORT`** | TalentCorp MyCOL, TalentCorp 2024 Impact Study | 730 days (2 yrs) | 1,460 days (4 yrs) | Indefinite for longitudinal baselines | Preserved as `ARCHIVAL_VALID`. |
| **`BENCHMARK_STANDARD`** | ILO GenAI Study 2023, MASCO 2020 | 1,095 days (3 yrs) | 2,190 days (6 yrs) | Multi-year structural validity | Preserved as `ARCHIVAL_VALID`. |

---

## 4. Current Audit of Ingested Sources (as of 2026-10-23)

| Source ID | Source Name | Publication Date | Age (Days) | Cadence Type | Freshness Category | Status in Engine |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- |
| `SRC-OPENALEX-TEMPORAL` | OpenAlex Scholarly Corpus | 2026-10-21 | 2 | `MULTI_YEAR_REPORT` | `FRESH` | Fully Active |
| `SRC-MYCOL-2024` | TalentCorp MyCOL (Latest Edition) | 2024-11-01 | 722 | `MULTI_YEAR_REPORT` | `FRESH` | Fully Active |
| `SRC-TALENTCORP-IMPACT-2024` | TalentCorp AI/Digital/Green Study | 2024-11-18 | 705 | `MULTI_YEAR_REPORT` | `FRESH` | Fully Active |
| `SRC-MYS-POLICY-2024` | Malaysian National Policy Mandates | 2024-09-20 | 764 | `MULTI_YEAR_REPORT` | `ACCEPTABLE` | Fully Active |
| `SRC-OPENDOSM-LIVE` | OpenDOSM Labour Force & Wages | 2024-01-01 | 1,026 | `ANNUAL_SURVEY` | `ACCEPTABLE` | Fully Active |
| `SRC-ILO-GENAI-2023` | ILO Working Paper 96 (GenAI & Jobs) | 2023-08-21 | 1,159 | `BENCHMARK_STANDARD` | `ARCHIVAL_VALID` | Fully Active |

---

## 5. Handling of Longitudinal Baselines

When computing longitudinal indicators (such as `number_of_editions_critical` across 2015–2025):
- The 2015/2016 inaugural MyCOL edition has an age of $>3,600$ days.
- **Critical Policy Rule:** Archival records belonging to a longitudinal series are NOT marked stale or discarded. They provide the historical numerator and denominator required to verify true persistence versus cyclical noise.
- Every individual signal record clearly distinguishes `source_date` (when the edition was published) from `retrieved_at` (when it was ingested into M2) and `valid_to` (the end of its formal forecasting window).
