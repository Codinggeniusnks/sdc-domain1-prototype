# Stage 8C Artifact: Stage 8D Readiness Assessment & Candidate Nomination

## 1. Readiness Audit Overview

This document provides the formal audit and gate evaluation for Stage 8C, assessing whether the model screening on Dataset v5 satisfies all scientific, architectural, and methodological requirements to proceed to **Stage 8D: Final Methodology Review & Model Freeze**.

---

## 2. Gate Criteria Compliance Checklist

| Evaluation Item | Protocol Requirement | Stage 8C Measured Result | Compliance Status |
| :--- | :--- | :--- | :---: |
| **1. Dataset Integrity** | Train only on Dataset v5 with frozen SHA-256 | SHA-256 verified: `9c59cc584167b3047e0d5f4177f205937e297da0605e99b369edfc738124032d` | **PASSED** |
| **2. Final Holdout Protection (Protocol B)** | Strict zero access (`real_world_test_set.json`) | **0 accesses**, strictly sealed in cold storage | **PASSED** |
| **3. Final Holdout Protection (Protocol C v2)** | Strict zero access (`unseen_occupation_test_set_v2.json`) | **0 accesses**, strictly sealed in cold storage | **PASSED** |
| **4. Grouped CV Strictness** | Use only `cv_split_manifest_v3.json` | 5 folds executed with zero group or template leakage | **PASSED** |
| **5. Fold-Level Preprocessing Isolation** | Fit TF-IDF, vectorizers, and heads on train folds only | Strict per-fold training isolation enforced | **PASSED** |
| **6. Architecture Boundaries** | Retain only Candidates A, C1, and probability Hybrid | Candidate B and feature concatenation omitted | **PASSED** |
| **7. Calibration Policy** | Compare raw vs calibrated; remove if no benefit | Platt calibration degraded Macro F1 by -0.0383; **removed** | **PASSED** |
| **8. Threshold Optimization** | Bounded search on pooled OOF probabilities | Optimal threshold identified at $\theta = 0.375$ | **PASSED** |
| **9. Dual-Threshold Policy Audit** | Evaluate Core ($\ge 0.45$) vs Suggested ($[0.25, 0.45)$) | Verified: Core Prec = 65.24%, Missed Recovery = 61.67% | **PASSED** |
| **10. Local CPU Execution** | No RunPod GPU used; pure local execution | Screened in 57.94s locally on CPU | **PASSED** |
| **11. OOF Artifact Serialization** | Save full OOF predictions for A, C1, H | Saved in `artifacts/stage8c_oof_predictions_{A,C1,H}.json` | **PASSED** |
| **12. Model Freeze Boundaries** | Do NOT freeze model or push to Git/production | No freeze, no commit, no deployment | **PASSED** |

---

## 3. Candidate Nominations for Stage 8D Methodology Review

Based on empirical performance, cross-fold stability, error complementarity, and operational latency, the following candidates are nominated for the upcoming Stage 8D review:

### 3.1. Primary Candidate: Hybrid Ensemble (`H_blend_0.70A_0.30C1`)
- **Architecture**: 70% Candidate A (`A_base_C2.5_W1.0`, Word 1-3 + Char 3-5 TF-IDF + Logistic Regression) + 30% Candidate C1 (`C1_MiniLM_C3.0_W1.0`, Frozen `all-MiniLM-L6-v2` + Logistic Regression).
- **Optimal Decision Threshold**: $\theta = 0.375$
- **Performance**:
  - **Macro F1**: **0.6434**
  - **Micro F1**: **0.6357**
  - **Rare-Class Recall**: **0.6313**
  - **Cross-Fold Stability**: SD = **0.1061** (lowest variance across all candidates)
  - **Dual-Threshold Core Precision**: **65.24%**
  - **Suggested Tier Recovery**: **61.67%** of missed skills recovered
- **System Footprint**: 95.7 MB disk, ~285 MB RAM, 16.0 ms CPU latency.
- **Justification**: Achieves top-tier F1, highest rare-class sensitivity, lowest fold variance, and recovers 286 semantic error cases that TF-IDF cannot solve.

### 3.2. Secondary Candidate / Compact Fallback: Candidate A (`A_base_C2.5_W1.0`)
- **Architecture**: Subword + Word Hybrid TF-IDF (Word 1-3, Char 3-5, $C=2.5$, `class_weight='balanced'`, $W_{\text{gold}}=1.0$).
- **Optimal Decision Threshold**: $\theta = 0.375$
- **Performance**:
  - **Macro F1**: **0.6248** ($0.6266$ with $W=1.5$)
  - **Micro F1**: **0.6202**
  - **Rare-Class Recall**: **0.5912**
  - **Cross-Fold Stability**: SD = **0.1100**
- **System Footprint**: 4.2 MB disk, ~45 MB RAM, 1.2 ms CPU latency.
- **Justification**: Extreme lightweight efficiency for micro-containers or browser/edge deployment where PyTorch/transformers cannot be installed.

---

## 4. Formal Readiness Verdict

All methodological checks, security gates, and reproducibility protocols have passed without reservation.

### Official Verdict:
$$\mathbf{READY\ FOR\ FINAL\ METHODOLOGY\ /\ MODEL-FREEZE\ REVIEW}$$

*(Stage 8C execution halted strictly; no model frozen, no holdouts accessed, no deployment).*
