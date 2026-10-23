# Regional Representativeness & Data Classification (v1.1.0)

**Defect Addressed:** DEF-P3-02  
**Status:** IMPLEMENTED & RUNTIME EMBEDDED

---

## 1. Migration from Narrative to Runtime Metadata

In O6 v1.0.0, the regional non-representativeness disclaimer was documented only in markdown artifacts. In O6 v1.1.0, this disclaimer is embedded directly into runtime API responses.

---

## 2. Embedded Fields in All Aggregation Payloads

Every response returned by `aggregate_cohort_alignment()` and `aggregate_region_alignment()` includes:
```json
{
  "representativeness_disclaimer": "Synthetic demonstration cohort; not statistically representative of the Malaysian national or regional workforce.",
  "data_source_class": "SYNTHETIC_DEMO"
}
```

Synthetic regional identifiers (`REGION_A`, `REGION_B`, `REGION_C`) are strictly preserved, preventing any false equivalence with official Department of Statistics Malaysia (DOSM) state-level labor statistics.
