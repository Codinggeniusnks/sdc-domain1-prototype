# O1 -> O2 Interface Contract Specification (v1.0.0)

**Interface Direction:** Upstream (O1) to Downstream (O2 Automatic Replanning Engine)  
**Status:** STATE FINGERPRINT HOOKS READY

---

## 1. O2 State Fingerprint Payload

To enable future O2 monitoring and automatic workforce replanning without running daemon polling loops, every O1 execution emits structured state fingerprints:

```json
{
  "o2_state_fingerprint": {
    "m2_version": "1.1.1",
    "m6_scenario": "REFERENCE_2026",
    "m4_pathway_version": "1.1.0",
    "cohort_snapshot_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "analysis_config_hash": "4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b"
  }
}
```

---

## 2. Future O2 Replanning Triggers Supported

1. **Cohort Drift:** `cohort_snapshot_hash` changes when new employees join, leave, or complete reskilling steps.
2. **Macro Trend Update:** `m2_version` changes upon scheduled labor market data ingestion.
3. **Scenario Shift:** `m6_scenario` changes when an organization alters its forward-looking planning horizon.
4. **Policy Adjustment:** `analysis_config_hash` changes when priority weights are retuned.
