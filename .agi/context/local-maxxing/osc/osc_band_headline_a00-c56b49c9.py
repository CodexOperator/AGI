#!/usr/bin/env python3
"""ONE committed zero-model command for the qwen2 band headline
(hypothesis:band-headline-reproducer): the headline came from a hand join, so no command
produced it. Join the byte-matched grid (GRID_RUN, random unseeded) with the seeded random
draws (SEEDS_RUN), drop the grid's n=1 random rows -- they cannot band a call (P3 in
osc_band_call2_a00-cc7b25cc.py band()) -- and run the pre-registered judge() under both
comparators. No model, no GPU, no network.
"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
import paths  # noqa: E402  dir comes from paths.local_maxxing.osc_band_qknorm_dir, not a literal
GRID_RUN, SEEDS_RUN = "a00-a721f95f-qwen2", "a00-2b3ca8c4-582f1e-qwen2-seeds"
STOCHASTIC, COMPARATORS = "random", ("uniform", "random")

def rule():
    """The pre-registered call rule, loaded by file so the dependency is real."""
    s = importlib.util.spec_from_file_location("osc_band_call2", os.path.join(HERE, "osc_band_call2_a00-cc7b25cc.py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def rows(root, run):
    with open(os.path.join(root, run, "cells.jsonl")) as fh:
        return [json.loads(x) for x in fh if x.strip()]

def join(root=None):
    """Grid rows minus their unseeded random rows, plus the seeded random draws."""
    root = root or paths.get_local("osc_band_qknorm_dir")
    return [d for d in rows(root, GRID_RUN) if d["arm"] != STOCHASTIC] + rows(root, SEEDS_RUN)

def headline(root=None):
    """{comparator: {(budget, arm, comparator, metric): (word, reason)}} for key_only."""
    r, recs = rule(), join(root)
    return {c: {k[2:]: v for k, v in r.judge(recs, "key_only", c).items()} for c in COMPARATORS}

def tally(h):
    """{comparator: {word: n}} -- the headline shape, counted."""
    return {c: {w: sum(1 for v in cells.values() if v[0] == w)
                for w in ("win", "loss", "inside-noise", "unresolved")} for c, cells in h.items()}

if __name__ == "__main__":
    h = headline()
    for c in COMPARATORS:
        print(c, json.dumps(tally(h)[c], sort_keys=True))
        for (b, _a, _c, met), (word, reason) in sorted(h[c].items()):
            print("  %-5s %-6s %-12s %s" % (b, met, word, reason))
