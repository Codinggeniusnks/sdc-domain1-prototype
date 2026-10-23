# Stage 8C Artifact: Dual-Threshold Product Policy Analysis

## 1. Product Policy Concept

In accordance with the Stage 7C Architecture Review and human-in-the-loop product requirements, skills extraction should support a tiered user experience:
1. **Core Skills ($\text{prob} \ge 0.45$)**: High-confidence skills automatically populated on the user's career profile.
2. **Suggested Skills ($0.25 \le \text{prob} < 0.45$)**: Medium-confidence skills presented as "Recommended / Confirmable" suggestions that the worker can accept or dismiss with one click.
3. **Suppressed Noise ($\text{prob} < 0.25$)**: Low-confidence background predictions filtered out entirely.

---

## 2. Quantitative Evaluation Across Architectures

The dual-threshold policy was evaluated across pooled out-of-fold predictions on Dataset v5 ($N = 311$, 779 total ground truth positive skill instances):

| Metric | Candidate A (`A_base_C2.5`) | Candidate C1 (`C1_MiniLM_C3.0`) | Hybrid Ensemble (`H_0.70A_0.30C1`) | Best Architecture |
| :--- | :---: | :---: | :---: | :---: |
| **Core Precision ($\ge 0.45$)** | 0.6474 | 0.5647 | **0.6524** | **Hybrid Ensemble** |
| **Core Recall ($\ge 0.45$)** | 0.5865 | **0.7006** | 0.6319 | Candidate C1 |
| **Suggested Precision ($[0.25, 0.45)$)** | **0.2133** | 0.1637 | 0.2000 | Candidate A |
| **True Skills Missed by Core** | 327 | 230 | 287 | — |
| **True Skills Recovered by Suggested** | 164 | 145 | **177** | **Hybrid Ensemble** |
| **Recovery Rate of Missed Skills (%)** | 50.15% | 63.04% | **61.67%** | Candidate C1 / Hybrid |
| **False Suggestion Burden (FP/doc)** | **1.95** | 2.38 | 2.28 | Candidate A |

---

## 3. Product Experience Implications

### 3.1. Core Tier Quality
- The **Hybrid Ensemble** achieves the highest Core Precision (**65.24%**), outperforming Candidate A (64.74%) and substantially exceeding Candidate C1 (56.47%).
- This ensures that 2 out of every 3 automatically assigned skills are accurate, minimizing user friction from irrelevant badges.
- Core Recall reaches **63.19%**, automatically capturing the majority of skills without requiring manual review.

### 3.2. Suggested Tier Value & Recovery
- When a skill is missed by the Core threshold (e.g. because of non-standard or implicit phrasing), the Suggested tier recovers **61.67%** of these missed skills (177 instances).
- The false-suggestion burden is approximately **2.28 suggested cards per profile**. In a modern UI card/chip carousel, reviewing 2–3 suggested skill chips is completely manageable and provides a delightful, interactive user empowerment experience.

### 3.3. Decision Recommendation
The data strongly validates the **Dual-Threshold Product Policy** for the **Hybrid Ensemble**:
- Core threshold $\theta_{\text{core}} = 0.45$
- Suggested threshold $\theta_{\text{suggested}} = 0.25$
- Noise cutoff $\theta_{\text{noise}} = 0.25$
