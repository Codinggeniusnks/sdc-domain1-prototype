"""Train the skill-trend forecaster.

usage: python train.py --data /workspace/dataset --out /workspace/models/forecast

The app sends a short history of trend indices (-100..+100) per skill. Real labour-market series
are turned into the same kind of index (year-on-year growth squashed with tanh), then quantile
gradient-boosting models learn the change in index over 3/6/9/12 months (10th, 50th, 90th pct).
Series are split by group so the backtest is on series the model never saw, and it is compared
with the damped-linear fallback the app already uses.
"""
import argparse, json
from collections import defaultdict
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

from features import FEATURES, HORIZONS, damped_linear, features, months

QUANTILES = (0.1, 0.5, 0.9)


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def raw_series(data):
    """Yield (name, [(iso_date, value), ...]) for every numeric column of every dated table."""
    for p in sorted((data / "trends" / "raw" / "opendosm").glob("*_snapshot.json")):
        rows = load(p).get("data", [])
        groups = defaultdict(list)
        for r in rows:
            if "date" not in r:
                continue
            key = tuple(sorted((k, v) for k, v in r.items() if isinstance(v, str) and k != "date"))
            groups[key].append(r)
        for key, rs in groups.items():
            rs.sort(key=lambda r: r["date"])
            for col in {k for r in rs for k, v in r.items() if isinstance(v, (int, float))}:
                pts = [(r["date"], float(r[col])) for r in rs if isinstance(r.get(col), (int, float))]
                yield f"{p.stem}:{dict(key)}:{col}", pts
    oa = load(data / "trends" / "raw" / "openalex" / "openalex_temporal_momentum.json")
    for skill, s in oa["skill_research_momentum"].items():
        yield f"openalex:{skill}", [(f"{y}-07-01", float(c)) for y, c in sorted(s["publications_by_year"].items()) if int(y) < 2026]


def to_index(pts):
    """Year-on-year growth -> index in -100..100 (25% growth ~ +76)."""
    out = []
    for i, (d, v) in enumerate(pts):
        base = [pv for pd, pv in pts[:i] if 11 <= months(pd, d) <= 13]
        if base and abs(base[-1]) > 1e-9:
            g = v / base[-1] - 1
            out.append({"asOf": d, "index": float(100 * np.tanh(g / 0.25))})
    return out


def windows(idx):
    by_date = {h["asOf"]: h["index"] for h in idx}
    rows = []
    for i in range(1, len(idx)):
        hist = idx[max(0, i - 23):i + 1]
        for j in range(i + 1, len(idx)):
            h = round(months(idx[i]["asOf"], idx[j]["asOf"]))
            if h in HORIZONS:
                rows.append((hist, h, by_date[idx[j]["asOf"]]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = Path(a.data)

    series = [(n, to_index(p)) for n, p in raw_series(data)]
    series = [(n, s) for n, s in series if len(s) >= 3 and np.ptp([h["index"] for h in s]) > 0]
    rng = np.random.default_rng(7)
    test_names = {n for n, _ in series if rng.random() < 0.2}
    sets = {"train": [], "test": []}
    for n, s in series:
        sets["test" if n in test_names else "train"] += windows(s)
    print(f"{len(series)} series, {len(sets['train'])} train windows, {len(sets['test'])} test windows")

    def xy(rows):
        X = np.array([features(h, hz) for h, hz, _ in rows]); y = np.array([t - h[-1]["index"] for h, _, t in rows])
        return X, y

    Xtr, ytr = xy(sets["train"]); Xte, yte = xy(sets["test"])
    models = {}
    for q in QUANTILES:
        m = GradientBoostingRegressor(loss="quantile", alpha=q, n_estimators=300, max_depth=3, learning_rate=0.05, subsample=0.8, random_state=0)
        models[q] = m.fit(Xtr, ytr)

    last = Xte[:, 0]
    pred = np.clip(last + models[0.5].predict(Xte), -100, 100)
    lo = last + models[0.1].predict(Xte); hi = last + models[0.9].predict(Xte)
    truth = last + yte
    base = np.array([damped_linear(h, hz) for h, hz, _ in sets["test"]])
    metrics = {
        "series": len(series), "train_windows": len(Xtr), "test_windows": len(Xte),
        "mae_model": round(float(np.abs(pred - truth).mean()), 2),
        "mae_damped_linear_baseline": round(float(np.abs(base - truth).mean()), 2),
        "mae_naive_last_value": round(float(np.abs(last - truth).mean()), 2),
        "interval_80_coverage": round(float(((truth >= lo) & (truth <= hi)).mean()), 3),
        "by_horizon_mae": {int(h): round(float(np.abs(pred - truth)[Xte[:, -1] == h].mean()), 2) for h in HORIZONS if (Xte[:, -1] == h).any()},
    }
    print(json.dumps(metrics, indent=2))

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    # refit on everything for the deployed model
    Xall, yall = xy(sets["train"] + sets["test"])
    for q in QUANTILES:
        models[q].fit(Xall, yall)
    joblib.dump({"features": FEATURES, "quantiles": {str(q): m for q, m in models.items()}}, out / "forecaster.joblib")
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("saved to", out)


if __name__ == "__main__":
    main()
