# O2 Scenario Change Contract — v1.0.0

## 1. Executive Summary & Semantic Clarification
A frequent point of confusion in workforce analytics is conflating **scenario selection** with **empirical market movement**. When an employer or learner toggles from `REFERENCE_2026` to `FAST_AGENTIC`:
- The labor market did **not** change.
- The external world did **not** accelerate overnight.
- **Only the user's macroeconomic foresight assumptions changed.**

## 2. Scenario Transition Semantics
O2 explicitly documents the transition semantics across M6 scenarios:
- `REFERENCE_2026`: Standard gradual baseline adoption of assistive enterprise AI.
- `MODERATE_COPILOT`: Accelerated copilot deployment across cognitive professional roles.
- `FAST_AGENTIC`: Autonomous agentic workflows with high displacement and extreme technical reskilling demands.

## 3. Downstream Attribution Invariant
Whenever an O2 replan is triggered by `M6_SCENARIO_CHANGED`:
1. `root_causes` must contain `SCENARIO_CHANGE`.
2. `quality_flags` must include `SCENARIO_ASSUMPTION_CHANGE`.
3. The explanation narrative must explicitly state:
   > `"Scenario changed from '{prev}' to '{new}'. Recommendations reflect alternative foresight assumptions, not an observed empirical labor-market shift."`
