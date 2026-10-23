# Denominator Integrity & Cohort Tracking (v1.1.0)

**Defect Addressed:** DEF-P1-01  
**Status:** IMPLEMENTED & TESTED

---

## 1. Denominator Contract

Every cohort aggregation payload in O6 v1.1.0 maintains explicit separation between raw input count and eligible cohort count:

$$N_{\text{raw}} = \text{input\_profile\_count}$$
$$N_{\text{elig}} = \text{eligible\_profile\_count}$$
$$N_{\text{excl}} = \text{excluded\_profile\_count} = N_{\text{raw}} - N_{\text{elig}}$$

All prevalence metrics, including SDG Alignment Prevalence (SAP) and Target Prevalence Index (TPI), are strictly evaluated against $N_{\text{elig}}$:
$$SAP(s) = \frac{\sum_{i=1}^{N_{\text{elig}}} \mathbb{I}(s \in \mathcal{S}_i)}{N_{\text{elig}}}$$
$$TPI(t) = \frac{\sum_{i=1}^{N_{\text{elig}}} \mathbb{I}(t \in \mathcal{T}_i)}{N_{\text{elig}}}$$

---

## 2. Cohort Tracking Payload Structure

```json
{
  "cohort_id": "TECH_CORP_2026",
  "input_profile_count": 12,
  "eligible_profile_count": 10,
  "excluded_profile_count": 2,
  "excluded_profiles_by_reason": {
    "INCOMPLETE_PROFILE_DATA": 1,
    "INVALID_PROFILE_TYPE": 1,
    "DUPLICATE_PROFILE_ID": 0
  },
  "eligible_count": 10,
  "suppressed": false
}
```

---

## 3. Empty Eligible Cohort Handling

If $N_{\text{raw}} > 0$ but $N_{\text{elig}} == 0$:
- The engine does NOT return 0% prevalence (which would falsely imply an evaluated cohort with zero alignment).
- Instead, it returns `suppressed = True` with status `INSUFFICIENT_ELIGIBLE_COHORT_DATA`.
- Metric distributions are set to `None`.
