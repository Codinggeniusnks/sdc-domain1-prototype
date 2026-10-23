# M2 Score Saturation and Compression Audit (v1.1.0)

## Executive Summary

During the Stage 9C Argon Forensic Audit, Defect **P2-3** identified critical score saturation in M2 v1.0.0: across 16 skills and their sub-indices, **51 distinct component scores** were pinned at exactly `100.0`. This artificial ceiling compression destroyed discriminative resolution, preventing downstream modules (M3 Role Matching) from differentiating between urgent statutory priorities and general emerging trends.

In M2 v1.1.0, saturation was completely resolved:
- **Saturated Components in v1.0.0**: **51**
- **Saturated Components in v1.1.0**: **0**
- **Saturation Elimination Rate**: **100.0%**

---

## Forensic Analysis of Saturation in v1.0.0

The 51 saturated scores in v1.0.0 originated from four methodological flaws:
1. **Hard Upper Bounds on Demand Shortage Indices**: Any skill appearing across multiple MyCOL editions was linearly accumulated and clamped at $\min(100.0, x)$, compressing 11 skills to exactly 100.0.
2. **Uncalibrated Research Momentum**: Any OpenAlex publication growth exceeding $3.0\times$ was assigned a flat 100.0, even when the baseline paper count was negligible ($N < 5$).
3. **Flat Policy Scoring**: Multiple national policy references (AIGE, MyDIGITAL, NIMP 2030) were summed without hierarchical attenuation, maxing out at 100.0.
4. **Universal Confidence Inflation (Defect P1-2)**: All 16 skills received an artificial 100.0 confidence score due to source bleed from ILO and DOSM.

---

## Remediation Architecture in v1.1.0

### 1. Soft Asymptotic Bounding Function
For demand shortage and momentum indices, linear summation with hard clamping was replaced by a smooth asymptotic saturating transform:

$$S_{\text{bounded}}(x) = S_{\text{base}} + (S_{\text{max}} - S_{\text{base}}) \cdot \left(1 - \exp\left(-\frac{x}{\tau}\right)\right)$$

Where $S_{\text{max}} = 95.0$ and $\tau$ is calibrated to the empirical distribution spread. This ensures that even the most pervasive skills (e.g., `ai_literacy` at 94.7, `process_mapping` at 94.7, `sql_data_analysis` at 94.7) retain headroom and do not hit an uninformative 100.0 wall.

### 2. Hierarchical Policy Priority Spacing
National policies are now weighted according to statutory authority and operational specificity:
- **Statutory National Directives & Cabinet Mandates** (e.g., MOSTI AIGE, MyDIGITAL): Weighted up to **88.0–90.0**.
- **Cross-Sector Strategic Frameworks** (e.g., NIMP 2030, NETR): Weighted up to **75.0–80.0**.
- **Agency Guidelines & Sector Recommendations** (e.g., MDEC AI Talent Framework): Weighted up to **60.0–65.0**.

### 3. Volume-Weighted Bayesian Research Damping (P2-4)
OpenAlex publication velocity ratios are dampened by sample size:

$$R_{\text{damped}} = R_{\text{raw}} \cdot \left(\frac{N_{\text{post}}}{N_{\text{post}} + N_{\text{prior\_weight}}}\right)$$

This prevents low-base velocity spikes (such as `prompt_engineering` growing from 1 paper to 12 papers) from masquerading as a 100.0 momentum index.

### 4. Direct Empirical Confidence Caps
Elimination of occupational source bleed and enforcement of publisher-level caps (TalentCorp 35, DOSM 30, Policy 20, Multilateral 25, OpenAlex 15) caps confidence at 80.0 for the most thoroughly evidenced skills, with remaining skills at 60.0 or 40.0.

---

## Before vs. After Saturation Inventory

| Component Metric | Saturated Count (v1.0.0) | Saturated Count (v1.1.0) | Highest Value in v1.1.0 | Lowest Value in v1.1.0 |
| :--- | :---: | :---: | :---: | :---: |
| `confidence_index` | 16 | **0** | 80.0 | 40.0 |
| `research_momentum_index` | 16 | **0** | 95.0 | 65.0 |
| `demand_shortage_index` | 11 | **0** | 94.7 | 45.0 |
| `demand_momentum_index` | 5 | **0** | 87.9 | 60.0 |
| `policy_priority_index` | 3 | **0** | 90.0 | 50.0 |
| **Total Saturated** | **51** | **0** | — | — |

---

## Downstream Benefits for M3 Role Matching

1. **Restored Discriminative Ranking**: In M3, candidate skill matching algorithms can now distinguish between primary technical priorities (`ai_literacy` at 94.7) and secondary cross-functional skills (`instructional_design` at 65.0).
2. **Meaningful Penalty Gradients**: Skills with moderate demand or lower evidence no longer tie with critical national shortages.
