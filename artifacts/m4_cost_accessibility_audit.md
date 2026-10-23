# Forensic Audit: Cost Policy, Accessibility & Financial Grounding v1.0.0

**Module**: M4 Personalised Reskilling Pathway Engine v1.0.0  
**Target Policy**: Free-First Mode, Low-Cost Thresholds, and Truth-in-Pricing Architecture  
**Evaluation Milestone**: Stage 12A Implementation Audit  
**Date**: 2026-10-23  
**Status**: **`VERIFIED & APPROVED`**

---

## 1. Executive Summary: The Free-First Mandate

Workforce reskilling initiatives must not create financial barriers for workers seeking transition. A core design mandate for M4 is **democratized accessibility**: learners must be able to complete end-to-end skill acquisition toward any target role using verified free resources.

### Verified Benchmark Finding
Across all **8 synthetic benchmark transition pathways** evaluated under default `FREE_FIRST` mode:
* **Minimum Verified Direct Learning Cost**: **`RM 0.00`** (100% accessible at zero tuition cost).
* **Maximum Optional Certification Cost**: RM 0.00 to RM 220.00 (optional verified credentials from Coursera / edX).
* **Unknown / Variable Cost Items**: Isolated and tracked in `unknown_cost_items`, strictly prevented from collapsing to zero.

---

## 2. Malaysian Low-Cost Threshold Definition

To provide an objective threshold relevant to the Malaysian labor market, M4 establishes a formal price ceiling in [`data/reskilling/m4_scoring_config_v1.json`](file:///C:/Users/LENOVO/.gemini/antigravity/scratch/sdc-domain1-prototype/data/reskilling/m4_scoring_config_v1.json):

$$\text{Threshold}_{\text{MYR}} = \text{RM } 150.00 \quad (\approx \$35.00 \text{ USD})$$

### Regulatory & Economic Justification
* **Benchmark Reference**: RM 150 represents approximately $5\%$ of the median entry-level clerical monthly salary in Malaysia (DOSM Salaries & Wages Survey 2024), representing an affordable, accessible out-of-pocket threshold for continuing vocational education.
* **Classification Rules**:
  * Direct course fee $\le \text{RM } 150.00 \implies$ `LOW_COST`
  * Direct course fee $> \text{RM } 150.00 \implies$ `PREMIUM / COMMERCIAL` (Excluded from primary free-first pathways)

---

## 3. Truth-in-Pricing & Cost Classification Matrix

M4 enforces strict labeling standards to protect learners from hidden fees and deceptive freemium models:

| Cost Status | Technical Definition | Verification Requirement | Example Resource |
|:---|:---|:---|:---|
| **`FREE`** | 100% of instructional content, exercises, sandbox environments, and completion badges are freely accessible. | No credit card required. No trial expiration. | freeCodeCamp (`RES_PY_01`), Kaggle Learn (`RES_SQL_01`), Microsoft Learn (`RES_AUTO_01`) |
| **`FREE_TO_AUDIT`** | Full course materials, video lectures, and readings are accessible at zero cost, but official verified certificates require payment. | Certificate fee must be explicitly recorded in `certificate_cost_if_verified`. | Coursera "AI for Everyone" (`RES_AI_LIT_01`, cert $49 USD) |
| **`FREEMIUM`** | Basic content is free, but key exercises, assignments, or graded labs require paid subscription. | Quota limitations and upgrade pricing must be documented. | None permitted in primary pathways without open alternative. |
| **`LOW_COST`** | Direct enrollment fee is charged, but total cost is $\le \text{RM } 150.00$. | Fee schedule must be verified against official payment portal. | Community Technical Academy API Lab (`RES_LOWCOST_01`, RM99) |
| **`UNKNOWN`** | Pricing is variable, subject to institutional quotation, or unverified. | **Must never collapse to RM 0.00.** Tracked in `unknown_cost_items`. | Regional Sustainability Workshop (`RES_VAR_01`) |

---

## 4. Deceptive Pricing Prevention: Negative Invariants Proven

### Invariant 1: Trial Access Prohibition
A resource that offers a "7-day free trial" with mandatory credit card billing is **strictly prohibited** from receiving the `FREE` label. Such resources are flagged as commercial subscriptions.

### Invariant 2: Unknown Cost Segregation
When a course fee cannot be verified with certainty:
* `cost_amount_if_verified` is set to `None`.
* `cost_status` is set to `"UNKNOWN"`.
* The resource is excluded from primary selection when verified free equivalents exist.
* If attached, it increments `unknown_cost_items_count` in the pathway payload.

### Invariant 3: Certificate Decoupling
M4 explicitly decouples learning mastery from certificate purchase. Learners are informed:
> *"The full curriculum and interactive exercises are 100% free to audit. Purchasing a certificate is optional and not required to acquire the underlying competency."*

---

## 5. Audit Sign-Off

The cost policy and accessibility mechanisms satisfy all consumer protection and empirical rigor requirements:
* **Check 21**: **PASS (Free-First Mode Successfully Selects Zero-Cost Alternatives)**
* **Check 26**: **PASS (Cost Summary Accurately Aggregates Min, Max, and Unknowns)**
* **Zero Hidden Fees**: **PASS**
