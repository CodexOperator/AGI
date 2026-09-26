#!/usr/bin/env python3
"""TWO calls over the same rows, kept separate. Pure python: no model, no torch.

The first kid's band() asked ONE question (min<=key_only<=max, the RANGE call) and reported the
answer as if it were the declared claim (abs(key_only-uniform)<=half_range, the MARGIN call).
They are different denominators and they disagree. Both are returned here, per (budget, metric),
never merged into one `inside?` column. ROW CONTRACT: the config cell
values.local_maxxing.osc_band_row_contract -- read at runtime, never re-declared here -- is what
p3 cites: the fields, n>=3 DISTINCT seeds for a stochastic group, deterministic arms as one row
with seed 0, n 1, arm_is_stochastic false.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing")]
import paths
KID = "a00-ec09e83b-8786a9"
SEEDS_RUN, DET_RUN = "a00-2b3ca8c4-582f1e-qwen2-seeds", "a00-a721f95f-qwen2"
OUT = os.path.join(paths.get_local("osc_band_qknorm_dir"), KID + "-qwen2-calls")
MIN_SEEDS, METRICS = 3, ("agree", "kl")  # margin signed so positive = key_only beats uniform
BEATS = {"agree": "above-peer", "kl": "below-peer"}  # peer side on which key_only WINS

def contract():
    return json.load(open(paths.config_path()))["values"]["local_maxxing"]["osc_band_row_contract"]

def rows(run):
    return [json.loads(l) for l in open(os.path.join(paths.get_local("osc_band_qknorm_dir"), run, "cells.jsonl"))]

def groups(rs):
    g = {}
    for r in rs:
        g.setdefault((r["budget"], r["arm"]), []).append(r)
    return g

def n_distinct(g):  # n counts DISTINCT seeds, never rows (falsifier 1)
    return len({r["seed"] for r in g if r["arm_is_stochastic"]})

def draws(g, bud):  # the random group at a budget, or a REFUSAL: <3 seeds is no call (falsifier 2)
    d = g[(bud, "random")]
    if n_distinct(d) < MIN_SEEDS:
        raise ValueError("refuse to call: %s/random has %d distinct seeds" % (bud, n_distinct(d)))
    return d

KINDS = ("margin", "range")  # the only two denominators that exist; anything else is a typo, not a kind

def call(g, kind):
    """(a) margin: abs(key_only - uniform) <= half_range(random). (b) range: min <= key_only <= max.

    Fail-closed in its OWN bytes, not only through the door (osc_band_gate_a00-be5449f2.py): an
    unnamed kind, or a budget that carries no control arm, is REFUSED. The old `else:` answered
    any typo with the RANGE call and a missing random group with {}, which reads downstream as
    "nothing to decide here" -- the exact slip this reader exists to end.
    """
    if kind not in KINDS:
        raise ValueError("refuse to call: %r is not one of %s" % (kind, list(KINDS)))
    for bud in sorted({b for (b, _arm) in g}):
        for arm in ("random", "uniform", "key_only"):
            if (bud, arm) not in g:
                raise ValueError("refuse to call: %s has no %s arm (missing control)" % (bud, arm))
    out = {}
    for (bud, arm) in sorted(g):
        if arm != "random":
            continue
        rnd = draws(g, bud)
        for m in METRICS:
            d = [r[m] for r in rnd]; k = g[(bud, "key_only")][0][m]; half = (max(d) - min(d)) / 2
            if kind == "margin":
                mg = -k + g[(bud, "uniform")][0][m] if m == "kl" else k - g[(bud, "uniform")][0][m]
                out[(bud, m)] = {"call": "margin", "margin": round(mg, 6), "half_range": round(half, 6),
                                 "verdict": "win" if mg > half else "loss" if mg < -half else "inside-noise"}
            else:
                out[(bud, m)] = {"call": "range", "key_only": k, "min": min(d), "max": max(d),
                                 "verdict": "inside-noise" if min(d) <= k <= max(d) else ("above-peer" if k > max(d) else "below-peer")}
    return out

def merged():  # the twelve measured random rows PLUS the deterministic arms as ROWS, per the contract
    c = contract()
    out = [dict(r, cell="%s:random@%s@s%d" % (r["model"], r["budget"], r["seed"])) for r in rows(SEEDS_RUN)]
    out += [dict(r, seed=0, n=1, arm_is_stochastic=False) for r in rows(DET_RUN) if r["arm"] in ("uniform", "key_only")]
    for r in out:
        assert not [f for f in c["fields"] if f not in r], "row contract violated on %s" % r["cell"]
    return out

def run():
    g = groups(merged()); m, r = call(g, "margin"), call(g, "range")
    key = lambda c: {"%s|%s" % k: v for k, v in c.items()}
    inside = lambda c, s: {k for k, v in c.items() if v["verdict"] == s}
    sk = lambda s: sorted("%s|%s" % k for k in s)
    doc = {"meta": {"k_id": KID, "runs": [SEEDS_RUN, DET_RUN], "contract_fields": contract()["fields"]},
           "margin_call": key(m), "range_call": key(r),
           "summary": {"margin_inside_budgets": sorted({k[0] for k in inside(m, "inside-noise")}),
                       "range_inside_cells": sk(inside(r, "inside-noise")),
                       "disagree": sk(inside(m, "inside-noise") ^ inside(r, "inside-noise")),
                       "key_only_beats_every_draw": sk({k for k, v in r.items() if v["verdict"] == BEATS[k[1]]})}}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "cells.jsonl"), "w") as fh:
        for x in merged():
            fh.write(json.dumps(x) + "\n")
    json.dump(doc, open(os.path.join(OUT, "calls.json"), "w"), indent=1)
    print(json.dumps(doc["summary"], indent=1))

if __name__ == "__main__":
    run()
