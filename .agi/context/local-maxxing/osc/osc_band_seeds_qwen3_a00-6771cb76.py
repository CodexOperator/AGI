#!/usr/bin/env python3
"""Per-cell noise band on the np64 qk-norm grid: the RANDOM arm redrawn at N seeds.

band = range (max - min) of the random arm's agree over the seed set; the
key_only-minus-uniform margin is called win / loss / inside-noise against it.
Deterministic arms (uniform, key_only) reach fixed.arm with no RNG in the path,
so they are drawn ONCE and labelled n=1 -- a 0.0 spread for them is spread by
construction, not an error bar.
Run: osc_band_seeds_qwen3_a00-6771cb76.py qwen3 --seeds 7,21,99,45
"""
import argparse, importlib.util, json, os, sys
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
import numpy as np, torch, paths, osc_band_prune as obp
_s = importlib.util.spec_from_file_location("m", os.path.join(HERE, "osc_band_matched_uniform_a00-a721f95f.py"))
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)
fixed, GRID, MINS, NP64, OUT = m.fixed, m.GRID, 3, 64, "a00-6771cb76-"
SEEDS_DEFAULT = ",".join(str(s) for s in json.load(open(paths.config_path()))["values"]["local_maxxing"]["osc_band_seeds"])

def band(vals):
    """Range of a stochastic arm's agree. REFUSES fewer than MINS DISTINCT VALUES with a
    raise, not an assert: `python -O` strips asserts, and a length-only gate is the n=1
    trap in an n=3 hat -- band([0.30]*3) would be 0.0 and every margin a 'win'."""
    n = len({round(v, 12) for v in vals})
    if len(vals) < MINS or n < MINS:
        raise ValueError("refuse a band from %d draws / %d distinct values; %d of each required"
                         % (len(vals), n, MINS))
    return round(max(vals) - min(vals), 9)

def call(margin, b):
    """Three-way: the parent asks win / loss / inside-noise, and a key_only 25 bands
    below uniform is a LOSS, not an overlap."""
    return "win" if margin > b else ("loss" if margin < -b else "inside-noise")

def guard(which, npv=None):
    """Refuse BEFORE any from_pretrained: this file is the np64 grid, so it admits
    only qwen3, and the measured head_dim must still be 64 afterwards."""
    if which != "qwen3": raise ValueError("np64 grid only: pass 'qwen3', not %r" % (which,))
    if npv is not None and npv != NP64: raise ValueError("np=%d measured, this grid is np%d" % (npv, NP64))

def run(which, seeds, budgets=None, n_prompts=None):
    guard(which)
    if len(set(seeds)) != len(seeds): raise ValueError("duplicate seeds would fake n: %r" % (seeds,))
    from transformers import AutoTokenizer, AutoModelForCausalLM
    hf = paths.get("osc15_hf_dir")
    tok = AutoTokenizer.from_pretrained(hf)
    model = AutoModelForCausalLM.from_pretrained(hf, dtype=torch.float32, attn_implementation="eager").eval()
    fixed.install(model); guard(which, fixed.SPEC["np"])
    prompts, emeta = obp.build_eval(tok)
    if n_prompts: prompts, emeta = prompts[:n_prompts], dict(emeta, n_prompts=len(prompts[:n_prompts]))
    E = m.profile(model, prompts)
    refs = [torch.log_softmax(fixed.forward(model, i).float(), -1) for i in prompts]
    out = paths.get_local("osc_band_qknorm_dir") + "/" + OUT + which
    os.makedirs(out, exist_ok=True); cells = {}
    with open(out + "/cells.jsonl", "w") as fh:
        def cell(budget, arm, seed, a, w):
            ag = kl = 0.0
            for r, i in zip(refs, prompts):
                x, y = obp.metrics(r, fixed.forward(model, i, a, w)); ag += x / len(prompts); kl += y / len(prompts)
            stoch = arm == "random"
            rec = {"model": which, "np": fixed.SPEC["np"], "cell": "%s@%s" % (which, budget), "budget": budget,
                   "arm": arm, "arm_is_stochastic": stoch, "seed": seed if stoch else 0,
                   "n": len(seeds) if stoch else 1, "n_prompts": len(prompts), "widths": w,
                   "agree": round(ag, 9), "kl": round(kl, 9)}
            fh.write(json.dumps(rec) + "\n"); fh.flush(); print(rec, flush=True)
            cells.setdefault(budget, {}).setdefault(arm, []).append(ag)
        for tag, (un, mt) in GRID[fixed.SPEC["np"]].items():
            if budgets and tag not in budgets: continue
            cell(tag, "uniform", 0, fixed.arm(E, un, "uniform"), un)
            cell(tag, "key_only", 0, fixed.arm(E, mt, "energy", 1), mt)
            for s in seeds: cell(tag, "random", s, fixed.arm(E, mt, "random", s), mt)
    calls = {}
    for tag, arms in cells.items():
        b = band(arms["random"]); mg = round(arms["key_only"][0] - arms["uniform"][0], 9)
        calls[tag] = {"band": b, "n_seeds": len(arms["random"]),
                      "n_distinct": len({round(v, 12) for v in arms["random"]}),
                      "key_only_minus_uniform": mg, "call": call(mg, b),
                      "random_agree": [round(v, 9) for v in arms["random"]], "uniform_agree": round(arms["uniform"][0], 9),
                      "key_only_agree": round(arms["key_only"][0], 9), "uniform_n": 1, "key_only_n": 1}
    json.dump({"model": which, "np": fixed.SPEC["np"], "seeds": seeds, "min_seeds": MINS, "band": "max-min of random agree",
               "eval": emeta, "grid": GRID[fixed.SPEC["np"]], "calls": calls}, open(out + "/summary.json", "w"), indent=1)
    print(json.dumps(calls, indent=1)); return calls

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("which", choices=("qwen3",)); p.add_argument("--seeds", default=SEEDS_DEFAULT)
    p.add_argument("--budgets", default=""); p.add_argument("--prompts", type=int, default=0)
    p.add_argument("--check", action="store_true"); a = p.parse_args()
    if a.check: m.check_table()
    else: run(a.which, [int(s) for s in a.seeds.split(",")],
              a.budgets.split(",") if a.budgets else None, a.prompts or None)
