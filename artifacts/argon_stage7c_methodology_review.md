# Argon Stage 7C: Independent Methodology Review & Architectural Decision

**Reviewer**: Senior ML Research Architect & Competition Systems Architect  
**Review Gate**: Stage 7C Post-Screening Audit  
**Prior Status**: Stage 7A Forensic Remediation (PASSED) | Stage 7B Clean Model Screening (PASSED)  
**Holdout Protection**: Protocol B ($N=63$) and Protocol C v2 ($N=25$) verified **STRICTLY SEALED** (0 accesses).

---

## 1. Validation of Stage 7B Screening Conclusions

We conducted an architectural and statistical review of the Stage 7B screening results (`artifacts/stage7b_screening_results.csv`, `artifacts/stage7b_candidate_comparison.md`, and `artifacts/stage7b_threshold_analysis.csv`).

### 1.1 Methodological Audit Checklist
1. **Grouped CV Integrity**: **VALID**. The 5 folds in `cv_split_manifest_v2.json` enforce mutually disjoint MASCO occupation unit groups and synthetic template families. Zero cluster overlap and zero template leakage exist across all folds.
2. **Gold Representation**: **VALID**. Each validation fold contains 18 to 24 Gold authoritative records (26% to 32% of validation samples), resolving the legacy defect where validation folds contained 0 Gold records.
3. **Preprocessing Isolation**: **VALID**. Feature extraction (`TfidfVectorizer`), subword analyzers, and normalization are fit strictly on training folds and transformed on validation folds.
4. **Sample Weighting vs Row Duplication**: **VALID**. Multi-tier weighting is passed directly as `sample_weight` to the loss functions without physical row repetition. Training set cardinality remains strictly $N=348$.
5. **Fair Candidate Comparison**: **VALID**. All 20 configurations were evaluated over identical fold splits with identical metric implementations.
6. **Threshold Tuning Isolation**: **VALID**. Threshold sweeps were conducted strictly on pooled out-of-fold (OOF) validation predictions. Final holdouts Protocol B and Protocol C v2 remained completely untouched.

### Methodological Classification:
### **VERDICT: VALID**
The Stage 7B screening methodology is scientifically sound, statistically defensible, and free of data leakage.

---

## 2. Primary Bottleneck Identification

The screening experiments definitively prove that **model architecture is no longer the binding constraint**:
- Candidate A achieves **0.6658 Macro F1** on the current dataset.
- Candidate B (PyTorch deep neural network) collapsed to **0.4714 Macro F1** because $N=348$ is too small to fit non-linear representations without severe sample starvation.
- Training on the 98 Gold samples alone collapsed performance to **0.2898 Macro F1**, proving that data sparsity across 16 multi-label classes is the root limiter.

```
       [Current State]                                     [Bottleneck Diagnosis]
 ┌─────────────────────────┐                           ┌────────────────────────────┐
 │  98 Real Gold Records   │ ──► Severe class sparsity │ DATA VOLUME & REAL LABEL   │
 │ 250 Synthetic Records   │     across 16 classes     │ COVERAGE IS THE PRIMARY    │
 │ Total N = 348           │                           │ BOTTLENECK (NOT MODEL TYPE)│
 └─────────────────────────┘                           └────────────────────────────┘
```

Further hyperparameter tuning or architectural complexity yields diminishing returns ($<0.005$ F1). Real-world generalization gains will come strictly from **targeted Gold data expansion** and **modular system integration**.

---

## 3. Core Architectural Decisions

### 3.1 Development Architecture Selection: Option C (Maintain Both)
- **Primary Runtime Engine**: **Candidate A (`A_base_C3.0`)**
  - Ultra-lightweight (~245 KB), sub-millisecond inference (0.82 ms), zero deep learning dependencies.
  - Delivers highest precision (59.24%) and highest peak Macro F1 (0.6658).
- **Semantic-Enhanced Benchmark Engine**: **Candidate Hybrid (`Hybrid_Ens_0.8A_0.2C1`)**
  - Convex probability ensemble: $0.8 \cdot P_{\text{Candidate A}} + 0.2 \cdot P_{\text{MiniLM}}$.
  - Reduces fold standard deviation by **22.4%** (0.0548 $\rightarrow$ 0.0425).
  - Lifts recall from 74.08% to **77.22%** and rare-class recall from 72.26% to **74.56%**.
  - Catches 83 semantic paraphrases and implicit skills that Candidate A misses.
- **Decision**: **Maintain both Candidate A and Hybrid Ensemble** until Gold data expands to $>300$ samples. Candidate B (PyTorch) is formally decommissioned.

### 3.2 Dual-Threshold & Human-in-the-Loop Policy
Rather than forcing a single rigid classification threshold, the M1 intake system will implement a **Dual-Threshold / Confirmation Framework**:
1. **Core / High-Confidence Skills ($\tau \ge 0.45$)**: Directly recognized and populated into the user's verified skills profile.
2. **Suggested / Inferred Skills ($0.25 \le \tau < 0.45$)**: Presented in the interactive UI for user confirmation (*"Based on your background in Operations, did your work include Process Mapping? Tap to confirm"*).
3. **Noise Floor ($\tau < 0.25$)**: Suppressed.

This architecture preserves human agency, aligns with Malaysian ethical AI guidelines, and completely eliminates the penalty of false-negative skill omissions for career changers.

---

## 4. Synthesis of Findings & Key Directives

| Domain | Key Directive | Rationale |
|---|---|---|
| **Model Selection** | Deploy Candidate A for latency/edge; use Hybrid for semantic recall | Optimal balance of precision (A) and contextual recall (MiniLM) |
| **Gold Weighting** | Set $w_{\text{gold}} \in [1.0, 2.0]$ | Eliminates gradient distortion caused by legacy 3.0 weighting |
| **Synthetic Policy** | Class-conditional support only | Retain synthetic samples only for classes with $<25$ real Gold positives |
| **Demand Model** | Decouple completely from M1 skills | Future demand belongs to dynamic M2 Trend Signal Layer |
| **Compute / Infra** | **No RunPod GPU needed yet** | CPU training takes $<5$ seconds; GPU is an unnecessary expense |
| **Next Action** | **EXPAND GOLD DATA NEXT** | Targeted acquisition of 150–200 Malaysian real records |
