"""goal:g5.37 falsifier, pre-registered BEFORE the first run.

  python g537_falsifier.py RESULTS_JSON     exit 0 = done (verdict printed), 2 = no results yet

Acc on the SHIFTED test, mean over the 5 seeds; band(cell) = max - min over seeds; two cells are
compared against the wider of their two bands.
  sigma* = the nonzero sigma with the best mean P acc; tau* = the best mean T acc.
  RED 1  unless P(sigma*) beats BOTH P(0) and T(tau*) by more than the band.
  RED 2  if P0(sigma*) (trained with sigma*, run at 0) keeps the gain: P(sigma*) - P0(sigma*) <= band
         -> the noise was a training regularizer, not dynamics at the core.
  MUTANT arm B with its filters rotated by one class must fall to <= 0.35 on EVERY seed
         (chance 0.25); if not, the task does not need orientation and the round is VOID.
verdict: VOID if the mutant fails, else DISPROVED if RED 1 or RED 2, else CONFIRMED.
"""
import json
import os
import sys

MUTANT_MAX = 0.35


def cell(seeds, arm, key=None):
    accs = [(s[arm][key] if key is not None else s[arm])["acc"] for s in seeds]
    return {"mean": sum(accs) / len(accs), "band": max(accs) - min(accs), "accs": accs}


def judge(res):
    seeds = res["seeds"]
    sig = [str(s) for s in res["params"]["sigmas"] if float(s) > 0]
    taus = [str(t) for t in res["params"]["taus"]]
    P = {s: cell(seeds, "P", s) for s in [str(res["params"]["sigmas"][0])] + sig}
    P0 = {s: cell(seeds, "P0", s) for s in sig}
    T = {t: cell(seeds, "T", t) for t in taus}
    p_zero = P[str(res["params"]["sigmas"][0])]
    s_star = max(sig, key=lambda s: P[s]["mean"])
    t_star = max(taus, key=lambda t: T[t]["mean"])
    ps, ts = P[s_star], T[t_star]
    gain_p0 = ps["mean"] - p_zero["mean"]
    band_p0 = max(ps["band"], p_zero["band"])
    gain_t = ps["mean"] - ts["mean"]
    band_t = max(ps["band"], ts["band"])
    red1 = not (gain_p0 > band_p0 and gain_t > band_t)
    drop = ps["mean"] - P0[s_star]["mean"]
    band_drop = max(ps["band"], P0[s_star]["band"])
    red2 = drop <= band_drop
    b, brot = cell(seeds, "B"), cell(seeds, "B_rot")
    mutant_red = max(brot["accs"]) <= MUTANT_MAX
    verdict = "VOID" if not mutant_red else ("DISPROVED" if (red1 or red2) else "CONFIRMED")
    return {
        "verdict": verdict, "sigma_star": s_star, "tau_star": t_star,
        "red1": red1, "gain_vs_P0": gain_p0, "band_vs_P0": band_p0,
        "gain_vs_T": gain_t, "band_vs_T": band_t,
        "red2": red2, "P_minus_P0_at_sigma_star": drop, "band_P_P0": band_drop,
        "mutant_red": mutant_red, "B": b, "B_rot": brot,
        "P": P, "P0": P0, "T": T,
    }


def main(argv):
    if len(argv) < 2 or not os.path.exists(argv[1]):
        print("NOT DONE: no results file")
        return 2
    print(json.dumps(judge(json.load(open(argv[1]))), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
