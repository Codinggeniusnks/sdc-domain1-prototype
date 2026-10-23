# M3 v1.0.0 vs M3 v1.1.0 Side-by-Side Comprehensive Comparison

**Milestone**: Stage 11C Targeted Remediation  
**Scope**: Complete Architectural, Algorithmic & Metric Comparison  
**Date**: 2026-10-23  

---

## 1. High-Level Summary Matrix

| Architectural Dimension | M3 v1.0.0 (Pre-Remediation) | M3 v1.1.0 (Post-Remediation) | Methodological Impact |
|:---|:---|:---|:---|
| **Version Identifier** | `1.0.0` | `1.1.0` | Clean semantic versioning; v1.0.0 preserved untouched. |
| **Confidence Architecture** | **Conflated**: `recommendation_confidence` derived directly from match score ($\ge 75 \implies \text{HIGH CONFIDENCE FIT}$). | **Decoupled**: Independent **Match Strength** (`STRONG CURRENT FIT`, etc.) and **Evidence Confidence Index** (0–100) / Label (`HIGH`, `MEDIUM`, `LOW`, `INSUFFICIENT`). | Eliminates semantic confusion; enables high match with low confidence and vice versa. |
| **Requirement Tier Derivation** | **Uncodified**: Ordinal tiers (`CORE`, `IMPORTANT`, `SUPPORTING`) declared without public derivation logic. | **Deterministic 3-Tier Rulebook**: Programmatic rules (`RULE_CORE_AUTHORITATIVE_ESSENTIAL`, etc.) with publisher de-duplication and invariant enforcement. | Fully auditable and reproducible; answers "Why is X core?". |
| **Zero-Overlap Score Handling** | **Hard Clamping**: Discontinuous ceiling ($\le 15.0$) creating an artificial **$21.2$-point step jump** ($15.0 \rightarrow 36.2$). | **Continuous Low-Fit Gating**: Smooth linear gating $G(S_{\text{fit}}) = \min(1.0, S_{\text{fit}} / 20.0)$ applied to M2 and M6 contextual signals. Max delta: **$11.7$ points**. | Restores mathematical continuity; zero score cliffs. |
| **Guardrail Reordering** | **Discrete Bubble Swap**: Post-sort reordering when $\Delta \text{fit} > 20.0\%$, introducing step instability around 19.9% vs 20.1%. | **Continuous Scoring**: Eliminated post-sort bubble swaps; skill primacy enforced mathematically by weights and gating. | Eliminates rank instability around threshold boundaries. |
| **Weight Sensitivity Flag** | **Over-Permissive**: Naive $\Delta \text{rank} \ge 2$ flagged **18 of 20 roles (90.0%)**. | **Recalibrated**: Requires Top-3 membership flip OR absolute rank displacement $\ge 4$. Flagged roles reduced to **7 of 20 (35.0%)**. | Restores utility of warnings; flags genuine decision pivots. |
| **Protected Demographic Fields** | **Brittle Exception**: Raised raw `ValueError`, crashing user sessions upon CV import. | **Resilient Stripping**: Programmatically strips forbidden keys, logs `PROTECTED_ATTRIBUTE_STRIPPED` warning, preserves 100% invariance. | Enterprise UX resilience; zero demographic leakage. |
| **Empty Profile Handling** | **Arbitrary Scores**: Ranked occupations based on unattenuated macro M2/M6 context alone. | **Explicit Insufficient State**: Returns `status = "INSUFFICIENT_PROFILE_DATA"`, `role_matches = []`, and guidance message. | Prevents ungrounded career recommendations. |
| **Tie-Breaking Precedence** | Undocumented default. | **Strictly Documented & Enforced**: `(role_match_index DESC, current_skill_fit DESC, masco_code ASC)`. | 100% deterministic ranking across all platforms. |
| **Payload Core Counts** | Implicit in nested gap lists. | **Explicit Top-Level Fields**: `missing_core_count`, `matched_core_count`, `core_requirements_count`, `core_coverage_pct`. | Direct consumption contract for M4 and UI. |
| **Automated Unit Tests** | 22 tests (100% passing) | **28 tests (100% passing)** | Complete regression and defect verification. |

---

## 2. Empirical Benchmark Comparison Across 8 Synthetic Personas

| Benchmark Metric | M3 v1.0.0 | M3 v1.1.0 | Evaluation |
|:---|:---:|:---:|:---|
| **Top-1 Weight Stability** | 75.0% | **75.0%** | Preserved exact primary stability |
| **Average Top-3 Overlap (Jaccard)** | 0.917 | **0.919** | +0.2% consistency improvement |
| **Average Top-5 Overlap (Jaccard)** | 0.942 | **0.958** | +1.6% consistency improvement |
| **Spearman Rank Correlation** | 0.988 | **0.991** | +0.3% correlation improvement |
| **Weight-Sensitive Roles Count** | 18 / 20 (90%) | **7 / 20 (35%)** | Recalibrated to meaningful subset |
| **Requirement Sensitivity Top-1 Stability** | Unreported | **100.0%** | Robust to borderline tier adjustments |
| **Requirement Sensitivity Top-3 Overlap** | Unreported | **1.000** | Perfect podium preservation |
| **Average Scoring Latency (p99)** | 8.2 ms | **7.9 ms** | High-performance execution |

---

## 3. Cryptographic Artifact Provenance & Hashes

| Artifact File | M3 v1.0.0 SHA-256 | M3 v1.1.0 SHA-256 |
|:---|:---:|:---:|
| **Scoring Config** | `8b0a9cb48fae...` | `a80479cb97424ea45f8cb4dd70b5514f77c5ba8f711ceecf15bda74e17ae924c` |
| **Role Requirements** | `e1d4b68e990c...` | `18260b45d2f627ba76a4df15a81ca04df71e3db4aee17bf9ffb269be4323aa24` |
| **Synthetic Personas** | `5095b8e8b0e6...` | `e99f4ffc040d3a5a40bb7f975d4cb05ef9c0496159da8133379cb99a0eec2605` |
| **Benchmark Results** | `4df301cb290e...` | `43224097f4c7bb5e5ebfc9659b92dd0bf1b41baea684d092ca86d4e73f47cbe6` |
| **Build Manifest** | `087e303d1a8a...` | `15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c` |
