# M5 Target 16.10 vs 16.6 Legal & Semantic Remediation Report v1.1.0

**Defect Reference**: P1-2 (Stage 13B Independent Review)  
**Legal Framework**: Malaysian Personal Data Protection Act 2010 (Act 709)  
**UN SDG Standard**: Target 16.10 vs Target 16.6  
**Status**: APPROVED  

---

## 1. Legal Analysis & Defect Description

In M5 v1.0.0, the competency `data_privacy_pdpa` was mapped to:
- **Target 16.10**: "Ensure public access to information and protect fundamental freedoms, in accordance with national legislation and international agreements."

This mapping suffered from a severe legal and policy category error:
1. **Nature of Target 16.10**:
   - Indicator 16.10.1: Number of verified cases of killing, kidnapping, enforced disappearance, arbitrary detention and torture of journalists, associated media personnel, trade unionists and human rights advocates.
   - Indicator 16.10.2: Number of countries that adopt and implement constitutional, statutory and/or policy guarantees for public access to information.
   - Target 16.10 is the international **Freedom of Information (FOI)** and press freedom target. It aims to compel public authorities to declassify and release government-held information for citizen oversight.
2. **Nature of Malaysian PDPA 2010 (Act 709)**:
   - The Malaysian Personal Data Protection Act 2010 is a commercial data privacy statute enacted under Federal List powers to regulate the processing of personal data in commercial transactions by data users.
   - PDPA enforces confidentiality, access restriction, data security, and consent. It operates in exact conceptual tension with public disclosure: while FOI promotes disclosing government records to the public, PDPA restricts commercial entities from releasing personal records.
   - Crucially, under Section 3(1), the PDPA 2010 **explicitly does not apply to the Federal Government and State Governments**.
   - Therefore, citing PDPA 2010 as direct evidence for Target 16.10 (public access to information) represented an untenable legal contradiction.

---

## 2. Remediated Mapping to Target 16.6

Under Stage 13C remediation, `data_privacy_pdpa` has been reallocated to **Target 16.6**:
- **Official Text of Target 16.6**: "Develop effective, accountable and transparent institutions at all levels."
- **Institutional Governance Grounding**:
  - Compliance with statutory data protection regimes (such as Act 709, General Data Protection Regulation principles, and mandatory data breach notification standards) is a foundational requirement for building trustworthy, accountable, and legally compliant institutions.
  - By establishing robust data protection principles (Notice and Choice, Disclosure, Security, Retention, Data Integrity, and Access Principles under Section 5(1) of Act 709), organizations implement accountable governance structures that safeguard citizen and consumer rights.
- **Mapping Classification**:
  - `mapping_type`: `DIRECT`
  - `alignment_strength`: `STRONG`
  - `confidence`: `HIGH`
  - `target_id`: `16.6`
  - `quality_flags`: `["DIRECT_GOVERNANCE_ROLE", "OFFICIAL_TARGET_TRACEABLE", "TARGET_SEMANTIC_REMEDIATED"]`
  - `evidence_references`: "Malaysian Personal Data Protection Act 2010 (Act 709); Personal Data Protection Department (JPDP) Standards; UN SDG Target 16.6 (effective, accountable and transparent institutions)."

---

## 3. Automated Invariant Verification

Benchmark `BM10_TARGET_16_10_BOUNDARY` and unit test `test_p1_2_pdpa_target_16_6_reallocation` confirm:
1. Target 16.10 is completely absent from `data_privacy_pdpa` and all other Domain 1 skills.
2. `data_privacy_pdpa` possesses a validated `DIRECT` alignment to Target 16.6 with `HIGH` confidence.
3. Automated verification returned `PASS` with zero regression findings.
