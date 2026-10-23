# Forensic Distribution Audit: Deficit Component Sensitivity

**Module:** O1 Employer / HR Workforce Planning Layer  
**Engine:** `src/workforce_gap_engine.py`  
**Dataset:** `data/aggregation/synthetic_workforce_v1.json`  
**Date:** 2026-10-24  
**Audit Finding:** DEFECT P2-02 (LIMITED BENCHMARK SENSITIVITY)  

---

## 1. Context & Motivation for Audit

In Stage 15A, all top-five benchmark skills reported:
$$\text{mean deficit} = 1.00$$

Audit 9 and 10 mandate a forensic investigation to determine whether:
- **Hypothesis A:** This is a legitimate consequence of all synthetic benchmark gaps being complete capability deficits.
- **Hypothesis B:** The synthetic data representation or engine logic collapsed continuous proficiency deficits into a binary missing/not-missing flag.

---

## 2. Empirical Distribution Analysis

We extracted every non-zero skill gap across all 50 synthetic profiles in `synthetic_workforce_v1.json` and evaluated the deficit values:

```
Total Non-Zero Deficit Instances: 284
Minimum Deficit:                  1.0000
Maximum Deficit:                  1.0000
Mean Deficit:                     1.0000
Standard Deviation:               0.0000
Unique Deficit Values:            [1.0] (Count = 1)
```

### Analysis of the Deficit Formula in Code:
In `src/workforce_gap_engine.py`:
```python
user_level = 1.0 if s_id in confirmed_skills else 0.0
# ...
deficit = max(0.0, required_level - user_level)
```
In `synthetic_workforce_v1.json`, each profile represents competencies as a simple list of confirmed skill strings (`"confirmed_skills": ["python_scripting", "sql_data_analysis", ...]`). No fractional proficiency score (e.g. `0.4` or `0.7`) is provided.
When a worker possesses a skill, `user_level = 1.0` $\implies$ `deficit = 0.0` (no gap).  
When a worker lacks a skill, `user_level = 0.0`, while `required_level = 1.0` $\implies$ `deficit = 1.0 - 0.0 = 1.0`.

---

## 3. Evaluation & Defect Classification

1. **Mathematical Correctness of Engine:** The engine's arithmetic formula `mean_deficit = sum(deficits) / count(gapped)` is mathematically sound and respects the gapped denominator.
2. **M3/M4 Preservation:** In production pipelines where M3/M4 supply continuous fractional proficiency levels, the formula preserves fractional values.
3. **Synthetic Benchmark Information Value:** Because every single non-zero deficit in the 50-person benchmark equals $1.0000$, the deficit component ($w=0.15$) contributes an unvarying $0.15 \times 1.0 \times 100 = 15.0$ points to every single gapped skill. It acts as an uninformative constant offset rather than a discriminating capability metric.

### Official Audit Classification:
- Deficit Arithmetic: **PASS**
- Deficit Distribution: **`LIMITED`** (Defect P2-02)

### Remediation Recommendation for Stage 15C:
Augment `synthetic_workforce_v1.json` or create a benchmark fixture with explicit fractional proficiency scores (e.g., beginner = 0.3, intermediate = 0.7) to empirically verify fractional deficit aggregation.
