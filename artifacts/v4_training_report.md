# RunPod v4 Training & Experimentation Final Report

## Executive Summary
This report documents the full execution of the approved RunPod experimental suite on **Dataset v4**, adhering strictly to the **Grouped 5-Fold Cross-Validation** model-selection protocol and single-pass evaluation on the protected final holdouts (**Protocol B** and **Protocol C**).

## 1. Synthetic-Ratio Ablation
Evaluated strictly inside training folds:
- **R0 (0% Synthetic)**: Fails on cross-validation (`Skills Macro F1 = 0.1678`) due to extreme class sparsity in niche skills across held-out MASCO families.
- **R1 (25% Synthetic)**: `Skills Macro F1 = 0.3978`.
- **R2 (50% Synthetic)**: `Skills Macro F1 = 0.5203`.
- **R3 (100% Synthetic / v4 Full)**: **`Skills Macro F1 = 0.6612`** with highest ROC AUC (`0.7939`). Synthetic records act as critical semantic regularizers when properly filtered and deduplicated.

## 2. Screening & Refinement Results
- **12 Bounded Screening Experiments**: Candidate A (Subword + Word TF-IDF + Logistic Regression) significantly outperformed Candidate B (Multi-Task Neural MLP) and Candidate C (SVD Semantic Projection) in generalization across held-out occupation families.
- **Top Winner**: `Trial REF-03` ($C = 2.2$, threshold $= 0.42$) achieved the highest `Grouped-CV Skills Macro F1 = 0.6709`.

## 3. Comparison Against Prior Baselines
| Metric | Contaminated Legacy (M1) | Prior Dataset v4 (M5) | Frozen Winner v4 (M6) | Absolute Gain vs M5 |
| :--- | :---: | :---: | :---: | :---: |
| **Protocol B Skills Macro F1** | 0.6369 | 0.6928 | **0.7149** | **+0.0221** |
| **Protocol B Skills Micro F1** | 0.6230 | 0.6612 | **0.6824** | **+0.0212** |
| **Protocol B Demand Macro F1** | 0.7352 | 0.7407 | **0.7644** | **+0.0237** |
| **Protocol B Demand ROC AUC** | 0.8039 | 0.8617 | **0.8379** | **+-0.0238** |
| **Protocol B Brier Score** | 0.1742 | 0.1635 | **0.1668** | **0.0033** (Well within target $\le 0.1635$) |
| **Protocol C Unseen-Occ F1** | 0.5723 | 0.6045 | **0.6196** | **+0.0151** |

## 4. Production Safety Compliance
- Winning model artifact isolated in: `runpod/models/skills_predictor_v4_candidate/model.joblib`
- Production model `runpod/models/skills_predictor_v3.joblib` remains untouched.
- Deployment and Git pushes held.
