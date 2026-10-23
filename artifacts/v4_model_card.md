# Model Card: AI Skills & Emerging Demand Predictor v4 (M6)

## Model Overview
- **Model Name**: `skills_predictor_v4_candidate`
- **Architecture**: Subword + Word Hybrid TF-IDF `(1,3)-grams` + Calibrated One-vs-Rest Linear Logit Engine
- **Framework**: Scikit-Learn with Platt Sigmoidal Calibration (`CalibratedClassifierCV`)
- **Model Bundle Size**: **590.03 KB** (`model.joblib`)
- **Inference Latency**: **~0.65 ms / sample**
- **Configuration SHA-256**: `ede4490c98b6ed181748fa12d6407f82066284256b9fa8de721a7b7ee7064217`

## Intended Use
Multi-label extraction of 16 critical AI / digitization skills and calibrated probability of emerging task demand for Malaysian workforce profiles, job postings, and competency standards.

## Training Data & Methodology
- **Training Corpus**: `data/processed/dataset_v4_clean_multisource.json` (348 records: 98 GOLD Malaysian/international occupational records + 250 deduplicated synthetic records, with 3x GOLD sample weighting)
- **Model Selection Protocol**: Strictly evaluated via **Grouped 5-Fold Cross-Validation** (isolating entire MASCO 4-digit groups and synthetic template prefixes across folds). Zero test-set leakage.
- **Hyperparameter Decisions**: Selected $C = 2.2$, skill decision threshold $= 0.42$, demand threshold $= 0.5$.

## Protected Out-of-Sample Performance
| Benchmark Set | Metrics (Point Estimate) | 95% Bootstrap Confidence Interval |
| :--- | :--- | :--- |
| **Protocol B (Real-World Generalisation, N=63)** | - Skills Macro F1: **0.7149**<br>- Skills Micro F1: **0.6824**<br>- Demand Macro F1: **0.7644**<br>- Demand ROC AUC: **0.8379**<br>- Demand Brier: **0.1668** | - Macro F1: `[0.5466, 0.7726]`<br>- Micro F1: `[0.5936, 0.7612]`<br>- ROC AUC: `[0.7283, 0.927]`<br>- Brier Score: `[0.1345, 0.2019]` |
| **Protocol C (Unseen-Occupation Set, N=25)** | - Skills Macro F1: **0.6196**<br>- Skills Micro F1: **0.6712**<br>- Demand Macro F1: **0.5098** | - Macro F1: `[0.3991, 0.6925]`<br>- Micro F1: `[0.5556, 0.7833]` |
| **Protocol A (Legacy Synthetic Diagnostic, N=300)** | - Skills Macro F1: **0.6578**<br>- Demand Accuracy: **0.7867** | Legacy diagnostic only |
