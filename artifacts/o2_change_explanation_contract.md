# O2 Change Explanation Contract — v1.0.0

## 1. Executive Summary & Prohibition of Generative Hallucination
In high-stakes career pathways and enterprise reskilling, automated explanations must be **traceable, reproducible, and verifiable**. O2 strictly prohibits using generative Large Language Models (LLMs) to synthesize speculative narratives explaining why a recommendation changed.

Instead, O2 implements a **Deterministic Template Explanation Engine** that binds verified diff metrics directly to standardized reason codes.

## 2. Root-Cause Attribution Taxonomy

| Root Cause Code | Trigger Condition | Narrative Template |
|---|---|---|
| `TREND_CHANGE` | M2 snapshot hash / id changed | "Macro labor market evidence updated from M2 trend snapshot '{snapshot_id}'. Occupational shortage and momentum indicators adjusted." |
| `SCENARIO_CHANGE` | M6 scenario changed (e.g. Reference → Fast) | "Macroeconomic AI adoption scenario selection changed from '{prev_scenario}' to '{new_scenario}'. Disruption and augmentation assumptions updated." |
| `PROFILE_CHANGE` | Learner confirmed skill set changed | "Learner profile skill verification state updated. Confirmed competencies and remaining gap boundaries recalculated." |
| `COHORT_CHANGE` | Employer cohort roster changed | "Employer workforce cohort composition updated. Organizational skill gap prevalences refreshed under k=5 privacy safeguards." |
| `MANUAL_RECOMPUTE` | User/system triggered re-check | "User or system requested an explicit state re-verification." |
| `MULTIPLE_INPUT_CHANGES` | Two or more inputs changed simultaneously | "Multiple independent input vectors changed simultaneously: {causes_list}." |

## 3. Disaggregated Multi-Cause Attribution
If both an M2 trend snapshot and an M6 scenario change simultaneously:
- O2 **never** collapses the attribution to a single speculative cause.
- O2 emits `root_causes = ["MULTIPLE_INPUT_CHANGES", "TREND_CHANGE", "SCENARIO_CHANGE"]`.
- The explanation explicitly details the separate contributions of trend evidence and scenario assumptions, ensuring complete audit transparency.

## 4. Evidence Confidence Index (ECI) Shift Explanation
When M2 or M6 updates evidence reliability without changing occupational fit:
- O2 emits an explicit disclaimer:
  > `"EVIDENCE_CONFIDENCE_CHANGE: ECI movement reflects updated empirical source data reliability (survey sample size, freshness, or policy validation), NOT an alteration in occupational desirability or career fit."`
This protects learners from misinterpreting a decrease in research sample size as an occupational demotion.
