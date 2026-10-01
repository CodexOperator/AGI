#!/usr/bin/env python3
"""P4' FAIR RE-TEST (hypothesis:lm-neuron-periodicity-fair-p4-every-seed-has-a-load-bearing-family): the SAVED checkpoints of
seeds 0, 1, 2, forward passes only. Families from the imported PC pipeline (S) / seeds module (T), unchanged; each family's
mean-ablation drop is compared with the 99th percentile of 200 uniform AND 200 norm-matched size-matched random sets.
Grid = <cell osc_neuron_period_p4fair_dir>/params.json. Run detached; per-seed results_s<N>.json make a relaunch resume."""
import hashlib, json, os, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_pc as S  # noqa: E402  sweep / stat / null / evaluate / data / make
import osc_neuron_period_seeds as T  # noqa: E402  families (the P1 set grouped by dominant frequency)
import paths  # noqa: E402

rp = lambda path: path if os.path.isabs(path) else os.path.join(paths.checkout_root(), path)   # repo-relative cells
sha = lambda path: hashlib.sha256(open(rp(path), "rb").read()).hexdigest()
pct = lambda x, drops: 100 * float(np.mean(np.asarray(drops) <= x))


def u_sets(n, m, rng, k):   # k uniform size-m sets over ALL n neurons
    return [sorted(int(i) for i in rng.choice(n, m, replace=False)) for _ in range(k)]


def n_sets(cn, m, target, rng, k, window, max_draws):
    """k size-m sets drawn uniformly, ACCEPTED iff |mean column norm - target| <= window; fewer than k in max_draws -> short."""
    out = []
    for _ in range(max_draws):
        s = rng.choice(len(cn), m, replace=False)
        if abs(float(cn[s].mean()) - target) <= window:
            out.append(sorted(int(i) for i in s))
        if len(out) == k:
            break
    return out


def judge(drop, ud, nd, q, k):
    """load-bearing iff drop > the q-quantile of U AND of N; an N-UNTESTABLE family (len(nd) < k) cannot pass the AND."""
    nt = len(nd) < k
    return {"load_bearing": bool(drop > np.quantile(ud, q) and not nt and drop > np.quantile(nd, q)), "n_untestable": nt}


def seed_run(P, ms, X, y, tr, te):
    ck = P["checkpoints"][str(ms)]
    if sha(ck["path"]) != ck["sha256"]:
        return {"seed": ms, "void": "checkpoint sha mismatch"}
    model, tol = S.make(P, ms), P["detrend_tol"]
    model.load_state_dict(torch.load(rp(ck["path"])))
    model.eval()
    acts, twin, n = S.sweep(model, P), S.sweep(S.make(P, P["twin_seed"]).eval(), P), P["model"]["d_mlp"]
    (pk, kb), tmax, nl = S.stat(acts, tol), float(S.stat(twin, tol)[0].max()), S.null(acts, P)
    p1, ks, cnt, fams = T.families(pk, kb, float(np.quantile(nl, P["null_quantile"])), tmax, P["family_floor"])
    S.evaluate(model, X, y)
    means, cn = model.seen.mean(0), model.w_out.weight.detach().norm(dim=0).numpy()
    arm = lambda ids: S.evaluate(model, X[te], y[te], (torch.isin(torch.arange(n), torch.tensor(ids, dtype=int)), means))[1]
    base, rows, k = arm([]), {}, P["n_sets"]
    if base < 0.99:
        return {"seed": ms, "void": f"held-out accuracy {base} < 0.99"}
    for f, fam in fams.items():
        ru, rn = (np.random.default_rng([P[s], ms, f]) for s in ("u_seed", "n_seed"))
        d = base - arm(fam)
        ud = [base - arm(s) for s in u_sets(n, len(fam), ru, k)]
        ns = n_sets(cn, len(fam), float(cn[fam].mean()), rn, k, P["norm_window"], P["max_draws"])
        nd = [base - arm(s) for s in ns]
        rows[f] = {"size": len(fam), "drop": d, "fam_norm": float(cn[fam].mean()), "pU": pct(d, ud), "pN": pct(d, nd) if nd else None,
                   "u_q": float(np.quantile(ud, P["percentile"])), "n_q": float(np.quantile(nd, P["percentile"])) if nd else None,
                   "n_accepted": len(nd), **judge(d, ud, nd, P["percentile"], k)}
    return {"seed": ms, "void": None, "base_test_acc": base, "n_p1": len(p1), "families": rows,
            "n_load_bearing": sum(r["load_bearing"] for r in rows.values())}


def main():
    out = paths.get_local("osc_neuron_period_p4fair_dir")
    pp = os.path.join(out, "params.json")
    P, psha, t0 = json.load(open(pp)), sha(pp), time.time()
    log = lambda m, f=open(os.path.join(out, "run.log"), "a"): (print(m, flush=True), f.write(m + "\n"), f.flush())
    if not os.path.exists(fs := os.path.join(out, "start.json")):
        json.dump({"params_sha256": psha}, open(fs, "w"))
    torch.set_num_threads(P["threads"]), S.R2.S.wait_box(P)
    log(f"launch: params sha256 {psha}, torch {torch.__version__}")
    X, y, tr, te = S.data(P)
    for ms in P["model_seeds"]:
        if not os.path.exists(rf := os.path.join(out, f"results_s{ms}.json")) and time.time() - t0 < P["wall_cap_s"]:
            json.dump(seed_run(P, ms, X, y, tr, te), open(rf, "w"), indent=1)
        R = json.load(open(rf)) if os.path.exists(rf) else {"seed": ms, "void": "wall cap"}
        log(f"seed {ms}: void={R['void']} n_load_bearing={R.get('n_load_bearing')} " + json.dumps(
            {f: (round(r["pU"], 1), r["pN"] and round(r["pN"], 1), r["load_bearing"]) for f, r in R.get("families", {}).items()}))
    seeds = [json.load(open(os.path.join(out, f"results_s{m}.json"))) if os.path.exists(os.path.join(out, f"results_s{m}.json"))
             else {"seed": m, "void": "wall cap"} for m in P["model_seeds"]]
    void = any(s["void"] for s in seeds) or json.load(open(fs))["params_sha256"] != psha
    v = "void" if void else "proved" if all(s["n_load_bearing"] >= 1 for s in seeds) else "disproved"
    json.dump({"verdict": v, "params_sha256": psha, "launch_sha256": json.load(open(fs))["params_sha256"], "seeds": seeds},
              open(os.path.join(out, "results.json"), "w"), indent=1)
    open(os.path.join(out, "summary.md"), "w").write(f"# P4' FAIR RE-TEST: {v}\n\n" + "\n".join(
        f"- seed {s['seed']}: void={s['void']} n_load_bearing={s.get('n_load_bearing')}" for s in seeds) + "\n")
    log(f"verdict {v}")


if __name__ == "__main__":
    main()
