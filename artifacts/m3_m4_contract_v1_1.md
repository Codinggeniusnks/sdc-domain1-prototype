# M3-to-M4 Downstream Interface & Safety Contract (v1.1.0)

**Interface Milestone**: Stage 11C Remediation Certified  
**Source Engine**: M3 Explainable Role Matching Engine v1.1.0  
**Target Consumer**: M4 Course Recommendation & Learning Pathways Engine  
**Contract Status**: **`CERTIFIED & READY FOR M4 CONSUMPTION`**  

---

## 1. Downstream Consumption Principles

The interface between M3 (Role Matching) and M4 (Learning Pathways) is governed by 5 core principles:
1. **Gap-Grounded Curriculum**: M4 must recommend courses targeting **only verified skill gaps** identified by M3. M4 must never hallucinate new prerequisites outside M3's role catalog.
2. **Deficit-Prioritized Sequencing**: M4 must sequence learning interventions strictly by requirement priority:
   $$\text{Missing Core Skills} \;\succ\; \text{Missing Important Skills} \;\succ\; \text{Missing Supporting Skills}$$
3. **No Redundant Coursework**: M4 must verify that skills marked as `matched_skills` (credit $\ge 0.50$) are **excluded** from required learning pathways.
4. **Evidence-Gated Recommendations**: Roles with `INSUFFICIENT` evidence confidence ($ECI < 25.0$) must not generate high-commitment or expensive certification pathways.
5. **Non-Hiring Context**: M4 pathways represent developmental reskilling roadmaps, not mandatory hiring prerequisites.

---

## 2. Standardized M3 $\rightarrow$ M4 Data Contract

For any matched candidate role, M3 v1.1.0 provides the following payload:

```json
{
  "masco_code": "2512",
  "occupation_title": "Software Developers",
  "role_match_index": 52.6,
  "match_strength_label": "GOOD FIT WITH GAPS",
  "evidence_confidence_index": 88.2,
  "evidence_confidence_label": "HIGH",
  "transition_distance": "MODERATE TRANSITION",
  "transition_distance_factor": 0.75,
  "core_requirements_count": 2,
  "matched_core_count": 1,
  "missing_core_count": 1,
  "core_coverage_pct": 50.0,
  "gaps": {
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
    "total_gap_count": 3
  },
  "confidence_reducing_flags": [],
  "data_completeness": "COMPLETE"
}
```

---

## 3. M4 Consumption Rules

### Rule 1: Pathway Assembly Hierarchy
M4 must generate modular learning stages conforming to M3's transition distance:
* **Stage 1 (Core Bridge)**: Targets `missing_core_skills`. Completion bridges core requirement coverage to 100%.
* **Stage 2 (Operational Modernization)**: Targets `missing_important_skills`. Focuses on workflow automation and cross-functional tooling.
* **Stage 3 (Advanced Augmentation)**: Targets `missing_supporting_skills`. Covers specialized emerging tools (e.g. RAG, copilot prompting).

### Rule 2: Handling Empty or Degenerate Profiles
When M3 returns `status = "INSUFFICIENT_PROFILE_DATA"` (`role_matches = []`), M4 **must not** generate speculative course recommendations. Instead, M4 displays a foundational competency discovery prompt:
> *"Declare or confirm at least one demonstrable competency to receive targeted career pathway recommendations."*

### Rule 3: Proxy-Mapped Evidence Warnings
For roles with `data_completeness = "PARTIAL"` or `evidence_confidence_label = "MEDIUM"` (e.g. role `2519` or `3322`), M4 must append an advisory note:
> *"Advisory: Role requirements are mapped via crosswalk proxy. Course pathways reflect general industry practices and should be verified against employer-specific requirements."*
