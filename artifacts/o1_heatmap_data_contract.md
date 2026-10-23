# O1 Heatmap Data Contract Specification (v1.0.0)

**Contract Identifier:** CONTRACT-O1-HEATMAP-v1.0.0  
**Target:** Future Frontend Dashboard / Heatmap Components (O1 Visualizer)  
**Status:** SCHEMA-LOCKED & READY

---

## 1. Payload Structure

The `build_heatmap_payload()` endpoint produces structured JSON without rendering HTML/UI:

```json
{
  "heatmap_version": "1.0.0",
  "metric_represented": "WORKFORCE_RESKILLING_PRIORITY_INDEX",
  "grouping_dimension": "cohort_id",
  "scenario": "REFERENCE_2026",
  "rows": [
    "ai_ethics_governance",
    "ai_literacy",
    "..."
  ],
  "columns": [
    "ADVANCED_MANUFACTURING",
    "BUSINESS_SERVICES",
    "DIGITAL_SERVICES",
    "GREEN_TRANSITION"
  ],
  "cells": [
    {
      "skill_id": "process_mapping",
      "group_id": "DIGITAL_SERVICES",
      "eligible_count": 16,
      "gap_prevalence": 0.4375,
      "core_gap_prevalence": 0.3125,
      "priority_index": 52.4,
      "suppressed": false,
      "quality_flags": [
        "HIGH_CORE_GAP_PREVALENCE"
      ]
    },
    {
      "skill_id": "process_mapping",
      "group_id": "PILOT_TEAM_A",
      "eligible_count_display": "<5",
      "gap_prevalence": null,
      "core_gap_prevalence": null,
      "priority_index": null,
      "suppressed": true,
      "quality_flags": [
        "SUPPRESSED_SMALL_CELL"
      ]
    }
  ],
  "color_scale_metadata": {
    "min_value": 0.0,
    "max_value": 100.0,
    "high_threshold": 50.0,
    "medium_threshold": 25.0,
    "palette": "blues"
  }
}
```

---

## 2. Invariants for Frontend Consumers

1. **Dimension Completeness:** Cells array contains exactly $|\text{Rows}| \times |\text{Columns}|$ entries.
2. **Explicit Semantic Metric:** `metric_represented` explicitly names the represented variable (`WORKFORCE_RESKILLING_PRIORITY_INDEX`). No ambiguous "risk score".
3. **Graceful Cell Suppression:** If `suppressed == true`, numerical values are strictly `null`; frontend must render shaded or masked badges.
