"""Fixtures for the TOTAL band call rule (hypothesis:a00-cc7b25cc-82fe33).
No model, no GPU: hand-written records, hand-computed words."""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m = _load("osc_band_call2_a00-cc7b25cc")
old = _load("osc_band_call_a00-ee9a5cdc")


def rec(arm, seed, agree, kl, np=32, budget=5.25, model="qwen2"):
    return {"model": model, "np": np, "budget": budget, "arm": arm,
            "seed": seed, "agree": agree, "kl": kl}


# cell A: stochastic arm really varies -> the band is earnable
CELL_A = [rec("random", 1, .50, .10), rec("random", 2, .53, .11),
          rec("random", 3, .56, .12), rec("uniform", 0, .54, .105),
          rec("key_only", 0, .60, .09)]
# cell B: P3 -- three ROWS, one DISTINCT seed
CELL_B = [rec("random", 7, .50, .10), rec("random", 7, .50, .10),
          rec("random", 7, .50, .10), rec("key_only", 0, .90, .05)]
# cell C: P4 -- three DISTINCT seeds, but the arm never varied
CELL_C = [rec("random", 1, .50, .10), rec("random", 2, .50, .10),
          rec("random", 3, .50, .10), rec("key_only", 0, .90, .05)]
# cell D: too few random draws at all
CELL_D = [rec("random", 1, .50, .10), rec("random", 2, .53, .11),
          rec("key_only", 0, .60, .09)]


def test_p3_one_seed_repeated_three_times_is_unresolved():
    j = m.judge(CELL_B)
    assert {v[0] for v in j.values()} == {"unresolved"}
    assert all("distinct" in v[1] for v in j.values()), j
    assert old.judge(CELL_B)["qwen2", 32, 5.25, "key_only", "agree"] == "win"  # the old hole


def test_p4_degenerate_band_is_unresolved_not_a_win():
    j = m.judge(CELL_C)
    assert {v[0] for v in j.values()} == {"unresolved"}
    assert all("degenerate" in v[1] for v in j.values()), j


def test_p4_zero_band_on_one_metric_only():
    # agree varies, kl does not: one word, one refusal, in the SAME cell
    mixed = [rec("random", 1, .50, .10), rec("random", 2, .53, .10),
             rec("random", 3, .56, .10), rec("key_only", 0, .60, .05)]
    j = m.judge(mixed)
    assert j["qwen2", 32, 5.25, "key_only", "random", "agree"] == ("win", "margin %+.4g vs band %+.4g" % (.07, .06000000000000005))
    assert j["qwen2", 32, 5.25, "key_only", "random", "kl"][0] == "unresolved"
    assert "degenerate" in j["qwen2", 32, 5.25, "key_only", "random", "kl"][1]


def test_p7_absent_seed_is_not_a_distinct_draw():
    # the 16 on-disk rows carry NO seed field (osc_band_matched_uniform_a00-a721f95f.py:74-77):
    # three rows that vary must NOT become three distinct seeds
    nos = [{k: v for k, v in d.items() if k != "seed"} for d in
           [rec("random", 1, .50, .10), rec("random", 2, .53, .11),
            rec("random", 3, .56, .12), rec("key_only", 0, .90, .05)]]
    j = m.judge(nos)
    assert {v[0] for v in j.values()} == {"unresolved"}, j
    assert all("no seed" in v[1] for v in j.values()), j
    assert old.judge(nos)["qwen2", 32, 5.25, "key_only", "agree"] == "win"  # the old hole


def test_p8_the_superseded_module_is_marked_deprecated():
    assert (HERE / "osc_band_call_a00-ee9a5cdc.py").read_text().startswith('"""DEPRECATED')


def test_too_few_random_draws_is_unresolved():
    j = m.judge(CELL_D)
    assert {v[0] for v in j.values()} == {"unresolved"}


def test_p6_both_comparators_appear_in_one_return():
    a = m.judge(CELL_A, comparator="random")
    b = m.judge(CELL_A, comparator="uniform")
    assert ("random" in {k[4] for k in a}) and ("uniform" in {k[4] for k in b})
    # key_only vs uniform: agree margin +.06 == band .06 -> inside-noise;
    # kl sign-corrected margin +.015 < band .02 -> inside-noise
    assert b["qwen2", 32, 5.25, "key_only", "uniform", "agree"][0] == "inside-noise"
    assert b["qwen2", 32, 5.25, "key_only", "uniform", "kl"][0] == "inside-noise"
    # the band is the stochastic arm's either way: the reason string is the same
    assert a["qwen2", 32, 5.25, "key_only", "random", "agree"][1].split(" vs ")[1] == \
        b["qwen2", 32, 5.25, "key_only", "uniform", "agree"][1].split(" vs ")[1]


def test_no_regression_against_the_old_module_on_an_earned_cell():
    for arm, comp in (("key_only", "random"),):
        new = m.judge(CELL_A, arm, comp)
        oldc = old.judge(CELL_A, arm)
        for k, v in new.items():
            assert v[0] == oldc[k[:3] + (k[3], k[5])], (k, v, oldc[k[:3] + (k[3], k[5])])


def test_kl_sign_still_inverts():
    hi = [rec("random", 1, .50, .10), rec("random", 2, .53, .11), rec("random", 3, .56, .12),
          rec("key_only", 0, .60, .30)]
    j = m.judge(hi)
    assert j["qwen2", 32, 5.25, "key_only", "random", "kl"][0] == "loss"
    assert j["qwen2", 32, 5.25, "key_only", "random", "agree"][0] == "win"


def test_module_stays_model_free():
    src = (HERE / "osc_band_call2_a00-cc7b25cc.py").read_text()
    assert "torch" not in src and "transformers" not in src
    assert src.count("import ") == 1
