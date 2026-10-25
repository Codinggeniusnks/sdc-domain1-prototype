# Training and serving the three models on RunPod

## What is deployed (Oct 2026)

| Model | Endpoint | Hardware | Status |
|---|---|---|---|
| Skill extraction (`skill-minilm-v1`) | `ppx76tp35fws8g` | CPU serverless, EUR-IS-1 | Connected in `.env` |
| Trend forecasting (`trend-gbq-v1`) | `q3x0b6d8s7048m` | CPU serverless, EUR-IS-1 | Deployed, **not connected** (see below) |
| Explanations: `Qwen/Qwen2.5-7B-Instruct` on vLLM worker `v2.28.0` | `xo1mji8eoavmna` | 24 GB Ada GPU serverless | Connected in `.env` |

All three scale to zero (`--workers-min 0`). Cold starts: skills ~30 s, forecast up to 2 min on a fresh worker, LLM a few minutes the first time.
The network volume `6g35h07oly` (20 GB, EUR-IS-1) holds the dataset, code, Python packages (`pylib/`) and trained models.
Pods mount it at `/workspace` and serverless workers at `/runpod-volume`, so the custom workers need no Docker build. The `Dockerfile`s are only for building standalone images later (build context = repo root).

## Results

Full numbers are in [`metrics/`](metrics/).

**Skill extraction.** Fine-tuned `paraphrase-multilingual-MiniLM-L12-v2` with 94 labels (the [`label_map.json`](label_map.json) taxonomy, mapped to 38 app skills).
Training data: `training_dataset.json` + the gold corpus (16 core labels, other labels masked), plus 2,277 JobStreet postings split into sentences and weakly labelled from the collector's keyword evidence. 700 `held_out_group` postings were kept out of training.

| Test set | Micro-F1 | Macro-F1 |
|---|---|---|
| frozen_test_set (300) | 0.946 | 0.943 |
| real_world_test_set (63) | 0.651 | 0.662 |
| unseen_occupation v1 / v2 (25 each) | 0.638 / 0.811 | 0.609 / 0.821 |
| JobStreet held-out postings (700) | 0.889 | 0.631 |

For comparison, the earlier baseline in `manifests/ablation_results.json` scored 0.932 micro-F1 on the frozen set.
The JobStreet labels are keyword-derived, so that row measures how well the model reproduces the keyword matcher.
The server merges model output with keyword matching (`scripts/ai.js`), so skills the model misses are still found.

**Known gap:** all training text is English, so BM and 中文 CVs are only partly detected (a BM teller sentence found bookkeeping but missed cash handling and customer service).

**Forecasting.** On held-out series it scores MAE 15.9, against 30.1 for the app's damped-linear fallback and 25.1 for "no change".
But it learned that DOSM growth rates mean-revert, and the app's index is structural: cash_handling at −95 is forecast to −23 within 3 months.
It is therefore left disconnected. Retrain it once the app has a few months of its own weekly snapshots (`public/data/snapshots/`).

**LLM.** Not fine-tuned: the dataset has no explanation examples. EN and 中文 output is good. The BM output drifts into Indonesian wording (e.g. "peran", "memiliki"); `SEA-LION` (on the RunPod hub) is worth trying for Malay.

## Re-training

```powershell
runpodctl doctor                                   # API key
runpodctl pod create --name fr-trainer --gpu-id "NVIDIA L4" `
  --image runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404 `
  --network-volume-id 6g35h07oly --data-center-ids EUR-IS-1 `
  --container-disk-in-gb 30 --ports "22/tcp,8888/http" --wait
```

`--ports "22/tcp,..."` is required. Without it the pod never publishes SSH and `--wait` times out while the pod keeps billing.
The pod must be in EUR-IS-1 to mount the volume. If a GPU type is sold out there, try `NVIDIA GeForce RTX 4090` or `NVIDIA RTX 4000 Ada Generation`.

```powershell
# ssh command: runpodctl pod get <POD_ID>   (field ssh.ssh_command)
scp -i $HOME\.runpod\ssh\runpodctl-ssh-key -P <PORT> runpod_training.tar.gz root@<IP>:/workspace/
ssh -i $HOME\.runpod\ssh\runpodctl-ssh-key -p <PORT> root@<IP>
#   cd /workspace && tar xzf runpod_training.tar.gz --no-same-owner && bash runpod/train_on_pod.sh
runpodctl pod delete <POD_ID>                      # the models stay on the volume
```

The run took ~7 min to install packages onto the volume (skipped on later runs), ~10 min to train on an L4, and cost about $0.25.
Serverless workers load the new models on their next cold start.

## Recreating the endpoints

```powershell
$IMG = "runpod/pytorch:1.0.3-cu1281-torch291-ubuntu2404"
runpodctl template create --serverless --name fr-skills --image $IMG --container-disk-in-gb 20 `
  --env '{\"PYTHONPATH\":\"/runpod-volume/pylib\",\"MODEL_DIR\":\"/runpod-volume/models/skills\"}' `
  --docker-start-cmd "python,-u,/runpod-volume/runpod/skills/handler.py"
runpodctl sls create --name fr-skills --template-id <TPL> --compute-type CPU `
  --network-volume-id 6g35h07oly --data-center-ids EUR-IS-1 --workers-min 0 --workers-max 1 --idle-timeout 30
# same for forecast with models/forecast and runpod/forecast/handler.py

# LLM: the hub listing for worker-vllm has no CLI-deployable release, so use the image directly
runpodctl template create --serverless --name fr-llm --image runpod/worker-v1-vllm:v2.28.0 --container-disk-in-gb 40 `
  --env '{\"MODEL_NAME\":\"Qwen/Qwen2.5-7B-Instruct\",\"MAX_MODEL_LEN\":\"8192\",\"GPU_MEMORY_UTILIZATION\":\"0.92\"}'
runpodctl sls create --name fr-llm --template-id <TPL> --gpu-id "NVIDIA GeForce RTX 4090" `
  --model-reference "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct:main" --workers-min 0 --workers-max 1 --idle-timeout 60
```

Test with `runpodctl sls run <ID> --input-file runpod/samples/skills.json --wait 5m`, and check the app with `GET /api/ai/status`.
