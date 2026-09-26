#!/usr/bin/env python3
"""ONE cut np64 qwen3 cell, end to end, on this box's real ML stack.

The stack EXISTS: numpy 2.5.3 / transformers 5.17.0 / torch 2.14.0 import fine from
/data/ml/.venv/bin/python with PYTHONPATH=/data/ml/scratch/osc03/pylib. Two kids read
`import numpy` failing from $PATH's python3 as "no ML stack on this box"; the
interpreter is the recipe, and the recipe is ENV, not code.

Nothing measured here is re-implemented: the reducer + band gate are
osc_band_reduce_a00-4c09956d's, the three-way call is osc_band_call2_a00-cc7b25cc's,
the GRID and check_table are a721f95f's. This file pins the output prefix, repairs
ONE call convention, and says the cut out loud.

Run (foreground, under the box slot; 299s, 10 rows):
  PYTHONPATH=/data/ml/scratch/osc03/pylib /data/ml/.venv/bin/python \\
    .agi/context/local-maxxing/osc/osc_band_np64_one_a00-385bc2f0.py qwen3 \\
    --budgets 4.125 --prompts 2 --seeds 7,21,99
"""
import argparse, importlib.util, json, os, sys
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
_s = importlib.util.spec_from_file_location("red", os.path.join(HERE, "osc_band_reduce_a00-4c09956d.py"))
red = importlib.util.module_from_spec(_s); _s.loader.exec_module(red)
red.OUT = "a00-385bc2f0-"  # the reducer is another node's: borrow it, never overwrite its rows
_deps = None  # LAZY: p3 imports this on a box with no torch, so nothing heavy runs at import
_raw_deps = red.deps

def _patched_deps():
    """The ONE repair: arm() -> (layers, widths), so the reducer's `forward(m, p, *al)`
    splat lands on forward's real signature. a721f95f calls forward(m, ids, a, widths);
    the splat of 30 layer tensors into a 5-arg forward was `takes from 2 to 5 positional
    arguments but 30 were given`, 53s of weight load in. arm() ignores widths, so this
    is a harness fix -- the call RULE is untouched."""
    global _deps
    if _deps is None:
        _deps = _raw_deps()
    fixed = _deps[4].fixed
    if not getattr(fixed, "_arms_are_paired", False):
        inner = fixed.arm
        fixed.arm = lambda E, w, mode="energy", seed=1: (inner(E, w, mode, seed), w)
        fixed._arms_are_paired = True
    return _deps

red.deps = _patched_deps

def summarize(tags):
    """rows already flushed -> aggregate + the ONE band + call2's verdict. Two quantities,
    never merged: the ALLOCATION band (spread of random SEED MEANS) and the per-prompt
    SAMPLING spread of key_only - uniform. Also repairs red.run()'s own summary line,
    which dies on `"%s|%s" % k` over call2's SIX-element key after the rows are safe."""
    out = _deps[2].get_local("osc_band_qknorm_dir") + "/" + red.OUT + "qwen3"
    rows = [json.loads(x) for x in open(out + "/cells.jsonl") if x.strip()]
    agg = red.aggregate(rows)
    open(out + "/cells_agg.jsonl", "w").write("".join(json.dumps(r) + "\n" for r in agg))
    cells = {}
    for b in tags:
        raw = [r for r in rows if r["budget"] == b]           # per-PROMPT: sampling error
        sm = red.seed_means(raw)
        try:
            bl = {"band": red.band(list(sm.values())), "band_why": "max-min over %d random seed means" % len(sm)}
        except ValueError as e:
            bl = {"band": None, "band_why": str(e)}
        pk = {a: sorted(r["agree"] for r in raw if r["arm"] == a) for a in ("uniform", "key_only")}
        pm = [round(k - u, 9) for u, k in zip(pk["uniform"], pk["key_only"])]
        cells[b] = {"seed_means": sm, **bl, "n_prompts": len(pm),
                    "key_only_minus_uniform": round(sum(pm) / len(pm), 9), "prompt_margins": pm,
                    "sampling_spread": round(max(pm) - min(pm), 9),
                    "calls": {"|".join(str(x) for x in k): v for k, v in
                              red.c2.judge([r for r in agg if r["budget"] == b], "key_only", "uniform").items()}}
    meta = {"model": rows[0]["model"], "np": rows[0]["np"], "budgets": tags, "min_seeds": red.MINS,
            "seeds": sorted({r["seed"] for r in agg if r["arm"] == "random"}),
            "grid_budgets": list(_deps[4].GRID[rows[0]["np"]]),
            "band_rule": "max-min over random SEED MEANS (allocation); per-prompt spread is the sampling error, never folded in",
            "call_rule": "osc_band_call2_a00-cc7b25cc.judge(key_only vs uniform)",
            "cut": "PARTIAL MEASUREMENT: %d of %d np64 budgets, %d eval prompts (first %d of build_eval)" % (
                len(tags), len(_deps[4].GRID[rows[0]["np"]]), cells[tags[0]]["n_prompts"], cells[tags[0]]["n_prompts"]),
            "cells": cells}
    json.dump(meta, open(out + "/summary.json", "w"), indent=1)
    return meta

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("which", choices=("qwen3",))
    p.add_argument("--budgets", default="4.125")
    p.add_argument("--prompts", type=int, default=2)
    p.add_argument("--seeds", default="7,21,99")
    p.add_argument("--check", action="store_true")
    a = p.parse_args()
    tags = [t.strip() for t in a.budgets.split(",") if t.strip()]
    if a.check:
        _patched_deps()[4].check_table()
    else:
        try:
            red.run(a.which, [int(s) for s in a.seeds.split(",")], tags, a.prompts)
        except TypeError as e:
            print("red.run summary stage refused (%s); rebuilding from flushed rows" % e, flush=True)
        print("LANDED", json.dumps(summarize(tags), indent=1), flush=True)
