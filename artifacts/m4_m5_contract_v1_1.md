# M4 to M5 Downstream Interface Contract Specification v1.1.0

**Reference Milestone**: Stage 12C Remediation (Downstream Readiness)  
**Producer Module**: M4 Personalised Reskilling Pathway Engine v1.1.0  
**Consumer Module**: Future M5 SDG & Socioeconomic Impact Engine (UNBUILT)  
**Status**: FORMALIZED & BOUNDED

---

## 1. Architectural Scope & Boundary Enforcement

In accordance with strict modular boundary rules:
- **M4 is an educational reskilling pathway engine**, responsible for converting skill gaps into pedagogically valid learning sequences with verified course recommendations, effort estimates, and evidence confidence indices.
- **M4 DOES NOT calculate SDG scores, national ESG impact indices, or macroeconomic social returns**. Those responsibilities reside exclusively within future M5.
- **M4 contains zero speculative M5 code, mock SDG calculators, or premature schema couplings**.

This document defines the formal, immutable JSON contract that M4 v1.1.0 guarantees to provide to downstream systems.

---

## 2. Guaranteed M4 Pathway Output Schema

When `M4ReskillingPathwayEngine.build_pathway(profile, m3_match_result, scenario_id, cost_preference, hours_per_week)` is invoked, it returns a JSON-serializable dictionary with the following guaranteed structure:

```json
{
  "pathway_id": "PATH_20261023_P02_2512_REF",
  "version": "1.1.0",
  "worker_id": "P02",
  "worker_name": "Aisyah",
  "target_role": {
    "masco_code": "2512",
    "occupation_title": "Software and Applications Developers and Analysts (Prompt Engineer)",
    "transition_distance": "MODERATE TRANSITION",
    "m3_match_index": 78.5,
    "scenario_id": "REFERENCE_2026"
  },
  "summary": {
    "status": "RESKILLING_PATHWAY_AVAILABLE",
    "total_pathway_steps": 3,
    "missing_core_count": 2,
    "total_estimated_hours_low": 48,
    "total_estimated_hours_high": 75,
    "schedule_estimate": null
  },
  "verified_cost_summary": {
    "minimum_verified_cost_myr": 0.0,
    "maximum_verified_cost_myr": 0.0,
    "currency": "MYR",
    "low_cost_threshold_myr": 150.0,
    "cost_preference_applied": "FREE_FIRST",
    "operational_disclaimer": "For this prototype, LOW_COST is operationally defined as a verified direct resource price of RM150 or less. This is a product classification threshold, not a claim that RM150 is universally affordable. Actual affordability depends on individual socioeconomic context, employer sponsorship, and national subsidy schemes such as HRD Corp.",
    "unknown_cost_items_count": 0,
    "unknown_cost_items": []
  },
  "pathway_evidence_confidence": {
    "score": 92.3,
    "label": "HIGH",
    "components": {
      "skill_gap_evidence": 94.7,
      "prerequisite_evidence_quality": 90.5,
      "resource_verification_quality": 90.0,
      "resource_freshness": 94.7
    },
    "confidence_reducing_flags": [],
    "confidence_source_refs": [
      "DEEPLEARNING_AI_2026",
      "FREECODECAMP_2026"
    ],
    "m3_evidence_confidence_context": 85.0
  },
  "pathway_steps": [
    {
      "step_number": 1,
      "skill_id": "python_scripting",
      "skill_name": "Python Scripting",
      "phase": "FOUNDATION",
      "priority_tier": "FOUNDATION_PREREQUISITE",
      "priority_score": 92.5,
      "reason_for_priority": "Essential foundation required before progressing to advanced role competencies.",
      "deficit": 1.0,
      "direct_prerequisites": [],
      "effort_category": "SHORT",
      "estimated_hours_low": 15,
      "estimated_hours_high": 25,
      "estimate_type": "DEFICIT_SCALED_RANGE",
      "estimation_rationale": "Scaled by deficit 1.00 from base hours [15, 25]",
      "scenario_relevance": 5.0,
      "transferability_pct": 35.0,
      "status": "NOT_STARTED",
      "resources": {
        "primary_resource": {
          "resource_id": "RES_PY_01",
          "title": "Python for Everybody",
          "provider_display_name": "freeCodeCamp",
          "provider_group_id": "FREECODECAMP",
          "provider_group_name": "freeCodeCamp",
          "cost_status": "FREE",
          "cost_amount_if_verified": 0.0,
          "currency": "MYR",
          "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
          "skill_alignment": 0.95,
          "provider_reliability": 0.92,
          "last_verified_date": "2026-10-23"
        },
        "alternative_resource": null,
        "practice_resource": null,
        "resource_selection_rationale": "Primary resource selected via FREE_FIRST policy (FREE from freeCodeCamp; verified 2026-10-23)."
      }
    }
  ],
  "quality_flags": [],
  "warnings": [],
  "generated_date": "2026-10-23",
  "resource_verification_date": "2026-10-23"
}
```

---

## 3. Explicit Guarantees for Future M5 Consumption

1. **Deterministic Skill Step IDs**: All `skill_id` values correspond to the 13 canonical domain skills mapped to UNESCO/ILO taxonomy crosswalks.
2. **Pedagogical Graph Validity**: `pathway_steps` is guaranteed to be topologically sorted with zero circular dependencies.
3. **Verified Financial Metrics**: `verified_cost_summary` provides verified financial ranges (min/max in MYR) with transparent unknown-cost counts, preventing false economic precision.
4. **Decoupled Confidence Metric**: `pathway_evidence_confidence.score` measures educational metadata trustworthiness, not worker capability or M3 match fit.
5. **Zero Speculative M5 Attributes**: M4 does NOT emit `sdg_impact_score`, `decent_work_index`, or `esg_alignment_score`. M5 will compute these independently in its own lifecycle.
