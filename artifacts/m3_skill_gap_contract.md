# M3 Skill-Gap Extraction & Transition Distance Contract

**Engine Version**: M3 v1.0.0  
**Interface**: `engine.get_role_skill_gaps(profile, masco_code)`  
**Status**: `CERTIFIED & CONTRACT BOUND`  
**Date**: 2026-10-23  

---

## 1. Governing Principle & Scope

The skill-gap interface in M3 is responsible for **extracting and categorizing missing competencies required for a candidate role**. 

### Critical Scope Boundary
- **What M3 DOES**: Identifies matched skills, missing core requirements, missing important skills, missing supporting skills, core requirement coverage percentage, and transition distance.
- **What M3 DOES NOT DO**: **M3 does NOT invent courses, credit hours, training durations, or learning pathway sequences.** That responsibility belongs strictly to downstream Module M4.

---

## 2. Skill Gap Schema & Data Contract

When `engine.get_role_skill_gaps(profile, masco_code)` is called, the output strictly conforms to the following schema:

```json
{
  "masco_code": "2512",
  "occupation_title": "Software Developers",
  "core_requirements_count": 2,
  "matched_core_count": 1,
  "core_coverage_pct": 50.0,
  "matched_skills": [
    {
      "skill_id": "python_scripting",
      "strength": "CORE_REQUIREMENT",
      "user_credit": 1.0
    }
  ],
  "missing_core_skills": [
    {
      "skill_id": "api_integration",
      "strength": "CORE_REQUIREMENT",
      "user_credit": 0.0,
      "deficit": 1.0
    }
  ],
  "missing_important_skills": [
    {
      "skill_id": "sql_data_analysis",
      "strength": "IMPORTANT",
      "user_credit": 0.0,
      "deficit": 1.0
    },
    {
      "skill_id": "workflow_automation",
      "strength": "IMPORTANT",
      "user_credit": 0.0,
      "deficit": 1.0
    }
  ],
  "missing_supporting_skills": [
    {
      "skill_id": "rag_knowledge_systems",
      "strength": "SUPPORTING",
      "user_credit": 0.0,
      "deficit": 1.0
    }
  ],
  "total_gap_count": 4,
  "transition_distance": "MODERATE TRANSITION",
  "transition_distance_factor": 0.75
}
```

---

## 3. Skill Deficit Quantification

For every skill required by a role, the deficit is mathematically computed as:
$$\text{Deficit}(s) = \max(0.0, 1.0 - C(s))$$
where $C(s)$ is the effective user credit derived from the User Override Hierarchy:
- `USER_CONFIRMED / USER_ADDED`: $C(s) = 1.0 \implies \text{Deficit} = 0.0$ (Fully Met)
- `M1_CORE`: $C(s) = 0.85 \implies \text{Deficit} = 0.15$ (Substantially Met)
- `M1_SUGGESTED`: $C(s) = 0.50 \implies \text{Deficit} = 0.50$ (Partially Met)
- `DISMISSED / ABSENT`: $C(s) = 0.0 \implies \text{Deficit} = 1.0$ (Complete Gap)

A skill is considered **matched** if $C(s) \ge 0.50$; otherwise, it is classified as a **gap**.

---

## 4. Transition Distance Determination Rules

Transition distance represents the estimated volume and complexity of skill acquisition needed to achieve role readiness:

| Transition Distance Tier | Criteria | Distance Factor ($F_{\text{trans}}$) | Semantic Interpretation |
|:---|:---|:---:|:---|
| **`SHORT TRANSITION`** | $\text{Core Coverage} \ge 75\%$ AND $\text{Missing Core} \le 1$ | **1.00** | Immediate transition potential; candidate possesses majority of primary technical skills. |
| **`MODERATE TRANSITION`** | $\text{Core Coverage} \ge 50\%$ AND $\text{Missing Core} \le 2$ | **0.75** | Viable career progression target; requires bridging 1–2 primary technical competencies. |
| **`SUBSTANTIAL TRANSITION`** | $\text{Core Coverage} \ge 25\%$ OR $\text{Missing Core} \le 3$ | **0.45** | Substantial career pivot; multiple core gaps require focused structured upskilling. |
| **`LONG TRANSITION`** | $\text{Core Coverage} < 25\%$ OR $\text{Missing Core} \ge 4$ | **0.15** | Deep occupational shift; foundational retraining required across multiple disciplines. |

---

## 5. Metric Interpretation Guardrail

> [!IMPORTANT]
> `core_coverage_pct` is strictly a measure of **task requirement coverage** based on catalog evidence. It is **NOT** a probability of passing a job interview, receiving an offer, or succeeding in employment. Downstream user interfaces must present this clearly as a learning gap checklist.
