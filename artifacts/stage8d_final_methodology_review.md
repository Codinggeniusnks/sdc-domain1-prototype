# Stage 8D Artifact: Final Methodology & Statistical Review

**Reviewer Role**: Senior ML Research Architect, Statistical Reviewer & Competition Systems Architect  
**Review Scope**: Stage 8A (Gold Expansion), Stage 8B (Dataset v5 Construction & CV v3), and Stage 8C (Clean Model Screening)  
**Methodology Verdict**: **VALID WITH MINOR CAVEATS**  
**Holdout Status**: Protocol B (`data/splits/real_world_test_set.json`) = **SEALED (0 ACCESSES)** | Protocol C v2 (`data/splits/unseen_occupation_test_set_v2.json`) = **SEALED (0 ACCESSES)**  

---

## 1. Executive Summary

Stage 8C executed a disciplined, leakage-controlled model screening across **Dataset v5** ($N = 311$: 305 authoritative Gold records [98.07%] and 6 synthetic deficit-support records [1.93%], SHA-256: `9c59cc584167b3047e0d5f4177f205937e297da0605e99b369edfc738124032d`).

Following forensic inspection of the screening pipeline ([`scripts/stage8c_model_screening.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/stage8c_model_screening.py)) and its output artifacts, the Stage 8C methodology is classified as **VALID WITH MINOR CAVEATS** and is scientifically sound to support freezing a single primary model for one-shot evaluation on the sealed final holdouts.

---

## 2. Task 1 — Forensic Audit of Stage 8C Methodology

### 2.1. Grouped Cross-Validation Validity
- **Partition Structure**: [`artifacts/cv_split_manifest_v3.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/cv_split_manifest_v3.json) partitions the 311 records across 5 folds grouped strictly by 61 real MASCO/framework occupational clusters and 6 distinct synthetic template families (67 total clusters).
- **Leakage Verification**: $G_{\text{train}}^{(k)} \cap G_{\text{val}}^{(k)} = \emptyset$ across all 5 folds. Zero occupation-group leakage and zero synthetic-template leakage occurred.
- **Validation Support**: Every validation fold ($n \in [61, 64]$) contains at least 1 positive instance for all 16 skills, eliminating undefined ($0/0$) fold-level per-class F1 scores.

### 2.2. Preprocessing & Feature Isolation
- **Candidate A (Lexical/Subword TF-IDF)**: Within each fold loop, `FeatureUnion` (`word` + `char_wb` `TfidfVectorizer`) was instantiated fresh and fitted strictly on `train_texts` (`vec.fit_transform(train_texts)`), with `val_texts` transformed only (`vec.transform(val_texts)`). No validation vocabulary or IDF weights leaked into training.
- **Candidate C1 (Frozen MiniLM Bi-Encoder)**: `sentence-transformers/all-MiniLM-L6-v2` was used strictly as a frozen pretrained feature extractor with L2-normalized 384-dimensional embeddings (`normalize_embeddings=True`). The downstream `MultiLabelBinaryClassifier(LogisticRegression)` head was fitted strictly on each fold's training indices.

### 2.3. Ensemble & Threshold Selection Methodology (Caveats 1 & 2)
- **Ensemble Construction**: Probability-level linear blending ($w_A P_A + w_{C1} P_{C1}$) was performed strictly on out-of-fold validation probability matrices.
  - *Minor Caveat 1 (Weight Standardization)*: In [`scripts/stage8c_model_screening.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/stage8c_model_screening.py), `best_a_id` was automatically selected by argmax at threshold 0.35 (`A_base_C2.5_W1.5`, Macro F1 = 0.6169 vs `A_base_C2.5_W1.0`, Macro F1 = 0.6157, $\Delta = 0.0012$). To enforce parsimony and eliminate unnecessary hyperparameter degrees of freedom, the frozen primary Hybrid model standardizes both Component A and Component C1 to uniform sample weighting ($W_{\text{gold}} = 1.0$).
  - *Minor Caveat 2 (Pooled OOF Threshold Selection)*: The single evaluation threshold ($\theta = 0.375$) was selected via a bounded grid search ($0.20$ to $0.50$) on pooled OOF probabilities rather than an inner nested CV loop. However, the improvement from the pre-specified default threshold ($\theta = 0.350 \rightarrow \text{Macro F1} = 0.6407$) to $\theta = 0.375$ ($\text{Macro F1} = 0.6434$) is only $+0.0027$, and architectural rankings are strictly invariant across the entire threshold range $[0.30, 0.425]$. Freezing $\theta = 0.375$ prior to opening the final holdouts is completely leakage-safe with respect to Protocols B and C v2.

### 2.4. Calibration Removal Verification
- Stage 8C tested leakage-safe 3-fold inner sigmoid (Platt) calibration (`CalibratedClassifierCV(method="sigmoid", cv=3)`) inside each training fold.
- While Platt scaling reduced pooled ECE from $0.0654$ to $0.0134$, it compressed output scores toward empirical class priors ($9.6\%$–$31.8\%$), reducing Grouped-CV Macro F1 from $0.6169$ to $0.5786$ ($-0.0383$). Removing post-hoc Platt calibration and using raw logistic confidence scores with `class_weight='balanced'` is empirically and theoretically justified.

---

## 3. Task 4 — Scientific Assessment of the Hybrid Gain

| Metric (Grouped 5-Fold CV) | Candidate A (`A_base_C2.5_W1.0`, $\theta=0.375$) | Candidate C1 (`C1_MiniLM_C3.0_W1.0`, $\theta=0.375$) | Hybrid H (`0.70 A + 0.30 C1`, $\theta=0.375$) | Hybrid vs Candidate A ($\Delta$) |
| :--- | :---: | :---: | :---: | :---: |
| **Skills Macro F1** | 0.6248 | 0.5982 | **0.6434** | **+0.0186** |
| **Skills Micro F1** | 0.6202 | 0.5824 | **0.6357** | **+0.0155** |
| **Macro Precision** | 0.5992 | 0.4912 | **0.6039** | **+0.0047** |
| **Macro Recall** | 0.6650 | **0.7842** | **0.7028** | **+0.0378** |
| **Rare-Class Recall** | 0.5912 | **0.7479** | **0.6313** | **+0.0401** |
| **Fold Standard Deviation** | 0.1100 | 0.1139 | **0.1061** | **-0.0039** |
| **Core Tier Precision ($\ge 0.45$)** | 0.6474 | 0.5647 | **0.6524** | **+0.0050** |
| **Suggested Tier Missed-Skill Recovery** | 50.15% | 63.04% | **61.67%** | **+11.52 pp** |

### Conservative Scientific Evaluation:
1. **Magnitude of Gain**: An absolute gain of $+0.0186$ in Macro F1 and $+0.0401$ in Rare-Class Recall across grouped cross-validation is **moderate and practically meaningful**, though not a dramatic order-of-magnitude leap.
2. **Mechanism of Complementarity**: Across $4,976$ binary prediction decisions, Candidate A and Candidate C1 disagreed on $772$ instances ($15.51\%$). Candidate C1 correctly recovered $286$ instances where Candidate A failed ($5.75\%$ of all decisions; $42.75\%$ of Candidate A's total errors), while the $0.70 / 0.30$ weighting prevented Candidate C1's lower precision ($0.4912$ standalone) from degrading overall precision ($0.6039$ in Hybrid vs $0.5992$ in Candidate A).
3. **Human-in-the-Loop Utility**: In the product's Suggested skill tier ($0.25 \le P < 0.45$), the Hybrid model recovers $61.67\%$ of skills missed by the Core threshold (177 instances vs 164 for Candidate A), directly improving recall for implicit and paraphrased user inputs at a cost of only $0.33$ additional false suggestions per profile ($2.28$ vs $1.95$).
4. **Cost-Benefit Conclusion**: Because the $91.5\text{ MB}$ MiniLM model runs locally on CPU in $\sim 16\text{ ms}$ mean latency ($25.2\text{ ms}$ p95) without requiring GPU infrastructure, the operational cost is well within competition and production tolerances.

---

## 4. Tasks 5 & 6 — Per-Class Generalisation Balance & Weak-Class Audit

### 4.1. Full 16-Class Performance Profile (Grouped CV on Dataset v5, $\theta = 0.375$)

| Skill Class | v5 Total Support | Fold Val Support `[F0, F1, F2, F3, F4]` | Cand A F1 | Cand C1 F1 | Hybrid H F1 | Hybrid Prec | Hybrid Rec | Diagnostic Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `rag_knowledge_systems` | 31 | `[3, 19, 2, 5, 2]` | 0.9333 | 0.8657 | **0.9333** | 0.9655 | 0.9032 | Strong (Distinctive technical terms) |
| `esg_sustainability_reporting` | 43 | `[11, 3, 3, 17, 9]` | 0.8864 | 0.8261 | **0.9070** | 0.9070 | 0.9070 | Strong (Distinctive statutory terms) |
| `carbon_footprint_analytics` | 31 | `[8, 1, 4, 15, 3]` | 0.8254 | 0.8108 | **0.8485** | 0.8000 | 0.9032 | Strong (GHG / Scope 1-3 vocabulary) |
| `prompt_engineering` | 31 | `[5, 19, 5, 1, 1]` | 0.8475 | 0.7200 | **0.8254** | 0.8125 | 0.8387 | Strong |
| `data_privacy_pdpa` | 44 | `[10, 8, 8, 11, 7]` | 0.7912 | 0.6852 | **0.7872** | 0.7400 | 0.8409 | Strong (Well-balanced across folds) |
| `python_scripting` | 63 | `[12, 20, 9, 17, 5]` | 0.6993 | 0.7324 | **0.7143** | 0.6494 | 0.7937 | Solid |
| `process_mapping` | 99 | `[17, 19, 27, 17, 19]` | 0.6538 | 0.6270 | **0.7009** | 0.6522 | 0.7576 | Solid (Broad occupational support) |
| `workflow_automation` | 67 | `[20, 12, 16, 16, 3]` | 0.6623 | 0.5876 | **0.6842** | 0.5977 | 0.8000 | Solid |
| `ai_literacy` | 38 | `[4, 16, 11, 5, 2]` | 0.6575 | 0.5843 | **0.6667** | 0.6757 | 0.6579 | Solid |
| `api_integration` | 42 | `[11, 12, 2, 16, 1]` | 0.5745 | 0.6471 | **0.6596** | 0.5962 | 0.7381 | Solid (MiniLM boosts recall) |
| `stakeholder_communication` | 98 | `[25, 19, 19, 16, 19]` | 0.5490 | 0.5891 | **0.5670** | 0.4540 | 0.7551 | Moderate (High recall, broad usage) |
| `human_in_the_loop_qa` | 59 | `[5, 25, 11, 9, 9]` | 0.5692 | 0.5444 | **0.5655** | 0.4767 | 0.6949 | Moderate |
| `sql_data_analysis` | 62 | `[21, 5, 11, 17, 8]` | 0.5417 | 0.5376 | **0.5263** | 0.4444 | 0.6452 | Moderate (Overlap with general analytics) |
| `ai_ethics_governance` | 30 | `[5, 5, 2, 10, 8]` | 0.4688 | 0.3462 | **0.4058** | 0.3590 | 0.4667 | Weak-Moderate (Overlap with PDPA/QA) |
| `data_visualization` | 42 | `[11, 3, 12, 12, 4]` | 0.2745 | 0.3026 | **0.2936** | 0.2388 | 0.3810 | Weak (Implicit narrative phrasing) |
| `instructional_design` | 31 | `[1, 1, 26, 1, 2]` | 0.0909 | 0.3636 | **0.2083** | 0.2941 | 0.1613 | Weak in OOF (Cluster-starved in Fold 2) |

### 4.2. Root-Cause Diagnosis of Weak Classes (Caveat 3)
1. **Why `instructional_design` had low OOF F1 ($0.2083$)**:
   - Inspecting [`artifacts/cv_split_manifest_v3.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/cv_split_manifest_v3.json) reveals that **26 of the 31 positive instances ($83.9\%$)** of `instructional_design` reside in Fold 2 validation (driven by occupational cluster `MASCO 2424` — *Training and Staff Development Professionals*).
   - Because Grouped CV strictly forbids splitting `MASCO 2424` across train and validation, the model trained in Fold 2 saw **only 5 positive examples** of `instructional_design` in its training split (`31 - 26 = 5`) and had to predict 26 unseen specialist records!
   - Crucially, when the frozen model is fitted on **100% of Dataset v5** ($N = 311$) for final holdout evaluation, it trains on **all 31 positive examples** (including all `MASCO 2424` records). Furthermore, Candidate C1 achieved $0.3636$ F1 vs Candidate A's $0.0909$ on this exact bottleneck, confirming that retaining MiniLM in the Hybrid ensemble directly mitigates out-of-group pedagogical phrasing.
2. **Why `data_visualization` had low OOF F1 ($0.2936$)**:
   - Unlike synthetic Dataset v4 records that repeated literal phrases ("build data visualizations"), authoritative Gold records describe visualization implicitly inside broader analytical duties ("present executive KPI scorecards", "publish operational dashboards", "communicate financial trends"). This causes false positives/negatives at the boundary with `sql_data_analysis` and `stakeholder_communication`.
3. **Why high-scoring classes (`rag_knowledge_systems` = $0.9333$, `esg_sustainability_reporting` = $0.9070$) are legitimate**:
   - These classes are anchored by unambiguous domain terminology in real regulatory and technical standards (e.g., "retrieval-augmented", "vector embeddings", "Scope 1, 2, and 3 emissions", "Bursa Malaysia sustainability disclosures").

### 4.3. Acceptance Decision on Weak Classes
- **Verdict**: **B — ACCEPTABLE WITH DOCUMENTED LIMITATIONS (NON-BLOCKING)**.
- Twelve of the 16 classes achieve F1 between $0.56$ and $0.93$, and the two weakest classes have clear, localized explanations (fold-level cluster starvation in Grouped CV for `instructional_design`, and narrative boundary overlap for `data_visualization`). Moreover, the dual-threshold human-in-the-loop interface ($0.25 \le P < 0.45$) is specifically architected to surface medium-confidence predictions for user confirmation.

---

## 5. Task 10, 11 & 12 — Architectural & Governance Boundaries

### 5.1. Multilingual Limitation (Task 10)
- **Status**: **DEFERRED (NON-BLOCKING FOR CURRENT ENGLISH FREEZE)**.
- `sentence-transformers/all-MiniLM-L6-v2` and English stop-word TF-IDF are optimized for English occupational texts, which matches 100% of Dataset v5 and the preliminary competition evaluation splits.
- Support for Bahasa Malaysia (e.g., JPK NOSS / MASCO Malay titles) and Chinese is documented as a scheduled Phase 2 architectural upgrade (swapping the frozen encoder to `paraphrase-multilingual-MiniLM-L12-v2` and language-agnostic character n-grams) and does not block the current English model freeze.

### 5.2. Fairness, Transparency & User Agency Boundary (Task 11)
- **Demographic Blindness**: The frozen M1 pipeline takes *only* occupational task/experience text as input. Age, gender, ethnicity, nationality, educational institution prestige, and socioeconomic background are never used as features.
- **Human-in-the-Loop Agency**: Inferred probabilities are raw model confidence scores, never unquestionable facts. The product interface separates skills into **Core ($\ge 0.45$)** and **Suggested ($[0.25, 0.45)$)** tiers, allowing users to one-click confirm, add, or remove any skill before role matching or pathway generation.

### 5.3. Static Demand Model Status (Task 12)
- **Status**: **LEGACY / DIAGNOSTIC ONLY**.
- Any static binary `is_emerging_demand` head in legacy scripts is strictly excluded from the M1 skills-extraction promotion gate. Dynamic labour-market demand, AI disruption exposure, and role trajectories belong exclusively to the **M2 Trend Intelligence Engine**.
