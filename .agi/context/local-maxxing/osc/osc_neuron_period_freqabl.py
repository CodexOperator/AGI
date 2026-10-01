#!/usr/bin/env python3
"""FREQUENCY ABLATION IN LOGIT SPACE (hypothesis:lm-neuron-periodicity-every-family-frequency-is-load-bearing-in-logit-space):
the SAVED checkpoints of seeds 0, 1, 2, forward passes only. Families from the imported PC pipeline (S) / seeds module (T),
unchanged, exactly as the p4fair run (F). C1: every family frequency's logit-frequency ablation drop beats EVERY non-key
frequency's. C2: every family's direct logit energy sits >= 0.5 in its own frequency and peaks there.
Grid = <cell osc_neuron_period_freqabl_dir>/params.json. ONE process; per-seed results are held in memory (a run is minutes)."""
import json, os, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_p4fair as F  # noqa: E402  sha / rp
import osc_neuron_period_pc as S  # noqa: E402  sweep / stat / null / evaluate / data / make
import osc_neuron_period_seeds as T  # noqa: E402  families (the P1 set grouped by dominant frequency)
import paths  # noqa: E402

acc = lambda L, y: float((L.argmax(1) == y).double().mean())
pair = lambda k: [2 * k - 1, 2 * k]   # columns of the basis: 0 = the constant, (2k-1, 2k) = frequency k


def basis(p):
    """(p, p) float64 orthonormal: column 0 = 1/sqrt(p), then per k = 1..(p-1)/2 the orthonormalised (cos, sin) pair."""
    c, cols = np.arange(p), [np.ones(p) / np.sqrt(p)]
    for k in range(1, (p - 1) // 2 + 1):
        a, s = np.cos(2 * np.pi * k * c / p), np.sin(2 * np.pi * k * c / p)
        a /= np.linalg.norm(a)
        s -= (s @ a) * a
        cols += [a, s / np.linalg.norm(s)]
    return torch.from_numpy(np.stack(cols, 1))


def ablate(L, Bm, cols):   # L - B B^T L over the given basis columns; no columns -> L - 0, bit-identical
    B = Bm[:, cols]
    return L - (L @ B) @ B.T


def energy(D, Bm, p):   # fraction of D's (centred) energy in each frequency 1..(p-1)/2 -> numpy (56,)
    D = D - D.mean(1, keepdim=True)
    return ((D @ Bm[:, 1:]) ** 2).sum(0).view(-1, 2).sum(1).numpy() / float((D ** 2).sum())


def seed_run(P, ms, X, y, te, Bm, p4):
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
    h, Wo, U = model.seen.double(), model.w_out.weight.detach().double(), model.U.weight.detach().double()
    if base < P["base_min_acc"]:
        return {"seed": ms, "void": f"held-out accuracy {base} < {P['base_min_acc']}"}
    recon = float((ablate(L, Bm, []) - L).abs().max()), float(((L @ Bm) @ Bm.T - L).abs().max())
    if not (acc(ablate(L, Bm, []), y[te]) == acc(L, y[te]) == base and recon[1] <= P["recon_tol"]):
        return {"seed": ms, "void": f"projection self-check failed: acc {acc(L, y[te])} vs {base}, recon {recon}"}
    pw = np.abs(np.fft.rfft(model.E.detach().numpy()[:p].astype(np.float64), axis=0)[1:(p - 1) // 2 + 1]) ** 2
    W = sorted(int(k) + 1 for k in np.argsort(-pw.sum(1), kind="stable")[:6])
    drop = {k: base - acc(ablate(L, Bm, pair(k)), y[te]) for k in range(1, (p - 1) // 2 + 1)}
    mx = max(d for k, d in drop.items() if k not in W)
    keep = [0] + [c for k in fams for c in pair(k)]
    suff = acc((L @ Bm[:, keep]) @ Bm[:, keep].T, y[te])
    rows = {}
    for k, fam in fams.items():
        fr = energy((h[:, fam] @ Wo[:, fam].T) @ U.T, Bm, p)
        rows[k] = {"size": len(fam), "drop": drop[k], "c1": bool(drop[k] > mx), "frac_own": float(fr[k - 1]),
                   "argmax_freq": int(fr.argmax()) + 1, "argmax_frac": float(fr.max()), "p4prime_drop": p4[ms][str(k)]["drop"],
                   "c2": bool(fr[k - 1] >= P["c2_min_fraction"] and int(fr.argmax()) + 1 == k), "k_in_key_set": k in W}
    return {"seed": ms, "void": None, "base_test_acc": base, "key_W": W, "max_nonkey_drop": mx, "self_check": recon,
            "sufficiency_acc": suff, "drop_by_freq": drop, "families": rows,
            "c1": all(r["c1"] for r in rows.values()), "c2": all(r["c2"] for r in rows.values())}


def main():
    out = paths.get_local("osc_neuron_period_freqabl_dir")
    pp = os.path.join(out, "params.json")
    P, psha, t0 = json.load(open(pp)), F.sha(pp), time.time()
    log = lambda m, f=open(os.path.join(out, "run.log"), "a"): (print(m, flush=True), f.write(m + "\n"), f.flush())
    if not os.path.exists(fs := os.path.join(out, "start.json")):
        json.dump({"params_sha256": psha}, open(fs, "w"))
    torch.set_num_threads(P["threads"]), S.R2.S.wait_box(P)
    log(f"launch: params sha256 {psha}, torch {torch.__version__}")
    X, y, _, te = S.data(P)
    p4 = {s["seed"]: s["families"] for s in json.load(open(F.rp("datasets/osc-band/2026-10-01-neuron-period-p4fair/results.json")))["seeds"]}
    seeds, Bm = [], basis(P["p"])
    for ms in P["model_seeds"]:
        seeds.append(seed_run(P, ms, X, y, te, Bm, p4) if time.time() - t0 < P["wall_cap_s"] else {"seed": ms, "void": "wall cap"})
        R = seeds[-1]
        log(f"seed {ms}: void={R['void']} c1={R.get('c1')} c2={R.get('c2')} " + json.dumps(
            {f: (round(r["drop"], 3), r["c1"], round(r["frac_own"], 3), r["argmax_freq"], r["c2"]) for f, r in R.get("families", {}).items()}))
    void = any(s["void"] for s in seeds) or json.load(open(fs))["params_sha256"] != psha
    v = "void" if void else "proved" if all(s["c1"] and s["c2"] for s in seeds) else "disproved"
    json.dump({"verdict": v, "params_sha256": psha, "launch_sha256": json.load(open(fs))["params_sha256"], "seeds": seeds},
              open(os.path.join(out, "results.json"), "w"), indent=1)
    open(os.path.join(out, "summary.md"), "w").write(f"# LOGIT-SPACE FREQUENCY ABLATION: {v}\n\n" + "\n".join(
        f"- seed {s['seed']}: void={s['void']} c1={s.get('c1')} c2={s.get('c2')}" for s in seeds) + "\n")
    log(f"verdict {v}")


if __name__ == "__main__":
    main()
