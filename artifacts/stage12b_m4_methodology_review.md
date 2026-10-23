# Stage 12B Independent Methodology Review: M4 Personalised Reskilling Pathway Engine v1.0.0

**Module**: M4 Personalised Reskilling Pathway Engine v1.0.0  
**Audit Role**: Independent Senior Learning-Pathway Methodologist, Education-Resource Auditor, Workforce-Reskilling Researcher & Reproducibility Engineer  
**Date**: 2026-10-23  
**Audited Artifacts**:
* `src/reskilling_pathway_engine.py` (SHA-256: `986e4f657e9eb302ff241e6d6bf28fab63f0384ad120b39f6d23a8faa9d7368f`)
* `data/reskilling/skill_prerequisites_v1.json` (SHA-256: `d78846dd7f445aa6950385c9189831439a33d0ae3fb86be6bf418928b7c70f6c`)
* `data/reskilling/learning_resources_v1.json` (SHA-256: `70735f76b547c2ca8ee9c182121c5c1ce1999491d86f51365e97b44e8262ef26`)
* `data/reskilling/m4_scoring_config_v1.json` (SHA-256: `1842f494f2b4c91b94c983a7f8891eb2b8bd5253e16774026be2d312664167c2`)
* `data/reskilling/m4_benchmark_results_v1.json` (SHA-256: `5c3eadb642adbff4a09100ce96d2bcd2c07a917187e0cebd67828331890a1350`)
* `data/reskilling/m4_build_manifest_v1.json` (SHA-256: `f3b3e793b29e1802e081311ba19b5dafa942f169515d5bb1ec26a582bfbeff1f`)

**Methodology Verdict**: **`REQUIRES REMEDIATION`**  
**Final Verdict**: **`TARGETED M4 REMEDIATION REQUIRED`**

---

## 1. Executive Summary & Defect Ledger

An exhaustive, forensic methodology review across all **56 audit checkpoints** was executed against M4 Personalised Reskilling Pathway Engine v1.0.0. The audit verified that M4's core architecture succeeds in several critical labor-market and recommender-system standards:
1. **Upstream Frozen Invariance**: Frozen modules M1 (`H_blend_0.70A_0.30C1_W1.0`), M2 (`v1.1.1`), M6 (`v1.1.0`), and M3 (`v1.1.0`) remain strictly read-only and unperturbed.
2. **Topological Feasibility**: Kahn's topological sort algorithm enforces an acyclic DAG (`PASS_ACYCLIC`) across all 15 prerequisite relations with guaranteed CORE-first sequencing.
3. **Demographic Fairness**: Protected attributes are stripped at ingestion, achieving zero disparate impact ($\text{DIR} = 1.000$) and 100% counterfactual invariance across all demographic perturbations.
4. **Democratized Accessibility**: 100% of benchmark transition pathways provide complete zero-cost instructional content access (`RM 0.00` direct content cost) under default `FREE_FIRST` mode.

However, the forensic audit identified **1 P1 defect**, **3 P2 defects**, and **2 P3 defects** requiring targeted remediation before final freeze and integration into M5 and the front-end UI.

### Defect Tally Summary
* **P0 (Catastrophic / Architectural Invalidation)**: **`0`**
* **P1 (Must Fix Before Freeze & User-Facing UI)**: **`1`**
* **P2 (Should Improve / Calibration & Normalization)**: **`3`**
* **P3 (Documentation & Operational Disclaimers)**: **`2`**

```
========================================================================================
DEFECT LEDGER: M4 RESKILLING PATHWAY ENGINE v1.0.0
========================================================================================
ID        Severity  Check     Component         Summary Description
----------------------------------------------------------------------------------------
M4-P1-01  P1        Audit 42  Confidence Engine Pathway Evidence Confidence is statically
                                                hardcoded (94.5 HIGH) across all pathways;
                                                lacks dynamic path-specific aggregation.
M4-P2-01  P2        Audit 20  Resource Catalog  Provider diversity overcounted (29 labels vs
                                                21 normalized institutional parent groups).
M4-P2-02  P2        Audit 8   Resource Catalog  RES_LOWCOST_01 & RES_VAR_01 are synthetic test
                                                fixtures with proxy URLs, not verified live
                                                commercial offerings.
M4-P2-03  P2        Audit 23  Time Estimation   Learning time multiplier floor (0.50) requires
                                                explicit pedagogical review/assessment rationale.
M4-P3-01  P3        Audit 14  Cost Policy       Low-cost threshold lacks explicit operational
                                                product policy disclaimer (<= RM150).
M4-P3-02  P3        Audit 27  Benchmarks        Benchmark schedule_weeks lacks explicit
                                                "TEST ASSUMPTION: 10h/week" labeling.
========================================================================================
```

---

## 2. Comprehensive 56-Check Audit Verification Matrix

| Check # | Audit Area | Description & Methodological Standard | Audit Result | Status |
|:---:|:---|:---|:---|:---:|
| **1** | M3 Gap Contract | Consumes missing CORE, IMPORTANT, SUPPORTING, deficit, and distance without altering M3 ranking. | M3 output consumed read-only; zero M3 score re-computation. | **VALID** |
| **2** | CORE-First Ordering | Unresolved CORE gaps prioritized before non-core unless prerequisite justifies inversion. | Kahn's algorithm sort key prioritizes `is_core` (`1` vs `0`). | **VALID** |
| **3** | Prerequisite Grounding | Audit all 15 relations for source, reason, and mapping confidence. | 15/15 relations grounded in authoritative frameworks. | **VALID** |
| **4** | REQUIRED Standard | REQUIRED used only when downstream skill cannot be learned without it. | 4/4 REQUIRED dependencies strictly justified; 0 unsupported. | **VALID** |
| **5** | Strength Distinction | REQUIRED vs RECOMMENDED/OPTIONAL deterministic operational meaning. | REQUIRED enforces DAG edges; others provide priority bonus. | **VALID** |
| **6** | Prerequisite Cycles | Recompute graph for circularity across all relations. | Verified acyclic; 0 cycles detected (`PASS_ACYCLIC`). | **VALID** |
| **7** | Graph Density | Graph density balanced; avoid artificial connectivity. | 5 roots (in-degree 0); max depth 2 hops; not artificially dense. | **VALID** |
| **8** | Live Resource Existence | Verify official pages resolve and match titles/providers. | 36 live verified; 2 synthetic fixtures (`RES_LOWCOST_01`, `RES_VAR_01`). | **NEEDS FIX (P2)** |
| **9** | Official URLs | Official provider domains used, avoiding affiliate/mirror links. | Verified official domains (Microsoft, freeCodeCamp, etc.). | **VALID** |
| **10** | FREE Status | Content accessible without paywall, credit card, or trial expiration. | 31 claimed FREE verified 100% free; 0 deceptive trials. | **VALID** |
| **11** | FREE_TO_AUDIT Status | Content auditable without fee; certificate cost segregated. | 5 claimed FREE_TO_AUDIT verified (Coursera/edX audit mode). | **VALID** |
| **12** | Certificate Decoupling | Free content access decoupled from optional paid certificates. | Explicit separation in data model; certs do not inflate min cost. | **VALID** |
| **13** | LOW_COST Resource | Verify official price, currency, taxes, and promotional status. | `RES_LOWCOST_01` (RM99) identified as synthetic benchmark fixture. | **NEEDS FIX (P2)** |
| **14** | Low-Cost Threshold | RM150 documented as operational policy, not objective affordability. | Wage link noted, but missing required explicit policy disclaimer. | **NEEDS FIX (P3)** |
| **15** | UNKNOWN Cost | Unknown cost resources never collapse to RM0. | Handled via `unknown_cost_items`; excluded from min cost. | **VALID** |
| **16** | Resource Language | Content verified in English beyond title-level inspection. | 38/38 verified English instructional materials. | **VALID** |
| **17** | Resource Level | BEGINNER / INTERMEDIATE / ADVANCED sourced from provider metadata. | 22 Beginner, 15 Intermediate, 1 Advanced accurately labeled. | **VALID** |
| **18** | Skill Alignment | Syllabus materially teaches assigned skill (HIGH / MED / LOW). | 36 primary resources rated HIGH alignment ($\ge 0.88$). | **VALID** |
| **19** | Catalog Overreach | No course duplication creating fake catalog coverage. | Zero duplicate courses; single courses not over-mapped. | **VALID** |
| **20** | Provider Diversity | Raw provider labels vs normalized institutional groups. | 29 raw labels collapse to 21 distinct institutional organizations. | **NEEDS FIX (P2)** |
| **21** | Resource Freshness | Verification timestamps reflect live audit dates. | All verified with `last_verified_date: 2026-10-23`. | **VALID** |
| **22** | Resource Independence | Removing primary resource does not remove skill from pathway. | Verified: absence of resource yields `primary_resource: null`. | **VALID** |
| **23** | Learning Time Formula | $M_{\text{eff}} = 0.50 + 0.50 \cdot \text{deficit}$ pedagogical defensibility. | Formula is continuous, but 0.50 floor needs explicit rationale. | **NEEDS FIX (P2)** |
| **24** | Time Estimate Source | Steps distinguish PROVIDER_STATED, SYSTEM_ESTIMATE, MIXED. | Metadata contract enforces transparent estimation type. | **VALID** |
| **25** | Effort Calibration | Base hour ranges plausible relative to skill complexity. | 4 tiers (5-15h, 15-30h, 30-60h, 60-120h) empirically sound. | **VALID** |
| **26** | Fake Precision | UI-facing estimates provide rounded integer ranges. | Hour bounds rounded to integers; no spurious decimals in UI. | **VALID** |
| **27** | Week Calculation | Weeks appear only when hours_per_week is explicitly supplied. | Requires input hours; benchmark omitted "TEST ASSUMPTION" label. | **NEEDS FIX (P3)** |
| **28** | Total Hours Range | Pathway total hours strictly equal sum of active step hours. | Verified: total hours low/high match component sums exactly. | **VALID** |
| **29** | Partial Skill Credit | Partial evidence reduces learning hours without erasing gap. | Deficit scaling reduces hours; user must explicitly confirm mastery. | **VALID** |
| **30** | Mastery Update | Marking skill USER_CONFIRMED removes step and re-orders. | Verified: confirmed skill eliminated, dependent DAG remains sound. | **VALID** |
| **31** | Scenario Influence | Scenario reorders grounded gaps; never manufactures new gaps. | Scenario bonus (+5 to +15) reorders existing gaps only. | **VALID** |
| **32** | Scenario Bonus Cap | Max scenario shift cannot override CORE requirement structure. | Kahn's algorithm preserves `is_core` priority over scenario bonus. | **VALID** |
| **33** | Transferability | Computed dynamically from catalog-wide role requirements. | Precomputed percentage across 20 MASCO role definitions. | **VALID** |
| **34** | Priority Formula | Linear composite of requirement, deficit, transferability, scenario. | Deterministic configuration weights; no hidden constants. | **VALID** |
| **35** | Effort Inversion | Easier skills do not crowd out critical difficult skills. | Requirement strength weighted 40%, deficit 25%; effort not overriding. | **VALID** |
| **36** | Topological Order | Step order respects 100% of REQUIRED prerequisite edges. | Kahn's algorithm strictly enforces in-degree == 0 before selection. | **VALID** |
| **37** | Resource Order Invariance | Changing catalog resource order does not change step sequence. | Step ordering depends on skill DAG; resource selection is downstream. | **VALID** |
| **38** | FREE_FIRST Policy | Verified free resources selected when alignment is comparable. | Cost rank 0/1 prioritized before paid options. | **VALID** |
| **39** | Free Pathway Claim | 100% benchmark pathways achieve RM0 direct content cost. | Verified: direct instructional tuition = RM0.00 across all 8. | **VALID** |
| **40** | Certification Claims | No claims that certificates equal competency or guaranteed jobs. | Strict decoupling; certs labeled as optional credentials. | **VALID** |
| **41** | Evidence Independence | Pathway confidence decoupled from M3 match score. | Pathway confidence evaluates data trustworthiness independently. | **VALID** |
| **42** | Benchmark Saturation | Verify spread of pathway confidence scores (not hardcoded). | **FAILED**: Constant 94.5 across all 8 pathways due to mock values. | **NEEDS FIX (P1)** |
| **43** | Confidence vs Hours | Low pathway confidence must not inflate learning hours. | Hours scaled strictly by deficit; confidence does not alter hours. | **VALID** |
| **44** | Demographic Stripping | Protected attributes stripped at entry with audit warnings. | Stripped 100% of demographic fields; warnings emitted. | **VALID** |
| **45** | Fairness Invariance | Identical pathways across demographic counterfactual variants. | $\text{DIR} = 1.000$; 100% bitwise invariance across 8 test personas. | **VALID** |
| **46** | Empty Gap Case | Zero skill gaps returns NO_RESKILLING_REQUIRED. | Verified: 0 gaps yields 0 steps and NO_RESKILLING_REQUIRED. | **VALID** |
| **47** | Non-Core Only Case | Only IMPORTANT/SUPPORTING gaps does not fabricate CORE gaps. | Verified: non-core gaps scheduled without inventing core steps. | **VALID** |
| **48** | Step Skipping | SKIPPED_BY_USER does not mark skill as mastered. | Status set to SKIPPED_BY_USER; mastery credit unchanged. | **VALID** |
| **49** | Resource Substitution | User rejection of resource allows alternative without priority change. | Engine provides primary and alternative from distinct providers. | **VALID** |
| **50** | Progress Status Lifecycle | NOT_STARTED, IN_PROGRESS, COMPLETED require user action. | Automated progress updates prohibited; explicit user action required. | **VALID** |
| **51** | M5 Interface Contract | Passes skills, role, priority, scenario context, source evidence. | Complete decoupled payload supplied; independent of provider choice. | **VALID** |
| **52** | No Employment Claims | No claims of guaranteed employment or career success probability. | Active documentation searched; zero employment guarantees found. | **VALID** |
| **53** | Upstream Immutability | Frozen M1, M2, M6, M3 hashes unchanged. | Upstream manifests verified byte-identical. | **VALID** |
| **54** | Deterministic Build | Deterministic logic separated from dynamic verification metadata. | Reproducible manifests track code and data SHA-256 hashes. | **VALID** |
| **55** | Resource Updateability | Catalog refreshable without modifying prerequisite DAG or M3. | Resource catalog decoupled in independent JSON store. | **VALID** |
| **56** | Web Citation Provenance | Official page, verification date, provider, access status stored. | Structured provenance fields populated for all 38 records. | **VALID** |

---

## 3. Methodological Assessment & Detailed Findings

### Finding 1: Pathway Evidence Confidence Static Saturation (P1)
In `src/reskilling_pathway_engine.py` (lines 230–236), `_calculate_pathway_confidence()` computes the evidence confidence score using hardcoded mock component values:
$$\text{Score} = 0.30 \cdot 95.0 + 0.25 \cdot 92.0 + 0.25 \cdot 96.0 + 0.20 \cdot 95.0 = 94.5$$
Consequently, every synthetic pathway generated across all 8 personas in `m4_benchmark_results_v1.json` outputs an identical confidence score of `94.5` (`HIGH`). This violates the core design requirement that evidence confidence reflect pathway-specific evidentiary variation (e.g., varying alignment scores, multi-hop prerequisite dependencies, and provider reliability metrics).

### Finding 2: Provider Diversity Normalization (P2)
The resource catalog lists 29 raw provider labels. However, this count includes brand variants of the same institution:
* **DeepLearning.AI**: Listed under 5 separate labels (`DeepLearning.AI`, `DeepLearning.AI / Coursera`, `DeepLearning.AI / OpenAI`, `DeepLearning.AI / Weights & Biases`, `LangChain / DeepLearning.AI`).
* **The Open University**: Listed under 2 labels (`The Open University (OpenLearn)` and `OpenLearn / The Open University`).
* **Alphabet**: Google Cloud Skills Boost and Kaggle Learn represent 2 divisions of Alphabet.
Normalizing these into institutional parent entities yields **21 distinct organizations**. The catalog must document both raw platform labels and normalized parent entities.

### Finding 3: Synthetic Test Fixtures Mapped to Commercial URLs (P2)
`RES_LOWCOST_01` ("Practical Enterprise API Testing Lab", RM99) and `RES_VAR_01` ("Advanced Enterprise ESG Disclosure Workshop", variable/unknown) were designed as edge-case fixtures to exercise the LOW_COST and UNKNOWN aggregation branches. However, their URLs point to proxy domains (`https://academy.postman.com/pricing` and `https://unglobalcompact.org`). These fixtures must be explicitly tagged as synthetic test fixtures in metadata or replaced with verified commercial courses.

### Finding 4: Deficit-Effort Scaling Floor (0.50) Rationale (P2)
The linear formula $M_{\text{eff}} = 0.50 + 0.50 \cdot \text{Deficit}$ imposes a minimum workload multiplier of $0.50$. For example, a learner with $0.95$ mastery ($\text{Deficit} = 0.05$) still incurs a $0.525$ multiplier, requiring over half of the baseline course duration. While adult learning research supports a non-zero floor (covering environment configuration, mandatory assessment grading, and capstone evaluation), this rationale must be explicitly documented in the methodology.

### Finding 5: Operational Low-Cost Threshold Disclaimer (P3)
The project threshold of $\text{RM } 150.00$ was linked to $5\%$ of the median entry-level clerical monthly salary (DOSM 2024). To prevent misinterpretation as a universal affordability claim, the documentation must explicitly state:
> *"For this prototype, LOW_COST is operationally defined as verified direct resource price <= RM150; it is not asserted as universally affordable."*

### Finding 6: Benchmark Weekly Study Pacing Assumptions (P3)
Benchmark summaries in `m4_benchmark_results_v1.json` report `schedule_weeks` without explicitly qualifying the metric as a benchmark test assumption assuming $10\text{ hours/week}$.

---

## 4. Remediation Sign-Off Protocol

To achieve final freeze readiness in Stage 12C, the following targeted remediation plan is mandated:
1. **Dynamic Confidence Recalibration**: Update `_calculate_pathway_confidence()` to dynamically aggregate `skill_alignment` and `provider_reliability` from attached primary resources and active prerequisite mapping confidences.
2. **Provider Normalization**: Add a `parent_organization` field to `learning_resources_v1.json` and document both raw (29) and normalized (21) provider metrics.
3. **Synthetic Fixture Tagging**: Tag `RES_LOWCOST_01` and `RES_VAR_01` with `"fixture_type": "BENCHMARK_SYNTHETIC_TEST_FIXTURE"`.
4. **Pedagogical Rationale Documentation**: Document the 0.50 effort floor rationale in `artifacts/m4_learning_time_methodology.md`.
5. **Operational Disclaimer Inclusion**: Add the explicit LOW_COST operational disclaimer to `artifacts/m4_cost_accessibility_audit.md`.
6. **Benchmark Column Labeling**: Update benchmark results to display `"TEST ASSUMPTION: 10h/week"`.

Final Stage 12B Review Verdict: **`TARGETED M4 REMEDIATION REQUIRED`**.
