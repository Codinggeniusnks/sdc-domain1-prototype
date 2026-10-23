# M5 Target 8.5 Decent Work & Beneficiary Alignment Specification v1.1.0

**Defect Reference**: P2-4 (Stage 13B Independent Review)  
**Occupations Audited**:
- MASCO 4110: General Office Clerks
- MASCO 4311: Accounting and Bookkeeping Clerks
- MASCO 3343: Administrative and Executive Secretaries  
**Quality Flag Introduced**: `CONTEXTUAL_BENEFICIARY_ALIGNMENT`  
**Status**: APPROVED  

---

## 1. Analysis of Defect P2-4

In M5 v1.0.0, clerical and administrative occupations were mapped to:
- **Target 8.5**: "By 2030, achieve full and productive employment and decent work for all women and men, including for young people and persons with disabilities, and equal pay for work of equal value."

### Review Finding:
1. **Conflation of Policy Drivers vs Employed Beneficiaries**:
   - Target 8.5 is primarily an institutional and labor-market macroeconomic goal. It directs governments and social partners to formulate minimum wage laws, labor inspection regimes, pay equity standards, and anti-discrimination mandates.
   - In v1.0.0, mapping general office clerks (MASCO 4110) to Target 8.5 could be misconstrued as claiming that clerical workers actively *execute* or *drive* national decent work policy.
   - In reality, clerical workers are **participants and beneficiaries** of the decent work agenda. Their gainful employment under formal contracts represents the *realization* of Target 8.5 in the labor market.
2. **Operational Conflation**:
   - Without an explicit flag, automated systems might equate a clerk's contribution to Target 8.5 with an industrial relations specialist or labor inspector.

---

## 2. Remediated Beneficiary Alignment Framework v1.1.0

Under Stage 13C remediation, a clear distinction is formalized:

### 1. The `CONTEXTUAL_BENEFICIARY_ALIGNMENT` Flag
Defined in `m5_config_v1_1.json`:
> "Role participates as an employed beneficiary within the decent work objective (Target 8.5) rather than directly executing systemic labor market policy."

### 2. Mandatory `CONTEXTUAL` Mapping Type
Clerical roles can never receive `DIRECT` or `ENABLING` mappings to Target 8.5. Their mapping type is strictly `CONTEXTUAL`.

### 3. Detailed Occupational Profiles:

| MASCO Code | Title | Target | Mapping Type | Confidence | Quality Flags | Pathway Narrative |
|---|---|---|---|---|---|---|
| **4110** | General Office Clerks | **8.5** | CONTEXTUAL | **MEDIUM** | `CONTEXTUAL_BENEFICIARY_ALIGNMENT`, `MASCO_TAXONOMY_GROUNDED` | Represents gainful formal employment within productive enterprise administration. Participation in decent work under formal labor standards fulfills Target 8.5 as an employed beneficiary. |
| **4311** | Accounting and Bookkeeping Clerks | **8.5** | CONTEXTUAL | **MEDIUM** | `CONTEXTUAL_BENEFICIARY_ALIGNMENT`, `MASCO_TAXONOMY_GROUNDED` | Formal employment in financial recordkeeping supports structured business administration and decent work participation under statutory Malaysian Employment Act standards. |
| **3343** | Administrative & Executive Secretaries | **8.5** | CONTEXTUAL | **MEDIUM** | `CONTEXTUAL_BENEFICIARY_ALIGNMENT`, `MASCO_TAXONOMY_GROUNDED` | Formal executive support employment contributes to productive organizational operations, realizing decent work participation under Target 8.5. |

### 4. Integration into Pathway Narrative
When a reskilling pathway targets a clerical occupation, `SDGImpactEngine.map_pathway_to_sdgs()` explicitly generates an explanatory disclosure in the synthesized impact narrative:
> "Note: Role-level alignment to Target 8.5 represents decent work participation as employed beneficiaries rather than institutional policy drivers."

---

## 3. Automated Invariant Verification

Benchmark `BM07_ADMINISTRATIVE_CLERICAL_CONTEXTUAL` and unit test `test_p2_4_clerical_beneficiary_flags` verify:
1. Roles 4110, 4311, and 3343 carry `CONTEXTUAL_BENEFICIARY_ALIGNMENT`.
2. Target 8.5 alignment is strictly `CONTEXTUAL`.
3. Confidence is calibrated to `MEDIUM`.
4. Automated verification returned `PASS` with zero violations.
