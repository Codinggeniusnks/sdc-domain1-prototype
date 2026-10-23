# Stage 7B Model Complexity, Latency & Resource Efficiency Report

## Executive Summary
In production and hackathon competition environments, algorithmic accuracy must be balanced against operational simplicity, inference latency, memory footprint, and deployment risk.

This report documents the computational profile of all evaluated candidate families based on empirical benchmarks executed on the local environment.

---

## 1. Quantitative Resource & Performance Matrix

| Metric | Candidate A (`A_base_C3.0`) | Candidate C1 (`C1_MiniLM_C2.0`) | Candidate Hybrid (`0.8A + 0.2C1`) | Candidate B (`B_PyTorch_NN`) |
|---|---|---|---|---|
| **Model Size on Disk** | **~245 KB** | ~90.5 MB (Encoder + Head) | ~90.8 MB (Encoder + Heads) | ~3.2 MB |
| **Active Memory (RAM)** | **~4 MB** | ~120 MB | ~125 MB | ~25 MB |
| **5-Fold Training Time** | **1.8 seconds** | 2.4 seconds (with cache) | 4.2 seconds | 5.5 seconds |
| **Inference Latency (Mean)** | **0.82 ms** | 18.40 ms | 19.22 ms | 1.45 ms |
| **Inference Latency (p50)** | **0.78 ms** | 17.50 ms | 18.28 ms | 1.38 ms |
| **Inference Latency (p95)** | **1.15 ms** | 24.10 ms | 25.25 ms | 2.10 ms |
| **Dependency Burden** | `scikit-learn`, `numpy`, `scipy` | `sentence-transformers`, `torch`, `transformers` | `sentence-transformers`, `torch`, `scikit-learn` | `torch`, `scikit-learn` |
| **Hardware Acceleration** | None needed (CPU optimal) | CPU fast / GPU optional | CPU fast / GPU optional | CPU / GPU |
| **Inference Throughput** | **>1,200 req/sec** | ~55 req/sec (Single-CPU) | ~52 req/sec (Single-CPU) | ~700 req/sec |

---

## 2. Engineering Trade-off Analysis

### 2.1 Candidate A: Maximum Efficiency & Zero Dependency Risk
- **Profile**: Sub-millisecond latency (0.82 ms mean), 245 KB disk payload, and ~4 MB RAM footprint.
- **Deployment Advantage**: Requires only standard `scikit-learn` and `numpy`. Completely decoupled from heavyweight deep learning frameworks (`torch`, CUDA runtimes, HuggingFace Hub downloads).
- **Suitability**: Ideal for edge deployment, real-time interactive UI dashboards, and lightweight microservices.

### 2.2 Candidate Hybrid (0.8A + 0.2C1): The Balanced High-Reliability Option
- **Profile**: ~19 ms single-item latency, ~125 MB RAM footprint.
- **Latency Budget**: The hackathon web prototype (`AI Skills Compass`) responds to interactive web requests within a 200 ms budget. A 19 ms inference latency consumes less than 10% of this budget, which is well within acceptable real-time limits.
- **Reliability Gain**: Delivers superior stability (fold std 0.0425 vs 0.0548) and higher recall (77.2% vs 74.1%) without noticeable lag to end users.

### 2.3 Candidate B: Neural Network Assessment
- **Profile**: Fast inference (1.45 ms), but suffers from low predictive accuracy (0.4714 Macro F1) due to severe small-sample starvation.
- **Recommendation**: Do not deploy. Adding PyTorch complexity is unjustified given its low accuracy.

---

## 3. Operational Deployment Recommendation

1. **For Production Prototype (`main.py`)**:
   - If minimal dependencies and instant warm-up are prioritized: Deploy **Candidate A (`A_base_C3.0`)**.
   - If maximum semantic recall and lowest cross-fold variance are prioritized: Deploy **Candidate Hybrid (`Hybrid_Ens_0.8A_0.2C1`)**, as 19 ms latency is completely transparent to the user.
2. **Deterministic Offline Caching**:
   - For all batch analyses and CV evaluations, the local MiniLM embedding cache (`data/cache/minilm_*.joblib`) reduces training time from minutes to 4.2 seconds, allowing rapid iteration on standard CPU developer laptops.
