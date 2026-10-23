# M6 Scenario Assumptions & Parameter Inventory (v1.0.0)

**Author:** Senior Workforce Foresight Engineer & Scenario-Modelling Researcher  
**Date:** 2026-10-23  
**Status:** **AUTHORITATIVE SCENARIO SPECIFICATION**  
**Data Reference:** [scenario_definitions_v1.json](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/scenarios/scenario_definitions_v1.json)  

---

## 1. Governance Declaration: Assumptions vs. Observations

```
================================================================================
                    CRITICAL FORESIGHT GOVERNANCE PRINCIPLE
  Scenario parameters are EXPLICIT MODELLING ASSUMPTIONS, NOT EMPIRICAL FACTS.
  They represent plausible future operating conditions designed to stress-test
  career pathways under technological uncertainty.
  Assumption Status: SCENARIO_ASSUMPTION (Never OBSERVED_EVIDENCE).
================================================================================
```

---

## 2. Complete Inventory of the 8 Core Foresight Parameters

| Parameter Name | Public Qualitative Band | Central Index | Range [Lower, Upper] | Affected Dimensions | Empirical Source Basis |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **`AI_ADOPTION_INTENSITY`** | `LOW` to `VERY HIGH` | 20.0 – 85.0 | [15.0, 95.0] | `effective_ai_pressure`, `automation_pressure`, `augmentation_opportunity` | DOSM ICT Survey, Gartner Enterprise AI Deployments |
| **`AGENTIC_TASK_REACH`** | `LOW` to `VERY HIGH` | 10.0 – 80.0 | [5.0, 90.0] | `automation_pressure`, `task_transformation` | ILO WP140 Task Boundaries, OpenAI/Anthropic Benchmarks |
| **`AUTOMATION_INTENSITY`** | `LOW` to `VERY HIGH` | 20.0 – 85.0 | [15.0, 95.0] | `automation_pressure`, `transition_pressure` | ILO WP140 Cognitive Task Exposure Ratios |
| **`AUGMENTATION_INTENSITY`** | `MODERATE` to `VERY HIGH` | 30.0 – 85.0 | [25.0, 95.0] | `augmentation_opportunity`, `task_transformation` | MIT/Stanford Productivity Empirical Studies |
| **`TECHNOLOGY_DIFFUSION_BREADTH`** | `LOW` to `HIGH` | 25.0 – 80.0 | [20.0, 90.0] | `skill_change_needed`, `effective_ai_pressure` | MDEC Digital Economy Diffusion Data |
| **`RESKILLING_RESPONSE_STRENGTH`** | `MODERATE` to `HIGH` | 30.0 – 60.0 | [20.0, 70.0] | `reskilling_urgency`, `augmentation_opportunity` | HRD Corp Training Levy Utilization Rates |
| **`POLICY_RESPONSE_STRENGTH`** | `MODERATE` to `HIGH` | 40.0 – 65.0 | [30.0, 75.0] | `policy_buffer`, `demand_resilience` | NIMP 2030, National AI Action Plan, MyDIGITAL |
| **`ORGANISATIONAL_ADAPTATION_SPEED`** | `LOW` to `HIGH` | 25.0 – 75.0 | [20.0, 85.0] | `augmentation_opportunity`, `role_transition_pressure` | McKinsey Global Institute Workflow Adaptation Studies |

---

## 3. Scenario-Specific Assumption Breakdowns

### A. Scenario 1: `REFERENCE_2026` (Current Evidence Baseline)
*Narrative*: Current labour-market conditions persist according to empirical 2024–2026 data. AI tools exist in early deployment; no accelerated technological shock is assumed. Multipliers evaluate to 1.0.

1. **`PARAM-REF-ADOPT`** (`AI_ADOPTION_INTENSITY`):
   - Band: `LOW` | Central: **20.0** | Range: `[15.0, 25.0]`
   - *Rationale*: Baseline generative AI deployment across Malaysian enterprises as measured in DOSM 2024 ICT surveys.
2. **`PARAM-REF-REACH`** (`AGENTIC_TASK_REACH`):
   - Band: `LOW` | Central: **10.0** | Range: `[5.0, 15.0]`
   - *Rationale*: Autonomous multi-step agent tools remain largely in experimental/pilot developer phases.
3. **`PARAM-REF-AUTO`** (`AUTOMATION_INTENSITY`):
   - Band: `LOW` | Central: **20.0** | Range: `[15.0, 25.0]`
   - *Rationale*: Routine cognitive task automation bounded by standard software scripting.
4. **`PARAM-REF-AUG`** (`AUGMENTATION_INTENSITY`):
   - Band: `MODERATE` | Central: **30.0** | Range: `[25.0, 35.0]`
   - *Rationale*: Early productivity improvements from conversational search and writing assistants.
5. **`PARAM-REF-DIFF`** (`TECHNOLOGY_DIFFUSION_BREADTH`):
   - Band: `LOW` | Central: **25.0** | Range: `[20.0, 30.0]`
   - *Rationale*: Concentrated primarily in multinational tech hubs and financial institutions in the Klang Valley.
6. **`PARAM-REF-RESKILL`** (`RESKILLING_RESPONSE_STRENGTH`):
   - Band: `MODERATE` | Central: **30.0** | Range: `[20.0, 40.0]`
   - *Rationale*: Standard historical rates of corporate training participation.
7. **`PARAM-REF-POLICY`** (`POLICY_RESPONSE_STRENGTH`):
   - Band: `MODERATE` | Central: **40.0** | Range: `[30.0, 50.0]`
   - *Rationale*: Baseline execution of National AI Roadmap 2021-2025.
8. **`PARAM-REF-ADAPT`** (`ORGANISATIONAL_ADAPTATION_SPEED`):
   - Band: `LOW` | Central: **25.0** | Range: `[20.0, 30.0]`
   - *Rationale*: Standard annual corporate procurement and job architecture revision cycles.

---

### B. Scenario 2: `MODERATE_COPILOT` (Assistive AI Expansion)
*Narrative*: Enterprises widely deploy copilot tools. Routine administrative subtasks are automated, but complex decision-making, stakeholder interaction, and verification remain human-led.

1. **`PARAM-COP-ADOPT`** (`AI_ADOPTION_INTENSITY`):
   - Band: `MODERATE` | Central: **55.0** | Range: `[45.0, 65.0]`
   - *Rationale*: Mainstream adoption of integrated copilot suites across professional services and corporate operations.
2. **`PARAM-COP-REACH`** (`AGENTIC_TASK_REACH`):
   - Band: `MODERATE` | Central: **35.0** | Range: `[25.0, 45.0]`
   - *Rationale*: Agents execute bounded multi-step tasks with mandatory human approval checkpoints.
3. **`PARAM-COP-AUTO`** (`AUTOMATION_INTENSITY`):
   - Band: `MODERATE` | Central: **45.0** | Range: `[35.0, 55.0]`
   - *Rationale*: Substantial automation of basic drafting, data summarisation, transcription, and boilerplate coding.
4. **`PARAM-COP-AUG`** (`AUGMENTATION_INTENSITY`):
   - Band: `HIGH` | Central: **70.0** | Range: `[60.0, 80.0]`
   - *Rationale*: Substantial amplification of knowledge-worker throughput, analysis speed, and synthesis capability.
5. **`PARAM-COP-DIFF`** (`TECHNOLOGY_DIFFUSION_BREADTH`):
   - Band: `MODERATE` | Central: **50.0** | Range: `[40.0, 60.0]`
   - *Rationale*: Broad adoption across Tier-1 and Tier-2 Malaysian enterprises; emerging uptake in government agencies.
6. **`PARAM-COP-RESKILL`** (`RESKILLING_RESPONSE_STRENGTH`):
   - Band: `HIGH` | Central: **60.0** | Range: `[50.0, 70.0]`
   - *Rationale*: Active upskilling grants, HRD Corp digital levy incentives, and updated university curricula.
7. **`PARAM-COP-POLICY`** (`POLICY_RESPONSE_STRENGTH`):
   - Band: `HIGH` | Central: **65.0** | Range: `[55.0, 75.0]`
   - *Rationale*: Proactive subsidies under NIMP 2030 Mission 1 and national AI sandbox initiatives.
8. **`PARAM-COP-ADAPT`** (`ORGANISATIONAL_ADAPTATION_SPEED`):
   - Band: `MODERATE` | Central: **55.0** | Range: `[45.0, 65.0]`
   - *Rationale*: Systematic restructuring of standard operating procedures around human-in-the-loop workflows.

---

### C. Scenario 3: `FAST_AGENTIC` (Accelerated Agentic AI Workflows)
*Narrative*: Breakthroughs in autonomous agents enable end-to-end multi-step tool execution. Routine clerical, administrative, and junior coding pipelines face sharp substitution pressure; human value pivots heavily toward governance, strategic coordination, and verification.

1. **`PARAM-AGE-ADOPT`** (`AI_ADOPTION_INTENSITY`):
   - Band: `VERY HIGH` | Central: **85.0** | Range: `[75.0, 95.0]`
   - *Rationale*: Universal deployment of autonomous agent fleets across digital workflows.
2. **`PARAM-AGE-REACH`** (`AGENTIC_TASK_REACH`):
   - Band: `VERY HIGH` | Central: **80.0** | Range: `[70.0, 90.0]`
   - *Rationale*: Autonomous multi-step tool use, code generation/testing, automated reconciliation, and API orchestration.
3. **`PARAM-AGE-AUTO`** (`AUTOMATION_INTENSITY`):
   - Band: `VERY HIGH` | Central: **85.0** | Range: `[75.0, 95.0]`
   - *Rationale*: Routine, codifiable information processing faces near-total automated substitution.
4. **`PARAM-AGE-AUG`** (`AUGMENTATION_INTENSITY`):
   - Band: `VERY HIGH` | Central: **85.0** | Range: `[75.0, 95.0]`
   - *Rationale*: High-level engineers and domain experts orchestrate fleets of agents, achieving 5x-10x throughput gains.
5. **`PARAM-AGE-DIFF`** (`TECHNOLOGY_DIFFUSION_BREADTH`):
   - Band: `HIGH` | Central: **80.0** | Range: `[70.0, 90.0]`
   - *Rationale*: Rapid cloud commodification democratises agentic tool access across all business sizes.
6. **`PARAM-AGE-RESKILL`** (`RESKILLING_RESPONSE_STRENGTH`):
   - Band: `MODERATE` | Central: **45.0** | Range: `[35.0, 55.0]`
   - *Rationale*: Technological capability outpaces institutional education cycles, resulting in transition friction.
7. **`PARAM-AGE-POLICY`** (`POLICY_RESPONSE_STRENGTH`):
   - Band: `HIGH` | Central: **60.0** | Range: `[50.0, 70.0]`
   - *Rationale*: Substantial government focus on AI safety guidelines and transition cushions, but reactive to technology.
8. **`PARAM-AGE-ADAPT`** (`ORGANISATIONAL_ADAPTATION_SPEED`):
   - Band: `HIGH` | Central: **75.0** | Range: `[65.0, 85.0]`
   - *Rationale*: Aggressive restructuring of corporate headcount and rapid decommissioning of manual data handovers.
