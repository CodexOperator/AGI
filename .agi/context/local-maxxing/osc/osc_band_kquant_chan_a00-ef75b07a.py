#!/usr/bin/env python3
"""OSC.14 a00-ef75b07a: per-channel / bias-subtracted post-RoPE KEY scales at 3.5 bits vs token-absmax.
Run: V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" nice -n 19 \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" .agi/context/local-maxxing/osc/osc_band_kquant_chan_a00-ef75b07a.py"""
import importlib.util, json, os, sys, time
import numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); import paths
_f = importlib.util.spec_from_file_location("kq", os.path.join(HERE, "osc_band_kquant_a00-86466b78.py"))
kq = importlib.util.module_from_spec(_f); _f.loader.exec_module(kq); obp = kq.obp
torch.set_num_threads(4)
AGENT, SIZES, WIDTHS = "a00-ef75b07a", [4, 4, 8, 16], [4, 4, 2, 2]
CAPQ = {}

def deq(x, a, w):
    """kq.quant's own symmetric-level reconstruction, factored out."""
    n = float(2 ** w - 1)
    return (torch.round((x / a + 1.0) * (n / 2.0)).clamp_(0.0, n) * (2.0 / n) - 1.0) * a

def quant_chan(kk, dimcls, widths):
    """Arm 3: ONE absmax per (class, kv head, CHANNEL) -- reduce over TOKEN axis -2."""
    out = torch.empty_like(kk)
    for h in range(dimcls.shape[0]):
        for c, w in enumerate(widths):
            d = (dimcls[h] == c).nonzero(as_tuple=True)[0]; x = kk[:, h, :, d]
            a = x.abs().amax(-2, keepdim=True).clamp_min(1e-30); CAPQ["chan_a"] = a
            out[:, h, :, d] = deq(x, a, w)
    return out

def quant_bias(kk, dimcls, widths):
    """Arm 4: per-CHANNEL mean removed, then ordinary per-TOKEN absmax on the residual."""
    out = torch.empty_like(kk)
    for h in range(dimcls.shape[0]):
        for c, w in enumerate(widths):
            d = (dimcls[h] == c).nonzero(as_tuple=True)[0]; x = kk[:, h, :, d]
            b = x.mean(-2, keepdim=True); a = (x - b).abs().amax(-1, keepdim=True).clamp_min(1e-30)
            CAPQ["bias_b"], CAPQ["bias_a"] = b, a
            out[:, h, :, d] = b + deq(x - b, a, w)
    return out

def _route(kk, dimcls, widths):
    m = kq.STATE.get("mode")
    return (quant_chan(kk, dimcls, widths) if m == "chan" else
            quant_bias(kk, dimcls, widths) if m == "bias" else _orig(kk, dimcls, widths))
_orig = kq.quant; kq.quant = _route   # rope() resolves the module global -> routes both new arms

def main():
    t0 = time.time()
    _x = importlib.util.spec_from_file_location("fx", os.path.join(HERE, "osc_band_kquant_chan_a00-ef75b07a_test.py"))
    fx = importlib.util.module_from_spec(_x); _x.loader.exec_module(fx)
    assert fx.fixture() and kq.selftest_bits() and kq.selftest_pairing() and kq.obm.selftest_head_var()
    prov = json.load(open(os.path.join(paths.get_local("osc_band_dir"), "provenance.json")))
    pf = os.path.join(paths.get_local("osc_band_dir"), "profiles.json"); psha = obp.sha(pf)
    rever = {f: (obp.sha(os.path.join(obp.HF, f)) == h) for f, h in prov["hf_sha256"].items()}
    assert all(rever.values()) and psha == "e80ec2772b1845f27a860d698e398b527fd4233141820ccbc27aecb98aab12a3"
    print("profiles sha:", psha, "| reverify:", rever, flush=True)
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(obp.HF)
    model = AutoModelForCausalLM.from_pretrained(obp.HF, dtype=torch.float32, attn_implementation="eager").eval()
    kq.install(model); prompts, eval_meta = obp.build_eval(tok)
    heads = json.load(open(pf))["heads"]
    E = np.array([[np.array([heads[f"L{L}H{k*7+g}"]["profile_pooled"] for g in range(7)]).sum(0)
                   for k in range(2)] for L in range(24)])
    dm, w = kq.make_arm(E, SIZES, WIDTHS); dm_u, w_u = kq.make_arm(E, [16, 16], [3, 3], by_energy=False)
    ids = prompts[0]; ref0 = kq.logits(model, ids, (None, None, False))
    l16 = kq.logits(model, ids, ([torch.zeros(2, 64, dtype=torch.int64)] * 24, [16], False))
    d16 = float((l16 - ref0).abs().max()); a16, kl16 = obp.metrics(torch.log_softmax(ref0.float(), -1), l16)
    kq.STATE["mode"] = "chan"; kq.logits(model, ids, (dm, w, False))
    hook_c = bool(torch.equal(kq.CAP["k_attn"], quant_chan(obp.CAP["k"], dm[0], w)))
    kq.STATE["mode"] = "bias"; kq.logits(model, ids, (dm, w, False))
    hook_b = bool(torch.equal(kq.CAP["k_attn"], quant_bias(obp.CAP["k"], dm[0], w)))
    print(f"16bit d={d16:.3e} agree={a16} KL={kl16:.2e} | hooks chan={hook_c} bias={hook_b}", flush=True)
    assert d16 < 0.5 and a16 == 1.0 and kl16 < 1e-3 and hook_c and hook_b
    kq.STATE["mode"] = None
    arms = {"token_absmax_3p5": (dm, w, False, None), "uniform_3p5": (dm_u, w_u, False, None),
            "per_channel_3p5": (dm, w, False, "chan"), "bias_subtracted_3p5": (dm, w, False, "bias")}
    bits = {k: kq.avg_bits(SIZES, WIDTHS, 4 if k != "bias_subtracted_3p5" else 8) for k in arms}
    bits["uniform_3p5"] = kq.avg_bits([16, 16], [3, 3], 2)
    print("arm bits (arm3 conservative nscale=4; arm4 +4 fp16/class):", json.dumps(bits), flush=True)
    assert bits["token_absmax_3p5"] == bits["uniform_3p5"] == bits["per_channel_3p5"] == 3.5
    outdir = os.path.join(paths.get_local("osc_band_kquant_0924_dir"), AGENT)
    os.makedirs(os.path.join(outdir, "bench"), exist_ok=True)
    bf = os.path.join(outdir, "bench", time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + ".jsonl")
    agg = {k: {"agree": 0.0, "kl": 0.0} for k in arms}
    for pi, ids in enumerate(prompts):
        kq.wait_mem(); ref_logp = torch.log_softmax(kq.logits(model, ids, (None, None, False)).float(), -1)
        for k, (d_, w_, b_, m_) in arms.items():
            kq.STATE["mode"] = m_; a, kl = obp.metrics(ref_logp, kq.logits(model, ids, (d_, w_, b_)))
            agg[k]["agree"] += a / len(prompts); agg[k]["kl"] += kl / len(prompts)
            with open(bf, "a") as f:  # persist every probe, never batched
                f.write(json.dumps({"prompt": pi, "arm": k, "agree": round(a, 6),
                                    "kl": round(kl, 6), "bits": bits[k]}) + "\n")
        print(f"prompt {pi+1}/{len(prompts)} {time.time()-t0:.0f}s", flush=True)
    res = {k: {"agree": round(agg[k]["agree"], 6), "kl": round(agg[k]["kl"], 6), "bits": bits[k]} for k in arms}
    base, ch, bi = res["token_absmax_3p5"], res["per_channel_3p5"], res["bias_subtracted_3p5"]
    clears = lambda v: bool(v["agree"] - base["agree"] > 0.10 and v["kl"] < 0.75 * base["kl"] and v["agree"] > 0.75)
    out = {"arms": res, "falsifier": "no variant clears BOTH (agree+0.10 vs token_absmax AND KL<0.75x) while agree>0.75",
           "delta_per_channel_minus_token_absmax": {m: round(ch[m]-base[m], 6) for m in ("agree", "kl")},
           "delta_bias_minus_token_absmax": {m: round(bi[m]-base[m], 6) for m in ("agree", "kl")},
           "per_channel_clears": clears(ch), "bias_clears": clears(bi),
           "agreement_gt_0p75": {k: bool(res[k]["agree"] > 0.75) for k in res},
           "meta": {"model": f"Qwen/Qwen2.5-0.5B-Instruct (rev {obp.REV})", "dtype": "float32", "eval": eval_meta,
                    "selftest_16bit": {"max_abs_logit_diff": d16, "agree": a16, "kl": kl16},
                    "hooks": {"per_channel": hook_c, "bias_subtracted": hook_b},
                    "bits_note": "arm3 charged nscale=4 like arm1 though shared across tokens (conservative); arm4 adds 4 fp16/class -> 4.5 nominal, not a 3.5-bit arm",
                    "profiles_sha256": psha, "sha_reverify": rever, "t_s": round(time.time()-t0, 1)}}
    json.dump(out, open(os.path.join(outdir, "raw.json"), "w"), indent=1)
    md = ["# OSC.14 per-channel / bias-subtracted key scales at 3.5 bits (a00-ef75b07a)", "",
          f"16-bit anchor d={d16:.3e} agree={a16} KL={kl16:.2e}; hooks chan={hook_c} bias={hook_b}", "",
          "| arm | bits | agree | mean KL | clears falsifier |", "|---|---|---|---|---|"]
    md += ["| %s | %s | %s | %s | %s |" % (k, res[k]["bits"], res[k]["agree"], res[k]["kl"],
           ("YES" if clears(res[k]) else "no") if k in ("per_channel_3p5", "bias_subtracted_3p5") else "-") for k in arms]
    md += ["", "delta per_channel - token_absmax: " + json.dumps(out["delta_per_channel_minus_token_absmax"]),
           "delta bias - token_absmax: " + json.dumps(out["delta_bias_minus_token_absmax"]),
           "arm4 is 4.5 nominal bits (bias charged extra), so only arm3 is a matched-3.5 comparison.", ""]
    open(os.path.join(outdir, "summary.md"), "w").write("\n".join(md))
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()