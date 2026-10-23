# M3 Algorithmic Fairness & Demographic Neutrality Review

**Audit Focus**: Protected Attributes, Programmatic Rejection, Geographic Proxies, and Metric Semantics  
**Auditor**: Fairness Engineer & Explainable-AI Auditor  
**Date**: 2026-10-23  
**Status**: **`FAIRNESS SOUND — P2 UX RESILIENCE IMPROVEMENT IDENTIFIED`**  

---

## 1. Demographic Attribute Neutrality Audit

We audited [`src/role_matching_engine.py`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/src/role_matching_engine.py) against protected demographic attributes:
`age`, `gender`, `race`, `ethnicity`, `religion`, `marital_status`, `nationality`, `disability`, `socioeconomic_background`, `income`.

### Key Verification Findings:
1. **Zero Protected Inputs in Mathematical Path**: The equations for $S_{\text{fit}}$, $S_{\text{core}}$, $S_{\text{gap}}$, $M2_{\text{score}}$, and $M6_{\text{score}}$ rely strictly on skill IDs, requirement weights, labor shortage metrics, and scenario multipliers. Zero demographic attributes are present in any calculation.
2. **Deterministic Invariance**: Passing identical competency profiles produces identical Role Match Indices down to floating-point precision, satisfying the mathematical definition of demographic individual fairness.

---

## 2. Review of the Programmatic Rejection Mechanism (Audit 35 — P2-3)

Currently, [`_validate_profile`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/src/role_matching_engine.py#L65-L72) raises a fatal `ValueError` if any demographic key is detected:
```python
def _validate_profile(self, profile: Dict[str, Any]):
    for k in profile:
        if k.lower() in self.FORBIDDEN_DEMOGRAPHIC_KEYS:
            raise ValueError(f"Demographic variable '{k}' is strictly prohibited...")
```

### Forensic Critique & UX Risk:
- In a production recruitment or workforce advisory system, user profiles often originate from parsed CVs or upstream profile aggregators that naturally contain benign fields such as `age: 28`, `nationality: "Malaysian"`, or `address: "Subang Jaya"`.
- Raising an unhandled `ValueError` crashes the recommender session, creating a broken user experience.
- **Recommended Remediation (P2-3)**:
  Rather than crashing the entire matching pipeline, M3 should:
  1. Automatically **strip and ignore** all forbidden demographic fields before feature extraction.
  2. Log an explicit audit event: `PROTECTED_ATTRIBUTE_STRIPPED: ['age', 'nationality']`.
  3. Proceed with clean competency-only matching.

---

## 3. Geographic Labor Market Preferences vs. Personal Address (Audit 36)

Currently, `postcode` and `address` are listed in `FORBIDDEN_DEMOGRAPHIC_KEYS`.

### Methodological Distinction:
- **Protected Demographic Proxies (Prohibited)**: Personal home address, neighbourhood residential postcode, or family location history (which can act as proxies for racial or socioeconomic residential clustering).
- **Legitimate Labor Market Filters (Permissible)**: Explicit, user-selected regional job-market preferences (e.g. `preferred_region: "Penang"`, `"Klang Valley"`, or `"Sarawak"`).
- **Recommendation**: Ensure that future iterations of M3 cleanly decouple personal demographic home addresses (which must remain prohibited) from macro regional labor market filters (which are legitimate policy and preference parameters).

---

## 4. Benchmark Framing & Metric Semantics (Audits 38 & 39)

We conducted a forensic text search across all code and documentation for inappropriate predictive claims:
- **"Accuracy" / "Precision" / "Recall"**: None used to describe role matching outcomes. Benchmark results are strictly described as **sanity invariant evaluations** and **sensitivity stress tests**.
- **"Hiring Probability" / "Employment Success"**: None used. The metric is explicitly labeled **`ROLE_MATCH_INDEX`** ($0–100$), accompanied by the mandatory disclaimer:
  > *"ROLE MATCH INDEX IS AN EXPLAINABLE ALIGNMENT METRIC — NOT A HIRING DECISION OR PROBABILITY OF EMPLOYMENT"*.
- **Verdict**: Metric semantics and ethical framing are **`FULLY COMPLIANT`**.
