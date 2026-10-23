# Interface Contract Specification: O6 Aggregation -> O2 Executive Dashboard (v1.1.0)

**Interface Direction:** Upstream (O6) to Downstream (O2)  
**Contract Version:** v1.1.0  
**Status:** READY FOR O2 DASHBOARD INTEGRATION

---

## 1. Output Payload Contract

O2 consumes aggregated cohort intelligence containing:
- Pre-computed prevalence metrics (SAP, TPI)
- Deduplicated mapping-type distribution shares
- Capability coverage ratios
- Partition breakdown with complementary suppression
- Runtime disclaimers and governance clauses

---

## 2. Sample Output Contract Payload

```json
{
  "aggregation_id": "AGG_a1b2c3d4e5f6",
  "aggregation_level": "WORKFORCE_COHORT",
  "cohort_id": "DIGITAL_SERVICES",
  "input_profile_count": 16,
  "eligible_profile_count": 16,
  "excluded_profile_count": 0,
  "eligible_count": 16,
  "suppressed": false,
  "privacy_threshold": 5,
  "time_dimension": "CURRENT",
  "time_dimension_label": "CURRENT_CAPABILITIES",
  "sdg_alignment_prevalence": {
    "SDG_8": { "prevalence_ratio": 0.8125, "prevalence_percentage": 81.25 }
  },
  "mapping_type_distribution": {
    "direct_share": 0.2500,
    "enabling_share": 0.6500,
    "contextual_share": 0.1000,
    "counting_unit": "UNIQUE_PROFILE_TARGET_MAPPING_TYPE_RELATION"
  },
  "pathway_alignment_coverage": {
    "pathway_alignment_coverage_scope": "PLANNED_CURRICULUM_SKILL_STEPS",
    "pathway_alignment_coverage_disclaimer": "Coverage reflects planned reskilling curriculum alignment, not verified course completion, skill mastery, or realised SDG impact."
  },
  "representativeness_disclaimer": "Synthetic demonstration cohort; not statistically representative of the Malaysian national or regional workforce.",
  "data_source_class": "SYNTHETIC_DEMO",
  "governance_safeguards": {
    "hr_decision_use_prohibited": true,
    "employee_sustainability_ranking_prohibited": true,
    "synthetic_impact_quantification_prohibited": true
  }
}
```
