# Workforce Reskilling Priority Index: Mathematical Specification & Audit (v1.0.0)

**Metric Name:** Workforce Reskilling Priority Index  
**Scale:** $[0.0, 100.0]$  
**Nature:** Deterministic Multi-Criteria Decision Analysis (MCDA)  
**Semantics:** Relative organizational training prioritisation score. **NOT a probability, forecast accuracy, employee performance score, or employment risk rating.**

---

## 1. Mathematical Formulation

For an eligible cohort $\mathcal{C}$ with $N = |\mathcal{C}| \ge 5$ and canonical skill $s$:

$$\text{PriorityIndex}(s) = \mathbf{1}[\text{GapCount}(s) > 0] \times 100 \times \sum_{j=1}^{6} w_j \cdot x_j(s)$$

### Configurable Product-Policy Weights:
$$\sum_{j=1}^{6} w_j = 0.35 + 0.20 + 0.15 + 0.15 + 0.10 + 0.05 = 1.0000$$

| Component ($x_j$) | Weight ($w_j$) | Derivation Formula | Range | Rationale |
|---|---|---|---|---|
| **1. CORE Gap Prevalence** | $0.35$ | $x_{\text{core}} = \frac{|\{i \in \mathcal{C} \mid s \in \text{CoreGaps}(i)\}|}{N}$ | $[0.0, 1.0]$ | Dominant weight: failure to master core requirements halts job execution. |
| **2. IMPORTANT Gap Prevalence** | $0.20$ | $x_{\text{imp}} = \frac{|\{i \in \mathcal{C} \mid s \in \text{ImportantGaps}(i)\}|}{N}$ | $[0.0, 1.0]$ | Secondary priority: operational productivity and effectiveness competencies. |
| **3. Mean Deficit Among Gapped** | $0.15$ | $x_{\text{def}} = \frac{\sum_{i \in \text{Gapped}(s)} \text{Deficit}(i, s)}{|\text{Gapped}(s)|}$ | $[0.0, 1.0]$ | Workload factor: measures distance from baseline to required proficiency. |
| **4. Cross-Role Transferability** | $0.15$ | $x_{\text{trans}} = \frac{\text{TransferabilityPct}(s)}{100.0}$ | $[0.0, 1.0]$ | Leverage factor: % of 20 national roles requiring skill in frozen M4 catalog. |
| **5. Scenario Urgency** | $0.10$ | $x_{\text{scen}} = \frac{\text{UrgencyBonus}(s, \text{scen})}{20.0}$ | $[0.0, 1.0]$ | Foresight factor: adjusts for disruption shocks under M6 AI scenarios. |
| **6. Prerequisite Centrality** | $0.05$ | $x_{\text{prereq}} = \frac{|\text{DownstreamDependencies}(s)|}{15.0}$ | $[0.0, 1.0]$ | Curriculum bottleneck: skills that unlock downstream capabilities in M4 graph. |

---

## 2. Benchmark Arithmetic Audit (Top 5 Skills Verified)

Evaluated on the 50-profile synthetic enterprise workforce cohort under `REFERENCE_2026`:

### 1. Process Mapping (`process_mapping`)
- $x_{\text{core}} = 0.22 \implies w \cdot x = 0.35 \times 0.22 = 0.0770$ (7.70 pts)
- $x_{\text{imp}} = 0.26 \implies w \cdot x = 0.20 \times 0.26 = 0.0520$ (5.20 pts)
- $x_{\text{def}} = 1.00 \implies w \cdot x = 0.15 \times 1.00 = 0.1500$ (15.00 pts)
- $x_{\text{trans}} = 0.65 \implies w \cdot x = 0.15 \times 0.65 = 0.0975$ (9.75 pts)
- $x_{\text{scen}} = 0.00 \implies w \cdot x = 0.10 \times 0.00 = 0.0000$ (0.00 pts)
- $x_{\text{prereq}} = 0.1333 \implies w \cdot x = 0.05 \times 0.1333 = 0.0067$ (0.67 pts)
- **Total Priority Index:** $7.70 + 5.20 + 15.00 + 9.75 + 0.00 + 0.67 = \mathbf{38.32}$ (Rank 1)

### 2. SQL Data Analysis (`sql_data_analysis`)
- $x_{\text{core}} = 0.20 \implies 7.00$ pts
- $x_{\text{imp}} = 0.28 \implies 5.60$ pts
- $x_{\text{def}} = 1.00 \implies 15.00$ pts
- $x_{\text{trans}} = 0.45 \implies 6.75$ pts
- $x_{\text{scen}} = 0.00 \implies 0.00$ pts
- $x_{\text{prereq}} = 0.1333 \implies 0.67$ pts
- **Total Priority Index:** $7.00 + 5.60 + 15.00 + 6.75 + 0.00 + 0.67 = \mathbf{35.02}$ (Rank 2)

### 3. Python Scripting (`python_scripting`)
- $x_{\text{core}} = 0.34 \implies 11.90$ pts
- $x_{\text{imp}} = 0.06 \implies 1.20$ pts
- $x_{\text{def}} = 1.00 \implies 15.00$ pts
- $x_{\text{trans}} = 0.35 \implies 5.25$ pts
- $x_{\text{scen}} = 0.00 \implies 0.00$ pts
- $x_{\text{prereq}} = 0.1333 \implies 0.67$ pts
- **Total Priority Index:** $11.90 + 1.20 + 15.00 + 5.25 + 0.00 + 0.67 = \mathbf{34.02}$ (Rank 3)

### 4. Workflow Automation (`workflow_automation`)
- $x_{\text{core}} = 0.06 \implies 2.10$ pts
- $x_{\text{imp}} = 0.36 \implies 7.20$ pts
- $x_{\text{def}} = 1.00 \implies 15.00$ pts
- $x_{\text{trans}} = 0.60 \implies 9.00$ pts
- $x_{\text{scen}} = 0.00 \implies 0.00$ pts
- $x_{\text{prereq}} = 0.0000 \implies 0.00$ pts
- **Total Priority Index:** $2.10 + 7.20 + 15.00 + 9.00 + 0.00 + 0.00 = \mathbf{33.30}$ (Rank 4)

### 5. Data Visualization (`data_visualization`)
- $x_{\text{core}} = 0.02 \implies 0.70$ pts
- $x_{\text{imp}} = 0.46 \implies 9.20$ pts
- $x_{\text{def}} = 1.00 \implies 15.00$ pts
- $x_{\text{trans}} = 0.50 \implies 7.50$ pts
- $x_{\text{scen}} = 0.00 \implies 0.00$ pts
- $x_{\text{prereq}} = 0.0000 \implies 0.00$ pts
- **Total Priority Index:** $0.70 + 9.20 + 15.00 + 7.50 + 0.00 + 0.00 = \mathbf{32.40}$ (Rank 5)

---

## 3. Structural Properties & Invariants

1. **Exact Component Decomposition:** $\sum_{j} \text{WeightedContribution}_j \equiv \text{PriorityIndex}$ within rounding tolerance (0.05).
2. **Core-First Primacy:** A skill with high CORE gap prevalence (e.g. Python at 34%) gains significant structural advantage ($11.90$ pts) over an equally prevalent SUPPORTING skill.
3. **Course & Commercial Independence:** Priority calculations depend strictly on competency demand and role structure. Course prices, provider brands, or platform commercial partnerships cannot alter priority scores.
4. **Zero-Deficit Protection:** If zero workers in the cohort possess a gap for skill $s$, its index is set to $0.00$ with tier `"NONE"` to prevent unneeded corporate training spend.
