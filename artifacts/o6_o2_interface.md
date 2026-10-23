# O6 to O2 Interface Specification: Replanning & State Refresh

**Interface Identifier**: INTERFACE-O6-O2-v1.0.0  
**Upstream System**: O6 SDG Contribution Aggregation Engine v1.0.0  
**Downstream Target**: O2 Automatic Replanning & Continuous Refresh Engine (Future Stage)  
**Author**: Enterprise Workforce Intelligence Architect, Foresight Systems Methodologist  
**Status**: SPECIFIED & RATIFIED (STAGE 14A)  

---

## 1. Purpose & Scope Boundary

Module **O2: Automatic Replanning & Refresh** will provide background monitoring capabilities that detect changes in:
- Upstream labor market signals (M2 trend score shifts)
- Macroeconomic scenario transformations (M6 scenario updates)
- Curated course availability or pricing (M4 catalog adjustments)
- Employee skill acquisitions or role transfers

When changes occur, O2 will trigger targeted re-planning and refresh aggregated workforce analytics.

In Stage 14A, **no background daemon, automated file watcher, or live refresh engine is implemented**.  
Instead, this document defines the cryptographic state metadata and version identifiers that O6 attaches to every aggregation output via `o2_interface_hook`. This allows future O2 to perform deterministic change detection without inspecting underlying data payloads.

```
+------------------------------------+
|  O6 SDG Aggregation Engine v1.0.0  |
|  - Cryptographic Input Hash        |
|  - Dependency Version Tracking     |
|  - Temporal State Snapshot         |
+-----------------+------------------+
                  |
                  | (o2_interface_hook JSON Schema)
                  v
+------------------------------------+
|  O2 Automatic Refresh (Future)     |
|  - Deterministic State Comparison  |
|  - Triggered Re-Aggregation        |
+------------------------------------+
```

---

## 2. Schema Specification: `o2_interface_hook`

The `o2_interface_hook` block provides the exact cryptographic snapshot required for state reconciliation:

```json
{
  "o2_interface_hook": {
    "input_profiles_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "m5_version": "1.1.0",
    "m4_version": "1.1.0",
    "m3_version": "1.1.0",
    "m6_version": "1.1.0",
    "refresh_supported": true
  }
}
```

---

## 3. Change Detection Logic for Future O2

When O2 evaluates an existing O6 aggregation artifact against the live system state, it executes three sequential verification gates:

### Gate 1: Upstream Dependency Check
O2 verifies whether the versions of M3, M4, M5, or M6 have changed:
- If `current_m5_version != o2_hook.m5_version` (e.g. M5 upgraded from v1.1.0 to v1.2.0), O2 flags the aggregation as **STALE_TAXONOMY** and invalidates cached prevalence metrics.
- If `current_m6_version != o2_hook.m6_version`, O2 invalidates scenario capability comparisons.

### Gate 2: Input Population Check
O2 computes the SHA-256 digest of the sorted list of `profile_id` keys in the current workforce roster:
$$\text{LiveHash} = \text{SHA256}\left( \text{JSON}(\text{sorted}(\text{active\_profile\_ids})) \right)$$
- If $\text{LiveHash} \neq \text{o2\_hook.input\_profiles\_hash}$, O2 detects that workers have joined or departed the cohort, triggering a re-aggregation.

### Gate 3: Skill & Role State Reconciliation
If profile IDs match, O2 inspects whether confirmed skills or assigned roles have evolved:
- Individual profile modification timestamps are compared against the aggregation's `generated_at` timestamp.
- Any profile updated after `generated_at` triggers incremental re-computation.

---

## 4. Stability & Idempotency Guarantee

Because all six core engines (M1, M2, M6, M3, M4, M5) are formally frozen, re-running `aggregate_cohort_alignment()` on an identical input profile set is **100% idempotent and deterministic**:
- Output metrics, shares, and prevalence ratios reproduce byte-for-byte.
- Zero drift or stochastic variance occurs.
