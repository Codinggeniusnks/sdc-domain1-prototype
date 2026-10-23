# Calibration Remediation: Resolving Duplicate-Record Leakage in Demand Forecasting

## Executive Summary
The independent forensic audit (`artifacts/opus_v4_independent_audit.md`) identified a critical methodological defect in the legacy RunPod calibration pipeline:
> *"The script implemented multi-tier weighting by physically duplicating Gold records 3 times in the training list. When passed to `CalibratedClassifierCV(cv=3)`, identical physical records were partitioned across internal calibration folds, causing train-calibration leakage and artificially deflating the reported Brier score to 0.1345."*

This remediation eradicates all physical record duplication. Sample tier weighting is passed directly as `sample_weight` to the underlying estimators without mutating dataset row cardinality ($N=348$ remains strictly 348 distinct rows).

---

## Controlled Benchmark: Uncalibrated vs Calibrated (Leakage-Free)

Evaluated across the 5 folds of `artifacts/cv_split_manifest_v2.json` under identical conditions:

| Metric | Uncalibrated (Balanced LogReg) | CalibratedClassifierCV (Platt / Sigmoid, cv=3) | Delta | Status |
|---|---|---|---|---|
| **Demand ROC AUC** | **0.7056** | 0.7026 | -0.0030 | Uncalibrated slightly superior |
| **Brier Score** | **0.2007** | 0.2067 | +0.0060 | **Uncalibrated is better calibrated** |
| **Expected Calibration Error (ECE)** | **0.2069** | 0.2251 | +0.0182 | **Uncalibrated has lower ECE** |
| **Demand Accuracy** | 0.7189 | **0.7268** | +0.0079 | Marginal shift in threshold balance |

---

## Root Cause & Statistical Mechanism

### 1. The Duplicate-Leakage Illusion in Legacy RunPod
- In the legacy script:
  ```python
  # FLAWED LEGACY CODE:
  weighted_train = []
  for r in train_records:
      mult = 3 if r.get("source_tier") == "GOLD" else 1
      for _ in range(mult):
          weighted_train.append(r)
  calibrator = CalibratedClassifierCV(base_estimator, method="sigmoid", cv=3)
  calibrator.fit(weighted_train_X, weighted_train_y)
  ```
- Because Gold records were triplicated, copy 1 was placed in fold 0, copy 2 in fold 1, and copy 3 in fold 2.
- The calibrator was fitting Platt scaling parameters ($A, B$ in $\frac{1}{1 + \exp(Az + B)}$) on the exact same records that the base estimator had trained on!
- This created an artificial, overly optimistic Brier score of 0.1345, completely masking model uncertainty.

### 2. Reality of Small-Sample Platt Scaling
- In small datasets ($N \approx 275$ in training folds), reserving 33% of data for internal calibration splits starves the base logistic regression estimator of training examples.
- Furthermore, binary logistic regression with standard cross-entropy loss already optimizes the log-likelihood (logistic loss), meaning its raw sigmoid outputs are theoretically calibrated under well-specified feature distributions.
- Fitting an additional 2-parameter logistic transformation on top of 3 small CV folds introduces estimation variance, slightly degrading Brier score (0.2007 -> 0.2067) and ECE (0.2069 -> 0.2251).

---

## Production & Screening Policy

1. **Do NOT apply post-hoc Platt calibration on $N < 1,000$ without proof of Brier score reduction on leak-free CV.**
2. Standard balanced logistic regression probabilities ($P(y=1|X) = \sigma(w^T x + b)$) provide more reliable, well-calibrated confidence estimates than post-hoc Platt scaling on this dataset.
3. For the upcoming screening, uncalibrated probabilities are designated as the baseline demand predictor.
