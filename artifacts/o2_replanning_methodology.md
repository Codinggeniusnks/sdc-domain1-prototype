# O2 Automatic Replanning & Change Detection Engine Methodology — v1.0.0

## 1. Executive Summary & Architectural Role
The **O2 Automatic Replanning & Change Detection Engine** serves as the central orchestration, temporal diffing, and change-control layer of the SDC Domain 1 platform. Its primary mandate is to deterministically detect when shifts in upstream labor-market trends (M2), macroeconomic foresight scenarios (M6), learner verified skill profiles, or enterprise workforce cohorts require recalculation of downstream recommendations across M3, M4, O6, and O1.

### 1.1 Critical Boundary Principle
O2 is strictly an **orchestration and change-detection layer**. It does **NOT** own, redefine, or modify the underlying methodologies, scoring algorithms, or taxonomies of:
- **M1**: Skills Extraction Engine
- **M2**: Trend Intelligence Engine (Frozen: `v1.1.1`)
- **M6**: Scenario Engine (Frozen: `v1.1.0`)
- **M3**: Future-Role Matching Engine (Frozen: `v1.1.0`)
- **M4**: Personalised Reskilling Pathways (Frozen: `v1.1.0`)
- **M5**: SDG Impact Mapping Engine (Frozen: `v1.1.0`)
- **O6**: SDG Aggregation Engine (Frozen: `v1.1.0`)
- **O1**: Employer Workforce Gap Engine (Frozen: `v1.1.0`)

O2 treats all upstream engines as immutable, frozen black-box oracles, observing inputs and outputs over time to detect meaningful variance.

## 2. Core Operating Principle: Automatic ≠ Silent Mutation
In automated decision-support systems, a severe failure mode is the silent background mutation of user-accepted plans when external data drifts. O2 enforces an absolute architectural invariant:
- **Automatic Detection**: O2 automatically monitors state fingerprints, detects input variance, calculates dependency plans, and computes candidate outputs.
- **Candidate Separation**: All recomputed results are tagged as `AUTO_RECOMPUTED_CANDIDATE` with `publication_status = "CANDIDATE_REQUIRES_ACKNOWLEDGEMENT"` for any material change.
- **No Silent Overwrite**: The currently accepted learner pathway and employer workforce plan (`CURRENT_ACCEPTED`) are preserved immutably. Adoption requires explicit human acknowledgement or deliberate downstream publication action.

## 3. End-to-End Orchestration Lifecycle
The O2 execution pipeline follows an eight-stage deterministic workflow:

```
[1. Event Ingestion & Validation]
       |  (Validates idempotency, sequence ordering, and upstream versions)
       v
[2. State Snapshot & Fingerprinting]
       |  (Computes deterministic SHA-256 state fingerprint over semantic fields)
       v
[3. Change Detection & Attribution]
       |  (Compares previous vs new state fingerprint; extracts changed dimensions)
       v
[4. Dependency Recomputation Plan]
       |  (Builds affected modules list; avoids unnecessary module re-runs)
       v
[5. Candidate Output Generation]
       |  (Executes candidate runs for affected downstream modules)
       v
[6. Multi-Module Structured Diffs]
       |  (Diffs M3 roles, M4 pathways, O6 alignment, and O1 workforce priority)
       v
[7. Materiality Classification]
       |  (Applies deterministic hierarchy: HIGH_MATERIALITY > MATERIAL > MINOR > NONE)
       v
[8. Audit Ledger & Package Emission]
          (Emits candidate replan package with changeset hash and rollback link)
```

## 4. Operational Boundaries & Stage 16A Scope
- **No Background Daemons**: O2 runs as a pure, deterministic local library. No cron jobs, background threads, filesystem pollers, or web crawlers are implemented.
- **No Live Ingestion**: Live scraping and unverified data feeds are forbidden. All trend changes are evaluated using controlled, versioned synthetic snapshots.
- **Deterministic Explanations**: All change explanations use fixed rule templates; no generative LLM hallucinated causality is permitted.
