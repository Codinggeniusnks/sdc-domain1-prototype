# Competition Role Assessment: AI Skills & Demand Predictor v4

**Auditor**: Competition Technical Judge & Systems Architect  
**Date**: October 22, 2026  
**Context**: Domain 1 Architecture Integration for Malaysian Workforce AI Resilience

---

## 1. Architectural Scope & Component Boundary

In the end-to-end competition system, the machine learning suite spans multiple coordinated modules:
- **`M1`: Skills Profile Intake & Multi-Label Extractor** (Processes CVs, job text, competency descriptors into 16 Domain 1 skills).
- **`M2`: AI Trend Signal Layer** (Dynamic ingestion of AI advancement, generative automation exposure, and patent/literature trends).
- **`M3`: Future Role Matching & Gap Analysis** (Vector/semantic similarity crosswalk to emerging Malaysian occupations).
- **`M4`: Personalised Reskilling Engine** (Stepwise transition pathways, modular course sequences, time-to-proficiency).
- **`M5`: SDG Impact Mapping** (Quantifiable alignment with SDG 8: Decent Work and SDG 4: Quality Education).
- **`M6`: Scenario & Uncertainty Engine** (Monte Carlo sensitivity under varying economic/regulatory scenarios).

### The Role of the Evaluated Model
The trained candidate model ([`model.joblib`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/runpod/models/skills_predictor_v4_candidate/model.joblib)) is strictly a **text-to-label statistical extractor for Module M1**.

It was built as a dual-head model:
1. Multi-label skill classifier (16 outputs).
2. Binary static demand classifier (`is_emerging_demand`).

---

## 2. The Architectural Failure of the Static Demand Head

The empirical results demonstrate that coupling `Demand` classification to the `M1` TF-IDF text extractor is an architectural anti-pattern:
1. **Low Cross-Occupation Generalisation**: On unseen occupation families (Protocol C), Demand Macro F1 drops to **0.5098** with an AUC of **0.6200** (scarcely better than a coin toss).
2. **Static Label Flaw**: Job descriptions describe current task responsibilities, not future macroeconomic trajectory. A static text classifier cannot anticipate external AI model releases or policy changes (e.g., National Energy Transition Roadmap NETR, Bursa Malaysia ESG mandates).
3. **Competition Requirement**: The competition specification explicitly demands that future role outlook be driven by **`M2` (AI trend signals)**, not a static binary label on CV text.

### Architectural Recommendation
**Decouple Demand from the M1 Text Extractor entirely**:
- Retain `M1` as a pure, high-precision skill extractor.
- Delegate demand forecasting, displacement vulnerability, and emergence scoring to `M2`, which fuses external indicators (TalentCorp Critical Occupations List MyCOL, wage trends, MDEC digital adoption indices).

---

## 3. Top 5 Improvement Opportunities Ranked by Expected Value

Based on the quantitative error audit ([`artifacts/error_analysis_v4.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/error_analysis_v4.json)):

1. **Targeted Real GOLD Malaysian Data Expansion for Zero/Low-Support Classes (Expected Impact: +0.06 to +0.08 Macro F1)**:
   In the 98 GOLD training records, classes like `data_privacy_pdpa`, `carbon_footprint_analytics`, and `instructional_design` have 0 to 2 examples, causing the classifier to depend entirely on synthetic priors. Sourcing 30–50 real job descriptions from JobStreet Malaysia and MyFutureJobs targeting these sectors will eliminate this bottleneck.

2. **True Pretrained Semantic Encoders (MiniLM / BGE-Small) (Expected Impact: +0.04 to +0.06 Macro F1)**:
   Candidate C was compromised by using TruncatedSVD. Pretrained transformer encoders with domain fine-tuning will resolve the 58 `semantic_ambiguity` errors where keyword overlap is low but conceptual meaning is identical.

3. **Tuned Threshold Policy (Expected Impact: +0.03 to +0.05 Macro F1)**:
   The current threshold of $\tau = 0.42$ yields 83.2% precision but only 68.8% recall (46 false negatives vs 35 false positives). Training-side out-of-fold curves indicate that lowering thresholds to $\tau \in [0.32, 0.36]$ for minority classes unlocks substantial recall without precision collapse.

4. **Decoupling Demand Modeling into an External Signal Pipeline (Expected Impact: Resolves Demand Gate)**:
   Removing the failing calibrated demand head from M1 and replacing it with an explicit rule/index crosswalk to MyCOL 2024/2025 and Malaysia's AI Roadmap ensures valid, explainable demand metrics.

5. **Fixing the Grouped Cross-Validation Pipeline & Leak-Free Calibration (Expected Impact: Trustworthy Optimization)**:
   Correcting the cluster assignment in the training harness so all 348 records (including all 98 Gold records) are properly validated in held-out folds ensures future hyperparameter decisions reflect real generalization.
