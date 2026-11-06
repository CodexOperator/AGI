"""goal:g5.49 falsifier, the council's text (goal:g5.49 ## Falsifier), committed BEFORE any run.

  python g549_falsifier.py RESULTS_JSON    exit 0 = done (verdict printed), 2 = not done

"templates" = distinct valid deduped templates (836-template set) among a cue's samples; per seed, MIN over the
2 cues; L-RICH-T reads valid, coverage and templates on the SAME 512 prior samples per cue.
  L-RICH-T  PROVED iff on EVERY seed, min over cues: CV valid >= 0.5, coverage >= 0.9, templates > 64.
  MS        speckle (leaf v2): templates <= 16 (max over cues) AND images >= 100 (min over cues) on every seed, else VOID.
  MC-T      512 true lines: templates >= 120 on every seed, min over cues, else VOID.
  MK        latent zeroed in training: test score <= 0.05 AND templates <= 16 (max over cues, of 512) on every
            seed, else a PROVED read is VOID; a RED stands.
  M2        the scorer as in g5.39, else VOID.
  VOID also if peak RSS > 3 GiB or a seed is reused from g5.43 / g5.46 (checked against their params.json).
REPORTED: Z6-ENUM templates; JV (Z3 code + CV latent) with remix's prediction: JV valid >= 0.87 AND JV
templates > CV's (both: mean over seeds of the min over cues, on the 512).
"""
import json
import os
import sys

VALID_MIN, COV_MIN, RICH_MIN = 0.5, 0.9, 64
MS_MAX, MS_IMAGES_MIN, MCT_MIN, MK_SCORE_MAX, MK_T_MAX = 16, 100, 120, 0.05, 16  # MS_MAX: leaf v2 (f12d7eef64)
M2_TRUE_MIN, M2_COIN_MAX, RSS_MAX_KIB, JV_VALID_PRED = 0.9, 0.05, 3 * 1024 * 1024, 0.87
_HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR = [os.path.join(_HERE, "../../../../datasets/plasma", d, "params.json")
         for d in ("2026-11-05-g5.43-code-inputs", "2026-11-05-g5.46-cvae")]


def mean(xs):
    return sum(xs) / len(xs)


def lo(cells, k):
    return min(c[k] for c in cells)


def judge(res, prior_seeds=None):
    seeds = res["seeds"]
    if prior_seeds is None:
        prior_seeds = set()
        for f in PRIOR:
            prior_seeds |= set(json.load(open(f))["seeds"])
    reused = sorted(set(x["seed"] for x in seeds) & set(prior_seeds))
    rss_ok = res.get("peak_rss_kib", 0) <= RSS_MAX_KIB
    cv = [x["CV2"]["rich"] for x in seeds]
    per_seed = [{"valid": lo(c, "valid"), "coverage": lo(c, "coverage"), "templates": lo(c, "templates"),
                 "images": lo(c, "images")} for c in cv]
    l_rich_t = all(s["valid"] >= VALID_MIN and s["coverage"] >= COV_MIN and s["templates"] > RICH_MIN for s in per_seed)
    ms = [(max(c["templates"] for c in x["MS"]), lo(x["MS"], "images")) for x in seeds]
    ms_ok = all(t <= MS_MAX and i >= MS_IMAGES_MIN for t, i in ms)
    mct = [lo(x["MC-T"], "templates") for x in seeds]
    mct_ok = min(mct) >= MCT_MIN
    mk = [(mean([c["score"] for c in x["MK"]["test"]]), max(c["templates"] for c in x["MK"]["rich"])) for x in seeds]
    mk_ok = all(s <= MK_SCORE_MAX and t <= MK_T_MAX for s, t in mk)
    m2t = [x["M2_true"]["score"] for x in seeds]
    m2c = [x["M2_coin"]["valid"] for x in seeds]
    m2_ok = min(m2t) >= M2_TRUE_MIN and max(m2c) <= M2_COIN_MAX
    if not (ms_ok and mct_ok and m2_ok and rss_ok and not reused):
        verdict = "VOID"
    elif not l_rich_t:
        verdict = "DISPROVED"
    else:
        verdict = "PROVED" if mk_ok else "VOID"
    rep = lambda arm, k: mean([lo(x[arm]["rich"], k) for x in seeds])
    jv_valid, jv_t, cv_t = rep("JV", "valid"), rep("JV", "templates"), rep("CV2", "templates")
    return {
        "L-RICH-T": verdict, "cv_per_seed": per_seed,
        "mutants": {"MS_templates_max_images_min": ms, "MS_ok": ms_ok, "MC-T_min": mct, "MC-T_ok": mct_ok,
                    "MK_score_templates": mk, "MK_ok": mk_ok, "M2_true": m2t, "M2_coin_valid": m2c, "M2_ok": m2_ok},
        "void_checks": {"peak_rss_kib": res.get("peak_rss_kib"), "rss_ok": rss_ok, "reused_seeds": reused},
        "reported": {a: {k: rep(a, k) for k in ("valid", "coverage", "templates", "images")}
                     for a in ("CV2", "Z6-ENUM", "JV", "MK")},
        "jv_prediction": {"jv_valid": jv_valid, "jv_templates": jv_t, "cv_templates": cv_t,
                          "came_true": jv_valid >= JV_VALID_PRED and jv_t > cv_t},
    }


def main(argv):
    if len(argv) < 2 or not os.path.exists(argv[1]):
        print("NOT DONE: no results file")
        return 2
    print(json.dumps(judge(json.load(open(argv[1]))), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
