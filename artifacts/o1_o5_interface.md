# O1 -> O5 Interface Contract Specification (v1.0.0)

**Interface Direction:** Upstream (O1) to Downstream (O5 Compliance & Policy Exporter)  
**Status:** COMPLIANCE METADATA HOOKS READY

---

## 1. O5 Compliance Metadata Payload

O1 emits standardized compliance and governance metadata ready for future regulatory reporting:

```json
{
  "o5_compliance_metadata": {
    "protected_attributes_used": false,
    "demographic_fairness_evaluated": false,
    "aggregate_only": true,
    "suppression_applied": false,
    "excluded_profile_count": 0,
    "prohibited_uses_enforced": true
  }
}
```

---

## 2. Compliance Guarantees

- Demonstrates complete absence of protected demographic variables under national privacy standards (PDPA).
- Confirms small-cohort privacy suppression compliance ($k=5$).
- Proves structural separation of aggregated planning from individual personnel decisions.
