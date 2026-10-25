"""Shared by train.py and handler.py: turn a short index history into model features."""
from datetime import date

import numpy as np

HORIZONS = (3, 6, 9, 12)
FEATURES = ["last", "slope", "prev_delta", "mean", "n_points", "span_months", "horizon"]


def months(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days / 30.44


def features(history, horizon):
    """history: [{"asOf": "YYYY-MM-DD", "index": float}, ...] sorted by date, len >= 1."""
    xs = np.array([months(history[0]["asOf"], h["asOf"]) for h in history])
    ys = np.array([float(h["index"]) for h in history])
    recent = xs >= xs[-1] - 12  # slope over the last year of points only
    slope = float(np.polyfit(xs[recent], ys[recent], 1)[0]) if recent.sum() >= 2 and np.ptp(xs[recent]) > 0 else 0.0
    prev = float(ys[-1] - ys[-2]) if len(ys) >= 2 else 0.0
    return [ys[-1], slope, prev, ys.mean(), min(len(ys), 24), float(xs[-1]), horizon]


def damped_linear(history, horizon):
    """Same baseline as linearForecast() in public/js/ai-shared.js, used for the backtest."""
    f = features(history, horizon)
    damp = (1 - 0.85 ** horizon) / 0.15
    return float(np.clip(f[0] + f[1] * damp, -100, 100))
