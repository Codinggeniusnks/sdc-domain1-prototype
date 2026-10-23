# Stage 8D Artifact: Final Model Freeze Decision

**Decision Authority**: Senior ML Research Architect & Competition Systems Architect  
**Status**: **APPROVED FOR ONE-SHOT FREEZE**  
**Holdout Access Count**: **0 (Protocol B and Protocol C v2 remain SEALED)**  

---

## 1. Primary Model Selection (Task 2)

- **Selected Primary Architecture**: **B — Hybrid Ensemble (`H_blend_0.70A_0.30C1_W1.0`)**
- **Single-Candidate Rule**: This Hybrid Ensemble is the **ONLY** model permitted to be evaluated on the sealed final holdouts (**Protocol B**: `data/splits/real_world_test_set.json` and **Protocol C v2**: `data/splits/unseen_occupation_test_set_v2.json`).

### Justification for Selecting Hybrid H over Standalone Candidate A:
1. **Superior Grouped-CV Generalization**: Improves Grouped 5-Fold Macro F1 from $0.6248$ to **$0.6434$ ($+0.0186$)** and Micro F1 from $0.6202$ to **$0.6357$ ($+0.0155$)**.
2. **Rare-Class & Semantic Recovery**: Improves Rare-Class Recall from $0.5912$ to **$0.6313$ ($+0.0401$)** and recovers $286$ out-of-fold skill instances missed by lexical TF-IDF ($42.75\%$ error recovery on paraphrased, implicit, and pedagogical expressions).
3. **Cross-Occupation Fold Stability**: Achieves the lowest fold standard deviation ($\text{SD} = 0.1061$ vs $0.1100$ for Candidate A), which is directly relevant to **Protocol C v2 (Unseen Occupations)**.
4. **Operational Feasibility**: Executes locally on CPU in $\sim 16.0\text{ ms}$ mean latency ($25.2\text{ ms}$ p95) with a $95.7\text{ MB}$ footprint, requiring zero cloud GPU infrastructure.

---

## 2. Exact Frozen Specification of the Primary Candidate

### 2.1. Training Corpus Freeze
- **Dataset Path**: [`data/processed/dataset_v5_clean_multisource.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/processed/dataset_v5_clean_multisource.json)
- **Frozen SHA-256**: `9c59cc584167b3047e0d5f4177f205937e297da0605e99b369edfc738124032d`
- **Records**: $N = 311$ (305 Gold + 6 Synthetic; zero physical duplication)
- **Target Taxonomy**: Frozen 16-skill vector (`TAXONOMY_SKILLS` in canonical order)

### 2.2. Component A — Lexical & Subword TF-IDF Branch (`weight = 0.70`)
- **Feature Pipeline (`FeatureUnion`)**:
  - `word`: `TfidfVectorizer(ngram_range=(1, 3), max_features=2048, min_df=1, sublinear_tf=True, stop_words="english")`
  - `subword`: `TfidfVectorizer(ngram_range=(3, 5), analyzer="char_wb", max_features=1024, min_df=2, sublinear_tf=True)`
- **Classifier Head**: `MultiLabelBinaryClassifier` wrapping 16 independent `LogisticRegression(C=2.5, class_weight="balanced", max_iter=1000, solver="liblinear", random_state=42)` estimators.
- **Sample Weighting**: Uniform (`sample_weight = 1.0` for all 311 records).

### 2.3. Component C1 — Frozen Pretrained Semantic Branch (`weight = 0.30`)
- **Feature Extractor**: Frozen `sentence-transformers/all-MiniLM-L6-v2` (`384` dimensions, `normalize_embeddings=True`, zero fine-tuning).
- **Classifier Head**: `MultiLabelBinaryClassifier` wrapping 16 independent `LogisticRegression(C=3.0, class_weight="balanced", max_iter=1000, solver="liblinear", random_state=42)` estimators.
- **Sample Weighting**: Uniform (`sample_weight = 1.0` for all 311 records).

### 2.4. Probability Combination Rule
For every document $x$ and skill $j \in \{1, \dots, 16\}$:
$$S_{\text{Hybrid}}(x, j) = 0.70 \cdot P_A(y_j = 1 \mid x) + 0.30 \cdot P_{C1}(y_j = 1 \mid x)$$

---

## 3. Compact Fallback Decision (Task 3)

- **Decision**: **KEEP FALLBACK (`A_base_C2.5_W1.0`)**
- **Role & Scope**: Component A (`4.2 MB` disk, `1.2 ms` latency, zero PyTorch/Transformer dependency) may be saved alongside the primary model as an operational fallback for ultra-constrained environments or degraded-mode fast previews.
- **Strict Holdout Prohibition**: To prevent multiple-hypothesis testing and post-hoc model selection leakage, the Compact Fallback **MUST NOT** be evaluated on Protocol B or Protocol C v2 as a competing candidate. The final holdout evaluation is strictly a one-shot test of the Primary Hybrid H model.

---

## 4. Threshold, Calibration & Weighting Freeze (Tasks 7, 8 & 9)

### 4.1. Threshold Freeze (Task 7)
1. **Frozen Model Evaluation Threshold (Protocol B & Protocol C v2)**:
   $$\theta_{\text{eval}} = \mathbf{0.375}$$
   All binary predictions $\hat{y}_{i,j} = \mathbb{I}(S_{\text{Hybrid}}(x_i, j) \ge 0.375)$ for primary holdout metrics (Macro F1, Micro F1, Precision, Recall, Rare-Class Recall) must be computed strictly at $\theta_{\text{eval}} = 0.375$.
2. **Frozen Product Display Thresholds (Human-in-the-Loop UI)**:
   - **CORE SKILL (Auto-Recognized)**: $S_{\text{Hybrid}} \ge \mathbf{0.450}$
   - **SUGGESTED SKILL (User-Confirmable)**: $\mathbf{0.250} \le S_{\text{Hybrid}} < \mathbf{0.450}$
   - **SUPPRESSED / NOISE**: $S_{\text{Hybrid}} < \mathbf{0.250}$
   *(Neither $\theta_{\text{eval}}$ nor the product display thresholds may be modified after viewing holdout results).*

### 4.2. Calibration Decision (Task 8)
- **Decision**: **RAW PROBABILITIES (UNCALIBRATED)**
- **Mandatory Interpretation Rule**: Because `class_weight="balanced"` reweights positive instances inversely to class frequency and post-hoc Platt scaling is omitted (having degraded CV Macro F1 by $-0.0383$), the outputs $S_{\text{Hybrid}}(x, j) \in [0, 1]$ are **uncalibrated model confidence scores** optimized for F1 ranking and thresholding, **not** calibrated frequentist empirical probabilities. All downstream UI tooltips and technical documentation must refer to them as *Model Confidence Scores*.

### 4.3. Sample Weighting Freeze (Task 9)
- **Decision**: **GOLD WEIGHT = 1.0 (Uniform Weighting)**
- **Rationale**: Dataset v5 is already $98.07\%$ real Gold data. Upweighting Gold to $1.5$ yielded a negligible $+0.0012$ difference in Candidate A CV Macro F1 ($0.6169$ vs $0.6157$). Uniform weighting ($W_{\text{gold}} = 1.0, W_{\text{synth}} = 1.0$) is frozen for mathematical simplicity.
