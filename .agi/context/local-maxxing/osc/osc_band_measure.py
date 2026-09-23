#!/usr/bin/env python3
"""OSC.03: per-head post-RoPE band-energy profiles of Qwen2.5-0.5B-Instruct.

Run: PYTHONPATH=/data/ml/scratch/osc03/pylib nice -n 19 /data/ml/.venv/bin/python osc_band_measure.py

One pass, CPU, 8 threads: capture q,k AFTER RoPE (patch apply_rotary_pos_emb),
assert the capture reproduces the model's own pre-softmax logit to 1e-3 relative,
then write profiles.json / summary.json / summary.md / provenance.json.
Out-of-repo roots (HF weights, pip target) stay literal per OSC.03 orders.
"""
import gzip, hashlib, json, os, sys, time
import numpy as np
import torch

torch.set_num_threads(8)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import paths

HF = "/data/ml/scratch/osc03/hf"
WIKI = "/data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw"
HEVAL = paths.get_local("humaneval_file")  # committed copy, same bytes (sha256 b796127e...)
REV = "7ae557604adf67be50417f59c2c2f167def9a775"
NPROMPT, MINTOK = 256, 256
LOW = list(range(21, 32))   # 11 lowest-frequency pairs
HIGH = list(range(0, 11))   # 11 highest-frequency pairs
CAP, CUR = {}, {"layer": None}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def build_prompts(tok):
    ids = tok(open(WIKI, encoding="utf-8").read(),
              add_special_tokens=False)["input_ids"]
    span = 320
    starts = [(len(ids) - span) * i // 10 for i in range(10)]
    wiki = [tok.decode(ids[s:s + span]) for s in starts]
    pros = []
    with gzip.open(HEVAL, "rt") as f:
        prob = sorted((json.loads(l) for l in f), key=lambda p: p["task_id"])[:10]
    for p in prob:
        t = tok(p["prompt"], add_special_tokens=False)["input_ids"]
        while len(t) < MINTOK:
            t = t + t
        pros.append(tok.decode(t))
    prompts = wiki + pros
    lens = [len(tok(p, add_special_tokens=False)["input_ids"]) for p in prompts]
    assert all(n >= MINTOK for n in lens), lens
    halves = {"A": [0, 1, 2, 3, 4] + [10, 11, 12, 13, 14],
              "B": [5, 6, 7, 8, 9] + [15, 16, 17, 18, 19]}
    return prompts, halves, lens


def head_var(q, k, g=7, pairs=32):
    """Variance of c_p(i,j) over all causal (i>=j), per (query head, pair).

    c_p = q_i[p] k_j[p] + q_i[p+32] k_j[p+32]. Uses prefix sums so cost is
    O(T * d) per head, exact (no pair matrix materialised).
    """
    q, k = q[0].transpose(0, 1), k[0].transpose(0, 1)
    T = q.shape[0]
    # HF rotate_half pairs dims (p, p + pairs), NOT consecutive dims -- so
    # split the head dim in HALVES: A=q[...,:32], B=q[...,32:], K0,K1 alike.
    # (Pairing consecutive dims was the OSC.03 kid-1 bug, caught by selftest.)
    kr = k.repeat_interleave(g, dim=1).numpy()
    qn = q.numpy()
    cs, cs2 = np.cumsum(kr[..., :pairs], 0), np.cumsum(kr[..., :pairs] ** 2, 0)
    cs1, cs21 = np.cumsum(kr[..., pairs:], 0), np.cumsum(kr[..., pairs:] ** 2, 0)
    A, B = qn[..., :pairs], qn[..., pairs:]
    K0, K1 = kr[..., :pairs], kr[..., pairs:]
    cross = np.cumsum(K0 * K1, 0)
    N = T * (T + 1) / 2.0
    sc = (A * cs + B * cs1).sum(0)
    sc2 = (A * A * cs2 + B * B * cs21 + 2 * A * B * cross).sum(0)
    return np.maximum(sc2 / N - (sc / N) ** 2, 0.0).astype(np.float64)


def selftest_head_var(g=7, pairs=32):
    """Synthetic check that head_var pairs dims (p, p+pairs), not consecutive.

    A position-varying signal on both dims of ONE contract pair must put ALL
    energy on that pair index. Run BEFORE any model pass; a failure means the
    decomposition is wrong and no measurement may be taken on it.
    """
    T, H, D = 16, 14, 64
    i = torch.arange(T).float().view(1, 1, T)
    ok = True
    for p in (0, 21):
        q, k = torch.zeros(1, H, T, D), torch.zeros(1, 2, T, D)
        q[..., p], q[..., p + 32] = torch.sin(0.7 * i), torch.sin(0.11 * i)
        for h in range(2):
            k[:, h, :, p], k[:, h, :, p + 32] = torch.cos(0.3 * i), torch.cos(0.5 * i)
        e = np.atleast_2d(head_var(q, k, g, pairs))[0]
        tot = float(e.sum())
        hits = [int(x) for x in np.nonzero(e > 1e-6 * tot)[0]]
        good = hits == [p]
        ok &= good
        print(f"selftest head_var pair {p}: hits={hits} "
              f"shares={[round(float(e[x] / tot), 4) for x in hits]} "
              f"-> {'PASS' if good else 'FAIL'}")
    print(f"selftest head_var: {'PASS' if ok else 'FAIL'}")
    return ok


def install_hooks(model):
    import transformers.models.qwen2.modeling_qwen2 as M
    orig = M.apply_rotary_pos_emb

    def rope(q, k, cos, sin, unsqueeze_dim=1):
        qq, kk = orig(q, k, cos, sin, unsqueeze_dim)
        CAP[CUR["layer"]] = (qq.detach().float(), kk.detach().float())
        return qq, kk

    M.apply_rotary_pos_emb = rope
    for i, layer in enumerate(model.model.layers):
        attn, fwd = layer.self_attn, layer.self_attn.forward

        def wrap(orig_fwd, idx):
            def f(*a, **kw):
                CUR["layer"] = idx
                out = orig_fwd(*a, **kw)
                if idx == 0:
                    CAP["W0"] = out[1]
                return out
            return f
        attn.forward = wrap(fwd, i)


def profile(e):
    return e / e.sum(-1, keepdims=True)


def main():
    t0 = time.time()
    assert selftest_head_var(), "head_var pairing self-test FAILED -- no measurement"
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(HF)
    model = AutoModelForCausalLM.from_pretrained(
        HF, dtype=torch.float32, attn_implementation="eager").eval()
    install_hooks(model)
    prompts, halves, lens = build_prompts(tok)

    with torch.no_grad():
        ids = tok("The capital of France is", return_tensors="pt")["input_ids"]
        paris = tok.decode(model(ids).logits[0, -1].argmax())
        wids = tok(open(WIKI, encoding="utf-8").read(),
                   add_special_tokens=False)["input_ids"][100000:100512]
        loss = model(torch.tensor([wids]), labels=torch.tensor([wids])).loss
        ppl = float(torch.exp(loss))

        # --- logit-reproduction check on layer 0 head 0, prompt 0 ---
        CAP.clear()
        model(input_ids=tok(prompts[0], return_tensors="pt")["input_ids"])
        q, k = CAP[0]
        q, k = q[0, 0], k[0, 0]
        W = CAP.pop("W0")[0, 0].double()
        S = (q.double() @ k.double().T) * (q.shape[-1] ** -0.5)
        j = torch.arange(S.shape[0])
        m = (j[None, :] <= j[:, None])
        logw = W.clamp_min(1e-30).log()
        d = ((S - S[:, :1]) - (logw - logw[:, :1]))[m].abs().max()
        rel = float(d / S[m].abs().max())

        # --- per-head energy accumulation ---
        acc = {h: np.zeros((24, 14, 32)) for h in ("A", "B")}
        for pi, p in enumerate(prompts):
            CAP.clear()
            model(input_ids=tok(p, return_tensors="pt")["input_ids"])
            e = np.stack([head_var(*CAP[L]) for L in range(24)])
            half = "A" if pi in halves["A"] else "B"
            acc[half] += e
    pool = (acc["A"] + acc["B"]) / 20.0
    profs = {h: profile(acc[h] / 10.0) for h in ("A", "B")}
    profs["pooled"] = profile(pool)
    pa, pb, pp = (profs[x].reshape(336, 32) for x in ("A", "B", "pooled"))
    cos = (pa * pb).sum(-1) / (np.linalg.norm(pa, axis=-1) * np.linalg.norm(pb, axis=-1))
    low = pp[:, LOW].sum(-1)
    high = pp[:, HIGH].sum(-1)
    keys = [f"L{L}H{h}" for L in range(24) for h in range(14)]
    band = paths.get_local("osc_band_dir")
    os.makedirs(band, exist_ok=True)
    profiles = {k: {"profile_A": pa[i].round(8).tolist(),
                    "profile_B": pb[i].round(8).tolist(),
                    "profile_pooled": pp[i].round(8).tolist()}
                for i, k in enumerate(keys)}
    json.dump({"meta": {"model": "Qwen/Qwen2.5-0.5B-Instruct", "revision": REV,
                        "dtype": "float32", "n_heads": 336, "n_pairs": 32,
                        "prompts": len(prompts), "min_tokens": int(min(lens))},
               "heads": profiles},
              open(os.path.join(band, "profiles.json"), "w"), indent=0)
    per_layer = [{"layer": L, "mean_cos": round(float(cos[L * 14:(L + 1) * 14].mean()), 6),
                  "mean_low": round(float(low[L * 14:(L + 1) * 14].mean()), 6),
                  "mean_high": round(float(high[L * 14:(L + 1) * 14].mean()), 6)}
                 for L in range(24)]
    summary = {
        "n_heads": 336, "n_stable": int((cos >= 0.9).sum()),
        "share_stable_0.9": round(float((cos >= 0.9).mean()), 6),
        "cos": {"mean": round(float(cos.mean()), 6), "min": round(float(cos.min()), 6),
                "median": round(float(np.median(cos)), 6),
                "q25": round(float(np.percentile(cos, 25)), 6),
                "q75": round(float(np.percentile(cos, 75)), 6),
                "q10": round(float(np.percentile(cos, 10)), 6),
                "q90": round(float(np.percentile(cos, 90)), 6)},
        "band": {
            "n_low_ge_0.80": int((low >= 0.80).sum()),
            "share_low_ge_0.80": round(float((low >= 0.80).mean()), 6),
            "n_high_ge_0.50": int((high >= 0.50).sum()),
            "share_high_ge_0.50": round(float((high >= 0.50).mean()), 6),
            "mean_low": round(float(low.mean()), 6),
            "mean_high": round(float(high.mean()), 6)},
        "per_layer": per_layer}
    json.dump(summary, open(os.path.join(band, "summary.json"), "w"), indent=1)
    json.dump({"hf_revision": REV,
               "hf_sha256": {f: sha(os.path.join(HF, f)) for f in sorted(os.listdir(HF))},
               "wikitext_zip_sha256": sha("/data/ml/scratch/osc02/wikitext-2-raw-v1.zip"),
               "wikitext_test_sha256": sha(WIKI),
               "humaneval_sha256": sha(HEVAL),
               "pip": {"transformers": "5.17.0", "safetensors": "0.8.0",
                       "tokenizers": "0.23.2", "numpy": "2.5.3",
                       "torch": torch.__version__},
               "logit_repro_rel": rel, "paris": paris, "ppl_512": ppl,
               "t0_s": round(time.time() - t0, 1)},
              open(os.path.join(band, "provenance.json"), "w"), indent=1)
    lines = ["# OSC.03 band profile summary", "",
             f"stable cos>=0.9: {int((cos>=0.9).sum())}/336 = {float((cos>=0.9).mean()):.4f}",
             f"cos mean {cos.mean():.4f} median {np.median(cos):.4f} min {cos.min():.4f}",
             f"low-third>=0.80: {int((low>=0.80).sum())}/336 = {float((low>=0.80).mean()):.4f}",
             f"high-third>=0.50: {int((high>=0.50).sum())}/336 = {float((high>=0.50).mean()):.4f}",
             "", "| layer | mean_cos | mean_low | mean_high |", "|---|---|---|---|"]
    lines += [f"| {r['layer']} | {r['mean_cos']} | {r['mean_low']} | {r['mean_high']} |"
              for r in per_layer]
    open(os.path.join(band, "summary.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps({"rel": rel, "paris": paris, "ppl": ppl, "summary": summary},
                     indent=1))
    assert rel < 1e-3, f"hook failed logit reproduction: rel={rel}"


if __name__ == "__main__":
    main()
