# O3 Multilingual & Low-Bandwidth Presentation Methodology v1.0.0

## 1. Executive Summary & Design Scope
The Malaysian National AI Workforce Reskilling & Foresight Engine serves a multilingual, diverse workforce across Peninsular and East Malaysia. The **O3 Presentation Layer** provides:
1. **Full Trilingual Parity**: Complete coverage across English (`en`), Bahasa Melayu (`ms`), and Simplified Chinese (`zh-CN`).
2. **Strict Mathematical & Algorithmic Invariance**: Changing the display language affects only human-facing narrative descriptions and labels. Under no circumstances does a language switch mutate numeric fit scores, career rankings, skill gap tiers, required curriculum hours, or Priority Reskilling Indices.
3. **Machine Identifier Immunity**: Standardized classifications—specifically MASCO 2020 codes, ESCO / OpenAlex skill IDs, scenario codes, and cryptographic hashes—remain globally invariant and strictly untranslated.
4. **Low-Bandwidth Edge Optimization**: Designed for rural and low-connectivity regions, reducing transfer payload sizes by $> 75\%$ through vector pruning, narrative truncation, and floating-point compaction.

## 2. Localization Architecture & Catalog Governance
- **Catalog Structure**: JSON-based key-value trees maintained under `locales/`.
  - `locales/en.json`: Canonical reference catalog (142 leaf keys).
  - `locales/ms.json`: Formal Bahasa Melayu terminology aligned with Jabatan Tenaga Kerja (JTK), ILMIA, and KSM.
  - `locales/zh-CN.json`: Standardized Simplified Chinese workforce intelligence terminology.
- **Key Parity Enforcement**: Automated static and runtime parity checks guarantee that the symmetric difference of leaf keys between any two catalogs is $\emptyset$.
- **Fallback Resolution**: If a key is missing in a localized catalog, the engine cascades:
  $$\text{Key} \longrightarrow \text{Active Locale} \longrightarrow \text{Fallback Locale (en)} \longrightarrow \text{Default String}$$

## 3. Mathematical Invariance Formal Guarantee
Let $\mathcal{P}$ represent the complete output state of the platform:
$$\mathcal{P} = \{ \mathcal{M}_{\text{scores}}, \mathcal{M}_{\text{ranks}}, \mathcal{M}_{\text{codes}}, \mathcal{L}_{\text{text}} \}$$
The localization transformation $\mathcal{T}_{\lambda}$ for locale $\lambda \in \{\text{en}, \text{ms}, \text{zh-CN}\}$ satisfies:
$$\mathcal{T}_{\lambda}(\mathcal{M}_{\text{scores}}) = \mathcal{M}_{\text{scores}}$$
$$\mathcal{T}_{\lambda}(\mathcal{M}_{\text{ranks}}) = \mathcal{M}_{\text{ranks}}$$
$$\mathcal{T}_{\lambda}(\mathcal{M}_{\text{codes}}) = \mathcal{M}_{\text{codes}}$$
$$\mathcal{T}_{\lambda}(\mathcal{L}_{\text{text}}) = \text{Catalog}_{\lambda}[\mathcal{L}_{\text{text}}]$$

This mathematical invariance prevents algorithmic bias where a worker speaking one language receives a different career pathway, priority index, or reskilling recommendation than another worker with identical skills.

## 4. Verification & Audit Results
- **Key Parity**: 142 / 142 keys (100.0% parity).
- **Resolution Speed**: $> 2,900,000$ operations per second.
- **Invariance Checks**: 0 violations observed across M3, M4, and O1 synthetic benchmarks.
