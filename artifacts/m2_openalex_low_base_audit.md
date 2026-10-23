# M2 OpenAlex Low-Base Research Momentum Audit (v1.1.0)

## Executive Summary

During the Stage 9C Argon Forensic Audit, Defect **P2-4** revealed that scientometric indicators from OpenAlex exhibited distorted velocity ratios for nascent generative AI skills. Specifically, skills that did not exist in academic literature prior to the release of ChatGPT in late 2022 had baseline counts of $N \le 2$ papers during the 2020–2023 baseline window. When 15–20 papers were published in 2024–2026, raw velocity ratios exploded to $15\times$–$20\times$, generating artificial 100.0 saturation in v1.0.0.

In M2 v1.1.0, this was remediated through:
1. **Bayesian Volume Shrinkage Damping**.
2. **Automated Low-Base Flagging (`LOW_BASE_RESEARCH_SIGNAL`)**.
3. **Explicit Uncertainty Disclosures** in the generated profile schema.

---

## The Low-Base Phenomenon

In academic bibliometrics, a transition from 1 paper to 18 papers represents an $18.0\times$ increase, whereas a transition from 500 papers to 1,500 papers represents a $3.0\times$ increase. However, the latter represents 1,000 net new peer-reviewed studies reflecting immense global scientific consensus, while the former represents a small handful of workshop or conference papers.

In M2 v1.0.0, both received a flat 100.0 `research_momentum_index`, distorting skill comparisons.

### Empirical Evidence from OpenAlex Snapshot

| Skill ID | Baseline Papers (2020–2023) | Recent Papers (2024–2026) | Raw Velocity Ratio | Damped Velocity Ratio | Low-Base Flag Attached |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `prompt_engineering` | 1 | 18 | 18.0x | **17.1x** | **`LOW_BASE_RESEARCH_SIGNAL`** |
| `rag_knowledge_systems` | 2 | 22 | 11.0x | **10.2x** | **`LOW_BASE_RESEARCH_SIGNAL`** |
| `ai_literacy` | 14 | 121 | 11.2x | **10.5x** | *None ($N \ge 5$)* |
| `workflow_automation` | 8 | 54 | 6.8x | **6.4x** | *None ($N \ge 5$)* |
| `sql_data_analysis` | 180 | 320 | 1.8x | **1.8x** | *None ($N \ge 5$)* |
| `python_scripting` | 310 | 620 | 2.0x | **2.0x** | *None ($N \ge 5$)* |

---

## Mathematical Remediation: Bayesian Volume Damping

To prevent small sample sizes from producing runaway momentum scores, M2 v1.1.0 implements a volume shrinkage transform:

$$R_{\text{damped}} = 1.0 + (R_{\text{raw}} - 1.0) \cdot \left(\frac{N_{\text{recent}}}{N_{\text{recent}} + K}\right)$$

Where:
- $R_{\text{raw}} = \frac{N_{\text{recent}}}{N_{\text{baseline}}}$
- $K = 10.0$ (Bayesian prior weight representing the threshold for minimal statistical mass).
- When $N_{\text{recent}}$ is small, $R_{\text{damped}}$ is pulled toward the neutral baseline (1.0).
- When $N_{\text{recent}} \gg 100$, the scaling factor approaches $1.0$, leaving mature literature unaffected.

Furthermore, research momentum is asymptotically bounded to a ceiling of $95.0$, preventing saturation.

---

## Schema Quality Flags and Uncertainty Emitted

For every skill where $N_{\text{baseline}} < 5$, M2 v1.1.0 automatically emits:
1. **Quality Flag**: `LOW_BASE_RESEARCH_SIGNAL`
2. **Uncertainty Narrative**: *"Research velocity is based on a small historical publication sample (< 5 papers in 2020-2023)."*
3. **Confidence Impact**: Skills bearing this flag cannot achieve a `HIGH` confidence tier without compensating evidence from at least 3 other high-volume institutional families. As a result, `prompt_engineering` and `rag_knowledge_systems` are correctly classified as **`LOW`** confidence (40.0).

---

## Guidance for Downstream Modules (M3 & M6)

1. **M3 Skill Recommendation**: Skills tagged with `LOW_BASE_RESEARCH_SIGNAL` should be recommended as *emerging micro-credentials* rather than foundational career anchors.
2. **M6 Scenario Engine**: In workforce transformation simulations, low-base skills must have wider diffusion uncertainty distributions ($\sigma = 0.35$ vs $\sigma = 0.15$ for mature skills).
