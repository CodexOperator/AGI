#!/usr/bin/env python3
"""OSC.13 a00-3d746bb5: a TRUE q4_0-analog blockwise uniform post-RoPE KEY baseline.

The sibling OSC.10 `quant_bw` is ternary: `round(v/a)` with a = per-block absmax
can only give -1/0/+1, so its 4.5-bit charge is a 3-level label. Here the
block-of-32, single-fp16-scale, 16-signed-level q4_0 pattern (GGML: d=a/8,
codes -8..7) is monkey-patched onto `kq.quant_bw` at call time; `kq.install`'s
rope() hook resolves that global, so the fix routes with no copied code.

Run: V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" nice -n 19 \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" .agi/context/local-maxxing/osc/osc_band_kquant_true_a00-3d746bb5.py
"""
import importlib.util, json, os, sys, time
import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import paths
_s = importlib.util.spec_from_file_location("kq", os.path.join(HERE, "osc_band_kquant_a00-86466b78.py"))
kq = importlib.util.module_from_spec(_s); _s.loader.exec_module(kq)
obp = kq.obp
torch.set_num_threads(4)
AGENT = "a00-3d746bb5"

def quant_bw_true(kk):
    """GGML q4_0: one fp16 absmax per 32-block, d=a/8, 16 codes -8..7."""
    v = kk.reshape(*kk.shape[:-1], 2, 32)
    a = v.abs().amax(-1, keepdim=True).clamp_min(1e-30).half().float()
    return (torch.round(v / (a / 8.0)).clamp_(-8.0, 7.0) * (a / 8.0)).reshape(kk.shape)

def levels(x):
    v = x.reshape(-1, 2, 32)
    return torch.tensor([len(z.unique()) for z in v.reshape(-1, 32)])

def fixture():
    """Hard-fail before any model load: 16 q4_0 levels, per-block scale, 4.5 bits."""
    x = torch.rand(1, 2, 4000, 64, generator=torch.Generator().manual_seed(11)) * 2 - 1
    d, old = levels(quant_bw_true(x)), levels(kq.quant_bw(x))
    shp = x.reshape(*x.shape[:-1], 2, 32).abs().amax(-1, keepdim=True).shape
    bits = (4 * 32 + 16) / 32
    print(f"fixture: levels median={int(d.median())} max={int(d.max())} dist={torch.bincount(d).tolist()} "
          f"| old ternary median={int(old.median())} max={int(old.max())} | scale={tuple(shp)} bits={bits}", flush=True)
    assert int(d.median()) >= 14 and int(d.max()) == 16, "true q4_0 does not reach 16 levels"
    assert int(old.max()) <= 3, "old quant_bw not ternary -- premise differs"
    assert shp[-2] == 2 and shp[-1] == 1, "scale is not one per 32-block"
    assert bits == 4.5 and kq.avg_bits([4, 4, 8, 16], [4, 4, 4, 3], 4) == 4.5

def main():
    t0 = time.time()
    fixture()
    kq.quant_bw = quant_bw_true
    assert kq.selftest_bits() and kq.selftest_pairing() and kq.obm.selftest_head_var()
    prov = json.load(open(os.path.join(paths.get_local("osc_band_dir"), "provenance.json")))
    pf = os.path.join(paths.get_local("osc_band_dir"), "profiles.json")
    rever = {f: (obp.sha(os.path.join(obp.HF, f)) == h) for f, h in prov["hf_sha256"].items()}
    psha = obp.sha(pf)
    print("profiles sha:", psha, "| reverify:", rever, flush=True)
    assert all(rever.values()) and psha == "e80ec2772b1845f27a860d698e398b527fd4233141820ccbc27aecb98aab12a3"
    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(obp.HF)
    model = AutoModelForCausalLM.from_pretrained(obp.HF, dtype=torch.float32, attn_implementation="eager").eval()
    kq.install(model)
    prompts, eval_meta = obp.build_eval(tok)
    heads = json.load(open(pf))["heads"]
    E = np.array([[np.array([heads[f"L{L}H{k*7+g}"]["profile_pooled"] for g in range(7)]).sum(0)
                   for k in range(2)] for L in range(24)])
    ids = prompts[0]
    ref0 = kq.logits(model, ids, (None, None, False))
    l16 = kq.logits(model, ids, ([torch.zeros(2, 64, dtype=torch.int64)] * 24, [16], False))
    d16 = float((l16 - ref0).abs().max()); a16, kl16 = obp.metrics(torch.log_softmax(ref0.float(), -1), l16)
    kq.logits(model, ids, (None, None, True))
    hook = bool(torch.equal(kq.CAP["k_attn"], quant_bw_true(obp.CAP["k"])))
    print(f"selftest 16bit: max abs logit diff={d16:.3e} agree={a16} KL={kl16:.2e} | patched-hook={hook}", flush=True)
    assert d16 < 0.5 and a16 == 1.0 and kl16 < 1e-3 and hook
    arms = {"true_uniform_4p5": (None, None, True),
            "energy_4p5": kq.make_arm(E, [4, 4, 8, 16], [4, 4, 4, 3]) + (False,)}
    bits = {"true_uniform_4p5": 4.5, "energy_4p5": kq.avg_bits([4, 4, 8, 16], [4, 4, 4, 3], 4)}
    assert bits == {"true_uniform_4p5": 4.5, "energy_4p5": 4.5}, bits
    outdir = os.path.join(paths.get_local("osc_band_q4_dir"), AGENT)
    os.makedirs(os.path.join(outdir, "bench"), exist_ok=True)
    benchf = os.path.join(outdir, "bench", time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + ".jsonl")
    agg = {k: {"agree": 0.0, "kl": 0.0} for k in arms}
    for pi, ids in enumerate(prompts):
        kq.wait_mem()
        ref_logp = torch.log_softmax(kq.logits(model, ids, (None, None, False)).float(), -1)
        for k, arm in arms.items():
            a, kl = obp.metrics(ref_logp, kq.logits(model, ids, arm))
            agg[k]["agree"] += a / len(prompts); agg[k]["kl"] += kl / len(prompts)
            with open(benchf, "a") as f:      # persist every probe, do not batch
                f.write(json.dumps({"prompt": pi, "arm": k, "agree": round(a, 6),
                                    "kl": round(kl, 6), "bits": bits[k]}) + "\n")
        print(f"prompt {pi + 1}/{len(prompts)} {time.time() - t0:.0f}s", flush=True)
    res = {k: {"agree": round(agg[k]["agree"], 6), "kl": round(agg[k]["kl"], 6), "bits": bits[k]} for k in arms}
    kqd = paths.get_local("osc_band_kquant_dir")
    old = json.load(open(os.path.join(kqd, "a00-86466b78", "results.json")))["settings"]["bw4"]
    ctl = json.load(open(os.path.join(kqd, "a00-ddd4762f", "results.json")))["settings"]["u45"]
    tu, en = res["true_uniform_4p5"], res["energy_4p5"]
    out = {"arms": res, "hits_both_bars": {k: bool(res[k]["agree"] >= 0.98 and res[k]["kl"] <= 0.02) for k in res},
           "old_bw4_ternary": old, "ddd4762f_u45_matched_control": ctl,
           "delta_vs_old_ternary_bw4": {m: round(tu[m] - old[m], 6) for m in ("agree", "kl")},
           "delta_vs_ddd4762f_u45_control": {m: round(tu[m] - ctl[m], 6) for m in ("agree", "kl")},
           "energy_minus_true_uniform": {m: round(en[m] - tu[m], 6) for m in ("agree", "kl")},
           "meta": {"model": f"Qwen/Qwen2.5-0.5B-Instruct (rev {obp.REV})", "dtype": "float32",
                    "eval": eval_meta, "selftest_16bit": {"max_abs_logit_diff": d16, "agree": a16, "kl": kl16},
                    "patched_hook": hook, "profiles_sha256": psha, "sha_reverify": rever,
                    "t_s": round(time.time() - t0, 1)}}
    json.dump(out, open(os.path.join(outdir, "raw.json"), "w"), indent=1)
    md = ["# true q4_0-analog post-RoPE key baseline (a00-3d746bb5)", "",
          f"16-bit anchor: max abs logit diff {d16:.3e}, agree {a16}, KL {kl16:.2e}; patched-hook {hook}.", "",
          "| arm | bits | agree | mean KL | both bars |", "|---|---|---|---|---|"]
    md += [f"| {k} | {res[k]['bits']} | {res[k]['agree']} | {res[k]['kl']} | {out['hits_both_bars'][k]} |" for k in res]
    md += ["", f"vs OLD ternary bw4 {old}: {out['delta_vs_old_ternary_bw4']}",
           f"vs ddd4762f u45 matched control {ctl}: {out['delta_vs_ddd4762f_u45_control']}",
           f"energy minus true uniform: {out['energy_minus_true_uniform']}", ""]
    open(os.path.join(outdir, "summary.md"), "w").write("\n".join(md))
    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    main()
