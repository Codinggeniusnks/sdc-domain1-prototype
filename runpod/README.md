# RunPod Model Training Guide — AI Skills & Demand Predictor

This guide provides instructions to train the **AI Skills & Demand Predictor** model on **RunPod GPU** to generate your official **RunPod Proof of Use (`SDC2026_TeamName_Runpod_POU.pdf`)**.

---

## 1. Quick Overview

- **Task**: Train a neural network to predict the 16 taxonomy skills and classify emerging vs. routine demand from worker bios, job descriptions, and scholarly AI research abstracts.
- **Compute Cost**: Runs on an entry-level GPU (RTX 3070, RTX 4000, or A4000 at **~$0.20/hour**). Total training runtime is **under 2 minutes** (costing **< $0.02** of your US$25 credit).
- **Files**:
  - `runpod/generate_dataset.py`: Creates `data/training_dataset.json` (600 labeled samples).
  - `runpod/train.py`: Trains PyTorch neural net on GPU (`--device cuda`) with BCE loss & evaluation metrics.
  - `runpod/predict.py`: Inference script for predicting skills and demand scores from raw text.
  - `runpod/run_on_runpod.sh`: One-click shell script for RunPod terminals.

---

## 2. Step-by-Step RunPod Execution Instructions

### Step 1: Deploy a Pod on RunPod
1. Log in to your [RunPod Console](https://www.runpod.io/console/pods).
2. Click **Deploy** under **Secure Cloud** or **Community Cloud**.
3. Choose the most economical GPU available:
   - **RTX 3070 / RTX 4000 / RTX A4000** (~$0.20 – $0.25/hr).
4. Select the official template:
   - **PyTorch 2.x** (`runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04` or similar).
5. Click **Continue** → **Deploy On-Demand**.

### Step 2: Open the Terminal & Clone Your Repo
1. Once the Pod shows **Running**, click **Connect** → **Connect to Web Terminal** (or use SSH).
2. In the RunPod terminal, run:
```bash
git clone https://github.com/Codinggeniusnks/sdc-domain1-prototype.git
cd sdc-domain1-prototype
```

### Step 3: Run the Training Script on GPU
Execute the one-click RunPod training script:
```bash
bash runpod/run_on_runpod.sh
```
Or run the Python steps directly:
```bash
# 1. Generate training dataset
python runpod/generate_dataset.py

# 2. Train neural network on CUDA GPU
python runpod/train.py --device cuda --epochs 30

# 3. Test inference
python runpod/predict.py
```

### Step 4: Capture Proof of Use & Stop the Pod
1. **Take a Screenshot**: Take a clear screenshot showing:
   - The RunPod web terminal showing `[RunPod Train] Training via PyTorch on device: cuda (NVIDIA ...)` and `Skill F1` / `Demand Accuracy` output.
   - The RunPod Pod Dashboard showing your active pod name and runtime.
2. **Save Screenshot**: Save this screenshot for `submission/SDC2026_TeamName_Runpod_POU.pdf`.
3. **STOP THE POD**: Immediately click **Stop Pod** (and **Terminate Pod**) in the RunPod console so it stops consuming credits! (Total spend will be under $0.05).

---

## 3. Local Verification (CPU Fallback)

To verify the training pipeline locally on your machine without spending GPU credits:
```bash
python runpod/generate_dataset.py
python runpod/train.py --device cpu
python runpod/predict.py
```
This trains the pipeline on CPU in < 2 seconds and exports `runpod/training_metrics.json`.
