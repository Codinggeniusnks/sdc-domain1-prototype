# Stage 7B Semantic Error Analysis: Candidate A vs Pretrained MiniLM

## Executive Summary
To understand the complementary behavior between lexical token matching (Candidate A) and dense semantic representations (Candidate C1 / MiniLM), we conducted a granular error analysis across the 348 pooled out-of-fold (OOF) cross-validation predictions.

### Quantitative Complementarity
- **MiniLM Rescues**: MiniLM correctly identified **83** ground-truth skill occurrences that Candidate A missed (False Negatives of A).
- **Candidate A Rescues**: Candidate A correctly identified **76** ground-truth skill occurrences that MiniLM missed (False Negatives of MiniLM).
- **False Positive Asymmetry**: MiniLM produced **3.1x more False Positives** than Candidate A across the corpus, explaining its lower precision (35.3% vs 59.2%).

---

## 1. Categorical Error Taxonomy

```
                              Error Domain Matrix
                                       │
         ┌─────────────────────────────┴────────────────────────────┐
         ▼                                                          ▼
  MiniLM Advantages (Semantic Recall)         Candidate A Advantages (Lexical Precision)
  - Paraphrased job tasks                      - Acronyms & Regulatory Tokens (PDPA, ESG)
  - Broad implicit competencies                - Fine-grained technical differentiation
  - Domain context association                 - Compound nouns (e.g. Prompt Engineering)
```

---

## 2. In-Depth Error Category Case Studies

### 2.1 Category 1: Abbreviations & Regulatory Standards
- **Exemplar Record**: `masco-2133-01`
  > *"Prepares corporate sustainability disclosures aligned with Bursa Malaysia Main Market ESG guidelines and ISSB standards..."*
  - **Ground Truth**: `esg_sustainability_reporting`, `carbon_footprint_analytics`, `data_visualization`, `sql_data_analysis`
  - **Candidate A Prediction**: `esg_sustainability_reporting`, `carbon_footprint_analytics`, `data_visualization` (Accurate)
  - **MiniLM Prediction**: `esg_sustainability_reporting`, `ai_ethics_governance`, `prompt_engineering`, `sql_data_analysis`
  - **Diagnostic**: Candidate A's subword char n-grams (`issb`, `esg`, `bursa`) cleanly fired on sustainability. MiniLM projected "corporate governance & guidelines" into the semantic neighborhood of `ai_ethics_governance` and hallucinated `prompt_engineering` due to general technology bias.

### 2.2 Category 2: Implicit Competencies & Contextual Association
- **Exemplar Record**: `masco-2511-01`
  > *"Evaluates enterprise standard operating procedures and performs business process mapping across Malaysian shared service centres, conducting audits on human review handoffs..."*
  - **Ground Truth**: `process_mapping`, `human_in_the_loop_qa`, `workflow_automation`, `api_integration`, `stakeholder_communication`
  - **Candidate A Misses**: Missed `human_in_the_loop_qa` and `stakeholder_communication` (predicted only `ai_literacy`, `process_mapping`, `api_integration`).
  - **MiniLM Rescues**: Correctly predicted `human_in_the_loop_qa` and `stakeholder_communication`.
  - **Diagnostic**: The text described human QA via the paraphrase *"conducting audits on human review handoffs"*. Candidate A lacked the exact n-gram token `human_in_the_loop` in the training fold vocabulary. MiniLM's contextual embedding recognized the semantic equivalence between "human review handoff" and `human_in_the_loop_qa`.

### 2.3 Category 3: Technical Compound Words (e.g., Prompt Engineering)
- **Exemplar Record**: `masco-2424-01`
  > *"Designs adult reskilling curricula and HRD Corp e-LATiH training modules on foundational AI literacy, structured prompt authoring techniques, and generative tools..."*
  - **Ground Truth**: `instructional_design`, `prompt_engineering`, `ai_literacy`, `process_mapping`, `stakeholder_communication`
  - **Candidate A Rescues**: Correctly triggered `prompt_engineering` and `ai_literacy`.
  - **MiniLM Misses**: Missed `prompt_engineering`, instead predicting `ai_ethics_governance` and generic `ai_literacy`.
  - **Diagnostic**: Because the text used the synonym phrase *"prompt authoring techniques"*, MiniLM's generic semantic space treated it as general AI authoring rather than assigning high probability to the specific taxonomy class `prompt_engineering`. Candidate A's subword `promp` character n-gram securely matched the root.

### 2.4 Category 4: Malaysian Localized Terminology
- **Exemplar Record**: `masco-2521-01`
  > *"Manages enterprise relational databases, writes complex SQL queries and data warehouse transformations, enforces Malaysian Personal Data Protection Act (PDPA 2010) compliance..."*
  - **Ground Truth**: `sql_data_analysis`, `data_privacy_pdpa`, `data_visualization`
  - **Candidate A Rescues**: Correctly anchored on `pdpa` and `sql_data_analysis`.
  - **MiniLM Behavior**: MiniLM detected `data_privacy_pdpa`, but also falsely triggered `ai_literacy` and `stakeholder_communication`.
  - **Diagnostic**: Localized regulatory acts like PDPA are best grounded by exact lexical matching. However, MiniLM reliably captures privacy intent even when authors write "personal data protection" without the acronym "PDPA".

---

## 3. High-Difficulty Classes Inspection

| Target Class Domain | Primary Failure Mode | Best Performing Architecture | Remedy Required |
|---|---|---|---|
| **PDPA / Privacy** | Low recall (48.6%) in Candidate A due to diverse phrasing | **MiniLM (Recall 71.4%) / Hybrid** | Hybrid ensemble captures paraphrases; expand training synonyms |
| **ESG / Sustainability** | False negatives in Candidate A (56.3% recall) | **Hybrid (F1 = 0.5397, Recall 70.8%)** | Hybrid ensemble significantly outperforms either standalone model |
| **RAG Knowledge Systems** | High performance across all models | **Hybrid (F1 = 0.8696, Prec 85.7%)** | Mature feature representation |
| **Instructional Design** | Low precision (46.2%) in Candidate A | **Candidate A (F1 = 0.5505)** | Needs domain-specific Gold HRD Corp curriculum examples |
| **Process Mapping** | High false positives (prec 38.8%) | **Candidate A (F1 = 0.4769)** | Difficult boundary; task descriptions frequently use "process" generically |

---

## 4. Conclusion & Architectural Recommendation

1. **Neither Model is Redundant**:
   Candidate A provides irreplaceable keyword precision (preventing hallucinations on non-existent technical skills), while MiniLM provides vital semantic recovery on paraphrased, implicit, or synonym-based descriptions.
2. **Hybrid Ensemble is the Mathematically Optimal Solution**:
   Combining Candidate A (weight 0.8) and MiniLM (weight 0.2) captures the majority of MiniLM's 83 semantic rescues while preserving Candidate A's high precision floor, lifting overall recall to **77.2%** and rare-class recall to **74.6%**.
