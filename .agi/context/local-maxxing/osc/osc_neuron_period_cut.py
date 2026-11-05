#!/usr/bin/env python3
"""KEY-FREQUENCY CUT (goal:g5.36, hypothesis:lm-the-mod-113-circuit-cut-to-its-key-frequency-neurons-keeps-its-accuracy):
the SAVED seed-0 PC checkpoint keeps N of its 512 MLP neurons; W_out / b_out are rewritten in closed form (least squares onto
the full net's TRAIN logits, 0 gradient steps) and the edited net is scored on the held-out rows. Frequency pick vs 5 seeded
random picks; the random-init twin under the same solve is the mutant (must stay < 0.5, else VOID). The PC pipeline (S),
families (T) and sha / rp (F) are IMPORTED, unchanged. Grid = <cell osc_neuron_period_cut_dir>/params.json."""
import copy, json, os, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_p4fair as F  # noqa: E402  sha / rp
import osc_neuron_period_pc as S  # noqa: E402  make / data / sweep / stat / null / evaluate
import osc_neuron_period_seeds as T  # noqa: E402  families
import paths  # noqa: E402


def freq_pick(pk, fams, n):
    """Round-robin over the families in their order, one neuron per family per round, each by pk desc (ties smallest index)."""
    q, out = [sorted(v, key=lambda i: (-pk[i], i)) for v in fams.values()], []
    while len(out) < n and any(q):
        for f in q:
            if f and len(out) < n:
                out.append(int(f.pop(0)))
    return out


def rand_pick(n_all, seed, n):   # nested: the first n of ONE seeded permutation over all neurons
    return [int(i) for i in np.random.default_rng(seed).permutation(n_all)[:n]]


def feats(model, X):
    """Post-ReLU h at '=' and the non-MLP logit path (L - U(W_out h + b_out)), float64."""
    with torch.no_grad():
        L = model(X).double()
    h, Wo, bo = model.seen.double(), model.w_out.weight.detach().double(), model.w_out.bias.detach().double()
    return h, L - (h @ Wo.T + bo) @ model.U.weight.detach().double().T


def solve(h, rest, target, keep, U):
    """M = lstsq([h_keep, 1], target - rest) in logit space; W' = M pinv(U^T) in the residual stream; u error = |W' U^T - M|."""
    Phi = torch.cat([h[:, keep], torch.ones(len(h), 1, dtype=h.dtype)], 1)
    M = torch.linalg.lstsq(Phi, target - rest, driver="gelsd").solution
    W = M @ torch.linalg.pinv(U.T)
    return W, float((W @ U.T - M).abs().max())


def install(model, keep, W):   # a COPY with W_out[:, keep] = W'[:n]^T, every other column 0, b_out = W'[n]
    m = copy.deepcopy(model)
    wo = torch.zeros_like(m.w_out.weight)
    wo[:, keep] = W[:-1].T.to(wo.dtype)
    m.w_out.weight.data, m.w_out.bias.data = wo, W[-1].to(wo.dtype)
    return m


def arm(model, keep, X, y, tr, te, target):
    h, rest = feats(model, X[tr])
    W, uerr = solve(h, rest, target, keep, model.U.weight.detach().double())
    m = install(model, keep, W)
    return {"n": len(keep), "test_acc": S.evaluate(m, X[te], y[te])[1], "train_acc": S.evaluate(m, X[tr], y[tr])[1],
            "test_loss": S.evaluate(m, X[te], y[te])[0], "u_err": uerr}, m


def verdict(freq, rand, mutant_max, P):
    """freq {N: acc}, rand {seed: {N: acc}} -> N_f, N_r per seed, N_r, mutant_red, proved (void checks live in main)."""
    first = lambda d: min((n for n in sorted(d) if d[n] >= P["acc_threshold"]), default=None)
    nf = first({n: a for n, a in freq.items() if n in P["n_grid"]})
    nrs = {s: first(d) for s, d in rand.items()}
    nr = min((v for v in nrs.values() if v is not None), default=None)
    return {"N_f": nf, "N_r": nr, "N_r_by_seed": nrs, "mutant_max": mutant_max, "mutant_red": mutant_max < P["mutant_max_acc"],
            "proved": nf is not None and (nr is None or nr >= 2 * nf)}


def main():
    out = paths.get_local("osc_neuron_period_cut_dir")
    pp = os.path.join(out, "params.json")
    P, psha, t0 = json.load(open(pp)), F.sha(pp), time.time()
    log = lambda m, f=open(os.path.join(out, "run.log"), "a"): (print(m, flush=True), f.write(m + "\n"), f.flush())
    if not os.path.exists(fs := os.path.join(out, "start.json")):
        json.dump({"params_sha256": psha}, open(fs, "w"))
    torch.set_num_threads(P["threads"]), S.R2.S.wait_box(P)
    log(f"launch: params sha256 {psha}, torch {torch.__version__}, numpy {np.__version__}")
    ck, void = P["checkpoint"], []
    if F.sha(ck["path"]) != ck["sha256"]:
        void.append("checkpoint sha mismatch")
    model, twin, n_all = S.make(P, ck["train_seed"]), S.make(P, P["twin_seed"]).eval(), P["model"]["d_mlp"]
    model.load_state_dict(torch.load(F.rp(ck["path"])))
    model.eval()
    X, y, tr, te = S.data(P)
    base = S.evaluate(model, X[te], y[te])[1]
    with torch.no_grad():
        target = model(X[tr]).double()
    tol, acts, tacts = P["detrend_tol"], S.sweep(model, P), S.sweep(twin, P)
    (pk, kb), (tpk, _), nl = S.stat(acts, tol), S.stat(tacts, tol), S.null(acts, P)
    _, ks, cnt, fams = T.families(pk, kb, float(np.quantile(nl, P["null_quantile"])), float(tpk.max()), P["family_floor"])
    log(f"baseline held-out acc {base}; families {{k: size}} {({k: len(v) for k, v in fams.items()})}")
    full = arm(model, list(range(n_all)), X, y, tr, te, target)[0]
    if base < P["acc_threshold"]:
        void.append(f"baseline held-out acc {base} < {P['acc_threshold']}")
    if abs(full["test_acc"] - base) > P["self_tol"]:
        void.append(f"512-neuron self-check: cut acc {full['test_acc']} vs baseline {base}")
    grid, rows, picks, uerr, cut = sorted(P["n_grid"] + P["n_grid_random_extra"]), {"freq": {}, "rand": {}}, {"freq": {}, "rand": {}}, [full["u_err"]], {}
    for n in grid:
        picks["freq"][n] = keep = freq_pick(pk, fams, n)
        rows["freq"][n], cut[n] = arm(model, keep, X, y, tr, te, target)
        for s in P["random_seeds"]:
            picks["rand"].setdefault(s, {})[n] = rk = rand_pick(n_all, s, n)
            rows["rand"].setdefault(s, {})[n] = arm(model, rk, X, y, tr, te, target)[0]
        uerr += [rows["freq"][n]["u_err"]] + [rows["rand"][s][n]["u_err"] for s in P["random_seeds"]]
        log(f"N {n}: freq {rows['freq'][n]['test_acc']:.5f} rand " + " ".join(f"{rows['rand'][s][n]['test_acc']:.5f}" for s in P["random_seeds"]))
    tsets = {"twin_top64": sorted(range(n_all), key=lambda i: (-tpk[i], i))[:64], **{f"rand_{s}": rand_pick(n_all, s, 64) for s in P["random_seeds"]}}
    mut = {k: arm(twin, v, X, y, tr, te, target)[0] for k, v in tsets.items()}
    uerr += [r["u_err"] for r in mut.values()]
    log("mutant (twin, 64 neurons) held-out acc " + json.dumps({k: round(r["test_acc"], 5) for k, r in mut.items()}))
    V = verdict({n: r["test_acc"] for n, r in rows["freq"].items()}, {s: {n: r["test_acc"] for n, r in d.items()} for s, d in rows["rand"].items()},
                max(r["test_acc"] for r in mut.values()), P)
    if max(uerr) > P["u_tol"]:
        void.append(f"u error {max(uerr)} > {P['u_tol']}")
    if not V["mutant_red"]:
        void.append(f"mutant not RED: twin max acc {V['mutant_max']} >= {P['mutant_max_acc']}")
    if time.time() - t0 > P["wall_cap_s"]:
        void.append("wall cap")
    if json.load(open(fs))["params_sha256"] != psha:
        void.append("params.json changed since launch")
    v = "void" if void else "proved" if V["proved"] else "disproved"
    if V["N_f"] is not None:
        torch.save(cut[V["N_f"]].state_dict(), os.path.join(out, "cut_nf.pt"))
    R = {"verdict": v, "void": void, **V, "params_sha256": psha, "launch_sha256": json.load(open(fs))["params_sha256"],
         "torch": torch.__version__, "numpy": np.__version__, "baseline_test_acc": base, "self_check_512": full, "max_u_err": max(uerr),
         "families": {int(k): len(f) for k, f in fams.items()}, "key_frequencies": [int(k) for k in fams], "p1_tally": {int(k): int(c) for k, c in zip(ks, cnt)},
         "freq": rows["freq"], "rand": rows["rand"], "mutant": mut, "picks": picks, "mutant_sets": tsets, "wall_s": round(time.time() - t0, 1)}
    json.dump(R, open(os.path.join(out, "results.json"), "w"), indent=1)
    lines = [f"# KEY-FREQUENCY CUT: {v}", "", f"- N_f {V['N_f']}, N_r {V['N_r']} (by seed {V['N_r_by_seed']}), mutant max {V['mutant_max']:.4f}, void {void}",
             f"- key frequencies {R['key_frequencies']}, baseline {base:.5f}, 512 self-check {full['test_acc']:.5f}", "", "| N | freq | " + " | ".join(f"rand {s}" for s in P["random_seeds"]) + " |",
             "|---|---|" + "---|" * len(P["random_seeds"])] + [f"| {n} | {rows['freq'][n]['test_acc']:.4f} | " + " | ".join(f"{rows['rand'][s][n]['test_acc']:.4f}" for s in P["random_seeds"]) + " |" for n in grid]
    open(os.path.join(out, "summary.md"), "w").write("\n".join(lines) + "\n")
    log(f"verdict {v} N_f {V['N_f']} N_r {V['N_r']} mutant_max {V['mutant_max']:.4f} void {void} ({R['wall_s']}s)")


if __name__ == "__main__":
    main()
