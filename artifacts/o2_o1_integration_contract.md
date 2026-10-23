# O2 — O1 Workforce Gap Engine Integration Contract — v1.0.0

## 1. Executive Summary
O2 interfaces directly with `O1 Employer / HR Workforce Gap & Cohort Reskilling Engine v1.1.0` to detect macro organizational skill shifts, identify newly emergent skill gaps across cohorts, and trigger cohort roadmap replanning.

## 2. State Fingerprint Consumption & Delta Tracking
O1 emits a deterministic aggregate state fingerprint for every cohort evaluation. O2 compares sequential cohort fingerprints:
- If the cohort fingerprint is unchanged, O2 returns `NO_SEMANTIC_CHANGE` and skips workforce replanning.
- If the cohort composition or gap matrix shifts by $\ge 10\%$, O2 flags `WORKFORCE_PRIORITY_CHANGED` and triggers candidate cohort roadmap recomputation.

## 3. Interface Methods
- `o1_interface_hook`: O1 exposes `get_state_fingerprint(cohort_id, scenario)` and `detect_gap_shifts(prev, curr)`.
- `build_privacy_safe_diff`: O2 sanitizes all O1 before-and-after tables using $k=5$ masking and complementary suppression.
- `governance_notice`: O2 binds O1's mandatory Responsible AI disclaimer to all employer diff payloads.
