# O2 Human Acknowledgement & Candidate Separation Contract — v1.0.0

## 1. Executive Summary
The O2 replanning architecture decouples **candidate plan generation** from **plan adoption**. Automated background algorithms are permitted to calculate and suggest replanned recommendations, but they are strictly barred from silently overwriting user-accepted plans.

## 2. State Acceptance Lifecycle

```
[CURRENT_ACCEPTED] (Immutable state currently guiding user/employer)
       |
       |  (State change detected: M2, M6, Profile, or Cohort)
       v
[AUTO_RECOMPUTED_CANDIDATE] (Isolated candidate package generated)
       |
       |---> Materiality = NONE or MINOR  --> Adopted / Logged as CURRENT_ACCEPTED
       |
       |---> Materiality = MATERIAL or HIGH_MATERIALITY
                   |
                   v
       [CANDIDATE_REQUIRES_ACKNOWLEDGEMENT]
             /                   \
            /                     \
           v                       v
   [ACCEPTED_REPLAN]       [REJECTED_REPLAN]
 (Promoted to new        (Archived in ledger;
  CURRENT_ACCEPTED)       CURRENT_ACCEPTED preserved)
```

## 3. Rollback & State Preservation Invariants
1. **Previous State Preservation**: Whenever a candidate replan package is emitted, O2 retains the exact `state_id` of the previous accepted state in `rollback_reference`.
2. **Rejection Safety**: If a learner or HR manager rejects a candidate replan, O2 immediately reverts all UI views to the `rollback_reference` state without data corruption or loss of historical progress.
3. **Audit Immutability**: Both the candidate package and the rejection decision are logged immutably in the audit ledger for governance compliance.
