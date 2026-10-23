# M4 Provider Normalization & Institutional Grouping v1.1.0

**Reference Milestone**: Stage 12C Remediation (Audit Finding M4-P2-01)  
**Target Module**: M4 Personalised Reskilling Pathway Engine v1.1.0  
**Status**: COMPLETE & VERIFIED

---

## 1. Problem Statement & Audit Findings

During the Stage 12B methodology review, Auditor Argon observed that while the learning resource catalog contained 36 production resources across 27 distinct provider strings, several entries represented different divisions or branding arms of identical parent institutions (e.g., "DeepLearning.AI via Coursera", "DeepLearning.AI", "DeepLearning.AI via DeepLearning.AI Platform"; "Google Career Certificates", "Google Cloud via Coursera", "Kaggle Learn").

Without an explicit parent grouping taxonomy:
1. Diversity filtering could not guarantee cross-institution resource recommendation.
2. Employer partner and national training agency auditing lacked aggregate institutional reporting.
3. Users could receive two "alternative" resources that both emanated from the same parent provider.

---

## 2. Institutional Normalization Architecture

In M4 v1.1.0, every learning resource in `data/reskilling/learning_resources_v1_1.json` provides a dual-layer provider representation:
- **`provider_display_name`** (string): The user-facing, brand-accurate provider label (27 distinct values across 36 courses).
- **`provider_group_id`** (string): An uppercase identifier denoting the parent legal/educational institution (21 distinct groups).
- **`provider_group_name`** (string): The formal canonical name of the parent institution.

This normalization allows the pathway engine's alternative resource selection heuristic to actively seek resources with `r.provider_group_id != primary.provider_group_id`, guaranteeing true multi-vendor institutional diversity.

---

## 3. Comprehensive Institutional Taxonomy Mapping (36 Live Courses)

| Provider Group ID | Normalized Institutional Parent Name | Raw Provider Display Labels Mapped | Live Course Count | Example Courses |
|:---|:---|:---|:---:|:---|
| `DEEPLEARNING_AI` | DeepLearning.AI | • DeepLearning.AI<br>• DeepLearning.AI via Coursera<br>• DeepLearning.AI via DeepLearning.AI Platform | 5 | Prompt Engineering for Developers, LangChain for LLM App Dev, Building Systems with ChatGPT API |
| `ALPHABET` | Alphabet Inc. (Google / Kaggle) | • Google Career Certificates<br>• Google Cloud via Coursera<br>• Kaggle Learn | 4 | Google Data Analytics Professional Certificate, Introduction to Generative AI, Kaggle Python |
| `OPEN_UNIVERSITY` | The Open University UK | • OpenLearn (The Open University UK) | 3 | Commercial Awareness, Introducing Environment, Work and the Environment |
| `MICROSOFT` | Microsoft Corporation | • Microsoft Learn<br>• Microsoft via Coursera | 6 | Microsoft Azure AI Fundamentals, Transform Business with AI, Copilot for M365, PL-900 Power Platform |
| `IBM` | IBM Corporation | • IBM SkillsBuild | 1 | Getting Started with Artificial Intelligence |
| `CISCO` | Cisco Systems | • Cisco Networking Academy | 1 | Data Analytics Essentials |
| `MOZILLA` | Mozilla Corporation | • MDN Web Docs | 1 | Getting Started with the Web (MDN) |
| `POSTMAN` | Postman Inc. | • Postman Academy | 1 | Postman API Fundamentals Student Expert |
| `ZAPIER` | Zapier Inc. | • Zapier Learn | 1 | Zapier Getting Started with Automation |
| `FREECODECAMP` | freeCodeCamp | • freeCodeCamp | 2 | Python for Everybody, Scientific Computing with Python |
| `LEARN_PROMPTING` | LearnPrompting | • LearnPrompting.org | 1 | Introductory Course on Generative AI |
| `UNIV_HELSINKI` | University of Helsinki | • University of Helsinki & MinnaLearn | 1 | Elements of AI: Introduction to AI |
| `UNIV_ILLINOIS` | University of Illinois Urbana-Champaign | • University of Illinois via Coursera | 1 | Process Mining in Healthcare / Business |
| `MACQUARIE_UNIV` | Macquarie University | • Macquarie University via Coursera | 1 | Excel Skills for Business: Essentials |
| `RIT` | Rochester Institute of Technology | • RIT via edX | 1 | Critical Thinking & Problem Solving |
| `JPDP_MALAYSIA` | Jabatan Perlindungan Data Peribadi Malaysia | • JPDP Malaysia | 1 | Panduan Asas Akta Perlindungan Data Peribadi 2010 |
| `MOSTI_MALAYSIA` | Ministry of Science, Technology and Innovation Malaysia | • MOSTI / ASM Malaysia | 1 | Malaysia National AI Guidelines (Pelan AI Negara) |
| `BURSA_MALAYSIA` | Bursa Malaysia Berhad | • Bursa Malaysia | 1 | Bursa Malaysia ESG Reporting Guide & Toolkit |
| `UN_GLOBAL_COMPACT` | United Nations Global Compact | • UN Global Compact Academy | 1 | Setting Science-Based Targets Basics |
| `GHG_PROTOCOL` | Greenhouse Gas Protocol Initiative | • GHG Protocol | 1 | Introduction to the GHG Protocol Corporate Standard |
| `OMG_CAMUNDA` | Object Management Group & Camunda | • Camunda Academy / OMG | 1 | BPMN 2.0 Process Modeling Masterclass |

### Summary Statistics
- **Total Production Learning Resources**: 36
- **Total Raw Provider Display Labels**: 27
- **Total Normalized Institutional Groups**: 21
- **Synthetics / Test Fixtures in Production**: 0

---

## 4. Verification and Backward Compatibility

Unit tests in `tests/test_reskilling_pathway_engine.py::test_provider_normalization_deterministic` automatically verify that:
1. `len(resources) == 36`
2. Every resource contains `provider_display_name`, `provider_group_id`, and `provider_group_name`.
3. Exactly 21 unique group IDs are instantiated.
4. Exactly 27 unique raw display names are preserved.
5. All legacy callers referencing `r["provider"]` remain functional as `r["provider"]` is mirrored to `r["provider_display_name"]`.
