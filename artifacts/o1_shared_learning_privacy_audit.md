# Forensic Deep Dive: Shared Learning Privacy Leak

**Module:** O1 Employer / HR Workforce Planning Layer  
**Engine:** `src/workforce_gap_engine.py::identify_shared_learning_opportunities`  
**Date:** 2026-10-24  
**Audit Finding:** DEFECT P1-01 (MUST FIX BEFORE FREEZE / UI)  

---

## 1. Forensic Inspection of Source Code

Inspecting lines 705–730 of `src/workforce_gap_engine.py`:
```python
for s_id, s_data in matrix_res["skills"].items():
    count = s_data["profiles_with_gap"]
    if count >= 2:  # Shared across 2 or more individuals
        # ...
        shared_opps.append({
            "shared_skill": s_id,
            "skill_name": s_data["skill_name"],
            "profiles_affected": count,
            # ...
        })
```

---

## 2. Privacy Disclosure Analysis

1. **The Conflict of Thresholds:**
   - The overall engine enforces an employer privacy floor of $k=5$ (`minimum_cohort_threshold: 5`).
   - However, `identify_shared_learning_opportunities` sets an internal threshold of $N \ge 2$.
2. **Re-Identification Scenario:**
   - In a department of 10 workers, the tool outputs a shared learning opportunity: `"shared_skill": "instructional_design", "profiles_affected": 2`.
   - In an enterprise setting, managers often know who does what. A manager knowing that only two instructional roles exist can immediately identify which two specific employees have been flagged as possessing capability deficits.
   - In the official Stage 15A benchmark cohort ($N=50$), `instructional_design` is emitted with `"profiles_affected": 2`, directly violating the employer-facing $k=5$ privacy rule.

---

## 3. Required Remediation in Stage 15C

To resolve Defect P1-01, Stage 15C must implement:
1. **Option A (Strict Privacy Floor):** Set `if count >= self.config["privacy_safeguards"]["minimum_cohort_threshold"]:` (i.e. $N \ge 5$). Opportunities affecting 2, 3, or 4 employees are omitted from employer-facing aggregate dashboards.
2. **Option B (Masked Subgroup Reporting):** If $2 \le count < 5$, report `"profiles_affected": "<5"`, and mask the aggregate learner-hour calculation to a bounded range (e.g. `"<150 hours"`).
3. **Recommendation:** Implement Option A for public employer summaries, with Option B for export payloads, ensuring zero exact small counts ($1..4$) are ever emitted.
