# O1 Downstream Integration Contracts — v1.1.0

## 1. Executive Summary
This document formalizes the downstream interface contracts between `O1 Workforce Gap Engine v1.1.0` and downstream consumer modules: **O2 Continuous Trend & Monitoring Engine**, **O5 Governance & Compliance Engine**, and the **Employer Dashboard UI**.

## 2. O2 Monitoring Engine Contract (`o1_o2_interface`)
- **Integration Role**: O2 consumes O1 cohort gap vectors to track structural workforce skill shifts over time across macroeconomic scenarios.
- **Contract Interface**:
  - `get_state_fingerprint(cohort_id, scenario)`: Emits a deterministic SHA-256 state fingerprint of the aggregated gap matrix.
  - `detect_gap_shifts(previous_state, current_state, threshold=0.10)`: Identifies skill gaps whose cohort prevalence has shifted by $\ge 10\%$.
- **Readiness Verdict**: **READY FOR O2**.

## 3. O5 Governance & Compliance Engine Contract (`o1_o5_interface`)
- **Integration Role**: O5 audits aggregate privacy compliance, verifies hash chains, and ensures regulatory adherence to Malaysian PDPA and ESG reporting standards.
- **Contract Interface**:
  - `verify_privacy_invariants(payload)`: Programmatically confirms that all cells with count $< 5$ are masked and complementary suppression rules hold.
  - `export_audit_ledger_entry(run_id)`: Generates a cryptographically signed audit trail entry linking input profile batch hashes to output report hashes.
- **Readiness Verdict**: **READY FOR O5**.

## 4. Employer Dashboard UI Contract
- **Integration Role**: Powers visual heatmaps, cohort roadmap charts, and strategic skills gap tables.
- **Contract Interface**:
  - `build_heatmap_payload(profiles, min_cell_threshold=5)`: Returns a structured JSON containing role-by-skill cells with explicit `suppressed: true` flags for cells $< 5$.
  - `build_executive_summary_payload(profiles)`: Emits macro summary KPIs with safe counts and disclaimer text.
- **Readiness Verdict**: **READY FOR EMPLOYER UI**.
