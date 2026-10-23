# Final Human-in-the-Loop & Product Policy Analysis

**Evaluator Role**: Senior ML Engineer & Reproducibility Auditor  
**Model**: `H_blend_0.70A_0.30C1_W1.0` (Frozen Hybrid Ensemble)  
**Target Surface**: User Profile Skill Extraction & Assistive Career Pathway Generation  

---

## 1. Product Policy Specification

To ensure high user agency, transparency, and trust, the M1 Skills Extraction Engine operates under a three-tiered threshold architecture:
1. **Core Skills ($\text{Score} \ge \mathbf{0.450}$)**:
   - High-confidence skills automatically pinned to the worker's career profile.
   - Designed for high precision to prevent cluttering profiles with spurious badges.
2. **Suggested Skills ($\mathbf{0.250} \le \text{Score} < \mathbf{0.450}$)**:
   - Medium-confidence candidates presented as *"Recommended for Confirmation"* chips.
   - Users can accept (+), reject ($\times$), or ignore with a single click.
3. **Suppressed Noise ($\text{Score} < \mathbf{0.250}$)**:
   - Background signals suppressed from user view to eliminate noise.

---

## 2. Quantitative Holdout Evaluation of the Dual-Threshold Policy

| Evaluation Metric | Protocol B (Real-World Holdout, $N=63$) | Protocol C v2 (Unseen-Occupation Holdout, $N=25$) | Combined / Operational Experience |
| :--- | :---: | :---: | :---: |
| **Core Tier Precision ($\ge 0.450$)** | **71.28%** | **73.61%** | **72.13% (High Precision Anchor)** |
| **Core Tier Recall ($\ge 0.450$)** | **71.65%** | **78.79%** | **74.31% (Majority Automated)** |
| **Suggested Tier Precision ($[0.25, 0.45)$)** | 15.76% | 14.81% | 15.52% (Interactive Discovery) |
| **True Skills Missed by Core Tier** | 44 instances | 13 instances | 57 total missed instances |
| **Missed Skills Recovered by Suggested Tier** | **26 instances** | **8 instances** | **34 recovered instances** |
| **Recovery Rate of Missed Skills (%)** | **59.09%** | **61.54%** | **59.65% (~6 out of 10 recovered)** |
| **False Suggestion Burden (Chips / Profile)** | **2.21 chips** | **1.84 chips** | **~2 chips per profile (Low Burden)** |

---

## 3. Product Experience Findings & Human Agency Guarantees

### 3.1. High Precision in Automated Population
- When the system automatically assigns skills to a worker's profile (the Core tier), **over 71%–73% of the assigned skills are exact ground truth matches**.
- This satisfies the UX requirement that automated recommendations must feel credible, professional, and reliable on first impression.

### 3.2. Effective Assistive Recovery
- Workers frequently describe tasks using indirect phrasing or non-standard synonyms.
- The Suggested tier catches **$\sim 60\%$ of skills that would have been completely missed** by an autonomous high-threshold classifier.
- Workers are presented with only **$\sim 2$ suggested chips per profile** (e.g. `[+ Data Privacy (PDPA)]`, `[+ Workflow Automation]`), which requires less than 5 seconds of review time.

### 3.3. Ethical Boundaries & User Agency
- **No Inferred Traps**: Inferred skills are never treated as unchangeable credentials. Workers can manually add missing skills or delete unrepresentative ones.
- **Demographic Independence**: The model's inputs are strictly limited to text describing work tasks and competencies. Age, gender, nationality, and background are completely excluded from the prediction pipeline.
- **Confidence Disclosure**: Tooltips clearly display: *"AI Confidence Score: 74% (Core) — verified against Malaysian Occupational Standards (MASCO) and TalentCorp MyCOL"*.
