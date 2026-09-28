#!/usr/bin/env python3
"""Largest-safe-step search ABOVE 3.5 bits (uniform w=8 already misses the bar).
Reuses the OSC.10 script's quantizer/hook/arm builder unchanged; adds higher-bit
arms: uniform keys w in {8,9,10,11,12} and ENERGY allocations at matched
avg_bits, plus 3 random seeds at the energy-9.0 point. 8 prompts x 512 tokens.
"""
import importlib.util, json, os, sys, time
import numpy as np, torch
HERE = "/data/work/agi/.agi/worktrees/a00-30502399/.agi/context/local-maxxing/osc"
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
_p = os.path.join(HERE, "osc_band_kquant_a00-86466b78.py")
_s = importlib.util.spec_from_file_location("kqm", _p)
kq = importlib.util.module_from_spec(_s); _s.loader.exec_module(kq)
import osc_band_prune as obp
import paths
torch.set_num_threads(4)
NPAIR, GROUP = 32, 7

from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained(obp.HF)
model = AutoModelForCausalLM.from_pretrained(obp.HF, dtype=torch.float32,
                                             attn_implementation="eager").eval()
kq.install(model)
prompts, meta = obp.build_eval(tok)
heads = json.load(open(os.path.join(paths.get_local("osc_band_dir"),
                                    "profiles.json")))["heads"]
E = np.array([[np.array([heads[f"L{L}H{k*GROUP+g}"]["profile_pooled"]
                         for g in range(GROUP)]).sum(0) for k in range(2)]
              for L in range(24)])

S = [4, 4, 8, 16]
SPEC = [("uniform_w8", "u", [32], [8], None),
        ("uniform_w9", "u", [32], [9], None),
        ("uniform_w10", "u", [32], [10], None),
        ("uniform_w11", "u", [32], [11], None),
        ("uniform_w12", "u", [32], [12], None),
        ("energy_6p0", "e", S, [8, 8, 4, 4], None),
        ("energy_8p0", "e", S, [8, 8, 8, 6], None),
        ("energy_9p0", "e", S, [8, 8, 8, 8], None),
        ("energy_10p5", "e", S, [12, 12, 10, 8], None),
        ("energy_13p0", "e", S, [12, 12, 12, 12], None),
        ("rand_9p0_s1", "r", S, [8, 8, 8, 8], 1),
        ("rand_9p0_s2", "r", S, [8, 8, 8, 8], 2),
        ("rand_9p0_s3", "r", S, [8, 8, 8, 8], 3),
        ("energy_3p5", "e", S, [4, 4, 2, 2], None)]
arms, bits = {}, {}
for name, mode, sizes, widths, seed in SPEC:
    ncl = len(sizes)
    if mode == "r":
        arms[name] = (*kq.make_arm(E, sizes, widths,
                                   np.random.default_rng(seed)), False)
    else:
        arms[name] = (*kq.make_arm(E, sizes, widths, by_energy=(mode == "e")), False)
    bits[name] = kq.avg_bits(sizes, widths, ncl)
print("arms:", {k: round(v, 4) for k, v in bits.items()}, flush=True)

agg = {k: {"agree": 0.0, "kl": 0.0} for k in arms}
t0 = time.time()
for pi, ids in enumerate(prompts):
    kq.wait_mem()
    ref = kq.logits(model, ids, (None, None, False))
    refp = torch.log_softmax(ref.float(), -1)
    for k, arm in arms.items():
        a, kl = obp.metrics(refp, kq.logits(model, ids, arm))
        agg[k]["agree"] += a / len(prompts)
        agg[k]["kl"] += kl / len(prompts)
    print(f"prompt {pi+1}/{len(prompts)} {time.time()-t0:.0f}s", flush=True)

res = {k: {"agree": round(agg[k]["agree"], 6), "kl": round(agg[k]["kl"], 6),
           "bits": round(bits[k], 6)} for k in arms}
hold = [k for k in res if res[k]["agree"] >= 0.98 and res[k]["kl"] <= 0.02]
best = min(hold, key=lambda k: (res[k]["bits"], -res[k]["agree"])) if hold else None
first = {}
for fam, pre in [("energy", "energy_"), ("uniform", "uniform_")]:
    c = [k for k in hold if k.startswith(pre)]
    first[fam] = min((res[k]["bits"] for k in c), default=None)
sn = "/data/work/agi/.agi/worktrees/a00-30502399/.agi/sessions/iter-OSC.10/a00-86466b78"
json.dump({"arms": res, "hold_both": hold, "largest_safe_step": best,
           "lowest_holding_bits": first, "eval": meta,
           "t_s": round(time.time() - t0, 1)},
          open(os.path.join(sn, "higher_bits.json"), "w"), indent=1)
md = ["# largest-safe-step search above 3.5 bits", "",
      "| arm | avg bits | agree | mean KL | holds |", "|---|---|---|---|---|"]
for k in sorted(res, key=lambda k: res[k]["bits"]):
    md.append(f"| {k} | {res[k]['bits']} | {res[k]['agree']} | {res[k]['kl']} | "
              f"{res[k]['agree'] >= 0.98 and res[k]['kl'] <= 0.02} |")
md += ["", f"lowest avg bits holding both bars: {best}", f"per family: {first}", ""]
open(os.path.join(sn, "higher_bits.md"), "w").write("\n".join(md))
print(json.dumps({"largest_safe_step": best, "lowest_holding_bits": first}, indent=1))
