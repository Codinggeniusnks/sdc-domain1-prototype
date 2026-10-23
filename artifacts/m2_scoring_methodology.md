# M2 AI Trend Intelligence Engine: Scoring Methodology Specification

**Author:** Senior Labour-Market Quantitative Researcher, ML Systems Engineer & Explainable-AI Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9B Explainable M2 Trend Scoring Engine  
**Version:** 1.0.0  
**Status:** COMPLETE & SEALED FOR REVIEW  

---

## 1. Executive Summary & Architectural Tenets

The M2 AI Trend Intelligence Engine generates transparent, decomposed labour-market trend vectors for skills and occupations in Malaysia. It explicitly rejects monolithic black-box "Future Scores" in favour of an auditable, multi-dimensional profile that separates state from momentum and AI exposure from occupational decline.

### Core Methodological Invariants:
1. **Decomposed Multi-Dimensional Profiling:** Every entity is scored across 10 distinct, bounded dimensions ([0.0, 100.0]).
2. **State vs. Momentum Separation:** High shortage persistence is differentiated from demand acceleration (e.g., persistent shortage does not equate to accelerating shortage; newly critical occupations have surging momentum despite moderate historical persistence).
3. **AI Exposure vs. Job Decline Separation:** High exposure to Generative AI is not treated as job contraction. Exposure is decomposed into task automation potential (substitutive) versus augmentation potential (complementary). Occupations with high exposure and high augmentation remain strongly rising.
4. **Transparent Provenance & Citation Traceability:** Every positive or negative driver directly references an underlying `signal_id`, `source_id`, publisher, observation date, and formal bibliographic reference.
5. **No Forced Imputation:** Dimensions with insufficient data remain strictly `null` (or return `INSUFFICIENT_DATA`), never filled with a neutral 50.

---

## 2. The 10 Decomposed Analytical Dimensions

| # | Dimension Name | Scale | Type | Primary Evidence Base | Interpretation |
| :--- | :--- | :---: | :---: | :--- | :--- |
| 1 | `demand_shortage_level` | 0–100 | Index | TalentCorp MyCOL, Impact Study | Current structural shortage severity & historical persistence |
| 2 | `demand_momentum` | 0–100 | Index | MyCOL longitudinal shifts, employer surveys | Annualized demand trajectory & emergence velocity |
| 3 | `employment_wage_momentum` | 0–100 | Index | OpenDOSM Salaries & Wages (2010–2025) | 5-year CAGR and medium-term wage growth percentile |
| 4 | `research_momentum` | 0–100 | Index | OpenAlex Scholarly Corpus (2020–2026) | Academic publication growth velocity ratio ($G_{\text{ratio}}$) |
| 5 | `ai_exposure` | 0–100 | Index | ILO Working Paper 96 | Share of occupational task-hours exposed to LLMs |
| 6 | `automation_exposure` | 0–100 | Index | ILO Working Paper 96 | Share of routine cognitive/manual tasks substitutable by AI |
| 7 | `augmentation_potential` | 0–100 | Index | ILO Working Paper 96 | Share of complex cognitive tasks complemented/accelerated by AI |
| 8 | `policy_priority` | 0–100 | Index | Statutory Laws, Bursa ESG, MOSTI AIGE, NSS | Legal and national economic development alignment |
| 9 | `evidence_confidence` | 0–100 | Index | Source independence & cross-source agreement | Reliability index (accompanied by categorical label) |
| 10 | `freshness` | Days | Metric | Retrieval timestamp vs. reference date | Signal-type aware temporal validity (Fresh/Aging/Stale) |

---

## 3. Mathematical Normalisation & Scaling

All index components are normalized into the interval $[0.0, 100.0]$:

### 3.1. Demand Shortage Level
For MASCO 4-digit occupations:
$$\text{Shortage}(o) = \begin{cases} 
\min(100.0, \text{Persistence}(o) \times 100.0) & \text{if Persistent Critical } (\ge 6/8 \text{ editions}) \\
60.0 & \text{if Newly Critical (appeared 2022/23 or 2024/25)} \\
20.0 & \text{if Dropped from latest edition} \\
\max(30.0, \text{Persistence}(o) \times 80.0) & \text{if Cyclical Critical}
\end{cases}$$

### 3.2. Demand Momentum
Captures the rate of change rather than cumulative state:
- Newly critical roles: $\text{Momentum} = 88.0$ (Surging acceleration).
- Persistent critical roles: $\text{Momentum} = 75.0$ (High, steady sustained demand).
- Cyclical roles: $\text{Momentum} = 55.0$ (Moderate/stable).
- Dropped roles: $\text{Momentum} = 25.0$ (Structural contraction).

### 3.3. Research Momentum
Evaluated at the skill/technology layer using OpenAlex publication velocity ratio:
$$G_{\text{ratio}}(s) = \frac{V_{\text{recent}}(s) / 3.0}{(V_{\text{base}}(s) / 4.0) + \epsilon}$$
$$\text{Index}_{\text{Research}}(s) = \min\left(100.0, \max\left(10.0, G_{\text{ratio}}(s) \times 40.0\right)\right)$$
*Note:* To prevent conflating academic publications with job vacancies, occupational profiles maintain `research_momentum = null`.

### 3.4. AI Exposure, Automation & Augmentation
Derived directly from ILO Working Paper 96 task evaluations, mapped to ISCO-08 sub-major groups and calibrated to MASCO 2020:
$$\text{Index}_{\text{Exposure}} = \text{round}(\text{Exposure\_Score} \times 100.0, 1)$$
$$\text{Index}_{\text{Auto}} = \text{round}(\text{Automation\_Potential} \times 100.0, 1)$$
$$\text{Index}_{\text{Aug}} = \text{round}(\text{Augmentation\_Potential} \times 100.0, 1)$$

---

## 4. Rule-Based Outlook Classification

Rather than training an uninterpretable machine learning classifier on limited macro data, M2 implements explicit, auditable classification rules:

```
+--------------------------------------------------------------------------------------------------+
|                                    OUTLOOK DECISION LOGIC                                        |
+--------------------------------------------------------------------------------------------------+
| 1. STRONGLY DECLINING:                                                                           |
|    IF Automation >= 2.5 * Augmentation AND Dropped from MyCOL AND Wage Momentum < 35            |
|                                                                                                  |
| 2. DECLINING:                                                                                    |
|    IF Automation > Augmentation AND (Dropped from MyCOL OR Wage Momentum < 40)                   |
|                                                                                                  |
| 3. STRONGLY RISING:                                                                              |
|    IF Demand Momentum >= 75 AND Augmentation >= Automation AND (Policy >= 75 OR Persistent Critical) |
|                                                                                                  |
| 4. RISING:                                                                                       |
|    IF (Demand Momentum >= 60 OR Shortage Level >= 65) AND Augmentation >= Automation             |
|                                                                                                  |
| 5. STABLE:                                                                                       |
|    IF Demand Momentum in [45, 65] AND Automation < 20                                            |
|                                                                                                  |
| 6. MIXED / UNCERTAIN:                                                                            |
|    IF Conflicting Evidence == True OR Confidence == INSUFFICIENT OR Sensitive to Perturbation     |
+--------------------------------------------------------------------------------------------------+
```

---

## 5. Confidence Engine & Family Independence

Confidence is not a Bayesian posterior probability of truth; it is an evidence quality and triangulation score based on:
1. **Independent Family Count ($N_{\text{fam}}$):** Number of distinct statutory, multilateral, and academic families providing corroborating signals. Multiple records from the same report count as 1 family.
2. **Quality Tier Weighting:** Tier A statutory evidence carries maximum authority ($1.0$), Tier B multilateral benchmark ($0.85$), Tier C scholarly infrastructure ($0.70$).
3. **Conflict Penalties:** Disagreement between demand shortages and high automation vulnerability incurs a 15–20 point penalty.
4. **Freshness Degradation:** Data exceeding 24 months without scheduled updates incurs an aging penalty.

### Categorical Tiers:
- **HIGH:** $\text{Index} \ge 75$ AND $N_{\text{fam}} \ge 3$ AND no unmitigated conflict.
- **MEDIUM:** $\text{Index} \ge 50$ AND $N_{\text{fam}} \ge 2$.
- **LOW:** $\text{Index} \ge 25$ OR single-source evidence.
- **INSUFFICIENT:** $\text{Index} < 25$ OR no direct signals.
