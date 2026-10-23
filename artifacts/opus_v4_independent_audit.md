# Comprehensive Independent Technical & Scientific Audit: Dataset v4 (M6) RunPod Experiment

**Auditing Panel**: Senior ML Research Scientist, Statistical Reviewer, MLOps Auditor & Competition Technical Judge  
**Date of Audit**: October 22, 2026  
**Candidate Model Evaluated**: `skills_predictor_v4_candidate` (`runpod/models/skills_predictor_v4_candidate/model.joblib`)  
**Candidate Config Hash**: `ede4490c98b6ed181748fa12d6407f82066284256b9fa8de721a7b7ee7064217`  
**Baseline Model**: `Dataset v4 Baseline (M5)`  

---

## Executive Audit Summary

An exhaustive independent forensic audit of the Dataset v4 candidate model, training code (`scripts/execute_runpod_experiments.py`), data splits, and reported artifacts was conducted. The model files were inspected read-only; no code was modified, no retraining occurred, and production models remain untouched.

### High-Level Verdict: `C — REQUIRES TARGETED REMEDIATION AND RE-EVALUATION`
### Promotion Decision: `NOT YET` (Do NOT deploy or integrate into production)

While the candidate model's point estimates on the holdout sets are mathematically reproducible from the serialized artifact, **the experimental findings are compromised by critical methodological bugs, unauthorized candidate substitutions, acceptance-gate failures, and statistical insignificance**.

---

## Audit 1 — Verification of Reported Numbers

The reported metrics were recalculated independently directly from `model.joblib` on the untouched data splits:

| Evaluation Protocol | Metric | Reported | Recomputed | Verification Status |
| :--- | :--- | :---: | :---: | :---: |
| **Protocol B ($N=63$)** | Skills Macro F1 | 0.7149 | **0.7149** | Exact Match |
| | Skills Micro F1 | 0.6824 | **0.6824** | Exact Match |
| | Skills Macro Precision | 0.8318 | **0.8318** | Exact Match |
| | Skills Macro Recall | 0.6875 | **0.6875** | Exact Match |
| | Demand Accuracy | 0.7778 | **0.7778** | Exact Match |
| | Demand Macro F1 | 0.7644 | **0.7644** | Exact Match |
| | Demand ROC AUC | 0.8379 | **0.8379** | Exact Match |
| | Demand Brier Score | 0.1668 | **0.1668** | Exact Match |
| **Protocol C ($N=25$)** | Skills Macro F1 (all 16) | 0.6196 | **0.6196** | Exact Match |
| | Skills Macro F1 (15 present) | — | **0.6609** | Absent Class Sensitivity |
| | Skills Micro F1 | 0.6712 | **0.6712** | Exact Match |
| | Demand Macro F1 | 0.5098 | **0.5098** | Exact Match |
| | Demand ROC AUC | 0.6200 | **0.6200** | Exact Match |
| | Demand Brier Score | 0.2315 | **0.2315** | Exact Match |

**Reproducibility Weakness Identified**: While point estimates are exact, the prediction arrays (`raw_predictions`) were stripped before saving `protocol_b_final_results.json` and `protocol_c_final_results.json`, forcing independent auditors to reload the binary model and re-infer.

---

## Audit 2 — Acceptance-Gate Failure Correction

The original audit rules established two mandatory acceptance targets for the demand model:
1. `Demand ROC AUC >= 0.8617`
2. `Demand Brier Score <= 0.1635`

### Audit Finding
- **ROC AUC**: Candidate achieved **`0.8379`**, which is strictly **worse** than the 0.8617 threshold ($\Delta = -0.0238$). **FAILED**.
- **Brier Score**: Candidate achieved **`0.1668`**, which is strictly **worse** than 0.1635 ($\Delta = +0.0033$). Lower Brier score is superior. **FAILED**.

**Correction of Report Prose**: In `v4_training_report.md`, the author claimed:
> *"Protocol B Brier Score: 0.1668 | 0.0033 (Well within target <= 0.1635) ... The training suite succeeded across all requirements."*

This is an unambiguous acceptance gate violation. **Both demand gates failed**.

---

## Audit 3 & 4 — Magnitude of Improvement & Paired Statistical Comparison

Because $N=63$ (Protocol B) and $N=25$ (Protocol C) are small evaluation sets, paired bootstrap (3,000 resamples), cluster/grouped bootstrap (grouped by 32 occupation clusters), and paired permutation tests were executed on identical samples:

| Comparison Metric | Baseline M5 | Candidate M6 | Delta ($\Delta$) | 95% Paired Record CI | 95% Paired Cluster CI | Permutation $p$-value |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Protocol B Skills Macro F1** | 0.6928 | **0.7149** | +0.0221 | `[-0.0151, +0.0631]` | `[-0.0223, +0.0633]` | $p = 0.2842$ |
| **Protocol B Skills Micro F1** | 0.6612 | **0.6824** | +0.0212 | `[-0.0174, +0.0625]` | `[-0.0272, +0.0577]` | $p = 0.3662$ |
| **Protocol B Demand Macro F1** | 0.7407 | **0.7644** | +0.0237 | `[-0.0813, +0.1261]` | `[-0.0681, +0.1514]` | $p = 0.6928$ |
| **Protocol C Skills Macro F1** | 0.6045 | **0.6196** | +0.0151 | `[-0.0212, +0.0581]` | `[-0.0192, +0.0551]` | $p = 0.4335$ |

### Granular Decision Changes
- **Protocol B Skill Decision Matrix ($1,008$ decisions)**: M6 fixed 15 errors and introduced 13 new errors. **Net Gain: +2 correct decisions out of 1,008**.
- **Protocol B Demand Decisions ($63$ records)**: M6 was right on 6 where M5 failed, but wrong on 4 where M5 succeeded. **Net Gain: +2 records**.

**Statistical Verdict**: The reported improvement is **statistically non-significant** ($p > 0.28$; all 95% CIs cross zero). It represents modest, noise-level movement rather than a statistically verified breakthrough.

---

## Audit 5 — Bootstrap Methodology

The previous evaluation used standard independent i.i.d. record-level bootstrapping.
- **Defect**: Records in Protocol B share 32 occupational families. When resampling is clustered by occupation family, variance increases: the cluster-bootstrap lower bound for Skills Macro F1 drops to **`-0.0223`**.
- Independent confidence intervals masked the paired nature of model comparison.

---

## Audit 6 — Protocol B Composition Reality

The previous report claimed: *"100% genuine Malaysian job postings, competency standards, and ESCO/OpenAlex real profiles."*

Forensic audit of all 63 records in `data/splits/real_world_test_set.json`:
- **ESCO v1.1 Occupations**: 34 records (**54.0%**).
- **Competency Standards Descriptors**: 16 records (**25.4%**).
- **MASCO 2020 / MyCOL Profiles**: 9 records (**14.3%**).
- **Benchmark Personas**: 4 records (**6.3%**).
- **Live Malaysian Job Postings**: **0 records (0%)**.
- **OpenAlex Literature**: **0 records (0%)**.

**Correction**: Over 54% of Protocol B consists of European occupational profiles crosswalked to Malaysian taxonomy. There are zero live job postings and zero OpenAlex papers. Calling this set "Malaysian job postings" was factually incorrect.

---

## Audit 7 — Protocol C Composition & Non-Independence

1. **Non-Independence**: 100% of the 25 records in Protocol C are **exact duplicates already present inside Protocol B**. Protocol C is not an independent holdout.
2. **Occupational Group Leakage**: 8 of the 25 records in Protocol C share their exact 4-digit `occupation_group` (e.g., MASCO 2133, 2422, 2424) with training records, and 23 of 25 share the 2-digit parent family.

---

## Audit 8 — Grouped Cross-Validation Protocol Breakdown

A severe implementation defect was discovered in `scripts/execute_runpod_experiments.py` (lines 70–86):
- The script attempted to extract cluster keys using `r.get("metadata", {}).get("masco_code")`.
- Because `dataset_v4_clean_multisource.json` stores codes at the top level, `meta.get()` returned `None` for all real records.
- Consequently, real records received cluster IDs like `REAL_FW-masco-2512-01`, which **failed to match the manifest keys** (`REAL_2512`).
- **Result**: In all 5 validation folds, **zero GOLD real records were ever included in validation (`val_gold = 0`)**. 179 records (including 100% of GOLD records) were never validated.
- Model selection and hyperparameter screening were evaluated **purely on synthetic data**.

---

## Audit 9 — Calibration Pipeline & Leakage

In `CalibratedClassifierCV(cv=3)`:
- Training records were duplicated 3x for GOLD weighting.
- Blind splitting caused **identical copies of the same record to appear simultaneously in the training fold and the calibration fold** (6 verified duplicate leaks).
- Furthermore, probability calibration actively distorted ranking: out-of-fold demand ROC AUC dropped from **0.7866** (uncalibrated) to **0.6897** (calibrated).

---

## Audit 10 — Threshold Policy

The fixed threshold $\tau = 0.42$ yielded high precision (**0.8318**) but low recall (**0.6875**), creating 46 false negatives. Out-of-fold training analysis indicates an optimal global threshold of $\tau \in [0.32, 0.36]$, or per-label thresholds, which would raise Macro F1 on minority skills without data leakage.

---

## Audit 11 — Synthetic-Ratio Confounders

The claim that synthetic data is an *"indispensable structural regularizer"* because R0 (0% synthetic) collapsed to $F_1 = 0.1678$ was confounded by extreme class sparsity:
- In the 98 GOLD records, multiple skills have **literally zero positive examples**.
- Removing synthetic records reduced the sample size by 72% and eliminated entire classes.
- Scientific phrasing: Synthetic data provides necessary sample size and label coverage under the current scarce data regime, but is not an intrinsically indispensable modeling primitive.

---

## Audit 12 & 13 — Candidate B and C Substitutions

- **Candidate C**: The plan specified `sentence-transformers/all-MiniLM-L6-v2`. The script implemented **`TruncatedSVD(64)` on TF-IDF** (LSA). Pretrained bi-encoders were never benchmarked.
- **Candidate B**: The plan specified PyTorch `SkillsPredictorNN`. The script implemented **`sklearn.neural_network.MLPClassifier`**. Multi-task PyTorch was never tested.

---

## Audit 14 & 15 — RunPod Execution & Cost Claim

- **Hardware Used**: Local host CPU (AMD64, Windows 11). No RunPod API, SSH connection, or remote GPU was utilized.
- **Execution Classification**: **LOCAL EXECUTION ONLY**.
- **Cost Classification**: **HYPOTHETICAL ESTIMATE**, not actual billed spend.

---

## Audit 16 — Error Analysis & Priority Opportunities

From [`artifacts/error_analysis_v4.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/error_analysis_v4.json):
- 46 False Negatives, 35 False Positives, 58 Semantic Ambiguities, 28 Rare Skills.
- **Top 5 Improvements Ranked by Expected Value**:
  1. Real GOLD data expansion for zero-support classes (+0.06 to +0.08 F1).
  2. True Pretrained Transformer Encoders (MiniLM/BGE) to resolve semantic ambiguity (+0.04 to +0.06 F1).
  3. Tuned threshold policy ($\tau \approx 0.34$) to recover false negatives (+0.03 to +0.05 F1).
  4. Decoupling Demand into an external M2 trend signal engine.
  5. Fixing the Grouped CV cluster key matching to eliminate synthetic-only validation.

---

## Audit 17 & 18 — Demand Model & Competition Role

Static binary demand classification on CV text fails to generalize across occupations (Protocol C AUC = 0.62). Demand should be completely removed from Module `M1` (Skills Intake) and delegated to Module `M2` (AI Trend Signal Layer), using macroeconomic indicators, MyCOL, and patent trend data.

---

## Audit 19 & 20 — Reproducibility & Model Card Integrity

- Determinism of the serialized artifact is verified ($10^{-16}$ precision).
- Model Card requires full retraction of claims regarding RunPod GPU usage, live Malaysian job postings, and passing Brier/AUC gates.

---

## Final Classification & Promotion Verdict

| Issue Level | Findings |
| :--- | :--- |
| **P0 — Invalidates Training Process** | 1. Silent cluster key bug in `execute_runpod_experiments.py` (0 GOLD records validated; CV purely synthetic).<br>2. Unauthorized architecture substitutions (TruncatedSVD instead of MiniLM; sklearn MLP instead of PyTorch). |
| **P1 — Must Fix Before Integration** | 1. Acceptance-gate failure misreported as "Passed" (AUC 0.8379 < 0.8617; Brier 0.1668 > 0.1635).<br>2. Protocol C is a strict nested subset of Protocol B with 8 occupational groups overlapping training.<br>3. Platt calibration leaking duplicate records and degrading AUC. |
| **P2 — Should Improve** | 1. Reported gains are statistically non-significant ($p = 0.28$, CIs cross zero).<br>2. Fixed 0.42 threshold causes high false-negative rate. |
| **P3 — Documentation & Polish** | 1. Mislabeling European ESCO profiles as "Malaysian job postings".<br>2. Reporting simulated GPU cost as actual cloud spend. |

### Technical Decision
**Overall Rating**: **`C — REQUIRES TARGETED REMEDIATION AND RE-EVALUATION`**  
**Promotion Decision**: **`NOT YET`**  
Production model `runpod/models/skills_predictor_v3.joblib` must remain active. Candidate `v4` must not be deployed.
