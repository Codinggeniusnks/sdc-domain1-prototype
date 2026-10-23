# M5 Confidence Recalibration Forensic Report v1.1.0

**Defect Reference**: P2-3 (Stage 13B Independent Review)  
**Scope**: All 16 Canonical Skills and 20 MASCO 4-Digit Occupations  
**Status**: APPROVED  

---

## 1. Problem Statement: Rating Saturation in v1.0.0

In M5 v1.0.0, confidence ratings were severely saturated:
- Total alignments across skills and roles: 77
- Mappings assigned `HIGH` confidence: 72 (93.5%)
- Mappings assigned `MEDIUM` confidence: 5 (6.5%)
- Mappings assigned `LOW` confidence: 0 (0.0%)

### Review Findings on Over-Confidence:
1. **Loss of Discriminative Power**: When virtually every mapping is rated `HIGH`, downstream users and policy analysts cannot distinguish between:
   - Hard, statutory, unambiguous alignments (e.g. `data_privacy_pdpa` enforcing statutory PDPA 2010 rules under Target 16.6).
   - Contextual, sector-dependent, or indirect alignments (e.g. an electrical engineer working on solar farms vs fossil fuel generation).
2. **Defective Calibration Criteria**: v1.0.0 conflated *relevance* with *confidence*. Even when an alignment was explicitly qualified as contingent on industry setting, it was still marked `HIGH`.

---

## 2. Recalibration Policy & Objective Rules v1.1.0

Under Stage 13C remediation, `data/sdg/m5_config_v1_1.json` instituted deterministic, objective calibration rules:

### Calibration Tiers:
- **`HIGH` Confidence Criteria**:
  1. Unambiguous direct semantic alignment to the official UN target text and indicator.
  2. Direct or foundational enabling causality.
  3. Corroborated by statutory frameworks (e.g. PDPA 2010, EQA 1974) or official technical standards (GHG Protocol, ISO 14064, IEEE).
  4. **Zero unstated sector dependencies**: The alignment holds regardless of whether the organization is a bank, factory, software consultancy, or public body.
- **`MEDIUM` Confidence Criteria**:
  1. Valid and conceptually sound alignment, but **contingent on specific sectoral deployment** (`SECTOR_DEPENDENT_ALIGNMENT`).
  2. Contingent on organizational operational setting (`CONTEXT_DEPENDENT_ALIGNMENT`).
  3. Represents employment participation as a worker beneficiary rather than institutional policy execution (`CONTEXTUAL_BENEFICIARY_ALIGNMENT`).
- **`LOW` Confidence Criteria**:
  - Permissible but weak causal linkage; eliminated from core candidate mappings to prevent noise.

---

## 3. Mathematical Distribution Before & After Remediation

Across all 16 skills and 20 occupations in M5 v1.1.0:

| Metric | M5 v1.0.0 | M5 v1.1.0 (Remediated) | Shift | Remediation Target |
|---|---|---|---|---|
| **Total Mappings Evaluated** | 77 | 76 | -1 | Purged redundant stretch mappings |
| **`HIGH` Confidence Mappings** | 72 (93.5%) | **59 (77.6%)** | -13 (-15.9%) | **< 80.0%** (Achieved) |
| **`MEDIUM` Confidence Mappings** | 5 (6.5%) | **17 (22.4%)** | +12 (+15.9%) | **> 20.0%** (Achieved) |
| **`LOW` Confidence Mappings** | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | Eliminated from canonical registry |

### Granular Breakdown by Entity Type:

#### A. Skills (16 Canonical Skills, 36 Target Alignments)
- `HIGH` Confidence: 30 / 36 (83.3%)
- `MEDIUM` Confidence: 6 / 36 (16.7%)
  - `stakeholder_communication` $\to$ Target 16.7 (`MEDIUM`, context-dependent on participatory consultation)
  - `prompt_engineering` $\to$ Target 8.2 (`MEDIUM`, context-dependent on organizational AI adoption)
  - `data_visualization` $\to$ Target 16.6 (`MEDIUM`, context-dependent on public transparency dashboards)
  - `process_mapping` $\to$ Target 8.2 (`MEDIUM`, context-dependent on workflow optimization scope)
  - `instructional_design` $\to$ Target 4.7 (`MEDIUM`, context-dependent on curriculum content containing sustainability)
  - `human_in_the_loop_qa` $\to$ Target 16.6 (`MEDIUM`, context-dependent on institutional auditing workflows)

#### B. Occupations (20 MASCO Occupations, 40 Target Alignments)
- `HIGH` Confidence: 29 / 40 (72.5%)
- `MEDIUM` Confidence: 11 / 40 (27.5%)
  - `2151` (Electrical Engineers) $\to$ Target 7.1 (`MEDIUM`, sector-dependent on clean energy grid)
  - `2151` (Electrical Engineers) $\to$ Target 7.2 (`MEDIUM`, sector-dependent on renewables)
  - `2143` (Environmental Engineers) $\to$ Target 13.2 (`MEDIUM`, sector-dependent on climate mitigation)
  - `2152` (Electronic Engineers) $\to$ Target 12.5 (`MEDIUM`, sector-dependent on circular electronics)
  - `4110` (General Office Clerks) $\to$ Target 8.5 (`MEDIUM`, beneficiary alignment)
  - `4311` (Accounting Clerks) $\to$ Target 8.5 (`MEDIUM`, beneficiary alignment)
  - `3343` (Administrative Secretaries) $\to$ Target 8.5 (`MEDIUM`, beneficiary alignment)
  - `3514` (Web Technicians) $\to$ Target 8.2 (`MEDIUM`, operational support)
  - `3322` (Commercial Sales Reps) $\to$ Target 8.2 (`MEDIUM`, commercial distribution context)
  - `2424` (Training & Development) $\to$ Target 4.7 (`MEDIUM`, content-dependent on sustainability)
  - `2166` (Graphic & Multimedia) $\to$ Target 8.2 (`MEDIUM`, commercial design context)

---

## 4. Verification Verdict

Automated benchmark `BM13_CONFIDENCE_CALIBRATION` and unit test `test_p2_3_confidence_recalibration` verify:
- High confidence percentage: **77.6%** (strictly satisfies the requirement of $\le 80.0\%$).
- Result: **PASS**. Rating saturation successfully eliminated.
