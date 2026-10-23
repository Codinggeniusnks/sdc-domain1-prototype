# Pathway Alignment Coverage Semantics & Governance (v1.1.0)

**Defect Addressed:** DEF-P3-01  
**Status:** IMPLEMENTED & EMBEDDED

---

## 1. Scope Clarification

Pathway Alignment Coverage measures the fraction of **planned reskilling curriculum skill steps** that carry at least one evidence-backed M5 SDG alignment.

It does **NOT** measure:
- Course or module completion
- Verified competency mastery
- Educational degree attainment
- Actual employee job transition
- Realized environmental or societal impact

---

## 2. Runtime Payload Specification

In O6 v1.1.0, all pathway alignment outputs include explicit scope and non-mastery disclaimer metadata:

```json
"pathway_alignment_coverage": {
  "total_planned_pathway_skill_instances": 48,
  "sdg_aligned_pathway_skill_instances": 36,
  "pathway_alignment_coverage_ratio": 0.7500,
  "pathway_alignment_coverage_percentage": 75.0,
  "pathway_alignment_coverage_scope": "PLANNED_CURRICULUM_SKILL_STEPS",
  "pathway_alignment_coverage_disclaimer": "Coverage reflects planned reskilling curriculum alignment, not verified course completion, skill mastery, or realised SDG impact.",
  "semantics_note": "Describes proportion of planned reskilling curriculum with sustainability relevance. Not a measure of course completion, skill mastery, educational attainment, or realized environmental impact."
}
```
