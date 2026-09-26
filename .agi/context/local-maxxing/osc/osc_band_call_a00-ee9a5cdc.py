"""DEPRECATED -- superseded by osc_band_call2_a00-cc7b25cc.py. Kept as prior art
only; it still returns win on a degenerate band and must not be imported anew.
Per-cell win/loss/inside-noise CALL rule over an osc band cells.jsonl.

Band statistic: the stochastic (random) arm's per-cell min-max spread.
Deterministic arms (uniform, key_only) have spread 0.0 and are never the
denominator. Sign-corrected margin: agree higher-is-better, kl lower-is-better.
"""
import json

STOCHASTIC = "random"
SIGN = {"agree": 1.0, "kl": -1.0}          # kl is lower-is-better
MIN_DRAWS = 3                               # gate: stochastic arm only
EPS = 1e-9                                 # float dust must not decide a verdict
CALLS = ("win", "loss", "inside-noise")


def load(records):
    """jsonl lines (or an iterable of dicts) -> list of draw dicts."""
    if isinstance(records, str):
        return [json.loads(x) for x in records.splitlines() if x.strip()]
    return list(records)


def cells(draws):
    """{(model, np, budget): [draw, ...]} from per-(cell, arm, seed) records."""
    out = {}
    for d in draws:
        out.setdefault((d["model"], d["np"], d["budget"]), []).append(d)
    return out


def arm_draws(cell, arm, metric):
    return [d[metric] for d in cell if d["arm"] == arm]


def band(cell, metric):
    """Named band statistic: stochastic arm's min-max spread. None if gated."""
    v = arm_draws(cell, STOCHASTIC, metric)
    return (max(v) - min(v)) if len(v) >= MIN_DRAWS else None


def margin(cell, arm, metric):
    """Sign-corrected treatment-minus-stochastic margin."""
    t, r = arm_draws(cell, arm, metric), arm_draws(cell, STOCHASTIC, metric)
    if not t or not r:
        return None
    return SIGN[metric] * (sum(t) / len(t) - sum(r) / len(r))


def call(m, b):
    if m is None or b is None:
        return "unresolved"
    if m > b + EPS:
        return "win"
    if m < -b - EPS:
        return "loss"
    return "inside-noise"


def judge(records, arm="key_only"):
    """{(model, np, budget, arm, metric): call} for one treatment arm."""
    return {(k[0], k[1], k[2], arm, met): call(margin(c, arm, met), band(c, met))
            for k, c in cells(load(records)).items() for met in SIGN}
