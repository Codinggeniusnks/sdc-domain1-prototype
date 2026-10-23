# M2 AI Trend Intelligence Engine: Quality Flags & Boundary Audit Report

**Author:** Senior Labour-Market Data Quality Auditor & ML Systems Engineer  
**Date:** 2026-10-23  
**Stage:** Stage 9B Explainable M2 Trend Scoring Engine  
**Version:** 1.0.0  

---

## 1. Quality Flag Schema & Definitions

To prevent silent failures, overconfident predictions, or ungrounded estimates, every entity profile in M2 supports machine-readable quality flags. The flags alert downstream modules (such as M3 Role Matching) to epistemic limitations:

| Quality Flag Name | Trigger Condition | Downstream Behavioural Impact |
| :--- | :--- | :--- |
| `LOW_SOURCE_COUNT` | Profile supported by fewer than 3 independent evidence families. | Confidence index capped at $70.0$; categorical label limited to `MEDIUM` or `LOW`. |
| `STALE_DYNAMIC_DATA` | Primary dynamic series (wages/vacancies) exceeds 36 months without refresh. | Confidence penalized by 15 points; flagged in UI audit drawer. |
| `LOW_MAPPING_CONFIDENCE` | Taxonomy crosswalk confidence score $< 0.85$. | Explanatory caveat attached; fallback to major group considered. |
| `CONFLICTING_EVIDENCE` | Divergence between shortage indicators and automation vulnerability. | Confidence penalized by 20 points; outlook forced to `MIXED / UNCERTAIN` if unmitigated. |
| `INTERNATIONAL_ONLY_EVIDENCE` | Entity possesses no direct Malaysian statutory or survey evidence. | Confidence capped at `MEDIUM`; explicit note on cross-border extrapolation. |
| `NO_OCCUPATION_SPECIFIC_DATA` | Profile relies on major group or sectoral proxy rather than 4-digit data. | Marked as approximate reference anchor; cannot be promoted to HIGH confidence. |
| `SPARSE_TEMPORAL_HISTORY` | Time-series contains fewer than 3 historical observation points. | Trend momentum marked tentative; long-term CAGR disabled. |
| `AGGREGATED_FALLBACK` | Profile generated as a 1-digit Major Group fallback anchor. | Used strictly for candidate role discovery when 4-digit code is unmapped. |

---

## 2. Quality Flag Distribution Across Entities

### 2.1. Level 1 Core Skills ($N = 16$)
- **Active Flags:** $0$ / $16$ skills triggered `LOW_SOURCE_COUNT`, `CONFLICTING_EVIDENCE`, or `STALE_DYNAMIC_DATA`.
- **Reason:** All 16 skills are extensively triangulated across TalentCorp MyCOL, TalentCorp Impact Study, National Policy mandates, OpenAlex scholarly corpus, and ILO task mappings (average of 4.8 independent families per skill).

### 2.2. MASCO 4-Digit Occupations ($N = 20$)
- `LOW_SOURCE_COUNT` ($N = 7$ Occupations):
  - Triggered for: `2529` (AI & Data Science Specialists NEC), `2519` (Cloud & Full-Stack Developers NEC), `2166` (Graphic & Multimedia Designers), `3322` (Commercial Sales Representatives), `3343` (Administrative & Executive Secretaries), `3514` (Web Technicians), `1219` (Business Services Managers).
  - *Mitigation:* Confidence appropriately capped at `MEDIUM` ($50.0 - 70.0$), reflecting their reliance on 2 independent families rather than 4+.
- `CONFLICTING_EVIDENCE` ($N = 0$ Occupations):
  - Zero unhandled conflicts. Earlier potential conflict between AI exposure and developer demand was cleanly resolved by decomposing exposure into automation vs. augmentation.
- `STALE_DYNAMIC_DATA` ($N = 0$ Occupations):
  - All occupational wage series are updated through OpenDOSM 2025 releases (540 days age).

### 2.3. MASCO Major Group Fallbacks ($N = 8$)
- `AGGREGATED_FALLBACK`: Triggered for all 8 major group profiles (`MAJOR_1` to `MAJOR_9`).
- `NO_OCCUPATION_SPECIFIC_DATA`: Correctly attached to all 8 major group profiles to notify M3 that they represent macroeconomic baselines rather than discrete job descriptions.

---

## 3. Data Gaps Preventing Reliable Scoring

The audit identified three genuine data gaps that are transparently surfaced rather than artificially imputed:
1. **Academic Research Velocity at Occupational Granularity:** OpenAlex tracks scholarly concepts (e.g. `machine_learning`, `ai_ethics`), NOT 4-digit occupation codes (e.g. MASCO 2512). To prevent fake vacancy estimates, `research_momentum` is strictly maintained as `null` for occupations.
2. **Sub-National State-Level Wage Disaggregation:** OpenDOSM publishes occupational wages at the national level. State-level granular distributions (e.g., Penang vs. Kelantan developer wages) are not yet integrated into M2.
3. **Green Economy Granular Classifications:** While ESG and carbon analytics skills are well-mapped, formal 4-digit MASCO codes for dedicated "Renewable Energy Grid Technicians" do not yet exist in the 2020 taxonomy; they remain subsumed under `2151` (Electrical Engineers).

---

## 4. Verification Verdict

All quality flags are operating deterministically according to spec. No synthetic smoothing or arbitrary imputation was detected.
