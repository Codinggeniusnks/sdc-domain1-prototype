# O1 Role Transition Privacy & Terminology Disambiguation v1.1.0

**Reference Date:** 2026-10-24  
**Defect Resolved:** DEF-P1-02 (Role Transition Volume Exposure) & DEF-P3-02  

---

## 1. Vulnerability Analysis: Transition Volume Exposure

In O1 v1.0.0, `build_role_gap_summary` emitted exact counts for all 33 role transitions in the 50-profile synthetic cohort (all of which had volume $1..4$). For example, knowing that exactly 1 worker is transitioning from MASCO 2151 to MASCO 2152 allows instant individual re-identification.

---

## 2. Remediated Transition Privacy

In O1 v1.1.0:
- Any transition pair with $0 < \text{volume} < 5$ is masked:
  - `transition_volume: null`
  - `transition_volume_display: "<5"`
  - `transition_percentage: null`
  - `transition_percentage_display: "<10%"`
  - `suppressed: true`
  - `suppression_reason: "SMALL_CELL_PRIVACY"`
  - `common_missing_core_skills: ["SUPPRESSED_SMALL_CELL"]`
  - `average_pathway_effort_range: null`
- Only transitions with $\text{volume} \ge 5$ expose numerical volume and skill breakdowns.

---

## 3. Terminology Disambiguation: Transition Pressure

To prevent misinterpretation of transition analytics:
> **Regulatory Notice:** **Role Transition Pressure** measures the collective capability distance between workers' current skills and future target roles. It is a curriculum design metric. It does **NOT** measure employee turnover probability, attrition risk, or workforce redundancy.
