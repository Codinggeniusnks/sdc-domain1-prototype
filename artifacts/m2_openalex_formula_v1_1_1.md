# M2 OpenAlex Low-Base Research Momentum: Canonical Formula Specification (v1.1.1)

## 1. Canonical Mathematical Formulation

The authoritative, production-frozen formula for OpenAlex publication velocity damping in M2 Trend Intelligence v1.1.1 is:

$$w_{\text{volume}} = \min\left(1.0, \frac{\ln(1 + N_{\text{baseline}})}{\ln(26)}\right)$$

$$R_{\text{adjusted}} = 1.0 + (R_{\text{raw}} - 1.0) \cdot w_{\text{volume}}$$

Where:
- $R_{\text{raw}} = \text{Raw Growth Velocity Ratio}$ from OpenAlex ($N_{\text{recent}} / N_{\text{baseline}}$ with smoothing floor).
- $N_{\text{baseline}} = \text{Total publications indexed between 2020 and 2023 inclusive}$.
- $N_{\text{recent}} = \text{Total publications indexed between 2024 and 2026 inclusive}$.
- $w_{\text{volume}} \in [0.0, 1.0] = \text{Volume reliability shrinkage weight}$.
- $R_{\text{adjusted}} = \text{Low-base adjusted research momentum ratio}$.

---

## 2. Theoretical & Methodological Rationale

### A. Why Baseline Volume ($N_{\text{baseline}}$) is Used Instead of Recent Volume
In scientometrics and velocity ratio modeling, statistical instability arises exclusively from **near-zero denominators**:
- If a concept has $N_{\text{baseline}} = 1$ and grows to $N_{\text{recent}} = 18$, the raw ratio is $18.0\times$. However, this represents an addition of only 17 papers—typically a single conference workshop or special issue.
- If a concept has $N_{\text{baseline}} = 200$ and grows to $N_{\text{recent}} = 600$, the raw ratio is $3.0\times$, but represents 400 net new peer-reviewed studies reflecting immense global consensus.
- Applying shrinkage to $N_{\text{recent}}$ would penalize topics that actually produced substantial recent output. Shrinking based on $N_{\text{baseline}}$ directly measures and neutralizes **small-sample denominator noise**.

### B. Why $\ln(26)$ is the Normalization Anchor
- In academic bibliometrics, a baseline count of **$N = 25$ publications** over a 4-year observation window (averaging $\sim 6$ publications per year) represents the empirical threshold for an established scientific field.
- The offset $+1$ in $\ln(1 + N_{\text{baseline}})$ serves two vital mathematical purposes:
  1. Prevents singularity at zero: When $N_{\text{baseline}} = 0$, $\ln(1 + 0) = \ln(1) = 0 \implies w_{\text{volume}} = 0$.
  2. Ensures that when $N_{\text{baseline}} = 25$, the numerator equals the denominator: $\ln(1 + 25) = \ln(26) \implies w_{\text{volume}} = \frac{\ln(26)}{\ln(26)} = 1.0$.

---

## 3. Asymptotic Behavior Across the Volume Spectrum

| Baseline Count ($N_{\text{baseline}}$) | $w_{\text{volume}} = \frac{\ln(1 + N)}{\ln(26)}$ | Signal Retention % | Excess Growth Shrunk % | Typical Qualitative Stage |
| :---: | :---: | :---: | :---: | :--- |
| **0** | **0.0000** | 0.0% | 100.0% | Zero baseline literature; unproven |
| **1** | **0.2127** | 21.3% | 78.7% | Nascent workshop topic (`prompt_engineering`) |
| **2** | **0.3372** | 33.7% | 66.3% | Emerging pre-standard (`workflow_automation`) |
| **3** | **0.4251** | 42.5% | 57.5% | Early academic adoption (`data_privacy_pdpa`) |
| **5** | **0.5499** | 55.0% | 45.0% | Minimum statistical mass threshold (`sql_data_analysis`) |
| **8** | **0.6743** | 67.4% | 32.6% | Growing discipline (`ai_ethics_governance`) |
| **14** | **0.8312** | 83.1% | 16.9% | Mature foundational capability (`ai_literacy`) |
| **15** | **0.8514** | 85.1% | 14.9% | Established enterprise discipline (`instructional_design`) |
| **$\ge 25$** | **1.0000** | 100.0% | 0.0% | Mature global scientific consensus |

---

## 4. Formal Retirement of Obsolete Draft Formula

During Stage 9D, an uncalibrated draft proposal suggested:
$$R_{\text{damped}} = 1.0 + (R_{\text{raw}} - 1.0) \cdot \frac{N_{\text{recent}}}{N_{\text{recent}} + K} \quad (K = 10)$$

This formula is **FORMALLY REJECTED AND RETIRED** for the following reasons:
1. It conditions on $N_{\text{recent}}$ rather than the noise source $N_{\text{baseline}}$.
2. It failed to prevent small-denominator explosions (e.g., $18 / (18 + 10) = 0.643$, retaining $64.3\%$ of noise for a 1-paper topic).
3. It was never actually implemented in production code.

All documentation, tests, and runtime engines in v1.1.1 strictly adhere to the logarithmic baseline-volume shrinkage formula.
