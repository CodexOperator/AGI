#!/usr/bin/env python3
"""SEED REPLICATION (hypothesis:lm-neuron-periodicity-control-replicates-across-training-seeds): the PC's exact run at
training seeds 1, 2, 3, every function IMPORTED from osc_neuron_period_pc (S) / osc_neuron_period2 (R2), none copied.
Grid = <cell osc_neuron_period_seeds_dir>/params.json. Run detached, seeds sequential; resumable (results_s<N>.json
per finished seed, partial/ckpt_s<N>.pt inside the running one)."""
import csv, hashlib, json, os, sys
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_pc as S  # noqa: E402  the PC's train / sweep / stat / null / evaluate / data / make
import paths  # noqa: E402


def families(pk, kb, q, tmax, floor):
    """P1 set, its frequency tally (count desc, ties smallest k) and {k: neurons} for every family >= floor."""
    p1 = np.flatnonzero((pk > q) & (pk > tmax))
    ks, cnt = np.unique(kb[p1], return_counts=True)
    ks, cnt = ks[o := np.lexsort((ks, -cnt))], cnt[o]
    return p1, ks, cnt, {int(k): [int(i) for i in p1 if kb[i] == k] for k, c in zip(ks, cnt) if c >= floor}


def random_sets(n, fam, seeds):   # size-matched, disjoint from the family, seed-deterministic
    rest = np.setdiff1d(np.arange(n), fam)
    return {s: sorted(int(i) for i in np.random.default_rng(s).choice(rest, len(fam), replace=False)) for s in seeds}


def analyse(model, P, X, y, tr, te):
    """P1, P2 and P4 for one grokked model (the PC's own statistics and ablation arm, per family)."""
    tol, acts, twin = P["detrend_tol"], S.sweep(model.eval(), P), S.sweep(S.make(P, P["twin_seed"]).eval(), P)
    (pk, kb), tmax, nl, n = S.stat(acts, tol), float(S.stat(twin, tol)[0].max()), S.null(acts, P), P["model"]["d_mlp"]
    q = float(np.quantile(nl, P["null_quantile"]))
    p1, ks, cnt, fams = families(pk, kb, q, tmax, P["family_floor"])
    n_cover = int(np.searchsorted(np.cumsum(cnt), P["p2_cover"] * len(p1)) + 1) if len(p1) else 0
    S.evaluate(model, X, y)
    means = model.seen.mean(0)
    arm = lambda ids: S.evaluate(model, X[te], y[te], (torch.isin(torch.arange(n), torch.tensor(ids, dtype=int)), means))
    base, fam_rows, match_ok = arm([])[1], {}, True
    for k, fam in fams.items():
        rs = random_sets(n, fam, P["random_seeds"])
        match_ok &= all(len(v) == len(fam) and not set(v) & set(fam) for v in rs.values())
        rd = [base - arm(rs[s])[1] for s in P["random_seeds"]]
        d, rm = base - arm(fam)[1], float(np.mean(rd))
        fam_rows[k] = {"size": len(fam), "drop": d, "rand_max": max(rd), "rand_mean": rm,
                       "load_bearing": d > max(rd), "passenger": d < rm}
    pw = np.abs(np.fft.rfft(model.E.detach().numpy()[:P["p"]].astype(np.float64), axis=0)[1:(P["p"] - 1) // 2 + 1]) ** 2
    we = sorted(int(k) + 1 for k in np.argsort(-pw.sum(1), kind="stable")[:6])
    v1, v2 = len(p1) / n >= P["p1_min_fraction"], bool(len(p1)) and n_cover <= P["p2_max_freqs"]
    v4 = any(r["load_bearing"] for r in fam_rows.values())
    return {"shape_ok": acts.shape == twin.shape == (len(P["b_set"]), P["p"], n) and nl.shape == (P["null_permutations"], n),
            "match_ok": bool(match_ok), "base_test_acc": base, "null_q999": q, "twin_max": tmax,
            "p1": {"pass": bool(v1), "count": len(p1), "fraction": len(p1) / n},
            "p2": {"pass": bool(v2), "n_cover": n_cover, "freq_counts": {int(k): int(c) for k, c in zip(ks, cnt)}},
            "p4": {"pass": bool(v4), "families": fam_rows, "n_load_bearing": sum(r["load_bearing"] for r in fam_rows.values()),
                   "n_passenger": sum(r["passenger"] for r in fam_rows.values())},
            "we_top6": we, "we_equals_families": we == sorted(fam_rows)}


def verdict(R, P):
    g = [r for r in R if r["train"]["grokked"]]
    if len(g) < 2 or not all(r["analysis"]["shape_ok"] and r["analysis"]["match_ok"] for r in g):
        return "void"
    return "proved" if all(r["analysis"][k]["pass"] for r in g for k in ("p1", "p2", "p4")) else "disproved"


def main():
    out = paths.get_local("osc_neuron_period_seeds_dir")
    pp, part = os.path.join(out, "params.json"), os.path.join(out, "partial")
    P, sha = json.load(open(pp)), hashlib.sha256(open(pp, "rb").read()).hexdigest()
    log = lambda m, f=open(os.path.join(out, "run.log"), "a"): (print(m, flush=True), f.write(m + "\n"), f.flush())
    os.makedirs(part, exist_ok=True)
    if not os.path.exists(fs := os.path.join(part, "start.json")):
        json.dump({"params_sha256": sha}, open(fs, "w"))
    torch.set_num_threads(P["threads"]), S.R2.S.wait_box(P)
    log(f"launch: params sha256 {sha}, torch {torch.__version__}")
    (X, y, tr, te), R = S.data(P), []
    for seed in P["train_seeds"]:
        if not os.path.exists(rf := os.path.join(out, f"results_s{seed}.json")):
            model, r = S.train(P, part, seed, X, y, tr, te, log)
            torch.save(model.state_dict(), os.path.join(out, f"model_s{seed}.pt"))
            a = analyse(model, P, X, y, tr, te) if r["grokked"] else None
            json.dump({"train": r, "analysis": a}, open(rf, "w"), indent=1)
        R.append(json.load(open(rf)))
        log(f"seed {seed}: " + json.dumps({k: v for k, v in R[-1]["train"].items() if k != "curve"}))
    with open(os.path.join(out, "curve.csv"), "w", newline="") as f:
        csv.writer(f).writerows([["seed", "step", "train_loss", "train_acc", "test_loss", "test_acc"]] +
                                [[r["train"]["seed"], *row] for r in R for row in r["train"]["curve"]])
    res = {"verdict": verdict(R, P), "params_sha256": sha, "launch_sha256": json.load(open(fs))["params_sha256"],
           "seeds": [{**{k: v for k, v in r["train"].items() if k != "curve"}, "analysis": r["analysis"]} for r in R]}
    if res["launch_sha256"] != sha:
        res["verdict"] = "void"
    json.dump(res, open(os.path.join(out, "results.json"), "w"), indent=1)
    log(t := "\n".join([f"# SEED REPLICATION: {res['verdict']}", ""] + [f"- seed {s['seed']}: " + json.dumps(
        {k: v for k, v in s.items() if k != "seed"})[:1500] for s in res["seeds"]]))
    open(os.path.join(out, "summary.md"), "w").write(t + "\n")


if __name__ == "__main__":
    main()
