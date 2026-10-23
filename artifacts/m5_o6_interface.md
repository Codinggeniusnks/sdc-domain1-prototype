# M5-to-O6 Aggregated Regional & Enterprise SDG Impact Interface

**System:** M5 SDG Impact Mapping Engine v1.0.0  
**Stage:** Stage 13A Architecture & Mapping  
**Date:** 2026-10-24  
**Author:** Senior Sustainability Data Architect, Quantitative Scenario Engineer  
**Downstream Target:** O6 Regional & Enterprise Aggregation Engine (Stage 14)  
**Status:** Architectural Specification & Contract Definition (Non-Executable Interface)

---

## 1. Context & Scope Separation

### Current Stage 13A Boundary:
M5 is strictly bounded to **individual entity-level mapping**:
- Skill $\to$ SDGs & Targets
- Occupation $\to$ SDGs & Targets
- Individual Learner Reskilling Pathway $\to$ SDGs & Targets

### Future Stage 14 Scope (O6):
O6 will aggregate individual reskilling trajectories across:
- **Enterprise Cohorts:** How a company's internal mobility program aligns with its corporate Bursa Malaysia / CSRD sustainability disclosures.
- **Regional & Economic Corridors:** How workforce upskilling in Penang (semiconductors) or Johor-Singapore Special Economic Zone (data centres & clean tech) advances national NETR and NIMP 2030 targets.

M5 provides the **unbiased, granular micro-data foundations** that O6 will ingest. M5 does NOT compute enterprise aggregations or macro indices directly.

---

## 2. Mathematical Aggregation Model for O6

When O6 aggregates $N$ individual workforce pathways $\{\mathcal{P}_1, \mathcal{P}_2, \dots, \mathcal{P}_N\}$ within an enterprise or region, it will consume M5's categorical outputs using the following formal aggregation framework:

### A. Target Prevalence Index ($TPI_k$):
For each official SDG Target $k \in \mathcal{T}$:

$$TPI_k = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(k \in \mathcal{P}_i.\text{targets\_addressed})$$

Where $\mathbb{I}(\cdot)$ is the indicator function indicating whether pathway $i$ develops capabilities addressing Target $k$.

### B. Direct vs. Enabling Capability Ratio ($DER_j$):
For each SDG Goal $j \in \{1, \dots, 17\}$:

$$DER_j = \frac{\sum_{i=1}^N \mathbb{I}(j \in \mathcal{P}_i.\text{direct\_sdgs})}{\sum_{i=1}^N \mathbb{I}(j \in \mathcal{P}_i.\text{direct\_sdgs}) + \sum_{i=1}^N \mathbb{I}(j \in \mathcal{P}_i.\text{enabling\_sdgs}) + \epsilon}$$

This metric provides corporate sustainability officers with an audited ratio distinguishing between **core green/sustainability roles** (e.g. environmental engineering, carbon accounting) and **enabling digital infrastructure roles** (e.g. cloud engineers, Python programmers).

---

## 3. Emitted Data Contract for O6 Ingestion

M5 provides an export contract allowing O6 to query batch pathways deterministically:

### Export Batch Record Schema:
```json
{
  "batch_id": "string",
  "evaluated_at": "ISO-8601 UTC timestamp",
  "pathway_evaluations": [
    {
      "pathway_id": "string",
      "learner_id": "string (pseudonymized)",
      "target_role_code": "string",
      "target_role_title": "string",
      "direct_sdgs": [12, 13],
      "enabling_sdgs": [8, 9, 17],
      "contextual_sdgs": [],
      "targets_addressed": ["12.6", "13.2", "8.2", "9.5", "17.18"],
      "quality_flags": ["OFFICIAL_TARGET_TRACEABLE", "GENERAL_PURPOSE_SAFE"]
    }
  ]
}
```

---

## 4. Downstream Safeguards for O6 Execution

When O6 is implemented in Stage 14, it must strictly adhere to the following M5 governance rules:
1. **No Synthetic Metric Inflation:** O6 must aggregate **capability headcount and target prevalence**, never synthetic "metric tons of carbon reduced by training". Training a programmer in Python does not equate to verified carbon sequestration.
2. **Auditability:** Every enterprise sustainability claim produced by O6 must maintain drill-down traceability back to specific M5 target-level evidence references.
3. **Data Privacy Compliance:** Regional aggregations must enforce $k$-anonymity ($k \ge 5$) to prevent re-identification of individual employees from small enterprise cohorts under Malaysia's PDPA 2010.

---

## 5. Interface Readiness Verdict

The M5 data structures and APIs are fully decoupled, typed, and ready to support O6 aggregation in Stage 14 without requiring changes to frozen M5 core mappings.
