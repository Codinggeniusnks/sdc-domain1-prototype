# M2 AI Trend Intelligence Engine: Normalisation & Scaling Specification

**Author:** Senior Labour-Market Data Engineer, AI Trend Research Engineer & ML Systems Architect  
**Date:** 2026-10-23  
**Stage:** Stage 9A Data Foundation & Evidence Architecture  
**Specification Version:** 1.0.0  

---

## 1. Mathematical Principles & Boundaries

Data ingested across Tier A, B, and C sources originate in radically different measurement units:
- Binary critical list inclusions (0 or 1 per edition)
- Monthly unemployment percentages (e.g. 3.3%)
- Monthly median salaries in Malaysian Ringgit (e.g. RM 4,800)
- Task-based exposure proportions (e.g. 0.48)
- Scholarly publication counts and citation rates (e.g. 42 papers, 18.5 citations/paper)
- Qualitative workforce transition classifications (Emerging, Transforming, Declining)

### Hard Invariance Rules:
1. **Bounded Domain:** Every normalized signal value (`signal_value_normalized`) MUST be strictly bounded in the closed interval $[0.0, 1.0]$.
2. **Preservation of Raw Values:** The raw, unscaled value and its native units MUST be preserved verbatim in `signal_value_raw` to maintain complete auditability and prevent false precision.
3. **No Stage 9A Fusion Weights:** Stage 9A standardizes component signals only. No arbitrary composite weights (e.g., "40% MyCOL + 30% OpenAlex + 20% ILO + 10% DOSM") are permitted. Evidence fusion equations are reserved for Stage 9B.

---

## 2. Source-Specific Normalisation Formulas

### 2.1. TalentCorp MyCOL Longitudinal Signals

MyCOL is evaluated over 8 national publication editions ($E = 8$) spanning 2015/2016 through 2024/2025.

#### Persistence Score Formula:
$$\text{Persistence}(o) = \frac{\sum_{e=1}^{E} \mathbb{I}(\text{Critical}_{e}(o))}{E}$$
where $\mathbb{I}(\cdot) \in \{0, 1\}$ indicates inclusion as a critical shortage occupation in edition $e$.

#### Status Classification & Direction Logic:
- **Persistent Critical:** $\text{Persistence}(o) \ge 0.75$ (critical in $\ge 6/8$ editions). Direction: `STRONGLY RISING`. Normalized score: $\text{Persistence}(o)$ (0.75 to 1.00).
- **Newly Critical:** First appeared in 2022/2023 or 2024/2025 with zero inclusions prior to 2021. Direction: `RISING`. Normalized score: $0.75 + 0.125 \times (\text{editions} - 1)$.
- **Cyclical Critical:** Appeared sporadically ($0.25 \le \text{Persistence}(o) < 0.75$). Direction: `STABLE`. Normalized score: $\text{Persistence}(o)$.
- **Dropped from Latest:** Listed in earlier editions but absent in 2024/2025. Direction: `DECLINING`. Normalized score: $\max(0.10, \text{Persistence}(o) \times 0.5)$.

---

### 2.2. OpenDOSM Macroeconomic & Wage Signals

#### Unemployment Health Index:
To map national unemployment rate $U \in [0\%, 10\%]$ into a $[0.0, 1.0]$ macro health indicator where lower unemployment yields a higher economic vitality score:
$$S_U = \text{clamp}\left(0.0, \frac{6.0 - U}{3.0}, 1.0\right)$$
- If $U = 3.0\%$, $S_U = 1.00$ (Optimal full employment).
- If $U = 4.5\%$, $S_U = 0.50$ (Moderate slack).
- If $U \ge 6.0\%$, $S_U = 0.00$ (Severe macroeconomic contraction).

#### Occupational Wage Benchmark:
Given the median wage $W_m$ for occupational major group $m$ and the maximum median occupational wage in the national series $W_{\max} = \max_{j} W_j$ (Managers: ~RM 6,500):
$$S_W(m) = \text{clamp}\left(0.0, \frac{W_m}{W_{\max}}, 1.0\right)$$
Direction assignment reflects the 5-year compound annual growth rate (CAGR):
$$\text{CAGR} = \left(\frac{W_{t}}{W_{t-5}}\right)^{1/5} - 1$$
- $\text{CAGR} \ge 4.0\%$: `RISING`
- $1.5\% \le \text{CAGR} < 4.0\%$: `STABLE`
- $\text{CAGR} < 1.5\%$: `DECLINING`

---

### 2.3. ILO Generative AI Task Exposure & Augmentation

From ILO Working Paper 96, task-level exposure is decomposed into autonomous task displacement ($\text{Auto}$) and cognitive tool enhancement ($\text{Aug}$):

#### Normalization:
Both metrics natively range between $0.00$ and $1.00$ representing the percentage of occupational task hours affected:
$$S_{\text{Auto}} = \text{clamp}(0.0, \text{Auto}, 1.0)$$
$$S_{\text{Aug}} = \text{clamp}(0.0, \text{Aug}, 1.0)$$

#### Direction Assignment:
- If $S_{\text{Aug}} \ge 0.35$ and $S_{\text{Auto}} < 0.10$: `STRONGLY RISING` (High complementary productivity gain).
- If $S_{\text{Aug}} \ge 0.20$ and $S_{\text{Auto}} < 0.15$: `RISING`.
- If $S_{\text{Auto}} \ge 0.20$ and $S_{\text{Auto}} > S_{\text{Aug}}$: `DECLINING` (Net task displacement vulnerability, as in routine clerical tasks).
- If $S_{\text{Auto}} < 0.05$ and $S_{\text{Aug}} < 0.05$: `STABLE` (Low exposure physical/manual roles).

---

### 2.4. OpenAlex Research Momentum Signals

#### 1. Research Volume Normalization:
Given publication volume $V(s)$ for skill topic $s$ and the maximum volume across all 16 skills $V_{\max} = \max_j V(j)$:
$$S_{\text{Vol}}(s) = \frac{V(s)}{V_{\max}}$$

#### 2. Research Growth Velocity Ratio:
To capture research momentum while preventing small-sample explosion, compare the annualized publication rate during the recent window ($W_{\text{recent}} = 2024\text{--}2026$, 3 years) against the historical baseline ($W_{\text{base}} = 2020\text{--}2023$, 4 years) with a smoothing prior $\epsilon = 0.1$:
$$G_{\text{ratio}}(s) = \frac{V_{\text{recent}}(s) / 3.0}{(V_{\text{base}}(s) / 4.0) + \epsilon}$$
$$S_{\text{Growth}}(s) = \text{clamp}\left(0.0, \frac{G_{\text{ratio}}(s)}{2.0}, 1.0\right)$$
- If $G_{\text{ratio}} \ge 2.0\times$ (doubling of publication rate): $S_{\text{Growth}} = 1.00$ (`STRONGLY RISING`).
- If $1.2\times \le G_{\text{ratio}} < 2.0\times$: $S_{\text{Growth}} \in [0.60, 0.99]$ (`RISING`).
- If $0.8\times \le G_{\text{ratio}} < 1.2\times$: $S_{\text{Growth}} \in [0.40, 0.59]$ (`STABLE`).
- If $G_{\text{ratio}} < 0.8\times$: `DECLINING`.

---

### 2.5. Policy Priority Signals

Statutory and national industrial policies are mapped using a documented ordinal scale based on regulatory enforcement strength:

| Policy Status | Legal Force | Normalized Score | Direction |
| :--- | :--- | :---: | :--- |
| `ENACTED_LEGISLATION` | Mandatory statutory law (e.g. PDPA 2024 Act A1720) | $1.00$ | `STRONGLY RISING` |
| `MANDATORY_REGULATION` | Capital market listing rule (e.g. Bursa ESG Scope 1-3) | $1.00$ | `STRONGLY RISING` |
| `ACTIVE_MANDATE` | National guidelines with ministerial oversight (e.g. MOSTI AIGE) | $0.90$ | `STRONGLY RISING` |
| `ACTIVE_NATIONAL_PRIORITY` | National investment strategy with funded targets (e.g. MITI NSS RM25B) | $0.90$ | `RISING` |
| `ACTIVE_STRATEGIC_PLAN` | Macro-development blueprint (e.g. MyDIGITAL) | $0.85$ | `RISING` |

---

## 3. Direction Enumeration Summary

Every signal is deterministically assigned one of six standardized directional classifications:

```
[STRONGLY DECLINING] <--- [DECLINING] <--- [STABLE / MIXED] ---> [RISING] ---> [STRONGLY RISING]
      (<= -25%)             (-10% to -25%)       (-10% to +10%)      (+10% to +25%)       (>= +25%)
```
This guarantees uniform downstream interpretability when the M2 scoring engine aggregates multiple signals in Stage 9B.
