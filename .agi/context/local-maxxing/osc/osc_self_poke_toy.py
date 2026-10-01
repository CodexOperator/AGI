#!/usr/bin/env python3
"""STAGE-2 HARNESS REHEARSAL (hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy): a controller
scales a family's W_out columns on the sha-pinned PC toy (its pipeline imported, unchanged) under REAL / SHAM / BLIND
arms; the stand-in report = mean entropy. Grid = <cell osc_self_poke_toy_dir>/params.json. Void run: move aside."""
import hashlib, json, os, subprocess, sys, time
import numpy as np, safetensors.torch as ST, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period2 as R2  # noqa: E402  R2.S.wait_box
import osc_neuron_period_pc as PC  # noqa: E402  OneLayer, make, data, evaluate, sweep, stat, null (unchanged)
import paths  # noqa: E402

sha_file = lambda path: hashlib.sha256(open(path, "rb").read()).hexdigest()
dump = lambda path, rows: open(path, "w").write("".join(json.dumps(r) + "\n" for r in rows))


def state_sha(model):   # sha256 over every named tensor's bytes, names sorted
    h = hashlib.sha256()
    for k, v in sorted(model.state_dict().items()):
        h.update(k.encode() + v.detach().contiguous().numpy().tobytes())
    return h.hexdigest()


def edit(model, ids, s):   # the controller's reversible scale: W_out column i is neuron i
    with torch.no_grad():
        model.w_out.weight[:, ids] *= s


def restore(model, ckpt):   # reload every weight from the checkpoint (torch zip, or safetensors by magic) -> state sha
    model.load_state_dict(torch.load(ckpt) if open(ckpt, "rb").read(2) == b"PK" else ST.load_file(ckpt))
    return state_sha(model)


def readout(model, X):   # r = mean predictive entropy (nats), float64; the model's outputs only
    with torch.no_grad():
        lp = torch.log_softmax(model(X).double(), 1)
    return float(-(lp.exp() * lp).sum(1).mean())


def probe(X, seed, n):   # n distinct rows of X by a seeded draw
    return X[torch.from_numpy(np.random.default_rng(seed).choice(len(X), n, replace=False))]


def families(model, Pc):   # PC's P1 neurons grouped by dominant frequency, by the IMPORTED sweep / stat / null
    tol, acts = Pc["detrend_tol"], PC.sweep(model.eval(), Pc)
    (pk, kb), tmax = PC.stat(acts, tol), float(PC.stat(PC.sweep(PC.make(Pc, Pc["twin_seed"]).eval(), Pc), tol)[0].max())
    p1 = np.flatnonzero((pk > float(np.quantile(PC.null(acts, Pc), Pc["null_quantile"]))) & (pk > tmax))
    return {int(k): [int(i) for i in p1 if kb[i] == k] for k in np.unique(kb[p1])}


def run_trial(model, ckpt, X, t, fams, n, consent=lambda t: True):   # the default stub: a toy has no language
    """REAL / BLIND ask consent, then edit; SHAM never edits; every trial ends by reloading from the checkpoint.
    The arm picks the edit; the told flag is bookkeeping and reaches no computation here."""
    ok = None if t["arm"] == "SHAM" else bool(consent(t))
    if ok:
        edit(model, fams[t["family"]], t["s"])
    r = readout(model, probe(X, t["probe_seed"], n))
    return r, {"consent": "not asked (sham)" if ok is None else "n/a (toy)", "edit_applied": bool(ok),
               "declined": ok is False, "restore_sha": restore(model, ckpt)}


def score(reports, r_ref, tau):
    """Reports only ({trial, r}); a record carrying any other column (a key column) is refused."""
    if bad := sorted({k for rec in reports for k in rec if k not in ("trial", "r")}):
        raise ValueError(f"scorer refuses key column(s) {bad}")
    return {rec["trial"]: {"r": rec["r"], "edited": abs(rec["r"] - r_ref) > tau} for rec in reports}


def schedule(P):   # 4 families x 2 scales x reps x 3 arms, shuffled by order_seed, ids assigned after the shuffle
    rows = [{"family": k, "s": s, "rep": rep, "arm": arm, "told": arm != "BLIND",
             "probe_seed": P["probe_seed_base"] + (fi * len(P["scales"]) + si) * P["reps"] + rep}
            for fi, k in enumerate(P["families"]) for si, s in enumerate(P["scales"])
            for rep in range(P["reps"]) for arm in P["arms"]]
    rows = [rows[i] for i in np.random.default_rng(P["order_seed"]).permutation(len(rows))]
    return [{"trial": f"t{i:03d}", **r} for i, r in enumerate(rows)]


def debrief(out, rows, recs):
    """Written only after scores.json exists; line 0 names the scores / reports sha256."""
    assert os.path.exists(sc := os.path.join(out, "scores.json")), "debrief before the scored file is closed"
    head = {"scores_sha256": sha_file(sc), "reports_sha256": sha_file(os.path.join(out, "reports.jsonl"))}
    dump(os.path.join(out, "debrief.jsonl"), [head] + [{**t, **recs[t["trial"]]} for t in rows])
    return head


def main():
    out = paths.get_local("osc_self_poke_toy_dir")
    pp, f = os.path.join(out, "params.json"), lambda n: os.path.join(out, n)
    P, sha = json.load(open(pp)), sha_file(pp)
    sys.exit("scores.json exists: a finished session is never overwritten") if os.path.exists(f("scores.json")) else 0
    log = lambda m: print(m, flush=True)   # the launcher redirects stdout to <out>/run.log
    t0 = (torch.set_num_threads(P["threads"]), R2.S.wait_box(P), time.time())[2]
    pc = paths.get_local(P["pc_dir_cell"])
    ckpt, Pc = os.path.join(pc, "model.pt"), json.load(open(os.path.join(pc, "params.json")))
    fsha0, model = sha_file(ckpt), PC.make(Pc, Pc["train_seed"]).eval()
    sha0, (X, y, tr, te), n = restore(model, ckpt), PC.data(Pc), P["probe_size"]
    base, fams, rows = PC.evaluate(model, X[te], y[te])[1], families(model, Pc), schedule(P)
    rd = lambda seed: readout(model, probe(X, seed, n))
    ru = {t["probe_seed"]: rd(t["probe_seed"]) for t in rows}   # the unedited r per probe seed (C2 / C4 reference)
    r_ref, taus = rd(P["ref_seed"]), [rd(P["tau_seed_base"] + i) for i in range(P["tau_n"])]
    tau = P["tau_mult"] * float(np.std(taus, ddof=1))
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a, "--", __file__, pp], capture_output=True, text=True)
    commit, dirty = git("log", "-1", "--format=%H").stdout.strip(), git("diff", "--quiet", "HEAD").returncode != 0
    log(f"launch: params {sha}, script {commit or 'NONE'} dirty {dirty}, r_ref {r_ref}, tau {tau}, state {sha0}")
    dump(f("key.jsonl"), rows)
    reports, recs = [], {}
    for t in rows:
        sys.exit("wall cap reached: no scores written") if time.time() - t0 > P["wall_cap_s"] else 0
        r, recs[t["trial"]] = run_trial(model, ckpt, X, {k: t[k] for k in t.keys() - {"told"}}, fams, n)
        reports.append({"trial": t["trial"], "r": r})
    dump(f("reports.jsonl"), reports)
    S = score([json.loads(l) for l in open(f("reports.jsonl"))], r_ref, tau)   # reports only
    json.dump(S, open(f("scores.json"), "w"), indent=0)
    sel = lambda k, s, arm: [t for t in rows if (t["family"], t["s"], t["arm"]) == (k, s, arm)]
    rate = lambda ts: sum(S[t["trial"]]["edited"] for t in ts) / len(ts)
    sham, lb, ps = [t for t in rows if t["arm"] == "SHAM"], P["families"][:2], P["families"][2:]
    rr = lambda t: S[t["trial"]]["r"]
    pair = {(t["family"], t["s"], t["rep"]): rr(t) for t in rows if t["arm"] == "REAL"}
    c3b = sum(rr(t) == pair[(t["family"], t["s"], t["rep"])] for t in rows if t["arm"] == "BLIND")
    c2 = sum(rr(t) == ru[t["probe_seed"]] for t in sham)
    c1 = sum(d["restore_sha"] == sha0 for d in recs.values())
    drop0 = {k: float(np.mean([abs(rr(t) - ru[t["probe_seed"]]) for t in sel(k, 0.0, "REAL")])) for k in P["families"]}
    det0 = {k: rate(sel(k, 0.0, "REAL")) for k in P["families"]}
    v = {"C1": c1 == len(rows) and sha_file(ckpt) == fsha0 == P["pc_model_sha256"], "C2": c2 == len(sham),
         "C3": all(det0[k] >= P["c3_real_min"] for k in lb) and rate(sham) <= P["c3_sham_max"],
         "C3b": c3b == len(sham), "C4": min(drop0[k] for k in lb) > max(drop0[k] for k in ps)}
    void = not (fsha0 == P["pc_model_sha256"] and sha_file(os.path.join(pc, "params.json")) == P["pc_params_sha256"]
                and abs(base - P["baseline_test_acc"]) <= P["baseline_test_acc_tol"]
                and {str(k): len(fams.get(k, [])) for k in P["families"]} == P["family_sizes"]
                and commit and len(git("ls-files").stdout.split()) == 2 and not dirty and sha_file(pp) == sha)
    R = {"verdict": "void" if void else "proved" if all(v.values()) else "disproved", "void": void, "conjuncts": v,
         "C1": {"restores_equal": c1, "n_trials": len(rows), "file_sha_start": fsha0, "file_sha_end": sha_file(ckpt)},
         "C2": {"sham_identical": c2, "n_sham": len(sham)}, "C3b": {"real_blind_identical": c3b, "n_pairs": len(sham)},
         "C3": {"det_rate_s0": det0, "sham_rate": rate(sham), "n_sham": len(sham)}, "C4": {"mean_abs_dr_s0": drop0},
         "r_ref": r_ref, "tau": tau, "tau_sd": float(np.std(taus, ddof=1)), "baseline_test_acc": base,
         "family_sizes": {k: len(m) for k, m in fams.items()}, "params_sha256": sha, "script_commit": commit,
         "script_dirty": dirty, "debrief_head": debrief(out, rows, recs), "torch": torch.__version__,
         "unscored": {"det_rate_s05": {k: rate(sel(k, 0.5, "REAL")) for k in P["families"]},
                      "r_by_arm_mean_sd_min_max": {a: [float(g([rr(t) for t in rows if t["arm"] == a])) for g in
                                                       (np.mean, np.std, np.min, np.max)] for a in P["arms"]}}}
    json.dump(R, open(f("results.json"), "w"), indent=1)
    log(t := "\n".join([f"# SELF-POKE TOY: {R['verdict']}", ""] + [f"- {k}: {json.dumps(x)}" for k, x in R.items()]))
    open(f("summary.md"), "w").write(t + "\n")


if __name__ == "__main__":
    main()
