# Next Experiment Gate: Stage 8 Execution Protocol & Holdout Release Policy

## Executive Summary
This document defines the strict gate criteria for **Stage 8**, establishing which experiments to retain, which to deprecate, the infrastructure requirements, and the exact cryptographic conditions under which final holdouts (Protocols B and C v2) may be unsealed.

---

## 1. Experimental Scope for Stage 8

To avoid wasting compute and developer quota on redundant configurations, Stage 8 experiments are strictly bounded:

```
Stage 8 Experimental Matrix (Max 6 Configurations)
├── 1. Candidate A (Sparse Hybrid TF-IDF, C=3.0, w_gold=1.5)
├── 2. Candidate A (Sparse Hybrid TF-IDF, C=2.2, w_gold=1.0)
├── 3. Candidate C1 (MiniLM Linear Head, C=2.0)
├── 4. Hybrid Ensemble (0.8 Candidate A + 0.2 MiniLM C1)
├── 5. Hybrid Ensemble (0.7 Candidate A + 0.3 MiniLM C1)
└── 6. Class-Conditional Synthetic Pruning Evaluation
```

### Models Permanently Deprecated from Screening:
- **Candidate B (PyTorch `SkillsPredictorNN`)**: Formally retired. $N \le 500$ is too small for over-parameterized neural nets without severe variance.
- **Candidate Hybrid Concat (Feature Stacking)**: Formally retired. Sparse-dense concatenation dilutes $L_2$ regularisation penalties.

---

## 2. Infrastructure & Compute Decision

### **VERDICT: NO RUNPOD NEEDED YET**

### Technical Reasoning:
1. **Computational Speed**: Candidate A trains across 5 grouped folds in **1.8 seconds on a standard 4-core CPU**.
2. **Deterministic Caching**: MiniLM 384-dimensional embeddings are pre-computed and cached locally. Training linear heads across 5 folds takes **2.4 seconds on CPU**.
3. **Budget Conservation**: Cloud GPU rental (RunPod / Lambda) adds latency, SSH tunneling overhead, and billing costs with zero predictive advantage on tabular/linear representations.
4. **When RunPod Becomes Justified**: Cloud GPUs will only be provisioned if:
   - Full end-to-end transformer encoder fine-tuning (LoRA / full backprop) is initiated.
   - The Gold training corpus expands to $>1,000$ records.

---

## 3. Terminal Holdout Unsealing Gate

Protocols B and C v2 are the irreplaceable final test of real-world generalisation. **They must never be touched during development.**

```
                       Terminal Holdout Release Protocol
                                       │
     1. Complete Gold Expansion (N_gold >= 300, 0 overlap with B/C v2)
                                       │
                                       ▼
     2. Execute Stage 8 Grouped CV (cv_split_manifest_v3.json)
                                       │
                                       ▼
     3. Select & Freeze Exactly ONE Candidate (Compute SHA-256 Hash)
                                       │
                                       ▼
     4. Formal Sign-off from Competition Systems Architect
                                       │
                                       ▼
     [ONE-SHOT TERMINAL EVALUATION ON PROTOCOL B & PROTOCOL C v2]
```

### Strict Preconditions for Holdout Release:
1. **Corpus Expansion Gate**: Minimum 300 total records with $\ge 200$ Gold authoritative samples. Zero ID or textual overlap with Protocol B and C v2.
2. **Single Production Freeze**: Exactly **one** configuration (e.g. `skills_predictor_v5_final.joblib`) must be written to disk, and its configuration hash recorded in git.
3. **One-Shot Blind Run**: Protocol B ($N=63$) and Protocol C v2 ($N=25$) will be evaluated exactly **once**. No tuning, threshold modification, or retraining is permitted after unsealing.

---

## 4. Competition Strategy Priority Ranking

To maximize overall competition score and deliver the full functionality mandated by the project requirements (M1 to M6 engines and O1 to O6 outcomes), development effort is ranked as follows:

### Priority #1: BUILD M2 TREND INTELLIGENCE ENGINE (Highest ROI)
- **Why**: Static demand classification is obsolete. The M2 Trend Engine provides dynamic labour market intelligence, AI displacement indices, and real-time temporal momentum that powers the downstream matching (M3), reskilling (M4), and scenario modeling (M6) engines. Without M2, the system cannot demonstrate future-readiness.

### Priority #2: EXPAND GOLD DATA (Foundation for ML Generalisation)
- **Why**: Moving from 98 to $\ge 300$ Gold Malaysian records directly eliminates the primary bottleneck of the skills extractor, boosting real-world precision and recall across weak classes (`data_privacy_pdpa`, `process_mapping`, `esg_sustainability_reporting`).

### Priority #3: MORE MODEL OPTIMISATION (Lowest Current ROI)
- **Why**: Algorithmic tuning is saturated on the current 348-sample dataset. Further grid searches or deep learning variants yield diminishing returns ($<0.005$ F1). Model refinement should only resume after expanded Gold data is ingested.
