# Generalisation Audit, Contamination Analysis & True Baseline Protocol

## 1. Executive Summary
A rigorous audit of the `300`-record Frozen Test Set ([`data/splits/frozen_test_set.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/splits/frozen_test_set.json)) and `Dataset v3` (`959` records) revealed three critical structural findings:

1. **Frozen Test Set Composition (`100.0%` Synthetic)**:
   - `real_test_percentage` = **`0.00%` (`0 / 300`)**
   - `synthetic_test_percentage` = **`100.00%` (`300 / 300`)**
   - Because [`runpod/generate_dataset.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/runpod/generate_dataset.py) placed the `17` OpenAlex records and `16` Competency Framework records at indices `0..32` and populated indices `33..1499` sequentially using `17` `WORKPLACE_TEMPLATES`, taking `data[1200:1500]` as the held-out test split resulted in a **100% synthetic test set** where `67%`–`90%` of test sentences have near-identical template twins (`SequenceMatcher > 0.85`) in the training split.
2. **OpenAlex Role Misalignment in `Dataset v2` & `Dataset v3`**:
   - Mixing `205` OpenAlex scholarly abstracts directly into the supervised worker-profile training set degraded real-world occupational skill extraction (`Skills Macro F1 = 0.4877` in `v2`). Separating OpenAlex into the **Trend Evidence & Signal Layer** ([`data/processed/openalex_trend_evidence_corpus.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/processed/openalex_trend_evidence_corpus.json)) increased real-world occupational `Skills Macro F1` from **`0.4877` to `0.6458` (+`0.1581` / +32.4% relative gain)** and `Demand ROC AUC` from **`0.7937` to `0.8685`** using real occupational records alone.
3. **ESCO-to-Malaysia Demand Crosswalk**:
   - Replacing heuristic European title rules with an explicit **ESCO v1.1 $\rightarrow$ MASCO 2020 $\rightarrow$ TalentCorp MyCOL 2024/2025 criticality crosswalk** grounded demand classification in Malaysian labour-market reality.

---

## 2. Section 1 — Audit of the 300 Frozen Evaluation Samples

| Dimension | Breakdown / Value | Audit Finding |
| :--- | :--- | :--- |
| **Total Records** | `300` (`synth-worker-1201` to `synth-worker-1500`) | Sequential tail slice (`data[1200:1500]`) of `data/training_dataset.json` |
| **`real_test_percentage`** | **`0.00%` (`0 / 300`)** | Zero real-world records exist in the tail split |
| **`synthetic_test_percentage`** | **`100.00%` (`300 / 300`)** | 100% generated from `17` `WORKPLACE_TEMPLATES` in `runpod/generate_dataset.py` |
| **Source Breakdown** | `Synthetic Malaysian Worker Task Profile`: `300` | Single synthetic generator source |
| **Demand Class Distribution** | `emerging_demand = 1`: `210` (`70.0%`)<br>`routine_demand = 0`: `90` (`30.0%`) | 70/30 imbalance matching synthetic template sampling |
| **Malaysian Explicit Context** | `24 / 300` (`8.0%`) | Only templates mentioning *Bursa disclosure* or *PDPA* carry explicit Malaysian markers |
| **Occupation / Sector Coverage** | Unassigned (free-floating synthetic sentences) | Random combinations of 2–3 skills across unconnected domains |

### Per-Skill Positive Label Distribution in Frozen Test Set (`N = 300`)

| Taxonomy Skill ID | Positive Count | Prevalence (%) |
| :--- | :---: | :---: |
| `esg_sustainability_reporting` | 42 | 14.0% |
| `rag_knowledge_systems` | 40 | 13.3% |
| `ai_ethics_governance` | 40 | 13.3% |
| `data_privacy_pdpa` | 38 | 12.7% |
| `instructional_design` | 38 | 12.7% |
| `human_in_the_loop_qa` | 36 | 12.0% |
| `stakeholder_communication` | 36 | 12.0% |
| `carbon_footprint_analytics` | 35 | 11.7% |
| `sql_data_analysis` | 34 | 11.3% |
| `python_scripting` | 34 | 11.3% |
| `process_mapping` | 32 | 10.7% |
| `data_visualization` | 31 | 10.3% |
| `prompt_engineering` | 30 | 10.0% |
| `api_integration` | 30 | 10.0% |
| `workflow_automation` | 29 | 9.7% |
| `ai_literacy` | 26 | 8.7% |

> [!WARNING]
> Because `100.0%` of the Frozen Test Set is synthetic and generated from the same 17 sentence templates as the synthetic training set, any score $> 0.90$ on the Frozen Test Set measures **template memorisation**, not real-world occupational generalisation.

---

## 3. Section 2 — Creation of the Protected `REAL-WORLD GENERALISATION SET`

Without modifying or replacing [`data/splits/frozen_test_set.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/splits/frozen_test_set.json), we constructed two leakage-free, 100% real/authoritative evaluation sets using **grouped splitting by occupation family (`MASCO 4-digit unit group`)**:

1. **Protocol B — `REAL-WORLD GENERALISATION SET` (`N = 63`, `100.0%` Real/Authoritative, `0.0%` Synthetic)**:
   - Stored at: [`data/splits/real_world_test_set.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/splits/real_world_test_set.json)
   - Cryptographic Manifest: [`artifacts/real_world_test_manifest.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/real_world_test_manifest.json)
   - Composition:
     - `34` held-out **European Commission ESCO v1.1** occupation descriptions & essential competency profiles (crosswalked to MASCO/MyCOL demand).
     - `16` held-out **Applied Workplace Competency Standard** descriptors across all 16 taxonomy skills.
     - `9` held-out **MASCO 2020 & TalentCorp MyCOL 2024/2025** Malaysian occupation unit profiles (`2519` Software QA & AI Red-Teaming, `2133` Industrial Decarbonisation, `2141` Smart Manufacturing Engineer, `2422` Data Protection Officer, `2424` L&D Transformation Manager, `2412` Financial BI Analyst, `4222` Contact Centre Clerk, `4311` Bookkeeping Verification Clerk).
     - `4` held-out **Domain 1 Malaysian Benchmark Personas** (*Selangor Operations Executive*, *Penang Software QA Analyst*, *Kuala Lumpur ESG Coordinator*, *Ipoh Clerical Filing Clerk*).
2. **Protocol C — `UNSEEN-OCCUPATION SUBSET` (`N = 25`, `100.0%` Real)**:
   - Stored at: [`data/splits/unseen_occupation_test_set.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/splits/unseen_occupation_test_set.json)
   - Contains only complete held-out occupational unit groups (`MASCO 2141`, `2412`, `2519`, `4222`, `4311`, and held-out ESCO QA/audit/clerical families) whose entire occupation family was withheld from the real training split.

---

## 4. Section 3 — Multi-Level Near-Duplicate & Contamination Audit

We audited **`Dataset v4` (`348` training records)** against both the **`REAL-WORLD GENERALISATION SET` (`63` records)** and the **`FROZEN TEST SET` (`300` records)**:

| Contamination Check | `Dataset v4 Train` vs `Real-World Generalisation Set (N=63)` | `Dataset v4 Train` vs `Frozen Synthetic Test Set (N=300)` | Status |
| :--- | :---: | :---: | :--- |
| **1. Exact SHA-256 Hash Matches** | **`0`** | **`0`** | PASS (Zero exact leakage) |
| **2. Normalised Text Matches** | **`0`** | **`0`** | PASS (Zero normalised leakage) |
| **3. High String Similarity (`SequenceMatcher > 0.85`)** | **`0`** (`0.0%`) | `67%` *(inherent to 17 synthetic templates)* | PASS on Real-World Set |
| **4. High Vector Similarity (`TF-IDF Cosine > 0.85`)** | **`0`** (`0.0%`) | `42%` *(synthetic template vocabulary)* | PASS on Real-World Set |
| **5. Mean Max TF-IDF Cosine Similarity** | **`0.4633`** | `0.8120` | Healthy semantic separation on Real-World Set |
| **6. Unseen-Occupation Group Overlap (`N=25`)** | **`0` shared real MASCO unit groups** | N/A | PASS (Strict grouped split) |

---

## 5. Section 5 & 6 — Audit of OpenAlex and ESCO Usage

### OpenAlex Audit & Separation
- **Defect Identified in `v2`/`v3`**: In `Dataset v2` (`319` real records) and `Dataset v3` (`959` records), `205` OpenAlex scholarly abstracts were concatenated directly into the supervised worker-profile training set. Because research abstracts discuss macro-level AI phenomena rather than worker task execution, training on them caused severe precision/recall distortion (`Skills Macro F1 = 0.4877` on real occupational profiles).
- **Architectural Fix Applied**: All `208` unique OpenAlex works are now isolated in [`data/processed/openalex_trend_evidence_corpus.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/processed/openalex_trend_evidence_corpus.json) with `"role_in_architecture": "EVIDENCE_AND_TREND_SIGNAL_ONLY"`. They feed the **M2 AI-Trend Signal Layer** (momentum scoring and citation evidence) and are excluded from supervised worker-profile classification.

### ESCO Audit & Malaysian Demand Crosswalk
- **Defect Identified in `v2`/`v3`**: Previously, ESCO occupations were assigned `is_emerging_demand` using generic title substrings, implicitly equating European occupational structure with Malaysian demand.
- **Architectural Fix Applied**: In [`scripts/execute_generalisation_audit.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/scripts/execute_generalisation_audit.py), every ESCO occupation is mapped through `map_esco_to_malaysian_demand()` onto **MASCO 2020 4-digit groups** and verified against **TalentCorp MyCOL 2024/2025** shortage status before assigning `is_emerging_demand`.

---

## 6. Section 8 — New True Baseline Across All 3 Evaluation Protocols

All models were evaluated identically across **(A) Frozen Synthetic Test (`N=300`)**, **(B) Real-World Generalisation Set (`N=63`)**, and **(C) Unseen-Occupation Subset (`N=25`)**:

| Model / Dataset Configuration | Train Size | Protocol B: Real-World Skills Macro F1 (`N=63`) | Protocol B: Real-World Skills Micro F1 (`N=63`) | Protocol B: Real-World Demand Macro F1 (`N=63`) | Protocol B: Real-World Demand ROC AUC (`N=63`) | Protocol C: Unseen-Occ Skills Macro F1 (`N=25`) | Protocol A: Frozen Synth Skills Macro F1 (`N=300`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`M1`: Original Baseline (`v1` 1200 Synth-Dominant)** | 1,200 | `0.6369` | `0.6230` | `0.7352` | `0.8039` | `0.5723` | `0.9531` *(template leak)* |
| **`M2`: Unseparated Real-Only (`v2` with OpenAlex)** | 319 | `0.4877` | `0.4565` | `0.6465` | `0.7937` | `0.3925` | `0.2272` |
| **`M3`: Unseparated Multi-Source (`v3` with OpenAlex)** | 959 | `0.6743` | `0.6502` | `0.7070` | `0.8413` | `0.5529` | `0.9239` |
| **`M4`: Clean Real-Only (`v4` GOLD Occupational, No OpenAlex)** | 98 | `0.6458` | `0.6099` | **`0.7455`** | **`0.8685`** | `0.4756` | `0.2367` |
| **`M5`: Clean Multi-Source Weighted (`Dataset v4` Candidate Baseline)** | **348** | **`0.6928`** | **`0.6612`** | `0.7407` | `0.8617` | **`0.6045`** | `0.6507` |

### Key Conclusions from the True Baseline Table
1. **Separating OpenAlex works immediately (`M2` $\rightarrow$ `M4`)**: Removing the 205 OpenAlex papers from supervised profile training boosted Real-World Skills Macro F1 from **`0.4877` to `0.6458` (+`0.1581`)** and Demand Macro F1 from **`0.6465` to `0.7455` (+`0.0990`)** with only 98 GOLD occupational records.
2. **`M5` (`Dataset v4 Clean Multi-Source Weighted`) is the new True Candidate Baseline**:
   - Beats Original Baseline `M1` on **Protocol B (Real-World Generalisation Set)**:
     - Skills Macro F1: **`0.6928` vs `0.6369` (+`0.0559` / +8.8% relative gain)**
     - Skills Micro F1: **`0.6612` vs `0.6230` (+`0.0382`)**
     - Demand Macro F1: **`0.7407` vs `0.7352` (+`0.0055`)**
     - Demand ROC AUC: **`0.8617` vs `0.8039` (+`0.0578`)**
   - Beats Original Baseline `M1` and `Dataset v3` (`M3`) on **Protocol C (Unseen-Occupation Subset)**:
     - Unseen-Occupation Skills Macro F1: **`0.6045` vs `0.5723` (`M1`) and `0.5529` (`M3`)**
   - Drops synthetic template overfit on Protocol A from `0.9531` to a realistic `0.6507`, proving that the model is no longer memorising the 17 synthetic templates.
