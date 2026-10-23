# M2 OpenAlex Score Effect Audit: Component Transformation & Ceiling Saturation Elimination (v1.1.1)

## 1. Executive Summary

In Stage 9E, the forensic audit identified that although the logarithmic shrinkage formula correctly reduced the excess velocity ratio of nascent topics (e.g., `prompt_engineering` from $17.143 \to 4.434$), the subsequent index mapping:
$$\text{research\_momentum\_index} = \min(95.0, R_{\text{adjusted}} \cdot 38.0)$$
rendered the damping operationally ineffective. Because $4.434 \times 38 = 168.5$, it saturated against the $95.0$ ceiling, receiving the identical top-tier score as mature topics like `ai_literacy` ($9.481 \times 38 = 360.3 \to 95.0$).

In M2 v1.1.1, this defect was completely resolved by replacing the linear multiplier with a **smooth, monotonic asymptotic exponential transform**:
$$\text{research\_momentum\_index} = 50.0 + 44.0 \cdot \left(1.0 - \exp\left(-\frac{R_{\text{adjusted}} - 1.0}{4.0}\right)\right)$$

This document audits the mathematical behavior and empirical score separation across skills.

---

## 2. Empirical Verification Across Required Benchmark Cases

| Case | Skill ID | $N_{\text{baseline}}$ | $N_{\text{recent}}$ | Raw Ratio ($R_{\text{raw}}$) | Volume Weight ($w_{\text{vol}}$) | Adjusted Ratio ($R_{\text{adj}}$) | Old Score (v1.1.0) | New Score (v1.1.1) | Score Delta ($\Delta$) | Quality Flag Attached |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **A** | `prompt_engineering` | 1 | 18 | 17.143 | 0.2127 | **4.434** | 95.0 | **75.4** | **-19.6** | `LOW_BASE_RESEARCH_SIGNAL` |
| **B** | `rag_knowledge_systems` | 1 | 30 | 28.571 | 0.2127 | **6.866** | 95.0 | **83.8** | **-11.2** | `LOW_BASE_RESEARCH_SIGNAL` |
| **C** | `ai_literacy` | 14 | 121 | 11.204 | 0.8312 | **9.481** | 95.0 | **88.7** | **-6.3** | *None ($N \ge 5$)* |
| **D1** | `instructional_design` | 15 | 97 | 8.398 | 0.8514 | **7.299** | 95.0 | **84.9** | **-10.1** | *None ($N \ge 5$)* |
| **D2** | `python_scripting` | 5 | 22 | 5.432 | 0.5499 | **3.437** | 95.0 | **70.1** | **-24.9** | *None ($N \ge 5$)* |
| **D3** | `sql_data_analysis` | 5 | 18 | 4.444 | 0.5499 | **2.894** | 95.0 | **66.6** | **-28.4** | *None ($N \ge 5$)* |

---

## 3. Analysis of Mathematical & Operational Impacts

### 1. Material Separation Between Low-Base and Mature Signals
- In v1.1.0, `prompt_engineering` ($N_{\text{base}} = 1$) and `ai_literacy` ($N_{\text{base}} = 14$) both received `95.0`.
- In v1.1.1, `prompt_engineering` receives **75.4**, while `ai_literacy` receives **88.7**.
- This creates a **$13.3$ point operational separation**, successfully penalizing low-base uncertainty while rewarding deep institutional publication mass.

### 2. Theoretical Verification of Low-Base vs. Mature High Velocity
To confirm that the damping prevents small denominators from being rewarded excessively:
- A hypothetical **1-paper nascent topic** with raw $18.0\times$ growth produces:
  $R_{\text{adj}} = 1 + 17 \cdot 0.2127 = 4.616 \implies \text{Score} = \mathbf{76.2}$.
- A hypothetical **mature topic** with baseline $N = 25$ and raw $18.0\times$ growth produces:
  $R_{\text{adj}} = 18.0 \implies \text{Score} = 50.0 + 44.0 \cdot (1 - \exp(-17/4)) = \mathbf{93.4}$.
- **Result**: The mature topic exceeds the low-base topic by **$17.2$ points**, confirming that the low-base guardrail has a profound, material effect on the final component.

### 3. Preservation of Headroom & Zero Saturation at 100.0
- The asymptotic ceiling of the transform is $50.0 + 44.0 = 94.0$.
- Even if a topic experiences infinite publication growth, its research momentum will never exceed $94.0$, completely preventing hard ceiling saturation at $100.0$.
- Total saturated components at 100.0 across all 16 skills: **0**.

### 4. Preservation of Monotonicity
- The derivative:
  $$\frac{d}{dR_{\text{adj}}} = 11.0 \cdot \exp\left(-\frac{R_{\text{adj}} - 1.0}{4.0}\right) > 0 \quad \forall R_{\text{adj}} \ge 1.0$$
- The transform is strictly monotonic increasing, guaranteeing that rankings are never inverted.
