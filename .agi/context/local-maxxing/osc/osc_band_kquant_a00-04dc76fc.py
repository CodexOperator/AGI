#!/usr/bin/env python3
"""OSC.10 L3: RoPE-band energy as a PRECISION allocator for post-RoPE KEYS.

Quantizes ONLY the post-RoPE key tensor, inside apply_rotary_pos_emb and before
attention. Each KV head's 32 RoPE pairs (HF rotate_half pair p = dims p, p+32)
are ranked by OSC.03's profile_pooled summed over the head's 7 query heads and
split into K=4 classes by ENERGY; the highest-energy classes get the most bits
(never zero). One fp16 absmax scale per class per token per KV head, counted.

Controls at each matched average-bit point: UNIFORM (one integer width on every
pair) and RANDOM (same class sizes, energy ranking replaced by a permutation,
3 seeds). Plus the blockwise q4_0 key baseline (32-value blocks, 4.5 bits/elem).

Run: V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" nice -n 19 \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" .agi/context/local-maxxing/osc/osc_band_kquant.py
"""
import json, os, sys, time
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import paths
import osc_band_prune as obp     # OSC.04: build_eval, metrics, install, CAP, CUR
import osc_band_measure as obm   # OSC.03: head_var selftest (pairing contract)
torch.set_num_threads(4)

NPAIR, NHEAD, GROUP = 32, 14, 7
AGENT = "a00-04dc76fc"
SEEDS = [1, 2, 3]
# tag: (K=4 energy class sizes, widths, (uniform classes, uniform width))
POINTS = {"3p5": ([4, 4, 8, 16], [4, 4, 2, 2], (2, 3)),
          "3p0": ([4, 4, 8, 16], [4, 4, 2, 1], (4, 2)),
          "2p5": ([4, 4, 8, 16], [2, 2, 2, 1], (2, 2))}
STATE, CAP = {"dm": None, "w": None, "bw": False}, {}


def avg_bits(sizes, widths, nscale):
    """Bits per KEY ELEMENT for one KV head / one token, scales counted.
    sum over classes of n_pairs*2 elements * width, plus nscale fp16 scales."""
    return (sum(2 * n * w for n, w in zip(sizes, widths)) + nscale * 16) / 64.0


def quant(kk, dimcls, widths):
    """kk (B,2,T,64), dimcls (2,64) class id per dim. Per class per (head,token)
    absmax a, then 2**w symmetric levels spanning [-a,a] (nearest level).
    Signed range realised symmetrically so w=1 stays meaningful (+-a, sign);
    a two's-complement [-2**(w-1), 2**(w-1)-1] collapses at w=1. Recorded."""
    out = torch.empty_like(kk)
    for h in range(dimcls.shape[0]):
        for c, w in enumerate(widths):
            d = (dimcls[h] == c).nonzero(as_tuple=True)[0]
            x = kk[:, h, :, d]
            a = x.abs().amax(-1, keepdim=True).clamp_min(1e-30)
            n = float(2 ** w - 1)
            j = torch.round((x / a + 1.0) * (n / 2.0)).clamp_(0.0, n)
            out[:, h, :, d] = (j * (2.0 / n) - 1.0) * a
    return out


def quant_bw(kk):
    """q4_0 analog: 32-element blocks, ONE fp16 absmax scale, [-8,7] -> 4.5."""
    v = kk.reshape(*kk.shape[:-1], 2, 32)
    a = v.abs().amax(-1, keepdim=True).clamp_min(1e-30).half().float()
    return (torch.round(v / a).clamp_(-8, 7) * a).reshape(kk.shape)


def selftest_bits():
    b = avg_bits(*POINTS["3p5"][:2], 4)
    no_scale = sum(2 * n * w for n, w in zip(*POINTS["3p5"][:2])) / 64.0
    print(f"selftest bits: with scales={b} without={no_scale}")
    return b == 3.5 and abs(no_scale - 2.5) < 1e-12


def selftest_pairing():
    """Our class map puts dims (p, p+32) in one class; the consecutive-dims map
    (2p, 2p+1) must FAIL that invariant AND change the reconstruction."""
    good = np.concatenate([np.arange(NPAIR) % 4, np.arange(NPAIR) % 4])
    bad = np.repeat(np.array([0] * 4 + [1] * 4 + [2] * 8 + [3] * 16), 2)  # (2p, 2p+1)
    g = torch.Generator().manual_seed(0)
    x = torch.randn(1, 2, 4, 64, generator=g)
    ok = [bool((good[:32] == good[32:]).all()),
          bool(not (bad[:32] == bad[32:]).all()),
          not torch.equal(quant(x, torch.from_numpy(np.stack([good, good])), [4, 4, 2, 2]),
                          quant(x, torch.from_numpy(np.stack([bad, bad])), [4, 4, 2, 2]))]
    print(f"selftest pairing: ours-shares-pair={ok[0]} consecutive-fails={ok[1]} "
          f"quant-differs={ok[2]}")
    return all(ok)


def make_arm(E, sizes, widths, rng=None, by_energy=True):
    """E (24,2,32) pair energies -> per-layer dimcls (2,64) [+ widths]."""
    dm = []
    for L in range(24):
        rows = []
        for k in range(2):
            order = np.argsort(-E[L, k]) if by_energy else np.arange(NPAIR)
            if rng is not None:
                order = rng.permutation(NPAIR)
            pc, i = np.empty(NPAIR, np.int64), 0
            for c, n in enumerate(sizes):
                pc[order[i:i + n]] = c
                i += n
            rows.append(np.concatenate([pc, pc]))
        dm.append(torch.from_numpy(np.stack(rows)))
    return dm, list(widths)


def install(model):
    import transformers.models.qwen2.modeling_qwen2 as M
    obp.install(model)                       # reuses OSC.04's layer tracker (CUR)
    inner, eaf = M.apply_rotary_pos_emb, M.eager_attention_forward

    def rope(q, k, cos, sin, unsqueeze_dim=1):
        qq, kk = inner(q, k, cos, sin, unsqueeze_dim)
        L = obp.CUR["l"]
        if STATE["bw"]:
            kk = quant_bw(kk)
        elif STATE["dm"] is not None:
            kk = quant(kk, STATE["dm"][L], STATE["w"])
        return qq, kk

    def attn(module, query, key, value, *a, **kw):
        if getattr(module, "layer_idx", None) == 0:
            CAP["q_attn"], CAP["k_attn"] = query.detach().clone(), key.detach().clone()
        return eaf(module, query, key, value, *a, **kw)

    M.apply_rotary_pos_emb = rope
    M.ALL_ATTENTION_FUNCTIONS["eager"] = attn


def logits(model, ids, arm):
    STATE["dm"], STATE["w"], STATE["bw"] = arm
    it = torch.as_tensor(ids, dtype=torch.long).reshape(1, -1)
    with torch.no_grad():
        return model(it).logits[0]


def wait_mem(need_mb=2000):
    while True:
        kb = [int(l.split()[1]) for l in open("/proc/meminfo")
              if l.startswith("MemAvailable")][0]
        if kb // 1024 >= need_mb:
            return
        print("mem low, waiting 60s", flush=True)
        time.sleep(60)


def main():
    t0 = time.time()
    for b, fn in [("bits", selftest_bits()), ("pairing", selftest_pairing()),
                  ("head_var", obm.selftest_head_var())]:
        assert fn, f"selftest {b} FAILED"
    prov = json.load(open(os.path.join(paths.get_local("osc_band_dir"), "provenance.json")))
    pf = os.path.join(paths.get_local("osc_band_dir"), "profiles.json")
    psha = obp.sha(pf)
    rever = {f: (obp.sha(os.path.join(obp.HF, f)) == h)
             for f, h in prov["hf_sha256"].items()}
    print("profiles sha:", psha, "| model sha re-verify:", rever, flush=True)
    assert all(rever.values()) and psha == "e80ec2772b1845f27a860d698e398b527fd4233141820ccbc27aecb98aab12a3"

    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(obp.HF)
    model = AutoModelForCausalLM.from_pretrained(
        obp.HF, dtype=torch.float32, attn_implementation="eager").eval()
    install(model)
    prompts, eval_meta = obp.build_eval(tok)
    heads = json.load(open(pf))["heads"]
    E = np.array([[np.array([heads[f"L{L}H{k*GROUP+g}"]["profile_pooled"]
                             for g in range(GROUP)]).sum(0) for k in range(2)]
                  for L in range(24)])

    ids = prompts[0]
    ref0 = logits(model, ids, (None, None, False))
    ref0p = torch.log_softmax(ref0.float(), -1)
    dm16 = [torch.zeros(2, 64, dtype=torch.int64)] * 24
    l16 = logits(model, ids, (dm16, [16], False))
    d16 = float((l16 - ref0).abs().max())
    a16, kl16 = obp.metrics(ref0p, l16)
    dm2 = make_arm(E, [32], [2])[0]
    logits(model, ids, (dm2, [2], False))
    kq = quant(obp.CAP["k"], dm2[0], [2])
    hook = {"q_untouched": bool(torch.equal(obp.CAP["q"], CAP["q_attn"])),
            "attn_k_is_quant_postrope_k": bool(torch.equal(CAP["k_attn"], kq)),
            "quant_changes_k": bool(not torch.equal(obp.CAP["k"], CAP["k_attn"]))}
    print(f"selftest 16bit: max abs logit diff={d16:.3e} agree={a16} KL={kl16:.2e} | hook: {hook}",
          flush=True)
    assert d16 < 0.5 and a16 == 1.0 and kl16 < 1e-3 and all(hook.values()), (d16, a16, kl16, hook)
    STATE["dm"] = None

    arms = {"bw4": (None, None, True)}
    for tag, (sizes, widths, (cu, wu)) in POINTS.items():
        arms[f"energy_{tag}"] = (*make_arm(E, sizes, widths), False)
        arms[f"uniform_{tag}"] = (*make_arm(E, [NPAIR // cu] * cu, [wu] * cu,
                                            by_energy=False), False)
        for s in SEEDS:
            arms[f"rand_{tag}_s{s}"] = (*make_arm(E, sizes, widths,
                                                 np.random.default_rng(s)), False)
    bits = {f"energy_{t}": avg_bits(*POINTS[t][:2], 4) for t in POINTS}
    bits.update({f"uniform_{t}": avg_bits([NPAIR // POINTS[t][2][0]] * POINTS[t][2][0],
                                          [POINTS[t][2][1]] * POINTS[t][2][0],
                                          POINTS[t][2][0]) for t in POINTS})
    bits.update({f"rand_{t}_s{s}": bits[f"energy_{t}"] for t in POINTS for s in SEEDS})
    bits["bw4"] = 4.5
    print("arms:", json.dumps({k: round(v, 4) for k, v in bits.items()}), flush=True)

    agg = {k: {"agree": 0.0, "kl": 0.0} for k in arms}
    for pi, ids in enumerate(prompts):
        wait_mem()
        ref = logits(model, ids, (None, None, False))
        ref_logp = torch.log_softmax(ref.float(), -1)
        for k, arm in arms.items():
            a, kl = obp.metrics(ref_logp, logits(model, ids, arm))
            agg[k]["agree"] += a / len(prompts)
            agg[k]["kl"] += kl / len(prompts)
        print(f"prompt {pi + 1}/{len(prompts)} {time.time() - t0:.0f}s", flush=True)

    res = {k: {"agree": round(agg[k]["agree"], 6), "kl": round(agg[k]["kl"], 6),
               "bits": round(bits[k], 6)} for k in arms}
    out = {}
    for t in POINTS:
        en = res[f"energy_{t}"]
        hits = {k: (res[k]["agree"] >= 0.98 and res[k]["kl"] <= 0.02)
                for k in [f"energy_{t}", f"uniform_{t}"] +
                [f"rand_{t}_s{s}" for s in SEEDS]}
        out[t] = {"energy": en, "uniform": res[f"uniform_{t}"],
                  "dot_ok_A": bool(hits[f"energy_{t}"]),
                  **{f"delta_energy_minus_uniform_{m}": round(en[m] - res[f"uniform_{t}"][m], 6)
                     for m in ("agree", "kl")},
                  "delta_energy_minus_uniform_bits": round(en["bits"] - res[f"uniform_{t}"]["bits"], 6),
                  "random": {f"s{s}": res[f"rand_{t}_s{s}"] for s in SEEDS},
                  "delta_energy_minus_rand_mean": {
                      m: round(en[m] - float(np.mean([res[f"rand_{t}_s{s}"][m]
                                                      for s in SEEDS])), 6)
                      for m in ("agree", "kl")},
                  "hits": hits}
    hold_both = [k for k, r in res.items() if r["agree"] >= 0.98 and r["kl"] <= 0.02]
    d = paths.get_local("osc_band_kquant_dir")
    od = os.path.join(d, AGENT)
    os.makedirs(od, exist_ok=True)
    json.dump({"res": res, "points": out, "bits": bits}, open(os.path.join(od, "raw.json"), "w"), indent=1)
    json.dump({"meta": {"model": "Qwen/Qwen2.5-0.5B-Instruct (rev %s)" % obp.REV,
                        "dtype": "float32", "eval": eval_meta, "K": 4,
                        "selftest_16bit": {"max_abs_logit_diff": d16, "agree": a16,
                                           "kl": kl16}, "hook": hook,
                        "profiles_sha256": psha, "sha_reverify": rever,
                        "t_s": round(time.time() - t0, 1)},
               "settings": res, "points": out, "hold_both_bars": hold_both},
              open(os.path.join(od, "results.json"), "w"), indent=1)
    json.dump({"profiles_sha256": psha, "sha_reverify": rever,
               "weights": os.path.join(obp.HF, "model.safetensors"),
               "humaneval_sha256": obp.sha(paths.get_local("humaneval_file")),
               "eval": eval_meta},
              open(os.path.join(od, "provenance.json"), "w"), indent=1)
    md = ["# OSC.10 L3: RoPE-band-energy key bit allocation (K=4)", "",
          "16-bit keys: max abs logit diff %.3e, agree %.4f, KL %.2e. Hook: %s"
          % (d16, a16, kl16, hook), "",
          "| arm | avg bits/elem | agree | mean KL |", "|---|---|---|---|"]
    for k in sorted(res):
        md.append(f"| {k} | {res[k]['bits']} | {res[k]['agree']} | {res[k]['kl']} |")
    md += ["", "| point | A energy holds both | dAgree E-U | dKL E-U | dAgree E-R | dKL E-R |",
           "|---|---|---|---|---|---|"]
    for t in POINTS:
        p = out[t]
        md.append(f"| {t} | {p['dot_ok_A']} | {p['delta_energy_minus_uniform_agree']} | "
                  f"{p['delta_energy_minus_uniform_kl']} | "
                  f"{p['delta_energy_minus_rand_mean']['agree']} | "
                  f"{p['delta_energy_minus_rand_mean']['kl']} |")
    md += ["", f"arms holding agree>=0.98 and KL<=0.02: {hold_both}", ""]
    open(os.path.join(od, "summary.md"), "w").write("\n".join(md))
    print(json.dumps({"points": out, "hold_both_bars": hold_both}, indent=1))


if __name__ == "__main__":
    main()
