#!/usr/bin/env python3
"""Byte-matched uniform, key-energy, inverse-energy, and random band sweep."""
import argparse, importlib.util, json, os, sys
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
HERE = os.path.dirname(__file__); ROOT = os.getcwd()
sys.path[:0] = [os.path.join(ROOT, ".agi/context/local-maxxing"), HERE]
import numpy as np, torch, paths, osc_band_prune as obp
_s = importlib.util.spec_from_file_location("fixed", os.path.join(HERE, "osc_band_kquant_qknorm_a00-bcb6c85e.py"))
fixed = importlib.util.module_from_spec(_s); _s.loader.exec_module(fixed)
BUDGETS = ("4.25", "5.25", "6.25", "7.25")
GRID = {
    32: {"4.25": ([4], [4, 4, 3, 3]), "5.25": ([5], [5, 5, 4, 4]),
         "6.25": ([6], [6, 6, 5, 5]), "7.25": ([7], [7, 7, 6, 6])},
    64: {"4.125": ([4], [5, 4, 4, 3]), "5.125": ([5], [6, 5, 5, 4]),
         "6.125": ([6], [7, 6, 6, 5]), "7.125": ([7], [8, 7, 7, 6])},
}
ARMS = ("uniform", "key_only", "inverse_energy", "random")

def check_table():
    """Pre-model acceptance: computed budgets equal and matched classes descend."""
    for npv, grid in GRID.items():
        fixed.SPEC["np"] = npv
        for tag, (uniform, matched) in grid.items():
            bu, bm = fixed.bits(uniform), fixed.bits(matched)
            assert bu == bm == float(tag) and all(matched[i] >= matched[i+1] for i in range(3))
            assert fixed.bits([4]) == 4 + 8 / npv
            print(npv, tag, uniform, bu, matched, bm, "OK")

def profile(model, prompts):
    """Raw squared post-RoPE key energy, averaged over four calibration prompts."""
    E = np.zeros((fixed.SPEC["nl"], fixed.SPEC["kv"], fixed.SPEC["np"]))
    for ids in prompts[:4]:
        fixed.CAP.clear(); fixed.forward(model, ids, capture=True)
        for L in range(fixed.SPEC["nl"]):
            k = fixed.CAP[L][1][0].float().reshape(fixed.SPEC["kv"], -1, fixed.SPEC["np"], 2)
            E[L] += k.square().sum(-1).mean(1).cpu().numpy() / 4
    return E

def allocation(E, widths, arm):
    if arm == "uniform": return fixed.arm(E, widths, "uniform")
    if arm == "key_only": return fixed.arm(E, widths, "energy", 1)
    if arm == "inverse_energy": return fixed.arm(-E, widths, "energy", 1)
    return fixed.arm(E, widths, "random", 7)

def run(which):
    from transformers import AutoTokenizer, AutoModelForCausalLM
    hf = paths.get("osc15_hf_dir" if which == "qwen3" else "osc03_hf_dir")
    tok = AutoTokenizer.from_pretrained(hf)
    model = AutoModelForCausalLM.from_pretrained(hf, dtype=torch.float32, attn_implementation="eager").eval()
    fixed.install(model)
    if "nl" not in fixed.SPEC: fixed.configure(model)
    prompts, emeta = obp.build_eval(tok); E = profile(model, prompts)
    npv = fixed.SPEC["np"]; out = paths.get_local("osc_band_qknorm_dir") + "/a00-a721f95f-" + which
    os.makedirs(out, exist_ok=True); path = out + "/cells.jsonl"
    done = set()
    if os.path.exists(path):
        with open(path) as f: done = {json.loads(x)["cell"] for x in f if x.strip()}
    with open(path, "a") as fh:
        for tag, (uniform, matched) in GRID[npv].items():
            for arm in ARMS:
                key = f"{which}:{arm}@{tag}"
                if key in done: continue
                widths = uniform if arm == "uniform" else matched; vals = [0.0, 0.0]; a = allocation(E, widths, arm)
                for ids in prompts:
                    ref = torch.log_softmax(fixed.forward(model, ids).float(), -1)
                    ag, kl = obp.metrics(ref, fixed.forward(model, ids, a, widths))
                    vals[0] += ag / len(prompts); vals[1] += kl / len(prompts)
                rec = {"model": which, "np": npv, "cell": key, "budget": tag, "arm": arm,
                       "widths": widths, "agree": round(vals[0], 9), "kl": round(vals[1], 9)}
                fh.write(json.dumps(rec) + "\n"); fh.flush(); print(rec, flush=True)
    with open(out + "/meta.json", "w") as f:
        json.dump({"model": which, "np": npv, "grid": GRID[npv], "eval": emeta, "complete": True}, f, indent=1)

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("which", nargs="?", choices=("qwen2", "qwen3")); p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if args.check: check_table()
    else: run(args.which)
