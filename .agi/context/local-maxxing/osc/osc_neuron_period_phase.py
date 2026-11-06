#!/usr/bin/env python3
"""JOINT PHASE, CEILING, WRITE (goal:g5.38, hypothesis:lm-honouring-the-mod-113-circuits-joint-phase-beats-random-and-plain-numerics):
the SAVED seed-0 PC checkpoint under g5.36's train-only solve and scoring (osc_neuron_period_cut, IMPORTED unchanged).
Arms: (a) random, (b) joint-phase pick, (c) OMP ceiling, (d) write-don't-pick, (e) model_s3.pt census; H1 / H2 / H3 and
mutants M1-M4. Grid = <cell osc_neuron_period_phase_dir>/params.json."""
import copy, json, os, sys, time
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_cut as Z  # noqa: E402  g5.36: feats / solve / install / arm / rand_pick (+ S, T, F)
import paths  # noqa: E402

S, T, F = Z.S, Z.T, Z.F


def phases(A, k):
    """A (p, p) one neuron's post-ReLU over every (a, b); -> (phi_a, phi_b) = arg fft2(A)[k, 0], arg fft2(A)[0, k]."""
    Fq = np.fft.fft2(A)
    return float(np.angle(Fq[k, 0])), float(np.angle(Fq[0, k]))


R = lambda th: float(np.abs(np.exp(1j * np.asarray(th)).mean())) if len(th) else 0.0   # mean resultant length


def quotas(counts, n):   # largest remainder; ties -> family order (as T.families orders them)
    ks, c = list(counts), np.array(list(counts.values()), float)
    q = n * c / c.sum()
    base = np.floor(q).astype(int)
    for i in sorted(range(len(ks)), key=lambda i: (-(q[i] - base[i]), i))[: n - base.sum()]:
        base[i] += 1
    return dict(zip(ks, (int(b) for b in base)))


def greedy_family(cands, ph, m, score):
    """m neurons from cands, each step the one minimising score(kept + [c]); ties (within 1e-12) -> smallest index."""
    kept, rest = [], sorted(cands)
    for _ in range(min(m, len(rest))):
        v = [score([ph[i] for i in kept + [c]]) for c in rest]
        best = min(range(len(rest)), key=lambda j: (round(v[j] / 1e-12) * 1e-12, rest[j]))
        kept.append(rest.pop(best))
    return kept


joint = lambda P: max(R([a + b for a, b in P]), R([a - b for a, b in P]))   # (b): minimise max(R_sum, R_diff)
twin_sum = lambda P: -R([a + b for a, b in P])   # M1: MAXIMISE R_sum


def phase_pick(fams, ph, n, score):
    return [i for k, m in quotas({k: len(v) for k, v in fams.items()}, n).items() for i in greedy_family(fams[k], ph, m, score)]


def omp(h, target_rest, n, tol=1e-9):
    """Greedy OMP on the TRAIN rows: the intercept is always in; add the column that most cuts the lstsq residual of the
    solve's own target (target - rest); dead / dependent columns are skipped; ties -> smallest index. -> the order list."""
    Q, Rs, out = torch.ones(len(h), 1, dtype=h.dtype) / len(h) ** 0.5, None, []
    Rs = target_rest - Q @ (Q.T @ target_rest)
    nrm0 = (h ** 2).sum(0)
    for _ in range(n):
        C = h - Q @ (Q.T @ h)
        c2 = (C ** 2).sum(0)
        gain = ((C.T @ Rs) ** 2).sum(1) / c2.clamp_min(1e-300)
        gain[(c2 <= tol * nrm0) | (nrm0 == 0)] = -1.0
        gain[out] = -1.0
        j = int(torch.nonzero(gain == gain.max())[0, 0])
        q = C[:, j:j + 1] / c2[j] ** 0.5
        Q, Rs = torch.cat([Q, q], 1), Rs - q @ (q.T @ Rs)
        out.append(j)
    return out


def lattice_g(m):   # the integer coprime to m nearest m / 1.618 (ties -> the smaller)
    return min((g for g in range(1, m + 1) if np.gcd(g, m) == 1), key=lambda g: (abs(g - m / 1.618), g))


def torus(m, equal=False):   # council pin: the rank-1 lattice (2 pi j / m, 2 pi (j g mod m) / m); M3: all 0
    g = lattice_g(m)
    return [(0.0, 0.0) if equal else (2 * np.pi * j / m, 2 * np.pi * ((j * g) % m) / m) for j in range(m)]


def resid_in(model, X):   # the MLP's input (residual stream at '=') for rows X, float64
    got = []
    hk = model.w_in.register_forward_hook(lambda mod, i, o: got.append(i[0].detach().double()))
    with torch.no_grad():
        model(X)
    hk.remove()
    return got[0]


def write(model, X, tr, ks, m, p, equal=False):
    """A COPY whose neurons 0..len(ks)*m-1 are written: per k, m neurons ReLU(w.r + b) with (w, b) = lstsq([r, 1]) of the
    TRAIN rows onto z = cos(2 pi k a / p + phi_j) + cos(2 pi k b / p + psi_j). -> (model, kept ids, probe R^2 per neuron)."""
    r, a, b = resid_in(model, X[tr]), X[tr, 0].double(), X[tr, 1].double()
    Phi, rows, r2 = torch.cat([r, torch.ones(len(r), 1, dtype=r.dtype)], 1), [], []
    for k in ks:
        for ph, ps in torus(m, equal):
            z = torch.cos(2 * np.pi * k * a / p + ph) + torch.cos(2 * np.pi * k * b / p + ps)
            w = torch.linalg.lstsq(Phi, z[:, None], driver="gelsd").solution[:, 0]
            rows.append(w), r2.append(float(1 - ((Phi @ w - z) ** 2).sum() / ((z - z.mean()) ** 2).sum()))
    mw, W = copy.deepcopy(model), torch.stack(rows)
    mw.w_in.weight.data[: len(rows)], mw.w_in.bias.data[: len(rows)] = W[:, :-1].float(), W[:, -1].float()
    return mw, list(range(len(rows))), r2


def first(d, th, grid):   # the smallest grid N whose acc >= th, else None
    return min((n for n in sorted(grid) if n in d and d[n] >= th), default=None)


def verdicts(A, P):
    """A = measured accuracies: rand {s: {N: acc}}, joint / m1 / omp / write {N: acc}, m2_max, m3, m4_max_frac.
    -> per-claim reads (void checks of the mutants here; run-level void lives in main)."""
    th, g = P["acc_threshold"], P["n_grid"]
    nb, nc = first(A["joint"], th, g), first(A["omp"], th, g)
    nrs = {s: first(d, th, g + P["n_grid_random_extra"]) for s, d in A["rand"].items()}
    nr = min((v for v in nrs.values() if v is not None), default=None)
    m1_red = all(A["m1"][n] < th for n in g)
    m2_red, m3_red, m4_red = A["m2_max"] < P["m2_max_acc"], A["m3"] < P["m3_max_acc"], A["m4_max_frac"] < P["m4_keep_frac"]
    h1_void = not (m1_red and m2_red and m4_red)
    h1 = "void" if h1_void else "proved" if nb is not None and (nr is None or nr >= 2 * nb) else "disproved"
    h2 = "void" if not m2_red else "no_verdict" if nb is None and nc is None else "red" if nc is not None and (nb is None or nc < nb) else "not_red"
    missing = [n for n in g if n not in A["write"] or n not in A["omp"]]   # forward fix (SM gate 12:41Z): a missing cell is VOID, never 'disproved'
    hits = [n for n in g if n not in missing and A["write"][n] >= th and A["omp"][n] < th]
    h3 = "void" if not m3_red or missing else "proved" if hits else "disproved"
    return {"N_b": nb, "N_c": nc, "N_r": nr, "N_r_by_seed": nrs, "N_w_hits": hits, "M1_red": m1_red, "M2_red": m2_red,
            "M3_red": m3_red, "M4_red": m4_red, "H1": h1, "H2": h2, "H3": h3}


def load(P, ck):
    m = S.make(P, ck["train_seed"])
    m.load_state_dict(torch.load(F.rp(ck["path"])))
    return m.eval()


def picks_for(model, P, X, y, tr, te, target, fams, ph, grid, with_joint=True):
    """Every pick on one model: random (5 seeds, grid + extra), OMP (to max grid), joint + M1 (if families); index sets kept."""
    h, rest = Z.feats(model, X[tr])
    o = omp(h, target - rest, max(grid))
    out = {"omp": {n: o[:n] for n in grid}, "rand": {s: {n: Z.rand_pick(P["model"]["d_mlp"], s, n) for n in grid + P["n_grid_random_extra"]}
                                                    for s in P["random_seeds"]}}
    if with_joint and fams:
        out["joint"] = {n: phase_pick(fams, ph, n, joint) for n in grid}
        out["m1"] = {n: phase_pick(fams, ph, n, twin_sum) for n in grid}
    return out


def score(model, sets, X, y, tr, te, target, key="test_acc"):
    run = lambda ids: Z.arm(model, ids, X, y, tr, te, target)[0]
    return {a: ({s: {n: run(ids) for n, ids in d.items()} for s, d in v.items()} if a == "rand" else {n: run(ids) for n, ids in v.items()})
            for a, v in sets.items()}


def census(model, P, X):
    tol, acts, tw = P["detrend_tol"], S.sweep(model, P), S.sweep(S.make(P, P["twin_seed"]).eval(), P)
    (pk, kb), (tpk, _), nl = S.stat(acts, tol), S.stat(tw, tol), S.null(acts, P)
    p1, ks, cnt, fams = T.families(pk, kb, float(np.quantile(nl, P["null_quantile"])), float(tpk.max()), P["family_floor"])
    with torch.no_grad():
        model(X)
    A = model.seen.double().numpy().reshape(P["p"], P["p"], -1)   # rows a*p+b -> [a, b, neuron]
    ph = {i: phases(A[:, :, i], k) for k, v in fams.items() for i in v}
    return {"p1": len(p1), "tally": {int(k): int(c) for k, c in zip(ks, cnt)}}, fams, ph


def main():
    out = paths.get_local("osc_neuron_period_phase_dir")
    pp = os.path.join(out, "params.json")
    P, psha, t0 = json.load(open(pp)), F.sha(pp), time.time()
    log = lambda m, f=open(os.path.join(out, "run.log"), "a"): (print(m, flush=True), f.write(m + "\n"), f.flush())
    if not os.path.exists(fs := os.path.join(out, "start.json")):
        json.dump({"params_sha256": psha}, open(fs, "w"))
    torch.set_num_threads(P["threads"]), S.R2.S.wait_box(P)
    log(f"launch: params sha256 {psha}, torch {torch.__version__}, numpy {np.__version__}")
    void = [f"{n} checkpoint sha mismatch" for n, ck in P["checkpoints"].items() if F.sha(ck["path"]) != ck["sha256"]]
    X, y, tr, te = S.data(P)
    grid, p, n_all = P["n_grid"], P["p"], P["model"]["d_mlp"]
    model, twin, s3 = load(P, P["checkpoints"]["pc"]), S.make(P, P["twin_seed"]).eval(), load(P, P["checkpoints"]["s3"])
    base = S.evaluate(model, X[te], y[te])[1]
    with torch.no_grad():
        target, t3 = model(X[tr]).double(), s3(X[tr]).double()
    cen, fams, ph = census(model, P, X)
    log(f"baseline {base}; families {({k: len(v) for k, v in fams.items()})}")
    full = Z.arm(model, list(range(n_all)), X, y, tr, te, target)[0]
    void += [f"baseline {base} < 0.99"] * (base < P["acc_threshold"]) + [f"512 self-check {full['test_acc']} vs {base}"] * (abs(full["test_acc"] - base) > P["self_tol"])
    sets = picks_for(model, P, X, y, tr, te, target, fams, ph, grid)
    rows = score(model, sets, X, y, tr, te, target)
    ks, wr = list(fams), {}
    for m in P["write_m"]:
        mw, ids, r2 = write(model, X, tr, ks, m, p)
        wr[len(ids)] = {**Z.arm(mw, ids, X, y, tr, te, target)[0], "m": m, "probe_r2_min": min(r2), "probe_r2_mean": float(np.mean(r2))}
    mw, ids, r2 = write(model, X, tr, ks, max(P["write_m"]), p, equal=True)
    m3 = {**Z.arm(mw, ids, X, y, tr, te, target)[0], "probe_r2_mean": float(np.mean(r2))}
    for n in grid:
        log(f"N {n}: joint {rows['joint'][n]['test_acc']:.4f} m1 {rows['m1'][n]['test_acc']:.4f} omp {rows['omp'][n]['test_acc']:.4f} write "
            f"{wr.get(n, {}).get('test_acc', float('nan')):.4f} rand " + " ".join(f"{rows['rand'][s][n]['test_acc']:.4f}" for s in P["random_seeds"]))
    tsets = {**{f"joint_{n}": v for n, v in sets["joint"].items()}, **{f"omp_{n}": v for n, v in sets["omp"].items()},
             **{f"rand_{s}_{n}": sets["rand"][s][n] for s in P["random_seeds"] for n in grid}}
    th, tr_ = Z.feats(twin, X[tr])
    to = omp(th, target - tr_, max(grid))
    tsets.update({f"twin_omp_{n}": to[:n] for n in grid})
    m2 = {k: Z.arm(twin, v, X, y, tr, te, target)[0]["test_acc"] for k, v in tsets.items()}
    tw_w = {}
    for m in P["write_m"]:
        mw, ids, r2 = write(twin, X, tr, ks, m, p)
        tw_w[len(ids)] = {**Z.arm(mw, ids, X, y, tr, te, target)[0], "probe_r2_mean": float(np.mean(r2))}
    log(f"M2 twin max {max(m2.values()):.4f}; M3 equal-phase write {m3['test_acc']:.4f}; item 5 twin write " + json.dumps({n: round(r["test_acc"], 4) for n, r in tw_w.items()}))
    b3 = {"train_acc": S.evaluate(s3, X[tr], y[tr])[1], "test_acc": S.evaluate(s3, X[te], y[te])[1]}
    c3, f3, ph3 = census(s3, P, X)
    s3sets = picks_for(s3, P, X, y, tr, te, t3, f3, ph3, grid)
    s3sets.pop("m1", None)
    s3rows = score(s3, s3sets, X, y, tr, te, t3)
    frac = lambda r: r["train_acc"] / b3["train_acc"]
    m4 = max([frac(s3rows["omp"][n]) for n in grid] + ([frac(s3rows["joint"][n]) for n in grid] if "joint" in s3rows else []))
    s3w = {}
    for m in P["write_m"] if f3 else []:   # council pin (2): optional, unscored; dropped when s3 has no families
        mw, ids, r2 = write(s3, X, tr, list(f3), m, p)
        s3w[len(ids)] = {**Z.arm(mw, ids, X, y, tr, te, t3)[0], "probe_r2_mean": float(np.mean(r2))}
    log(f"s3 census {b3} {c3}; M4 max (b)/(c) train-acc fraction at N <= 32: {m4:.4f}")
    acc = lambda d: {n: r["test_acc"] for n, r in d.items()}
    A = {"rand": {s: acc(d) for s, d in rows["rand"].items()}, "joint": acc(rows["joint"]), "m1": acc(rows["m1"]), "omp": acc(rows["omp"]),
         "write": acc(wr), "m2_max": max(m2.values()), "m3": m3["test_acc"], "m4_max_frac": m4}
    V = verdicts(A, P)
    uerr = [r["u_err"] for a in ("joint", "m1", "omp") for r in rows[a].values()] + [r["u_err"] for d in rows["rand"].values() for r in d.values()]
    void += [f"u error {max(uerr)} > {P['u_tol']}"] * (max(uerr) > P["u_tol"]) + ["wall cap"] * (time.time() - t0 > P["wall_cap_s"])
    void += ["params.json changed since launch"] * (json.load(open(fs))["params_sha256"] != psha)
    if void:
        V.update(H1="void", H2="void", H3="void")
    Rk = lambda ids: {k: {"R_sum": R([ph[i][0] + ph[i][1] for i in ids if i in fams[k]]), "R_diff": R([ph[i][0] - ph[i][1] for i in ids if i in fams[k]])} for k in fams}
    res = {"void": void, **V, "params_sha256": psha, "launch_sha256": json.load(open(fs))["params_sha256"], "torch": torch.__version__,
           "numpy": np.__version__, "baseline_test_acc": base, "self_check_512": full, "max_u_err": max(uerr), "census_pc": cen,
           "key_frequencies": ks, "arms": rows, "write": wr, "m3": m3, "m2": m2, "twin_write_item5": tw_w,
           "phase_R_at_32": {"joint": Rk(sets["joint"][32]), "m1": Rk(sets["m1"][32]), "rand_0": Rk(sets["rand"][0][32])},
           "s3": {"baseline": b3, "census": c3, "arms": s3rows, "m4_max_frac": m4, "write_unscored": s3w}, "picks": sets, "s3_picks": s3sets, "twin_sets": tsets,
           "wall_s": round(time.time() - t0, 1)}
    json.dump(res, open(os.path.join(out, "results.json"), "w"), indent=1)
    rr = lambda d, n: f"{d[n]['test_acc']:.4f}" if n in d else "-"
    lines = [f"# JOINT PHASE / CEILING / WRITE: H1 {V['H1']} · H2 {V['H2']} · H3 {V['H3']}", "",
             f"- N_b {V['N_b']}, N_c {V['N_c']}, N_r {V['N_r']} {V['N_r_by_seed']}, N_w hits {V['N_w_hits']}; M1 {V['M1_red']} M2 {V['M2_red']} M3 {V['M3_red']} M4 {V['M4_red']}; void {void}",
             "", "| N | joint (b) | M1 | OMP (c) | write (d) | " + " | ".join(f"rand {s}" for s in P["random_seeds"]) + " |", "|---|---|---|---|---|" + "---|" * len(P["random_seeds"])]
    lines += [f"| {n} | {rr(rows['joint'], n)} | {rr(rows['m1'], n)} | {rr(rows['omp'], n)} | {rr(wr, n)} | " + " | ".join(rr(rows['rand'][s], n) for s in P["random_seeds"]) + " |"
              for n in grid + P["n_grid_random_extra"]]
    open(os.path.join(out, "summary.md"), "w").write("\n".join(lines) + "\n")
    log(f"H1 {V['H1']} H2 {V['H2']} H3 {V['H3']} void {void} ({res['wall_s']}s)")


if __name__ == "__main__":
    main()
