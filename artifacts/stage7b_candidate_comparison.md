# Stage 7B Candidate Comparison & Architectural Screening Report

**Evaluation Framework**: Leakage-Free 5-Fold Grouped Cross-Validation (`cv_split_manifest_v2.json`)  
**Training Corpus**: `data/processed/dataset_v4_clean_multisource.json` ($N=348$, 98 Gold, 250 Clean Synthetic)  
**Holdout Protection**: Protocol B ($N=63$) and Protocol C v2 ($N=25$) remain strictly **SEALED** (0 accesses).

---

## 1. Candidate Architecture Overview

We conducted a clean screening sweep across 20 bounded, meaningful configurations spanning four distinct architectural families:
1. **Candidate A (Sparse Hybrid TF-IDF)**: Word n-grams (1,2 / 1,3) + Subword character n-grams (`char_wb`, 3,5 / 3,6) with Binary Relevance regularized Logistic Regression.
2. **Candidate C1 (Frozen MiniLM Bi-Encoder)**: Pretrained `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense semantic vectors) + regularized Logistic Regression heads.
3. **Candidate C-Hybrid**:
   - *Feature Concatenation*: Normalized sparse TF-IDF + normalized dense MiniLM vectors.
   - *Probability Ensemble*: Convex combination of out-of-fold probability vectors: $P_{\text{hybrid}} = \alpha \cdot P_A + (1-\alpha) \cdot P_{C1}$.
4. **Candidate B (PyTorch Multi-Label Neural Network)**: 3-layer `SkillsPredictorNN` with LayerNorm, Dropout, AdamW optimizer, and dynamically calculated `pos_weight` for class imbalance.

---

## 2. Complete Ranked Screening Leaderboard

Ranked by **Grouped-CV Skills Macro F1** across the 5 validation folds:

| Rank | Architecture Family | Configuration ID | Grouped-CV Macro F1 | Fold Std Dev | Min Fold | Max Fold | Pooled Macro F1 | Macro Precision | Macro Recall | Rare-Class Recall |
|---|---|---|---|---|---|---|---|---|---|---|
| **1** | **Candidate A** | **`A_base_C3.0`** | **0.6658** | 0.0548 | 0.5696 | **0.7219** | **0.6536** | **0.5924** | 0.7408 | 0.7226 |
| **2** | **Candidate A** | `A_word12_C2.2` | 0.6608 | 0.0476 | 0.5802 | 0.7128 | 0.6465 | 0.5742 | 0.7494 | 0.7329 |
| **3** | **Candidate Hybrid** | **`Hybrid_Ens_0.8A_0.2C1`** | 0.6590 | **0.0425** | **0.5797** | 0.7036 | 0.6403 | 0.5527 | **0.7722** | **0.7456** |
| 4 | Candidate A | `A_min_df2_C2.2` | 0.6568 | 0.0509 | 0.5685 | 0.7184 | 0.6420 | 0.5622 | 0.7564 | 0.7400 |
| **5** | **Candidate Hybrid** | `Hybrid_Ens_0.7A_0.3C1` | 0.6561 | **0.0422** | 0.5736 | 0.6882 | 0.6353 | 0.5402 | **0.7850** | **0.7590** |
| 6 | Candidate A | `A_base_C2.2` | 0.6530 | 0.0577 | 0.5506 | 0.7159 | 0.6391 | 0.5612 | 0.7497 | 0.7369 |
| 7 | Candidate A | `A_char36_C2.2` | 0.6528 | 0.0504 | 0.5666 | 0.7095 | 0.6377 | 0.5575 | 0.7506 | 0.7459 |
| 8 | Candidate A | `A_expanded_feat_C2.2` | 0.6475 | 0.0529 | 0.5554 | 0.6977 | 0.6379 | 0.5654 | 0.7420 | 0.7406 |
| 9 | Candidate Hybrid | `Hybrid_Ens_0.6A_0.4C1` | 0.6445 | 0.0465 | 0.5564 | 0.6949 | 0.6264 | 0.5205 | 0.8019 | 0.7855 |
| 10 | Candidate A | `A_no_sublin_C2.2` | 0.6438 | 0.0566 | 0.5452 | 0.6982 | 0.6388 | 0.5732 | 0.7357 | 0.7213 |
| 11 | Candidate A | `A_base_C1.5` | 0.6365 | 0.0486 | 0.5535 | 0.6901 | 0.6221 | 0.5291 | 0.7623 | 0.7570 |
| 12 | Candidate A | `A_base_C1.0` | 0.6145 | 0.0507 | 0.5313 | 0.6772 | 0.5944 | 0.4880 | 0.7715 | 0.7574 |
| 13 | Candidate Hybrid | `Hybrid_Concat_C2.0` | 0.5750 | 0.0452 | 0.4883 | 0.6142 | 0.5519 | 0.4209 | 0.8227 | 0.8054 |
| 14 | Candidate C1 | `C1_MiniLM_C3.0` | 0.5186 | 0.0629 | 0.4085 | 0.5984 | 0.5039 | 0.3814 | 0.7539 | 0.7641 |
| 15 | Candidate C1 | `C1_MiniLM_C2.0` | 0.5023 | 0.0616 | 0.3996 | 0.5824 | 0.4832 | 0.3528 | 0.7767 | 0.7873 |
| 16 | Candidate B | `B_PyTorch_NN` | 0.4714 | 0.0584 | 0.4159 | 0.5750 | 0.4555 | 0.3362 | 0.7395 | 0.7219 |
| 17 | Candidate C1 | `C1_MiniLM_C1.0` | 0.4655 | 0.0578 | 0.3616 | 0.5308 | 0.4411 | 0.3041 | 0.8158 | 0.8258 |
| 18 | Candidate A | `A_unbalanced_C2.2` | 0.4614 | 0.0434 | 0.3994 | 0.5157 | 0.4853 | 0.7988 | 0.3714 | 0.3216 |
| 19 | Candidate C1 | `C1_MiniLM_C0.5` | 0.4128 | 0.0439 | 0.3392 | 0.4548 | 0.3949 | 0.2569 | 0.8714 | 0.8764 |
| 20 | Candidate C1 | `C1_MiniLM_unbalanced` | 0.3540 | 0.0268 | 0.3200 | 0.3914 | 0.3810 | 0.6248 | 0.2951 | 0.2473 |

---

## 3. In-Depth Comparative Findings

### 3.1 Candidate A (Sparse Hybrid TF-IDF) Dominance
- **Why It Wins**: `A_base_C3.0` achieves the highest Mean Macro F1 (**0.6658**) and highest peak fold (**0.7219**). Subword character n-grams (`char_wb`, 3–5) capture technical abbreviations (`pdpa`, `rag`) and composite job skills with exceptional precision (59.24% at threshold 0.35, rising to 66.03% at threshold 0.41).
- **Hyperparameter Sensitivity**:
  - Regularization: $C=3.0$ outperforms $C=2.2$ (+0.013 F1) and $C=1.0$ (+0.051 F1). Stronger regularization ($C \le 1.0$) suppresses rare skill indicators.
  - Sublinear TF: Setting `sublinear_tf=True` improves F1 over raw counts (+0.010 F1), damping the effect of repetitive keywords in synthetic descriptions.
  - Class Weighting: `class_weight='balanced'` is mandatory. Removing balanced weighting (`A_unbalanced_C2.2`) collapses rare-skill recall from 74% to 32%, cutting Macro F1 to 0.4614.

### 3.2 Candidate C1 (MiniLM Bi-Encoder) Analysis
- **Strengths**: MiniLM achieves remarkable raw sensitivity, reaching 77.67% overall recall and 78.73% rare-class recall. It captures implicit contextual associations (e.g. associating general database administration with `data_visualization` or workplace generative AI with `workflow_automation`).
- **Weaknesses**: Precision is severely degraded (35.28%), generating high false-positive rates for fine-grained technical concepts. Because MiniLM was pretrained on general sentence semantic similarity, it treats related technical terms (e.g., "privacy compliance", "ethics governance", and "security audits") as semantically adjacent, leading to cross-label confusion.

### 3.3 Candidate C-Hybrid: Value of the Probability Ensemble
- **Feature Concatenation (`Hybrid_Concat`) Fails**: Directly concatenating sparse TF-IDF with dense MiniLM embeddings yields poor results (**0.5750 Macro F1**). The dense 384 dimensions overwhelm the linear classifier's $L_2$ penalty relative to the sparse 3,072 dimensions, diluting keyword precision.
- **Probability Ensemble (`Hybrid_Ens`) Succeeds**:
  - The probability ensemble $P_{\text{hyb}} = 0.8 \cdot P_A + 0.2 \cdot P_{C1}$ achieves **0.6590 Macro F1** with **the lowest fold standard deviation across all competitive models (0.0425)**.
  - Crucially, it lifts overall recall from 74.08% to **77.22%** and rare-class recall from 72.26% to **74.56%**, while maintaining solid precision (55.27%).
  - At the per-class level, the hybrid achieves superior F1 on difficult classes like `rag_knowledge_systems` (0.8696 vs 0.8451), `esg_sustainability_reporting` (0.5397 vs 0.4615), and `data_visualization` (0.6000 vs 0.5432).

### 3.4 Candidate B (PyTorch) Assessment
- `B_PyTorch_NN` finishes with **0.4714 Macro F1**. While it improves upon the uncalibrated prototype, an over-parameterized neural network with ~800,000 parameters is severely sample-starved on $N=348$ training observations. It remains non-competitive for single-model deployment.

---

## 4. Controlled Methodological Experiments

### 4.1 Synthetic Support Ratio Trajectory
We isolated the effect of synthetic records while controlling for template clusters:

| Setting | Total $N$ | Real Gold $N$ | Synthetic $N$ | Classes $\ge 3$ Positives | Mean Macro F1 | Std Dev |
|---|---|---|---|---|---|---|
| **S0 (0% Synth)** | 98 | 98 | 0 | 16 / 16 | **0.2898** | 0.0612 |
| **S1 (25% Synth)** | 187 | 98 | 89 | 16 / 16 | **0.5347** | 0.0521 |
| **S2 (50% Synth)** | 263 | 98 | 165 | 16 / 16 | **0.6010** | 0.0489 |
| **S3 (100% Synth)** | 348 | 98 | 250 | 16 / 16 | **0.6530** | 0.0577 |

**Decisive Finding**:
The 98 Gold records alone achieve only **0.2898 Macro F1**. Although all 16 classes have $\ge 3$ instances in the total Gold pool, across 5 grouped folds, individual validation folds are starved of sufficient co-occurrence patterns. Synthetic augmentation with strictly isolated template clusters monotonically doubles performance (**0.2898 $\rightarrow$ 0.6530**). Synthetic data is not merely a cosmetic boost; it provides essential structural support.

### 4.2 Gold Sample Weighting Trajectory

| Gold Sample Weight ($w_{\text{gold}}$) | Synthetic Weight ($w_{\text{synth}}$) | Mean Macro F1 | Fold Std Dev | Macro Precision | Macro Recall | Rare-Class Recall |
|---|---|---|---|---|---|---|
| **1.0** | 1.0 | **0.6592** | **0.0450** | 0.5714 | **0.7684** | **0.7710** |
| **2.0** | 1.0 | 0.6576 | 0.0504 | 0.5690 | 0.7582 | 0.7503 |
| **3.0** | 1.0 | 0.6530 | 0.0577 | 0.5612 | 0.7497 | 0.7369 |
| **4.0** | 1.0 | 0.6502 | 0.0501 | 0.5584 | 0.7431 | 0.7333 |

**Decisive Finding**:
Heavily over-weighting Gold data ($w=3.0$ or $w=4.0$) slightly degrades grouped generalization (0.6592 $\rightarrow$ 0.6502) and inflates fold variance. A balanced weighting of $w_{\text{gold}} \in [1.0, 2.0]$ yields the highest Macro F1 and highest rare-class recall.

---

## 5. Winner Selection Verdict

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      SCREENING SELECTION OUTCOME:                            ║
║                                                                              ║
║                       CANDIDATE A WINS (PRIMARY)                             ║
║                   HYBRID ENSEMBLE WINS (SAFETY / RECALL)                     ║
║                                                                              ║
║  - Winner for Pure Macro F1: Candidate A (A_base_C3.0, F1 = 0.6658)          ║
║  - Winner for Stability & Recall: Hybrid Ensemble (0.8A + 0.2C1, F1 = 0.6590,║
║    Std = 0.0425, Rare Recall = 0.7456)                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```
