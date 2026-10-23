# O1 Cohort Reskilling Plan Freeze Audit — v1.1.0

## 1. Executive Summary
This document provides the formal audit of the multi-phase **Cohort Reskilling Roadmap** and curriculum planning algorithms in `O1 Workforce Gap Engine v1.1.0`. It verifies roadmap phasing, privacy filtering, learner-hour semantics, and the jurisdictional boundary with M4 Personalised Reskilling Pathways.

## 2. Cohort Roadmap Phasing Architecture
O1 generates structured, dependency-aware cohort training roadmaps organized into three distinct pedagogical phases:

```
[Phase 1: Foundational Capabilities]
  - High prerequisite centrality (C(s) >= 0.35)
  - Zero unmet prerequisite dependencies in graph
  - Unlocks subsequent technical learning
         |
         v
[Phase 2: Core Domain Competencies]
  - High CORE gap prevalence across cohort
  - Critical occupational requirements
         |
         v
[Phase 3: Advanced & Transferable Capabilities]
  - High cross-role transferability (T(s) >= 0.50)
  - Scenario-urgent specializations (U(s) >= 0.50)
```

## 3. Learner-Hours vs Calendar Duration Weeks
O1 strictly separates cumulative effort from cohort pacing to prevent misinterpretation:
- **Total Learner-Hours (`total_learner_hours`)**: Represents the total human capital investment across the enterprise:
  $$\text{Learner-Hours}(s) = N_{\text{affected}}(s) \times \text{EstimatedHours}(s)$$
  Used by HR for corporate training budget allocation and vendor procurement.
- **Estimated Calendar Duration (`estimated_calendar_duration_weeks`)**: Represents the chronological elapsed time for a cohort:
  $$\text{CalendarWeeks}(s) = \left\lceil \frac{\text{EstimatedHours}(s)}{\text{PacingHoursPerWeek}} \right\rceil$$
  Assuming a standard corporate pacing of 5–8 hours/week. Calendar weeks do NOT scale linearly with cohort size.

## 4. Privacy Filtering in Cohort Plans
- If a recommended training cohort contains fewer than 5 employees ($N < 5$), O1 suppresses the collective cohort plan.
- The plan status is marked `INDIVIDUAL_M4_RECOMMENDED`, and the small employee group is directed to individual self-paced pathways in M4 to prevent managerial tracking of minority learning needs.

## 5. Sovereign Boundary: O1 Macro Planning vs M4 Individual Authority
- **O1 Jurisdiction**: Strategic macro workforce planning, collective training procurement, departmental budgeting, and organization-wide reskilling schedules.
- **M4 Jurisdiction**: Sovereign individual pathway construction, elective course selection, real-time pace adaptation, and personal milestone tracking.
- **Boundary Invariant**: O1 cohort recommendations provide guidance and scheduling frameworks; they **NEVER** override an individual employee's M4 personalized learning pathway.
