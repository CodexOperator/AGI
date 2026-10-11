#!/usr/bin/env python3
"""PAIR ABLATION ON LOSS (hypothesis:lm-neuron-periodicity-single-failing-frequencies-are-redundant-carriers-on-loss): the SAVED
checkpoints of seeds 0, 1, 2, forward passes only. Basis / ablate / pair / acc and the family pipeline are IMPORTED from the
freqabl module (and its S / T / F imports), unchanged. Score = held-out cross-entropy. Grid = <cell osc_neuron_period_pairloss_dir>/params.json."""
import json, os, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_freqabl as Q  # noqa: E402  basis, ablate, pair, acc (+ F, S, T)
import paths  # noqa: E402

F, S, T = Q.F, Q.S, Q.T
cols = lambda ks: sorted({c for k in ks for c in Q.pair(k)})   # a SET of frequencies: duplicates merge, never project twice


def ce(L, y):
    return float(-torch.log_softmax(L, 1)[torch.arange(len(y)), y].mean())


def margin(L, y):
    r = L.gather(1, y[:, None])[:, 0]
    return float((r - L.scatter(1, y[:, None], -float("inf")).max(1).values).mean())


def dce(L, y, Bm, ks, c0):
    return ce(Q.ablate(L, Bm, cols(ks)), y) - c0


def target_set(d1, fam, nk):   # step A: the family frequencies that do NOT beat the worst non-key frequency alone
    return [f for f in fam if d1[f] <= max(d1[j] for j in nk)]


def pair_table(L, y, Bm, f, fam, nk, c0):   # f against each partner g: its marginal beside g vs the exhaustive non-key null
    rows = {}
    for g in (g for g in fam if g != f):
        base = dce(L, y, Bm, [g], c0)
        nul = {j: dce(L, y, Bm, [j, g], c0) - base for j in nk}
        j = max(nul, key=nul.get)
        m = dce(L, y, Bm, [f, g], c0) - base
        rows[g] = {"marginal": m, "null_max": nul[j], "null_argmax_j": j, "beats": bool(m > nul[j]), "gap": m - nul[j]}
    return rows


def seed_run(P, ms, X, y, te, Bm):
    ck, p = P["checkpoints"][str(ms)], P["p"]
    if F.sha(ck["path"]) != ck["sha256"]:
        return {"seed": ms, "void": "checkpoint sha mismatch"}
    model, tol = S.make(P, ms), P["detrend_tol"]
    model.load_state_dict(torch.load(F.rp(ck["path"])))
    model.eval()
    acts, twin = S.sweep(model, P), S.sweep(S.make(P, P["twin_seed"]).eval(), P)
    (pk, kb), tmax, nl = S.stat(acts, tol), float(S.stat(twin, tol)[0].max()), S.null(acts, P)
    _, _, _, fams = T.families(pk, kb, float(np.quantile(nl, P["null_quantile"])), tmax, P["family_floor"])
    base = S.evaluate(model, X[te], y[te])[1]
    with torch.no_grad():
        L = model(X[te]).double()
    yt = y[te]
    if base < P["base_min_acc"]:
        return {"seed": ms, "void": f"held-out accuracy {base} < {P['base_min_acc']}"}
    L0, c0 = Q.ablate(L, Bm, []), ce(L, yt)
    recon = float(((L @ Bm) @ Bm.T - L).abs().max())
    if not (ce(L0, yt) == c0 and Q.acc(L0, yt) == Q.acc(L, yt) == base and recon <= P["recon_tol"]):
        return {"seed": ms, "void": f"projection self-check failed: ce {ce(L0, yt)} vs {c0}, acc {Q.acc(L0, yt)} vs {base}, recon {recon}"}
    pw = np.abs(np.fft.rfft(model.E.detach().numpy()[:p].astype(np.float64), axis=0)[1:(p - 1) // 2 + 1]) ** 2
    W = sorted(int(k) + 1 for k in np.argsort(-pw.sum(1), kind="stable")[:6])
    ks, nk = range(1, (p - 1) // 2 + 1), [k for k in range(1, (p - 1) // 2 + 1) if k not in W]
    d1 = {k: dce(L, yt, Bm, [k], c0) for k in ks}
    mg = {k: margin(Q.ablate(L, Bm, Q.pair(k)), yt) for k in ks}
    fam = sorted(fams)
    Ts = target_set(d1, fam, nk)
    extra = [f for f in P["extra_pair_table"].get(str(ms), []) if f in fam and f not in Ts]
    tabs = {f: pair_table(L, yt, Bm, f, fam, nk, c0) for f in Ts + extra}
    R = {f: any(r["beats"] for r in tabs[f].values()) for f in Ts}
    return {"seed": ms, "void": None, "base_test_acc": base, "ce0": c0, "margin0": margin(L, yt), "key_W": W, "families": fam,
            "max_nonkey_d1": max(d1[j] for j in nk), "T": Ts, "extra_tables": extra, "d1": d1, "margin_ablated": mg,
            "pairs": tabs, "R": R, "R_strict": {f: all(r["beats"] for r in tabs[f].values()) for f in Ts}, "R_all": all(R.values())}


def main():
    out = paths.get_local("osc_neuron_period_pairloss_dir")
    pp = os.path.join(out, "params.json")
    P, psha, t0 = json.load(open(pp)), F.sha(pp), time.time()
    log = lambda m, f=open(os.path.join(out, "run.log"), "a"): (print(m, flush=True), f.write(m + "\n"), f.flush())
    if not os.path.exists(fs := os.path.join(out, "start.json")):
        json.dump({"params_sha256": psha}, open(fs, "w"))
    torch.set_num_threads(P["threads"]), S.R2.S.wait_box(P)
    log(f"launch: params sha256 {psha}, torch {torch.__version__}")
    X, y, _, te = S.data(P)
    seeds, Bm = [], Q.basis(P["p"])
    for ms in P["model_seeds"]:
        seeds.append(seed_run(P, ms, X, y, te, Bm) if time.time() - t0 < P["wall_cap_s"] else {"seed": ms, "void": "wall cap"})
        r = seeds[-1]
        log(f"seed {ms}: void={r['void']} T={r.get('T')} R={r.get('R')} " + json.dumps(
            {f: {g: [round(x["marginal"], 4), round(x["null_max"], 4), x["beats"]] for g, x in t.items()} for f, t in r.get("pairs", {}).items()}))
    void = any(s["void"] for s in seeds) or json.load(open(fs))["params_sha256"] != psha
    T_all = [(s["seed"], f) for s in seeds if not s["void"] for f in s["T"]]
    v = "void" if void else "inconclusive" if not T_all else "proved" if all(s["R_all"] for s in seeds) else "disproved"
    json.dump({"verdict": v, "T_all": T_all, "params_sha256": psha, "launch_sha256": json.load(open(fs))["params_sha256"], "seeds": seeds},
              open(os.path.join(out, "results.json"), "w"), indent=1)
    open(os.path.join(out, "summary.md"), "w").write(f"# PAIR ABLATION ON LOSS: {v}\n\nT = {T_all}\n\n" + "\n".join(
        f"- seed {s['seed']}: void={s['void']} T={s.get('T')} R={s.get('R')}" for s in seeds) + "\n")
    log(f"verdict {v}")


if __name__ == "__main__":
    main()
