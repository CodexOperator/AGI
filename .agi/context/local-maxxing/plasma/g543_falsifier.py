"""goal:g5.43 falsifier, the council's text (goal:g5.43 ## Falsifier), committed BEFORE any run.

  python g543_falsifier.py RESULTS_JSON    exit 0 = done (verdict printed), 2 = not done

TEST means over seeds and cues unless a line says "every seed"; "paired" = per seed, on test score;
"X vs Y" = the delta X - Y; each sigma* = its arm's best MEAN VALIDATION score.
  L-REP     (the gate) PROVED iff Z3-ENUM valid >= 0.5 AND coverage >= 0.9. RED -> line 3 (L-ENUM,
            L-STATES, L-DISC) is NOT READ; L-Z and L-Z6 are always read (leaf v2).
  L-Z       PROVED iff Z3-ENUM valid >= 0.5 AND coverage >= 0.9 AND Z3-ENUM - G(sigma*) > 0 on 5/5 seeds
            with mean > 0.05.
  L-ENUM    Z3-ENUM - Z3-SAMP; L-STATES Z3-SAMP - Z5-SAMP; L-DISC Z3-SAMP - C3-SAMP: each PROVED iff the
            paired delta is > 0 on 5/5 seeds with mean > 0.05.
  L-Z6      PROVED iff on EVERY seed Z6-ENUM valid >= 0.5 AND coverage >= 0.9 AND distinct valid images
            >= 16 in EACH cue's 64 samples, AND Z6-ENUM - G64(sigma*) > 0 on 5/5 seeds with mean > 0.05.
  Mutants   (leaf v2) Mz1: EVERY latent arm (Z3-ENUM, Z3-SAMP, Z5-SAMP, C3-SAMP, Z6-ENUM), latent frozen to ONE
            seeded draw per seed and cue, scores <= 0.05 on every seed; a failing Mz1 on either arm of a pair
            VOIDs that pair's line (L-ENUM, L-STATES, L-DISC). It is vacuous on the sigma-0 ENUM arms and never
            guards L-REP or L-Z. Mz6: Z6-ENUM sampled through (code mod 8) has distinct valid images < 16 in
            EACH cue on every seed, else L-Z6 is VOID. Mz2: MZ2 (one uniform code per target per step, K = 1)
            valid <= 0.1 on every seed, else L-ENUM is VOID. M2: the scorer as in g5.39, else EVERY line VOID.
REPORTED, no claim: win fraction per discrete arm, distinct valid images for every arm, Z2/Z3/Z4-ENUM.
"""
import json
import os
import sys

DELTA_MIN, VALID_MIN, COV_MIN, DISTINCT_MIN, M1_MAX, MZ2_MAX, M2_TRUE_MIN, M2_COIN_MAX = \
    0.05, 0.5, 0.9, 16, 0.05, 0.1, 0.9, 0.05
CLAIMED = ("Z3-ENUM", "Z3-SAMP", "Z5-SAMP", "C3-SAMP", "Z6-ENUM")


def mean(xs):
    return sum(xs) / len(xs)


def paired(a, b):
    d = [x - y for x, y in zip(a, b)]
    return d, all(v > 0 for v in d) and mean(d) > DELTA_MIN


def judge(res):
    seeds, p = res["seeds"], res["params"]
    star = {arm: max([str(s) for s in p[key]], key=lambda s: mean([x[arm][s]["val"]["score"] for x in seeds]))
            for arm, key in (("G", "sigmas_g"), ("G64", "sigmas_g64"))}
    sc = lambda arm: [x[arm][star[arm]]["test"]["score"] if arm in star else x[arm]["test"]["score"] for x in seeds]
    tm = lambda arm, k: mean([x[arm]["test"][k] for x in seeds])
    z3_ok = tm("Z3-ENUM", "valid") >= VALID_MIN and tm("Z3-ENUM", "coverage") >= COV_MIN
    d_z, z_pair = paired(sc("Z3-ENUM"), sc("G"))
    d_enum, enum_ok = paired(sc("Z3-ENUM"), sc("Z3-SAMP"))
    d_states, states_ok = paired(sc("Z3-SAMP"), sc("Z5-SAMP"))
    d_disc, disc_ok = paired(sc("Z3-SAMP"), sc("C3-SAMP"))
    z6_every = all(x["Z6-ENUM"]["test"]["valid"] >= VALID_MIN and x["Z6-ENUM"]["test"]["coverage"] >= COV_MIN
                   and x["Z6-ENUM"]["test"]["distinct_valid_min"] >= DISTINCT_MIN for x in seeds)
    d_z6, z6_pair = paired(sc("Z6-ENUM"), sc("G64"))
    mz1 = {a: [x[a]["mz1_fixed"]["score"] for x in seeds] for a in CLAIMED}
    mz1_ok = {a: max(v) <= M1_MAX for a, v in mz1.items()}
    pair_ok = lambda a, b: mz1_ok[a] and mz1_ok[b]
    mz6 = [x["Z6-ENUM"]["mz6_mod8"]["distinct_valid_min"] for x in seeds]
    mz6_max = [max(c["distinct_valid"] for c in x["Z6-ENUM"]["mz6_mod8"]["cues"]) for x in seeds]
    mz6_red = max(mz6_max) < DISTINCT_MIN
    mz2 = [x["MZ2"]["test"]["valid"] for x in seeds]
    mz2_red = max(mz2) <= MZ2_MAX
    m2t = [x["M2_true"]["score"] for x in seeds]
    m2c = [x["M2_coin"]["valid"] for x in seeds]
    m2_red = min(m2t) >= M2_TRUE_MIN and max(m2c) <= M2_COIN_MAX

    def line(ok, mutant=True, read=True):
        if not (m2_red and mutant):
            return "VOID"
        if not read:
            return "NOT_READ"
        return "PROVED" if ok else "DISPROVED"

    gate = z3_ok
    arms = [a for a in seeds[0] if a not in ("seed", "M2_true", "M2_coin")]
    report = {}
    for a in arms:
        cells = [x[a][star[a]] if a in star else x[a] for x in seeds]
        r = {k: mean([c["test"][k] for c in cells]) for k in ("valid", "coverage", "score", "distinct_valid_mean")}
        r["distinct_valid_min"] = min(c["test"]["distinct_valid_min"] for c in cells)
        if "win_fraction" in cells[0]:
            r["win_fraction"] = mean([c["win_fraction"] for c in cells])
            r["win_fraction_per_seed"] = [c["win_fraction"] for c in cells]
        report[a] = r
    return {
        "L-REP": line(gate), "L-Z": line(z3_ok and z_pair),
        "L-ENUM": line(enum_ok, mz2_red and pair_ok("Z3-ENUM", "Z3-SAMP"), gate),
        "L-STATES": line(states_ok, pair_ok("Z3-SAMP", "Z5-SAMP"), gate),
        "L-DISC": line(disc_ok, pair_ok("Z3-SAMP", "C3-SAMP"), gate), "L-Z6": line(z6_every and z6_pair, mz6_red),
        "sigma_star": star,
        "deltas": {"Z3-ENUM - G": d_z, "Z3-ENUM - Z3-SAMP": d_enum, "Z3-SAMP - Z5-SAMP": d_states,
                   "Z3-SAMP - C3-SAMP": d_disc, "Z6-ENUM - G64": d_z6},
        "z6_every_seed": z6_every,
        "mutants": {"Mz1": mz1, "Mz1_red": mz1_ok, "Mz6_distinct_valid_max": mz6_max, "Mz6_red": mz6_red, "Mz2_valid": mz2, "Mz2_red": mz2_red,
                    "M2_true": m2t, "M2_coin_valid": m2c, "M2_red": m2_red},
        "arms": report,
    }


def main(argv):
    if len(argv) < 2 or not os.path.exists(argv[1]):
        print("NOT DONE: no results file")
        return 2
    print(json.dumps(judge(json.load(open(argv[1]))), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
