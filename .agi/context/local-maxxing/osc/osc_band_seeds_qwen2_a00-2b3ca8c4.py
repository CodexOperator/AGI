#!/usr/bin/env python3
"""Qwen2 np32: the random control re-drawn at N seeds per budget -> the allocation-noise band.
a00-a721f95f compared ONE hardcoded random draw (n=1) against uniform and key_only; this
re-draws it at every seed in the config cell values.local_maxxing.osc_band_seeds (never a
literal here). The ROW CONTRACT and the TWO calls -- (a) MARGIN, the adopted rule, and
(b) RANGE -- are canonical in the config cell values.local_maxxing.osc_band_row_contract.
Cite that CELL, not this script: no second copy of the contract lives here (PASS 8 item 5)."""
import importlib.util, json, os, sys, time
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]  # collect from any cwd
import numpy as np, torch, paths, osc_band_prune as obp

_s = importlib.util.spec_from_file_location("grid", os.path.join(HERE, "osc_band_matched_uniform_a00-a721f95f.py"))
grid = importlib.util.module_from_spec(_s); _s.loader.exec_module(grid)
fixed = grid.fixed  # ONE instance: grid.profile() and run() must share the configured SPEC
KID, NP = "a00-2b3ca8c4-582f1e", 32
OUT = os.path.join(paths.get_local("osc_band_qknorm_dir"), KID + "-qwen2-seeds")
os.makedirs(OUT, exist_ok=True)

def seeds():
    """The seed LIST is a config cell (values.local_maxxing.osc_band_seeds), read at runtime."""
    return [int(s) for s in json.load(open(paths.config_path()))["values"]["local_maxxing"]["osc_band_seeds"]]

def check():
    """No model. Falsifier 1: the seed reaches the allocation (and energy is deterministic)."""
    fixed.SPEC.update(np=NP, nl=24, kv=2)  # qwen2.5 geometry, so the check needs no model
    E = np.zeros((24, 2, NP)); E[0, 0, 0] = 1.0; w = grid.GRID[NP]["5.25"][1]
    draws = [fixed.arm(E, w, "random", s) for s in seeds()]; e = fixed.arm(E, w, "energy", 1)
    assert len(draws) >= 3, "falsifier 3: fewer than 3 distinct seeds"
    assert all(any(not torch.equal(x, y) for x, y in zip(p, q)) for p, q in zip(draws, draws[1:])), "falsifier 1: seed ignored"
    assert all(torch.equal(x, y) for x, y in zip(e, fixed.arm(E, w, "energy", 1))), "energy arm not deterministic"
    grid.check_table()  # falsifier 4: bit-matched uniform == matched, all four budgets
    print("check OK np", NP, "seeds", seeds())

def run(which="qwen2"):
    from transformers import AutoTokenizer, AutoModelForCausalLM
    hf = paths.get("osc03_hf_dir")
    tok = AutoTokenizer.from_pretrained(hf); model = AutoModelForCausalLM.from_pretrained(hf, dtype=torch.float32, attn_implementation="eager").eval()
    fixed.install(model)  # configures fixed.SPEC
    assert fixed.SPEC["np"] == NP
    prompts, emeta = obp.build_eval(tok); E = grid.profile(model, prompts); S = seeds()
    arms = [(tag, m, fixed.arm(E, m, "random", s), s) for tag, (u, m) in grid.GRID[NP].items() for s in S]
    t = time.time(); agg = {}
    for pi, ids in enumerate(prompts):
        ref = torch.log_softmax(fixed.forward(model, ids).float(), -1)
        for tag, m, a, s in arms:
            ag, kl = obp.metrics(ref, fixed.forward(model, ids, a, m))
            r = agg.setdefault((tag, s), [0., 0.]); r[0] += ag / len(prompts); r[1] += kl / len(prompts)
        print(which, pi + 1, round(time.time() - t), flush=True)
    with open(os.path.join(OUT, "cells.jsonl"), "w") as fh:
        for (tag, s), (ag, kl) in sorted(agg.items()):
            fh.write(json.dumps({"model": which, "np": NP, "cell": f"{which}:random@{tag}@s{s}", "budget": tag, "arm": "random",
                                 "seed": s, "n": len(S), "arm_is_stochastic": True, "widths": grid.GRID[NP][tag][1],
                                 "agree": round(ag, 9), "kl": round(kl, 9)}) + "\n")
        for tag in grid.GRID[NP]:  # DETERMINISTIC arms: ONE row, seed 0, n 1 (row contract) so p3 has a group to count
            for arm in ("uniform", "key_only"):
                ag, kl = _baselines()[arm + "|" + tag]
                fh.write(json.dumps({"model": which, "np": NP, "cell": f"{which}:{arm}@{tag}@s0", "budget": tag, "arm": arm,
                                     "seed": 0, "n": 1, "arm_is_stochastic": False, "widths": grid.GRID[NP][tag][1],
                                     "agree": ag, "kl": kl}) + "\n")
    doc = {"meta": {"seeds": S, "grid": grid.GRID[NP], "eval": emeta}, "band": band(agg), "cells": {f"{tg}@s{s}": v for (tg, s), v in sorted(agg.items())}, "t_s": round(time.time() - t, 1)}
    json.dump(doc, open(os.path.join(OUT, "band.json"), "w"), indent=1)
    print(json.dumps(doc["band"], indent=1))

def _baselines():
    """The matched run's uniform/key_only rows, keyed '<arm>|<budget>' -- the same rows run() now emits."""
    return {r["arm"] + "|" + r["budget"]: (r["agree"], r["kl"])
            for r in map(json.loads, open(os.path.join(paths.get_local("osc_band_qknorm_dir"),
                                                      "a00-a721f95f-qwen2", "cells.jsonl")))}

def band(agg, base=None):
    """Per budget: half-range over seeds and BOTH calls of the canonical row contract, named apart.

    (a) MARGIN, the ADOPTED rule: |key_only - uniform| <= the FULL min-max range of the random seeds
        -> `margin_call_inside_*`.  (b) RANGE: min(random) <= key_only <= max(random) -> `inside_*`.
    Different denominators, different answers; a reader must name the one it applies. The two
    margins are sign-EXPLICIT and in OPPOSITE order: key_only-minus-uniform on agree,
    uniform-minus-key_only on KL.
    """
    base = base or _baselines()
    out = {}
    for tag in grid.GRID[NP]:
        ag = [v[0] for (t, s), v in agg.items() if t == tag]; kl = [v[1] for (t, s), v in agg.items() if t == tag]
        ua, uk = base["uniform|" + tag]; oa, ok = base["key_only|" + tag]
        dag, dkl = oa - ua, uk - ok
        out[tag] = {"agree_half_range": round((max(ag) - min(ag)) / 2, 6), "kl_half_range": round((max(kl) - min(kl)) / 2, 6),
                    "key_only_minus_uniform_agree": round(dag, 6), "uniform_minus_key_only_kl": round(dkl, 6),
                    "margin_call_inside_agree": bool(abs(dag) <= max(ag) - min(ag)),
                    "margin_call_inside_kl": bool(abs(dkl) <= max(kl) - min(kl)),
                    "inside_agree": bool(min(ag) <= oa <= max(ag)), "inside_kl": bool(min(kl) <= ok <= max(kl))}
    return out

if __name__ == "__main__":
    if "--check" in sys.argv: check()
    else: run()
