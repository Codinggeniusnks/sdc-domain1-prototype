# Technical Specification: Deterministic Profile Validation Layer (v1.1.0)

**Component:** `SDGAggregationEngine.validate_profile_for_aggregation()`  
**Defect Addressed:** DEF-P1-01  
**Status:** IMPLEMENTED & TESTED

---

## 1. Overview & Architectural Role

In O6 v1.0.0, raw inputs were loosely iterated over, leading to two severe vulnerabilities:
1. Profiles with `"confirmed_skills": None` crashed with `TypeError: 'NoneType' object is not iterable` when constructing skill sets.
2. Malformed or empty dictionary inputs (e.g. `{}`) silently incremented the cohort denominator ($N_{\text{elig}} += 1$), improperly diluting prevalence metrics.

In O6 v1.1.0, all input records must pass through `validate_profile_for_aggregation()` before reaching any aggregation logic or defaulting procedures.

---

## 2. Validation State Machine

```
Input Record
    │
    ├─► Not isinstance(record, dict)? ──────► EXCLUDED_INVALID_TYPE
    │                                          (Reason: INVALID_PROFILE_TYPE)
    │
    ├─► Contains forbidden demographic key? ─► Raise ValueError
    │                                          (Anti-Surveillance / Privacy Policy)
    │
    ├─► Missing or empty profile_id? ────────► EXCLUDED_INCOMPLETE
    │                                          (Reason: INCOMPLETE_PROFILE_DATA)
    │
    ├─► Zero operational competencies? ─────► EXCLUDED_INCOMPLETE
    │   (no role, skills, pathway, target)    (Reason: INCOMPLETE_PROFILE_DATA)
    │
    └─► Valid Operational Profile ──────────► ELIGIBLE
```

---

## 3. Safe Defaulting Rules

For eligible profiles, optional attributes are defaulted defensively:
```python
confirmed_skills = set(list(profile.get("confirmed_skills") or []))
pathway_data = profile.get("reskilling_pathway") or {}
planned_skills = list(pathway_data.get("planned_skills") or [])
current_role_data = profile.get("current_role") or {}
target_role_data = profile.get("target_role") or {}
```
These safe defaults guarantee that legitimate profiles with missing optional fields operate smoothly without raising exceptions, while malformed records are strictly excluded beforehand.
