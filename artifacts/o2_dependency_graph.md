# O2 Dependency Graph & Recomputation Architecture — v1.0.0

## 1. Overview
O2 maintains an explicit, deterministic Directed Acyclic Graph (DAG) governing how upstream input shifts cascade across downstream recommendations. This prevents arbitrary recomputations, guarantees execution order, and optimizes computational efficiency.

## 2. Dependency Cascade Rules

```
                       [Event Sources]
                       /      |      \
                     /        |        \
                    v         v         v
               [M2 Trends] [M6 Scenario] [Profile Skills] [Cohort Snapshot]
                    \         |         /                   |
                     \        |        /                    |
                      v       v       v                     |
                         [M3 Matching]                      |
                              |                             |
                              v                             |
                         [M4 Pathway]                       |
                              |                             |
                              v                             v
                        [O6 Aggregation] <------------------+
                              |                             |
                              v                             v
                        [O1 Workforce] <--------------------+
```

### 2.1 Event-to-Module Mapping Table

| Triggering Event | Changed Dimension | Affected Modules | Recomputation Order | Optimization / Pruning Rule |
|---|---|---|---|---|
| `M2_TREND_SNAPSHOT_UPDATED` | Occupational shortage / momentum | M3, M4, O6, O1 | M3 → M4 → O6 → O1 | M5 taxonomy and M6 scenario assumptions remain unmutated. |
| `M6_SCENARIO_CHANGED` | AI foresight macro scenario | M3, M4, O6, O1 | M3 → M4 → O6 → O1 | M6 assumptions are not modified; outputs recomputed under new scenario context. |
| `PROFILE_SKILL_STATE_UPDATED` | Learner verified skill set | M3, M4, O6, O1 | M3 → M4 → O6 → O1 | M1 is not retrained. Only affected learner's M3/M4 recalculated. |
| `COHORT_SNAPSHOT_UPDATED` | Enterprise employee roster | O6, O1 | O6 → O1 | **Avoids Unnecessary Recomputation**: Skips individual M3/M4 for unchanged profiles. |
| `MANUAL_REPLAN_REQUESTED` | Explicit re-evaluation | None / All | Conditional | If state fingerprints match, recomputation is completely bypassed (`NO_SEMANTIC_CHANGE`). |

## 3. Unnecessary Recomputation Pruning Proof
In enterprise settings, workforce rosters change frequently (e.g. employee onboarding/offboarding). If an organization updates its cohort from 50 to 51 profiles by adding 1 new employee:
- **Naive Architecture**: Recomputes M3 and M4 for all 51 employees (102 expensive model executions).
- **O2 Pruned Architecture**: Identifies that only cohort composition changed (`COHORT_SNAPSHOT_UPDATED`). Recomputes aggregate modules O6 and O1 directly from existing profile vectors. M3 and M4 are run only for the 1 new employee, saving over 98% of redundant compute while guaranteeing bit-exact aggregate alignment.
