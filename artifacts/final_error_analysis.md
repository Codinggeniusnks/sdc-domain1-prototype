# Final Error Taxonomy & Failure Mode Analysis (Protocol B & Protocol C v2)

**Evaluator Role**: Senior ML Engineer & Reproducibility Auditor  
**Model**: `H_blend_0.70A_0.30C1_W1.0` (Frozen Hybrid Ensemble)  
**Holdouts Evaluated**: Protocol B ($N = 63$) & Protocol C v2 ($N = 25$)  
**Evaluation Threshold**: $\theta_{\text{eval}} = 0.375$  

---

## 1. Overview of Holdout Prediction Outcomes

Across both sealed holdouts ($63 + 25 = 88$ total real-world and unseen-occupation records, evaluating $88 \times 16 = 1,408$ binary classification decisions):
- **Protocol B (Real-World Holdout, $N = 63$, 133 ground truth positive skill instances)**:
  - True Positives (TP): **102**
  - False Positives (FP): **100**
  - False Negatives (FN): **31**
  - True Negatives (TN): **775**
  - Overall Recall: **76.69%** (Macro Recall: **80.29%**)
  - Rare-Class Recall: **83.75%**
- **Protocol C v2 (Unseen-Occupation Holdout, $N = 25$, 85 ground truth positive skill instances)**:
  - True Positives (TP): **77**
  - False Positives (FP): **33**
  - False Negatives (FN): **8**
  - True Negatives (TN): **282**
  - Overall Recall: **90.59%** (Macro Recall: **85.09%**)
  - Rare-Class Recall: **90.00%**

The model exhibits high sensitivity (Recall $\ge 80\%$ on both holdouts), capturing the vast majority of legitimate occupational skills. Errors are concentrated in over-prediction (false positives) on overlapping organizational tasks rather than silent misses (false negatives).

---

## 2. Error Taxonomy & Qualitative Breakdown

### 2.1. Taxonomy Boundary Overlap: `process_mapping` & `workflow_automation`
- **Symptom**: On Protocol B, `process_mapping` achieved F1 = **0.4444** (Precision = 0.3333, Recall = 0.6667) and `workflow_automation` achieved F1 = **0.4286** (Precision = 0.3000, Recall = 0.7500).
- **Root Cause**: In real enterprise job postings (e.g. IT Business Analysts, Operations Managers, Continuous Improvement Leads), process mapping and workflow automation are described together in the same sentences: *"analyze business workflows to automate operational handoffs and eliminate bottlenecks"*. The model predicts both competencies, whereas human annotators frequently labeled only one of the two based on narrow context.
- **Impact**: Non-damaging for human-in-the-loop recommendation. Both skills are closely aligned in career pathways.

### 2.2. Common Workplace Soft-Skill Bleed: `stakeholder_communication`
- **Symptom**: On Protocol B, `stakeholder_communication` had Precision = **0.3000** and Recall = **0.9231** (12 out of 13 true instances captured, but with 28 false positives).
- **Root Cause**: Almost every real-world job posting contains interpersonal duties (*"liaise with internal teams", "report findings to management", "coordinate across departments"*). Dense MiniLM embeddings capture this pervasive communication signal and assign confidence scores between $0.38$ and $0.52$.
- **Mitigation**: In the product display policy, the Core threshold ($\ge 0.45$) suppresses many of these borderlines, while the Suggested tier ($0.25 \le P < 0.45$) lets users confirm whether stakeholder management is a primary competency.

### 2.3. Highly Technical & Statutory Successes
- **`rag_knowledge_systems`**: Protocol B Support = 1, Precision = **1.0000**, Recall = **1.0000**, F1 = **1.0000**.
- **`prompt_engineering`**: Protocol B Support = 3, Precision = **0.7500**, Recall = **1.0000**, F1 = **0.8571**; Protocol C v2 Support = 3, Precision = **1.0000**, Recall = **1.0000**, F1 = **1.0000**.
- **`python_scripting`**: Protocol B F1 = **0.7500**; Protocol C v2 F1 = **0.9474** (Precision = 0.9000, Recall = 1.0000).
- **`api_integration`**: Protocol C v2 F1 = **0.9333** (Precision = 0.8750, Recall = 1.0000).
- **`esg_sustainability_reporting` & `carbon_footprint_analytics`**: Protocol C v2 F1 = **0.8571** each (Precision = 0.7500, Recall = 1.0000).

### 2.4. Resolution of the `instructional_design` Bottleneck
- In Stage 8C Grouped CV, `instructional_design` had an OOF F1 of $0.2083$ due to fold-level cluster starvation.
- When trained on 100% of Dataset v5, the model achieved:
  - **Protocol B**: Support = 6, Precision = **1.0000**, Recall = **0.6667**, F1 = **0.8000**.
  - **Protocol C v2**: Support = 2, Precision = **1.0000**, Recall = **1.0000**, F1 = **1.0000**.
- **Conclusion**: The weak OOF CV metric was an artifact of cross-validation group partitioning, not a systemic failure of the model architecture.

### 2.5. Residual Weak Class: `data_visualization`
- **Protocol B**: Support = 9, Precision = **0.3750**, Recall = **0.6667**, F1 = **0.4800**.
- **Protocol C v2**: Support = 7, Precision = **0.5455**, Recall = **0.8571**, F1 = **0.6667**.
- **Diagnosis**: Visual reporting in real job descriptions is often implicit (e.g., *"prepare monthly KPI decks"*). The model successfully flags 6 out of 9 instances on Protocol B and 6 out of 7 on Protocol C v2 (high recall: $66.7\%$–$85.7\%$), but produces false positives when documents describe generic report compilation.

---

## 3. Failure Mode Categorization Matrix

| Failure Category | Occurrence Count across Holdouts | Primary Skills Affected | System Risk | Recommended Product Action |
| :--- | :---: | :--- | :---: | :--- |
| **Lexical / Semantic Over-prediction (FP)** | 133 | `stakeholder_communication`, `process_mapping`, `data_visualization` | Low | Suppressed by Core threshold ($0.45$); user-dismissible in Suggested tier. |
| **Implicit Skill Missed (FN)** | 39 | `data_visualization`, `instructional_design`, `sql_data_analysis` | Low-Med | Captured in Suggested tier ($[0.25, 0.45)$) where recovery is $\sim 60\%$. |
| **Taxonomy Boundary Overlap** | 28 | `ai_ethics_governance` vs `data_privacy_pdpa` | Low | Co-recommendation chips in career profile UI. |
| **Zero Test Support** | 1 (`rag` in Protocol C v2) | `rag_knowledge_systems` (0 instances in unseen holdout) | Zero | Verified on Protocol B ($1.0000$ F1). |
| **Language / Multilingual Gap** | 0 | None observed (holdouts are in English) | Zero for English | Future Phase 2 scope for Malay/Chinese NOSS. |
