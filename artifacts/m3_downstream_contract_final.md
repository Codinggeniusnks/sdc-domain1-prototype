# Downstream Safety Contract & Interface Specification: M3 to M4 / UI

**Publishing Module**: M3 Explainable Future-Role Matching Engine v1.1.0  
**Consuming Modules**: M4 Course Recommendation Engine & Front-End Career Compass UI  
**Effective Date**: 2026-10-23  
**Status**: **`FORMALLY CERTIFIED`**

---

## 1. Executive Summary & Governance Boundaries

This contract establishes the programmatic data schema, semantic interpretations, and safety boundaries governing how downstream consumers (M4 Course Recommendation and user-facing UI) consume M3 Role Matching outputs.

### Strict Downstream Guardrails
1. **No Probabilistic Employment Claims**: Downstream systems must **never** present the Role Match Index ($0–100$) as an "employment probability", "hiring likelihood", or "job placement guarantee". It must strictly be labeled as a **"Competency & Readiness Matching Index"**.
2. **Orthogonal Confidence Consumption**: M4 must **never** interpret `evidence_confidence` as a skill deficit, learning priority, or learner weakness. Evidence Confidence reflects evidentiary certainty of labor market data, not learner capability.
3. **Core-First Upskilling Mandate**: M4 course generation algorithms must prioritize closing `missing_core_count` before recommending elective or supporting skill modules.

---

## 2. Programmatic Payload Schema (M3 Output $\to$ M4 Input)

Each role match object returned by `rank_roles()` adheres to the following JSON specification:

```json
{
  "masco_code": "2512",
  "role_title": "Software Developer",
  "role_match_index": 82.4,
  "match_strength_label": "STRONG CURRENT FIT",
  "evidence_confidence_index": 88.5,
  "evidence_confidence_label": "HIGH",
  "core_requirements_count": 3,
  "matched_core_count": 2,
  "missing_core_count": 1,
  "core_coverage_pct": 66.7,
  "overall_skill_fit_score": 78.5,
  "contextual_scores": {
    "m2_labor_growth_score": 84.0,
    "m6_scenario_multiplier": 1.15,
    "m6_scenario_score": 88.0,
    "effective_context_contribution": 24.2
  },
  "skill_gaps": [
    {
      "skill_id": "api_integration",
      "skill_name": "API Integration",
      "requirement_strength": "CORE_REQUIREMENT",
      "user_proficiency": 0.0,
      "required_proficiency": 0.85,
      "deficit": 0.85,
      "learning_priority": 1,
      "source_ids": ["DOSM_MASCO_2020", "MYCOL_VACANCY_2025"],
      "publisher_count": 2
    },
    {
      "skill_id": "docker_containerization",
      "skill_name": "Docker Containerization",
      "requirement_strength": "IMPORTANT_REQUIREMENT",
      "user_proficiency": 0.25,
      "required_proficiency": 0.70,
      "deficit": 0.45,
      "learning_priority": 2,
      "source_ids": ["MDEC_DIGITAL_TALENT_2024"],
      "publisher_count": 1
    }
  ],
  "explanations": {
    "fit_summary": "Strong competency overlap in Python scripting and SQL data analysis.",
    "core_gap_summary": "Missing 1 core competency: API Integration.",
    "labor_outlook_summary": "High employment growth (+4.2% p.a.) evidenced by DOSM and MyCOL data.",
    "scenario_outlook_summary": "Strongly resilient under Rapid AI Acceleration scenario (+15% demand).",
    "evidence_certainty_summary": "High evidence certainty supported by 3 independent Malaysian labor publishers."
  },
  "quality_flags": [],
  "warnings": []
}
```

---

## 3. Core Contract Fields for M4 Course Recommendation

### A. Core Requirements Invariant
Downstream M4 logic must verify:
$$\text{missing\_core\_count} + \text{matched\_core\_count} \equiv \text{core\_requirements\_count}$$
If `missing_core_count > 0`, M4 course pathway generation must tag the learning pathway as **"Bridging Core Gaps"** rather than "Elective Upskilling".

### B. Ordered Skill Gaps Contract
The `skill_gaps` array is pre-sorted by M3 according to learning priority:
1. `requirement_strength == "CORE_REQUIREMENT"` (sorted descending by `deficit`)
2. `requirement_strength == "IMPORTANT_REQUIREMENT"` (sorted descending by `deficit`)
3. `requirement_strength == "SUPPORTING_REQUIREMENT"` (sorted descending by `deficit`)

M4 is strictly prohibited from re-ordering core gaps behind supporting skills based on course popularity, sponsor placement, or course duration.

---

## 4. UI Delivery & Explainability Rules

### Rule 1: Dual Metric Display
The UI must display Match Strength and Evidence Confidence as two distinct visual indicators:
* **Primary Indicator**: Match Strength (Progress Bar or Score Pill, labeled e.g., "Match Score: 82 / 100 — Strong Current Fit").
* **Secondary Indicator**: Evidence Certainty (Badge, labeled e.g., "Evidence Quality: High — Verified by 3 National Sources").

The UI must **never** blend them into a single synthetic number (e.g., displaying $82 \times 0.885 = 72.5$).

### Rule 2: Insufficient Confidence Handling
If `evidence_confidence_label == "INSUFFICIENT"`, the UI must:
1. Display an informational banner: *"Limited labor market evidence available for this emerging occupation."*
2. Render the computed match score with an amber cautionary icon.
3. Provide the user with an option to explore the role while highlighting data limitations.

### Rule 3: Faithful Explanation Attribution
UI explanation cards must quote directly from the structured `explanations` object. No generative model may invent qualitative claims that cannot be traced to the `source_ids` or `contextual_scores`.

---

## 5. Standardized System Terminology

To maintain audit consistency across all project domains, the following terminology conventions are mandatory:

| Topic | Approved Terminology | Strictly Prohibited Terminology |
|:---|:---|:---|
| **Role Match Index** | Competency and readiness matching index | Employment probability, hiring likelihood, job guarantee |
| **Evidence Confidence** | Data certainty and evidence robustness | Applicant confidence, worker capability, test score |
| **Synthetic Personas** | Sanity tests and robustness evaluations | Empirical accuracy validation, ground-truth benchmarks |
| **School Attribute** | Excluded background / proxy feature | Protected demographic attribute |
| **Low-Fit Roles** | Developing transition / Distant transition | Failed match, rejected applicant |

---

## 6. Contract Sign-Off

M3 v1.1.0 certifies this downstream safety contract as binding for all Stage 12 implementations. Downstream systems adhering to this contract are assured mathematical consistency, explainability faithfulness, and demographic safety.
