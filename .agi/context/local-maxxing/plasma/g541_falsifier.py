"""goal:g5.41 falsifier, the council's text (goal:g5.41 ## Falsifier), committed BEFORE any step-1 run.

  python g541_falsifier.py STEP0_JSON RESULTS_JSON    exit 0 = done (verdict printed), 2 = not done

Every sigma* is the best MEAN VALIDATION score over the 5 seeds, per arm (G, GC, GP); scores, valid
fractions and coverages are TEST means over seeds and cues; "paired" = per seed, on test score.
  S-OUT     PROVED iff S valid >= 0.5 AND S - G(sigma*) > 0 on 5/5 seeds with mean > 0.05.
  S-MECH    PROVED iff STEP 0's BLEND share >= 0.5 of g5.39's invalid samples AND S's BLEND share of its
            own invalid samples < G(sigma*)'s on 5/5 seeds (a share with no invalid samples = 0).
            STEP 0 < 0.5 -> S-MECH is RED at the pre-run.
  G-CHAMFER PROVED iff GC(sigma*) valid >= 0.5 AND coverage >= 0.9 AND GC - G(sigma*) > 0 on 5/5 seeds
            with mean > 0.05.
  Mutants   M1-S (S, every unit at its likelier state) <= 0.05 on every seed, else S-OUT and S-MECH VOID;
            M1-C (GC(sigma*), one draw frozen per seed and cue) <= 0.05 on every seed, else G-CHAMFER VOID;
            M2 (true lines >= 0.9, Bernoulli(0.5) valid <= 0.05, every seed), else EVERY line VOID.
  PREDICTION (remix, REPORTED): BLEND >= 0.5 predicts S > GC on mean test score; else GC >= S.
  REPORTED, no claim: SC, GP, Z, MF. Each line is judged only against G on its own text.
"""
import json
import os
import sys

DELTA_MIN, VALID_MIN, COV_MIN, BLEND_MIN, M1_MAX, M2_TRUE_MIN, M2_COIN_MAX = 0.05, 0.5, 0.9, 0.5, 0.05, 0.9, 0.05


def mean(xs):
    return sum(xs) / len(xs)


def best(seeds, arm, sigmas):
    return max(sigmas, key=lambda s: mean([x[arm][s]["val"]["score"] for x in seeds]))


def test_means(cells):
    return {k: mean([c["test"][k] for c in cells]) for k in ("valid", "coverage", "score", "blend_share")}


def judge(step0, res):
    seeds = res["seeds"]
    sig = [str(s) for s in res["params"]["sigmas"]]
    sg, sc, sp = best(seeds, "G", sig), best(seeds, "GC", sig), best(seeds, "GP", sig)
    g = [x["G"][sg] for x in seeds]
    s = [x["S"] for x in seeds]
    c = [x["GC"][sc] for x in seeds]
    g_sc = [x["test"]["score"] for x in g]
    d_s = [a["test"]["score"] - b for a, b in zip(s, g_sc)]
    d_c = [a["test"]["score"] - b for a, b in zip(c, g_sc)]
    ms, mc = test_means(s), test_means(c)
    blend0 = step0["blend_share"]
    s_out = ms["valid"] >= VALID_MIN and all(v > 0 for v in d_s) and mean(d_s) > DELTA_MIN
    s_mech_lower = [a["test"]["blend_share"] < b["test"]["blend_share"] for a, b in zip(s, g)]
    s_mech = blend0 >= BLEND_MIN and all(s_mech_lower)
    g_ch = mc["valid"] >= VALID_MIN and mc["coverage"] >= COV_MIN and all(v > 0 for v in d_c) and mean(d_c) > DELTA_MIN
    m1s = [x["M1_S"]["score"] for x in seeds]
    m1c = [x["M1_C"][sc]["score"] for x in seeds]
    m2t = [x["M2_true"]["score"] for x in seeds]
    m2c = [x["M2_coin"]["valid"] for x in seeds]
    m1s_red, m1c_red = max(m1s) <= M1_MAX, max(m1c) <= M1_MAX
    m2_red = min(m2t) >= M2_TRUE_MIN and max(m2c) <= M2_COIN_MAX

    def line(ok, red_mutant):
        return "VOID" if not (m2_red and red_mutant) else ("PROVED" if ok else "DISPROVED")

    predicts_s = blend0 >= BLEND_MIN
    came_true = (ms["score"] > mc["score"]) if predicts_s else (mc["score"] >= ms["score"])
    rep = lambda arm: test_means([x[arm] for x in seeds])
    return {
        "S-OUT": line(s_out, m1s_red), "S-MECH": line(s_mech, m1s_red), "G-CHAMFER": line(g_ch, m1c_red),
        "s_mech_red_at_pre_run": blend0 < BLEND_MIN,
        "sigma_star": {"G": sg, "GC": sc, "GP": sp},
        "step0_blend_share": blend0, "step0_shares": step0["shares"],
        "S": ms, "GC": mc, "G": test_means(g),
        "delta_S_minus_G": d_s, "delta_GC_minus_G": d_c,
        "S_blend_below_G": s_mech_lower,
        "S_blend_share": [a["test"]["blend_share"] for a in s], "G_blend_share": [b["test"]["blend_share"] for b in g],
        "mutants": {"M1_S": m1s, "M1_S_red": m1s_red, "M1_C": m1c, "M1_C_red": m1c_red,
                    "M2_true": m2t, "M2_coin_valid": m2c, "M2_red": m2_red},
        "prediction": {"predicts": "S > GC" if predicts_s else "GC >= S", "came_true": came_true},
        "reported": {"SC": rep("SC"), "Z": rep("Z"), "GP": test_means([x["GP"][sp] for x in seeds]),
                     "MF": {k: mean([x["MF"][sg][k] for x in seeds]) for k in ("valid", "coverage", "score")}},
        "val": {arm: {s_: mean([x[arm][s_]["val"]["score"] for x in seeds]) for s_ in sig} for arm in ("G", "GC", "GP")},
    }


def main(argv):
    if len(argv) < 3 or not (os.path.exists(argv[1]) and os.path.exists(argv[2])):
        print("NOT DONE: no step-0 or step-1 results file")
        return 2
    print(json.dumps(judge(json.load(open(argv[1])), json.load(open(argv[2]))), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
