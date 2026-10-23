# M2 AI Trend Intelligence Engine: Forensic Review of Backtesting Methodology

**Reviewer:** Quantitative Research Reviewer & Statistical Auditor  
**Date:** 2026-10-23  
**Stage:** Stage 9C High-Value Methodology Review  
**Subject Artifacts:** `artifacts/m2_component_backtest.csv` & `artifacts/m2_backtest_report.md`  
**Evaluation Outcome:** **RECLASSIFIED AS LIMITED DIRECTIONAL ALIGNMENT CHECK**  

---

## 1. Executive Summary & Review Objective

Stage 9B reported a **97.5% component backtest accuracy** (39 / 40 tests aligned) across TalentCorp MyCOL, OpenDOSM Salaries & Wages, and OpenAlex Scholarly Corpus. This forensic review was commissioned to investigate:
1. Potential direct or indirect look-ahead leakage.
2. Circularity in feature construction.
3. Baseline difficulty and class balance.
4. Whether the reported alignment represents genuine out-of-sample predictive power or trivial directional persistence.

---

## 2. Source-by-Source Forensic Audit

### 2.1. OpenAlex Research Velocity Backtest (16 Tests)
- **Reported Metric:** Publication velocity ratio $G_{\text{ratio}} \ge 1.2$ during 2020–2023 predicting publication acceleration in 2024–2026.
- **Forensic Finding (Circularity & In-Sample Leakage):**
  - In `openalex_temporal_momentum.json` and `scripts/build_trend_scores.py`, the metric is calculated as:
    $$G_{\text{ratio}}(s) = \frac{V_{\text{recent}}(s) / 3.0}{(V_{\text{base}}(s) / 4.0) + \epsilon}$$
    where $V_{\text{recent}}$ is the publication count during **2024–2026**, and $V_{\text{base}}$ is the count during **2020–2023**.
  - The backtest script then evaluated:
    ```python
    pred_rising = ratio >= 1.2
    actual_rising = rec_count > base_count
    ```
  - **Fatal Methodological Defect:** $G_{\text{ratio}}$ was constructed **using the 2024–2026 data in its numerator**. Testing whether an index containing $V_{\text{recent}}$ predicts whether $V_{\text{recent}} > V_{\text{base}}$ is a mathematical tautology (in-sample definition check), NOT an out-of-sample predictive test.
  - A valid predictive backtest would require calculating velocity between 2017–2019 ($V_{\text{prior}}$) and 2020–2022 ($V_{\text{base}}$), and using *that* historical ratio to predict 2023–2026 growth.

### 2.2. TalentCorp MyCOL Criticality Persistence Backtest (20 Tests)
- **Reported Metric:** Leave-one-out historical criticality across Editions 1–7 predicting Edition 8 (2024/2025).
- **Forensic Finding (Trivial Persistence Baseline):**
  - In `scripts/build_trend_scores.py`:
    ```python
    pred_critical = (n_prior >= 4) or r.get("newly_critical", False)
```
  - **Indirect Look-Ahead:** `r.get("newly_critical")` is an attribute extracted from the full 8-edition longitudinal series summary table. In Edition 7, an analyst would not have access to the retrospective 8-edition label.
  - **Naive Persistence Baseline Comparison:**
    - If a naive baseline simply predicts: "An occupation critical in $\ge 50\%$ of past editions remains critical in the next edition", it achieves **95.0% accuracy** (19 / 20).
    - Malaysian occupational shortages are heavily structural (e.g. software developers, systems analysts, civil engineers experience chronic shortages spanning a decade). High accuracy is a property of macroeconomic inertia, not sophisticated model prediction.

### 2.3. OpenDOSM Salaries & Wages Directional Sign Backtest (4 Tests)
- **Reported Metric:** 2018–2021 wage momentum predicting positive wage growth in 2022–2025 across 4 major groups.
- **Forensic Finding (Trivial Macroeconomic Baseline):**
  - Nominal median wages in Malaysia have trended upward across broad occupational major groups in virtually every rolling 3-year window over the past 15 years.
  - A naive "Always Positive" baseline achieves **100.0% accuracy** (4 / 4).
  - With $N = 4$ aggregated categories, the sample size is statistically insufficient to claim empirical model validation.

---

## 3. Baseline Comparison Table

| Source Family | Stage 9B Reported Alignment | Naive Historical Baseline | Baseline Description | Net Informational Value Above Baseline |
| :--- | :---: | :---: | :--- | :---: |
| **OpenAlex Scholarly** | 100.0% (16/16) | 100.0% (In-sample) | Mathematical tautology ($G_{\text{ratio}}$ embeds numerator) | **0.0%** (In-sample circularity) |
| **TalentCorp MyCOL** | 95.0% (19/20) | 95.0% (19/20) | Naive persistence ($\ge 4$ editions critical remains critical) | **0.0%** (Macroeconomic inertia) |
| **OpenDOSM Wages** | 100.0% (4/4) | 100.0% (4/4) | Naive always-positive nominal wage drift | **0.0%** (Aggregate nominal drift) |
| **OVERALL ENGINE** | **97.5% (39/40)** | **97.5% (39/40)** | **Combined Inertia & Definition Baseline** | **0.0% Net Predictive Gain** |

---

## 4. Methodological Reclassification & Recommendations

### Formal Reclassification:
The claim of **"97.5% Predictive Backtest Accuracy"** is scientifically unsupportable and must be formally struck from system documentation. It is reclassified as:
```
LIMITED DIRECTIONAL ALIGNMENT CHECK
```

### Required Remediations (P2):
1. **Report Prose Rectification:** Update `artifacts/m2_backtest_report.md` and downstream competition documentation to clarify that the 97.5% figure represents historical consistency and directional concordance, not an out-of-sample forecast.
2. **True Out-of-Sample Split (Future Enhancement):** In a future release cycle, construct an authentic historical split:
   - Fit research velocity using strictly pre-2022 publications and evaluate against 2023–2025 without data re-use.
   - Evaluate MyCOL using strictly Editions 1–6 to predict Edition 7, stripping all retrospective labels.
