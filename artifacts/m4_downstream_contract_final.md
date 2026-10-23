# M4 Downstream Interface Contract Specification (Final Freeze)

**Reference Milestone**: Stage 12D Freeze Audit (Checks 49–51)  
**Producer Module**: M4 Personalised Reskilling Pathway Engine v1.1.0 (FORMALLY FROZEN)  
**Consumer Modules**: M5 SDG & Socioeconomic Impact Engine (UNBUILT), Career Navigation UI  
**Status**: APPROVED, RATIFIED & IMMUTABLE

---

## 1. Modular Boundary Guarantees

1. **Role of M4**: M4 is strictly an educational reskilling pathway engine. It sequences curriculum gaps, attaches verified learning resources, computes effort ranges, and evaluates empirical evidence confidence.
2. **Decoupling from M5**: M4 contains zero SDG impact scores, ESG carbon offsets, or macroeconomic return metrics. Those calculations belong exclusively to M5.
3. **Decoupling from UI**: M4 emits strictly typed, structured JSON payloads. Presentation details, styling, and localization reside in the UI layer.
4. **Employment Guarantee Prohibition**: In strict compliance with Labour-Market ethics, M4 payloads make no claims regarding job guarantees, hiring probabilities, or career success certitude.

---

## 2. Guaranteed Pathway Output Schema

Every pathway returned by `ReskillingPathwayEngine.build_pathway` adheres to the following immutable JSON structure:

```typescript
interface ReskillingPathwayPayload {
  pathway_id: string;                                // e.g. "PATHWAY_2512_REFERENCE_2026"
  engine_version: "1.1.0";
  target_role: string;                               // MASCO 4-digit code (e.g. "2512")
  occupation_title: string;                          // MASCO occupation title
  scenario_id: string;                               // e.g. "REFERENCE_2026"
  transition_distance: string;                       // "SHORT TRANSITION" | "MODERATE TRANSITION" | "LONG TRANSITION" | "ZERO TRANSITION"
  status: "RESKILLING_PATHWAY_GENERATED" | "NO_RESKILLING_REQUIRED";
  total_pathway_steps: number;                      // Integer >= 0
  missing_core_count: number;                       // Integer >= 0
  total_estimated_hours_low: number;                // Integer >= 0
  total_estimated_hours_high: number;               // Integer >= 0
  schedule_estimate: ScheduleEstimate | null;       // Null unless user explicitly supplies hours_per_week
  verified_cost_summary: VerifiedCostSummary;
  pathway_evidence_confidence_index: number;        // Float in [0.0, 100.0]
  pathway_evidence_confidence_label: "HIGH" | "MEDIUM" | "LOW" | "INSUFFICIENT";
  pathway_evidence_confidence_components: {
    skill_gap_evidence: number;                     // 0.30 weight
    prerequisite_evidence_quality: number;          // 0.25 weight
    resource_verification_quality: number;          // 0.25 weight
    resource_freshness: number;                     // 0.20 weight
  };
  pathway_evidence_confidence: {
    score: number;
    label: string;
    components: Record<string, number>;
    confidence_reducing_flags: string[];
    confidence_source_refs: string[];
    m3_evidence_confidence_context: number;
  };
  pathway_steps: PathwayStep[];
  quality_flags: string[];
  warnings: string[];
  generated_date: string;                           // "YYYY-MM-DD"
  resource_verification_date: string;               // "YYYY-MM-DD"
}

interface PathwayStep {
  step_number: number;
  skill_id: string;
  skill_name: string;
  phase: "FOUNDATION" | "CORE ROLE SKILLS" | "AI-ERA ADAPTATION" | "OPTIONAL SPECIALISATION";
  priority_tier: "FOUNDATION_PREREQUISITE" | "CORE_REQUIREMENT" | "IMPORTANT_REQUIREMENT" | "SUPPORTING_REQUIREMENT";
  priority_score: number;
  reason_for_priority: string;
  deficit: number;                                  // Float in [0.0, 1.0]
  direct_prerequisites: string[];                   // Topological upstream skill_ids
  effort_category: "QUICK_FOUNDATION" | "SHORT" | "MODERATE" | "COMPREHENSIVE";
  estimated_hours_low: number;                      // Bounded integer
  estimated_hours_high: number;                     // Bounded integer
  estimate_type: "DEFICIT_SCALED_RANGE" | "PROVIDER_STATED" | "SYSTEM_ESTIMATE";
  estimation_rationale: string;
  scenario_relevance: number;
  transferability_pct: number;
  status: "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED" | "SKIPPED_BY_USER";
  resources: {
    primary_resource: ResourceDetail | null;
    alternative_resource: ResourceDetail | null;
    practice_resource: ResourceDetail | null;
    resource_selection_rationale: string;
  };
}

interface ResourceDetail {
  resource_id: string;
  title: string;
  provider_display_name: string;
  provider_group_id: string;                        // 21 normalized institutional groups
  provider_group_name: string;
  cost_status: "FREE" | "FREE_TO_AUDIT" | "LOW_COST" | "VARIABLE_PRICE" | "UNKNOWN";
  cost_amount_if_verified: number | null;
  currency_if_verified: string;
  official_url: string;
  skill_alignment: number;
  provider_reliability: number;
  last_verified_date: string;
}

interface VerifiedCostSummary {
  minimum_verified_cost_myr: number;
  maximum_verified_cost_myr: number;
  currency: "MYR";
  low_cost_threshold_myr: 150.0;
  cost_preference_applied: string;
  operational_disclaimer: string;
  unknown_cost_items_count: number;
  unknown_cost_items: Array<{
    resource_id: string;
    title: string;
    cost_status: string;
  }>;
}

interface ScheduleEstimate {
  study_hours_per_week: number;
  estimated_weeks_low: number;
  estimated_weeks_high: number;
  label: "USER-SCHEDULE-DEPENDENT ESTIMATE";
}
```

---

## 3. Guarantees for Future M5 Development

1. **Topological Order Integrity**: Future M5 can safely assume that `pathway_steps` is sequentially ordered according to pedagogical necessity.
2. **Socioeconomic Impact Independence**: The commercial cost of an educational resource (free vs paid) must not bias or distort M5's calculation of SDG 8 (Decent Work and Economic Growth) or SDG 4 (Quality Education) impact scores.
3. **Decoupled Updateability**: M4's resource catalog may be refreshed on a quarterly schedule without invalidating M5's downstream impact modeling rules.
