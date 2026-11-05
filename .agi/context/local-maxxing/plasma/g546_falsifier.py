"""goal:g5.46 falsifier, the council's text (goal:g5.46 ## Falsifier), committed BEFORE any run.

  python g546_falsifier.py RESULTS_JSON    exit 0 = done (verdict printed), 2 = not done

CV = CV2 (z in R^2). Means are TEST means over seeds and cues (64 samples per cue); "distinct" = distinct
valid images per cue, min over cues; "of 512" = among 512 prior samples per cue (its own RICH stream).
  CV-OUT  PROVED iff CV valid >= 0.5 AND coverage >= 0.9 AND distinct (of 64) >= 14 on EVERY seed;
          a seed whose KL < 0.01 nats (posterior collapse) reads RED on its own.
  L-RICH  PROVED iff on EVERY seed CV valid >= 0.5 AND coverage >= 0.9 AND distinct of 512 > 64.
  MK      CV with z ZEROED in training, z ~ N(0, I) at sampling: score <= 0.05 AND distinct of 512 <= 16
          (MAX over cues) on every seed, else a PROVED CV-OUT or L-RICH is VOID; a RED stands even if MK
          fails (leaf v2: a vacuity mutant never VOIDs a deserved RED).
  MC      the distinct counter on 512 true target lines per cue reads >= 150 on every seed, MIN over cues,
          else L-RICH VOID (either way).
  M2      the scorer as in g5.39, else the round is VOID.
REPORTED: distinct-over-latent for CV and Z3, KL per seed, CV1 and CV4, CV's BLEND / SPARSE / OTHER split
with remix's prediction (BLEND the largest share).
"""
import json
import os
import sys

VALID_MIN, COV_MIN, DISTINCT_OUT, RICH_MIN, KL_MIN = 0.5, 0.9, 14, 64, 0.01
MK_SCORE_MAX, MK_DISTINCT_MAX, MC_MIN, M2_TRUE_MIN, M2_COIN_MAX = 0.05, 16, 150, 0.9, 0.05


def mean(xs):
    return sum(xs) / len(xs)


def judge(res):
    seeds = res["seeds"]
    cv = [x["CV2"] for x in seeds]
    tm = lambda cells, k: mean([c["test"][k] for c in cells])
    v, cov = tm(cv, "valid"), tm(cv, "coverage")
    dist64 = [c["test"]["distinct_valid_min"] for c in cv]
    rich = [min(c["rich_distinct"]) for c in cv]
    kls = [c["kl_nats"] for c in cv]
    collapsed = [k < KL_MIN for k in kls]
    cv_out = v >= VALID_MIN and cov >= COV_MIN and all(dd >= DISTINCT_OUT for dd in dist64) and not any(collapsed)
    l_rich = all(c["test"]["valid"] >= VALID_MIN and c["test"]["coverage"] >= COV_MIN and r > RICH_MIN
                 for c, r in zip(cv, rich))
    mk = [x["MK"] for x in seeds]
    mk_red = all(c["test"]["score"] <= MK_SCORE_MAX and max(c["rich_distinct"]) <= MK_DISTINCT_MAX for c in mk)
    mc = [min(x["MC_distinct"]) for x in seeds]
    mc_red = min(mc) >= MC_MIN
    m2t = [x["M2_true"]["score"] for x in seeds]
    m2c = [x["M2_coin"]["valid"] for x in seeds]
    m2_red = min(m2t) >= M2_TRUE_MIN and max(m2c) <= M2_COIN_MAX

    def line(ok, mk_ok, other_ok=True):
        """M2 and MC VOID either way; MK VOIDs a PROVED read only (leaf v2)."""
        if not (m2_red and other_ok):
            return "VOID"
        if not ok:
            return "DISPROVED"
        return "PROVED" if mk_ok else "VOID"

    inv = {k: sum(c["split"][k] for c in cv) for k in ("blend", "sparse", "other")}
    tot = sum(inv.values())
    shares = {k: (n / tot if tot else 0.0) for k, n in inv.items()}
    rep = {}
    for a in ("CV2", "CV1", "CV4", "MK", "Z3-ENUM"):
        cells = [x[a] for x in seeds]
        rep[a] = {k: tm(cells, k) for k in ("valid", "coverage", "score")}
        rep[a]["distinct_of_64_min"] = [c["test"]["distinct_valid_min"] for c in cells]
        rep[a]["distinct_of_512_min"] = [min(c["rich_distinct"]) for c in cells]
        if "kl_nats" in cells[0]:
            rep[a]["kl_nats"] = [c["kl_nats"] for c in cells]
    return {
        "CV-OUT": line(cv_out, mk_red), "L-RICH": line(l_rich, mk_red, mc_red),
        "cv_valid": v, "cv_coverage": cov, "cv_distinct_of_64_min": dist64, "cv_distinct_of_512_min": rich,
        "cv_kl_nats": kls, "collapsed_seeds": collapsed,
        "cv_per_seed": [{"valid": c["test"]["valid"], "coverage": c["test"]["coverage"]} for c in cv],
        "mutants": {"MK_score": [c["test"]["score"] for c in mk], "MK_distinct_of_512_max": [max(c["rich_distinct"]) for c in mk],
                    "MK_red": mk_red, "MC_distinct_min": mc, "MC_red": mc_red,
                    "M2_true": m2t, "M2_coin_valid": m2c, "M2_red": m2_red},
        "prediction_blend_largest": {"shares": shares, "came_true": tot > 0 and shares["blend"] == max(shares.values())},
        "arms": rep,
    }


def main(argv):
    if len(argv) < 2 or not os.path.exists(argv[1]):
        print("NOT DONE: no results file")
        return 2
    print(json.dumps(judge(json.load(open(argv[1]))), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
