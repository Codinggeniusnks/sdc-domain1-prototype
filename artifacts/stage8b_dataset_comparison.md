# Stage 8B Artifact: Dataset Comparison (Dataset v4 vs Dataset v5)

## 1. Executive Summary

Dataset v5 represents a major architectural upgrade in data quality, realism, and methodological rigor for the occupational skills and demand prediction system. While Dataset v4 was artificially inflated with 71.84% synthetic records to overcome small-sample constraints, **Dataset v5 establishes strict real-data dominance**, with **98.07% authoritative Gold records** and only **1.93% synthetic augmentation**.

Synthetic data has been pruned by **97.6%** (from 250 records down to 6). The 6 retained synthetic records were selected through a deterministic class-conditional marginal utility algorithm with an active semantic dissimilarity filter ($\le 0.50$ TF-IDF cosine similarity to Gold), ensuring zero memorization, zero paraphrasing leakage, and targeted deficit reduction.

---

## 2. High-Level Dataset Composition Matrix

| Metric | Dataset v4 (Baseline / Screening) | Dataset v5 (Constructed) | Absolute Change | Percentage Change |
| :--- | :---: | :---: | :---: | :---: |
| **Total Records ($N$)** | 348 | **311** | -37 | -10.63% |
| **Authoritative Gold Records** | 98 | **305** | +207 | **+211.22%** |
| **Gold Record Share (%)** | 28.16% | **98.07%** | +69.91 pp | **+248.26%** |
| **Synthetic Augmentation Records** | 250 | **6** | -244 | **-97.60%** |
| **Synthetic Record Share (%)** | 71.84% | **1.93%** | -69.91 pp | **-97.31%** |
| **Unique Real Occupation Groups** | 34 | **61** | +27 | +79.41% |
| **Primary Real Data Sources** | 3 | **14** | +11 | +366.67% |
| **Dataset SHA-256 Digest** | `8e32f...` | `9c59cc584167b3047e0d5f4177f205937e297da0605e99b369edfc738124032d` | Frozen | Immutable |

---

## 3. Class-by-Class Support & Dominance Comparison

In Dataset v4, minority classes relied heavily on synthetic augmentation (e.g., RAG Knowledge Systems had only 7 real positives and 35 synthetic positives). In Dataset v5, every single class is **authoritatively real-dominant ($\ge 83.87\%$ Gold)**.

| Skill Class | v4 Gold | v4 Synth | v4 Total | v5 Gold | v5 Synth | v5 Total | v5 Gold % | v5 Dominance Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `ai_literacy` | 13 | 41 | 54 | **36** | 2 | **38** | 94.74% | REAL_DOMINANT |
| `prompt_engineering` | 8 | 46 | 54 | **31** | 0 | **31** | 100.00% | REAL_DOMINANT |
| `process_mapping` | 33 | 70 | 103 | **99** | 0 | **99** | 100.00% | REAL_DOMINANT |
| `sql_data_analysis` | 23 | 55 | 78 | **62** | 0 | **62** | 100.00% | REAL_DOMINANT |
| `python_scripting` | 19 | 49 | 68 | **63** | 0 | **63** | 100.00% | REAL_DOMINANT |
| `data_visualization` | 18 | 48 | 66 | **41** | 1 | **42** | 97.62% | REAL_DOMINANT |
| `workflow_automation` | 27 | 64 | 91 | **67** | 0 | **67** | 100.00% | REAL_DOMINANT |
| `human_in_the_loop_qa` | 16 | 45 | 61 | **59** | 0 | **59** | 100.00% | REAL_DOMINANT |
| `rag_knowledge_systems` | 7 | 35 | 42 | **26** | 5 | **31** | 83.87% | REAL_DOMINANT |
| `api_integration` | 14 | 38 | 52 | **42** | 0 | **42** | 100.00% | REAL_DOMINANT |
| `ai_ethics_governance` | 10 | 36 | 46 | **30** | 0 | **30** | 100.00% | REAL_DOMINANT |
| `data_privacy_pdpa` | 13 | 36 | 49 | **44** | 0 | **44** | 100.00% | REAL_DOMINANT |
| `esg_sustainability_reporting` | 16 | 35 | 51 | **43** | 0 | **43** | 100.00% | REAL_DOMINANT |
| `carbon_footprint_analytics` | 5 | 29 | 34 | **29** | 2 | **31** | 93.55% | REAL_DOMINANT |
| `stakeholder_communication` | 34 | 69 | 103 | **98** | 0 | **98** | 100.00% | REAL_DOMINANT |
| `instructional_design` | 11 | 38 | 49 | **29** | 2 | **31** | 93.55% | REAL_DOMINANT |

---

## 4. Analysis of Synthetic Pruning & Quality Filtering

### 4.1. Synthetic Reduction Ratio
- **Baseline Synthetic Candidates**: 250 records in Dataset v4.
- **Selected Synthetic Records**: 6 records.
- **Pruned Synthetic Records**: 244 records (**97.60% reduction**).
- **Justification**: Stage 7C and Stage 8A demonstrated that synthetic data in v4 suffered from low lexical variance, repetitive syntactic boilerplate (e.g., standard phrasing prefixes), and artificial feature correlation that degraded out-of-distribution generalization on Protocols B and C. By pruning 244 synthetic records and expanding real Gold data to 305 records, Dataset v5 eliminates synthetic bias while maintaining class balance.

### 4.2. Semantic Dissimilarity Audit
All 250 synthetic candidates were evaluated against the 305 Gold records using TF-IDF cosine similarity.
- **Maximum similarity in candidate pool**: 0.524 (filtered out).
- **Threshold applied**: Cosine similarity $\le 0.500$.
- **Similarity profile of the 6 accepted records**:
  - `synth-worker-0200`: Max Cosine Sim = **0.2657**
  - `synth-worker-0197`: Max Cosine Sim = **0.2773**
  - `synth-worker-0070`: Max Cosine Sim = **0.2956**
  - `synth-worker-0190`: Max Cosine Sim = **0.3029**
  - `synth-worker-0063`: Max Cosine Sim = **0.3629**
  - `synth-worker-0036`: Max Cosine Sim = **0.4590**
- **Average Similarity**: 0.3272.
- **Conclusion**: None of the retained synthetic records duplicate, paraphrase, or closely mimic real Gold records.

---

## 5. Shift in Data Distribution & Real-World Alignment

1. **Elimination of Synthetic Artefacts**:
   In Dataset v4, models could learn synthetic syntax markers (e.g., predictable template structures) that did not exist in real job descriptions. In Dataset v5, 98.07% of the texts originate from verified Malaysian government frameworks, statutory guidelines, industry competency bodies, and accredited occupational standards.
2. **Expansion of Occupational Breadth**:
   The number of real MASCO 4-digit unit groups expanded from 34 to 61 (+79.4%). This introduces authentic domain vocabulary across engineering, healthcare, finance, legal, manufacturing, and IT disciplines.
3. **Multi-Label Complexity**:
   Real job roles exhibit authentic multi-label co-occurrences (e.g., ESG reporting paired with carbon footprint analytics and stakeholder communication, rather than synthetic uniform distributions).
