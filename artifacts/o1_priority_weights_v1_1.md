# O1 Priority Index Weights & Mathematical Specification v1.1.0

**Reference Date:** 2026-10-24  
**Framework:** Deterministic Multi-Criteria Reskilling Prioritization  

---

## 1. Weight Derivation & Renormalization

In v1.0.0, the six weights were:
$$\text{CORE} = 0.35, \quad \text{IMPORTANT} = 0.20, \quad \text{DEFICIT} = 0.15, \quad \text{TRANSFER} = 0.15, \quad \text{SCENARIO} = 0.10, \quad \text{PREREQ} = 0.05$$
Summing the 5 active components excluding deficit yields:
$$\text{Sum}_{\text{active}} = 0.35 + 0.20 + 0.15 + 0.10 + 0.05 = 0.85$$

Proportional renormalization preserves exact policy ratios:
$$w_i^{(1.1)} = \frac{w_i^{(1.0)}}{0.85}$$

| Component | v1.0.0 Weight | Renormalization Formula | v1.1.0 Exact Weight | v1.1.0 Approx |
| :--- | :---: | :---: | :---: | :---: |
| **CORE Gap Prevalence** | 0.35 | $0.35 / 0.85$ | **0.4117647059** | 41.18% |
| **IMPORTANT Gap Prevalence** | 0.20 | $0.20 / 0.85$ | **0.2352941176** | 23.53% |
| **Cross-Role Transferability** | 0.15 | $0.15 / 0.85$ | **0.1764705882** | 17.65% |
| **Scenario Urgency** | 0.10 | $0.10 / 0.85$ | **0.1176470588** | 11.76% |
| **Prerequisite Centrality** | 0.05 | $0.05 / 0.85$ | **0.0588235294** | 5.88% |
| **Average Deficit** | 0.15 | $0.00$ | **0.0000000000** | 0.00% |
| **Total** | **1.00** | — | **1.0000000000** | **100.00%** |

---

## 2. Invariants & Mathematical Properties

1. **Exact Unity Sum:** $\sum w_i = 1.0000000000$.
2. **Zero-Gap Gate:** If $\text{raw\_gap\_count} = 0$, $\text{Priority} = 0.00$.
3. **Range:** Bounded in $[0.00, 100.00]$.
4. **Monotonicity:** $\frac{\partial \text{Priority}}{\partial x_i} \ge 0$ for all components.
