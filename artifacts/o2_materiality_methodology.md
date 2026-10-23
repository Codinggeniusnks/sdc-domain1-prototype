# O2 Materiality Classification Methodology — v1.0.0

## 1. Core Philosophy: Structural Dominance over Numeric Fluctuation
A critical challenge in automated replanning is distinguishing between **benign numerical score drift** (e.g., Match Index moving from 82.5 to 83.1) and **structural career/workforce disruption** (e.g., top recommended target role changing, or a new mandatory skill gap emerging).

O2 codifies the **Structural Dominance Principle**:
> *A structural modification to recommendations, mandatory learning requirements, or privacy status always strictly outranks numeric score shifts, regardless of score magnitude.*

## 2. Four-Tier Materiality Hierarchy

```
[HIGH_MATERIALITY]  --> Structural disruption: Top role change, CORE gap added/removed, required step changed
         |
[MATERIAL]          --> Significant secondary shift: Top-3 rank change, IMPORTANT gap change, pathway reordering
         |
[MINOR]             --> Numeric movement only: Match index drift, ECI movement, minor hours shift (<40h)
         |
[NONE]              --> Semantically identical recommendations across all dimensions
```

### 2.1 Tier Definitions and Triggers

| Materiality Level | Operational Definition | Exact Triggers | Publication Action Required |
|---|---|---|---|
| **`HIGH_MATERIALITY`** | Fundamental shift in primary recommendation or mandatory learning requirements. | - Top recommended target role changes (`top_recommended_role_changed == True`)<br>- CORE skill gap added (`core_gaps_added > 0`)<br>- CORE skill gap resolved/removed (`core_gaps_removed > 0`)<br>- Required pathway step added/removed (`required_steps_added/removed > 0`)<br>- Cohort privacy threshold breached ($k < 5$) | `CANDIDATE_REQUIRES_ACKNOWLEDGEMENT`<br>Candidate plan held; human confirmation required before adoption. |
| **`MATERIAL`** | Meaningful secondary shift affecting elective choices, pathway sequence, or top workforce priorities. | - Top-3 role membership or relative ordering changes<br>- IMPORTANT skill gap set changes (`important_gaps_added/removed > 0`)<br>- Recommended pathway step order changes (`pathway_order_changed == True`)<br>- O1 top priority skill changes<br>- Learning hour band shifts by $\ge 40.0$ hours | `CANDIDATE_REQUIRES_ACKNOWLEDGEMENT`<br>Advisory notice presented to user/HR. |
| **`MINOR`** | Score movement with stable recommendations and invariant learning structures. | - Match Index drift with identical top-3 roles and identical gap sets<br>- Evidence Confidence Index (ECI) update<br>- Minor learning hours adjustment ($< 40.0$ hours)<br>- O1 priority score movement without top-skill displacement | `CURRENT_ACCEPTED`<br>Information updated in background; no replanning alert needed. |
| **`NONE`** | Semantically identical outputs across all evaluated dimensions. | - Identical state fingerprints or replicated snapshot execution with unchanged outputs | `CURRENT_ACCEPTED`<br>No action. |

## 3. Flapping Prevention & Hysteresis Margin
To prevent recommendation "flapping" where two closely matched roles repeatedly alternate as top recommendation due to minor quarterly noise:
- O2 enforces a product policy threshold: Match Index score shifts below the hysteresis margin ($0.02$) without structural justification are suppressed from triggering replan candidates.
- If two roles remain within $0.05$ Match Index of each other, O2 flags the candidate with `STABLE_TIE_BREAKING_ACTIVE` to inform the user of near-equivalent occupational paths.
