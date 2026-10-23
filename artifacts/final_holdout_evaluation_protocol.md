# Stage 8D Artifact: Final Holdout Evaluation Protocol (One-Shot Execution Plan)

**Protocol Authority**: Senior ML Research Architect & Statistical Reviewer  
**Target Stage**: Stage 9 — Model Freeze & One-Shot Sealed Holdout Evaluation  
**Current Holdout Access Count**: **0 (Both Holdouts Remain Strictly SEALED)**  

---

## 1. The 16 Mandatory Execution Rules (Task 13)

The next stage must execute the final holdout evaluation under the following non-negotiable operational sequence:

1. **Freeze Architecture**: Instantiate only the approved Primary Hybrid Ensemble (`H_blend_0.70A_0.30C1_W1.0`).
2. **Freeze Hyperparameters**: Lock Component A (`LogisticRegression(C=2.5, class_weight="balanced", solver="liblinear", random_state=42)`) and Component C1 (`LogisticRegression(C=3.0, class_weight="balanced", solver="liblinear", random_state=42)`).
3. **Freeze Feature Pipeline**: Lock `FeatureUnion` (`word` n-grams `(1,3)`, max `2048`, `min_df=1`, `sublinear_tf=True`, `stop_words="english"`; `subword` `char_wb` `(3,5)`, max `1024`, `min_df=2`, `sublinear_tf=True`) and frozen `sentence-transformers/all-MiniLM-L6-v2` (`384`-d L2-normalized embeddings).
4. **Freeze Ensemble Weights**: Lock linear probability combination weights at $w_A = 0.70$ and $w_{C1} = 0.30$.
5. **Freeze Thresholds**: Lock primary evaluation threshold at $\theta_{\text{eval}} = 0.375$, and product human-in-the-loop thresholds at $\theta_{\text{core}} = 0.450$ and $\theta_{\text{suggested}} = 0.250$.
6. **Freeze Preprocessing & Fit on Full Dataset v5**: Fit the TF-IDF vectorizers and both linear classifier heads once on 100% of `data/processed/dataset_v5_clean_multisource.json` ($N = 311$) with uniform sample weight $1.0$.
7. **Verify Dataset v5 SHA-256 Before Fitting**: Programmatically assert that `data/processed/dataset_v5_clean_multisource.json` matches SHA-256 `9c59cc584167b3047e0d5f4177f205937e297da0605e99b369edfc738124032d` before training begins.
8. **Serialize Frozen Model & Record SHA-256 Prior to Unsealing Holdouts**: Save the fitted model artifact (`models/skills_predictor_v5_frozen/model.joblib` and `config.json`), compute their SHA-256 digests, and write the lock manifest **before** reading either holdout file.
9. **Evaluate Protocol B Exactly Once**: Unseal and run inference on `data/splits/real_world_test_set.json` exactly once, incrementing the Protocol B access log from `0` to `1`.
10. **Evaluate Protocol C v2 Exactly Once**: Unseal and run inference on `data/splits/unseen_occupation_test_set_v2.json` exactly once, incrementing the Protocol C v2 access log from `0` to `1`.
11. **Save Record-Level Predictions**: Persist complete record-level ground truth, confidence scores, binary predictions at $\theta_{\text{eval}} = 0.375$, and Core/Suggested tier assignments for both holdouts.
12. **Calculate 95% Confidence Intervals**: Compute non-parametric paired bootstrap 95% confidence intervals ($B = 2,000$ resamples, `random_state=42`) for all primary metrics on Protocol B and Protocol C v2.
13. **Zero Post-Hoc Tuning**: No hyperparameter, vocabulary size, regularization parameter, or sample weight may be modified after viewing holdout results.
14. **No Second Candidate Evaluation**: Neither Candidate C1 nor Candidate A may be evaluated as competing models on the holdouts to pick a post-hoc winner.
15. **No Threshold Adjustment**: Neither $\theta_{\text{eval}} = 0.375$ nor the Core/Suggested thresholds ($0.450 / 0.250$) may be adjusted after viewing holdout performance.
16. **No Architecture Substitution**: Whatever metrics the frozen model achieves on Protocol B and Protocol C v2 must be reported truthfully as the official result.

---

## 2. Conservative Statistical Reporting Standards (Task 14)

Because real-world and unseen-occupation holdouts are finite sample sizes, all reporting in Stage 9 and competition submission documents must adhere to strict statistical discipline:

### 2.1. Required Quantitative Disclosures
For both **Protocol B (Real-World Holdout)** and **Protocol C v2 (Unseen-Occupation Holdout)**, report:
1. **Point Estimate + 95% Bootstrap CI**:
   - Skills Macro F1 `[95% CI: lower, upper]`
   - Skills Micro F1 `[95% CI: lower, upper]`
   - Macro Precision & Macro Recall `[95% CI: lower, upper]`
   - Rare-Class Recall `[95% CI: lower, upper]`
2. **Per-Class Breakdown**:
   - Report per-class Precision, Recall, F1, and positive support $n_k$.
   - Explicitly flag any class with holdout support $n_k < 5$ as **low-support / high-variance diagnostic**.
3. **Baseline Comparison Discipline**:
   - When comparing against historical M5/v4 baselines on Protocol B, report both point deltas and whether the 95% bootstrap confidence interval of the difference excludes zero.
   - Note that Protocol C v2 (`unseen_occupation_test_set_v2.json`) is a remediated, stricter holdout than the legacy Protocol C v1; therefore, Protocol C v2 results must be reported as the new clean benchmark rather than a paired delta against v1.
4. **Structured Error Analysis**:
   - Categorize false positives and false negatives by occupational group, implicit vs explicit phrasing, and whether missed Core skills were captured by the Suggested tier ($0.25 \le S < 0.45$).

### 2.2. Prohibited Claims & Language Hygiene
- **Prohibited Phrases**: Do **not** use unsubstantiated superlatives such as *"proves superiority"*, *"decisively beats"*, *"flawless extraction"*, or *"production-grade certainty"* unless directly backed by a statistically significant confidence interval ($p < 0.05$) and adequate sample support.
- **Required Framing**: Frame confidence outputs as *"uncalibrated model confidence scores"* and frame the model as a *"human-in-the-loop decision-support extractor paired with user confirmation."*
