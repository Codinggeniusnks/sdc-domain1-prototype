# O2 Privacy-Preserving Diff Contract — v1.0.0

## 1. Executive Summary & Threat Model
When workforce gap metrics are updated over time, publishing naive before-and-after differences can inadvertently leak confidential small-cell counts that were previously masked.

### 1.1 The Temporal Differencing Vulnerability
Suppose an employer cohort of 10 employees initially has 4 employees with an AI literacy gap (masked as `"<5"` under O1's $k=5$ privacy rule). In the next quarter, 1 additional employee develops the gap, bringing the count to 5.
- **Naive Diff Display**: `"<5" → 5 (+1)` or `4 → 5`.
- **Privacy Leak**: The employer immediately deduces that the prior count was exactly 4, completely compromising the historical $k=5$ small-cell protection!

## 2. O2 Privacy-Safe Diff Transformation Rules
To completely eliminate temporal differencing leakage, O2 implements four strict string transformation rules across all employer-facing outputs:

| Prior State ($t_0$) | New State ($t_1$) | Naive Display (FORBIDDEN) | O2 Certified Safe Diff Display | Privacy Protection Rationale |
|---|---|---|---|---|
| $< 5$ (e.g. 4) | $\ge 5$ (e.g. 5) | `4 → 5` or `<5 → 5` | `"Previously suppressed; now above reporting threshold."` | **Completely conceals prior exact small integer ($4$).** |
| $\ge 5$ (e.g. 5) | $< 5$ (e.g. 4) | `5 → 4` or `5 → <5` | `"Previously reportable; now below reporting threshold."` | **Completely conceals new exact small integer ($4$).** |
| $< 5$ (e.g. 2) | $< 5$ (e.g. 3) | `2 → 3` or `Δ+1` | `"SUPPRESSED → SUPPRESSED"` | **Maintains absolute suppression across small-number shifts.** |
| $\ge 5$ (e.g. 10) | $\ge 5$ (e.g. 14) | `10 → 14` | `10 → 14 (+4)` | Reportable standard delta; both values safely exceed threshold. |

## 3. Individual Identity & Surveillance Invariants
In accordance with Responsible AI principles and Malaysian PDPA 2010:
1. **Zero Profile IDs**: Employer-facing O2 replan packages contain NO individual employee IDs, usernames, or employee email addresses.
2. **Zero Employee Rankings**: O2 strictly refuses to rank individual employees by reskilling difficulty, cost, replacement vulnerability, or adaptability.
3. **No Punitive Action Automation**: O2 replanning diffs include an immutable governance notice prohibiting the use of gap shift data for disciplinary, termination, or compensation decisions.
