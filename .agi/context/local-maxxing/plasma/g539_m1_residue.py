"""goal:g5.39 residue (SM's gate via thought-master [fix] 12:41Z 11-05): g539_joint_samples.sample_p(frozen=True)
broadcasts ONE noise row over the 64 samples, so M1 reads one image per cue (coverage 0) for ANY net.
Does g5.39's verdict move with a per-sample M1? g5.39's script is imported, never edited.

  (a) per-sample PASS: 64 separate forward passes, each with the SAME frozen row drawn from g5.39's M1 stream
      (the leaf's text, "ONE noise draw frozen per seed and cue", without the broadcast)
  (b) per-sample DRAW: each of the 64 samples gets its OWN row, drawn once from the M1 stream and frozen
      (a recorded tape: in distribution this is the arm P itself, not a mutant of it)

  python g539_m1_residue.py G539_PARAMS G539_RESULTS OUT_JSON
"""
import json
import sys

import numpy as np

import g539_joint_samples as E
import g541_blend_race as R


def m1_variants(net, cue, sigma, n, seed, si):
    h = E.hidden_pre(net, E.onehot(cue, 1))[0]
    (_, _), (w2, b2) = net
    committed = E.sample_p(net, cue, sigma, n, E.rng_for(seed, E.M1_STREAM, E.ARM_P, si, cue), frozen=True)
    row = E.rng_for(seed, E.M1_STREAM, E.ARM_P, si, cue).normal(0.0, sigma, size=(1, h.shape[0]))[0]
    a = np.stack([((np.maximum(h + row, 0.0) @ w2 + b2) > 0).astype(np.float64) for _ in range(n)])
    rows = E.rng_for(seed, E.M1_STREAM, E.ARM_P, si, cue).normal(0.0, sigma, size=(n, h.shape[0]))
    b = np.stack([((np.maximum(h + r, 0.0) @ w2 + b2) > 0).astype(np.float64) for r in rows])
    return committed, a, b


def main(argv):
    p, res39 = json.load(open(argv[1])), json.load(open(argv[2]))
    sigma = 2.0  # g5.39's sigma* (verdict.json)
    si = p["sigmas"].index(sigma)
    tmpl, tcls = E.templates(p)
    rows = []
    for seed, r39 in zip(p["seeds"], res39["seeds"]):
        x, t = R.targets_and_sparse(seed, p)
        ss = np.random.SeedSequence(seed)
        r_init, r_batch, r_tnoise = [np.random.default_rng(s) for s in ss.spawn(4)[1:]]
        net = E.init_net(r_init, p["sizes"])
        bs, ts = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))
        net = E.train(net, x, t, sigma, p["k_best_of"], p["train"], np.random.default_rng(bs), np.random.default_rng(ts))
        cells = {"committed": [], "a_per_sample_pass": [], "b_per_sample_draw": []}
        same_a = True
        for c in (0, 1):
            com, a, b = m1_variants(net, c, sigma, p["n_samples"], seed, si)
            same_a &= bool(np.array_equal(com, a))
            for k, s in (("committed", com), ("a_per_sample_pass", a), ("b_per_sample_draw", b)):
                cells[k].append(E.score(s, c, tmpl, tcls, p["score"]["iou_min"]))
        row = {k: E.score_cues(v) for k, v in cells.items()}
        row.update({"seed": seed, "a_equals_committed_bytes": same_a,
                    "committed_matches_results_json": row["committed"]["score"] == r39["M1"][str(sigma)]["score"]})
        rows.append(row)
    out = {"leaf": "goal:g5.39", "residue": "M1 broadcast (SM gate, 12:41Z 11-05)", "numpy": np.__version__,
           "sigma": sigma, "seeds": rows,
           "max_score": {k: max(r[k]["score"] for r in rows) for k in ("committed", "a_per_sample_pass", "b_per_sample_draw")}}
    with open(argv[3], "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv)
