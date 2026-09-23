#!/usr/bin/env python3
"""OSC.04 hop 2: per-query-head RoPE-pair pruning from hop 1's pooled profiles.

Run: PYTHONPATH=/data/ml/scratch/osc03/pylib nice -n 19 \
       /data/ml/.venv/bin/python .agi/context/local-maxxing/osc/osc_band_prune.py

Keep, per query head, the smallest prefix of RoPE pairs (HF rotate_half pair
p = dims (p, p+32)) carrying 90/95/99 pct of that head's logit energy, zero the
rest in q AFTER RoPE, and measure top-1 next-token agreement + mean per-token
KL against the unmasked model on a 4096-token eval disjoint from hop 1. Random
masks dropping the SAME number of pairs per head are the control. Out-of-repo
roots stay literal per OSC.04 orders.
"""
import gzip, hashlib, json, os, sys, time
import numpy as np
import torch

torch.set_num_threads(8)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import paths
import osc_band_measure as obm   # hop 1: head_var + its per-pair selftest

HF = "/data/ml/scratch/osc03/hf"
WIKI = "/data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw"
HEVAL = ("/data/work/agi/.agi/sessions/iter-ABC.02/a00-c4441397/scratch/venv/"
         "lib/python3.12/site-packages/human_eval/data/HumanEval.jsonl.gz")
REV = "7ae557604adf67be50417f59c2c2f167def9a775"
T, NHEAD, NPAIR, GROUP = 512, 14, 32, 7
ENERGIES = [(0.80, "80"), (0.85, "85"), (0.90, "90"), (0.93, "93"),
            (0.95, "95"), (0.97, "97"), (0.99, "99"), (0.995, "995"),
            (0.999, "999"), (1.0, "1000")]  # 1000 = keep all 32 pairs (no-op anchor)
CONTROL_AT, SEEDS = ["90", "95", "99"], [1, 2, 3]
COUNTS = [(31, "k31"), (29, "k29")]   # drop the 1 / 3 lowest-energy pairs per head
WIKI_STARTS = [5000, 61000, 120000, 240000]
HEVAL_SLICE = slice(10, 14)
MASK, CUR, CAP = {"m": None}, {"l": -1}, {}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def build_eval(tok):
    """4096 tokens = 4 x 512 wikitext slices + 4 x 512 HumanEval prompts,
    disjoint from hop 1's 20 prompts (asserted, not assumed)."""
    ids = tok(open(WIKI, encoding="utf-8").read(), add_special_tokens=False)["input_ids"]
    hop1 = [((len(ids) - 320) * i // 10, 320) for i in range(10)]
    for s in WIKI_STARTS:
        assert all(s + T <= t or t + L <= s for t, L in hop1), s
    wiki = [ids[s:s + T] for s in WIKI_STARTS]
    with gzip.open(HEVAL, "rt") as f:
        js = sorted((json.loads(l) for l in f), key=lambda p: p["task_id"])
    band = js[:10]
    pros = js[HEVAL_SLICE]
    assert not ({p["task_id"] for p in pros} & {p["task_id"] for p in band})
    he = []
    for p in pros:
        t = tok(p["prompt"], add_special_tokens=False)["input_ids"]
        while len(t) < T:
            t = t + t
        he.append(t[:T])
    meta = {"wiki_slice_starts": WIKI_STARTS, "wiki_span": T,
            "heval_task_ids": [p["task_id"] for p in pros],
            "heval_padded_to": T, "n_prompts": len(wiki) + len(he),
            "n_tokens": (len(wiki) + len(he)) * T,
            "hop1_wiki_starts": [t for t, _ in hop1],
            "hop1_heval_task_ids": [p["task_id"] for p in band]}
    return wiki + he, meta


def kept_energy(prof, target):
    order = np.argsort(-prof)
    return order[:int(np.searchsorted(np.cumsum(prof[order]), target) + 1)]


def kept_count(prof, n_keep):
    return np.argsort(-prof)[:n_keep]


def kept_random(n_keep, rng):
    return rng.choice(NPAIR, size=n_keep, replace=False)


def mask_tensor(kept):
    m = np.zeros((NHEAD, 2 * NPAIR), dtype=np.float32)
    for h, ks in enumerate(kept):
        for p in ks:
            m[h, p] = m[h, p + NPAIR] = 1.0
    return torch.from_numpy(m).view(1, NHEAD, 1, 2 * NPAIR)


def install(model):
    import transformers.models.qwen2.modeling_qwen2 as M
    orig = M.apply_rotary_pos_emb

    def rope(q, k, cos, sin, unsqueeze_dim=1):
        qq, kk = orig(q, k, cos, sin, unsqueeze_dim)
        if MASK["m"] is not None:
            qq = qq * MASK["m"][CUR["l"]]
        if CUR["l"] == 0:
            CAP["q"], CAP["k"] = qq.detach().float(), kk.detach().float()
        return qq, kk
    M.apply_rotary_pos_emb = rope
    for i, layer in enumerate(model.model.layers):
        fwd = layer.self_attn.forward

        def wrap(f, i):
            def g(*a, **kw):
                CUR["l"] = i
                return f(*a, **kw)
            return g
        layer.self_attn.forward = wrap(fwd, i)


def kside(kept):
    """Per KV head (GROUP query heads share one), the UNION of kept pairs."""
    return [sorted(set().union(*kept[k * GROUP:(k + 1) * GROUP]))
            for k in range(NHEAD // GROUP)]


def selftest_mask(model, ids):
    """A mask dropping ONLY pair 0 must leave every other pair's c_p unchanged
    and zero pair 0. Run BEFORE the model pass (hop 1's pairing contract)."""
    assert obm.selftest_head_var(), "hop 1 head_var selftest FAILED"
    def cap(m):
        MASK["m"] = None if m is None else [m] * 24
        CAP.clear()
        with torch.no_grad():
            model(ids)
        return obm.head_var(CAP["q"], CAP["k"])
    e0 = cap(None)
    e1 = cap(mask_tensor([np.arange(1, NPAIR)] * NHEAD))  # drop pair 0, keep the rest
    ok_other = np.array_equal(e1[:, 1:], e0[:, 1:])
    ok_zero = float(np.abs(e1[:, 0]).max()) == 0.0
    print(f"selftest mask: other-pairs-unchanged={ok_other} pair0-zero={ok_zero}")
    return ok_other and ok_zero


def metrics(ref_logp, logits):
    lp = torch.log_softmax(logits.float(), -1)
    agree = float((ref_logp.argmax(-1) == lp.argmax(-1)).float().mean())
    d = ref_logp - lp
    d.mul_(ref_logp.exp())
    return agree, float(d.sum(-1).mean())


def main():
    t0 = time.time()
    prov = json.load(open(os.path.join(paths.get_local("osc_band_dir"),
                                       "provenance.json")))
    rever = {f: (sha(os.path.join(HF, f)) == h)
             for f, h in prov["hf_sha256"].items()}
    assert all(rever.values()), rever
    print("sha re-verify:", rever)

    from transformers import AutoTokenizer, AutoModelForCausalLM
    tok = AutoTokenizer.from_pretrained(HF)
    model = AutoModelForCausalLM.from_pretrained(
        HF, dtype=torch.float32, attn_implementation="eager").eval()
    install(model)
    prompts, eval_meta = build_eval(tok)
    print("eval:", json.dumps(eval_meta))
    assert selftest_mask(model, torch.tensor([prompts[0]])), "mask selftest FAILED"

    heads = json.load(open(os.path.join(paths.get_local("osc_band_dir"),
                                        "profiles.json")))["heads"]
    prof = np.array([heads[f"L{L}H{h}"]["profile_pooled"]
                     for L in range(24) for h in range(NHEAD)])
    kept = {f"energy_{tag}": [[kept_energy(prof[L * NHEAD + h], t)
                               for h in range(NHEAD)] for L in range(24)]
            for t, tag in ENERGIES}
    for n, tag in COUNTS:
        kept[f"keep_{tag}"] = [[kept_count(prof[L * NHEAD + h], n)
                                for h in range(NHEAD)] for L in range(24)]
    for tag in CONTROL_AT:
        for s in SEEDS:
            rng = np.random.default_rng(s)
            kept[f"rand_{tag}_s{s}"] = [
                [kept_random(len(kept[f"energy_{tag}"][L][h]), rng) for h in range(NHEAD)]
                for L in range(24)]
    masks = {k: [mask_tensor(v[L]) for L in range(24)] for k, v in kept.items()}
    band2 = paths.get_local("osc_band_hop2_dir")
    os.makedirs(band2, exist_ok=True)
    dropq = {k: float(np.mean([1 - len(v[L][h]) / NPAIR
                               for L in range(24) for h in range(NHEAD)]))
             for k, v in kept.items()}
    dropk = {k: float(np.mean([1 - len(u) / NPAIR
                               for L in range(24) for u in kside(v[L])]))
             for k, v in kept.items()}

    agg = {k: {"agree": 0.0, "kl": 0.0} for k in masks}
    for pi, ids in enumerate(prompts):
        it = torch.tensor([ids])
        MASK["m"] = None
        with torch.no_grad():
            ref_logp = torch.log_softmax(model(it).logits[0].float(), -1)
        for k, m in masks.items():
            MASK["m"] = m
            with torch.no_grad():
                lg = model(it).logits[0]
            a, kl = metrics(ref_logp, lg)
            agg[k]["agree"] += a / len(prompts)
            agg[k]["kl"] += kl / len(prompts)
        print(f"prompt {pi + 1}/{len(prompts)} done {time.time() - t0:.0f}s", flush=True)

    json.dump({"agg": agg, "dropq": dropq, "dropk": dropk, "keys": sorted(masks)},
              open(os.path.join(band2, "raw.json"), "w"), indent=1)
    res = {k: {"target": k.replace("energy_", "").replace("rand_", "").split("_")[0],
               "agree": round(agg[k]["agree"], 6),
               "kl": round(agg[k]["kl"], 6), "dropped_q": round(dropq[k], 6),
               "dropped_k": round(dropk[k], 6)}
           for k in masks}
    cand = [res[f"energy_{tag}"] for _, tag in ENERGIES] + \
           [res[f"keep_{tag}"] for _, tag in COUNTS]
    hit = [r for r in cand if r["agree"] >= 0.98 and r["kl"] <= 0.02
           and r["dropped_q"] > 0]
    best = max(hit, key=lambda r: r["dropped_q"]) if hit else None
    e95 = res["energy_95"]
    ok95 = (e95["dropped_q"] >= 0.40 and e95["agree"] >= 0.98 and e95["kl"] <= 0.02)
    ctrl = {tag: np.mean([res[f"rand_{tag}_s{s}"]["agree"] for s in SEEDS])
            for tag in CONTROL_AT}
    beats = {tag: bool(res[f"energy_{tag}"]["agree"] > ctrl[tag]) for tag in CONTROL_AT}
    out = {"meta": {"model": "Qwen/Qwen2.5-0.5B-Instruct", "revision": REV,
                    "dtype": "float32", "mask": "q after RoPE, pair (p,p+32)",
                    "eval": eval_meta, "sha_reverify": rever,
                    "t_s": round(time.time() - t0, 1)},
           "settings": res, "control_mean_agree": {k: round(float(v), 6) for k, v in ctrl.items()},
           "energy_beats_random": beats,
           "at_95_pct": {"dropped_q": e95["dropped_q"], "agree": e95["agree"],
                         "kl": e95["kl"], "passes": ok95},
           "largest_dropped_fraction_both_hold": best}
    json.dump(out, open(os.path.join(band2, "results.json"), "w"), indent=1)
    json.dump({"eval": eval_meta, "sha_reverify": rever,
               "weights": os.path.join(HF, "model.safetensors"),
               "wikitext_sha256": sha(WIKI), "humaneval_sha256": sha(HEVAL),
               "profiles_sha256": sha(os.path.join(paths.get_local("osc_band_dir"),
                                                   "profiles.json"))},
              open(os.path.join(band2, "provenance.json"), "w"), indent=1)
    md = ["# OSC.04 hop 2: per-query-head RoPE pair pruning", "",
          f"eval: {eval_meta['n_prompts']} prompts x {T} = {eval_meta['n_tokens']} tokens"
          f" (disjoint from hop 1, asserted)", "",
          "| setting | dropped q | dropped k (union) | agree | mean KL |", "|---|---|---|---|---|"]
    for k in ([f"energy_{t}" for _, t in ENERGIES] +
              [f"keep_{t}" for _, t in COUNTS] +
              [f"rand_{t}_s{s}" for t in CONTROL_AT for s in SEEDS]):
        r = res[k]
        md.append(f"| {k} | {r['dropped_q']} | {r['dropped_k']} | {r['agree']} | {r['kl']} |")
    md += ["", f"at 95 pct: dropped q {e95['dropped_q']}, agree {e95['agree']}, "
           f"KL {e95['kl']} -> passes={ok95}",
           f"largest dropped fraction with both hold: {best}", ""]
    open(os.path.join(band2, "summary.md"), "w").write("\n".join(md))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
