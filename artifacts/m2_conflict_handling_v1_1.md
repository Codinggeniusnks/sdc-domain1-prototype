# M2 Conflict Handling and Resolution Architecture (v1.1.0)

## Executive Summary

Labour market trend intelligence frequently encounters seemingly contradictory evidence streams: an occupation may experience severe acute labor shortages while simultaneously exhibiting high vulnerability to generative AI exposure. 

In M2 v1.1.0, a formal **Four-Tier Conflict Taxonomy** and deterministic resolution engine were implemented to resolve divergent signals transparently and prevent simplistic or contradictory classifications.

---

## The Four-Tier Conflict Taxonomy

```
+--------------------------------------------------------------------------+
|                       M2 Signal Conflict Taxonomy                        |
+--------------------------------------------------------------------------+
| 1. NO_CONFLICT                                                           |
|    - All evidence streams agree directionally.                           |
|    - Example: Accounting Clerks (4311) - Low demand, high automation.    |
+--------------------------------------------------------------------------+
| 2. CROSS_DIMENSION_TENSION                                               |
|    - High demand / shortage coincides with high AI exposure.             |
|    - Resolution: Task-level Augmentation vs Automation Decomposition.    |
|    - Example: Software Developers (2512), Systems Analysts (2511).       |
+--------------------------------------------------------------------------+
| 3. WITHIN_DIMENSION_CONFLICT                                             |
|    - Conflicting reports within the same analytical dimension.           |
|    - Resolution: Statutory Institutional Hierarchy Weighting.            |
|    - Example: Divergent vacancy counts between survey and job portal.    |
+--------------------------------------------------------------------------+
| 4. HIGH_UNCERTAINTY                                                      |
|    - Multidirectional divergence without decisive institutional consensus|
|    - Resolution: Flag as UNCERTAIN; widen downstream confidence bounds.  |
+--------------------------------------------------------------------------+
```

---

## Detailed Resolution Mechanics

### 1. Resolving Cross-Dimension Tension via Augmentation Decomposition

The most common apparent contradiction occurs in highly skilled professional roles:
- **Employer Demand**: TalentCorp MyCOL indicates critical shortage (Status: `PERSISTENT_CRITICAL`).
- **AI Exposure**: ILO Working Paper 140 indicates high AI exposure ($62.0\%$).

#### The Resolution Algorithm:
Rather than averaging these two opposing signals into an uninformative "Neutral" or "Stable" outlook, M2 evaluates the **Augmentation-to-Automation Ratio**:

$$R_{\text{aug/auto}} = \frac{\text{Augmentation Potential}}{\text{Automation Potential}}$$

1. **If $R_{\text{aug/auto}} \ge 2.0$**: The role is classified as **`STRONGLY RISING`** or **`RISING`** with conflict status **`CROSS_DIMENSION_TENSION`**. AI exposure acts as a productivity multiplier that intensifies demand for workers who can leverage AI tools.
   - *Empirical Example*: **Software Developers (2512)**
     - Demand Shortage: $89.6$
     - AI Exposure: $62.0\%$ (Augmentation: $54.0\%$, Automation: $8.0\%$)
     - Ratio: $R = \frac{54.0}{8.0} = 6.75$
     - Outlook: **`STRONGLY RISING`**
     - Conflict Note: *"Simultaneous high occupational shortage/demand and significant AI exposure (62.0), resolved via dominant augmentation potential (54.0 vs automation 8.0)."*

2. **If $R_{\text{aug/auto}} \le 1.0$**: The role is subject to genuine displacement. High AI exposure represents substitution rather than enhancement.
   - *Empirical Example*: **General Office Clerks (4110)**
     - Demand Shortage: $0.0$ (Non-critical)
     - AI Exposure: $45.0\%$ (Augmentation: $10.0\%$, Automation: $35.0\%$)
     - Ratio: $R = \frac{10.0}{35.0} = 0.29$
     - Outlook: **`STRONGLY DECLINING`**
     - Conflict Status: **`NO_CONFLICT`** (demand and automation both push downward).

3. **If $1.0 < R_{\text{aug/auto}} < 2.0$**: Transition zone with mixed restructuring.
   - *Empirical Example*: **Administrative Secretaries (3343)**
     - Under ILO 2025 WP 140: Automation ($25.0\%$) now exceeds augmentation ($17.0\%$).
     - Ratio: $R = 0.68$.
     - Outlook: **`DECLINING`** (Shifted from `MIXED / UNCERTAIN` in v1.0.0).

---

### 2. Resolving Within-Dimension Conflict via Institutional Hierarchy

When two sources report conflicting values for the same parameter (e.g., skill demand trend):
1. **Tier 1 (Authoritative National Mandate)**: TalentCorp MyCOL, OpenDOSM, MOSTI/EPU national directives. (Weight = 1.0)
2. **Tier 2 (Authoritative Multilateral Bodies)**: ILO, World Bank, OECD. (Weight = 0.85)
3. **Tier 3 (Global Research Literature)**: OpenAlex scientometrics. (Weight = 0.70)
4. **Tier 4 (Market Job Scrapes / Unverified Portals)**: (Weight = 0.50)

Higher-tier sources override lower-tier contradictions by default, with discordance logged in the `uncertainties` array.

---

## Complete Audit of Conflicts in v1.1.0 Profiles

| Domain | Entity ID | Entity Title | Conflict Status | Resolution Mechanism Applied | Resulting Outlook |
| :--- | :---: | :--- | :---: | :--- | :---: |
| **Skill** | `ai_literacy` | Foundational AI Literacy | `CROSS_DIMENSION_TENSION` | High demand (87.9) + High Augmentation (78.0) | `STRONGLY RISING` |
| **Skill** | `prompt_engineering` | Structured Prompting | `CROSS_DIMENSION_TENSION` | Demand (80.0) + Augmentation (78.0) | `RISING` |
| **Skill** | `sql_data_analysis` | SQL & Structured Data | `NO_CONFLICT` | Consistent positive across all streams | `STRONGLY RISING` |
| **Occupation** | `2512` | Software Developers | `CROSS_DIMENSION_TENSION` | Ratio $6.75\times$ favors augmentation | `STRONGLY RISING` |
| **Occupation** | `2511` | Systems Analysts | `CROSS_DIMENSION_TENSION` | Ratio $5.88\times$ favors augmentation | `STRONGLY RISING` |
| **Occupation** | `2166` | Graphic Designers | `CROSS_DIMENSION_TENSION` | Ratio $2.22\times$ (Aug 40% vs Auto 18%) | `STABLE` |
| **Occupation** | `3343` | Administrative Secretaries | `NO_CONFLICT` | Auto (25%) > Aug (17%), low demand | `DECLINING` |
| **Occupation** | `4110` | General Office Clerks | `NO_CONFLICT` | Auto (35%) > Aug (10%), zero shortage | `STRONGLY DECLINING` |
| **Occupation** | `4311` | Accounting Clerks | `NO_CONFLICT` | Auto (38%) > Aug (12%), zero shortage | `STRONGLY DECLINING` |

---

## Downstream Interface Safety (M3 & M6)

1. **Role Transition Guidance in M3**: When an occupation has `CROSS_DIMENSION_TENSION`, M3 must NOT advise candidates to abandon the role. Instead, M3 generates an **"Augmentation Pivot"** recommendation: upskill in AI tool orchestration within the role.
2. **Displacement Warnings**: When an occupation has `NO_CONFLICT` with dominant automation (e.g. 4110, 4311), M3 displays a high-priority career transition advisory into adjacent technical roles (e.g. 2511, 2521).
