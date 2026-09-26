"""TOTAL per-cell win/loss/inside-noise call rule over an osc band cells.jsonl.
Amends osc_band_call_a00-ee9a5cdc.py at its three holes (parent probes P3/P4/P6):
P3 gate on DISTINCT draw indices not rows; P4 a zero-width band is refused with
its reason; P6 the comparator is a parameter. The band is ALWAYS the stochastic
arm's min-max spread -- a deterministic comparator gives a mean, never a band.
"""
import json
STOCHASTIC = "random"                 # the only denominator, whatever the comparator
SIGN = {"agree": 1.0, "kl": -1.0}     # agree higher-is-better, kl lower-is-better
MIN_SEEDS, EPS = 3, 1e-9              # DISTINCT draw indices; float dust decides nothing
def load(records):
    return [json.loads(x) for x in records.splitlines() if x.strip()] if isinstance(records, str) else list(records)
def cells(draws):
    out = {}
    for d in draws: out.setdefault((d["model"], d["np"], d["budget"]), []).append(d)
    return out  # {(model, np, budget): [draw, ...]}
def arm_draws(cell, arm, metric):
    return [d[metric] for d in cell if d["arm"] == arm]
def n_seeds(cell, arm):
    return len({d["seed"] for d in cell if d["arm"] == arm and "seed" in d})  # distinct, EXPLICIT
def band(cell, metric):  # (spread, reason) -- (None, why) when the band is unearned
    v = arm_draws(cell, STOCHASTIC, metric)
    seeded = [d for d in cell if d["arm"] == STOCHASTIC and "seed" in d]
    n = len({d["seed"] for d in seeded})  # distinct, EXPLICIT seeds only
    if not v: return None, "no %s draws" % STOCHASTIC
    if len(seeded) != len(v): return None, "%d of %d %s draws carry no seed: n=1 rows cannot band a call" % (len(v) - len(seeded), len(v), STOCHASTIC)
    if n < MIN_SEEDS: return None, "fewer than %d distinct %s seeds" % (MIN_SEEDS, STOCHASTIC)
    b = max(v) - min(v)
    if b <= EPS: return None, "degenerate band: %s arm never varied" % STOCHASTIC
    return b, "random min-max over %d distinct seeds" % n
def margin(cell, arm, comparator, metric):
    t, c = arm_draws(cell, arm, metric), arm_draws(cell, comparator, metric)  # sign-corrected
    return None if not t or not c else SIGN[metric] * (sum(t) / len(t) - sum(c) / len(c))
def call(m, b, reason):
    """(word, reason); strict on both sides, so equality is inside-noise."""
    if m is None: return "unresolved", "arm or comparator absent"
    if b is None: return "unresolved", reason
    word = "win" if m > b + EPS else "loss" if m < -b - EPS else "inside-noise"
    return word, "margin %+.4g vs band %+.4g" % (m, b)
def judge(records, arm="key_only", comparator=STOCHASTIC):
    """{(model, np, budget, arm, comparator, metric): (word, reason)}."""
    return {(k + (arm, comparator, met)): call(margin(c, arm, comparator, met), *band(c, met))
            for k, c in cells(load(records)).items() for met in SIGN}  # band ignores comparator
