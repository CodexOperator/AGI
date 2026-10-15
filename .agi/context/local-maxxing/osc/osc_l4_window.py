#!/usr/bin/env python3
"""L4 (hypothesis:lm-l4-local-heads-keep-a-recent-window): windowed KV heads keep keys {0..sinks-1} U {t-W+1..t},
one mask per GQA group. Arms band / random / ref; grid = <cell osc_band_l4_dir>/params.json, outputs beside it.
Run: PYTHONPATH="$(paths.py osc_test_pythonpath)" "$(paths.py ml_python)" osc_l4_window.py (detached, see CEILING).
"""
import json, os, re, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import paths  # noqa: E402

S = {"win": {}, "bad": None, "dist": None, "lo": 0, "hi": 0}   # layer -> windowed kv heads
ORIG = {}


def disallow(T, W, sinks):
    """Bool (T, T): True where a windowed head's query t may NOT see key j (includes j > t)."""
    t, j = torch.arange(T)[:, None], torch.arange(T)[None, :]
    return ~((j <= t) & ((j < sinks) | (j > t - W)))


def window_mask(mask, heads, nq, group, bad):
    """Expand the (B,1,T,K) additive causal mask to (B,nq,T,K); window every q head of each listed kv head."""
    B, _, T, K = mask.shape
    m = mask.expand(B, nq, T, K).clone()
    for g in heads:
        m[:, g * group:(g + 1) * group].masked_fill_(bad[:T, :K], torch.finfo(m.dtype).min)
    return m


def attn(module, query, key, value, attention_mask, scaling, dropout=0.0, **kw):
    heads = S["win"].get(module.layer_idx, ())
    if heads:
        attention_mask = window_mask(attention_mask, heads, query.shape[1],
                                     module.num_key_value_groups, S["bad"])
    out, w = ORIG["eager"](module, query, key, value, attention_mask, scaling, dropout, **kw)
    if S["dist"] is not None:   # mean attention distance per q head over the scored rows
        t = torch.arange(S["lo"], S["hi"])[:, None].float()
        d = w[0, :, S["lo"]:S["hi"]] * (t - torch.arange(w.shape[-1])[None, :]).clamp_min(0)
        S["dist"][module.layer_idx] = d.double().sum(-1).mean(-1)
    return out, w


def install(M):
    ORIG.setdefault("eager", M.eager_attention_forward)
    M.eager_attention_forward = attn


def kept_fraction(k, W, sinks, L, n):
    return (n - k + k * min(L, W + sinks) / L) / n


def kv_ranking(profiles, high, n_layers, n_kv, group):
    """KV heads (index L*n_kv+g) by the mean over their query group of the high-band share, desc; ties by index."""
    share = [float(np.mean([sum(profiles[f"L{L}H{g * group + j}"]["profile_pooled"][p] for p in high)
                            for j in range(group)])) for L in range(n_layers) for g in range(n_kv)]
    return sorted(range(len(share)), key=lambda i: (-share[i], i)), share


def load_docs(tok, P):
    text = open(os.path.join(os.path.dirname(paths.get(P["text_cell"])), P["text_file"]), encoding="utf-8").read()
    parts = re.split(r"(?m)^ = ([^=].*?) = \n", text)
    arts = list(zip(parts[1::2], parts[2::2]))
    out = {}
    for idx, title in P["eval_docs"] + [P["calib_doc"]]:
        assert arts[idx][0] == title, (idx, arts[idx][0], title)
        ids = tok(arts[idx][1], add_special_tokens=False)["input_ids"]
        assert len(ids) >= P["L"], (title, len(ids))
        out[idx] = torch.tensor([ids[:P["L"]]])
    return out


def as_win(heads, n_kv):
    w = {}
    for i in heads:
        w.setdefault(i // n_kv, []).append(i % n_kv)
    return w


def score(model, hf, ha, chunk):
    agree, kl = 0, 0.0
    for a in range(0, hf.shape[0], chunk):
        lf = torch.log_softmax(model.lm_head(hf[a:a + chunk]).double(), -1)
        la = torch.log_softmax(model.lm_head(ha[a:a + chunk]).double(), -1)
        agree += int((lf.argmax(-1) == la.argmax(-1)).sum())
        kl += float((lf.exp() * (lf - la)).sum())
    return agree, kl


def main():
    out = paths.get_local("osc_band_l4_dir")
    P = json.load(open(os.path.join(out, "params.json")))
    torch.set_num_threads(P["threads"])
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import transformers.models.qwen2.modeling_qwen2 as M
    hfdir, t0 = paths.get(P["model_cell"]), time.time()
    tok = AutoTokenizer.from_pretrained(hfdir)
    model = AutoModelForCausalLM.from_pretrained(hfdir, dtype=torch.float32, attn_implementation="eager").eval()
    install(M)
    c = model.config
    nkv, group, nl = c.num_key_value_heads, c.num_attention_heads // c.num_key_value_heads, c.num_hidden_layers
    n, L, lo, hi = nl * nkv, P["L"], P["score_lo"], P["score_hi"]
    S["lo"], S["hi"], S["bad"] = lo, hi, disallow(L, P["W"], P["sinks"])
    docs = load_docs(tok, P)
    prof = json.load(open(os.path.join(paths.get_local(P["profiles_cell"]), P["profiles_file"])))["heads"]
    band, share = kv_ranking(prof, P["high_pairs"], nl, nkv, group)

    def hidden(ids):
        with torch.no_grad():
            return model.model(input_ids=ids).last_hidden_state[0, lo:hi].clone()

    S["win"], S["dist"] = {}, {}
    hidden(docs[P["calib_doc"][0]])
    dist = [float(S["dist"][i // nkv][(i % nkv) * group:(i % nkv + 1) * group].mean()) for i in range(n)]
    S["dist"] = None
    ref = sorted(range(n), key=lambda i: (dist[i], i))
    tol = 0.5 * (1 - (P["W"] + P["sinks"]) / L) / n
    arms, kept = {}, {}
    for b, k in zip(P["budgets"], P["k"]):
        kept[str(b)] = kept_fraction(k, P["W"], P["sinks"], L, n)
        arms[str(b)] = {"band": band[:k], "ref": ref[:k], **{f"random_s{s}": sorted(
            int(x) for x in np.random.default_rng(s).choice(n, k, replace=False)) for s in P["seeds"]}}
    budget_ok = all(abs(kept[str(b)] - b) <= tol for b in P["budgets"])
    part = os.path.join(out, "partial.json")   # per-doc checkpoint: a PSI stop costs one doc, not the round
    st = json.load(open(part)) if os.path.exists(part) else {
        "P": P, "arms": arms, "done": [], "per_doc": [], "repro": True, "wl_exact": None,
        "acc": {b: {a: [0, 0.0, 0] for a in A} for b, A in arms.items()}}
    assert st["P"] == P and st["arms"] == arms, "partial.json belongs to another grid"
    acc, per_doc, resumed = st["acc"], st["per_doc"], list(st["done"])
    for d, _ in P["eval_docs"]:
        if d in st["done"]:
            continue
        S["win"] = {}
        h1, h2 = hidden(docs[d]), hidden(docs[d])
        st["repro"] &= bool(torch.equal(h1, h2))
        if st["wl_exact"] is None:   # test 1 on the real model: every head windowed at W = L equals full
            S["bad"], S["win"] = disallow(L, L, P["sinks"]), as_win(range(n), nkv)
            st["wl_exact"] = bool(torch.equal(hidden(docs[d]), h1))
            S["bad"] = disallow(L, P["W"], P["sinks"])
        for b, A in arms.items():
            for a, heads in A.items():
                S["win"] = as_win(heads, nkv)
                ag, kl = score(model, h1, hidden(docs[d]), P["lm_head_chunk"])
                acc[b][a] = [acc[b][a][0] + ag, acc[b][a][1] + kl, acc[b][a][2] + (hi - lo)]
                per_doc.append({"doc": d, "budget": b, "arm": a, "agree": ag / (hi - lo), "kl": kl / (hi - lo)})
                print(f"{time.time() - t0:7.0f}s doc {d} b {b} {a} agree {ag / (hi - lo):.4f} kl {kl / (hi - lo):.5f}",
                      flush=True)
        st["done"].append(d)
        json.dump(st, open(part, "w"))
    repro, wl_exact = st["repro"], st["wl_exact"]
    table, wins = {}, 0
    for b, A in acc.items():
        row = {a: {"agree": v[0] / v[2], "kl": v[1] / v[2]} for a, v in A.items()}
        rnd = [row[a] for a in row if a.startswith("random")]
        rmin = {m: min(r[m] for r in rnd) for m in ("agree", "kl")}
        rmax = {m: max(r[m] for r in rnd) for m in ("agree", "kl")}
        win = row["band"]["agree"] > rmax["agree"] and row["band"]["kl"] < rmin["kl"]
        wins += win
        table[b] = {"arms": row, "random_min": rmin, "random_max": rmax, "band_wins": win, "kept": kept[b]}
    void = not (budget_ok and repro and wl_exact)
    verdict = "void" if void else ("proved" if wins >= P["min_budget_wins"] else "disproved")
    res = {"verdict": verdict, "budget_wins": wins, "budget_ok": budget_ok, "kept_tol": tol,
           "full_repro_bitexact": repro, "w_ge_L_exact": wl_exact, "table": table, "arms": arms,
           "band_share": share, "calib_mean_dist": dist, "per_doc": per_doc, "n_scored_per_doc": hi - lo,
           "docs_resumed_from_checkpoint": resumed,
           "wall_s": round(time.time() - t0, 1), "torch": torch.__version__}
    json.dump(res, open(os.path.join(out, "results.json"), "w"), indent=1)
    os.remove(part)
    lines = [f"# L4 window round: {verdict} (band wins {wins}/{len(acc)} budgets, needs {P['min_budget_wins']})", "",
             f"void checks: kept within +-{tol:.5f}: {budget_ok}; full-KV bit-exact x2: {repro}; W=L exact: {wl_exact}",
             "", "| budget | k | kept | band agree | random agree min-max | ref agree | band KL | random KL min-max "
             "| ref KL | band wins |", "|---|---|---|---|---|---|---|---|---|---|"]
    for (b, r), k in zip(table.items(), P["k"]):
        a = r["arms"]
        lines.append(f"| {b} | {k} | {r['kept']:.4f} | {a['band']['agree']:.4f} | {r['random_min']['agree']:.4f}-"
                     f"{r['random_max']['agree']:.4f} | {a['ref']['agree']:.4f} | {a['band']['kl']:.5f} | "
                     f"{r['random_min']['kl']:.5f}-{r['random_max']['kl']:.5f} | {a['ref']['kl']:.5f} | {r['band_wins']} |")
    open(os.path.join(out, "summary.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps({k: res[k] for k in ("verdict", "budget_wins", "budget_ok", "full_repro_bitexact",
                                          "w_ge_L_exact", "wall_s")}), flush=True)


if __name__ == "__main__":
    main()
