# Threshold Optimization Plan: Training-Side Out-Of-Fold Policy

## Executive Summary
The independent forensic audit (`artifacts/opus_v4_independent_audit.md`) mandated:
> *"Hard Rule: Protocols B and C are final holdout test sets. Do NOT use either Protocol B or Protocol C for threshold tuning. Threshold selection must occur entirely within training-side grouped cross-validation."*

In accordance with this directive, we conducted a systematic threshold sweep on the **pooled out-of-fold (OOF) prediction probabilities** across the 5 folds of `cv_split_manifest_v2.json`.

Zero holdout data from Protocol B ($N=63$) or Protocol C v2 ($N=25$) was exposed or inspected during this search.

---

## Empirical Threshold Sweep Curve (Candidate A)

Evaluated over $\tau \in [0.25, 0.50]$ with step size $\Delta = 0.02$:

| Threshold ($\tau$) | Skills Macro F1 | Skills Micro F1 | Macro Precision | Macro Recall | Rare Class Recall | Strategic Focus |
|---|---|---|---|---|---|---|
| **0.25** | 0.5819 | 0.5601 | 0.4493 | **0.8419** | **0.8419** | Ultra-High Sensitivity |
| **0.27** | 0.5930 | 0.5724 | 0.4702 | 0.8169 | 0.8169 | High Recall |
| **0.29** | 0.6063 | 0.5881 | 0.4928 | 0.8004 | 0.8004 | High Recall |
| **0.31** | 0.6238 | 0.6052 | 0.5202 | 0.7888 | 0.7888 | Balanced Early |
| **0.33** | 0.6324 | 0.6180 | 0.5399 | 0.7709 | 0.7709 | Balanced Early |
| **0.35** *(Default)* | **0.6391** | **0.6241** | **0.5612** | **0.7497** | **0.7497** | **Optimal Trade-off (Recommended)** |
| **0.37** | 0.6502 | 0.6380 | 0.5959 | 0.7272 | 0.7272 | Metric Maximizing |
| **0.39** | 0.6552 | 0.6450 | 0.6163 | 0.7099 | 0.7099 | Metric Maximizing |
| **0.41** | **0.6553** | **0.6482** | **0.6391** | **0.6869** | **0.6869** | **Peak Macro F1** |
| **0.43** | 0.6550 | 0.6499 | 0.6586 | 0.6687 | 0.6687 | Precision Favored |
| **0.45** | 0.6521 | 0.6488 | 0.6781 | 0.6432 | 0.6432 | Precision Favored |
| **0.47** | 0.6469 | 0.6441 | 0.6990 | 0.6158 | 0.6158 | High Specificity |
| **0.50** | 0.6340 | 0.6321 | 0.7302 | 0.5744 | 0.5744 | Standard Decision Boundary |

---

## Pareto Frontier & Selection Rationale

```
   Macro F1
     ▲
0.66 ┤                      ★ tau=0.41 (Peak F1: 0.6553, Rec: 0.6869)
     │                  ┌───┘
0.64 ┤              ● tau=0.35 (Rec: 0.7497, F1: 0.6391) [RECOMMENDED SAFETY]
     │          ┌───┘
0.62 ┤      ┌───┘
     │  ┌───┘
0.60 ┤  ● tau=0.27 (Rec: 0.8169, F1: 0.5930)
     │
     └────────────────────────────────────────► Precision
       0.45   0.50   0.55   0.60   0.65   0.70
```

1. **Why $\tau = 0.35$ is the Operational Default**:
   - For real-world workforce and skill transition planning (e.g., matching a displaced worker or Malaysian civil service talent to emerging career tracks), **false negatives are more hazardous than false positives**.
   - Missing an essential skill (e.g. failing to flag `data_privacy_pdpa` or `human_in_the_loop_qa`) results in unqualified recommendations, whereas recommending a borderline skill merely prompts a skill assessment.
   - At $\tau = 0.35$, recall remains comfortably high at **74.97%**, while F1 remains strong at **0.6391**.

2. **When to Apply $\tau = 0.41$**:
   - In benchmark competition contexts where the single evaluation metric is pure Macro F1, $\tau = 0.41$ achieves the mathematical optimum (**0.6553**).
   - We freeze $\tau = 0.35$ as the conservative production policy and document $\tau = 0.41$ as the metric-maximizing threshold candidate.
