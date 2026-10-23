# Forensic Audit: Pathway Evidence Confidence Architecture & Saturation Analysis v1.0.0

**Module**: M4 Personalised Reskilling Pathway Engine v1.0.0  
**Target Asset**: [`src/reskilling_pathway_engine.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/src/reskilling_pathway_engine.py) (lines 218–264)  
**Audit Role**: Independent Senior Recommender-Systems Methodologist & Evidence-Grounding Auditor  
**Date**: 2026-10-23  
**Audit Scope**: Audits 41, 42, 43 (Decoupling, Calibration, Component Weights, Benchmark Saturation)  
**Evidence Engine Verdict**: **`REMEDIATION REQUIRED (P1 DEFECT IDENTIFIED)`**

---

## 1. Executive Summary & Core Architectural Principle

In explainable AI systems for workforce development, **Pathway Evidence Confidence** must quantify the empirical trustworthiness of the recommendations—measuring data freshness, alignment quality of external learning resources, and prerequisite mapping confidence.

### Upstream Safety Guarantee (Audit 41 & 43)
1. **M3 Decoupling**: Pathway Evidence Confidence is evaluated **independently** from M3's Role Match Index and M3 Evidence Confidence. A high M3 match score does not artificially inflate pathway confidence, and a low M3 match score does not penalize pathway resource trustworthiness.
2. **Hours Independence**: Pathway Evidence Confidence **never alters learning hours or adds remedial steps**. A pathway with lower evidence confidence informs the user of data uncertainty; it does not assign more homework.

### Critical P1 Finding (Audit 42)
While the architectural design is sound, the implementation in `src/reskilling_pathway_engine.py` contains a critical defect: **the four underlying evidence components are statically hardcoded**, causing **100% of benchmark pathways to output an identical saturated confidence score of `94.5` (`HIGH`)**.

---

## 2. Mathematical Formulation & Component Weights (Audit 41)

In [`data/reskilling/m4_scoring_config_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/reskilling/m4_scoring_config_v1.json), Pathway Evidence Confidence is defined as a weighted linear combination of four empirical dimensions:

$$\text{Confidence Score} = w_{\text{gap}} \cdot S_{\text{gap}} + w_{\text{prereq}} \cdot S_{\text{prereq}} + w_{\text{res}} \cdot S_{\text{res}} + w_{\text{fresh}} \cdot S_{\text{fresh}}$$

Where:
* $w_{\text{gap}} = 0.30$ (Skill gap grounding in M3 and Malaysian national standards)
* $w_{\text{prereq}} = 0.25$ (Authoritative grounding of prerequisite dependencies)
* $w_{\text{res}} = 0.25$ (Official verification and domain quality of learning resources)
* $w_{\text{fresh}} = 0.20$ (Verification recency and absence of link rot)

### Weight Summation Invariant
$$\sum w_i = 0.30 + 0.25 + 0.25 + 0.20 = 1.00 \quad \text{(Verified Exact)}$$

### Threshold Classification Bands
* $\ge 85.0 \implies$ **`HIGH`**
* $70.0 – 84.9 \implies$ **`MEDIUM`**
* $50.0 – 69.9 \implies$ **`LOW`**
* $< 50.0 \implies$ **`INSUFFICIENT`**

---

## 3. Forensic Root-Cause Analysis of P1 Saturation Defect (Audit 42)

In `src/reskilling_pathway_engine.py` (lines 227–244), the method `_calculate_pathway_confidence()` is implemented as follows:

```python
def _calculate_pathway_confidence(
    self,
    steps: List[Dict[str, Any]],
    role_evidence_confidence: float
) -> Tuple[float, str, Dict[str, float]]:
    w_cfg = self.config["pathway_evidence_confidence"]["component_weights"]
    
    # 1. Skill gap evidence score (grounded in M3 and Malaysian standards)
    gap_ev = 95.0
    # 2. Prerequisite evidence quality
    prereq_ev = 92.0
    # 3. Resource verification quality (official portals, 0 broken links)
    res_ev = 96.0
    # 4. Resource freshness
    fresh_ev = 95.0

    score = (
        w_cfg["skill_gap_evidence"] * gap_ev +
        w_cfg["prerequisite_evidence_quality"] * prereq_ev +
        w_cfg["resource_verification_quality"] * res_ev +
        w_cfg["resource_freshness"] * fresh_ev
    )
    score = round(max(0.0, min(100.0, score)), 1)
```

### Numerical Evaluation
$$\text{Score} = (0.30 \times 95.0) + (0.25 \times 92.0) + (0.25 \times 96.0) + (0.20 \times 95.0)$$
$$\text{Score} = 28.5 + 23.0 + 24.0 + 19.0 = 94.5$$

### Defect Consequences
1. **Zero Variance**: Across all 8 synthetic benchmark personas in `data/reskilling/m4_benchmark_results_v1.json`, every single pathway receives `pathway_evidence_confidence: 94.5`.
2. **False Insensitivity**:
   * A pathway with simple, single-step skills and 100% verified government resources receives `94.5`.
   * A pathway with multi-hop prerequisite dependencies, complex third-party MOOCs, or synthetic fixtures (`RES_LOWCOST_01`, `RES_VAR_01`) also receives `94.5`.
3. **Audit Assessment**: This is an uncalibrated, mock-saturated implementation that violates the requirements of an empirical explainable-AI system. It is classified as **`P1 (Must Fix Before User-Facing UI / M5 Freeze)`**.

---

## 4. Required Dynamic Calculation Architecture for Stage 12C

To remediate Defect `M4-P1-01`, `_calculate_pathway_confidence()` must dynamically aggregate empirical metrics from the active pathway:

### 1. Dynamic Resource Verification Score ($S_{\text{res}}$)
Computed as the average alignment and reliability of the attached primary resources across all $N$ steps:
$$S_{\text{res}} = \frac{100}{N} \sum_{i=1}^{N} \left(0.50 \cdot \text{Alignment}(r_i) + 0.50 \cdot \text{Reliability}(r_i)\right)$$

### 2. Dynamic Prerequisite Quality Score ($S_{\text{prereq}}$)
Computed from the mean mapping confidence of the active prerequisite edges utilized in the pathway:
$$S_{\text{prereq}} = 100 \cdot \frac{1}{|E_{\text{active}}|} \sum_{e \in E_{\text{active}}} \text{Confidence}(e)$$
*(If the pathway has zero active prerequisite dependencies, defaults to baseline 95.0).*

### 3. Dynamic Gap Evidence Score ($S_{\text{gap}}$)
Calibrated to the proportion of CORE vs SUPPORTING requirements and verified source backing:
$$S_{\text{gap}} = 90.0 + 10.0 \cdot \frac{N_{\text{core}}}{N}$$

### 4. Dynamic Freshness Score ($S_{\text{fresh}}$)
Calculated based on days elapsed since `last_verified_date`:
$$S_{\text{fresh}} = \max\left(70.0, 100.0 - 0.10 \times \text{DaysElapsed}\right)$$

---

## 5. Verification of Decoupling Invariants (Audit 41 & 43)

The audit verified that even with the hardcoded mock score:
1. **M3 Decoupling**: M3 Evidence Confidence ($85.0$) is passed strictly as context metadata in `"m3_evidence_confidence_context"`; it does not multiply or distort the pathway score.
2. **Effort Independence**: In `_calculate_step_effort()`, learning hours $[h_{\text{low}}, h_{\text{high}}]$ depend strictly on baseline complexity and skill deficit. Pathway evidence confidence has **zero mathematical influence on hours**.

---

## 6. Audit Verdict

* **Component Weights**: **`VALID (Sum = 1.00)`**
* **M3 Decoupling**: **`VALID`**
* **Hours Independence**: **`VALID`**
* **Benchmark Calibration**: **`FAILED (P1 DEFECT: STATIC SATURATION AT 94.5)`**
* **Remediation Requirement**: **`MANDATORY DYNAMIC RECALIBRATION IN STAGE 12C`**
