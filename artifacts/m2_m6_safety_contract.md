# M2 → M6 Systems Integration & Scenario Safety Contract

**Author:** Senior Competition Systems Architect & Quantitative Research Reviewer  
**Date:** 2026-10-23  
**Stage:** Stage 9C High-Value Methodology Review  
**Consumer Module:** M6 Macroeconomic & Technological Scenario Engine  
**Producer Module:** M2 AI Trend Intelligence Engine (Baseline Truth)  
**Contract Version:** 1.0.0  

---

## 1. Principle of Separation: Observed Evidence vs. Hypothetical Scenarios

A catastrophic failure mode in workforce simulation engines is blending empirical observations with speculative scenario assumptions, making it impossible to distinguish what is real from what is modeled. 

This contract enforces strict architectural boundary isolation:
```
+-------------------------------------------------------------+
|               M2 BASELINE INTELLIGENCE                      |
| (Historical, Observed, Empirical Malaysian & Global Data)   |
|   - TalentCorp MyCOL (2015-2025)                            |
|   - OpenDOSM Salaries & Wages (2010-2025)                   |
|   - ILO Benchmarks (Task Evaluation)                        |
|   - Enacted Statutory Policies                              |
+-------------------------------------------------------------+
                              |
                              | [IMMUTABLE READ-ONLY ACCESS]
                              v
+-------------------------------------------------------------+
|                M6 SCENARIO SIMULATION ENGINE                |
| (Hypothetical Macroeconomic, Technology & Policy Shocks)    |
|   - Scenario A: "Accelerated Agentic Automation"            |
|   - Scenario B: "Green Industrial Boom (NSS/NETR)"          |
|   - Scenario C: "Regulatory Friction & AI Bottleneck"       |
|                                                             |
|   Output: Baseline + Scenario Shock Delta (\Delta Vector)   |
+-------------------------------------------------------------+
```

---

## 2. Inviolable Safety Guardrails for M6

1. **M2 Baseline Immutability:** M6 must treat all outputs in `skill_trend_profiles_v1.json` and `occupation_trend_profiles_v1.json` as read-only frozen baselines. M6 is strictly prohibited from modifying, overwriting, or monkey-patching M2 store records.
2. **Delta Modeling Architecture:** All scenario calculations must be expressed as explicit perturbation vectors ($\Delta$):
   $$\text{Vector}_{\text{Scenario}}(o, s) = \text{Vector}_{\text{Baseline}}(o) + \Delta_{\text{Scenario}}(o, s)$$
   where $s$ is the scenario identifier (e.g. $s = \text{Agentic\_Acceleration}$).
3. **Decomposed Shock Parameters:** Scenarios must not shock an aggregate score. M6 must apply parameterized shifts to specific underlying dimensions:
   - Shock to Automation: $\Delta \text{Auto}$ (e.g. $+15.0$ index points for routine cognitive roles).
   - Shock to Augmentation: $\Delta \text{Aug}$ (e.g. $+20.0$ index points for professional engineers).
   - Shock to Policy Priority: $\Delta \text{Policy}$ (e.g. $+25.0$ index points for ESG roles under strict carbon tax enforcement).
   - Shock to Demand Momentum: $\Delta \text{Demand}$ (e.g. $-10.0$ index points under global macroeconomic recession).
4. **Transparent Labeling in Visualizations:** Any UI or report presenting scenario projections must explicitly render two distinct markers:
   - `[CURRENT OBSERVED BASELINE]` (Originating from M2)
   - `[PROJECTED SCENARIO IMPACT: <NAME>]` (Originating from M6)

---

## 3. Allowed Scenario Shock Parameters

| Scenario Parameter | Target M2 Dimension | Valid Shock Range | Real-World Narrative Example |
| :--- | :--- | :---: | :--- |
| `automation_shock` | `automation_exposure` | $[-20.0, +35.0]$ | Rapid deployment of multimodal autonomous coding agents. |
| `augmentation_shock` | `augmentation_potential` | $[-15.0, +30.0]$ | Enterprise adoption of RAG internal knowledge bases. |
| `policy_acceleration`| `policy_priority` | $[0.0, +30.0]$ | Enactment of mandatory EU-style AI liability directives. |
| `wage_pressure_shock`| `employment_wage_momentum`| $[-25.0, +25.0]$ | Shift in Singapore exchange rate driving intense talent drain. |
| `talent_scarcity_shock`| `demand_shortage_level` | $[-20.0, +25.0]$ | Graduation of 60,000 national semiconductor engineers. |

M6 is fully unblocked to consume M2 once the P1 remediations specified in Stage 9C are completed.
