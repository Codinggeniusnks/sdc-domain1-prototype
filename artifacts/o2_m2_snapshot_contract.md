# O2 M2 Snapshot Consumption Contract — v1.0.0

## 1. Executive Summary
To evaluate O2's responsiveness to labor-market evidence updates without mutating or querying unapproved external feeds, Stage 16A utilizes **controlled synthetic M2 snapshots**. These snapshots conform strictly to the frozen M2 v1.1.1 output schema.

## 2. Controlled Snapshot Catalog

| Snapshot ID | Label | Purpose / Description | Expected Materiality Outcome |
|---|---|---|---|
| `M2_SNAP_BASELINE_2026Q1` | `SNAPSHOT_A_BASELINE` | Standard baseline labor-market trend evidence across 20 MASCO occupations. | Reference baseline |
| `M2_SNAP_MINOR_2026Q2` | `SNAPSHOT_B_MINOR_CHANGE` | Minor score fluctuation ($\pm 1.5$ points shortage) without rank shifts. | **`MINOR`** |
| `M2_SNAP_MATERIAL_2026Q3` | `SNAPSHOT_C_MATERIAL_TREND_CHANGE` | Major surge in AI Engineering (2529) causing top role re-ranking. | **`HIGH_MATERIALITY`** |
| `M2_SNAP_REPLICATED_2026Q1` | `SNAPSHOT_D_SEMANTICALLY_IDENTICAL` | Identical numbers to Baseline with different timestamp/ID. | **`NONE`** (`NO_SEMANTIC_CHANGE`) |
| `M2_SNAP_UNSUPPORTED_2027` | `SNAPSHOT_E_INVALID_VERSION` | Claims uncertified M2 version "2.0.0". | **`UNSUPPORTED_UPSTREAM_VERSION`** |

## 3. Provenance & Non-Fabrication Guarantee
All synthetic M2 snapshots are explicitly tagged with `data_source_class = "SYNTHETIC_CHANGE_FIXTURE"`. They are intended solely for orchestration benchmarking and must never be cited as real empirical labor-market observations.
