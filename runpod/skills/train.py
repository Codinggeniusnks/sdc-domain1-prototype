"""Fine-tune a multilingual MiniLM encoder as a 94-label skill classifier.

usage: python train.py --data /workspace/dataset --out /workspace/models/skills [--epochs 6]

Two sources, one label space (runpod/label_map.json):
  - core rows: training_dataset.json + processed/gold_corpus_v5_candidate.json. They only label
    the first 16 skills, so the other 78 are masked out of the loss (unknown, not "absent").
    Any text that appears in a test split is dropped.
  - jobstreet_postings_balanced.json: each posting is split into sentences and a sentence gets a
    skill when it contains one of that posting's matched evidence terms (weak, keyword-derived
    labels). Postings with held_out_group=true are kept out and scored at posting level.
10% of training rows tune one threshold per label. Writes metrics.json next to the model.
"""
import argparse, json, random, re
from pathlib import Path

import numpy as np
import torch
from torch import nn
from transformers import AutoModel, AutoTokenizer

from textsplit import sentences, term_regex

HERE = Path(__file__).resolve().parent
LMAP = json.loads(next(p for p in (HERE / "label_map.json", HERE.parent / "label_map.json") if p.exists()).read_text(encoding="utf-8"))
LABELS, CORE = LMAP["labels"], LMAP["core"]
IDX = {l: i for i, l in enumerate(LABELS)}
CORE_MASK = np.array([1.0] * CORE + [0.0] * (len(LABELS) - CORE), dtype=np.float32)
FULL_MASK = np.ones(len(LABELS), dtype=np.float32)


def norm(t):
    return re.sub(r"\s+", " ", t.lower()).strip()


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def vec(skills):
    y = np.zeros(len(LABELS), dtype=np.float32)
    for s in skills:
        if s in IDX:
            y[IDX[s]] = 1.0
    return y


def posting_sentences(post):
    """[(sentence, label vector)] using the posting's own evidence terms."""
    pats = {s: [term_regex(t) for t in terms] for s, terms in (post.get("skill_evidence") or {}).items() if s in IDX}
    rows = []
    for s in sentences(f"{post.get('title') or ''}.\n{post['text']}"):
        rows.append((s, vec([sid for sid, ps in pats.items() if any(p.search(s) for p in ps)])))
    return rows


class SkillClassifier(nn.Module):
    def __init__(self, base):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(base)
        self.head = nn.Linear(self.encoder.config.hidden_size, len(LABELS))

    def forward(self, input_ids, attention_mask):
        h = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        m = attention_mask.unsqueeze(-1).float()
        return self.head((h * m).sum(1) / m.sum(1).clamp(min=1e-6))


@torch.no_grad()
def predict(model, tok, texts, device, bs=128):
    model.eval()
    out = []
    for i in range(0, len(texts), bs):
        enc = tok(texts[i:i + bs], padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
        out.append(torch.sigmoid(model(enc["input_ids"], enc["attention_mask"])).cpu().numpy())
    return np.concatenate(out) if out else np.zeros((0, len(LABELS)))


def f1s(y, p, mask=None):
    """Micro and macro F1 over labels with mask=1 (macro skips labels with no positives and no predictions)."""
    mask = np.ones(y.shape[1]) if mask is None else mask
    tp = (y * p).sum(0); fp = ((1 - y) * p).sum(0); fn = (y * (1 - p)).sum(0)
    keep = (mask > 0) & ((tp + fp + fn) > 0)
    per = np.where(keep, 2 * tp / np.maximum(2 * tp + fp + fn, 1e-9), np.nan)
    micro = 2 * tp[keep].sum() / max(2 * tp[keep].sum() + fp[keep].sum() + fn[keep].sum(), 1e-9)
    return float(micro), float(np.nanmean(per)) if keep.any() else 0.0, per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    ap.add_argument("--epochs", type=int, default=6)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=4e-5)
    ap.add_argument("--neg-ratio", type=float, default=1.0, help="unlabelled posting sentences kept per labelled one")
    ap.add_argument("--limit", type=int, default=0, help="smoke test: cap rows per source")
    ap.add_argument("--seed", type=int, default=13)
    a = ap.parse_args()

    random.seed(a.seed); np.random.seed(a.seed); torch.manual_seed(a.seed)
    data = Path(a.data)
    tests = {p.stem: load(p) for p in sorted((data / "splits").glob("*.json")) if "manifest" not in p.stem}
    held = {norm(r["text"]) for recs in tests.values() for r in recs}

    # core rows: (text, y, mask, weight)
    seen, core = set(), []
    for rec in load(data / "training_dataset.json") + load(data / "processed" / "gold_corpus_v5_candidate.json"):
        k = norm(rec["text"])
        if k not in held and k not in seen:
            seen.add(k); core.append((rec["text"], vec(rec["skills"]), CORE_MASK, float(rec.get("sample_weight", 1.0))))

    # jobstreet sentences
    posts = load(data / "jobstreet_postings_balanced.json")
    js_test = [p for p in posts if p.get("held_out_group")]
    pos, neg = [], []
    for p in (p for p in posts if not p.get("held_out_group")):
        for s, y in posting_sentences(p):
            if norm(s) in seen:
                continue
            seen.add(norm(s))
            (pos if y.any() else neg).append((s, y, FULL_MASK, 1.0))
    random.shuffle(neg)
    js = pos + neg[:int(len(pos) * a.neg_ratio)]
    if a.limit:
        random.shuffle(core); random.shuffle(js); core, js, js_test = core[:a.limit], js[:a.limit], js_test[:max(20, a.limit // 10)]

    train = core + js
    random.shuffle(train)
    n_val = max(1, len(train) // 10)
    val, train = train[:n_val], train[n_val:]
    print(f"core rows {len(core)}  jobstreet sentences {len(js)} ({len(pos)} labelled)  -> train {len(train)}  val {len(val)}")
    print(f"jobstreet held-out postings {len(js_test)}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tok = AutoTokenizer.from_pretrained(a.base)
    model = SkillClassifier(a.base).to(device)
    opt = torch.optim.AdamW([
        {"params": model.encoder.parameters(), "lr": a.lr},
        {"params": model.head.parameters(), "lr": 1e-3},
    ], weight_decay=0.01)
    X = [r[0] for r in train]
    Y = torch.tensor(np.stack([r[1] for r in train])); M = torch.tensor(np.stack([r[2] for r in train]))
    W = torch.tensor([r[3] for r in train])
    steps = a.epochs * ((len(X) + a.batch - 1) // a.batch)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=[a.lr, 1e-3], total_steps=steps, pct_start=0.1)
    loss_fn = nn.BCEWithLogitsLoss(reduction="none")
    use_amp = device == "cuda"
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)

    for ep in range(a.epochs):
        model.train()
        order = np.random.permutation(len(X)); total = 0.0
        for i in range(0, len(X), a.batch):
            idx = order[i:i + a.batch]
            enc = tok([X[j] for j in idx], padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
            with torch.autocast(device_type=device, dtype=torch.float16, enabled=use_amp):
                logits = model(enc["input_ids"], enc["attention_mask"])
            m = M[idx].to(device)
            per_row = (loss_fn(logits.float(), Y[idx].to(device)) * m).sum(1) / m.sum(1)
            loss = (per_row * W[idx].to(device)).mean()
            opt.zero_grad(); scaler.scale(loss).backward(); scaler.step(opt); scaler.update(); sched.step()
            total += loss.item() * len(idx)
        print(f"epoch {ep + 1}/{a.epochs}  loss {total / len(X):.4f}")

    # One threshold per label on the validation rows where that label is known.
    yv = np.stack([r[1] for r in val]); mv = np.stack([r[2] for r in val])
    pv = predict(model, tok, [r[0] for r in val], device)
    grid = np.arange(0.2, 0.81, 0.05)
    thresholds = []
    for k in range(len(LABELS)):
        rows = mv[:, k] > 0
        y, p = yv[rows, k:k + 1], pv[rows, k:k + 1]
        best = max(grid, key=lambda t: f1s(y, (p >= t).astype(float))[0]) if y.any() else 0.5
        thresholds.append(round(float(best), 2))
    th = np.array(thresholds)

    metrics = {"base": a.base, "train_rows": len(train), "val_rows": len(val), "thresholds": dict(zip(LABELS, thresholds)), "splits": {}}

    def report(name, y, p, mask):
        mi, ma, per = f1s(y, p, mask)
        metrics["splits"][name] = {"rows": len(y), "micro_f1": round(mi, 4), "macro_f1": round(ma, 4),
                                   "per_label_f1": {l: round(float(v), 3) for l, v in zip(LABELS, per) if not np.isnan(v)}}
        print(f"{name:34s} rows {len(y):5d}  micro-F1 {mi:.3f}  macro-F1 {ma:.3f}")

    report("validation (sentences)", yv, (pv >= th).astype(float) * mv, FULL_MASK)
    for name, recs in tests.items():  # core test splits: the 16 core labels only
        y = np.stack([vec(r["skills"]) for r in recs])
        report(name, y, (predict(model, tok, [r["text"] for r in recs], device) >= th).astype(float), CORE_MASK)
    # held-out postings: a skill is predicted if any sentence passes its threshold (as in handler.py)
    yd, pd = [], []
    for post in js_test:
        sents = [s for s, _ in posting_sentences(post)]
        probs = predict(model, tok, sents, device) if sents else np.zeros((1, len(LABELS)))
        yd.append(vec(post.get("skills", []))); pd.append((probs >= th).any(0).astype(float))
    if js_test:
        report("jobstreet_held_out (postings)", np.stack(yd), np.stack(pd), FULL_MASK)

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    model.encoder.save_pretrained(out / "encoder"); tok.save_pretrained(out / "encoder")
    torch.save(model.head.state_dict(), out / "head.pt")
    (out / "config.json").write_text(json.dumps({"labels": LABELS, "thresholds": thresholds, "base": a.base}, indent=2))
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("saved to", out)


if __name__ == "__main__":
    main()
