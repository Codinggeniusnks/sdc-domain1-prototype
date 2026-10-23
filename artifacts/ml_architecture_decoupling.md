# ML Architecture Decoupling: Modular Multi-Task Decomposition

## Executive Summary
In early iterations of Domain 1, skills extraction (16-class multi-label tagging) and emerging demand prediction (binary classification) were tightly coupled into an ad-hoc monolithic pipeline.

The independent forensic audit (`artifacts/opus_v4_independent_audit.md`) noted that while multi-task joint modeling is conceptually appealing, coupling these two tasks into a shared representation without independent calibration and thresholding created severe architectural entanglements and obscured diagnostic attribution.

This document formalizes the **decoupling of the Domain 1 ML architecture** into modular, independently testable, and independently retrainable sub-systems.

---

## Modular Component Architecture

```
                    Raw Input Text (CV, Bio, Task Profile)
                                      │
                     ┌────────────────┴────────────────┐
                     ▼                                 ▼
         [Skills Extraction Engine]       [Emerging Demand Engine]
                     │                                 │
                     ▼                                 ▼
           Text Feature Extractor            Text Feature Extractor
         (Hybrid Word + Subword)           (Domain TF-IDF / Bigram)
                     │                                 │
                     ▼                                 ▼
          Binary Relevance Heads               Logistic Regressor
           (16 Regularized Clfs)             (Balanced Class Weights)
                     │                                 │
                     ▼                                 ▼
            Thresholding Engine              Confidence Calibrator
           (Per-Class / Global tau)          (Direct Sigmoid Odds)
                     │                                 │
                     ▼                                 ▼
           Extracted Skills Set            Emerging Demand Probability
          ['prompt_eng', 'pdpa']             P(Demand=1) in [0.0, 1.0]
                     │                                 │
                     └────────────────┬────────────────┘
                                      ▼
                       [Downstream Compass Recommender]
                          (matcher.py / signals.py)
```

---

## Architectural Separation Guarantees

1. **Independent Loss Formulations**:
   - Skills Extraction optimizes multi-label cross-entropy over $K=16$ non-mutually-exclusive binary tasks:
     $$\mathcal{L}_{\text{skills}} = -\sum_{j=1}^{16} \left[ y_j \log \sigma(z_j) + (1 - y_j) \log (1 - \sigma(z_j)) \right]$$
   - Demand Prediction optimizes binary cross-entropy:
     $$\mathcal{L}_{\text{demand}} = -\left[ y \log \sigma(z_d) + (1 - y) \log (1 - \sigma(z_d)) \right]$$

2. **Decoupled Hyperparameters**:
   - Skills extraction features require fine-grained morphological character n-grams (`char_wb`, $3-5$) to capture acronyms (`pdpa`, `rag`) and compound words (`prompt_engineering`).
   - Demand prediction focuses on macroeconomic indicators, industry shifts, and adoption verbs, benefiting from standard word n-grams ($1-2$) with higher regularization ($C=1.5$).

3. **Isolated Lifecycle & Versioning**:
   - Model artifacts are serialized into separate decoupled files:
     - `models/skills_extractor_v4.joblib`
     - `models/demand_predictor_v4.joblib`
   - Updating the skills taxonomy or retraining skills heads does not risk altering demand calibration curves or vice versa.

4. **Inference Pipeline Integration**:
   - The application layer (`src/main.py`) interacts with both models through unified, decoupled interface adapters:
     ```python
     skills = skills_engine.predict(text, threshold=0.35)
     demand_prob = demand_engine.predict_proba(text)
     ```
   - In the event of an isolated failure in the demand engine, the skills extractor continues serving predictions with graceful degradation to fallback market signals.
