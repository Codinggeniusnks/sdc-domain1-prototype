#!/usr/bin/env bash
# One-click execution script for RunPod GPU Terminal
set -e

echo "=== 1. Checking GPU Environment ==="
nvidia-smi

echo "=== 2. Generating Synthetic Training Dataset ==="
python runpod/generate_dataset.py

echo "=== 3. Training AI Skills & Demand Predictor on CUDA GPU ==="
python runpod/train.py --device cuda --epochs 30

echo "=== 4. Running Sample Inference Verification ==="
python runpod/predict.py

echo "=== Training Finished Successfully! ==="
echo "You can now capture your screenshot for SDC2026_TeamName_Runpod_POU.pdf"
echo "Remember to STOP and TERMINATE your RunPod pod to preserve your credits!"
