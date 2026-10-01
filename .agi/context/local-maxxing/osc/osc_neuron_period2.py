#!/usr/bin/env python3
"""Neuron periodicity MAP run 2 (hypothesis:lm-neuron-periodicity-detrended-families-carry-addition): detrended
value-axis peakiness vs 2 detrended nulls (D1); mean-ablating period families vs 5 layer-matched random sets on the
gold sum's log-prob (D2); C3 layer-stratified overlap (reported). Grid = <cell osc_neuron_period2_dir>/params.json;
run 1's template/problems/doc read from run 1's params by path. Detached: `--twin` (own process) first, then bare."""
import json, math, os, re, shutil, subprocess, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period as S  # noqa: E402  run 1: loader, hooks, prompts, problems, peakiness (unchanged)
import paths  # noqa: E402

DROP = ("members", "top_ids", "arms")   # long lists: results.json only, not summary.md


def detrend(X, tol=1e-9):
    """Remove each column's least-squares fit c0 + c1*t over axis 0; residual SS <= tol * centred SS -> exactly 0."""
    C = np.asarray(X, np.float64) - np.mean(X, 0)
    t = np.arange(len(C)) - (len(C) - 1) / 2
    R = C - np.outer(t, t @ C / (t @ t))
    return np.where((R ** 2).sum(0) <= tol * (C ** 2).sum(0), 0.0, R)


dpeak = lambda X, tol=1e-9: S.peakiness(detrend(X, tol))   # (detrended peakiness, dominant bin k)


def detrended_null(acts, n, seed, tol):   # permute a FIRST, then detrend against the a-slot, then peakiness
    rng = np.random.default_rng(seed)
    return np.stack([dpeak(acts[rng.permutation(len(acts))], tol)[0] for _ in range(n)])


def layer_matched(family, width, layers, seed):
    """Same count per layer as family, drawn from that layer minus the family; layers ascending."""
    rng, fam, cnt, out = np.random.default_rng(seed), set(family), np.bincount(np.array(family, int) // width,
                                                                                 minlength=layers), []
    for li in (li for li in range(layers) if cnt[li]):
        pool = [f for f in range(li * width, (li + 1) * width) if f not in fam]
        out += sorted(int(x) for x in rng.choice(pool, cnt[li], replace=False))
    return out


def strat_sf(x, n_l, K_l, N):
    """P(X >= x), X = sum over layers of independent Hypergeometric(N, K_l, n_l): exact convolution."""
    lc = lambda a, b: math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)
    pmf = np.ones(1)
    for n, K in zip(n_l, K_l):
        pmf = np.convolve(pmf, [math.exp(lc(K, i) + lc(N - K, n - i) - lc(N, n)) if n - (N - K) <= i else 0.0
                                for i in range(min(K, n) + 1)])
    return float(min(1.0, pmf[x:].sum()))


class Neurons2(S.Neurons):
    """Run 1's hooks and ablate(); an ablated input becomes x*mask + (1-mask)*mean (means set) or x*mask (zero)."""
    means = None

    def _hook(self, i):
        def h(_mod, args):
            x = args[0] if i not in self.mask else args[0] * self.mask[i] + (
                0.0 if self.means is None else (1 - self.mask[i]) * self.means[i])
            return (x, self.fn(i, x))[:1] if self.fn is not None else (x,)
        return h


def gold_logp(model, tok, texts, gold, bs):
    """Per problem log P(full gold sum | prompt) = sum over its tokens, teacher forcing, right-padded batches."""
    enc = lambda s: tok(s, add_special_tokens=False)["input_ids"]
    rows, L0, out = [enc(t) + enc(g) for t, g in zip(texts, gold)], S.encode(tok, texts).shape[1], []
    assert all(r == enc(t + g) for r, t, g in zip(rows, texts, gold)), "sum tokens merge with the prompt"
    for b in range(0, len(rows), bs):
        rs, T = rows[b:b + bs], max(map(len, rows[b:b + bs]))
        with torch.no_grad():   # kept logits start at position L0-1, which predicts token L0
            lp = torch.log_softmax(model(input_ids=torch.tensor([r + r[-1:] * (T - len(r)) for r in rs]),
                                         logits_to_keep=T - L0 + 1).logits.float(), -1)
        out += [float(sum(lp[j, p, r[L0 + p]] for p in range(len(r) - L0))) for j, r in enumerate(rs)]
    return np.array(out)


def num_mask_take(skip, toks, perm, tol):
    """C3 reader: positions whose token has a digit -> that series' unmasked mean; detrend; peakiness."""
    m = np.array([bool(re.search(r"\d", toks[j])) for j in perm])[skip:]

    def take(x):
        s = x[0, skip:].numpy().astype(np.float64)
        s[m] = s[~m].mean(0)
        return dpeak(s, tol)[0][None]
    return take, int(m.sum())


def main(twin):
    out, t0 = paths.get_local("osc_neuron_period2_dir"), time.time()
    P, part = json.load(open(os.path.join(out, "params.json"))), os.path.join(out, "partial")
    P1, tol = json.load(open(os.path.join(paths.get_local("osc_neuron_period_dir"), "params.json"))), P["detrend_tol"]
    os.makedirs(part, exist_ok=True)
    torch.set_num_threads(P["threads"])
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(hfdir := paths.get(P["model_cell"]))
    S.wait_box(P)
    torch.manual_seed(P["twin_seed"])   # seeds the twin's init; inert for the pretrained load
    model = (AutoModelForCausalLM.from_config(AutoConfig.from_pretrained(hfdir), dtype=torch.float32) if twin
             else AutoModelForCausalLM.from_pretrained(hfdir, dtype=torch.float32)).eval()
    N, tag = Neurons2(model), "_twin" if twin else ""
    ids = S.encode(tok, [P1["c1_template"].format(few="\n".join(P1["few_shot"]), a=a) for a in range(*P1["c1_a"])])
    assert len(set(ids[:, -1].tolist())) == 1, "last token differs across a"
    if not os.path.exists(fa := os.path.join(part, f"acts{tag}.npy")):
        np.save(fa, N.read(model, ids, S.last_token))
    acts = np.load(fa)
    pk, kb = dpeak(acts, tol)
    np.savez_compressed(os.path.join(out, f"value_acts{tag}.npz"), acts=acts.astype(np.float16),
                        peak_raw=S.peakiness(acts)[0].astype(np.float32), peak_detrended=pk.astype(np.float32),
                        k_detrended=kb.astype(np.int16))
    if twin:
        json.dump({"P": P, "max": float(pk.max()), "q999": float(np.quantile(pk, 0.999)), "n": int(pk.size),
                   "layer_max": pk.reshape(-1, N.width).max(1).tolist()}, open(os.path.join(out, "twin.json"), "w"))
        return print(f"twin detrended max {pk.max():.4f} ({time.time() - t0:.0f}s)", flush=True)
    tw = json.load(open(os.path.join(out, "twin.json")))   # missing twin -> crash, never a silent skip
    assert tw["P"] == P, "twin.json belongs to another grid"
    nl, W, n = len(N.mlps), N.width, acts.shape[1]
    grid_ok = W == 4864 and nl == 24 and acts.shape == (100, nl * W) and tw["n"] == n
    null = detrended_null(acts, P["null_permutations"], P["null_seed"], tol)
    q = float(np.quantile(null, P["null_quantile"]))
    d1 = np.flatnonzero((pk > q) & (pk > tw["max"]))
    fams = {f: [int(i) for i in d1 if kb[i] in ks] for f, ks in P["families"].items()}   # rule fixed in params
    arms, match_ok, per_l = {"baseline": []}, True, lambda s: np.bincount(np.array(s, int) // W, minlength=nl)
    for f, mem in fams.items():   # match_ok: every random set has its family's per-layer counts and is disjoint
        arms.update({f: mem, **(rnd := {f"{f}_rand_s{s}": layer_matched(mem, W, nl, s) for s in P["random_seeds"]})})
        match_ok &= all(np.array_equal(per_l(v), per_l(mem)) and not set(v) & set(mem) for v in rnd.values())
    means, (texts, gold) = torch.from_numpy(acts.mean(0).reshape(nl, W)).float(), S.c2_problems(P1)
    res = json.load(open(fd)) if os.path.exists(fd := os.path.join(part, "d2.json")) else {}
    for key, ab in ((f"{a}|{m}", ab) for a, ab in arms.items() for m in (["mean", "zero"] if ab else ["mean"])):
        if key not in res:
            N.means = means if key.endswith("mean") else None
            N.ablate(ab)
            lp = gold_logp(model, tok, texts, gold, P["score_batch"])
            res[key] = {"logp": float(lp.mean()), "exact": S.addition_acc(model, tok, N, P1, ab)[0], "n": len(ab)}
            json.dump(res, open(fd, "w"))   # addition_acc ends with ablate([])
        print(f"D2 {key}: {res[key]} ({time.time() - t0:.0f}s)", flush=True)
    base, d2 = res["baseline|mean"]["logp"], {}
    for f, mem in fams.items():
        drop = lambda a, m: base - res[f"{a}|{m}"]["logp"] if mem else 0.0
        ex = lambda a, m: res[f"{a}|{m}"]["exact"] if mem else None
        rs = [f"{f}_rand_s{s}" for s in P["random_seeds"]]
        d2[f] = {"size": len(mem), "flag_small": len(mem) < P["family_min_size_flag"], "per_layer": per_l(mem).tolist(),
                 "pass": bool(mem) and drop(f, "mean") > max(drop(a, "mean") for a in rs), "members": mem,
                 **{f"{k}_{m}": ([fn(a, m) for a in rs] if k.startswith("rand") else fn(f, m)) for m in ("mean", "zero")
                    for k, fn in (("drop", drop), ("rand_drop", drop), ("exact", ex), ("rand_exact", ex))}}
    if not os.path.exists(fc := os.path.join(part, "c3.npz")):
        doc = S.load_doc(tok, P1)
        perm = np.random.default_rng(P1["c3_shuffle_seed"]).permutation(doc.shape[1])   # run 1's shuffle
        toks = tok.batch_decode([[t] for t in doc[0].tolist()])
        (to, nm), (ts, _) = (num_mask_take(P1["c3_skip"], toks, p, tol) for p in (np.arange(doc.shape[1]), perm))
        np.savez(fc, orig=N.read(model, doc, to)[0], shuf=N.read(model, doc[:, torch.from_numpy(perm)], ts)[0], nm=nm)
    z = np.load(fc)
    s3, n3 = z["orig"] - z["shuf"], int(P1["c3_top_fraction"] * n)
    top3 = np.argsort(-s3, kind="stable")[:n3]
    ov, n_l, K_l = int(np.isin(top3, d1).sum()), per_l(top3), per_l(d1)
    c3 = {"overlap": ov, "draws": n3, "d1_size": len(d1), "masked_positions": int(z["nm"]),
          "expected_stratified": float((n_l * K_l).sum() / W), "p_stratified": strat_sf(ov, n_l, K_l, W),
          "expected_unstratified": n3 * len(d1) / n, "p_unstratified": S.hyper_sf(ov, n, len(d1), n3),
          "top_per_layer": n_l.tolist(), "top_ids": top3[:200].tolist()}
    saved = all(os.path.exists(os.path.join(out, f"value_acts{t}.npz")) for t in ("", "_twin"))
    void = not (grid_ok and match_ok and saved and null.shape == (P["null_permutations"], n))
    d1_pass, d2_pass = len(d1) / n >= P["d1_min_fraction"], any(v["pass"] for v in d2.values())
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a, "--", __file__], capture_output=True, text=True)
    commit, dirty = git("log", "-1", "--format=%H").stdout.strip(), git("diff", "--quiet", "HEAD").returncode != 0
    R = {"verdict": "void" if void else "proved" if d1_pass and d2_pass else "disproved", "void": void,
         "grid_ok": grid_ok, "match_ok": match_ok, "saved": saved, "script_commit": commit, "script_dirty": dirty,
         "d1": {"pass": bool(d1_pass), "count": len(d1), "fraction": len(d1) / n, "n_neurons": n, "null_q999": q,
                "null_n": int(null.size), "twin_max": tw["max"], "twin_q999": tw["q999"],
                "count_beat_null": int((pk > q).sum()), "count_beat_twin": int((pk > tw["max"]).sum()),
                "per_layer": K_l.tolist(), "twin_layer_max": tw["layer_max"],
                "period_hist": {f"T{100 / k:g}": int(c) for k, c in zip(*np.unique(kb[d1], return_counts=True))}},
         "d2": {"pass": bool(d2_pass), "baseline_logp": base, "baseline_exact": res["baseline|mean"]["exact"],
                "families": d2, "arms": res}, "c3": c3, "wall_s": round(time.time() - t0, 1), "torch": torch.__version__}
    json.dump(R, open(os.path.join(out, "results.json"), "w"), indent=1)
    shutil.rmtree(part)
    short = lambda d: {k: short(v) if isinstance(v, dict) else v for k, v in d.items() if k not in DROP}
    lines = [f"# Neuron periodicity MAP run 2: {R['verdict']}", ""] + [f"- {k}: {json.dumps(v)}" for k, v in
                                                                        short(R).items()]
    open(os.path.join(out, "summary.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main("--twin" in sys.argv[1:])
