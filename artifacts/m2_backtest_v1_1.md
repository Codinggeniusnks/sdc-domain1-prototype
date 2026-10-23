# M2 Limited Directional Alignment Evaluation (v1.1.0)

## Executive Summary & Methodological Reclassification

In Stage 9C, Defect **P2-1** identified that previous evaluations referred to historical signal consistency as "backtest accuracy" or "predictive performance". In labour market economics and empirical quantitative research, evaluating static policy lists or persistent multi-year economic surveys against subsequent periods measures **structural persistence**, not predictive foresight.

Accordingly, this evaluation is formally reclassified:
- **Authoritative Classification**: **Limited Directional Alignment Check**
- **Explicitly Prohibited Terminology**: "Predictive accuracy", "Forecast accuracy", "Backtest validation", "Model accuracy".

The purpose of this check is strictly to verify that the M2 scoring pipeline correctly preserves directional signal flow without distorting known historical labour market dynamics.

---

## Evaluation Design & Strict Temporal Separation

All tests enforce strict temporal barriers between feature computation and evaluation targets:
- **Training / Feature Extraction Window**: Information published on or before December 31, 2023 ($t \le 2023$).
- **Evaluation Window**: Observed outcomes in 2024–2026 ($t > 2023$).
- **Leakage Prevention**: No post-2023 observations were accessible to feature transformers during evaluation.

---

## Empirical Alignment Results vs. Naive Baselines

| Evidence Stream | Sample Size ($N$) | Evaluation Target Metric | Engine Directional Alignment | Naive Heuristic Baseline | Incremental Engine Gain |
| :--- | :---: | :--- | :---: | :---: | :---: |
| **TalentCorp MyCOL** | 20 | Directional Shortage Consistency (Ed. 8 2024/25) | **85.0%** (17 / 20) | **80.0%** (16 / 20) | **+5.0%** |
| **OpenDOSM Wages** | 4 | Wage Growth Sign Continuity (2022–2024) | **100.0%** (4 / 4) | **100.0%** (4 / 4) | **0.0%** |
| **OpenAlex Research** | 16 | Research Velocity Acceleration (2024–2026) | **100.0%** (16 / 16) | **100.0%** (16 / 16) | **0.0%** |
| **Overall Corpus** | **40** | **Directional Consistency Check** | **92.5%** (37 / 40) | **90.0%** (36 / 40) | **+2.5%** |

### Detailed Breakdown by Source Family

#### 1. TalentCorp MyCOL Directional Alignment
- **Methodology**: Editions 1–7 (2015–2023) historical presence used to project Edition 8 (2024/2025) status.
- **Naive Baseline (Persistence)**: Predicts that any occupation listed as Critical in Edition 7 remains Critical in Edition 8.
- **Performance**:
  - Engine achieved **17 / 20 (85.0%)** directional alignment.
  - Correctly identified 11 persistent critical roles (e.g., Software Developers 2512, Systems Analysts 2511, Accountants 2411).
  - Correctly identified 3 non-critical clerical roles (General Office Clerks 4110, Accounting Clerks 4311, Administrative Secretaries 3343).
  - Incremental gain (+5.0%): Engine correctly identified Environmental Engineers & Sustainability Analysts (2143) as critical due to policy/ESG pressure, whereas the naive persistence baseline missed it.
  - False negatives (3): Training Professionals (2424), Graphic Designers (2166), and Web Technicians (3514) were newly added to Edition 8 without prior multi-year persistent shortage scores.

#### 2. OpenDOSM Formal Sector Wage Growth Continuity
- **Methodology**: Pre-2022 compound annual growth rate (CAGR) by Major Group used to evaluate post-2022 positive wage expansion.
- **Naive Baseline (Always Positive)**: Predicts positive wage growth across all Major Groups.
- **Performance**:
  - Engine: **100.0%** (4 / 4 Major Groups exhibited positive wage growth).
  - Baseline: **100.0%** (4 / 4).
  - **Incremental Gain: 0.0%**. In an inflationary emerging market, median formal nominal wages virtually always grow; the engine merely reflects macroeconomic trend continuity.

#### 3. OpenAlex Scientific Momentum Continuation
- **Methodology**: 2020–2023 baseline research velocity used to evaluate 2024–2026 literature growth.
- **Naive Baseline (Continuation)**: Predicts continued publication expansion for established technological concepts.
- **Performance**:
  - Engine: **100.0%** (16 / 16 concepts).
  - Baseline: **100.0%** (16 / 16).
  - **Incremental Gain: 0.0%**. AI and computational research has expanded across the board globally since 2022; the engine mirrors global scientometric trends.

---

## Scientific and Methodological Conclusion

1. **Verification of Signal Preservation**: The test confirms that M2 v1.1.0 mathematical transformations do not corrupt, invert, or attenuate real-world labour market trends.
2. **Honest Attribution**: The high alignment score (92.5%) is overwhelmingly driven by **underlying institutional and economic persistence**, not algorithmic intelligence. The engine provides an incremental gain of only +2.5% over simple persistence heuristics.
3. **Guardrails Against Over-Claiming**: M2 v1.1.0 documentation and downstream consumers must treat these results as confirmation of *internal data fidelity*, and must NEVER advertise them as "92.5% predictive accuracy".
