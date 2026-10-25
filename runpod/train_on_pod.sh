#!/usr/bin/env bash
# Run inside a RunPod GPU pod after unpacking runpod_training.tar.gz into /workspace.
# /workspace is the network volume. Serverless workers see the same volume at /runpod-volume,
# so the models, code and Python packages left here are what the endpoints load.
set -euo pipefail
cd /workspace
# Packages go on the volume so serverless workers (same base image) can reuse them via PYTHONPATH.
pip install -q --target /workspace/pylib "transformers==4.46.3" "scikit-learn==1.5.2" "joblib==1.4.2" "runpod==1.7.9"
export PYTHONPATH=/workspace/pylib
( cd runpod/skills   && python train.py --data /workspace/dataset --out /workspace/models/skills )
( cd runpod/forecast && python train.py --data /workspace/dataset --out /workspace/models/forecast )
echo; echo "== skills";   python -c "import json;m=json.load(open('/workspace/models/skills/metrics.json'));print(json.dumps({k:{'micro_f1':v['micro_f1'],'macro_f1':v['macro_f1']} for k,v in m['splits'].items()},indent=1))"
echo; echo "== forecast"; cat /workspace/models/forecast/metrics.json
