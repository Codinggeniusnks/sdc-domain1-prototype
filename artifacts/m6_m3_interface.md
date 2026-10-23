# M6 to M3 Interface Specification: Future-Proof Role Matching Contract (v1.0.0)

**Author:** Senior ML Systems Architect & Explainable-AI Engineer  
**Date:** 2026-10-23  
**Status:** **AUTHORITATIVE DOWNSTREAM INTERFACE SPECIFICATION**  
**Module Reference:** [scenario_engine.py](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/src/scenario_engine.py)  

---

## 1. Architectural Scope & Decoupling Boundaries

This document defines the formal software and data contract between **M6 (Future Workforce Scenario Engine)** and future **M3 (Personalised Role Matching Engine)**.

### Strict Governance Boundary:
- **M6 Responsibilities**: Model macroeconomic, technological, and policy conditions across plausible futures; provide scenario-adjusted occupational profiles, transition pressures, and scenario deltas.
- **M3 Responsibilities**: Compare candidate skill vectors (from frozen M1) against target occupational requirements; rank role recommendations; apply scenario resilience multipliers.
- **Strict Prohibition**: Stage 10A **does NOT implement M3 ranking** or personalised candidate scoring. Only the scenario query and delta interfaces are exposed.

---

## 2. Python API Contract (`ScenarioEngine`)

Future M3 development will interact exclusively with the instantiated `ScenarioEngine` class:

```python
from src.scenario_engine import ScenarioEngine

engine = ScenarioEngine()
```

### Method 1: `get_role_scenario(masco_code: str, scenario_id: str) -> dict`
Retrieves the complete scenario foresight profile for a specific 4-digit MASCO or Major Group.

**Input Arguments**:
- `masco_code`: 4-digit MASCO code (e.g., `"2512"`) or Major Group identifier (e.g., `"MAJOR_2"`).
- `scenario_id`: One of `"REFERENCE_2026"`, `"MODERATE_COPILOT"`, `"FAST_AGENTIC"`.

**Return Schema**:
```json
{
  "masco_code": "2512",
  "occupation_title": "Software Developers",
  "major_group": "2",
  "scenario_id": "FAST_AGENTIC",
  "baseline_outlook": "STRONGLY RISING",
  "effective_ai_pressure": 80.6,
  "automation_pressure": 15.9,
  "augmentation_opportunity": 84.0,
  "demand_resilience": 78.2,
  "policy_buffer": 54.0,
  "transition_pressure": 29.3,
  "reskilling_urgency": "HIGH",
  "scenario_outlook": "TRANSFORMING",
  "scenario_confidence": "HIGH",
  "sensitivity_classification": "HIGHLY SENSITIVE",
  "uncertainty_band": {
    "metric": "transition_pressure",
    "lower": 24.8,
    "central": 29.3,
    "upper": 33.7
  },
  "scenario_delta_from_reference": {
    "transition_pressure_delta": 9.1,
    "automation_pressure_delta": 7.9,
    "augmentation_opportunity_delta": 30.0,
    "demand_resilience_delta": 2.7
  },
  "quality_flags": [
    "MAJOR_GROUP_WAGE_CONTEXT",
    "NO_ROLE_SPECIFIC_WAGE_DATA"
  ]
}
```

---

### Method 2: `get_scenario_delta(masco_code: str, scenario_id: str, baseline_scenario: str = "REFERENCE_2026") -> dict`
Extracts the net shock experienced by an occupation between baseline reference and future scenario.

**Return Schema**:
```json
{
  "masco_code": "4110",
  "target_scenario": "FAST_AGENTIC",
  "baseline_scenario": "REFERENCE_2026",
  "outlook_shift": "HIGHLY PRESSURED -> HIGHLY PRESSURED",
  "reskilling_urgency_shift": "MODERATE -> HIGH",
  "transition_pressure_delta": 17.4,
  "automation_pressure_delta": 29.7,
  "augmentation_opportunity_delta": 4.4,
  "demand_resilience_delta": 1.5
}
```

---

### Method 3: `compare_role_scenarios(masco_code: str) -> dict`
Returns a unified multi-scenario comparison object for UI presentation and cross-scenario stability analysis.

---

### Method 4: `explain_role_scenario(masco_code: str, scenario_id: str) -> dict`
Generates structured natural-language explanations answering WHAT, WHY, EVIDENCE, ASSUMPTIONS, and UNCERTAINTY.

---

## 3. How Future M3 Will Consume M6 Outputs

When M3 is constructed in subsequent stages, it will evaluate candidate match scores using a **Dual-Horizon Objective Function**:

$$\text{FinalMatchScore}(C, O, s) = w_{\text{skill}} \cdot \text{SkillFit}(C, O) + w_{\text{resilience}} \cdot S_{\text{resilience}}(O, s) - w_{\text{friction}} \cdot T_{\text{role}}(O, s)$$

Where:
- $\text{SkillFit}(C, O)$: Semantic and categorical overlap between candidate skills $C$ and role requirements $O$.
- $S_{\text{resilience}}(O, s)$: M6 Scenario Demand Resilience under selected scenario $s$.
- $T_{\text{role}}(O, s)$: M6 Role Transition Pressure under scenario $s$.

### Candidate-Facing Explanations Enabled by M6 Contract:
> *"Software Developer (MASCO 2512) is an 88% skill match for you today. Under the **Fast Agentic AI** scenario, this role remains **Transforming** with strong employer demand, but will require high reskilling in AI governance and prompt orchestration."*

---

## 4. Anti-Patterns Barred by This Contract

1. **NO Demographic Inputs**: Passing `age`, `gender`, `ethnicity`, or socioeconomic background to `ScenarioEngine` raises an immediate `ValueError`.
2. **NO Role-Specific Wage Projections**: M3 must not multiply M6 indices by salary numbers to produce speculative future income claims.
3. **NO Single-Score Opaque Collapse**: M3 must preserve the distinction between skill fit and scenario resilience.
