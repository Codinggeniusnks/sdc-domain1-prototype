# O1 SDG Capability Context Contract (v1.0.0)

**Contract Scope:** Downstream Integration of M5 & O6 SDG Metadata  
**Status:** DESCRIPTIVE METRIC CONTRACT VERIFIED

---

## 1. Integration Scope

O1 consumes frozen M5 v1.1.0 and O6 v1.1.0 alignment metadata to attach sustainability capability context to organizational reskilling priorities:
- **Target References:** Identifies UN SDG targets supported by priority skills (e.g. `8.2`, `8.5`, `9.5`, `12.6`, `13.2`, `16.6`).
- **Mapping Types:** Surfaces evidence tiers (`DIRECT`, `ENABLING`, `CONTEXTUAL`).
- **Cohort Prevalence Context:** Reports the proportion of the eligible workforce currently holding competencies aligned to specific SDGs.

---

## 2. Anti-Greenwashing & Governance Safeguards

1. **Zero Corporate Impact Scoring:**
   O1 outputs strictly omit corporate SDG impact scores, ESG performance ratings, or fabricated quantitative impact claims (e.g. "this training saved 500 tonnes of CO2" or "created 20 green jobs").
2. **Quality Flag Attachment:**
   All SDG context payloads embed:
   `"sdg_mappings_status": "DESCRIPTIVE_ALIGNMENT_NOT_IMPACT"`
3. **Mandatory Disclaimer:**
   `"SDG capability alignments reflect descriptive competency mapping and do not represent corporate carbon reduction, job creation, or societal impact scoring."`
