# O6 to O1 Interface Specification: Employer Workforce-Gap Analytics

**Interface Identifier**: INTERFACE-O6-O1-v1.0.0  
**Upstream System**: O6 SDG Contribution Aggregation Engine v1.0.0  
**Downstream Target**: O1 Employer Workforce-Gap Heatmap & Reskilling Planner (Future Stage)  
**Author**: Enterprise Workforce Intelligence Architect  
**Status**: SPECIFIED & RATIFIED (STAGE 14A)  

---

## 1. Purpose & Scope Boundary

Module **O1: Employer Workforce-Gap Heatmap** will provide HR executives, workforce planners, and industrial transformation managers with visual heatmaps identifying corporate skill deficits, transition bottlenecks, and reskilling urgencies.

In Stage 14A, **no UI components, heatmaps, or frontend views are constructed**.  
Instead, this document defines the decoupled, structured JSON data payload that O6 computes and exposes via `o1_interface_hook` within every cohort aggregation result. This guarantees that when O1 is implemented, it consumes pre-aggregated, privacy-safe analytics directly without accessing raw employee records.

```
+------------------------------------+
|  O6 SDG Aggregation Engine v1.0.0  |
|  - Cohort Skill Gap Counts         |
|  - Core vs Important Gap Breakdown |
|  - Role Transition Distributions   |
|  - SDG-Aligned Capability Deficits |
+-----------------+------------------+
                  |
                  | (o1_interface_hook JSON Schema)
                  v
+------------------------------------+
|  O1 Workforce-Gap Heatmap (Future) |
|  - Enterprise Gap Visualizations   |
|  - Cohort Reskilling Priorities    |
+------------------------------------+
```

---

## 2. Schema Specification: `o1_interface_hook`

The `o1_interface_hook` block is embedded directly in the output dictionary of `aggregate_cohort_alignment()`:

```json
{
  "o1_interface_hook": {
    "cohort_skill_gap_counts": {
      "workflow_automation": 7,
      "python_scripting": 6,
      "prompt_engineering": 5,
      "esg_sustainability_reporting": 4,
      "rag_knowledge_systems": 3,
      "carbon_footprint_analytics": 3,
      "data_privacy_pdpa": 3,
      "sql_data_analysis": 2,
      "ai_ethics_governance": 2
    },
    "cohort_core_gap_counts": {
      "workflow_automation": 5,
      "python_scripting": 4,
      "esg_sustainability_reporting": 4,
      "carbon_footprint_analytics": 3,
      "rag_knowledge_systems": 3
    },
    "role_distribution": {
      "2512": 3,
      "2511": 2,
      "2521": 2,
      "2529": 1,
      "2519": 2,
      "2522": 2,
      "3514": 3,
      "2166": 2,
      "1330": 1
    },
    "sdg_aligned_gap_skills": [
      "workflow_automation",
      "python_scripting",
      "prompt_engineering",
      "esg_sustainability_reporting",
      "rag_knowledge_systems",
      "carbon_footprint_analytics",
      "data_privacy_pdpa",
      "sql_data_analysis",
      "ai_ethics_governance"
    ]
  }
}
```

---

## 3. Field Definitions & Downstream Utility

1. **`cohort_skill_gap_counts`**:
   - Ranked frequency distribution of all skills planned in M4 pathways across the cohort.
   - **Downstream O1 Use**: Populates the primary Y-axis of the workforce gap heatmap, highlighting which skills are most urgently required across the workforce.
2. **`cohort_core_gap_counts`**:
   - Subset of skill gaps flagged as `CORE` (critical prerequisite deficits that block job transitions).
   - **Downstream O1 Use**: Renders high-priority visual alert badges indicating immediate structural training needs.
3. **`role_distribution`**:
   - Headcount distribution across active 4-digit MASCO occupations.
   - **Downstream O1 Use**: Populates the X-axis of the heatmap, allowing enterprise planners to filter gaps by occupational department.
4. **`sdg_aligned_gap_skills`**:
   - List of identified skill deficits that possess M5 SDG alignments.
   - **Downstream O1 Use**: Bridges human-capital reskilling with ESG compliance, allowing HR leaders to identify reskilling programs that simultaneously address operational deficits and national sustainability goals (e.g. training in `carbon_footprint_analytics` addresses both corporate GHG reporting and Target 12.6).

---

## 4. Privacy & Governance Guarantees for O1

1. **Suppression Pass-Through**: If the parent cohort is suppressed ($N < 5$), the entire `o1_interface_hook` is suppressed (`None`), ensuring that small-group heatmaps cannot be rendered to expose individual workers.
2. **Non-Identifiability**: The payload contains aggregate frequencies and MASCO codes only; zero employee identifiers or individual gap vectors are exposed.
3. **No HR Decision Use**: Future O1 documentation and UI banners must repeat the mandatory guardrail prohibiting individual performance scoring or termination decisions.
