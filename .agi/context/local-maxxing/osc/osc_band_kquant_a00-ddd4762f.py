#!/usr/bin/env python3
"""OSC.10 L3: post-RoPE KEY quantization by RoPE-band energy vs uniform absmax.
Run: V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" nice -n 19 \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" .agi/context/local-maxxing/osc/osc_band_kquant_a00-ddd4762f.py
Per KV head, sum OSC.03's pooled band profiles over the head's 7 query heads,
rank the 32 HF rotate_half pairs (dims p, p+32) by energy, and give the top
pairs more bits. Each bit class is absmax-scaled per (kv head, token) with an
fp16 scale counted in the budget. Uniform absmax uses equal-size blocks at the
matched average bits; a random class assignment of the same sizes is the
control. Keys are quantized AFTER RoPE and before attention; q is untouched.
"""
import hashlib, json, os, sys, time
import numpy as np
import torch
torch.set_num_threads(8)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import paths
import osc_band_prune as obp   # OSC.04: build_eval + metrics, imported unchanged
HF = paths.get("osc03_hf_dir")
SCALE_BITS = 16
# (name, pair counts per class, bits per class): avg = (sum 2*s*b + 16*classes)/64
E = [("e30", [8, 24], [4, 2]),
     ("e35a", [4, 12, 16], [5, 3, 2]),
     ("e35b", [8, 8, 16], [4, 3, 2]),
     ("e45", [4, 12, 16], [6, 4, 3])]
U = [("u30", 16, 2), ("u35", 32, 3), ("u45", 32, 4)]
# supplementary sweep (--high) to bracket the safe budget: 6 / 8 / 12 bits per key
E_HI = [("e60", [4, 12, 16], [8, 6, 4]),
        ("e80", [4, 12, 16], [10, 8, 6]),
        ("e120", [4, 12, 16], [14, 12, 10])]
U_HI = [("u60", 16, 5), ("u80", 16, 7), ("u120", 16, 11)]
RAND_OF, SEEDS, Q16 = "e35a", [1, 2, 3], ("q16", 64, 16)
QCFG, CARP, CAP = {"fn": None}, {"l": -1}, {}
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
def avg_bits(sizes, bits):
    return (sum(s * 2 * b for s, b in zip(sizes, bits))
            + len(sizes) * SCALE_BITS) / 64.0
def uniform_bits(block, bits):
    return (block * bits + SCALE_BITS) / float(block)
def expand_classes(cls, npair):
    """HF rotate_half pairs are dims (p, p+npair), NOT consecutive dims."""
    e = np.zeros(2 * npair, dtype=np.int64)
    e[:npair], e[npair:] = cls, cls
    return e
def classed_from_rank(rank, sizes):
    """rank: pair indices best-first. Class 0 (most bits) takes the first slice."""
    cls = np.empty(len(rank), dtype=np.int64)
    i = 0
    for c, s in enumerate(sizes):
        cls[rank[i:i + s]] = c
        i += s
    return cls
def quant_classwise(kk, cls, bits, npair):
    out = kk.clone()
    for c, b in enumerate(bits):
        dims = np.where(expand_classes(cls, npair) == c)[0].tolist()
        if not dims:
            continue
        x = out[..., dims]
        qmax = 2 ** (b - 1) - 1
        scale = (x.abs().amax(-1, keepdim=True) / qmax).clamp_min(1e-12)
        out[..., dims] = torch.clamp(torch.round(x / scale), -qmax, qmax) * scale
    return out
def quant_block(kk, block, bits):
    out = kk.clone()
    qmax = 2 ** (bits - 1) - 1
    for s in range(0, kk.shape[-1], block):
        x = out[..., s:s + block]
        scale = (x.abs().amax(-1, keepdim=True) / qmax).clamp_min(1e-12)
        out[..., s:s + block] = torch.clamp(torch.round(x / scale), -qmax, qmax) * scale
    return out
def make_qfn(class_map=None, bits=None, block=None, ubits=None):
    """class_map: [layer][kv_head] -> class per pair (classwise); else blockwise."""
    if class_map is not None:
        def fn(kk, layer):
            npair = kk.shape[-1] // 2
            for h in range(kk.shape[1]):
                kk[:, h] = quant_classwise(kk[:, h].unsqueeze(0), class_map[layer][h],
                                           bits, npair)[0]
            return kk
    else:
        def fn(kk, layer):
            return quant_block(kk, block, ubits)
    return fn
def install(model):
    import transformers.models.qwen2.modeling_qwen2 as M
    orig = M.apply_rotary_pos_emb
    def rope(q, k, cos, sin, unsqueeze_dim=1):
        qq, kk = orig(q, k, cos, sin, unsqueeze_dim)
        if CARP["l"] == 0:
            CAP["q"] = qq.detach().float()
            CAP["k_pre"] = kk.detach().float()
        if QCFG["fn"] is not None:
            kk = QCFG["fn"](kk, CARP["l"])
        if CARP["l"] == 0:
            CAP["k_post"] = kk.detach().float()
        return qq, kk
    M.apply_rotary_pos_emb = rope
    for i, layer in enumerate(model.model.layers):
        fwd = layer.self_attn.forward
        def wrap(f, i):
            def g(*a, **kw):
                CARP["l"] = i
                return f(*a, **kw)
            return g
        layer.self_attn.forward = wrap(fwd, i)
def energy_profiles(profiles):
    """[24][2] normalised pair profiles, one per KV head (7 query heads summed)."""
    out = []
    for L in range(24):
        row = []
        for kv in range(2):
            p = np.sum([profiles[f"L{L}H{h}"]["profile_pooled"]
                        for h in range(kv * 7, kv * 7 + 7)], axis=0)
            row.append(p / p.sum())
        out.append(row)
    return out
def build_masks(prof_all, Es, Us, with_random=True):
    masks = {"q16": make_qfn(block=Q16[1], ubits=Q16[2])}
    for name, sizes, bits in Es:
        cm = [[classed_from_rank(np.argsort(-prof_all[L][kv]), sizes)
               for kv in range(2)] for L in range(24)]
        masks[name] = make_qfn(cm, bits=bits)
    for name, block, bits in Us:
        masks[name] = make_qfn(block=block, ubits=bits)
    if with_random:
        rsizes = dict((n, (s, b)) for n, s, b in Es)[RAND_OF]
        for s in SEEDS:
            rng = np.random.default_rng(s)
            cm = [[classed_from_rank(rng.permutation(32), rsizes[0])
                   for kv in range(2)] for L in range(24)]
            masks[f"rand_s{s}"] = make_qfn(cm, bits=rsizes[1])
    return masks
def main():
    t0 = time.time()
    HIGH = "--high" in sys.argv
    Es, Us = (E_HI, U_HI) if HIGH else (E, U)
    band = paths.get_local("osc_band_dir")
    prof_sha = sha(os.path.join(band, "profiles.json"))
    profiles = json.load(open(os.path.join(band, "profiles.json")))["heads"]
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(HF)
    model = AutoModelForCausalLM.from_pretrained(
        HF, dtype=torch.float32, attn_implementation="eager").eval()
    install(model)
    prompts, meta = obp.build_eval(tok)
    prof_all = energy_profiles(profiles)
    masks = build_masks(prof_all, Es, Us, with_random=not HIGH)
    budget = {n: round(avg_bits(s, b), 4) for n, s, b in Es}
    budget.update({n: round(uniform_bits(bl, b), 4) for n, bl, b in Us})
    budget[Q16[0]] = round(uniform_bits(Q16[1], Q16[2]), 4)
    agg = {k: {"agree": 0.0, "kl": 0.0} for k in masks}
    for pi, ids in enumerate(prompts):
        it = torch.tensor([ids])
        QCFG["fn"] = None
        with torch.no_grad():
            ref_logp = torch.log_softmax(model(it).logits[0].float(), -1)
        for k, fn in masks.items():
            QCFG["fn"] = fn
            with torch.no_grad():
                lg = model(it).logits[0]
            a, kl = obp.metrics(ref_logp, lg)
            agg[k]["agree"] += a / len(prompts)
            agg[k]["kl"] += kl / len(prompts)
        print(f"prompt {pi + 1}/{len(prompts)} {time.time() - t0:.0f}s", flush=True)
    out = {"meta": {"model": "Qwen/Qwen2.5-0.5B-Instruct", "dtype": "float32",
                    "target": "keys only, post-RoPE (p,p+32) band-energy bit classes",
                    "scale": "fp16 absmax per (kv head, token, class); 16 bits counted",
                    "eval": meta, "profiles_sha256": prof_sha,
                    "t_s": round(time.time() - t0, 1)},
           "budget_bits": budget,
           "settings": {k: {"agree": round(v["agree"], 6), "kl": round(v["kl"], 6)}
                        for k, v in agg.items()}}
    q16_ok = agg["q16"]["agree"] >= 0.999 and agg["q16"]["kl"] <= 1e-4
    out["q16_anchor_ok"] = bool(q16_ok)
    if not HIGH:
        e35 = {"agree": min(agg["e35a"]["agree"], agg["e35b"]["agree"]),
               "kl": max(agg["e35a"]["kl"], agg["e35b"]["kl"])}
        u35 = agg["u35"]
        out["at_3p5"] = {
            "energy_pass": bool(e35["agree"] >= 0.98 and e35["kl"] <= 0.02),
            "energy_agree": round(e35["agree"], 6), "energy_kl": round(e35["kl"], 6),
            "uniform_agree": round(u35["agree"], 6), "uniform_kl": round(u35["kl"], 6),
            "beats_uniform_both": bool(e35["agree"] > u35["agree"] and e35["kl"] < u35["kl"])}
        rc = {s: agg[f"rand_s{s}"]["agree"] for s in SEEDS}
        out["random_e35a"] = {"agree": {str(s): round(rc[s], 6) for s in SEEDS},
                              "mean_agree": round(float(np.mean(list(rc.values()))), 6),
                              "energy_beats_random": bool(agg["e35a"]["agree"] > np.mean(list(rc.values())))}
    hold = {n: bool(agg[n]["agree"] >= 0.98 and agg[n]["kl"] <= 0.02)
            for n in list(budget)}
    out["both_bars"] = hold
    out["lowest_bits_both_hold"] = min([n for n in hold if hold[n]],
                                       key=lambda n: budget[n], default=None)
    dst = os.path.join(paths.get_local("osc_band_kquant_dir"), "a00-ddd4762f")
    os.makedirs(dst, exist_ok=True)
    tag = "results_high.json" if HIGH else "results.json"
    json.dump(out, open(os.path.join(dst, tag), "w"), indent=1)
    json.dump({"profiles_sha256": prof_sha, "eval": meta,
               "weights": os.path.join(HF, "model.safetensors"),
               "humaneval_sha256": sha(paths.get_local("humaneval_file"))},
              open(os.path.join(dst, "provenance.json"), "w"), indent=1)
    md = ["# OSC.10 L3 band-energy KEY quantization", "",
          f"eval {meta['n_tokens']} tokens; budgets and metrics", "",
          "| setting | bits/el | agree | mean KL |", "|---|---|---|---|"]
    md += [f"| {k} | {budget.get(k, '-')} | {v['agree']} | {v['kl']} |"
           for k, v in out["settings"].items()]
    md += ["", f"q16 anchor ok: {q16_ok}"]
    if not HIGH:
        md += [f"at 3.5: {json.dumps(out['at_3p5'])}",
               f"random: {json.dumps(out['random_e35a'])}"]
    md += [f"lowest bits both hold: {out['lowest_bits_both_hold']}", ""]
    open(os.path.join(dst, tag.replace(".json", ".md")), "w").write("\n".join(md))
    print(json.dumps(out, indent=1))
    assert q16_ok, "q16 anchor failed -- quantizer/dequant path is broken"
if __name__ == "__main__":
    main()
