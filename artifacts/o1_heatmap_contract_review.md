# Backend Data Contract Review: Workforce Reskilling Heatmap

**Module:** O1 Employer / HR Workforce Planning Layer  
**Engine:** `src/workforce_gap_engine.py::build_heatmap_payload`  
**Date:** 2026-10-24  
**Audit Finding:** AUDITS 56 & 57 PASS; DEFECT P2-04 NOTED FOR CELL PREVALENCE  

---

## 1. Heatmap Data Contract Overview

The `build_heatmap_payload` method generates a structured JSON payload for future frontend dashboard rendering without rendering UI components in the backend.

### Top-Level Schema:
```json
{
  "heatmap_version": "1.0.0",
  "metric_represented": "WORKFORCE_RESKILLING_PRIORITY_INDEX",
  "grouping_dimension": "cohort_id",
  "scenario": "REFERENCE_2026",
  "rows": ["process_mapping", "sql_data_analysis", "..."],
  "columns": ["COHORT_A", "COHORT_B"],
  "cells": [...],
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

## 2. Cell-Level Privacy Evaluation

When a cohort column has $N < 5$:
- All 16 skill cells are emitted with `"suppressed": true`, `"eligible_count_display": "<5"`, and null metric values. (Verified PASS).

When a cohort column has $N \ge 5$:
- Each cell reports `gap_prevalence` and `core_gap_prevalence`.
- **Finding (Defect P2-04):** If a column has $N=10$, and exactly 1 worker has a gap, `gap_prevalence = 0.10` implies $10 \times 0.10 = 1$ worker. In Stage 15C, cell-level quality flags must include `SMALL_CELL_ESTIMATE` to signal frontend consumers to mask precise prevalence for counts $< 5$.
