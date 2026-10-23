# Partition-Aware Complementary Suppression & Differencing Resilience (v1.1.0)

**Defect Addressed:** DEF-P2-02  
**Status:** IMPLEMENTED & VERIFIED

---

## 1. Differencing Threat & Complementary Suppression Mechanics

When a workforce cohort is partitioned across an attribute (e.g., department, region), primary threshold suppression ($k=5$) alone is insufficient. If a parent cohort of $N=10$ is partitioned into Subcohort A ($N=6$) and Subcohort B ($N=4$):
- Subcohort B ($N < 5$) is suppressed.
- If Subcohort A ($N=6$) and Parent ($N=10$) are displayed, an attacker computes:
  $$\text{Aggregate}(B) = \text{Aggregate}(\text{Parent}) - \text{Aggregate}(A)$$
  This completely defeats small-cell suppression.

---

## 2. Implementation: `aggregate_partition_breakdown()`

In O6 v1.1.0, the engine implements partition-aware complementary suppression:
1. It partitions profiles by the requested attribute and evaluates the parent total and child cells.
2. Any cell with $0 < N_{\text{elig}} < k$ is marked `SUPPRESSED_SMALL_COHORT`.
3. If small cells exist, the engine deterministically selects the **smallest non-small eligible sibling** ($N_{\text{elig}} \ge k$) and suppresses it as well, setting:
   - `suppression_reason: "SUPPRESSED_COMPLEMENTARY_RULE"`
   - Statistical distributions masked to `None`.
4. With two or more cells suppressed, linear reconstruction via subtraction is mathematically thwarted.

---

## 3. Honest Disclosure of Prototype Privacy Limitations

Even with complementary suppression across engine-generated partitions, stateless prototype APIs cannot prevent arbitrary repeated adaptive queries from external callers.

Therefore, O6 v1.1.0 truthfully exposes:
```json
"privacy_safeguards": {
  "minimum_cohort_size": 5,
  "privacy_protection_level": "PROTOTYPE_PARTITION_SUPPRESSION",
  "cross_query_differencing_protection": "PARTIAL",
  "privacy_limitations": [
    "Arbitrary adaptive query-history reconstruction is not fully prevented in this prototype.",
    "Production deployment with sensitive real-world data would require stronger disclosure controls such as query-history enforcement and/or formally calibrated privacy mechanisms."
  ],
  "differencing_warning": "Protection applies to engine-generated partition outputs. Arbitrary repeated/adaptive cross-query differencing is not fully prevented in this prototype.",
  "differential_privacy_claimed": false
}
```
