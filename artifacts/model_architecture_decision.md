# Model Architecture Decision: Modular System Engineering & Dual-Model Policy

## Executive Summary
This document establishes the binding architectural decisions for the **AI Skills Compass** system, formally decoupling system responsibilities, defining the dual-model development pathway, and establishing the threshold policy.

---

## 1. Development Architecture Selection: Option C (Dual Pathway)

We formally select **Option C — MAINTAIN BOTH UNTIL MORE GOLD DATA EXISTS**, deploying each model to its specific operational role:

```
                            Dual-Model Operational Framework
                                           │
             ┌─────────────────────────────┴─────────────────────────────┐
             ▼                                                           ▼
     [Candidate A: Sparse Hybrid]                                [Hybrid Ensemble: 0.8A + 0.2C1]
     Role: Edge & Real-Time Engine                               Role: Semantic Verification Engine
     - Disk: 245 KB | RAM: ~4 MB                                 - Disk: 90.8 MB | RAM: ~125 MB
     - Latency: 0.82 ms (>1,200 req/s)                           - Latency: 19.22 ms (~52 req/s)
     - Macro F1: 0.6658 (Peak)                                   - Macro F1: 0.6590 (Std: 0.0425)
     - Precision: 59.24% (Anti-hallucination)                    - Recall: 77.22% (Anti-omission)
```

### 1.1 Technical Justification for the Hybrid Trade-off
The Hybrid Ensemble sacrifices a negligible **0.0068 Macro F1** compared to Candidate A, but provides immense real-world value for workforce transitions:
1. **Variance Reduction**: Reduces cross-fold standard deviation from **0.0548 to 0.0425** (a 22.4% reduction in volatility across unseen occupation families).
2. **Transferable Skills Recovery**: Lifts overall recall from 74.08% to **77.22%** (+3.14%) and rare-class recall from 72.26% to **74.56%** (+2.30%).
3. **Paraphrase Robustness**: In empirical error auditing, MiniLM rescued **83 skill instances** that Candidate A missed entirely due to lexical mismatch (e.g. non-standard CV phrasing, synonym usage, and career-changer self-descriptions).
4. **Latency Feasibility**: The 19.22 ms inference latency consumes less than 10% of the interactive 200 ms web response budget.

### 1.2 Retirement of Candidate B (PyTorch)
Candidate B (`SkillsPredictorNN`) is **formally retired from the screening pool**. At $N=348$, deep neural architectures overfit lexical noise and achieve only 0.4714 Macro F1. Reintroducing deep learning will only be considered if the real training corpus expands beyond $1,000$ records.

---

## 2. Decoupled Modular System Responsibilities

To prevent tight coupling and fragile monolithic dependencies, system responsibilities are partitioned across six distinct, independently verifiable engines:

```
                     [Raw Worker CV / Bio / Task Text]
                                     │
                                     ▼
                   ┌───────────────────────────────────┐
                   │   M1: Skills & Profile Engine     │
                   │  - Text Normalization             │
                   │  - Candidate A / Hybrid Predictor │
                   │  - Dual-Threshold Filter          │
                   └─────────────────┬─────────────────┘
                                     │ Extracted Skills Profile
                                     ▼
      ┌────────────────────────────────────────────────────────────────┐
      │                  M3: Role Matching Engine                      │
      │   - Consumes M1 Skills Profile                                 │
      │   - Consumes User Transition Preferences & Seniority           │
      │   - Consumes Dynamic M2 Disruption & Growth Multipliers        │
      │   - Computes Fit Scores, Skill Gaps, & Trajectory Ranking      │
      └──────┬───────────────────────┬──────────────────────────┬──────┘
             │                       │                          │
             ▼                       ▼                          ▼
 ┌───────────────────────┐ ┌───────────────────┐ ┌─────────────────────┐
 │ M4: Reskilling Engine │ │ M5: SDG Impact    │ │ M6: Scenario Engine │
 │ - Concrete Gap Map    │ │ - Quantified      │ │ - Moderate Copilot  │
 │ - Micro-credentials   │ │   Alignment with  │ │   vs Fast Agentic   │
 │ - HRD Corp / TVET     │ │   SDG 4, 8, 9, 10 │ │ - Dynamic Modifiers │
 └───────────────────────┘ └───────────────────┘ └─────────────────────┘
                                     ▲
                                     │ Trend Multipliers
                   ┌─────────────────┴─────────────────┐
                   │    M2: Trend Intelligence Engine  │
                   │  - Live / Snapshot Labor Signals  │
                   │  - AI Automation Vulnerability    │
                   │  - Provenance & Citation Tracking │
                   └───────────────────────────────────┘
```

### 2.1 Confirmation on M2 Trend Decoupling
- **Decisive Rule**: **Static binary demand classification (`is_emerging_demand`) is hereby officially decoupled from M2**.
- Static classification labels in the training set are historical heuristics. Real labour market demand is non-stationary, evolving continuously based on technology adoption and policy (e.g., NETR, National Semiconductor Strategy).
- **M2 must operate as an independent evidence layer**, tracking:
  - Year-over-year hiring momentum from official sources (OpenDOSM, TalentCorp).
  - GenAI displacement vs augmentation indices.
  - Transparent temporal citation (`source: "TalentCorp MyCOL", date: "2025/2026"`).

---

## 3. Threshold Architecture: Dual-Threshold Human-in-the-Loop Policy

Workforce matching systems must never behave as opaque black boxes. We reject the single rigid cutoff policy in favor of a **Dual-Threshold Human Agency Framework**:

```
 Probability (P)
      ▲
 1.00 ┤
      │   CORE SKILLS (Directly Verified & Credited)
      │   P >= 0.45 ──► Added to profile automatically with high confidence.
 0.45 ┼─────────────────────────────────────────────────────────────────────
      │   INFERRED / SUGGESTED SKILLS (Human-in-the-Loop Confirmation)
      │   0.25 <= P < 0.45 ──► Interactive prompt: "Did your experience in
      │                        [Role] involve [Skill]? Tap to add."
 0.25 ┼─────────────────────────────────────────────────────────────────────
      │   NOISE FLOOR (Suppressed)
      │   P < 0.25 ──► Ignored as statistically ungrounded.
 0.00 ┴─────────────────────────────────────────────────────────────────────
```

### Benefits:
- **Zero Penalty on Ambiguity**: Ambiguous descriptions (where probabilities sit between 0.30 and 0.44) are neither falsely attributed nor permanently missed.
- **Fairness & User Ownership**: Workers actively curate and validate their profiles, complying with ethical AI standards.

---

## 4. Future Roadmap for Pretrained Embeddings & Multilingualism

### 4.1 Current Decision on MiniLM: Option B (Reconsider After $>300$ Gold)
- In the current Stage 7 development, `sentence-transformers/all-MiniLM-L6-v2` will remain in its frozen ensemble capacity ($20\%$ weight in Hybrid).
- Full fine-tuning will only be re-evaluated when Gold data exceeds $300$ records.

### 4.2 Multilingual Requirement Flag
- **Critical Limitation**: `all-MiniLM-L6-v2` is strictly an English-language model.
- **Competition Requirement**: The final product must support Malaysia's multilingual workforce: **English, Bahasa Malaysia (BM), and Chinese**.
- **Architectural Migration Path (Stage 9)**:
  - When multilingual evaluation commences, the MiniLM backbone will be swapped with a compact multilingual embedding model:
    - Primary candidate: `paraphrase-multilingual-MiniLM-L12-v2` (118M params) or quantized `bge-m3`.
    - Candidate A's subword char n-grams (`char_wb`) already demonstrate inherent cross-lingual robustness on Bahasa Malaysia morphological roots.
  - *Current Status*: Flagged for Stage 9. Do not introduce multilingual complexity during Stage 7/8 Gold expansion.
