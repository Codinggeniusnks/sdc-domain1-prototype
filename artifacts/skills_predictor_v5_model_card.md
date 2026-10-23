# Model Card: M1 Skills Extraction Engine (v5.0-hybrid-frozen)

## Model Details
- **Model Name**: M1 Skills Predictor (Domain 1 Prototype)
- **Model Version**: `5.0-hybrid-frozen`
- **Release Date**: 2026-10-23
- **Model Architecture**: Probability-Level Hybrid Ensemble (`H_blend_0.70A_0.30C1_W1.0`)
  - **Branch A (70%)**: Lexical & Subword FeatureUnion (Word n-grams 1–3, max 2048; Char_wb n-grams 3–5, max 1024) + One-vs-Rest Logistic Regression ($C=2.5$, `class_weight='balanced'`).
  - **Branch C1 (30%)**: Dense Pretrained Semantic Encoder (`sentence-transformers/all-MiniLM-L6-v2`, 384-d L2-normalized embeddings, frozen) + One-vs-Rest Logistic Regression ($C=3.0$, `class_weight='balanced'`).
- **Ensemble Combination**: $P_{\text{final}} = 0.70 \cdot P_A + 0.30 \cdot P_{C1}$ (uncalibrated model confidence scores).
- **Evaluation Decision Threshold**: $\theta_{\text{eval}} = \mathbf{0.375}$
- **Product Display Thresholds**:
  - **Core Tier**: $\ge \mathbf{0.450}$ (Auto-populated with high precision)
  - **Suggested Tier**: $[\mathbf{0.250}, \mathbf{0.450})$ (Interactive user-confirmable chips)
  - **Suppressed Noise**: $< \mathbf{0.250}$ (Hidden from UI)
- **Model Artifact Hashes**:
  - `candidate_a.joblib`: `43f01ab7107cd7be484c17d23e8d1312ad902dbf21017584681e95d56d13d759`
  - `candidate_c1_head.joblib`: `b0ab7a9de28ab7a8f25272a77fa40ed12cc68b9b37fe9986e8e198de202c6c6c`
  - `ensemble_config.json`: `70b9a8be5075d6f49a4529e6f4bdc9ccdbe7b8bd3fe8624684c9df651ed7f6f8`
  - Bundle Composite SHA-256: `13fb05838e923dc8d008173ba9c719a4929b6ba3c4b8f064777dff6a2eef19b3`

---

## Intended Use
- **Primary Use**: Assistive multi-label skill extraction from worker task narratives, job experience summaries, and curriculum vitae to populate profile skill inventories.
- **Downstream Integration**: Feeds verified skill profiles into the future M2 Trend Intelligence Engine and M3 Personalised Reskilling Pathway Recommender.
- **Human-in-the-Loop Mode**: Designed strictly as a decision-support and assistive profiling tool. Suggested skills must always be confirmable, editable, or dismissible by the worker.

## Out-of-Scope & Prohibited Uses
- **Autonomous Employment Decisions**: Must NOT be used as an automated filter to reject job candidates, terminate employment, or determine compensation.
- **High-Stakes Legal/Licensing Certification**: Inferred skills are self-reported task signals, not certified statutory credentials.
- **Surveillance & Productivity Tracking**: Must NOT be used to monitor or score real-time workplace activity.

---

## Training Data & Methodology
- **Training Corpus**: [`data/processed/dataset_v5_clean_multisource.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/processed/dataset_v5_clean_multisource.json)
- **Dataset Hash (SHA-256)**: `9c59cc584167b3047e0d5f4177f205937e297da0605e99b369edfc738124032d`
- **Volume**: $N = 311$ unique records (zero duplicate rows).
- **Composition**: **305 Authoritative Gold Records (98.07%)** across 14 institutional sources (TalentCorp MyCOL 2024/2025, MASCO 2020, MDEC/MOSTI AI Standards, JPK TVET, Bursa Malaysia ESG, JPDP Act 709, Bank Negara Malaysia, ESCO v1.1/v1.2 crosswalks) and **6 Approved Synthetic Records (1.93%)** selected to satisfy residual class deficit targets with confirmed semantic dissimilarity ($\le 0.4590$ cosine similarity to Gold).
- **Sample Weighting**: Uniform ($W = 1.0$ for all records).

---

## Evaluation Results & Benchmarks

### 1. Protocol B: Real-World Generalization Holdout ($N = 63$)
- **Skills Macro F1**: **0.6703** [95% Bootstrap CI: `0.4855`, `0.7231`]
- **Skills Micro F1**: **0.6090** [95% Bootstrap CI: `0.5129`, `0.6938`]
- **Macro Precision**: **0.6112** | **Macro Recall**: **0.8029**
- **Rare-Class Recall**: **0.8375**
- **Core Tier Precision ($\ge 0.45$)**: **71.28%** | **Core Tier Recall**: **71.65%**
- **Suggested Tier Recovery Rate**: Recovers **59.09%** of true skills missed by Core tier.

### 2. Protocol C v2: Unseen-Occupation Generalization Holdout ($N = 25$)
- **Skills Macro F1**: **0.7443** [95% Bootstrap CI: `0.6130`, `0.7866`]
- **Skills Micro F1**: **0.7897** [95% Bootstrap CI: `0.7549`, `0.8272`]
- **Macro Precision**: **0.6792** | **Macro Recall**: **0.8509**
- **Rare-Class Recall**: **0.9000**
- **Core Tier Precision ($\ge 0.45$)**: **73.61%** | **Core Tier Recall**: **78.79%**
- **Suggested Tier Recovery Rate**: Recovers **61.54%** of true skills missed by Core tier.

---

## Known Limitations & Failure Modes
1. **Implicit Data Visualization Phrasing**: `data_visualization` achieved F1 = 0.4800 on Protocol B due to workplace descriptions embedding reporting tasks implicitly (*"compile monthly KPI decks"*).
2. **English Language Scope**: Pretrained on `all-MiniLM-L6-v2` and English TF-IDF. Malay and Chinese occupational titles require dedicated multilingual encoder integration (Phase 2 roadmap).
3. **Soft Skill Bleed**: Broad interpersonal phrases occasionally trigger `stakeholder_communication` false positives (Precision = 0.3000), which are mitigated in UI by requiring user confirmation for non-core scores.
4. **Static Demand Exclusion**: The legacy static binary demand classifier is completely removed from M1. Dynamic skill and role demand forecasting is delegated exclusively to the M2 Trend Intelligence Engine.

---

## Ethical & Governance Safeguards
- **Demographic Blindness**: The model does not ingest age, gender, race, religion, geographic location, or institutional affiliation.
- **Uncalibrated Confidence Disclosure**: Probability outputs are model ranking scores, not empirical likelihoods.
- **User Agency**: The worker maintains 100% control over their profile and can override any AI recommendation.
