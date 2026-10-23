# Stage 12C Readiness Dossier: Targeted M4 Remediation Handover

**Target Module**: M4 Personalised Reskilling Pathway Engine v1.0.0  
**Current Milestone**: Stage 12B Independent Methodology Review Completed  
**Next Milestone**: Stage 12C Targeted M4 Remediation  
**Date**: 2026-10-23  
**Review Verdict**: **`TARGETED M4 REMEDIATION REQUIRED`**  
**Readiness Verdict**: **`READY FOR TARGETED M4 REMEDIATION (STAGE 12C)`**

---

## 1. Executive Summary & Review Verdict

Stage 12B independent methodology review has concluded. The core foundational architecture of M4 v1.0.0 is validated:
* **Prerequisite DAG**: 15 relations grounded in authoritative standards, 0 cycles (`PASS_ACYCLIC`).
* **Demographic Fairness**: Protected attributes stripped at entry, $\text{DIR} = 1.000$, 100% counterfactual invariance.
* **Cost Accessibility**: 100% verified zero-cost content access for all 8 benchmark transition pathways.
* **Upstream Invariance**: M1, M2 v1.1.1, M6 v1.1.0, and M3 v1.1.0 remain strictly read-only.

However, the independent audit identified **1 P1 defect**, **3 P2 defects**, and **2 P3 defects** that must be resolved in Stage 12C before final freeze and integration into M5 and the UI.

### Defect Ledger
* **P0**: `0`
* **P1**: `1`
* **P2**: `3`
* **P3**: `2`

---

## 2. Stage 12C Actionable Remediation Backlog

The remediation team for Stage 12C must implement the following bounded, targeted improvements:

### Item 1: Dynamic Pathway Evidence Confidence Calculation (P1 — Check 42)
* **Defect**: `_calculate_pathway_confidence()` in `src/reskilling_pathway_engine.py` statically hardcodes mock component values (95, 92, 96, 95), resulting in a constant 94.5 HIGH score across all 8 benchmark pathways.
* **Remediation Task**:
  * Replace static component assignments with dynamic pathway aggregation:
    * $S_{\text{res}}$: Mean of primary resources' `skill_alignment` and `provider_reliability` ($\times 100$).
    * $S_{\text{prereq}}$: Mean of active prerequisite relations' `mapping_confidence` ($\times 100$).
    * $S_{\text{gap}}$: Scaled to proportion of CORE vs SUPPORTING requirements ($90.0 + 10.0 \times \frac{N_{\text{core}}}{N}$).
    * $S_{\text{fresh}}$: Days elapsed since verification.
  * Recompute benchmark confidence scores to demonstrate dynamic spread across pathways.

### Item 2: Provider Diversity Normalization (P2 — Check 20)
* **Defect**: Catalog documents 29 raw provider labels without institutional parent normalization (e.g. DeepLearning.AI in 5 labels, OpenLearn in 2 labels).
* **Remediation Task**:
  * Add `parent_institution` field to `data/reskilling/learning_resources_v1.json`.
  * Update documentation to report both raw platform count (29) and normalized parent institution count (21).

### Item 3: Synthetic Test Fixture Tagging (P2 — Checks 8, 13, 15)
* **Defect**: `RES_LOWCOST_01` (RM99) and `RES_VAR_01` (UNKNOWN) are synthetic edge-case test fixtures with proxy URLs.
* **Remediation Task**:
  * Add `"fixture_type": "BENCHMARK_SYNTHETIC_TEST_FIXTURE"` to these two records in `learning_resources_v1.json`.
  * Document their role as pricing edge-case test fixtures in `artifacts/m4_learning_resource_provenance.md`.

### Item 4: Deficit-Effort Scaling Floor Rationale (P2 — Check 23)
* **Defect**: Multiplier floor $M_{\text{eff}} \ge 0.50$ needs explicit pedagogical rationale for why marginal deficits incur $>50\%$ baseline hours.
* **Remediation Task**:
  * Update `artifacts/m4_learning_time_methodology.md` to document the fixed adult learning overhead: environment configuration, mandatory unit assessments, and capstone project evaluation.

### Item 5: Low-Cost Threshold Operational Disclaimer (P3 — Check 14)
* **Defect**: RM150 threshold lacks explicit operational product policy disclaimer.
* **Remediation Task**:
  * Insert required disclaimer verbatim into `artifacts/m4_cost_accessibility_audit.md` and engine docstrings:
    > *"For this prototype, LOW_COST is operationally defined as verified direct resource price <= RM150; it is not asserted as universally affordable."*

### Item 6: Weekly Study Assumption Labeling in Benchmarks (P3 — Check 27)
* **Defect**: Benchmark outputs in `m4_benchmark_results_v1.json` report `schedule_weeks` without indicating it assumes 10h/week.
* **Remediation Task**:
  * Rename field or add metadata: `"schedule_weeks_at_10h_per_week (TEST ASSUMPTION)"`.
  * Update documentation tables accordingly.

---

## 3. Strict Boundary Invariants for Stage 12C

The remediation engineer must adhere strictly to the following scope boundaries:
1. **Do NOT rebuild M4 from scratch**: Targeted fixes only.
2. **Do NOT modify upstream frozen systems**: M1, M2 v1.1.1, M6 v1.1.0, and M3 v1.1.0 must remain bitwise identical.
3. **Do NOT build M5 (SDG Impact Engine)**: Reserved for Stage 13.
4. **Do NOT build UI**: Reserved for later stages.
5. **Do NOT use RunPod or Argon**: Run all remediation scripts and tests locally.

---

## 4. Handover Sign-Off

All 10 required Stage 12B review reports have been generated and committed to `artifacts/`. Stage 12B formally concludes with:
**`TARGETED M4 REMEDIATION REQUIRED`**.
