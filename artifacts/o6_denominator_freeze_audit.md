# Forensic Denominator Integrity & Validation Audit (v1.1.0)

**Component:** `SDGAggregationEngine.validate_profile_for_aggregation()`  
**Audit Scope:** Checks 9–20 & DEF-P1-01 Verification  
**Status:** PASS — FULLY HARDENED

---

## 1. Profile Validation Matrix

| Input Case | Type | Profile ID | Operational Fields | Classification Status | Reason Code | In Denominator? |
|---|---|---|---|---|---|---|
| **Valid Profile** | `dict` | Present (str) | Role + Skills | `ELIGIBLE` | `None` | **YES** |
| **Valid Role Only** | `dict` | Present (str) | Role only | `ELIGIBLE` | `None` | **YES** |
| **Confirmed Skills None** | `dict` | Present (str) | Role + `skills: None` | `ELIGIBLE` | `None` (Safe default `[]`) | **YES** |
| **Empty Dictionary** | `dict` | Absent | Zero operational fields | `EXCLUDED_INCOMPLETE` | `INCOMPLETE_PROFILE_DATA` | **NO** |
| **Missing Profile ID** | `dict` | Absent / Empty | Skills present | `EXCLUDED_INCOMPLETE` | `INCOMPLETE_PROFILE_DATA` | **NO** |
| **Zero Competencies** | `dict` | Present (str) | No role/skill/pathway | `EXCLUDED_INCOMPLETE` | `INCOMPLETE_PROFILE_DATA` | **NO** |
| **None Input** | `NoneType`| N/A | N/A | `EXCLUDED_INVALID_TYPE` | `INVALID_PROFILE_TYPE` | **NO** |
| **String Literal** | `str` | N/A | N/A | `EXCLUDED_INVALID_TYPE` | `INVALID_PROFILE_TYPE` | **NO** |
| **List Object** | `list` | N/A | N/A | `EXCLUDED_INVALID_TYPE` | `INVALID_PROFILE_TYPE` | **NO** |
| **Duplicate ID** | `dict` | Seen PID | Role + Skills | `EXCLUDED_DUPLICATE` | `DUPLICATE_PROFILE_ID` | **NO** |

---

## 2. Denominator Accounting Formula

The engine enforces exact accounting:
$$\text{input\_profile\_count} = \text{eligible\_profile\_count} + \sum \text{excluded\_profiles\_by\_reason}$$

All cohort prevalence metrics (SAP, TPI, mapping shares) use $\text{eligible\_profile\_count}$ as their denominator. In an all-invalid cohort ($N_{\text{raw}} > 0, N_{\text{elig}} == 0$), the engine returns `suppressed = True` with `INSUFFICIENT_ELIGIBLE_COHORT_DATA` rather than 0% prevalence.
