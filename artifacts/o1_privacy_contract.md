# O1 Privacy & Data Protection Contract (v1.0.0)

**Contract Scope:** Privacy Preservation, Suppression Policy, and Differencing Limits  
**Classification:** PROTOTYPE PARTITION SUPPRESSION (PARTIAL)

---

## 1. Privacy Safeguards

1. **$k$-Anonymity Floor ($k=5$):**
   Any cohort, department, regional slice, or role family with $N_{\text{eligible}} < 5$ is completely suppressed from statistical reporting.
2. **Small-Cell Distribution Masking:**
   When a cell is suppressed:
   - `gap_prevalence` $\implies$ `None`
   - `core_gap_prevalence` $\implies$ `None`
   - `priority_index` $\implies$ `None`
   - `quality_flags` $\implies$ includes `"SUPPRESSED_SMALL_CELL"`
3. **Small-Cell Exact Count Masking:**
   In O1 payloads, suppressed cells surface `eligible_count_display: "<5"` rather than raw integers, eliminating single-worker count disclosure.
4. **Partition-Aware Complementary Suppression:**
   When a workforce is partitioned (e.g. into departments or roles), if any single cell is suppressed for small size ($0 < N < 5$), the next smallest sibling cell is complementarily suppressed to prevent algebraic subtraction recovery from the parent total.

---

## 2. Realistic Differencing Rating: `PARTIAL`

- **Rating:** `cross_query_differencing_protection = "PARTIAL"`
- **Truthful Boundary Statement:**
  O1 enforces static small-cell suppression and partition-aware complementary suppression. However, because the system does not maintain a stateful cross-query reconstruction ledger across arbitrary ad-hoc queries, it does NOT provide complete tracker reconstruction resistance or $(\epsilon, \delta)$-Differential Privacy.
- **Prohibited Overclaims:**
  - Zero claims of Differential Privacy.
  - Zero claims of complete anonymity under arbitrary interactive queries.
