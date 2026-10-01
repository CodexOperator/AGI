#!/usr/bin/env python3
# L4 run 3 (hypothesis:lm-l4-outside-window-mass-picks-the-heads-to-window): KV heads by MEASURED attention MASS on the
# keys a sinks + last-W window drops (3 calibration docs), the k LOWEST windowed, vs run 1's random arms (rerun here).
# Reported: DIRECT (each KV head windowed alone, its KL) and run 1's sink-COUNTING distance; band (run 1) and run 2's
# distance per-doc results are reused when the full-KV reference and the random arms reproduce bit for bit.
# Loader / mask / kept_fraction / scoring / attention capture / spearman / ranking IMPORTED from osc_l4_window.py and
# osc_l4_distance.py (both unchanged). Grid: <cell osc_band_l4_mass_dir>/params.json; outputs beside it.
# Run detached: PYTHONPATH=<osc_test_pythonpath> <ml_python> this.
import hashlib, json, os, subprocess, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import osc_l4_window as W  # noqa: E402  (puts the local-maxxing dir on sys.path)
import osc_l4_distance as D  # noqa: E402
import paths  # noqa: E402

MASS = {"on": False, "m": {}}
REUSE = ("band", "distance")


def mass_outside(w, bad, lo, hi):
    # (nq, T, K) weights -> per q head, mean over query rows lo..hi-1 of the weight on keys the window drops:
    # bad = W.disallow(T, W, sinks) is True for sinks <= j <= t - W (and for j > t, where the weight is 0).
    return (w[:, lo:hi] * bad[lo:hi, :w.shape[-1]]).double().sum(-1).mean(-1)


def attn(module, query, key, value, attention_mask, scaling, dropout=0.0, **kw):
    out, w = W.attn(module, query, key, value, attention_mask, scaling, dropout, **kw)   # also run 1's distance hook
    if MASS["on"]:
        MASS["m"][module.layer_idx] = mass_outside(w[0], W.S["bad"], W.S["lo"], W.S["hi"])
    return out, w


def load_params(out):
    P = D.load_params(out)   # run 1's keys by cell
    r2 = json.load(open(os.path.join(paths.get_local(P["run2_cell"]), "params.json")))
    return {**{k: r2[k] for k in P["inherit_run2"]}, **P}


def hidden(model, ids, lo, hi, win=None):
    W.S["win"] = win or {}   # full KV unless a window dict {layer: [kv heads]} is given
    with torch.no_grad():
        return model.model(input_ids=ids).last_hidden_state[0, lo:hi].clone()


def scored(model, h_full, ids, heads, nkv, lo, hi, chunk):
    # window `heads` with W.S["bad"], rerun, score vs h_full -> (agree, kl) per scored position
    with torch.no_grad():   # lm_head under no_grad
        ag, kl = W.score(model, h_full, hidden(model, ids, lo, hi, W.as_win(heads, nkv)), chunk)
    return ag / (hi - lo), kl / (hi - lo)


per_kv = lambda x, n, nkv, g: [float(x[i // nkv][(i % nkv) * g:(i % nkv + 1) * g].mean()) for i in range(n)]  # noqa
rhos = lambda v, cal: {f"{cal[i]}-{cal[j]}": D.spearman(v[i], v[j]) for i in range(3) for j in range(i + 1, 3)}  # noqa


def dump(out, res, lines):
    json.dump(res, open(os.path.join(out, "results.json"), "w"), indent=1)
    open(os.path.join(out, "summary.md"), "w").write("\n".join(lines) + "\n")


def main():
    P, t0 = load_params(out := paths.get_local("osc_band_l4_mass_dir")), time.time()
    psha = hashlib.sha256(open(os.path.join(out, "params.json"), "rb").read()).hexdigest()
    R1, R2 = (json.load(open(os.path.join(paths.get_local(P[c]), "results.json"))) for c in ("run1_cell", "run2_cell"))
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
    nkv, g, nl = c.num_key_value_heads, c.num_attention_heads // c.num_key_value_heads, c.num_hidden_layers
    n, L, lo, hi, ch = nl * nkv, P["L"], P["score_lo"], P["score_hi"], P["lm_head_chunk"]
    W.S.update(bad=W.disallow(L, P["W"], P["sinks"]), win={}, lo=lo, hi=hi)
    cal, ev = [d for d, _ in P["calib_docs"]], [d for d, _ in P["eval_docs"]]
    leak = bool(set(cal) & (set(ev) | set(P["exclude_docs"])))
    docs = W.load_docs(tok, dict(P, eval_docs=P["eval_docs"] + P["calib_docs"][1:], calib_doc=P["calib_docs"][0]))
    masses, sdist, hf, MASS["on"], W.S["dist"] = [], [], {}, True, {}
    for d in cal:   # one full-KV pass per calibration doc captures mass AND run 1's sink-counting distance
        hf[d] = hidden(model, docs[d], lo, hi)
        masses.append(per_kv(MASS["m"], n, nkv, g))
        sdist.append(per_kv(W.S["dist"], n, nkv, g))
    MASS["on"], W.S["dist"] = False, None
    rho = rhos(masses, cal)
    (rank, mean_mass), (srank, mean_sdist) = D.ranking(masses), D.ranking(sdist)
    res = {"P": P, "params_sha256": psha, "script_commit": commit, "script_dirty": dirty, "calib_leak": leak,
           "spearman": rho, "calib_mass": masses, "mean_mass": mean_mass, "mass_ranking": rank,
           "sinkcount_spearman": rhos(sdist, cal), "mean_sinkcount": mean_sdist, "sinkcount_ranking": srank}
    head = f"calibration Spearman (mass) {json.dumps(rho)}; calib leak {leak}; script {commit} dirty {dirty}"
    if min(rho.values()) < P["min_spearman"]:   # precondition failed: stop before scoring
        res.update(verdict="inconclusive", wall_s=round(time.time() - t0, 1))
        return dump(out, res, ["# L4 mass round: inconclusive (mass Spearman < min_spearman)", "", head])
    part = os.path.join(out, "partial.json")   # checkpoint per DIRECT head and per eval doc
    st = json.load(open(part)) if os.path.exists(part) else {"P": P, "direct": {}, "done": [], "per_doc": [],
                                                             "repro": True, "ref_match": True, "h_sha256": {}}
    assert st["P"] == P, "partial.json belongs to another grid"
    res["docs_resumed_from_checkpoint"], res["direct_heads_resumed"] = list(st["done"]), len(st["direct"])
    for h in [h for h in range(n) if str(h) not in st["direct"]]:
        st["direct"][str(h)] = [scored(model, hf[d], docs[d], [h], nkv, lo, hi, ch)[1] for d in cal]
        print(f"{time.time() - t0:7.0f}s direct head {h} kl {st['direct'][str(h)]}", flush=True)
        json.dump(st, open(part, "w"))
    direct = np.asarray([st["direct"][str(h)] for h in range(n)]).T.tolist()   # 3 x n
    drank, mean_dkl = D.ranking(direct)
    res.update(direct_kl=direct, mean_direct_kl=mean_dkl, direct_ranking=drank, direct_spearman=rhos(direct, cal),
               spearman_mass_vs={"direct": D.spearman(mean_mass, mean_dkl), "sinkcount": D.spearman(
                   mean_mass, mean_sdist), "distance": D.spearman(mean_mass, R2["mean_dist"])})
    ks = dict(zip(map(str, P["budgets"]), P["k"]))
    kept = {b: W.kept_fraction(k, P["W"], P["sinks"], L, n) for b, k in ks.items()}
    arms = {b: {"mass": rank[:k], "direct": drank[:k], "sinkcount": srank[:k], "distance": R2["arms"][b]["distance"],
                **{a: h for a, h in R1["arms"][b].items() if a != "ref"}} for b, k in ks.items()}
    same_k = all(len(h) == ks[b] for b in arms for h in arms[b].values())   # one W, one mask for every arm
    kept_ok = all(kept[b] == R1["table"][b]["kept"] == R2["table"][b]["kept"] for b in arms)
    old = {(r["doc"], r["budget"], r["arm"]): (r["agree"], r["kl"]) for R in (R1, R2) for r in R["per_doc"]
           if r["arm"] != "ref" and (r["arm"] == "distance") == (R is R2)}   # band/random: run 1; distance: run 2
    for d in [d for d in ev if d not in st["done"]]:
        h1, h2 = hidden(model, docs[d], lo, hi), hidden(model, docs[d], lo, hi)
        st["repro"] &= bool(torch.equal(h1, h2))
        st["h_sha256"][str(d)] = hashlib.sha256(h1.numpy().tobytes()).hexdigest()
        got, cache = {}, {}
        for b, A in arms.items():   # scored + reported + random arms first; identical head sets run once
            for a in [a for a in A if a not in REUSE]:
                key = (b, tuple(A[a]))
                got[(b, a)] = cache[key] = cache.get(key) or scored(model, h1, docs[d], A[a], nkv, lo, hi, ch)
                print(f"{time.time() - t0:7.0f}s doc {d} b {b} {a} agree, kl {got[(b, a)]}", flush=True)
        ok = st["h_sha256"][str(d)] == R2["full_h_sha256"][str(d)] and all(
            got[(b, a)] == old[(d, b, a)] for b, a in got if a.startswith("random"))
        st["ref_match"] &= ok
        for b, a in [(b, a) for b in arms for a in REUSE]:   # reused only when the reference reproduced; else rerun
            got[(b, a)] = old[(d, b, a)] if ok else scored(model, h1, docs[d], arms[b][a], nkv, lo, hi, ch)
        st["per_doc"] += [{"doc": d, "budget": b, "arm": a, "agree": v[0], "kl": v[1], "reused": a in REUSE and ok}
                          for (b, a), v in got.items()]
        st["done"].append(d)
        json.dump(st, open(part, "w"))
    N, table = hi - lo, {}
    for b, A in arms.items():   # pooled exactly as runs 1/2: sum of per-doc totals / (docs * N)
        row = {a: {m: sum(r[m] * N for r in st["per_doc"] if (r["budget"], r["arm"]) == (b, a)) / (N * len(ev))
                   for m in ("agree", "kl")} for a in A}
        rmin, rmax = ({m: f(v[m] for a, v in row.items() if a.startswith("random")) for m in ("agree", "kl")}
                      for f in (min, max))
        table[b] = {"arms": row, "random_min": rmin, "random_max": rmax, "kept": kept[b],
                    "beats_random": row["mass"]["agree"] > rmax["agree"] and row["mass"]["kl"] < rmin["kl"],
                    "kl_below_distance": row["mass"]["kl"] < row["distance"]["kl"]}
    rw, dw = (sum(t[x] for t in table.values()) for x in ("beats_random", "kl_below_distance"))
    void = leak or not (same_k and kept_ok and st["repro"] and st["ref_match"])
    res.update(verdict="void" if void else ["disproved", "proved"][rw >= P["need_random_wins"] and dw >= P[
        "need_distance_kl_wins"]], random_wins=rw, distance_kl_wins=dw, same_k=same_k, kept_equals_run1_run2=kept_ok,
        full_repro_bitexact=st["repro"], ref_matches_run1_run2=st["ref_match"], full_h_sha256=st["h_sha256"],
        table=table, arms=arms, per_doc=st["per_doc"], n_scored_per_doc=N, wall_s=round(time.time() - t0, 1))
    lines = [f"# L4 mass round: {res['verdict']} (MASS beats random {rw}/3, needs {P['need_random_wins']}; MASS KL < "
             f"distance KL {dw}/3, needs {P['need_distance_kl_wins']})", "", head, "", f"void checks: same k {same_k}; "
             f"kept == runs 1/2 {kept_ok}; full-KV bit-exact x2 {st['repro']}; ref == runs 1/2 {st['ref_match']}", "",
             "| budget | k | kept | metric | MASS | random min-max | distance | band | DIRECT | sinkcount | MASS beats "
             "random | MASS KL < distance |", "|---" * 12 + "|"]
    for b, r in table.items():
        for m, f in (("agree", ".4f"), ("kl", ".5f")):
            v = [f"{(r if x[:3] == 'ran' else r['arms'])[x][m]:{f}}" for x in (
                "mass", "random_min", "random_max", "distance", "band", "direct", "sinkcount")]
            lines.append(f"| {b} | {ks[b]} | {r['kept']:.4f} | {m} | {v[0]} | {v[1]}-{v[2]} | {' | '.join(v[3:])} | "
                         f"{r['beats_random']} | {r['kl_below_distance']} |")
    dump(out, res, lines)
    os.remove(part)


if __name__ == "__main__":
    main()
