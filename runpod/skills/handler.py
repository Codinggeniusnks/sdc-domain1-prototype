"""RunPod Serverless handler: skill extraction from CV text (contract in docs/RUNPOD.md).

The CV is split into sentences; each one is classified and a skill's confidence is its best
sentence score. Those sentences become the evidence shown to the user. Level is a heuristic
(how many sentences support the skill), since the training data has no proficiency labels.
"""
import json, os
from pathlib import Path

import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer

from textsplit import sentences

MODEL_DIR = Path(os.environ.get("MODEL_DIR", "/runpod-volume/models/skills"))
HERE = Path(__file__).resolve().parent
TO_APP = json.loads(next(p for p in (HERE / "label_map.json", HERE.parent / "label_map.json") if p.exists()).read_text(encoding="utf-8"))["to_app"]
cfg = json.loads((MODEL_DIR / "config.json").read_text())
LABELS, TH = cfg["labels"], torch.tensor(cfg["thresholds"])

device = "cuda" if torch.cuda.is_available() else "cpu"
tok = AutoTokenizer.from_pretrained(MODEL_DIR / "encoder")
encoder = AutoModel.from_pretrained(MODEL_DIR / "encoder").to(device).eval()
head = nn.Linear(encoder.config.hidden_size, len(LABELS))
head.load_state_dict(torch.load(MODEL_DIR / "head.pt", map_location="cpu"))
head.to(device).eval()


@torch.no_grad()
def score(sents):
    probs = []
    for i in range(0, len(sents), 64):
        enc = tok(sents[i:i + 64], padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
        h = encoder(**enc).last_hidden_state
        m = enc["attention_mask"].unsqueeze(-1).float()
        probs.append(torch.sigmoid(head((h * m).sum(1) / m.sum(1).clamp(min=1e-6))).cpu())
    return torch.cat(probs)


def handler(job):
    inp = job["input"]
    allowed = {s["id"] for s in inp.get("taxonomy", [])}
    sents = sentences(inp.get("text", ""))
    if not sents:
        return {"skills": [], "model": "skill-minilm-v1"}
    probs = score(sents)
    found = {}
    for k, label in enumerate(LABELS):
        app_id = TO_APP.get(label)
        if not app_id or (allowed and app_id not in allowed):
            continue
        hits = (probs[:, k] >= TH[k]).nonzero().flatten().tolist()
        if not hits:
            continue
        hits.sort(key=lambda i: -probs[i, k].item())
        conf = probs[hits[0], k].item()
        prev = found.get(app_id)
        if prev and prev["confidence"] >= conf:
            continue
        found[app_id] = {
            "id": app_id,
            "level": 1 if len(hits) == 1 else 2 if len(hits) <= 3 else 3,
            "confidence": round(conf, 3),
            "evidence": [sents[i][:160] for i in hits[:3]],
        }
    return {"skills": sorted(found.values(), key=lambda s: -s["confidence"]), "model": "skill-minilm-v1"}


if __name__ == "__main__":
    import runpod
    runpod.serverless.start({"handler": handler})
