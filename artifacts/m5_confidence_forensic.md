# M5 Confidence & Evidentiary Forensic Audit

**Review Date:** 2026-10-24  
**Auditor:** Independent Senior Sustainability Taxonomy Auditor, Quantitative Methodologist  
**Artifact Evaluated:** `data/sdg/m5_config_v1.json`, `data/sdg/skill_sdg_mappings_v1.json`, `data/sdg/role_sdg_mappings_v1.json`

---

## 1. The Confidence Saturation Phenomenon

In Stage 13A, M5 reported:
- **`HIGH` Confidence:** 93.5% of all alignments.
- **`MEDIUM` Confidence:** 6.5%.
- **`LOW` Confidence:** 0.0%.

### Forensic Diagnosis:
This distribution exhibits classic **confidence saturation**. The root cause is a methodological conflation:
1. **Citation Count vs. Causal Certainty:** Stage 13A treated the existence of $\ge 2$ document citations as sufficient proof of `HIGH` confidence.
2. **Failure to Penalize Contextual Dependence:** An alignment that is explicitly labeled `CONTEXTUAL` (meaning its validity depends entirely on unstated employer or deployment circumstances) was still assigned `HIGH` confidence simply because MASCO mentions the task.
3. **Conflation with Alignment Strength:** Reviewers conflated `STRONG` alignment with `HIGH` confidence.

---

## 2. Orthogonal Separation: Confidence vs. Strength

The M5 taxonomy must enforce strict mathematical orthogonality between **Alignment Strength** and **Mapping Confidence**:

```
                       ┌─────────────────────────┬─────────────────────────┐
                       │ HIGH CONFIDENCE         │ MEDIUM CONFIDENCE       │
                       │ (Unconditional certainty)│ (Context-dependent)     │
┌──────────────────────┼─────────────────────────┼─────────────────────────┤
│ STRONG ALIGNMENT     │ Example:                │ Example:                │
│ (Core task match     │ - carbon_footprint → 12.6│ - electrical_eng → 7.2  │
│  with SDG target)    │ - accountants → 16.6    │   (requires renewable   │
│                      │ - env_eng → 13.2        │    sector deployment)   │
├──────────────────────┼─────────────────────────┼─────────────────────────┤
│ MODERATE / LIMITED   │ Example:                │ Example:                │
│ (Enabling, indirect  │ - python → 9.5          │ - clerical clerks → 8.5 │
│  or operational)     │   (well-established     │ - stakeholder_comm → 16 │
│                      │    enabling tool)       │   (operational setting) │
└──────────────────────┴─────────────────────────┴─────────────────────────┘
```

---

## 3. Recalibration Protocol for Stage 13C

To eliminate confidence inflation, the following deterministic rules must be applied:

1. **Rule 1 (Sector-Conditional Downgrade):** Any alignment flagged with `SECTOR_DEPENDENT_ALIGNMENT` (e.g. electrical engineers to renewable energy) must be capped at `MEDIUM` confidence until user or enterprise profile data confirms the employment sector.
2. **Rule 2 (Contextual Mapping Downgrade):** All `CONTEXTUAL` mappings (e.g. routine clerical support to decent work 8.5) must be assigned `MEDIUM` confidence by definition, as their SDG contribution is an indirect consequence of employment rather than an intrinsic professional outcome.
3. **Rule 3 (Target 9.c & 17.18 Elimination):** Remove overstretched Tier 4 alignments rather than grading them `LOW`. M5 should contain zero low-confidence noise.

### Projected Recalibrated Distribution:
- **`HIGH` Confidence:** 60% – 70% (Authoritative, direct, or well-established enabling relationships).
- **`MEDIUM` Confidence:** 30% – 40% (Sector-conditional, contextual, or deployment-dependent relationships).
- **`LOW` Confidence:** 0.0% (Eliminated from production datasets).
