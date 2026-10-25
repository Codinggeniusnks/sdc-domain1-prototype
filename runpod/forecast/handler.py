"""RunPod Serverless handler: skill-trend forecasting (contract in docs/RUNPOD.md)."""
import os
from datetime import date, timedelta
from pathlib import Path

import joblib
import numpy as np

from features import features

MODEL_DIR = Path(os.environ.get("MODEL_DIR", "/runpod-volume/models/forecast"))
bundle = joblib.load(MODEL_DIR / "forecaster.joblib")
Q = bundle["quantiles"]


def handler(job):
    inp = job["input"]
    horizon = int(inp.get("horizonMonths", 12))
    out = {}
    for skill, hist in (inp.get("series") or {}).items():
        hist = sorted((h for h in hist if "asOf" in h and "index" in h), key=lambda h: h["asOf"])
        if not hist:
            continue
        last, points = float(hist[-1]["index"]), []
        for m in range(3, horizon + 1, 3):
            x = np.array([features(hist, min(m, 12))])
            mid, lo, hi = (float(np.clip(last + Q[q].predict(x)[0], -100, 100)) for q in ("0.5", "0.1", "0.9"))
            if m > 12:  # beyond the trained horizon: hold the 12-month view and widen the band
                w = (m - 12) / 12 * 10; lo, hi = max(-100, lo - w), min(100, hi + w)
            as_of = (date.fromisoformat(hist[-1]["asOf"]) + timedelta(days=round(m * 30.44))).isoformat()
            points.append({"month": m, "asOf": as_of, "index": round(mid, 1), "low": round(min(lo, mid), 1), "high": round(max(hi, mid), 1)})
        out[skill] = {"points": points}
    return {"model": "trend-gbq-v1", "forecasts": out}


if __name__ == "__main__":
    import runpod
    runpod.serverless.start({"handler": handler})
