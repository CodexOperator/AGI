#!/usr/bin/env python3
"""Band REDUCER with the distinct-value gate, plus the smallest run that feeds it.
The gate lives in the REDUCER, not the CLI: run() already refuses duplicate SEEDS, but
that is a different quantity -- three DISTINCT seeds returning three IDENTICAL agrees is
a stub, and `len(vals) < 3` cannot see it (band([0.30]*3) returned a measured 0.0 and
every cell then read as an infinite win). band() refuses n<3 AND distinct<3 and says which.
Run: osc_band_reduce_a00-4c09956d.py qwen3 --budgets 4.125 --prompts 2 --seeds 7,21,99
"""
import argparse, importlib.util, json, os, sys
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
_c = importlib.util.spec_from_file_location("c2", os.path.join(HERE, "osc_band_call2_a00-cc7b25cc.py"))
c2 = importlib.util.module_from_spec(_c); _c.loader.exec_module(c2)
MINS, NP64, OUT = 3, 64, "a00-4c09956d-"
def deps():
    """torch/numpy/transformers/paths imported HERE, not at module scope: p3 is a
    model-free decide layer and must import this reducer on a box with no torch."""
    import numpy as np, torch, paths, osc_band_prune as obp
    s = importlib.util.spec_from_file_location("m", os.path.join(HERE, "osc_band_matched_uniform_a00-a721f95f.py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return np, torch, paths, obp, m
def band(vals, arm="random"):
    """Range (max-min) of a STOCHASTIC arm's agree. Raises, never asserts: `python -O`
    strips asserts and would report a one-draw spread as a measured 0.0."""
    n = len(vals); d = len({round(float(v), 12) for v in vals})
    if n < MINS: raise ValueError("refuse band: n=%d draws of %s, %d required" % (n, arm, MINS))
    if d < MINS: raise ValueError("refuse band: n=%d draws of %s but only %d DISTINCT value(s) -- a repeated draw is a stub, not a measurement" % (n, arm, d))
    return round(max(vals) - min(vals), 9)
def guard(which, npv=None):
    """Refuse BEFORE any from_pretrained: this grid is np64/qwen3 only. The last harness
    spent 53s and 3.2 GiB loading the WRONG weights before it crashed on `OUT + None`."""
    if which != "qwen3": raise ValueError("np64 grid only: pass 'qwen3', not %r" % (which,))
    if npv is not None and npv != NP64: raise ValueError("np=%s measured, this grid is np%d" % (npv, NP64))
def seed_means(rows, arm="random"):
    """{seed: mean agree} over per-prompt rows = the ALLOCATION band, one number per
    seed. The per-prompt spread is a different quantity and is never folded in here."""
    acc = {}
    for r in rows:
        if r["arm"] == arm: acc.setdefault(r["seed"], []).append(r["agree"])
    return {s: round(sum(v) / len(v), 9) for s, v in acc.items()}
def aggregate(rows):
    """Per-prompt rows -> one values.local_maxxing.osc_band_row_contract row per
    (budget, arm, seed): what call2 consumes. n counts DISTINCT seeds, never rows."""
    g, sd = {}, {}
    for r in rows:
        g.setdefault((r["budget"], r["arm"], r["seed"]), []).append(r)
        if r["arm"] == "random": sd.setdefault((r["budget"], r["arm"]), set()).add(r["seed"])
    return [{"model": rows[0]["model"], "np": rows[0]["np"], "budget": b, "arm": a, "seed": s,
             "n": len(sd[(b, a)]) if a == "random" else 1, "arm_is_stochastic": a == "random",
             "widths": v[0]["widths"], "prompts": len(v),
             "agree": round(sum(x["agree"] for x in v) / len(v), 9),
             "kl": round(sum(x["kl"] for x in v) / len(v), 9)} for (b, a, s), v in g.items()]
def run(which, seeds, budgets, n_prompts):
    guard(which)
    np, torch, paths, obp, m = deps(); fixed = m.fixed; GRID = m.GRID
    if len(set(seeds)) != len(seeds): raise ValueError("duplicate seeds would fake n: %r" % (seeds,))
    if len(seeds) < MINS: raise ValueError("n=%d seeds, %d required to band anything" % (len(seeds), MINS))
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(paths.get("osc15_hf_dir"))
    model = AutoModelForCausalLM.from_pretrained(paths.get("osc15_hf_dir"), dtype=torch.float32, attn_implementation="eager").eval()
    fixed.install(model); guard(which, fixed.SPEC["np"])
    prompts, emeta = obp.build_eval(tok)
    emeta = dict(emeta, n_prompts=min(n_prompts, len(prompts)), cut="first %d prompts of build_eval" % n_prompts)
    prompts = prompts[:n_prompts]
    E = m.profile(model, prompts)
    out = paths.get_local("osc_band_qknorm_dir") + "/" + OUT + which
    os.makedirs(out, exist_ok=True); rows = []
    fh = open(out + "/cells.jsonl", "w")
    for tag in budgets:
        un, mt = GRID[fixed.SPEC["np"]][tag]
        # every (arm, seed) allocation FIRST, then prompts OUTER: one ref per prompt.
        arms = [("uniform", None, fixed.arm(E, un, "uniform")), ("key_only", None, fixed.arm(E, mt, "energy", 1))]
        arms += [("random", s, fixed.arm(E, mt, "random", s)) for s in seeds]
        for i, p in enumerate(prompts):
            ref = torch.log_softmax(fixed.forward(model, p).float(), -1)  # one ref, DROPPED per prompt
            for a, s, al in arms:
                ag, kl = obp.metrics(ref, fixed.forward(model, p, *al))
                r = {"model": which, "np": fixed.SPEC["np"], "cell": "%s/%s/%s" % (tag, a, s), "budget": tag,
                     "arm": a, "seed": 0 if s is None else s, "n": 1 if s is None else len(seeds),
                     "arm_is_stochastic": s is not None, "prompt": i, "widths": un if a == "uniform" else mt,
                     "agree": round(ag, 9), "kl": round(kl, 9)}
                rows.append(r); fh.write(json.dumps(r) + "\n"); fh.flush(); print(r, flush=True)
    fh.close()
    agg = aggregate(rows)
    sm = {b: seed_means([r for r in agg if r["budget"] == b]) for b in budgets}
    bl = {}
    for b in budgets:
        try: bl[b] = {"band": band(list(sm[b].values())), "why": "measured"}
        except ValueError as e: bl[b] = {"band": None, "why": str(e)}
    meta = {"model": which, "np": fixed.SPEC["np"], "seeds": seeds, "budgets": budgets, "min_seeds": MINS,
            "eval": emeta, "grid_budgets": list(GRID[fixed.SPEC["np"]]),
            "band_rule": "max-min over random SEED MEANS (allocation); per-prompt spread is the sampling error, never folded in",
            "call_rule": "osc_band_call2_a00-cc7b25cc.judge(key_only vs uniform) over cells_agg.jsonl",
            "cut": "PARTIAL MEASUREMENT: %d of %d np64 budgets, %d eval prompts" % (len(budgets), len(GRID[fixed.SPEC["np"]]), emeta["n_prompts"]),
            "cells": {}}
    for b in budgets:
        sel = [r for r in agg if r["budget"] == b]
        marg = {a: [r["agree"] for r in sel if r["arm"] == a] for a in ("uniform", "key_only")}
        meta["cells"][b] = {"seed_means": sm[b], **bl[b], "n_prompts": emeta["n_prompts"],
                            "uniform_agree": marg["uniform"][0], "key_only_agree": marg["key_only"][0],
                            "prompt_margins": [round(k - u, 9) for u, k in zip(marg["uniform"], marg["key_only"])],
                            "calls": {"%s|%s" % k: v for k, v in c2.judge(sel, "key_only", "uniform").items() if k[2] == b}}
    json.dump(meta, open(out + "/summary.json", "w"), indent=1)
    open(out + "/cells_agg.jsonl", "w").write("".join(json.dumps(r) + "\n" for r in agg))
    print(json.dumps(meta["cells"], indent=1)); return meta
if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("which", choices=("qwen3",))
    p.add_argument("--seeds", default="7,21,99"); p.add_argument("--budgets", default="4.125")
    p.add_argument("--prompts", type=int, default=2); p.add_argument("--check", action="store_true")
    a = p.parse_args()
    if a.check: deps()[4].check_table()
    else: run(a.which, [int(s) for s in a.seeds.split(",")], [b.strip() for b in a.budgets.split(",") if b.strip()], a.prompts)
