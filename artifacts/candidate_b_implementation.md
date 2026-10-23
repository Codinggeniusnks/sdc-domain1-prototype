# Candidate B Implementation: Genuine PyTorch Multi-Label Neural Network

## Executive Summary
During the independent forensic audit (`artifacts/opus_v4_independent_audit.md`), Candidate B was flagged as a placeholder that failed to meet competition specifications. Specifically, earlier scripts utilized a basic feedforward approximation with artificial weights.

This remediation implements an **authentic PyTorch neural network** (`SkillsPredictorNN`) adhering to modern multi-label classification standards, featuring positive class weighting (`pos_weight`), layer normalization, dropout regularization, AdamW optimization, sample-weighted loss reduction, and early stopping on validation loss.

---

## Architecture Specification

```
Input Features (X: TF-IDF sparse -> dense, 3072 dims)
         │
         ▼
    Linear (3072 -> 256)
         │
         ▼
    LayerNorm (256)
         │
         ▼
      ReLU()
         │
         ▼
   Dropout (p = 0.30)
         │
         ▼
    Linear (256 -> 128)
         │
         ▼
      ReLU()
         │
         ▼
   Dropout (p = 0.21)
         │
         ▼
    Linear (128 -> 16)
         │
         ▼
Raw Logits (16 classes) ──► BCEWithLogitsLoss(pos_weight, reduction='none')
         │
         ▼ (Inference)
    Sigmoid() ──► Multi-label Probabilities P(y_j = 1 | X)
```

### PyTorch Definition (`src/remediation_engine.py`):
```python
class SkillsPredictorNN(nn.Module):
    def __init__(self, in_features: int, hidden_1: int = 256, hidden_2: int = 128, num_skills: int = 16, dropout: float = 0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_1),
            nn.LayerNorm(hidden_1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_1, hidden_2),
            nn.ReLU(),
            nn.Dropout(dropout * 0.7),
            nn.Linear(hidden_2, num_skills),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
```

---

## Training & Regularization Details

1. **Handling Severe Class Imbalance (`pos_weight`)**:
   In multi-label skill tagging, negative instances outnumber positive instances for rare skills by up to 20:1. We compute positive class weights dynamically per training fold:
   $$\text{pos\_weight}_j = \text{clip}\left(\frac{N - N_j^+}{N_j^+ + \epsilon}, 1.0, 10.0\right)$$
   This prevents the neural network from trivial collapse into predicting all zeros for rare labels.

2. **Sample Weight Integration**:
   Loss reduction is set to `reduction='none'`. Each sample's raw multi-label binary cross-entropy is scaled by its source tier weight ($w_i = 3.0$ for Gold, $w_i = 1.0$ for Synthetic) before mean reduction:
   $$\mathcal{L} = \frac{1}{B} \sum_{i=1}^B w_i \cdot \text{BCEWithLogitsLoss}(z_i, y_i)$$

3. **Optimization & Early Stopping**:
   - Optimizer: `torch.optim.AdamW(lr=1e-3, weight_decay=1e-4)`
   - Mini-batch size: 32 with shuffle
   - Max epochs: 50
   - Patience: 8 epochs monitoring validation BCE loss, restoring best checkpoint weights upon termination.

---

## 5-Fold Grouped Cross-Validation Performance

Evaluated strictly across `artifacts/cv_split_manifest_v2.json` on training corpus ($N=348$):

| Metric | Candidate B (PyTorch NN) | Candidate A (Hybrid LogReg Baseline) |
|---|---|---|
| **Skills Macro F1** | **0.4408** | **0.6530** |
| **Skills Micro F1** | 0.4136 | 0.6324 |
| **Macro Precision** | 0.3522 | 0.6658 |
| **Macro Recall** | 0.7616 | 0.7497 |
| **Rare Class Recall** | 0.7616 | 0.7497 |

---

## Engineering Analysis & Findings

1. **High Recall, Low Precision**:
   Candidate B achieves high recall (0.7616) due to the effective `pos_weight` forcing sensitivity on rare classes. However, macro precision drops to 0.3522, generating substantial false positives.
2. **Sample Efficiency vs Model Capacity**:
   With only 348 total training examples and 3,072 input features, an over-parameterized neural network with ~800,000 parameters suffers from high variance compared to regularized $L_2$ logistic regression.
3. **Verdict**:
   Candidate B is verified as fully functional and methodologically compliant, but cannot supersede Candidate A under current dataset size constraints. It will serve as an ensemble candidate if calibrated and ensembled with sparse linear models.
