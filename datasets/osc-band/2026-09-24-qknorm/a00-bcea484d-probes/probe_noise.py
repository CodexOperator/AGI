#!/usr/bin/env python3
"""PARENT PROBE 2 (qwen2 @ 5.25): is the key_only win larger than allocation NOISE?

The cells report ONE random allocation per budget. If re-drawing the random
control moves agree by as much as key_only's margin over uniform, the
"band beats uniform" reading is a single-sample artefact.
"""
import importlib.util, os, sys
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
HERE = "/data/work/agi/.agi/worktrees/a00-bcea484d/.agi/context/local-maxxing/osc"
ROOT = "/data/work/agi/.agi/worktrees/a00-bcea484d"
sys.path[:0] = [os.path.join(ROOT, ".agi/context/local-maxxing"), HERE]
import numpy as np, torch, paths, osc_band_prune as obp
s = importlib.util.spec_from_file_location("fixed", HERE + "/osc_band_kquant_qknorm_a00-bcb6c85e.py")
fixed = importlib.util.module_from_spec(s); s.loader.exec_module(fixed)
s2 = importlib.util.spec_from_file_location("h", HERE + "/osc_band_matched_uniform_a00-a721f95f.py")

from transformers import AutoTokenizer, AutoModelForCausalLM
hf = paths.get("osc03_hf_dir")
tok = AutoTokenizer.from_pretrained(hf)
model = AutoModelForCausalLM.from_pretrained(hf, dtype=torch.float32, attn_implementation="eager").eval()
fixed.install(model)
prompts, _ = obp.build_eval(tok)
E = np.zeros((fixed.SPEC["nl"], fixed.SPEC["kv"], fixed.SPEC["np"]))
for ids in prompts[:4]:
    fixed.CAP.clear(); fixed.forward(model, ids, capture=True)
    for L in range(fixed.SPEC["nl"]):
        k = fixed.CAP[L][1][0].float().reshape(fixed.SPEC["kv"], -1, fixed.SPEC["np"], 2)
        E[L] += k.square().sum(-1).mean(1).cpu().numpy() / 4

UNIF, MATCHED = [5], [5, 5, 4, 4]
runs = [("uniform", UNIF, ("uniform", 1)), ("key_only", MATCHED, ("energy", 1))]
runs += [(f"random_seed{seed}", MATCHED, ("random", seed)) for seed in (7, 21, 99)]
out = {}
for name, widths, (mode, seed) in runs:
    a = fixed.arm(E if mode != "uniform" else -E, widths, mode, seed)
    ag = kl = 0.0
    for ids in prompts:
        ref = torch.log_softmax(fixed.forward(model, ids).float(), -1)
        g, k2 = obp.metrics(ref, fixed.forward(model, ids, a, widths))
        ag += g / len(prompts); kl += k2 / len(prompts)
    out[name] = (round(ag, 6), round(kl, 6))
    print(name, out[name], flush=True)

rs = [out[n][0] for n in out if n.startswith("random_seed")]
print("random agree spread: min %.6f max %.6f range %.6f" % (min(rs), max(rs), max(rs) - min(rs)))
print("key_only margin over uniform (agree): %+.6f  (kl): %+.6f"
      % (out["key_only"][0] - out["uniform"][0], out["key_only"][1] - out["uniform"][1]))
print("VERDICT: win exceeds noise" if (out["key_only"][0] - out["uniform"][0]) > (max(rs) - min(rs))
      else "VERDICT: win WITHIN single-sample noise")
