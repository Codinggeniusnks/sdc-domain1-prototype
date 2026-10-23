# Forensic Deep Dive: Role Transition Small-Cell Privacy Leak

**Module:** O1 Employer / HR Workforce Planning Layer  
**Engine:** `src/workforce_gap_engine.py::build_role_gap_summary`  
**Date:** 2026-10-24  
**Audit Finding:** DEFECT P1-02 (MUST FIX BEFORE FREEZE / UI)  

---

## 1. Forensic Inspection of Source Code

Inspecting lines 565–585 of `src/workforce_gap_engine.py`:
```python
role_transitions: List[Dict[str, Any]] = []
for (c_code, t_code), count in sorted(transition_counts.items(), key=lambda x: -x[1]):
    c_title = self.m3.roles.get(c_code, {}).get("occupation_title", f"Role {c_code}")
    t_title = self.m3.roles.get(t_code, {}).get("occupation_title", f"Role {t_code}")
    role_transitions.append({
        "current_masco": c_code,
        "current_role_title": c_title,
        "target_masco": t_code,
        "target_role_title": t_title,
        "transition_volume": count,
        "transition_percentage": round(count / eligible_count * 100, 2),
        "common_missing_core_skills": sorted(list(missing_core_by_transition.get((c_code, t_code), []))),
        "average_pathway_effort_range": [30, 60]
    })
```

---

## 2. Privacy Disclosure Analysis

In the 50-profile synthetic cohort:
- Total role transitions evaluated: **33**
- Number of transitions with volume $< 5$: **33 (100%)**
- Examples of emitted records:
  - `Role 2151 -> Role 2151`: volume = 4 (8.00%)
  - `Role 2143 -> Role 2143`: volume = 4 (8.00%)
  - `Role 2152 -> Role 2152`: volume = 3 (6.00%)
  - `Role 2511 -> Role 2512`: volume = 1 (2.00%)

In an enterprise workforce, reporting that exactly 1 individual from MASCO 2511 is targeting MASCO 2512 discloses that individual's private career transition plans directly to HR or executive leadership.

---

## 3. Required Remediation in Stage 15C

To resolve Defect P1-02, Stage 15C must update `build_role_gap_summary`:
1. Transitions with `count < 5` must have their volume masked:
   ```python
   "transition_volume_display": "<5" if count < 5 else str(count),
   "transition_percentage_display": "<10%" if count < 5 else f"{pct}%",
   ```
2. Any transition with `count < 5` must omit individual-identifying transition details unless aggregated into major occupational groups or filtered out of the top transition view.
