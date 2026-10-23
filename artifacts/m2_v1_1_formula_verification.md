# M2 v1.1 OpenAlex Damping Formula & Arithmetic Forensic Verification

## 1. Executive Summary & Audit Mandate

During the Post-Remediation Review of M2 Trend Intelligence v1.1.0, a mandatory forensic audit of the **OpenAlex Low-Base Research Momentum Damping** was conducted to verify mathematical consistency between declared methodology and actual code implementation.

The Stage 9D documentation ([m2_openalex_low_base_audit.md](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/artifacts/m2_openalex_low_base_audit.md)) stated:
$$R_{\text{damped}} = 1.0 + (R_{\text{raw}} - 1.0) \cdot \left(\frac{N_{\text{recent}}}{N_{\text{recent}} + K}\right) \quad \text{with } K = 10.0$$
And reported in its summary table:
- `prompt_engineering`: $N_{\text{baseline}} = 1, N_{\text{recent}} = 18, R_{\text{raw}} = 18.0x, R_{\text{damped}} = 17.1x$
- `rag_knowledge_systems`: $N_{\text{baseline}} = 2, N_{\text{recent}} = 22, R_{\text{raw}} = 11.0x, R_{\text{damped}} = 10.2x$

An immediate mathematical evaluation reveals that the written formula yields:
- For `prompt_engineering`: $1 + (18 - 1) \cdot \frac{18}{18 + 10} = 1 + 17 \cdot \frac{18}{28} \approx 11.93 \neq 17.1$
- For `rag_knowledge_systems`: $1 + (11 - 1) \cdot \frac{22}{22 + 10} = 1 + 10 \cdot \frac{22}{32} \approx 7.875 \neq 10.2$

This document presents the deterministic audit findings from inspecting the underlying raw data, the production script, and the generated profile artifacts.

---

## 2. Forensic Code & Data Inspection Findings

### A. The Underlying Raw OpenAlex Data
In [openalex_temporal_momentum.json](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/trends/raw/openalex/openalex_temporal_momentum.json):
```json
"prompt_engineering": {
  "baseline_count_2020_2023": 1,
  "recent_count_2024_2026": 18,
  "growth_rate_ratio": 17.143
},
"rag_knowledge_systems": {
  "baseline_count_2020_2023": 1,
  "recent_count_2024_2026": 30,
  "growth_rate_ratio": 28.571
}
```
*Key Finding 1*: The raw file `growth_rate_ratio` for `prompt_engineering` is **17.143** (due to baseline smoothing in the extraction query).

### B. The Actual Implemented Code in `scripts/build_trend_scores_v1_1.py`
Inspection of lines 460–474 reveals:
```python
# Line 470 in scripts/build_trend_scores_v1_1.py:
vol_weight = min(1.0, math.log(1.0 + base_count) / math.log(1.0 + 25.0))
damped_growth = 1.0 + (raw_growth - 1.0) * vol_weight
research_momentum = round(max(10.0, min(95.0, damped_growth * 38.0)), 1)
```
*Key Finding 2*: The code did **NOT** implement the rational function $N_{\text{recent}} / (N_{\text{recent}} + K)$.  
Instead, it implemented a **logarithmic shrinkage function based on $N_{\text{baseline}}$**:
$$w_{\text{vol}} = \min\left(1.0, \frac{\ln(1 + N_{\text{baseline}})}{\ln(26)}\right)$$
$$R_{\text{damped}} = 1.0 + (R_{\text{raw}} - 1.0) \cdot w_{\text{vol}}$$

### C. The Format String Defect in Line 623
Inspection of lines 612–624 reveals:
```python
# Line 623 in scripts/build_trend_scores_v1_1.py:
"summary": f"Publication velocity ratio of {srm.get('growth_rate_ratio', 1.0):.1f}x ({srm.get('recent_count_2024_2026', 0)} papers in 2024-2026 vs {srm.get('baseline_count_2020_2023', 0)} baseline, volume-damped)."
```
*Key Finding 3*: Line 623 interpolates `{srm.get('growth_rate_ratio', 1.0):.1f}x` — which is the **RAW** ratio from OpenAlex (17.143 $\to$ 17.1x) — and appends the label `", volume-damped"`!  
The generated profile JSON literally displayed the un-damped raw ratio while claiming it was volume-damped.

---

## 3. Deterministic Arithmetic Test & Comparison

A deterministic test was executed via `scripts/verify_check4.py`:

| Skill | $N_{\text{base}}$ | $N_{\text{recent}}$ | Raw $R$ in JSON | Code Implemented $R_{\text{damped}}$ | Documented Formula $R_{\text{damped}}$ | Reported Value in Stage 9D |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `prompt_engineering` | 1 | 18 | **17.143** | **4.434** | **11.378** | *17.1x (WRONG)* |
| `rag_knowledge_systems` | 1 | 30 | **28.571** | **6.866** | **21.678** | *10.2x (WRONG)* |
| `ai_literacy` | 14 | 121 | **11.204** | **9.481** | **10.425** | *10.5x* |
| `workflow_automation` | 2 | 33 | **18.333** | **6.845** | **14.302** | *6.4x* |
| `sql_data_analysis` | 5 | 18 | **4.444** | **2.894** | **3.214** | *1.8x* |
| `python_scripting` | 5 | 22 | **5.432** | **3.437** | **4.047** | *2.0x* |

### Detailed Evaluation of Question Options:
- **A. Formula in documentation is WRONG**: YES. The documentation wrote a rational formula $N_{\text{recent}} / (N_{\text{recent}} + K)$ while the code implemented logarithmic shrinkage on $N_{\text{baseline}}$.
- **B. Reported values in documentation are WRONG**: YES. The values reported in the Stage 9D table (17.1x, 10.2x) did not match either formula. 17.1x was actually the raw ratio from the JSON file!
- **C. Implementation is WRONG**: PARTIALLY. The mathematical implementation in line 470 ($\ln(1 + \text{base})/\ln(26)$) is a valid, elegant shrinkage formula that effectively reduces 17.143 to 4.434. However:
  1. Line 623 had a bug printing raw `growth_rate_ratio` instead of `damped_growth`.
  2. Line 472 multiplied `damped_growth` by 38.0, meaning $4.434 \times 38 = 168.5$, which saturated at the 95.0 ceiling regardless of damping!
- **D. Another variable is actually used**: YES. The code used `base_count` ($N_{\text{baseline}}$), not $N_{\text{recent}}$.

---

## 4. Evaluation of Low-Base Material Effect (Check 5)

Comparing the code's logarithmic shrinkage behavior across scale:
1. **$1 \to 18$ (`prompt_engineering`)**: $N_{\text{base}} = 1 \implies w = \frac{\ln(2)}{\ln(26)} = 0.2127$. Excess velocity is reduced by **$78.7\%$** ($17.143 \to 4.434$).
2. **$2 \to 22$ (hypothetical / `workflow_automation`)**: $N_{\text{base}} = 2 \implies w = \frac{\ln(3)}{\ln(26)} = 0.3372$. Excess velocity is reduced by **$66.3\%$**.
3. **$14 \to 121$ (`ai_literacy`)**: $N_{\text{base}} = 14 \implies w = \frac{\ln(15)}{\ln(26)} = 0.8312$. High volume retains **$83.1\%$** of signal strength.

*Conclusion*: The logarithmic shrinkage on baseline volume $N_{\text{base}}$ is scientifically superior to shrinkage on $N_{\text{recent}}$, because low-base distortion is fundamentally caused by a near-zero denominator ($N_{\text{base}} \le 2$), not the numerator. However, the documentation formula, the line 623 display bug, and the multiplier must be formally reconciled.

---

## 5. Required Actionable Remediation Items

Before M2 v1.1 can be frozen, the following targeted fix must be executed:
1. **Code Format Fix**: In `scripts/build_trend_scores_v1_1.py` line 623, replace `{srm.get('growth_rate_ratio', 1.0):.1f}x` with `{damped_growth:.1f}x` so the generated citation summary truthfully displays the damped velocity.
2. **Documentation Formula Reconciliation**: In `artifacts/m2_openalex_low_base_audit.md`, document the exact logarithmic formula implemented in code:
   $$R_{\text{damped}} = 1.0 + (R_{\text{raw}} - 1.0) \cdot \min\left(1.0, \frac{\ln(1 + N_{\text{baseline}})}{\ln(1 + N_{\text{threshold}})}\right)$$
   and replace the inconsistent table entries with verified recomputed values.
3. **Multiplier Calibration**: Adjust the research momentum multiplier or apply soft-bounding directly to prevent damped values from re-saturating at 95.0.
