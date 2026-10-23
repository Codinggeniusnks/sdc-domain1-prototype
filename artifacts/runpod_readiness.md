# RunPod Readiness Verdict & Experiment Specification

## 1. Official Verdict

> [!IMPORTANT]
> **VERDICT: `RUNPOD PROTOCOL READY`** *(using `Dataset v4` + Grouped 5-Fold Cross-Validation + Protected Final Holdouts)*

### Justification for Verdict
1. **Methodological Separation Enforced**:
   - **Training-Side Optimization**: All model selection, hyperparameter tuning, synthetic ratio ablation, decision thresholds, and probability calibration fitting are performed **strictly inside** `data/processed/dataset_v4_clean_multisource.json` (`348` records) via **Grouped 5-Fold Cross-Validation**.
   - **Cluster Isolation**: Grouping by MASCO 4-digit unit groups / competency frameworks for real records and sentence template prefixes for synthetic records guarantees that entire occupation families and syntactic templates never straddle training and validation folds (`artifacts/cv_split_manifest.json`).
   - **Holdout Protection**: **Protocol B** (`real_world_test_set.json`, $N=63$) and **Protocol C** (`unseen_occupation_test_set.json`, $N=25$) are designated **STRICT FINAL HOLDOUT TEST SETS**. They are evaluated **strictly ONCE** after all architecture and hyperparameter choices are frozen, preventing any test set leakage or over-tuning.
   - **Legacy Diagnostic**: **Protocol A** (`frozen_test_set.json`, $N=300$) is preserved solely as a legacy synthetic diagnostic.

---

## 2. Training-Side Model Selection Specification (Grouped 5-Fold CV)

All experimentation, architecture screening, and tuning use the training corpus alone:

| Parameter | Specification |
| :--- | :--- |
| **Training Corpus** | **`data/processed/dataset_v4_clean_multisource.json`** ($N = 348$: 98 GOLD occupational/competency records + 250 deduplicated BRONZE synthetic records) |
| **CV Splitting Scheme** | **Grouped 5-Fold Cross-Validation** (Grouped by MASCO unit group, competency framework ID, or synthetic template family) |
| **Split Manifest** | [`artifacts/cv_split_manifest.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/cv_split_manifest.json) |
| **Primary Selection Metric** | **`Grouped-CV Skills Macro F1`** |
| **Secondary CV Metrics** | - `Grouped-CV Skills Micro F1`<br>- `Grouped-CV Demand Macro F1`<br>- `Grouped-CV Demand ROC AUC`<br>- `Grouped-CV Demand Brier Score`<br>- Per-class Precision & Recall |
| **Probability Calibration** | Platt scaling / isotonic calibration fitted strictly inside CV folds (`CalibratedClassifierCV(method="sigmoid", cv=3)`), never touching holdout sets |
| **Synthetic Ratio Selection** | Selected strictly via Grouped CV across 0%, 25%, 50%, 100% synthetic inclusion ratios |

### Verified Training-Side Grouped-CV Screening Results (`artifacts/grouped_cv_results.json`)

#### Synthetic Ratio Ablation (Grouped 5-Fold CV on Dataset v4)
- **0% Synthetic** (Pure Real, $N=98$): `Skills Macro F1 = 0.2827 ± 0.0687`, `Demand Macro F1 = 0.5589` (severe sparsity on niche skill classes).
- **25% Synthetic** ($N=160$): `Skills Macro F1 = 0.4929 ± 0.0526`, `Demand Macro F1 = 0.5459`.
- **50% Synthetic** ($N=223$): `Skills Macro F1 = 0.5827 ± 0.0540`, `Demand Macro F1 = 0.5949`.
- **100% Synthetic** ($N=348$): `Skills Macro F1 = 0.6821 ± 0.0666`, `Demand Macro F1 = 0.5947` (optimal regularization and vocabulary coverage without template leakage across folds).

#### Architecture & Hyperparameter Screening (Grouped 5-Fold CV)
- **Candidate 1 (LinearSVC, C=1.0)**: `Grouped-CV Skills Macro F1 = 0.6683`, `Demand ROC AUC = 0.8395`, `Brier = 0.1595`
- **Candidate 2 (LogisticRegression, C=2.0, Thresh=0.45)**: `Grouped-CV Skills Macro F1 = 0.6821`, `Demand ROC AUC = 0.8396`, `Brier = 0.1578`
- **Candidate 3 (LogisticRegression, C=3.0, Thresh=0.40)**: **`Grouped-CV Skills Macro F1 = 0.6947 ± 0.0728`**, `Demand ROC AUC = 0.8413`, `Brier = 0.1568` *(WINNING TRAINING-SIDE CONFIGURATION)*

---

## 3. Final Protected Holdout Evaluation (Evaluated ONCE Post-Selection)

Evaluated only after freezing the winning configuration (`LogisticRegression_C3_T40`) selected via Grouped CV:

| Protocol | Dataset | Samples | Skills Macro F1 | Skills Micro F1 | Demand Macro F1 | Demand ROC AUC | Brier Score | Role in Pipeline |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Protocol B** | `real_world_test_set.json` | 63 | **0.6888** | 0.6517 | **0.7380** | **0.8413** | **0.1676** | **FINAL HOLDOUT: Real-World Generalisation** |
| **Protocol C** | `unseen_occupation_test_set.json` | 25 | **0.6061** | 0.6531 | **0.4762** | **0.6200** | **0.2260** | **FINAL HOLDOUT: Unseen-Occupation Generalisation** |
| **Protocol A** | `frozen_test_set.json` | 300 | 0.6752 | 0.6672 | 0.6730 | 0.8814 | 0.1500 | *Legacy Synthetic Diagnostic Only* |

---

## 4. RunPod Execution Specifications

| Parameter | Specification |
| :--- | :--- |
| **Search Space** | Deep Bi-Encoder fine-tuning (`all-MiniLM-L6-v2`) + Multi-Task Head vs. Multi-Task MLP with Sample Weights |
| **CV Constraint** | All candidate tuning and early stopping must execute against the 5 folds defined in `artifacts/cv_split_manifest.json` |
| **GPU Requirement** | NVIDIA RTX 3070 / RTX A4000 (16 GB VRAM) ($<\$0.25/\text{hr}$); total run time $< 5$ minutes |
| **Termination Criteria** | Final candidate weights chosen strictly by highest `Grouped-CV Skills Macro F1`; holdouts (Protocols B and C) evaluated strictly once for final reporting |
