# M2 AI Trend Intelligence Engine: Confidence Framework Validation Report

**Author:** Senior Labour-Market Quantitative Researcher & Explainable-AI Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9B Explainable M2 Trend Scoring Engine  
**Configuration Reference:** `data/trends/processed/m2_confidence_config_v1.json`  

---

## 1. Evidence Confidence Design Tenets

The M2 Confidence Engine evaluates the epistemic robustness of trend findings. It explicitly avoids confusing confidence with a probability score. Instead, confidence measures:
1. **Source Family Independence:** Confidence increases only when independent statutory, multilateral, and academic bodies corroborate a trend. Multiple citations or web summaries from the same underlying study count strictly as **one** evidence family.
2. **Authority Hierarchy:** Direct Malaysian statutory evidence (Tier A) carries primary authority; multilateral benchmarks (Tier B) provide structural task parameters; global academic corpora (Tier C) provide technology velocity.
3. **Cross-Source Agreement & Conflict Penalization:** When sources disagree (e.g., high reported vacancy shortage accompanied by severe task automation vulnerability), confidence is penalized by 15–20 points, and the conflict is explicitly flagged in machine-readable metadata.
4. **Freshness Degradation:** Outdated data decays confidence gracefully without invalidating foundational structural benchmarks.

---

## 2. Confidence Tier Distribution

### 2.1. Overall Entity Distribution ($N = 36$ Unique Entities)

| Confidence Tier | Required Score | Min. Independent Families | Skills Count ($N=16$) | Occupations Count ($N=20$) | Total Entities | Percentage |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HIGH** | $\ge 75$ | $\ge 3$ families | 16 | 13 | **29** | **80.6%** |
| **MEDIUM** | $50 - 74$ | $\ge 2$ families | 0 | 7 | **7** | **19.4%** |
| **LOW** | $25 - 49$ | 1 family | 0 | 0 | **0** | **0.0%** |
| **INSUFFICIENT** | $< 25$ | 0 families | 0 | 0 | **0** | **0.0%** |

*Note on Major Groups:* The 8 MASCO major group fallback profiles (`MAJOR_1` to `MAJOR_9`) are scored separately as aggregate reference anchors with a fixed `MEDIUM` confidence (Index: 55.0) and marked with the quality flag `AGGREGATED_FALLBACK`.

---

## 3. Detailed Validation by Entity Type

### 3.1. Level 1 Core Skills ($16 / 16$ HIGH Confidence)
All 16 Level 1 skills achieved HIGH confidence (Index: $80.0 - 100.0$) due to multi-source triangulation:
- **Corroborating Evidence Families:** Every skill is represented in at least 4 independent families:
  1. `TALENTCORP_MYCOL` (Future skill demand mentions)
  2. `TALENTCORP_IMPACT_STUDY` (Required future competencies across 13 emerging roles)
  3. `MALAYSIAN_GOVERNMENT_POLICY` (MOSTI AIGE, Bursa ESG, JPDP PDPA, or MITI NSS mandates)
  4. `OPENALEX_SCHOLARLY` (Longitudinal publication corpus)
  5. `ILO_GENAI_STUDY` (Task domain exposure mapping)
  6. `DOSM_WAGES` (Associated occupational wage momentum)
- **Zero Intersource Conflict:** Because these 16 skills represent emerging, complementary competencies rather than routine manual tasks, augmentation consistently outpaces automation potential, preventing cross-source conflict penalties.

### 3.2. MASCO 4-Digit Occupations ($13$ HIGH, $7$ MEDIUM Confidence)
- **HIGH Confidence ($13$ Roles):**
  - Roles with longitudinal presence in MyCOL ($\ge 4$ editions), ILO sub-group task mapping, OpenDOSM wage records, and National Policy alignment (e.g., Software Developers 2512, Systems Analysts 2511, Database Designers 2521, Environmental Engineers 2143).
  - Also includes General Office Clerks (4110) and Accounting Clerks (4311), which possess unanimous corroborating evidence of high automation exposure across ILO, OpenDOSM, and MyCOL exclusion.
- **MEDIUM Confidence ($7$ Roles):**
  - Roles with fewer longitudinal MyCOL editions or broader mapping reliance (e.g. Database & Network Professionals NEC 2529, Applications Developers NEC 2519, Graphic & Multimedia Designers 2166).
  - Scored between 50.0 and 70.0 index, reflecting solid but less dense primary documentation.

---

## 4. Conflict & Quality Flag Audit

- **Conflicting-Evidence Profiles:** $0$ unhandled conflicts. Any observed tension (e.g., high AI exposure alongside high shortage for developers) was resolved by decomposing exposure into automation vs. augmentation, which eliminated false conflicts.
- **Single-Source Guardrail Verification:** Unit test `test_03_source_family_independence` validated that an entity with signals from only one family cannot exceed a confidence cap of 45 (LOW confidence).
- **Quality Flags Applied:**
  - `AGING_DATA`: Applied to dynamic signals older than 24 months.
  - `LOW_SOURCE_COUNT`: Applied to any entity with fewer than 3 independent families.
  - `AGGREGATED_FALLBACK`: Applied to major group reference profiles.

The confidence framework is fully validated and ready for independent methodology review.
