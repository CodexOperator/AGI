#!/usr/bin/env python3
"""CORRECTIVE DH.1 (hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy): C5 (scored) = the 4
families vs 20 random 128-sets at s = 0, common probes; run 2's C3 re-scored vs the median reference; a dose-response
(unscored). Run 2's helpers imported unchanged. Grid = <cell osc_self_poke_toy_dh1_dir>/params.json."""
import json, os, subprocess, sys
import numpy as np, torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_self_poke_toy as T  # noqa: E402  edit / restore / readout / probe / families / score / sha_file (unchanged)
rand_sets = lambda P, n: {f"rand{j}": sorted(int(i) for i in np.random.default_rng(P["set_seed_base"] + j).choice(
    n, P["set_size"], replace=False)) for j in range(P["n_random"])}


def main():
    out, run2 = T.paths.get_local("osc_self_poke_toy_dh1_dir"), T.paths.get_local("osc_self_poke_toy_dir")
    f = lambda n: os.path.join(out, n)
    P, sha = json.load(open(pp := f("params.json"))), T.sha_file(pp)
    sys.exit("results.json exists: a finished session is never overwritten") if os.path.exists(f("results.json")) else 0
    torch.set_num_threads(P["threads"]), T.R2.S.wait_box(P)
    pc = T.paths.get_local(P["pc_dir_cell"])
    ckpt, Pc = os.path.join(pc, "model.pt"), json.load(open(os.path.join(pc, "params.json")))
    fsha0, model = T.sha_file(ckpt), T.PC.make(Pc, Pc["train_seed"]).eval()
    sha0, (X, y, tr, te), n = T.restore(model, ckpt), T.PC.data(Pc), P["probe_size"]
    base, fams = T.PC.evaluate(model, X[te], y[te])[1], T.families(model, Pc)
    S = {**{f"k{k}": fams[k] for k in P["families"]}, **rand_sets(P, Pc["model"]["d_mlp"])}
    rd = lambda seed: T.readout(model, T.probe(X, seed, n))
    seeds, taus = [P["c5_base"] + r for r in range(P["reps"])], [rd(P["tau_base"] + i) for i in range(P["tau_n"])]
    ru, r_med, tau = {s: rd(s) for s in seeds}, float(np.median(taus)), P["tau_mult"] * float(np.std(taus, ddof=1))
    D, ok = {}, True   # (set, s) -> [(abs(r - r_unedited), call, r)] per common seed; ok = every restore equals sha0
    for name, ids in S.items():
        for s in P["scales"]:
            D[(name, s)] = []
            for sd in seeds:
                r = (T.edit(model, ids, s), rd(sd))[1]   # edit, then read
                ok &= T.restore(model, ckpt) == sha0
                D[name, s].append((abs(r - ru[sd]), abs(r - r_med) > tau, r))
    open(f("raw.jsonl"), "w").write("".join(   # the per-trial raw rows
        json.dumps({"set": k[0], "s": k[1], "seed": seeds[i], **dict(zip(("dr", "call", "r"), d))}) + "\n"
        for k, v in D.items() for i, d in enumerate(v)))
    mean = lambda name, s, i=0: float(np.mean([d[i] for d in D[(name, s)]]))   # i 0 = mean abs dr, 1 = detection rate
    dr, rnd = {k: mean(k, 0.0) for k in S}, [mean(k, 0.0) for k in S if k.startswith("rand")]
    c5a, c5b = (min(dr[f"k{k}"] for k in P["bearing"]) > max(rnd), max(dr[f"k{k}"] for k in P["passengers"]) < min(rnd))
    norm = {k: float(model.w_out.weight.detach()[:, ids].norm(dim=0).mean()) for k, ids in S.items()}
    rho = float(np.corrcoef(*[np.argsort(np.argsort([m[k] for k in S])) for m in (dr, norm)])[0, 1])   # Spearman
    sc, key = T.score((rd2 := lambda nm: [json.loads(l) for l in open(os.path.join(run2, nm))])("reports.jsonl"),
                      r_med, tau), rd2("key.jsonl")   # run 2's C3 re-scored against the median reference
    rate = lambda arm, k=None: float(np.mean([sc[t["trial"]]["edited"] for t in key if t["arm"] == arm and (
        k is None or (t["family"], t["s"]) == (k, 0.0))]))
    c3 = {"det_rate_s0": {k: rate("REAL", k) for k in P["families"]}, "sham_rate": rate("SHAM")}
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a, "--", __file__, pp], capture_output=True, text=True)
    commit, dirty = git("log", "-1", "--format=%H").stdout.strip(), git("diff", "--quiet", "HEAD").returncode != 0
    void = not (fsha0 == P["pc_model_sha256"] and T.sha_file(os.path.join(pc, "params.json")) == P["pc_params_sha256"]
                and abs(base - P["baseline_test_acc"]) <= P["baseline_test_acc_tol"] and ok and T.sha_file(pp) == sha
                and {str(k): len(fams.get(k, [])) for k in P["families"]} == P["family_sizes"]
                and commit and len(git("ls-files").stdout.split()) == 2 and not dirty)
    R = {"verdict": "void" if void else "stands" if c5a and c5b else "demoted", "void": void,
         "c5a": c5a, "c5b": c5b, "dr": dr, "c3": c3, "r_med": r_med, "tau": tau, "sha": sha, "commit": commit,
         "unscored": {"w_out_col_norm": norm, "spearman_dr_norm": rho,
                      "detect_by_scale": {k: {str(s): mean(k, s, 1) for s in P["scales"]} for k in S},
                      "dr_by_scale": {k: {str(s): mean(k, s) for s in P["scales"]} for k in S}}}
    json.dump(R, open(f("results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
