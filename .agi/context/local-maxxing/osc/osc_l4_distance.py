#!/usr/bin/env python3
# L4 run 2 (hypothesis:lm-l4-measured-distance-heads-keep-a-recent-window): KV heads by MEASURED sink-free attention
# distance (3 calibration docs) keep sinks + last W, vs run 1's random arms (same heads) and band arm. Loader / mask /
# kept_fraction / scoring IMPORTED from osc_l4_window.py. Grid: <cell osc_band_l4_distance_dir>/params.json (inherits
# run 1's params.json keys by cell); outputs beside it. Run detached: PYTHONPATH=<osc_test_pythonpath> <ml_python> this.
import hashlib, json, os, subprocess, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import osc_l4_window as W  # noqa: E402  (puts the local-maxxing dir on sys.path)
import paths  # noqa: E402

DIST = {"on": False, "sinks": 4, "lo": 0, "hi": 0, "d": {}}


def sink_free_distance(w, lo, hi, sinks):
    # (nq, T, K) weights -> per q head, mean over rows lo..hi-1 of sum_{sinks <= j <= t} w[t, j] * (t - j).
    # Sink keys contribute 0, nothing is renormalised: a head attending only to sinks has distance 0.
    t, j = torch.arange(lo, hi)[:, None].float(), torch.arange(w.shape[-1])[None, :]
    return (w[:, lo:hi] * ((t - j).clamp_min(0) * (j >= sinks))).double().sum(-1).mean(-1)


def attn(module, query, key, value, attention_mask, scaling, dropout=0.0, **kw):
    out, w = W.attn(module, query, key, value, attention_mask, scaling, dropout, **kw)
    if DIST["on"]:
        DIST["d"][module.layer_idx] = sink_free_distance(w[0], DIST["lo"], DIST["hi"], DIST["sinks"])
    return out, w


def spearman(a, b):
    return float(np.corrcoef(*(np.argsort(np.argsort(x, kind="stable"), kind="stable") for x in (a, b)))[0, 1])


def ranking(dists):
    # KV heads by the mean over calibration docs of their sink-free distance, ascending; ties by index.
    m = np.mean(np.asarray(dists, dtype=float), 0)
    return sorted(range(len(m)), key=lambda i: (m[i], i)), m.tolist()


def load_params(out):
    P = json.load(open(os.path.join(out, "params.json")))
    base = json.load(open(os.path.join(paths.get_local(P["run1_cell"]), "params.json")))
    return {**{k: base[k] for k in P["inherit"]}, **P}


def dump(out, res, lines):
    json.dump(res, open(os.path.join(out, "results.json"), "w"), indent=1)
    open(os.path.join(out, "summary.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps({k: res.get(k) for k in ("verdict", "budget_wins", "spearman", "wall_s")}), flush=True)


def main():
    P, t0 = load_params(out := paths.get_local("osc_band_l4_distance_dir")), time.time()
    R1 = json.load(open(os.path.join(paths.get_local(P["run1_cell"]), "results.json")))
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a, "--", __file__], capture_output=True, text=True)  # noqa
    commit, dirty = git("log", "-1", "--format=%H").stdout.strip(), git("diff", "--quiet", "HEAD").returncode != 0
    torch.set_num_threads(P["threads"])
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import transformers.models.qwen2.modeling_qwen2 as M
    tok = AutoTokenizer.from_pretrained(paths.get(P["model_cell"]))
    model = AutoModelForCausalLM.from_pretrained(paths.get(P["model_cell"]), dtype=torch.float32,
                                                 attn_implementation="eager").eval()
    W.install(M)
    M.eager_attention_forward = attn
    c = model.config
    nkv, group, nl = c.num_key_value_heads, c.num_attention_heads // c.num_key_value_heads, c.num_hidden_layers
    n, L, lo, hi, N = nl * nkv, P["L"], P["score_lo"], P["score_hi"], P["score_hi"] - P["score_lo"]
    W.S["bad"], W.S["win"] = W.disallow(L, P["W"], P["sinks"]), {}
    DIST.update(sinks=P["sinks"], lo=lo, hi=hi)
    cal, ev = [d for d, _ in P["calib_docs"]], [d for d, _ in P["eval_docs"]]
    leak = bool(set(cal) & (set(ev) | set(P["exclude_docs"])))
    docs = W.load_docs(tok, dict(P, eval_docs=P["eval_docs"] + P["calib_docs"][1:], calib_doc=P["calib_docs"][0]))

    def hidden(ids):
        with torch.no_grad():
            return model.model(input_ids=ids).last_hidden_state[0, lo:hi].clone()

    dists, DIST["on"] = [], True
    for d in cal:
        hidden(docs[d])   # every layer overwrites DIST["d"][layer]
        dists.append([float(DIST["d"][i // nkv][(i % nkv) * group:(i % nkv + 1) * group].mean()) for i in range(n)])
    DIST["on"] = False
    rho = {f"{cal[i]}-{cal[j]}": spearman(dists[i], dists[j]) for i in range(3) for j in range(i + 1, 3)}
    rank, mean_dist = ranking(dists)
    res = {"P": P, "script_commit": commit, "script_dirty": dirty, "calib_leak": leak, "spearman": rho,
           "calib_dist": dists, "mean_dist": mean_dist, "distance_ranking": rank, "torch": torch.__version__}
    head = f"calibration Spearman {json.dumps(rho)}; calib leak {leak}; script {commit} dirty {dirty}"
    if min(rho.values()) < P["min_spearman"]:   # precondition failed: stop before scoring
        res.update(verdict="inconclusive", wall_s=round(time.time() - t0, 1))
        return dump(out, res, ["# L4 distance round: inconclusive (Spearman < min_spearman)", "", head])
    ks = dict(zip(map(str, P["budgets"]), P["k"]))
    kept = {b: W.kept_fraction(k, P["W"], P["sinks"], L, n) for b, k in ks.items()}
    arms = {b: {"distance": rank[:k], **{a: h for a, h in R1["arms"][b].items() if a != "ref"}} for b, k in ks.items()}
    same_k = all(len(h) == ks[b] for b in arms for h in arms[b].values())   # one W, one mask for every arm
    kept_ok = all(kept[b] == R1["table"][b]["kept"] for b in arms)
    r1 = {(r["doc"], r["budget"], r["arm"]): (r["agree"], r["kl"]) for r in R1["per_doc"]}
    part = os.path.join(out, "partial.json")   # per-doc checkpoint: a PSI stop costs one doc, not the round
    st = json.load(open(part)) if os.path.exists(part) else {"P": P, "arms": arms, "done": [], "per_doc": [],
                                                             "repro": True, "ref_match": True, "h_sha256": {}}
    assert st["P"] == P and st["arms"] == arms, "partial.json belongs to another grid"
    res["docs_resumed_from_checkpoint"] = list(st["done"])
    for d in [d for d in ev if d not in st["done"]]:
        W.S["win"] = {}
        h1, h2 = hidden(docs[d]), hidden(docs[d])
        st["repro"] &= bool(torch.equal(h1, h2))
        st["h_sha256"][str(d)] = hashlib.sha256(h1.numpy().tobytes()).hexdigest()
        for b, A in arms.items():
            for a, heads in A.items():
                W.S["win"] = W.as_win(heads, nkv)
                with torch.no_grad():   # run 1 residue: lm_head now under no_grad
                    ag, kl = W.score(model, h1, hidden(docs[d]), P["lm_head_chunk"])
                row = {"doc": d, "budget": b, "arm": a, "agree": ag / N, "kl": kl / N}
                if a != "distance":   # band / random rerun must equal run 1 digit for digit (same full-KV reference)
                    st["ref_match"] &= r1[(d, b, a)] == (row["agree"], row["kl"])
                st["per_doc"].append(row)
                print(f"{time.time() - t0:7.0f}s doc {d} b {b} {a} agree {ag / N:.4f} kl {kl / N:.5f}", flush=True)
        st["done"].append(d)
        json.dump(st, open(part, "w"))
    table = {}
    for b, A in arms.items():   # pooled exactly as run 1: sum of per-doc totals / (docs * N)
        row = {a: {m: sum(r[m] * N for r in st["per_doc"] if (r["budget"], r["arm"]) == (b, a)) / (N * len(ev))
                   for m in ("agree", "kl")} for a in A}
        rmin, rmax = ({m: f(v[m] for a, v in row.items() if a.startswith("random")) for m in ("agree", "kl")}
                      for f in (min, max))
        win = row["distance"]["agree"] > rmax["agree"] and row["distance"]["kl"] < rmin["kl"]
        table[b] = {"arms": row, "random_min": rmin, "random_max": rmax, "distance_wins": win, "kept": kept[b]}
    wins, void = sum(t["distance_wins"] for t in table.values()), leak or not (same_k and kept_ok and st["repro"])
    verdict = "void" if void or not st["ref_match"] else ("proved" if wins >= P["min_budget_wins"] else "disproved")
    res.update(verdict=verdict, budget_wins=wins, same_k=same_k, kept_equals_run1=kept_ok, full_repro_bitexact=st[
        "repro"], ref_matches_run1=st["ref_match"], full_h_sha256=st["h_sha256"], table=table, arms=arms, per_doc=st[
        "per_doc"], n_scored_per_doc=N, wall_s=round(time.time() - t0, 1))
    lines = [f"# L4 distance round: {verdict} (distance wins {wins}/{len(arms)} budgets, needs "
             f"{P['min_budget_wins']})", "", head, "", f"void checks: same k {same_k}; kept == run 1 "
             f"{kept_ok}; full-KV bit-exact x2 {st['repro']}; band+random == run 1 per doc {st['ref_match']}", "",
             "| budget | k | kept | distance agree | random agree min-max | band agree | distance KL | random KL "
             "min-max | band KL | distance wins |", "|---|---|---|---|---|---|---|---|---|---|"]
    for b, r in table.items():
        a, mn, mx = r["arms"], r["random_min"], r["random_max"]
        v = [f"{a['distance'][m]:{f}} | {mn[m]:{f}}-{mx[m]:{f}} | {a['band'][m]:{f}}" for m, f in (("agree", ".4f"),
                                                                                                 ("kl", ".5f"))]
        lines.append(f"| {b} | {ks[b]} | {r['kept']:.4f} | {v[0]} | {v[1]} | {r['distance_wins']} |")
    dump(out, res, lines)
    os.remove(part)


if __name__ == "__main__":
    main()
