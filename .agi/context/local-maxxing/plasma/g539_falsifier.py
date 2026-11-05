"""goal:g5.39 falsifier, the council's pre-registration (goal:g5.39 ## Falsifier), committed BEFORE any run.

  python g539_falsifier.py RESULTS_JSON     exit 0 = done (verdict printed), 2 = no results yet

score = valid fraction x coverage, mean over the 2 cues, 64 samples per cue.
sigma* / tau* = the best MEAN VALIDATION score over the 5 seeds (a held-out stream, never the test stream).
  PROVED iff (1) the PAIRED per-seed TEST delta P(sigma*) - T(tau*) is > 0 on all 5 seeds (sign test,
             p = 1/32) AND its mean is > 0.05, AND (2) P(sigma*)'s TEST valid fraction is >= 0.5
             (mean over seeds and cues). RED (DISPROVED) if (1) or (2) fails.
  M1     P(sigma*) with ONE noise draw frozen per seed and cue scores <= 0.05 on EVERY seed.
  M2     on EVERY seed: 64 true target lines per cue (32 per class) score >= 0.9, and 64
         Bernoulli(0.5) images have valid fraction <= 0.05.
  Each mutant must read RED, else the round is VOID.
  MF (P's weights at the hidden layer's Gaussian expectation) is REPORTED ONLY; "RED if MF matches P"
  was withdrawn before mint (plasma CORRECTION 1, 11:07Z 11-05).
verdict: VOID if a mutant fails, else PROVED or DISPROVED.
"""
import json
import os
import sys

DELTA_MIN, VALID_MIN, M1_MAX, M2_TRUE_MIN, M2_COIN_MAX = 0.05, 0.5, 0.05, 0.9, 0.05


def mean(xs):
    return sum(xs) / len(xs)


def judge(res):
    seeds = res["seeds"]
    sig = [str(s) for s in res["params"]["sigmas"]]
    taus = [str(t) for t in res["params"]["taus"]]
    s_star = max(sig, key=lambda s: mean([x["P"][s]["val"]["score"] for x in seeds]))
    t_star = max(taus, key=lambda t: mean([x["T"][t]["val"]["score"] for x in seeds]))
    p_test = [x["P"][s_star]["test"]["score"] for x in seeds]
    t_test = [x["T"][t_star]["test"]["score"] for x in seeds]
    deltas = [a - b for a, b in zip(p_test, t_test)]
    p_valid = mean([x["P"][s_star]["test"]["valid"] for x in seeds])
    c1 = all(dl > 0 for dl in deltas) and mean(deltas) > DELTA_MIN
    c2 = p_valid >= VALID_MIN
    m1 = [x["M1"][s_star]["score"] for x in seeds]
    m2_true = [x["M2_true"]["score"] for x in seeds]
    m2_coin = [x["M2_coin"]["valid"] for x in seeds]
    m1_red = max(m1) <= M1_MAX
    m2_red = min(m2_true) >= M2_TRUE_MIN and max(m2_coin) <= M2_COIN_MAX
    verdict = "VOID" if not (m1_red and m2_red) else ("PROVED" if (c1 and c2) else "DISPROVED")
    return {
        "verdict": verdict, "sigma_star": s_star, "tau_star": t_star,
        "c1_paired": c1, "deltas": deltas, "delta_mean": mean(deltas),
        "c2_valid": c2, "P_valid_test": p_valid,
        "P_test": p_test, "T_test": t_test,
        "m1_red": m1_red, "M1": m1, "m2_red": m2_red, "M2_true": m2_true, "M2_coin_valid": m2_coin,
        "val": {"P": {s: mean([x["P"][s]["val"]["score"] for x in seeds]) for s in sig},
                "T": {t: mean([x["T"][t]["val"]["score"] for x in seeds]) for t in taus}},
        "test": {"P": {s: {k: mean([x["P"][s]["test"][k] for x in seeds]) for k in ("valid", "coverage", "score")}
                       for s in sig},
                 "T": {t: {k: mean([x["T"][t]["test"][k] for x in seeds]) for k in ("valid", "coverage", "score")}
                       for t in taus}},
        "MF_reported": {s: {k: mean([x["MF"][s][k] for x in seeds]) for k in ("valid", "coverage", "score")}
                        for s in sig},
    }


def main(argv):
    if len(argv) < 2 or not os.path.exists(argv[1]):
        print("NOT DONE: no results file")
        return 2
    print(json.dumps(judge(json.load(open(argv[1]))), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
