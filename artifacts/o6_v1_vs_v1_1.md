# Comparison: O6 Engine v1.0.0 vs v1.1.0

**Review Date:** 2026-10-24  
**Audit Dimension:** Forensic Version Comparison

---

| Dimension | O6 v1.0.0 (Stage 14A) | O6 v1.1.0 (Stage 14C) | Impact & Rationale |
|---|---|---|---|
| **Input Profile Validation** | No validation; iterated raw list | Deterministic `validate_profile_for_aggregation()` layer | Rejects non-dicts, empty dicts, incomplete records. Prevents unhandled crashes and data corruption. |
| **Denominator Contract** | Unfiltered raw count entered denominator | Strictly uses `eligible_profile_count` | Guarantees prevalence ratios are mathematically sound and not diluted by empty records. |
| **Handling of `confirmed_skills=None`** | Unhandled `TypeError` | Safe defaulting via `list(p.get(...) or [])` | Hardens system against malformed upstream payloads. |
| **Fairness Language** | Claimed empirical `DIR ≡ 1.000` | Structural Protected-Attribute Non-Use | Removes misleading empirical parity claim; truthfully documents demographic exclusion. |
| **Differencing Attack Protection** | Single-cohort suppression only ($k=5$) | Partition-aware complementary suppression ($N=10 = 6+4$ protected) | Prevents subtraction recovery across engine partition breakdowns. |
| **Privacy Limitation Transparency** | Unstated cross-query limitations | Truthful `PARTIAL` rating and documented limitations | No fake Differential Privacy; transparent risk boundaries. |
| **Mapping-Type Counting Unit** | Sum of raw mapping instances | Unique Profile–Target–Mapping_Type Relation $(i, t, \tau)$ | Eliminates duplicate multi-skill inflation; reconciles code with specification. |
| **Pathway Alignment Coverage** | Basic count ratio | Includes `PLANNED_CURRICULUM_SKILL_STEPS` scope & disclaimers | Clarifies metric represents planned reskilling, not verified educational attainment. |
| **Regional Representativeness** | Documentation only | Embedded in runtime JSON payloads | Guarantees downstream consumers receive synthetic demo disclaimers. |
| **Test Suite Coverage** | 22 tests | 37 tests (15 new targeted remediation tests) | 100% automated coverage of all remediated edge cases. |
| **Benchmark Suite** | 8 benchmarks | 13 benchmarks (BM01–BM13) | Formally validates all 6 defect resolutions. |
