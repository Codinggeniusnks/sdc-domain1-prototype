# Interface Specification & Downstream Contract: M4 to M5 (SDG Impact Engine)

**Publishing Engine**: M4 Personalised Reskilling Pathway Engine v1.0.0  
**Consuming Engine**: M5 SDG Alignment & Socioeconomic Impact Mapping Engine  
**Evaluation Milestone**: Stage 12A Implementation Interface  
**Date**: 2026-10-23  
**Status**: **`FORMALLY CERTIFIED`**

---

## 1. Purpose & Architectural Relationship

This contract defines the data schema, semantic interpretations, and downstream boundaries between **M4 (Reskilling Pathway Engine)** and **M5 (SDG Impact Engine)**.

While M4 produces the personalized, step-by-step vocational roadmap toward a target occupation, M5 evaluates the broader developmental and socioeconomic impact of that reskilling pathway against the **United Nations Sustainable Development Goals (SDGs)** and national socioeconomic development frameworks (12th Malaysia Plan, National Fourth Industrial Revolution Policy).

---

## 2. Programmatic Interface Payload (M4 Output $\to$ M5 Ingestion)

M4 emits the complete pathway payload for downstream M5 impact scoring:

```json
{
  "pathway_id": "PATHWAY_2511_REFERENCE_2026",
  "target_role": "2511",
  "occupation_title": "Systems Analysts",
  "scenario_id": "REFERENCE_2026",
  "transition_distance": "SHORT TRANSITION",
  "total_pathway_steps": 3,
  "missing_core_count": 0,
  "total_estimated_hours_low": 50,
  "total_estimated_hours_high": 90,
  "schedule_estimate": {
    "study_hours_per_week": 10,
    "estimated_weeks_low": 5.0,
    "estimated_weeks_high": 9.0,
    "label": "USER-SCHEDULE-DEPENDENT ESTIMATE"
  },
  "verified_cost_summary": {
    "minimum_verified_cost_myr": 0.0,
    "maximum_verified_cost_myr": 0.0,
    "currency": "MYR",
    "cost_preference_applied": "FREE_FIRST",
    "unknown_cost_items_count": 0,
    "unknown_cost_items": []
  },
  "pathway_evidence_confidence": {
    "score": 94.5,
    "label": "HIGH",
    "components": {
      "skill_gap_evidence": 95.0,
      "prerequisite_evidence_quality": 92.0,
      "resource_verification_quality": 96.0,
      "resource_freshness": 95.0
    }
  },
  "pathway_steps": [
    {
      "step_number": 1,
      "skill_id": "api_integration",
      "skill_name": "Api Integration",
      "phase": "OPTIONAL SPECIALISATION",
      "priority_tier": "IMPORTANT_REQUIREMENT",
      "priority_score": 67.25,
      "deficit": 1.0,
      "estimated_hours_low": 20,
      "estimated_hours_high": 35,
      "resources": {
        "primary_resource": {
          "resource_id": "RES_API_01",
          "title": "Client-Side Web APIs and REST Fundamentals",
          "provider": "Mozilla Developer Network (MDN)",
          "cost_status": "FREE"
        }
      }
    }
  ]
}
```

---

## 3. SDG Target Mapping Framework for M5 Consumption

M5 consumes M4 pathway metadata to compute impact scores across four primary United Nations SDG targets:

| UN SDG Target | Mapping Dimension | Consumed M4 Payload Attributes | Intended M5 Impact Calculation |
|:---|:---|:---|:---|
| **SDG 4: Quality Education** (Target 4.4: Relevant skills for employment) | Free & Open Educational Access | `verified_cost_summary.minimum_verified_cost_myr`, `resources.cost_status`, `total_estimated_hours` | Evaluates democratized access to vocational training; rewards zero-cost learning pathways that eliminate tuition barriers. |
| **SDG 8: Decent Work & Economic Growth** (Target 8.2: Economic productivity & diversification) | Workforce Mobility & Automation Resilience | `target_role`, `transition_distance`, `missing_core_count`, `pathway_steps.phase` | Quantifies transition velocity from automation-pressured occupations into resilient, high-productivity digital roles. |
| **SDG 10: Reduced Inequalities** (Target 10.2: Empower and promote social & economic inclusion) | Demographic Neutrality & Barrier Elimination | `warnings` (stripping audit), `cost_preference_applied` | Measures equity of access regardless of learner age, gender, race, or educational prestige background. |
| **SDG 13: Climate Action** (Target 13.3: Improve education on climate change mitigation) | Green Skills & ESG Disclosure | `pathway_steps.skill_id` matching `carbon_footprint_analytics`, `esg_sustainability_reporting` | Tracks the national diffusion of carbon accounting and environmental reporting capabilities. |

---

## 4. Downstream Safety Guardrails for M5

To preserve methodological integrity across domain boundaries:
1. **Read-Only Consumption**: M5 is an **evaluator**, not a planner. M5 must **never** modify the sequence of pathway steps, inject ungrounded courses, or alter estimated hours.
2. **No Penalization of Low-Hour Pathways**: Efficient pathways (e.g., short 2-step transitions) must not receive lower SDG 4 impact scores solely because they require fewer study hours. Rapid, targeted upskilling is economically virtuous.
3. **Transparent Traceability**: M5 SDG impact scores must cite the specific M4 skills and resources that substantiate each development indicator.

---

## 5. Interface Certification

M4 v1.0.0 certifies that this data contract provides complete, structured, and auditable inputs for all future M5 implementations.
