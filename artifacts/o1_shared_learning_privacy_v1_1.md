# O1 Shared Learning Privacy & Hour Semantics v1.1.0

**Reference Date:** 2026-10-24  
**Defect Resolved:** DEF-P1-01 (Shared Learning Small-Subgroup Disclosure)  

---

## 1. Problem Statement & Vulnerability Analysis

In O1 v1.0.0, `identify_shared_learning_opportunities` applied a candidate inclusion threshold of `count >= 2`.
In the synthetic 50-profile benchmark, this caused `instructional_design` to be published with `profiles_affected: 2`. In an enterprise department of 50 people, HR managers knowing which two employees expressed this learning need could immediately re-identify their confidential reskilling trajectories.

---

## 2. Remediated Shared Learning Logic

Under O1 v1.1.0:
1. **Public Employer Listing Floor:** A shared learning module is only surfaced in employer-facing listings if:
   $$\text{profiles\_affected} \ge 5$$
2. **Small-Cell Handling:** Modules with $1 \le N < 5$ affected workers are excluded from default employer listings and aggregated into audit metadata:
   - `additional_small_cell_learning_needs_suppressed: true`
   - `small_cell_learning_needs_suppressed_count: 1`
3. **Suppressed Serialization:** When serialized in diagnostic mode, the affected count is emitted as:
   `{"profiles_affected": null, "profiles_affected_display": "<5", "candidate_shared_resources": ["SUPPRESSED"]}`

---

## 3. Hour Semantics Separation

To prevent HR managers from misinterpreting training hours as project completion schedules, O1 v1.1.0 enforces strict semantic decoupling:
- **Shared Curriculum Hours:** Duration of the joint instructional module (e.g. `[15, 30]` hours). This is the session length.
- **Aggregate Learner-Hours:** Total organizational person-hours invested:
  $$\text{Aggregate Hours} = \text{profiles\_affected} \times \text{Session Hours}$$
- **Disclaimers:** Explicitly states that joint session duration must never be multiplied as project calendar time.
