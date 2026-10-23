# M5 Direct Mapping Standard Forensic Audit

**Review Date:** 2026-10-24  
**Auditor:** Independent Senior SDG Methodologist, Sustainability Taxonomy Auditor  
**Artifact Evaluated:** `data/sdg/skill_sdg_mappings_v1.json`, `data/sdg/role_sdg_mappings_v1.json`

---

## 1. The DIRECT Mapping Standard

In international sustainability taxonomies (EU Taxonomy for Sustainable Activities, UN IAEG-SDGs), `DIRECT` is the highest evidentiary tier. 

### Mandatory Criteria for `DIRECT` Classification:
1. **Intrinsic Domain Specificity:** The skill or occupational core task must inherently address the physical, institutional, or social phenomenon described in the target text.
2. **Zero Intermediary Hops:** The action itself constitutes execution of the target (not merely providing a tool or an indirect support service).
3. **Absence of Sector-Neutrality:** General-purpose capabilities (programming, data entry, basic communication) that can be applied to harmful or neutral activities as easily as sustainable activities are disqualified from `DIRECT`.

---

## 2. Line-by-Line Audit of Direct Skill Mappings

M5 v1.0.0 designated 5 canonical skills with `DIRECT` mappings:

| Skill ID | Claimed Direct Target | Forensic Evaluation | Audit Verdict | Recommended Remediation |
| :--- | :---: | :--- | :---: | :--- |
| `carbon_footprint_analytics` | **13.2** | Scope 1/2/3 carbon accounting is an enterprise disclosure activity under Target 12.6. Target 13.2 governs national public climate policy. Corporate carbon accounting enables national policy but does not directly implement it. | **TOO STRONG (P2)** | Reclassify Target 13.2 to `ENABLING`. Retain Target 12.6 as `DIRECT`. |
| `esg_sustainability_reporting` | **12.6** | The skill directly produces corporate sustainability disclosures in accordance with Bursa Malaysia, IFRS S1/S2, and GRI standards. 100% literal match with Target 12.6. | **VALID (DIRECT)** | Retain as primary `DIRECT`. |
| `ai_ethics_governance` | **16.6** | Auditing automated algorithms for demographic bias, disparate impact, and model transparency directly enforces institutional accountability and procedural fairness. | **VALID (DIRECT)** | Retain as primary `DIRECT`. |
| `data_privacy_pdpa` | **16.10** | Malaysia PDPA 2010 regulates commercial data privacy, not public access to information (Freedom of Information). Mapping PDPA directly to 16.10 is legally indefensible. | **INVALID (P1)** | Reassign `DIRECT` mapping to **Target 16.6** (accountable institutions). |
| `instructional_design` | **4.4** | Formulating technical reskilling curricula directly operationalizes Target 4.4 (*increase youth and adults with technical and vocational skills for employment*). | **VALID (DIRECT)** | Retain as primary `DIRECT`. |

---

## 3. Line-by-Line Audit of Direct Occupational Mappings

M5 v1.0.0 designated 6 MASCO 4-digit occupations with `DIRECT` mappings:

| MASCO Code | Occupation Title | Claimed Direct Targets | Forensic Evaluation | Audit Verdict | Recommended Remediation |
| :---: | :--- | :---: | :--- | :---: | :--- |
| **2143** | Environmental Engineers | **13.2, 12.6, 11.6** | Statutory engineering tasks under Board of Engineers Malaysia (BEM) include emissions abatement, effluent treatment, and municipal waste engineering. | **VALID (DIRECT)** | Add `SECTOR_DEPENDENT_ALIGNMENT` flag to account for private vs. public consultancy. |
| **2151** | Electrical Engineers | **7.2, 7.3, 9.4** | Engineering solar PV, grid battery interconnectors, and industrial power factor efficiency. However, general electrical engineers may work on fossil systems. | **SECTOR DEPENDENT (P2)** | Add explicit `SECTOR_DEPENDENT_ALIGNMENT` flag. Direct impact materializes when deployed in clean energy. |
| **2152** | Electronic Engineers (Semiconductor) | **9.5** | IC design and semiconductor fabrication directly constitute high-tech industrial R&D and technological upgrading under Malaysia's NIMP 2030. | **VALID (DIRECT)** | Retain Target 9.5 as `DIRECT`. Retain Target 7.3 as `ENABLING`. |
| **2411** | Accountants & Auditors | **16.6, 12.6** | Statutory financial auditing directly enforces Target 16.6 (fiduciary accountability). Sustainability assurance directly enforces Target 12.6. | **VALID (DIRECT)** | Retain as `DIRECT`. |
| **2422** | Policy & Corporate Planning | **16.6, 12.6** | Designing enterprise corporate governance frameworks directly enforces Target 16.6. Formulating corporate ESG transition roadmaps supports 12.6. | **VALID (DIRECT)** | Retain Target 16.6 as `DIRECT`. Reclassify Target 12.6 as `ENABLING`. |
| **2424** | Training & Staff Development | **4.4** | Designing and delivering adult vocational upskilling and TVET interventions directly executes Target 4.4. | **VALID (DIRECT)** | Retain Target 4.4 as `DIRECT`. |

---

## 4. Synthesis & Direct Standard Integrity

- **Valid Direct Mappings:** 9 / 11 (81.8%).
- **Contested / Overstated Direct Mappings:** 2 / 11 (18.2%):
  - `data_privacy_pdpa` $\to$ Target 16.10 (**P1 Defect: Reallocate to 16.6**).
  - `carbon_footprint_analytics` $\to$ Target 13.2 (**P2 Defect: Reclassify to ENABLING; promote 12.6 to DIRECT**).
- **Sector-Dependence Gap:** 2 engineering disciplines (`2151`, `2143`) require explicit conditional flags (`SECTOR_DEPENDENT_ALIGNMENT`).
