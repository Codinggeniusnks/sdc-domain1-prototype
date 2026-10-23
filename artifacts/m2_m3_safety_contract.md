# M2 → M3 Systems Integration & Safety Contract

**Author:** Senior Competition Systems Architect & ML Systems Engineer  
**Date:** 2026-10-23  
**Stage:** Stage 9C High-Value Methodology Review  
**Consumer Module:** M3 Role Matching & User Recommendation Engine  
**Producer Module:** M2 AI Trend Intelligence Engine  
**Interface Specification:** [`src/trend_engine.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/src/trend_engine.py)  

---

## 1. Architectural Purpose & Contract Scope

M2 provides external macroeconomic, technological, and statutory labour-market intelligence. M3 matches individual user skill profiles against target occupations and career pathways. This contract governs the valid consumption of M2 outputs by M3 to prevent algorithmic bias, deceptive recommendations, or mathematical distortions.

---

## 2. Safe vs. Unsafe Consumption Matrix

| M2 Output Field | Data Type | Consumption Status in M3 | Mandatory M3 Behaviour & Guardrails |
| :--- | :---: | :---: | :--- |
| `demand_momentum` | Float (0–100) | **SAFE** | Primary multiplier for career viability ranking. Prioritizes accelerating roles. |
| `augmentation_potential`| Float (0–100) | **SAFE** | Positive career longevity indicator. Highlights roles enhanced by AI tooling. |
| `policy_priority` | Float (0–100) | **SAFE** | Strategic priority weight. Used to boost national priority pathways (e.g. ESG, Semiconductor). |
| `ai_exposure` | Float (0–100) | **CONDITIONAL (RESTRICTED)**| **CRITICAL GUARDRAIL:** M3 MUST NOT use `ai_exposure` as a negative penalty. High exposure must be combined with augmentation to recommend AI-augmented roles (e.g. Software Developers). |
| `automation_exposure` | Float (0–100) | **SAFE (CAUTION)** | Used to generate reskilling warnings if a user targets an automation-vulnerable role (e.g. Clerks). |
| `employment_wage_momentum`| Float (0–100) | **SAFE (GROUP-LEVEL)**| **CRITICAL GUARDRAIL:** Must be displayed as broad sectoral/major-group wage trend, NEVER as a guaranteed 4-digit salary forecast. |
| `research_momentum` | Float / Null | **SAFE (SKILL-ONLY)** | Applicable only to skill matching; null for occupations. Must not be used to rank job vacancies. |
| `confidence_label` | String Enum | **SAFE (MANDATORY)** | Must be used to discount uncertain recommendations. Roles with `LOW` or `INSUFFICIENT` confidence must carry explanatory caveats. |
| `overall_outlook` | String Enum | **SAFE** | High-level badge (`STRONGLY RISING`, `STABLE`, etc.) displayed in career card UI. |
| `is_major_group_fallback`| Boolean | **SAFE (MANDATORY)** | If `True`, M3 must inform the user: *"Group-level baseline; specific 4-digit occupational evidence unavailable."* |

---

## 3. Strict Prohibitions for M3 Engine

1. **NO Single Scalar Synthesis:** M3 must NOT collapse M2's decomposed vector into an uninterpretable single number (e.g. `career_score = 0.5 * skill_match + 0.5 * m2_score`). The match score (user compatibility) and the trend vector (market outlook) must remain separate, inspectable axes.
2. **NO Negative Filtering by AI Exposure:** High AI exposure alone must NEVER filter out or penalize an occupational pathway. If `automation_exposure > augmentation_potential` (e.g. routine clerical), M3 should suggest upskilling into adjacent analytical or administrative management pathways rather than abruptly blocking the user.
3. **NO Null Imputation:** If a dimension is `null` in M2, M3 must NOT replace it with 0 or 50. It must evaluate candidate match scores using available dimensions with proportional re-weighting.

---

## 4. API Interface Invariants

M3 must integrate strictly through the standardized APIs in `src/trend_engine.py`:
- Single Role Query: `get_role_trend(masco_code: str) -> dict`
- Single Skill Query: `get_skill_trend(skill_id: str) -> dict`
- Batch Candidate Evaluation: `get_trend_batch(entity_ids: list[str]) -> dict`
- Audit Explanations: `explain_trend(entity_id: str) -> dict`

Direct access to internal raw JSON files (`trend_signals_v1.json`, raw ILO files) by M3 is strictly prohibited.
