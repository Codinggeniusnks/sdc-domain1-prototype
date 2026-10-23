# M4 Learning Time Estimation & Pacing Freeze Audit v1.1.0

**Reference Milestone**: Stage 12D Freeze Audit (Checks 21–29)  
**Target Module**: M4 Personalised Reskilling Pathway Engine v1.1.0  
**Status**: AUDITED, VERIFIED & FROZEN

---

## 1. Audit Scope & Pedagogical Foundations

This audit evaluates the mathematical soundness, configuration management, and pacing disclaimers of the learning effort estimation engine in M4 v1.1.0.

---

## 2. Multiplier Floor Configuration & Pedagogical Rationale

### Checks 21 & 22: Configuration Decoupling & Rationale
In M4 v1.1.0, the minimum effort multiplier floor is loaded from `data/reskilling/m4_scoring_config_v1_1.json`:
- **Config Key**: `learning_time_estimation.deficit_effort_scaling.min_multiplier_floor`
- **Value**: **`0.50`**
- **Documented Rationale**: *"The 0.50 floor represents minimum validation and application effort: development environment configuration, mandatory unit assessments, target-role contextualisation, practice drills, and capstone evaluation that must be completed even when partial competency exists."*

The floor reflects fixed pedagogical and technical setup requirements, strictly distinguishing itself from learner background, age, or speed.

---

## 3. Boundary & Partial-Gap Behavior

### Check 23: Mastered Skill Zero-Step Short-Circuit
If a worker profile fully satisfies all core and prerequisite requirements of a target role, M4 v1.1.0 short-circuits:
- **`total_pathway_steps`**: `0`
- **`total_estimated_hours_low`**: `0`
- **`total_estimated_hours_high`**: `0`
- **`status`**: `"NO_RESKILLING_REQUIRED"`
- **Audit Finding**: The 0.50 floor correctly **does not apply** to mastered skills.

### Check 24: Deficit-Scaled Effort Formulation
When a skill deficit $D \in (0.0, 1.0]$ exists, the effective multiplier $M_{\text{eff}}$ is computed as:

$$M_{\text{eff}} = M_{\text{floor}} + (M_{\text{max}} - M_{\text{floor}}) \times D$$

For $M_{\text{floor}} = 0.50$ and $M_{\text{max}} = 1.00$:
- When $D = 0.50$ (50% prior familiarity), $M_{\text{eff}} = 0.50 + 0.50 \times 0.50 = 0.75$.
- For `prompt_engineering` (base nominal range: $[10, 15]$ hours):
  - $h_{\text{low}} = \max(2, \text{round}(10 \times 0.75)) = 8$ hours.
  - $h_{\text{high}} = \max(8 + 2, \text{round}(15 \times 0.75)) = \mathbf{11}$ hours.

---

## 4. Floor Sensitivity Analysis (Floors 0.35, 0.50, 0.65)

### Check 25: Topological Prerequisite Invariance
Varying the floor between 0.35, 0.50, and 0.65 was evaluated across all 8 benchmark personas:
- **Prerequisite Step Sequence Invariance**: **100% INVARIANT**. Across all 3 floor settings, the ordered list of skill steps generated is identical.
- **Monotonic Effort Scaling**: For partial deficits, hours scale monotonically with the floor ($h_{0.35} < h_{0.50} < h_{0.65}$). For complete gaps ($D = 1.0$), effective multiplier is $1.00$, yielding stable baseline estimates.

---

## 5. Provenance, Anti-Fake-Precision & Pacing Disclaimers

### Checks 26 & 27: Time Provenance & Integer Ranges
- Every pathway step outputs an explicit `estimate_type` (`DEFICIT_SCALED_RANGE`, `PROVIDER_STATED`, or `SYSTEM_ESTIMATE`).
- All user-facing hour metrics are expressed as bounded integer ranges (`[total_estimated_hours_low, total_estimated_hours_high]`). Decimals such as `50.4` hours are restricted to internal macro-analytics and never presented as personal commitments.

### Check 28: Benchmark Pacing Disclaimers
- In benchmark reports, estimated weeks are derived using the test pace and are explicitly tagged:
  `"TEST ASSUMPTION: 10 STUDY HOURS/WEEK"`.
- In live API operation, `hours_per_week` is required from the user before emitting completion weeks. If omitted, `schedule_estimate: null` is returned to prevent deceptive velocity claims.

### Check 29: Pathway Totals Aggregation
Recomputation across all 8 benchmark personas confirms:
$$\sum_{i=1}^N h_{\text{low}, i} = \text{total\_estimated\_hours\_low} \quad \text{and} \quad \sum_{i=1}^N h_{\text{high}, i} = \text{total\_estimated\_hours\_high}$$
Zero double-counting or unallocated hours detected.
