# O6 Metric Definitions & Mathematical Specifications

**Engine Version**: 1.0.0  
**Phase**: Stage 14A Feature Construction  
**Framework**: UN 2030 Agenda for Sustainable Development (17 Goals, 169 Targets)  
**Status**: DRAFT IMPLEMENTATION — READY FOR METHODOLOGY REVIEW  

---

## 1. Overview of Descriptive Metrics

O6 implements seven formal descriptive metrics designed to quantify workforce sustainability capability alignment across cohorts without generating fabricated quantitative impact claims:

| Metric Identifier | Metric Name | Mathematical Domain | Primary Purpose |
|---|---|---|---|
| **Metric A** | SDG Alignment Prevalence ($SAP_s$) | $[0.0, 1.0]$ ($\%$) | Proportion of cohort represented in a specific SDG |
| **Metric B** | Target Prevalence Index ($TPI_t$) | $[0.0, 1.0]$ ($\%$) | Proportion of cohort represented in a specific official target |
| **Metric C** | Mapping-Type Evidence Ratio | Direct, Enabling, Contextual Shares ($\sum = 1.0$) | Structural distribution of evidence rigor |
| **Metric D** | SDG Capability Coverage | $[0.0, 1.0]$ ($\%$) | Breadth of distinct canonical skills present vs. domain |
| **Metric E** | Pathway Alignment Coverage | $[0.0, 1.0]$ ($\%$) | Share of planned reskilling steps carrying SDG relevance |
| **Metric F** | Role Alignment Distribution | Counts & Proportions by Role | Occupational composition aligned with SDGs |
| **Metric G** | Scenario Capability View | Multi-Scenario Matrices | Foresight workforce composition under M6 scenarios |

---

## 2. Metric A: SDG Alignment Prevalence ($SAP_s$)

### 2.1 Mathematical Formulation
For a designated eligible cohort $\mathcal{C}$ with size $N_{\text{elig}} = |\mathcal{C}|$ and SDG $s \in \{1, \dots, 17\}$:

$$SAP_s = \frac{\sum_{i \in \mathcal{C}} \mathbb{I}\left( \text{Profile } i \text{ has } \ge 1 \text{ valid mapping to SDG } s \right)}{N_{\text{elig}}}$$

Where:
- $\mathbb{I}(\cdot)$ is the indicator function returning $1$ if true, $0$ otherwise.
- A profile possesses a valid mapping to SDG $s$ if either its active occupational role or at least one of its confirmed skills has a primary or secondary alignment to SDG $s$ in M5 v1.1.0.

### 2.2 Deduplication Invariant
Each individual worker is counted **at most once** per SDG $s$, regardless of whether they hold 1 skill, 5 skills, or an occupational role aligning to that same goal.

### 2.3 Semantic Meaning & Boundary
- **Correct Interpretation**: *"68.75% of workers in the Digital Services division possess at least one technical competency or occupational function aligned with SDG 8 (Decent Work and Economic Growth)."*
- **Prohibited Interpretation**: *"The Digital Services division has achieved 68.75% of SDG 8."*

---

## 3. Metric B: Target Prevalence Index ($TPI_t$)

### 3.1 Mathematical Formulation
For an indexed official UN target $t \in \mathcal{T}_{\text{indexed}}$ and eligible cohort $\mathcal{C}$:

$$TPI_t = \frac{\sum_{i \in \mathcal{C}} \mathbb{I}\left( \text{Profile } i \text{ has } \ge 1 \text{ valid alignment to Target } t \right)}{N_{\text{elig}}}$$

Where $\mathcal{T}_{\text{indexed}}$ represents the 21 domain-relevant official targets indexed in M5 v1.1.0.

### 3.2 Deduplication Invariant
Each individual worker is counted **at most once** per target $t$. Multiple skills mapped to the same target within one profile do not inflate the numerator.

### 3.3 Semantic Meaning & Boundary
- **Correct Interpretation**: *"43.75% of cohort members hold technical capabilities that enable Target 9.5 (enhancing scientific research and industrial technological capabilities)."*
- **Prohibited Interpretation**: *"The company has completed 43.75% of Target 9.5."*

---

## 4. Metric C: Mapping-Type Evidence Ratio (DIRECT / ENABLING / CONTEXTUAL)

### 4.1 Mathematical Formulation
Let $\mathcal{M}_{\mathcal{C}}$ represent the set of all unique profile-target alignments across the cohort:

$$\mathcal{M}_{\mathcal{C}} = \bigcup_{i \in \mathcal{C}} \{ (i, t, \tau) \mid \text{Profile } i \text{ aligns with Target } t \text{ via mapping type } \tau \in \{\text{DIRECT}, \text{ENABLING}, \text{CONTEXTUAL}\} \}$$

Let $K_{\text{direct}} = |\{ m \in \mathcal{M}_{\mathcal{C}} \mid \tau = \text{DIRECT} \}|$, $K_{\text{enabling}} = |\{ m \in \mathcal{M}_{\mathcal{C}} \mid \tau = \text{ENABLING} \}|$, and $K_{\text{contextual}} = |\{ m \in \mathcal{M}_{\mathcal{C}} \mid \tau = \text{CONTEXTUAL} \}|$.  
Total mappings $K_{\text{total}} = K_{\text{direct}} + K_{\text{enabling}} + K_{\text{contextual}}$.

The normalized evidence shares are:

$$\text{direct\_share} = \frac{K_{\text{direct}}}{K_{\text{total}}}, \quad \text{enabling\_share} = \frac{K_{\text{enabling}}}{K_{\text{total}}}, \quad \text{contextual\_share} = \frac{K_{\text{contextual}}}{K_{\text{total}}}$$

$$\text{direct\_share} + \text{enabling\_share} + \text{contextual\_share} = 1.0$$

### 4.2 Semantic Meaning & Boundary
- **Correct Interpretation**: Describes the distribution of qualitative evidence rigor within the workforce's sustainability alignment (e.g. foundational IT enabling tools vs direct environmental reporting).
- **Prohibited Interpretation**: Must **never** be used to claim that DIRECT mappings generate more social value than ENABLING tools.

---

## 5. Metric D: SDG Capability Coverage

### 5.1 Mathematical Formulation
For SDG $s$, let $\mathcal{S}_{\text{canon}}(s)$ denote the set of canonical M5 skills mapped to SDG $s$, and $\mathcal{S}_{\text{cohort}}$ denote the set of all unique skills confirmed or acquired by cohort members:

$$\text{Coverage}(s) = \frac{|\mathcal{S}_{\text{canon}}(s) \cap \mathcal{S}_{\text{cohort}}|}{|\mathcal{S}_{\text{canon}}(s)|}$$

Where $|\mathcal{S}_{\text{canon}}(s)| > 0$. If $|\mathcal{S}_{\text{canon}}(s)| = 0$ (unrelated SDGs), $\text{Coverage}(s) = 0.0$.

### 5.2 Semantic Meaning & Boundary
- **Correct Interpretation**: Measures the breadth of relevant technical competencies present in the talent pool relative to the M5 domain skill catalog.
- **Prohibited Interpretation**: Not a measure of "SDG skill completeness" or "comprehensive goal satisfaction".

---

## 6. Metric E: Pathway Alignment Coverage

### 6.1 Mathematical Formulation
For all planned M4 reskilling pathway skill steps across the cohort $\mathcal{P}_{\text{cohort}} = \bigcup_{i \in \mathcal{C}} \text{PathwaySkills}(i)$:

$$\text{PathwayCoverage} = \frac{\sum_{s \in \mathcal{P}_{\text{cohort}}} \mathbb{I}\left( s \text{ has } \ge 1 \text{ M5 SDG alignment} \right)}{|\mathcal{P}_{\text{cohort}}|}$$

### 6.2 Semantic Meaning & Boundary
- **Correct Interpretation**: Quantifies the extent to which planned training curricula carry an evidence-backed sustainability or decent-work alignment.
- **Prohibited Interpretation**: Not a measure of course quality, instructor effectiveness, or student success.

---

## 7. Metric F: Role Alignment Distribution

### 7.1 Mathematical Formulation
For each 4-digit MASCO occupation $r \in \mathcal{R}$ present in the cohort:

$$\text{Count}(r) = \sum_{i \in \mathcal{C}} \mathbb{I}(\text{ActiveRole}(i) = r), \quad \text{Share}(r) = \frac{\text{Count}(r)}{N_{\text{elig}}}$$

Each role record displays its primary and secondary SDG alignments, along with statutory caveats (e.g., `SECTOR_DEPENDENT_ALIGNMENT` for electrical engineers).

---

## 8. Metric G: Scenario Capability View

### 8.1 Mathematical Formulation
Evaluates cohort composition under the three M6 foresight scenarios:
1. `REFERENCE_2026`: Baseline empirical labor-market trajectory.
2. `MODERATE_COPILOT`: Assistive AI adoption expanding technical productivity.
3. `FAST_AGENTIC`: Accelerated autonomous AI workflows driving structural task displacement and augmentation.

For each scenario $\sigma \in \{\text{REFERENCE\_2026}, \text{MODERATE\_COPILOT}, \text{FAST\_AGENTIC}\}$ and role $r$:
- Retrieves M6 Automation Risk Score $A(r, \sigma)$.
- Retrieves M6 Augmentation Potential Score $U(r, \sigma)$.
- Retrieves M6 Demand Resilience Score $D(r, \sigma)$.

### 8.2 Invariance Invariant
M6 scenario projections provide macroeconomic context on occupational transformation, but **never alter M5 qualitative target definitions or statutory mappings**.
