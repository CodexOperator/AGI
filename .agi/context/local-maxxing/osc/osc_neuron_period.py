#!/usr/bin/env python3
"""Neuron periodicity MAP (hypothesis:lm-neuron-periodicity-map-finds-function-neurons) on Qwen2.5-0.5B MLP neurons
(down_proj input): C1 value-axis peakiness vs 2 nulls, C2 ablation on addition, C3 position-axis overlap. Grid =
<cell osc_neuron_period_dir>/params.json. Run detached: `osc_neuron_period.py --twin` (SEPARATE process), then bare."""
import json, math, os, re, shutil, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import paths  # noqa: E402


def peakiness(X):
    """Series along axis 0 -> (max non-DC power / total non-DC power, dominant bin k >= 1); zero power -> 0."""
    P = np.abs(np.fft.rfft(np.asarray(X, np.float64), axis=0)[1:]) ** 2
    tot = P.sum(0)
    return np.where(tot > 0, P.max(0) / np.where(tot > 0, tot, 1.0), 0.0), P.argmax(0) + 1


def shuffled_null(acts, n, seed):
    """Peakiness of the same activations with the a-axis permuted, n permutations -> (n, neurons)."""
    rng = np.random.default_rng(seed)
    return np.stack([peakiness(acts[rng.permutation(len(acts))])[0] for _ in range(n)])


def hyper_sf(x, N, K, n):
    """P(X >= x), X ~ Hypergeometric(population N, K successes, n draws)."""
    lc = lambda a, b: math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1)
    lo, hi = max(x, n - (N - K), 0), min(K, n)
    return min(1.0, sum(math.exp(lc(K, i) + lc(N - K, n - i) - lc(N, n)) for i in range(lo, hi + 1)))


class Neurons:
    """Forward pre-hooks on every mlp.down_proj: optional zero mask on its input, optional reader fn(layer, input)."""
    def __init__(self, model):
        self.mlps = [layer.mlp for layer in model.model.layers]
        self.width, self.mask, self.fn = self.mlps[0].down_proj.in_features, {}, None
        for i, m in enumerate(self.mlps):
            m.down_proj.register_forward_pre_hook(self._hook(i))

    def _hook(self, i):
        def h(_mod, args):
            x = args[0] * self.mask[i] if i in self.mask else args[0]
            if self.fn is not None:
                self.fn(i, x)
            return (x,)
        return h

    def ablate(self, flat_ids):   # flat id = layer * width + index
        self.mask = {}
        for f in flat_ids:
            self.mask.setdefault(int(f) // self.width, torch.ones(self.width))[int(f) % self.width] = 0.0

    def read(self, model, ids, take, bs=25):
        """Run model.model on ids in batches; take(x) per layer -> per-layer outputs, concatenated on the last axis."""
        got = {}
        self.fn = lambda i, x: got.setdefault(i, []).append(take(x.detach().float()))
        with torch.no_grad():
            for b in range(0, len(ids), bs):
                model.model(input_ids=ids[b:b + bs])
        self.fn = None
        return np.concatenate([np.concatenate(got[i]) for i in range(len(self.mlps))], axis=-1)


last_token = lambda x: x[:, -1].numpy().copy()   # (batch, width) at the prompt's last token


def encode(tok, texts):
    return torch.tensor([tok(t, add_special_tokens=False)["input_ids"] for t in texts])  # equal lengths or raises


def c2_problems(P):
    ab = np.random.default_rng(P["c2_seed"]).integers(P["c2_operand_range"][0], P["c2_operand_range"][1] + 1,
                                                      size=(P["c2_problems"], 2))
    return [P["c2_template"].format(few="\n".join(P["few_shot"]), a=a, b=b) for a, b in ab], [str(a + b) for a, b in ab]


def greedy(model, ids, n):
    """Plain argmax decode with KV cache (no generation_config), n new tokens."""
    out, past, x = [], None, ids
    with torch.no_grad():
        for _ in range(n):
            o = model(input_ids=x, past_key_values=past, use_cache=True, logits_to_keep=1)
            past, x = o.past_key_values, o.logits[:, -1:].argmax(-1)
            out.append(x)
    return torch.cat(out, 1)


def addition_acc(model, tok, N, P, ablate):
    (texts, gold), got, bs = c2_problems(P), [], P["c2_batch"]
    ids = encode(tok, texts)
    N.ablate(ablate)
    for b in range(0, len(ids), bs):
        got += [re.match(r"\d*", tok.decode(r)).group() for r in greedy(model, ids[b:b + bs], P["c2_max_new_tokens"])]
    N.ablate([])
    return sum(g == y for g, y in zip(got, gold)) / len(gold), got[:10]


def wait_box(P):
    while True:
        avail = int(next(l for l in open("/proc/meminfo") if l.startswith("MemAvailable:")).split()[1]) // 1024
        psi = float(open("/proc/pressure/memory").read().split()[1].split("=")[1])
        print(f"box: avail {avail} MiB, memory psi some avg10 {psi}", flush=True)
        if avail >= P["box_min_avail_mib"] and psi < P["box_max_psi_some_avg10"]:
            return
        time.sleep(30)


def load_doc(tok, P):
    text = open(os.path.join(os.path.dirname(paths.get(P["c3_text_cell"])), P["c3_text_file"]), encoding="utf-8").read()
    parts, (idx, title) = re.split(r"(?m)^ = ([^=].*?) = \n", text), P["c3_doc"]
    assert parts[1::2][idx] == title, (idx, parts[1::2][idx], title)
    ids = tok(parts[2::2][idx], add_special_tokens=False)["input_ids"]
    assert len(ids) >= P["c3_L"], len(ids)
    return torch.tensor([ids[:P["c3_L"]]])


def main(twin):
    out = paths.get_local("osc_neuron_period_dir")
    P, part = json.load(open(os.path.join(out, "params.json"))), os.path.join(out, "partial")
    os.makedirs(part, exist_ok=True)
    torch.set_num_threads(P["threads"])
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    hfdir, t0 = paths.get(P["model_cell"]), time.time()
    tok = AutoTokenizer.from_pretrained(hfdir)
    wait_box(P)
    torch.manual_seed(P["twin_seed"])   # seeds the twin's init; inert for the pretrained load
    model = (AutoModelForCausalLM.from_config(AutoConfig.from_pretrained(hfdir), dtype=torch.float32) if twin
             else AutoModelForCausalLM.from_pretrained(hfdir, dtype=torch.float32)).eval()
    N = Neurons(model)
    ids = encode(tok, [P["c1_template"].format(few="\n".join(P["few_shot"]), a=a) for a in range(*P["c1_a"])])
    assert len(set(ids[:, -1].tolist())) == 1, "last token differs across a"
    if twin:
        pk = peakiness(N.read(model, ids, last_token))[0]
        json.dump({"P": P, "max": float(pk.max()), "q999": float(np.quantile(pk, 0.999)), "n": int(pk.size),
                   "layer_max": pk.reshape(-1, N.width).max(1).tolist()}, open(os.path.join(part, "twin.json"), "w"))
        return print(f"twin max peakiness {pk.max():.4f} ({time.time() - t0:.0f}s)", flush=True)
    tw = json.load(open(os.path.join(part, "twin.json")))   # missing twin -> crash, never a silent skip
    assert tw["P"] == P, "twin.json belongs to another grid"
    f1, f2, f3 = (os.path.join(part, f) for f in ("c1_acts.npy", "c2.json", "c3.npz"))
    if not os.path.exists(f1):
        np.save(f1, N.read(model, ids, last_token))
    acts = np.load(f1)
    nl, A, pkN = len(N.mlps), acts.shape[0], acts.shape[1]
    grid_ok = N.width == 4864 and nl == 24 and acts.shape == (100, nl * N.width) and tw["n"] == pkN
    pk, kbin = peakiness(acts)
    null = shuffled_null(acts, P["c1_null_permutations"], P["c1_null_seed"])
    q = float(np.quantile(null, P["c1_null_quantile"]))
    c1, order = np.flatnonzero((pk > q) & (pk > tw["max"])), np.argsort(-pk, kind="stable")
    frac = len(c1) / pkN
    acc = json.load(open(f2)) if os.path.exists(f2) else {}
    arms = {"baseline": [], "top": [int(i) for i in order[:P["c2_k"]]], **{f"random_s{s}": sorted(
        int(x) for x in np.random.default_rng(s).choice(pkN, P["c2_k"], replace=False)) for s in P["c2_random_seeds"]}}
    for name, ab in arms.items():
        if name not in acc:
            acc[name] = addition_acc(model, tok, N, P, ab)
            json.dump(acc, open(f2, "w"))
        print(f"C2 {name}: acc {acc[name][0]:.4f} ({time.time() - t0:.0f}s)", flush=True)
    if not os.path.exists(f3):
        doc = load_doc(tok, P)
        shuf = doc[:, torch.from_numpy(np.random.default_rng(P["c3_shuffle_seed"]).permutation(doc.shape[1]))]
        take = lambda x: peakiness(x[0, P["c3_skip"]:].numpy())[0][None]
        np.savez(f3, orig=N.read(model, doc, take)[0], shuf=N.read(model, shuf, take)[0])
    z = np.load(f3)
    s3, n3 = z["orig"] - z["shuf"], int(P["c3_top_fraction"] * pkN)
    top3 = np.argsort(-s3, kind="stable")[:n3]
    ov = int(np.isin(top3, c1).sum())
    p3 = hyper_sf(ov, pkN, len(c1), n3)
    rnd = {a: acc[a][0] for a in arms if a.startswith("random")}
    base, top64 = acc["baseline"][0], acc["top"][0]
    c2_void, c1_pass = base < P["c2_min_baseline"], frac >= P["c1_min_fraction"]
    c2_pass = (not c2_void) and top64 < min(rnd.values())
    void = not (grid_ok and null.shape == (P["c1_null_permutations"], pkN))
    verdict = ("void" if void else "disproved" if not c1_pass or (not c2_void and not c2_pass)
               else "inconclusive" if c2_void else "proved")
    hist, per = np.bincount(kbin[c1], minlength=A // 2 + 1), (lambda k: round(A / int(k), 2))
    row = lambda i: {"id": int(i), "layer": int(i) // N.width, "index": int(i) % N.width,
                     "peakiness": round(float(pk[i]), 4), "k": int(kbin[i]), "period": per(kbin[i])}
    c = {"pass": bool(c1_pass), "count": len(c1), "fraction": frac, "null_q999": q, "null_n": int(null.size),
         "twin_max": tw["max"], "twin_q999": tw["q999"], "twin_layer_max": tw["layer_max"],
         "count_beat_null": int((pk > q).sum()), "count_beat_twin": int((pk > tw["max"]).sum()),
         "per_layer": np.bincount(c1 // N.width, minlength=nl).tolist(), "top": [row(i) for i in order[:40]],
         "period_hist": [{"k": int(k), "period": per(k), "n": int(hist[k])} for k in np.argsort(-hist)[:10] if hist[k]],
         "set": c1[:20000].tolist()}
    d = {"void": bool(c2_void), "pass": bool(c2_pass), "baseline": base, "top64": top64, "random": rnd,
         "random_min": min(rnd.values()), "random_max": max(rnd.values()), "arms": arms,
         "samples": {a: v[1] for a, v in acc.items()}}
    e = {"pass": bool(p3 < P["c3_alpha"]), "overlap": ov, "draws": n3, "successes": len(c1), "p": p3,
         "expected": n3 * len(c1) / pkN, "top_ids": top3[:200].tolist(), "top_score": s3[top3[:20]].round(4).tolist(),
         "mean_orig": float(z["orig"].mean()), "mean_shuf": float(z["shuf"].mean())}
    json.dump({"verdict": verdict, "void": void, "grid_ok": grid_ok, "n_neurons": pkN, "c1": c, "c2": d, "c3": e,
               "wall_s": round(time.time() - t0, 1), "torch": torch.__version__},
              open(os.path.join(out, "results.json"), "w"), indent=1)
    shutil.rmtree(part)
    tag = lambda ok, v=False: "void" if v else "pass" if ok else "fail"
    lines = [f"# Neuron periodicity MAP: {verdict}", "", f"grid 24 x 4864 ok: {grid_ok}; void: {void}", "",
             f"C1 ({tag(c1_pass)}): {len(c1)} / {pkN} = {frac:.5f} clear BOTH null q999 {q:.4f} and twin max "
             f"{tw['max']:.4f} (need >= {P['c1_min_fraction']}); beat null {c['count_beat_null']}, beat twin "
             f"{c['count_beat_twin']}", "periods (C1 set): " + ", ".join(f"T{h['period']} x{h['n']}" for h in
                                                                       c["period_hist"]),
             "top: " + ", ".join(f"L{r['layer']}.{r['index']} {r['peakiness']} T{r['period']}" for r in c["top"][:8]),
             f"per layer: {c['per_layer']}", "", f"C2 ({tag(c2_pass, c2_void)}): baseline {base:.4f}; top-64 "
             f"{top64:.4f}; random min-max {d['random_min']:.4f}-{d['random_max']:.4f}", "",
             f"C3 ({tag(e['pass'])}, scored separately): overlap {ov} of top {n3} with C1 set {len(c1)} "
             f"(expected {e['expected']:.2f}); hypergeometric p {p3:.3g}"]
    open(os.path.join(out, "summary.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)


if __name__ == "__main__":
    main("--twin" in sys.argv[1:])
