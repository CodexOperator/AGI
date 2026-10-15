#!/usr/bin/env python3
"""OSC-CTL.10 control arm: post-RoPE KEY quantization by RoPE-band energy.

Run: V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" nice -n 19 \
       "$(python3 .agi/context/local-maxxing/paths.py ml_python)" .agi/context/local-maxxing/osc/osc_band_kquant_a00-527993c5.py

Only the post-RoPE keys are quantized (queries/values untouched). Each KV head's
32 HF rotate_half pairs (p = dims (p, p+32)) are ranked by OSC.03's profile_pooled
summed over the head's 7 query heads; a class partition by that rank gets one
integer width per class, each class absmax-scaled per token per KV head. Arms:
energy / uniform / random-same-sizes / blockwise4, measured against the
unquantized model with OSC.04's held-out 4096-token eval and its metrics().
Selftests: --selftest (see the sibling *_test.py). Out-of-repo roots are resolved through paths.py.
"""
import hashlib
import itertools
import json
import os
import sys
import time

import numpy as np
import torch

torch.set_num_threads(4)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import paths
import osc_band_measure as obm
import osc_band_prune as obp

HF, REV = obp.HF, obp.REV
NLAYER, NHEAD, NPAIR, GROUP, KVD = 24, 14, 32, 7, 2
WIDTHS = (2, 3, 4, 5)
BUDGETS = (3.5, 3.25, 3.0, 2.75, 2.5, 2.25)
PROF_SHA = "e80ec2772b1845f27a860d698e398b527fd4233141820ccbc27aecb98aab12a3"
ALLOC, CUR = {"a": None}, {"l": -1}
CANDS = []


def sha(p):
    return obp.sha(p)


def pair_view(k):
    """HF rotate_half pairs: pair p = dims (p, p+32). -> [..., seq, 32, 2]"""
    return torch.stack([k[..., :NPAIR], k[..., NPAIR:]], dim=-1)


def quantize_k(k, cls, widths):
    """Round-to-nearest absmax per class, dequantized; k: [..., seq, 64]."""
    pv = pair_view(k)
    out = torch.empty_like(pv)
    for c, w in enumerate(widths):
        idx = [p for p in range(NPAIR) if cls[p] == c]
        blk = pv[..., idx, :]
        scale = blk.abs().amax(dim=(-1, -2), keepdim=True).clamp_min(1e-8)
        hi = (1 << (w - 1)) - 1
        out[..., idx, :] = torch.clamp(torch.round(blk / scale * hi), -(hi + 1), hi) / hi * scale
    return torch.cat([out[..., 0], out[..., 1]], dim=-1)


def blockwise4(k, w=4):
    """Plain blockwise: 32-value contiguous blocks, one fp16 scale each."""
    pv = pair_view(k)
    out = torch.empty_like(pv)
    hi = (1 << (w - 1)) - 1
    for e in (0, 1):
        blk = pv[..., e]
        scale = blk.abs().amax(-1, keepdim=True).clamp_min(1e-8)
        out[..., e] = torch.clamp(torch.round(blk / scale * hi), -(hi + 1), hi) / hi * scale
    return torch.cat([out[..., 0], out[..., 1]], dim=-1)


def quantize_heads(k, alloc):
    """k: [batch, KVD, seq, 64]; alloc: per-KV list of (mode, cls, widths)."""
    out = torch.empty_like(k)
    for kv, (mode, cls, widths) in enumerate(alloc):
        out[:, kv] = quantize_k(k[:, kv], cls, widths) if mode == "pair" \
            else blockwise4(k[:, kv], widths[0])
    return out


def make_rope(orig):
    """Wrap apply_rotary_pos_emb: quantize the k it returns, never q."""
    def rope(q, k, cos, sin, unsqueeze_dim=1):
        qq, kk = orig(q, k, cos, sin, unsqueeze_dim)
        a = ALLOC["a"]
        if a is not None:
            kk = quantize_heads(kk, a[CUR["l"]])
        return qq, kk
    return rope


def install(model):
    import transformers.models.qwen2.modeling_qwen2 as M
    M.apply_rotary_pos_emb = make_rope(M.apply_rotary_pos_emb)
    for i, layer in enumerate(model.model.layers):
        fwd = layer.self_attn.forward

        def wrap(f, i):
            def g(*a, **kw):
                CUR["l"] = i
                return f(*a, **kw)
            return g
        layer.self_attn.forward = wrap(fwd, i)


def comp(n, k):
    if k == 1:
        yield (n,)
        return
    for i in range(1, n - k + 2):
        for r in comp(n - i, k - 1):
            yield (i,) + r


def candidates():
    out = []
    for C in (1, 2, 3):
        for s in comp(NPAIR, C):
            for w in itertools.combinations_with_replacement(WIDTHS, C):
                w = tuple(sorted(w, reverse=True))
                data = sum(a * b for a, b in zip(w, s))
                out.append({"C": C, "sizes": s, "widths": w, "data": data / 32.0,
                            "bits": data / 32.0 + 0.25 * C})
    return out


def best_cand(B):
    """Largest avg_bits <= B; ties -> larger data, fewer classes, more spread
    (concentrate precision on the top rank), most balanced, then sizes."""
    best = None
    for c in CANDS:
        if c["bits"] > B + 1e-12:
            continue
        key = (c["bits"], c["data"], -c["C"], max(c["widths"]),
               -max(c["sizes"]), c["widths"], c["sizes"])
        if best is None or key > best[0]:
            best = (key, c)
    return best[1] if best is not None else None


def energy_alloc(cand, prof):
    order = np.argsort(-prof)
    cls = np.empty(NPAIR, dtype=np.int64)
    r = 0
    for ci, s in enumerate(cand["sizes"]):
        cls[order[r:r + s]] = ci
        r += s
    return ("pair", cls, list(cand["widths"]))


def perm_cls(a, rng):
    """Same class SIZES, pairs assigned by a random permutation."""
    mode, cls, widths = a
    p = rng.permutation(NPAIR)
    nc = np.empty_like(cls)
    nc[p] = cls
    return (mode, nc, list(widths))


def uniform(w):
    return [[("pair", np.zeros(NPAIR, dtype=np.int64), [w]) for _ in range(KVD)]
            for _ in range(NLAYER)]


def alloc_data_bits(alloc):
    vals = []
    for layer in alloc:
        for mode, cls, ws in layer:
            vals.append(4.0 if mode == "block" else
                        sum(ws[cls[p]] for p in range(NPAIR)) / 32.0)
    return float(np.mean(vals))


def build_arms(kprof):
    arms = {}
    for B in BUDGETS:
        cd = best_cand(B)
        e = [[energy_alloc(cd, kprof[L, kv]) for kv in range(KVD)]
             for L in range(NLAYER)]
        arms["energy_%s" % B] = e
        for s in (1, 2, 3):
            rng = np.random.default_rng(s)
            arms["random_%s_s%d" % (B, s)] = [
                [perm_cls(e[L][kv], rng) for kv in range(KVD)] for L in range(NLAYER)]
        w = int(np.floor(cd["data"] + 0.5 - 1e-9))
        arms["umatch_%s" % B] = uniform(min(5, max(2, w)))
        arms["ubudget_%s" % B] = uniform(min(5, max(2, int(np.floor(B - 0.25)))))
    for w in WIDTHS:
        arms["uniform_w%d" % w] = uniform(w)
    arms["blockwise4"] = [[("block", None, [4]) for _ in range(KVD)]
                          for _ in range(NLAYER)]
    return arms


def alloc_key(alloc):
    return tuple(tuple((mode, tuple(cls) if cls is not None else None, tuple(ws))
                       for mode, cls, ws in layer) for layer in alloc)


def arm_meta(alloc):
    """avg_bits (= data + 16*C/64, mean over layers/KV heads) and C."""
    bits, cs = [], []
    for layer in alloc:
        for mode, cls, ws in layer:
            if mode == "block":
                C, data = 2, 4.0
            else:
                C = len(ws)
                data = sum(ws[cls[p]] for p in range(NPAIR)) / 32.0
            bits.append(data + 0.25 * C)
            cs.append(C)
    return float(np.mean(bits)), float(np.mean(cs))


def load_profiles():
    heads = json.load(open(os.path.join(paths.get_local("osc_band_dir"), "profiles.json")))["heads"]
    kprof = np.zeros((NLAYER, KVD, NPAIR))
    for L in range(NLAYER):
        for kv in range(KVD):
            for j in range(GROUP):
                v = np.array(heads["L%dH%d" % (L, GROUP * kv + j)]["profile_pooled"],
                             dtype=np.float64)
                kprof[L, kv] += v / v.sum()
            kprof[L, kv] /= kprof[L, kv].sum()
    return kprof


def verify_hashes():
    prov = json.load(open(os.path.join(paths.get_local("osc_band_dir"), "provenance.json")))
    rever = {f: sha(os.path.join(HF, f)) == h for f, h in prov["hf_sha256"].items()}
    assert all(rever.values()), rever
    prof = sha(os.path.join(paths.get_local("osc_band_dir"), "profiles.json"))
    assert prof == PROF_SHA, prof
    return prov, rever, prof


def selftest():
    global CANDS
    CANDS = candidates()
    assert obm.selftest_head_var(), "hop1 head_var selftest FAILED"
    torch.manual_seed(0)
    q, k = torch.randn(1, 2, 8, 64), torch.randn(1, 2, 8, 64)
    ref = q @ k.transpose(-1, -2)
    kq = quantize_heads(k, [[("pair", np.zeros(NPAIR, dtype=np.int64), [16])] * KVD])
    rel = float((q @ kq.transpose(-1, -2) - ref).abs().max() / ref.abs().max())
    assert rel < 1e-3, rel
    c16 = [c for c in CANDS if c["C"] == 1 and c["widths"] == (4,) and c["sizes"] == (32,)][0]
    assert abs(c16["bits"] - (c16["data"] + 0.25)) < 1e-12
    c2 = [c for c in CANDS if c["C"] == 2 and c["sizes"] == (16, 16) and c["widths"] == (3, 2)][0]
    assert abs(c2["bits"] - (2 * (3 * 16 + 2 * 16) + 16 * 2) / 64.0) < 1e-12, c2
    v = torch.arange(64).float().view(1, 1, 1, 64)
    pv = pair_view(v)
    assert all(float(pv[0, 0, 0, p, 0]) == p and float(pv[0, 0, 0, p, 1]) == p + 32
               for p in range(NPAIR))
    verify_hashes()
    print("selftest: head_var PASS; 16-bit rel %.2e; bits C1/C2 PASS; pairing PASS; sha PASS" % rel)
    return True


def metrics(ref_logp, logits):
    return obp.metrics(ref_logp, logits)


def main():
    global CANDS
    CANDS = candidates()
    t0 = time.time()
    prov, rever, prof_sha = verify_hashes()
    print("sha re-verify:", rever)
    kprof = load_profiles()
    arms = build_arms(kprof)
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(HF)
    model = AutoModelForCausalLM.from_pretrained(
        HF, dtype=torch.float32, attn_implementation="eager").eval()
    install(model)
    assert obm.selftest_head_var(), "hop1 head_var selftest FAILED"
    prompts, eval_meta = obp.build_eval(tok)
    print("eval:", json.dumps(eval_meta))
    uniq, alias = {}, {}
    for name, alloc in arms.items():
        key = alloc_key(alloc)
        uniq.setdefault(key, alloc)
        alias[name] = key
    agg = {k: {"agree": 0.0, "kl": 0.0} for k in uniq}
    for pi, ids in enumerate(prompts):
        it = torch.tensor([ids])
        ALLOC["a"] = None
        with torch.no_grad():
            ref = torch.log_softmax(model(it).logits[0].float(), -1)
        for key, alloc in uniq.items():
            ALLOC["a"] = alloc
            with torch.no_grad():
                lg = model(it).logits[0]
            a, kl = metrics(ref, lg)
            agg[key]["agree"] += a / len(prompts)
            agg[key]["kl"] += kl / len(prompts)
        print("prompt %d/%d %.0fs" % (pi + 1, len(prompts), time.time() - t0), flush=True)
    res = {}
    for name, key in alias.items():
        bits, C = arm_meta(uniq[key])
        res[name] = {"agree": round(agg[key]["agree"], 6), "kl": round(agg[key]["kl"], 6),
                     "avg_bits": round(bits, 4), "avg_data_bits": round(alloc_data_bits(uniq[key]), 4),
                     "C": C}
    return finish(res, eval_meta, rever, prof_sha, prov, arms, t0)


def verdicts(res):
    out = {}
    for B in BUDGETS:
        e, u, r = res["energy_%s" % B], res["umatch_%s" % B], [
            res["random_%s_s%d" % (B, s)] for s in (1, 2, 3)]
        rm = {m: float(np.mean([x[m] for x in r])) for m in ("agree", "kl")}
        out[str(B)] = {
            "a_energy_holds": e["agree"] >= 0.98 and e["kl"] <= 0.02,
            "b_beats_uniform_matched": e["agree"] > u["agree"] and e["kl"] < u["kl"],
            "b_delta": {"agree": round(e["agree"] - u["agree"], 6),
                        "kl": round(e["kl"] - u["kl"], 6)},
            "c_beats_random_mean": e["agree"] > rm["agree"] and e["kl"] < rm["kl"],
            "c_random_mean": {m: round(rm[m], 6) for m in rm}}
    return out


def finish(res, eval_meta, rever, prof_sha, prov, arms, t0):
    outdir = os.path.join(paths.get_local("osc_band_kquant_dir"), "a00-527993c5")
    os.makedirs(outdir, exist_ok=True)
    v = verdicts(res)
    safe = [B for B in BUDGETS if res["energy_%s" % B]["agree"] >= 0.98
            and res["energy_%s" % B]["kl"] <= 0.02]
    ref_bits = [B for B in BUDGETS if res["umatch_%s" % B]["agree"] >= 0.98
                and res["umatch_%s" % B]["kl"] <= 0.02]
    out = {"meta": {"model": "Qwen/Qwen2.5-0.5B-Instruct", "revision": REV,
                    "dtype": "float32", "quantized": "post-RoPE keys only; q,v untouched",
                    "pairing": "HF rotate_half (p, p+32)", "budgets": list(BUDGETS),
                    "eval": eval_meta, "sha_reverify": rever, "profiles_sha256": prof_sha,
                    "t_s": round(time.time() - t0, 1)},
           "results": res, "falsifier_verdicts": v,
           "largest_safe_step": {"lowest_budget_holding_both_bars_energy": max(safe) if safe else None,
                                 "energy_holds": safe,
                                 "lowest_budget_holding_both_bars_uniform_matched": max(ref_bits) if ref_bits else None},
           "note_tie_break": "budget rule left ties open; ties -> larger data bits, fewer classes, "
                             "then most balanced sizes, then lexicographically largest sizes"}
    json.dump(out, open(os.path.join(outdir, "results.json"), "w"), indent=1)
    json.dump({"weights": os.path.join(HF, "model.safetensors"),
               "hf_sha256_verified": rever, "profiles_sha256": prof_sha,
               "eval": eval_meta, "t_s": round(time.time() - t0, 1)},
              open(os.path.join(outdir, "provenance.json"), "w"), indent=1)
    md = ["# OSC-CTL.10 kquant control arm a00-527993c5", "",
          "eval: %d prompts x 512 = %d tokens (OSC.04 build_eval, disjoint from hop 1)" % (
              eval_meta["n_prompts"], eval_meta["n_tokens"]),
          "bars: agree >= 0.98 and mean per-token KL <= 0.02", "",
          "| arm | avg_bits | avg_data_bits | C | agree | KL |", "|---|---|---|---|---|---|"]
    for name in sorted(res):
        r = res[name]
        md.append("| %s | %s | %s | %s | %s | %s |" % (
            name, r["avg_bits"], r["avg_data_bits"], r["C"], r["agree"], r["kl"]))
    md += ["", "## falsifier verdicts", json.dumps(v, indent=1),
           "", "## largest safe step", json.dumps(out["largest_safe_step"], indent=1), ""]
    open(os.path.join(outdir, "summary.md"), "w").write("\n".join(md))
    json.dump({"results": res, "falsifier_verdicts": v, "arms_keys": sorted(arms)},
              open(os.path.join(outdir, "raw.json"), "w"), indent=1)
    print(json.dumps(out["falsifier_verdicts"], indent=1))
    print("wrote", outdir)
    return out


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        main()
