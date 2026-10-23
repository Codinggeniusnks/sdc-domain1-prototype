# Stage 8D Artifact: Final Model Promotion Gate & Next Competition Stage Roadmap

**Authority**: Senior ML Research Architect & Competition Systems Architect  
**Scope**: Post-Evaluation Promotion Criteria (Stage 9) & Transition to M2 Trend Intelligence Engine  

---

## 1. Pre-Registered Promotion Gate Criteria (Task 15)

Following the one-shot evaluation of the frozen Primary Hybrid Model (`H_blend_0.70A_0.30C1_W1.0`, $\theta_{\text{eval}} = 0.375$) on **Protocol B** (`real_world_test_set.json`) and **Protocol C v2** (`unseen_occupation_test_set_v2.json`), the model will be classified into one of three dispositions.

> [!IMPORTANT]
> The invalidated historical v4/M6 score ($\sim 0.93$) was an artifact of synthetic template memorization and holdout leakage and is permanently excluded as a reference target.

### Disposition 1 — `PROMOTE` (Full Production Promotion for Competition Prototype)
All of the following criteria are satisfied:
1. **Protocol B (Real-World Holdout) Performance**:
   - Skills Macro F1 $\ge \mathbf{0.6800}$ (matching or exceeding the clean M5 baseline regime of $0.6928$ within sampling variance) **AND** Skills Micro F1 $\ge \mathbf{0.6500}$.
2. **Protocol C v2 (Unseen-Occupation Holdout) Generalization**:
   - Unseen-Occupation Skills Macro F1 $\ge \mathbf{0.5800}$ with zero catastrophic fold/cluster collapse (no major occupational cluster scoring $0.00$ across all assigned skills).
3. **Rare-Class & Human-in-the-Loop Safety**:
   - Rare-Class Recall $\ge \mathbf{0.5500}$ on Protocol B, **AND** combined Core + Suggested recall ($\theta \ge 0.250$) captures $\ge \mathbf{70\%}$ of true holdout skills with a false-suggestion burden $\le \mathbf{3.0}$ skills per profile.
4. **Operational SLA**:
   - Single-document CPU p95 inference latency $\le \mathbf{50\text{ ms}}$ and memory footprint $\le \mathbf{500\text{ MB}}$.

### Disposition 2 — `PROMOTE WITH LIMITATIONS` (Approved for Competition Integration with Explicit Scope Guards)
The model does not meet every strict `PROMOTE` threshold above, **but** satisfies all of the following minimum viability bounds:
1. **Protocol B Viability**: Skills Macro F1 $\in [\mathbf{0.6000}, 0.6800)$ and Micro F1 $\ge \mathbf{0.5800}$.
2. **Protocol C v2 Viability**: Unseen-Occupation Skills Macro F1 $\ge \mathbf{0.5000}$.
3. **Human-in-the-Loop Mitigation**: Even if single-threshold recall on 1–2 implicit classes (e.g., `instructional_design` or `data_visualization`) is low at $\theta_{\text{eval}} = 0.375$, the Suggested tier ($0.250 \le S < 0.450$) plus UI manual skill confirmation ensures safe end-to-end user journeys without blocking career pathway generation.
4. **Required Action**: Promote the frozen model into the application with documented class-level caveats in the UI and Technical Declaration, and **do not** enter another M1 retraining loop.

### Disposition 3 — `DO NOT PROMOTE` (Critical Failure / Fallback Trigger)
Triggered only if one or more of the following severe failures occur:
1. Protocol B Skills Macro F1 $< \mathbf{0.6000}$ or Protocol C v2 Skills Macro F1 $< \mathbf{0.4800}$.
2. Severe runtime failure, corrupted serialization, or p95 CPU latency $> \mathbf{250\text{ ms}}$.
3. **Contingency Action**: Revert the application's M1 extractor to the preserved clean M5 baseline (`runpod/models/skills_predictor_v3.joblib`) or the frozen Compact Fallback (`A_base_C2.5_W1.0`), document the negative experimental finding transparently, and immediately advance to M2.

---

## 2. Strategic Transition to Next Competition Stage (Task 16)

### 2.1. Termination of M1 Optimisation Loops
Regardless of whether the Stage 9 one-shot evaluation results in `PROMOTE` or `PROMOTE WITH LIMITATIONS`, **Stage 9 concludes all M1 skills-extraction dataset and model optimization**. Further iterative tuning of the 16-skill classifier yields diminishing returns relative to the holistic judging rubric of **SDC Hackathon 2026 — Domain 1 (The Aiversecity Future-Ready Workforce Domain)**, which weights:
- **Problem-Solution Fit (25%)**: Whole-chain coverage from tracking AI advancement $\rightarrow$ predicting emerging/declining skills and jobs $\rightarrow$ matching people to future roles $\rightarrow$ personalised reskilling pathways $\rightarrow$ UN SDG 4 & 8 connection, while keeping humans in charge.
- **Originality & Innovation (25%)**: How trend signals become skill forecasts, how AI disruption scenarios are modelled, and how SDG links inform user choices.

### 2.2. Next Major Engineering Stage: `M2 TREND INTELLIGENCE ENGINE`
Immediately following the one-shot holdout evaluation of M1, engineering effort transitions to **M2: Dynamic Trend Intelligence & Scenario Forecasting Engine**, comprising:
1. **Updatable Multi-Source Evidence Registry**:
   - Structured ingestion of dated public labor-market signals (TalentCorp MyCOL 2024/2025, DOSM Labour Force & MASCO updates, MDEC/MOSTI AI adoption indicators, WEF Future of Jobs & global AI benchmark milestones) with explicit `source`, `publisher`, `publication_date`, `retrieval_date`, and `url` provenance.
2. **Explainable Skill & Role Trend Scoring**:
   - Replacing the legacy static binary demand flag with decomposed, inspectable **Skill Trend Scores** (Momentum, Policy/Regulatory Push, Employer Demand Signal, Complementarity vs Automation Exposure) and **Role Trajectory Classifications** (*Emerging*, *Transforming*, *Resilient*, *At-Risk / Declining*).
3. **Interactive AI Disruption Scenario Modelling**:
   - Allowing workers and HR planners to toggle between concrete macroeconomic/technological scenarios (e.g., *Baseline Adoption*, *Accelerated GenAI & Agentic Automation*, *Green & ESG Regulatory Mandate*) and observe transparent, real-time recalculations of role match scores, skill urgency, and SDG 4/8 alignment.
4. **Uncertainty & Confidence Disclosures**:
   - Explicitly surfacing evidence density and confidence intervals per forecast so users retain informed human agency over career and reskilling decisions.
