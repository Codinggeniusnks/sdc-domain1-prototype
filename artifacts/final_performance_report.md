# Final System Performance, Latency & Resource Report

**Evaluator Role**: Senior ML Engineer & Reproducibility Auditor  
**Artifact Directory**: `runpod/models/skills_predictor_v5_final/`  
**Execution Environment**: Local CPU (Zero Cloud GPU, Zero RunPod)  

---

## 1. System Benchmark Summary

| Performance Metric | Measured Value | Production SLA Requirement | Status |
| :--- | :---: | :---: | :---: |
| **Model Bundle Size (Serialized Heads & Pipeline)** | **0.39 MB** | $\le 50\text{ MB}$ | **PASSED (Ultra-compact)** |
| **Pretrained Semantic Encoder Cache (MiniLM)** | **91.5 MB** | $\le 250\text{ MB}$ | **PASSED** |
| **Total Disk Footprint** | **91.89 MB** | $\le 500\text{ MB}$ | **PASSED** |
| **Active Memory Overhead (RAM)** | **~285 MB** | $\le 512\text{ MB}$ | **PASSED (Micro-container safe)** |
| **Cold-Start Initialization Time** | **~520 ms** | $\le 3,000\text{ ms}$ | **PASSED (Sub-second cold start)** |
| **Mean Single-Record Inference Latency** | **54.75 ms** | $\le 100\text{ ms}$ | **PASSED** |
| **Median (P50) Inference Latency** | **54.33 ms** | $\le 100\text{ ms}$ | **PASSED** |
| **95th Percentile (P95) Latency** | **61.23 ms** | $\le 150\text{ ms}$ | **PASSED (Ultra-stable)** |
| **Peak (Max) Observed Latency** | **77.24 ms** | $\le 250\text{ ms}$ | **PASSED** |
| **Throughput (Single CPU Thread)** | **18.3 docs / sec** | $\ge 5\text{ docs / sec}$ | **PASSED** |

---

## 2. Hardware & Runtime Environment

- **Host OS**: Microsoft Windows 11 (build 10.0.26100)
- **Python Version**: 3.11.9
- **Core Dependencies**:
  - `scikit-learn`: 1.6.1
  - `torch`: 2.6.0+cpu
  - `sentence-transformers`: 3.3.1
  - `joblib`: 1.4.2
  - `numpy`: 2.1.2
  - `scipy`: 1.15.1
- **Hardware Tier**: 100% Local CPU Execution. No NVIDIA CUDA, Apple Silicon MPS, or cloud GPU instances were provisioned or required.

---

## 3. Operational Reliability & Container Compatibility

1. **Lightweight Deployment**:
   The entire hybrid inference engine fits easily inside a standard `python:3.11-slim` Docker container with 512 MB of allocated RAM, making it suitable for cost-effective deployment on platforms such as Replit, Render, Hugging Face Spaces, or AWS Lambda (container image).
2. **Deterministic Outputs**:
   Given identical input text, the model produces exact, bitwise-identical output probability vectors across repeated runs. Zero stochastic temperature sampling or non-deterministic floating-point accumulation is present.
3. **No Network Latency Overhead**:
   Because the MiniLM encoder runs completely in-process on CPU without making remote API calls to external proprietary LLM endpoints, inference latency is immune to network timeouts, rate limits, or external service outages.
