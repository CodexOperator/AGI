#!/usr/bin/env python3
"""Byte audit: count the bits fixed.quant() actually emits, per arm per layer per head.

Wraps the shipped quant() (no second copy of it, no second copy of bits()) and, on
each real call, re-derives the count from the very class sets and absmax values
that call iterates.  The mask entry d is ONE channel, and the cost of a channel is
w bits (2*w per RoPE PAIR, two channels); the per-class scale is one 16-bit value
per class actually visited, shared by that class's channels.  A degenerate class is
therefore VISIBLE, which a nominal-size re-derivation could never show.
"""
import argparse, importlib.util, json, os, sys
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.getcwd()
sys.path[:0] = [os.path.join(ROOT, ".agi/context/local-maxxing"), HERE]
import numpy as np, torch, paths, osc_band_prune as obp
_s = importlib.util.spec_from_file_location("fixed", os.path.join(HERE, "osc_band_kquant_qknorm_a00-bcb6c85e.py"))
fixed = importlib.util.module_from_spec(_s); _s.loader.exec_module(fixed)
STATE = {"arm": None, "rows": []}

def audit(k, dm, widths):
    """Emit one row per kv head: bits, scales, per-class channels and max step."""
    out = []
    for h in range(dm.shape[0]):
        n_scales = 0; payload = 0; chans = []; step = {}
        for c, w in enumerate(widths):
            d = (dm[h] == c).nonzero().flatten()
            if d.numel() == 0:                      # quant() emits no scale for an empty class
                chans.append(0); continue
            n_scales += 1; payload += int(d.numel()) * w; chans.append(int(d.numel()))
            x = k[:, h, :, d]
            a = x.abs().amax(-1, keepdim=True).clamp_min(1e-30)
            step[c] = round(float((2 * a / float(2 ** w - 1)).max()), 8)
        out.append({"arm": STATE["arm"], "emitted_bits": payload + 16 * n_scales, "n_scales": n_scales,
                    "n_channels": int(dm.shape[1]), "class_channels": chans, "class_step": step})
    STATE["rows"] += out
    return out

def instrument():
    """Replace the module-level name quant() looks up, keeping the one real quant."""
    real = fixed.quant
    def counted(k, dm, widths):
        audit(k, dm, widths); return real(k, dm, widths)
    fixed.quant = counted
    return real

def grid():
    n = fixed.SPEC["np"]
    return {k: (w if n == 64 else w[:-1] + [w[-1] - 1]) for k, w in fixed.WIDTHS.items()}

def profile(model, prompts):
    E = np.zeros((fixed.SPEC["nl"], fixed.SPEC["kv"], fixed.SPEC["np"]))
    for ids in prompts[:2]:
        fixed.CAP.clear(); fixed.forward(model, ids, capture=True)
        for L in range(fixed.SPEC["nl"]):
            k = fixed.CAP[L][1][0].float().reshape(fixed.SPEC["kv"], -1, fixed.SPEC["np"], 2)
            E[L] += k.square().sum(-1).mean(1).cpu().numpy() / 2
    return E

def audit_arm(E, name, widths, mode="energy", seed=1):
    STATE["arm"] = name; STATE["rows"] = []
    a = fixed.arm(E, widths, mode, seed)
    fixed.forward(MODEL[0], PROMPTS[0], a, widths)
    heads = STATE["rows"]; per = fixed.bits(widths) * 2 * fixed.SPEC["np"]
    assert heads and all(r["emitted_bits"] == per for r in heads), (name, per, heads[:1])
    nar = min(min(r["class_channels"][c] for r in heads) for c in range(len(widths)))
    nar_w = widths[[min(r["class_channels"][c] for r in heads) for c in range(len(widths))].index(nar)]
    ns = heads[0]["n_scales"]; pay = per - 16 * ns
    return {"arm": name, "mode": mode, "widths": widths, "n_scales": ns, "bits_per_pair": per,
            "emitted_bits": heads[0]["emitted_bits"], "payload_bits": pay,
            "overhead_pct": round(100 * 16 * ns / pay, 4),
            "narrow_class": {"w": nar_w, "channels": nar, "pairs": nar // 2, "payload_bits": nar * nar_w},
            "heads": len(heads),
            "max_step": {str(c): max(r["class_step"][c] for r in heads if c in r["class_step"]) for c in range(len(widths))}}

def run(which):
    from transformers import AutoTokenizer, AutoModelForCausalLM
    global MODEL, PROMPTS
    hf = paths.get("osc15_hf_dir" if which == "qwen3" else "osc03_hf_dir")
    tok = AutoTokenizer.from_pretrained(hf)
    MODEL = [AutoModelForCausalLM.from_pretrained(hf, dtype=torch.float32, attn_implementation="eager").eval()]
    fixed.install(MODEL[0]); instrument()
    PROMPTS, emeta = obp.build_eval(tok); E = profile(MODEL[0], PROMPTS)
    g = grid(); out = paths.get_local("osc_band_qknorm_dir") + "/bytes-a00-7a3bd2b1-" + which
    os.makedirs(out, exist_ok=True)
    arms = [("energy_" + k, w, "energy", 1) for k, w in g.items()]
    arms += [("uniform_3p5", [3], "uniform", 1), ("uniform_2p0", [2], "uniform", 1), ("random_4p5", g["4p5"], "random", 7)]
    summary = [audit_arm(E, n, w, m, s) for n, w, m, s in arms]
    with open(out + "/cells.jsonl", "w") as f:
        for (n, w, m, s), summ in zip(arms, summary):
            rows = STATE["rows"]
            f.write(json.dumps({"event": "arm", "model": which, "np": fixed.SPEC["np"], "mode": m, **summ}) + "\n")
            for r in rows:
                f.write(json.dumps({"event": "head", "model": which, "arm": n, **r}) + "\n")
    json.dump({"model": which, "np": fixed.SPEC["np"], "eval": emeta, "arms": summary}, open(out + "/summary.json", "w"), indent=1)
    print(json.dumps(summary, indent=1))

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("which", choices=("qwen2", "qwen3")); run(p.parse_args().which)
