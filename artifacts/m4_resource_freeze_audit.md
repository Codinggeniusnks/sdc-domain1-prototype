# M4 Learning Resource Catalog & Provider Freeze Audit v1.1.0

**Reference Milestone**: Stage 12D Freeze Audit (Checks 7–20)  
**Target Module**: M4 Personalised Reskilling Pathway Engine v1.1.0  
**Status**: AUDITED, VERIFIED & FROZEN

---

## 1. Audit Scope & Verification Objective

This audit verifies that the production learning resource catalog (`data/reskilling/learning_resources_v1_1.json`) contains only authentic, live, verified educational resources, with all synthetic test fixtures strictly quarantined to test fixtures directories.

---

## 2. Production Catalog Integrity & Fixture Isolation

### Check 7 & 8: Synthetic Fixture Purging
- **Production Catalog Live Count**: Exactly **36** learning resources.
- **Test Fixtures in Production**: **0**.
- **Quarantined Fixtures**: `RES_LOWCOST_01` (RM99) and `RES_VAR_01` (VARIABLE_PRICE) have been relocated to `tests/fixtures/m4_resource_pricing_fixtures.json` with `test_only: true` and `fixture_type: "BENCHMARK_SYNTHETIC_TEST_FIXTURE"`.
- Automated tests in `tests/test_m4_freeze.py` verify that no resource in the production catalog has `test_only == true` or matches any fixture ID.

---

## 3. Live Verification & Cost Distribution

### Checks 9, 10, 11, 12: Cost Verification
All 36 production resources were reverified against official provider endpoints as of `2026-10-23`:
- **Verified Active & Reachable**: **36 / 36**
- **Changed / Moved**: **0**
- **Unavailable / Broken**: **0**
- **Unverifiable**: **0**

### Breakdown by Cost Status

| Cost Classification | Count | Audit Verification Standard |
|:---|:---:|:---|
| **`FREE`** | **31** | Verified 100% free access to syllabus, videos, and built-in exercises without mandatory subscription, credit card entry, or trial expiration. |
| **`FREE_TO_AUDIT`** | **5** | Verified free audit mode on Coursera / edX platforms. Optional certificate purchase is available but explicitly labeled and not required for learning mastery. |
| **`FREEMIUM`** | **0** | No paywalled core materials in production catalog. |
| **`LOW_COST`** | **0** | No synthetic low-cost fixtures in production. |
| **`VARIABLE_PRICE`** | **0** | Zero variable or subscription-only paywalls in production. |
| **`UNKNOWN`** | **0** | Zero unverified price statuses in production. |
| **Total Production** | **36** | **100% verified authentic courses** |

---

## 4. Provider Normalization & Institutional Grouping

### Checks 15 & 16: Institutional Taxonomy
The catalog normalizes 27 raw provider display labels into 21 parent institutional organizations:
- **Raw Provider Labels Count**: **27**
- **Normalized Institutional Parent Groups**: **21**

### Institutional Group Mapping Table

| Provider Group ID | Institutional Parent Organization | Raw Display Labels | Live Courses |
|:---|:---|:---|:---:|
| `DEEPLEARNING_AI` | DeepLearning.AI | DeepLearning.AI, DeepLearning.AI / Coursera, DeepLearning.AI / OpenAI, DeepLearning.AI / Weights & Biases, LangChain / DeepLearning.AI | 5 |
| `MICROSOFT` | Microsoft Corporation | Microsoft Learn | 6 |
| `ALPHABET` | Alphabet Inc. (Google / Kaggle) | Google Cloud Skills Boost / Coursera, Kaggle Learn | 4 |
| `OPEN_UNIVERSITY` | The Open University UK | OpenLearn / The Open University, The Open University (OpenLearn) | 3 |
| `FREECODECAMP` | freeCodeCamp | freeCodeCamp | 2 |
| `IBM` | IBM Corporation | IBM SkillsBuild | 1 |
| `CISCO` | Cisco Systems | Cisco Networking Academy | 1 |
| `MOZILLA` | Mozilla Corporation | Mozilla Developer Network (MDN) | 1 |
| `POSTMAN` | Postman Inc. | Postman Academy | 1 |
| `ZAPIER` | Zapier Inc. | Zapier Learn | 1 |
| `LEARN_PROMPTING` | LearnPrompting.org | LearnPrompting.org | 1 |
| `UNIV_HELSINKI` | University of Helsinki | University of Helsinki & MinnaLearn | 1 |
| `UNIV_ILLINOIS` | Univ. of Illinois Urbana-Champaign | University of Illinois / Coursera | 1 |
| `MACQUARIE_UNIV` | Macquarie University | Macquarie University / Coursera | 1 |
| `RIT` | Rochester Institute of Technology | Rochester Institute of Technology / edX | 1 |
| `JPDP_MALAYSIA` | Jabatan Perlindungan Data Peribadi | Department of Personal Data Protection Malaysia (JPDP) | 1 |
| `MOSTI_MALAYSIA` | MOSTI Malaysia | Ministry of Science, Technology and Innovation (MOSTI) Malaysia | 1 |
| `BURSA_MALAYSIA` | Bursa Malaysia Berhad | Bursa Malaysia Berhad | 1 |
| `UN_GLOBAL_COMPACT`| United Nations Global Compact | UN Global Compact Academy | 1 |
| `GHG_PROTOCOL` | Greenhouse Gas Protocol Initiative | Greenhouse Gas Protocol / WRI / WBCSD | 1 |
| `OMG_CAMUNDA` | Camunda & Object Management Group | Camunda / Object Management Group | 1 |

Aliasing audits confirm that unrelated entities are never co-grouped, while related subsidiaries (e.g. Kaggle and Google Cloud under Alphabet) are properly consolidated for institutional diversity filtering.

---

## 5. Architectural Independence Proofs

### Check 19: Catalog Order Independence
Shuffling the order of resources in `learning_resources_v1_1.json` resulted in **zero changes** to the generated sequence of pathway steps for all benchmark personas.

### Check 20: Resource Failure Independence
Completely clearing the resource catalog (`engine.resources = []`) preserves:
1. The exact same ordered sequence of required skills.
2. The exact same priority scores and phase allocations.
3. The exact same learning hour estimates.

Course availability issues never redefine educational skill gaps.
