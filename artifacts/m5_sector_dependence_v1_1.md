# M5 Sector-Dependence in Engineering Occupations v1.1.0

**Defect Reference**: P2-2 (Stage 13B Independent Review)  
**Occupations Audited**:
- MASCO 2151: Electrical Engineers
- MASCO 2143: Environmental Engineers
- MASCO 2152: Electronic Engineers  
**Quality Flag Introduced**: `SECTOR_DEPENDENT_ALIGNMENT`  
**Status**: APPROVED  

---

## 1. Analysis of Defect P2-2

In M5 v1.0.0, general engineering occupations were assigned direct and unqualified alignments to green targets:
- MASCO 2151 (Electrical Engineers) $\to$ Target 7.1 & 7.2 (`DIRECT`, `HIGH` confidence)
- MASCO 2143 (Environmental Engineers) $\to$ Target 13.2 (`DIRECT`, `HIGH` confidence)
- MASCO 2152 (Electronic Engineers) $\to$ Target 12.5 (`DIRECT`, `HIGH` confidence)

### Contextual Defect Identified in Review:
1. **Occupational Granularity vs Industrial Sector**:
   - The 4-digit MASCO classification defines the **functional occupation**, not the **employing industry sector**.
   - An electrical engineer (MASCO 2151) may be employed in fossil-fuel power plants, offshore oil platforms, or luxury commercial real estate, where their day-to-day duties have zero relation to renewable energy expansion (Target 7.2).
   - An environmental engineer (MASCO 2143) may work on routine municipal drainage permits or industrial effluent compliance without working on national climate change mitigation (Target 13.2).
   - An electronic engineer (MASCO 2152) may design consumer gadgets with planned obsolescence rather than circular e-waste recycling (Target 12.5).
2. **Confidence Saturation**:
   - Marking these broad engineering occupations as `HIGH` confidence `DIRECT` contributors to SDG 7 and 13 generated substantial false-positive sustainability claims and inflated impact reporting.

---

## 2. Remediated Sector-Dependence Framework v1.1.0

Under Stage 13C remediation, all three engineering occupations have been audited and equipped with explicit sector-dependence safeguards:

### 1. `SECTOR_DEPENDENT_ALIGNMENT` Flagging
Each affected role is assigned the quality flag `SECTOR_DEPENDENT_ALIGNMENT`, formally defined in `m5_config_v1_1.json`:
> "SDG alignment is contingent on employment within a specific industry sector (e.g., clean energy, renewables, environmental remediation)."

### 2. Confidence Calibration to `MEDIUM`
The confidence level for sector-dependent targets has been calibrated from `HIGH` to `MEDIUM` in accordance with the confidence calibration rules:
> "MEDIUM applies to valid mappings that are sector-dependent (SECTOR_DEPENDENT_ALIGNMENT), application-dependent (CONTEXT_DEPENDENT_ALIGNMENT), or contextual beneficiary alignments (CONTEXTUAL_BENEFICIARY_ALIGNMENT)."

### 3. Detailed Occupational Alignments:

| MASCO Code | Title | Target | Type | Strength | Confidence | Required Sector Condition |
|---|---|---|---|---|---|---|
| **2151** | Electrical Engineers | **7.1** | DIRECT | STRONG | **MEDIUM** | Contingent on deployment in renewable energy generation, smart grid modernization, or rural electrification projects. |
| **2151** | Electrical Engineers | **7.2** | DIRECT | STRONG | **MEDIUM** | Contingent on deployment in solar PV, wind, biomass, or energy storage design (aligned with Malaysia NETR). |
| **2143** | Environmental Engineers | **13.2** | DIRECT | STRONG | **MEDIUM** | Contingent on deployment in climate mitigation engineering, facility decarbonization roadmaps, or carbon capture systems. |
| **2143** | Environmental Engineers | **12.6** | DIRECT | STRONG | **HIGH** | Statutory environmental impact assessments (EIA) and effluent verification under Environmental Quality Act 1974. |
| **2152** | Electronic Engineers | **9.5** | ENABLING | STRONG | **HIGH** | Semiconductor IC design and automated industrial testing equipment under NIMP 2030. |
| **2152** | Electronic Engineers | **12.5** | ENABLING | MODERATE | **MEDIUM** | Contingent on circular electronics design, RoHS compliance, and WEEE e-waste reduction engineering. |

---

## 3. Automated Invariant Verification

Benchmark `BM05_GREEN_ENGINEERING_OCCUPATIONS` and unit test `test_p2_2_sector_dependence_flags` verify:
1. Roles 2151, 2143, and 2152 carry `SECTOR_DEPENDENT_ALIGNMENT` in their `quality_flags`.
2. All sector-dependent primary alignments carry `MEDIUM` confidence.
3. Verification returned `PASS` with zero violations.
