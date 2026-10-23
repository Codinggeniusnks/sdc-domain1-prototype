# Candidate C Implementation: Pretrained Sentence-Transformers Bi-Encoder

## Executive Summary
In the previous RunPod execution, Candidate C was falsely documented as utilizing `all-MiniLM-L6-v2`, when forensic code analysis revealed it was actually executing `TruncatedSVD(n_components=64)` over TF-IDF matrices.

In this remediation, we replaced the fake SVD substitution with a genuine, production-grade integration of **`sentence-transformers/all-MiniLM-L6-v2`** (384-dimensional dense semantic representations). We implemented and evaluated two classification heads:
1. **Candidate C1**: Frozen MiniLM Embeddings + Balanced Logistic Regression (`sample_weight=3.0` for Gold).
2. **Candidate C2**: Frozen MiniLM Embeddings + PyTorch 2-Layer MLP Head with `BCEWithLogitsLoss`.

---

## Bi-Encoder Architecture & Verification

- **Backbone**: `sentence-transformers/all-MiniLM-L6-v2`
- **Parameter Count**: 22.7M parameters
- **Output Dimensionality**: 384 dimensions, $L_2$ normalized
- **Device Support**: CPU / CUDA compatible with deterministic caching to `data/cache/minilm_<hash>.joblib` to optimize local developer iteration speed.

### Verified in `tests/test_remediation.py`:
- Test `test_08_minilm_loads_and_encodes_384_dim` explicitly verifies model instantiation, forward encoding pass, 384-dim tensor output, and unit vector normalization ($\|v\|_2 \approx 1.0$).

---

## Comparative Experimental Setup

```
[Job / Task Text]
       │
       ▼
[all-MiniLM-L6-v2 Bi-Encoder]
       │
       ▼
[384-dim Dense Vector]
       ├─────────────────────────────────────────┐
       ▼                                         ▼
Candidate C1 (Linear Head)             Candidate C2 (MLP Head)
OneVsRest LogisticRegression           PyTorch nn.Sequential:
C=2.0, class_weight='balanced'         Linear(384->256) -> LayerNorm -> ReLU
sample_weight applied directly         -> Dropout(0.3) -> Linear(256->128)
                                       -> Dropout(0.2) -> Linear(128->16)
```

---

## 5-Fold Grouped Cross-Validation Benchmark

Evaluated on `artifacts/cv_split_manifest_v2.json` ($N=348$):

| Metric | Candidate A (Hybrid TF-IDF) | Candidate C1 (MiniLM + Linear) | Candidate C2 (MiniLM + MLP) |
|---|---|---|---|
| **Skills Macro F1** | **0.6530** | 0.5023 | 0.3899 |
| **Skills Micro F1** | **0.6324** | 0.4739 | 0.3739 |
| **Macro Precision** | **0.6658** | 0.4172 | 0.2835 |
| **Macro Recall** | 0.7497 | **0.7692** | **0.7789** |
| **Rare Class Recall** | 0.7497 | 0.7692 | 0.7789 |

---

## Scientific Analysis & Findings

1. **Why Dense Bi-Encoders Lag Sparse TF-IDF on this Specific Task**:
   - `all-MiniLM-L6-v2` is pretrained on generic semantic sentence similarity (MS-MARCO, SNLI, etc.). It projects texts into high-level conceptual spaces (e.g. "software development", "leadership").
   - Domain 1 taxonomy skills are fine-grained, technical lexical tokens (e.g. `data_privacy_pdpa`, `rag_knowledge_systems`, `sql_data_analysis`, `carbon_footprint_analytics`).
   - A generic sentence embedding clusters "data privacy" and "cloud computing" relatively close together, leading to high recall (76.92%) but low precision (41.72%) because subtle technical distinctions are blurred.
   - In contrast, Candidate A's subword + word n-gram features (1 to 3 words, 3 to 5 character n-grams) explicitly match exact keywords and morphology, yielding 66.58% precision.

2. **Linear Head (C1) vs MLP Head (C2)**:
   - The linear head (C1) achieved 0.5023 Macro F1, heavily outperforming the MLP head (0.3899).
   - This aligns with statistical learning theory: with $N=348$ observations in 384 dimensions, non-linear deep heads overfit representation artifacts, while regularized linear hyperplanes preserve maximum margin.

3. **Strategic Recommendation**:
   - Keep Candidate A as the primary inference backbone for single-model screening.
   - Use MiniLM embeddings in hybrid feature fusion (concatenating sparse TF-IDF with dense MiniLM vectors) or in a late-fusion ensemble in future phases once training data expands to $>1,000$ real examples.
