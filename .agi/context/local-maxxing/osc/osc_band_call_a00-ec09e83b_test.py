#!/usr/bin/env python3
"""No-model acceptance for the two calls: distinct seeds, refusal, the hand table, the contract."""
import importlib.util, json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]  # paths.py sits beside osc/: __file__, never cwd

S = importlib.util.spec_from_file_location("call", os.path.join(HERE, "osc_band_call_a00-ec09e83b.py"))
C = importlib.util.module_from_spec(S); S.loader.exec_module(C)


def _rows(bud, seeds, arm="random", stochastic=True):
    return [{"cell": "x", "budget": bud, "arm": arm, "seed": s, "n": len(seeds), "arm_is_stochastic": stochastic,
             "widths": [4], "agree": 0.5 + 0.01 * i, "kl": 1.0 - 0.01 * i} for i, s in enumerate(seeds)]


def test_falsifier_1_duplicates_are_not_replication():
    """3 DISTINCT seeds -> n=3; the same row written 3x -> n=1."""
    g = C.groups(_rows("5.25", [7, 21, 99]))
    assert C.n_distinct(g[("5.25", "random")]) == 3
    dup = C.groups(_rows("5.25", [7, 7, 7]))
    assert C.n_distinct(dup[("5.25", "random")]) == 1


def test_falsifier_2_a_stochastic_group_under_three_seeds_is_refused():
    g = C.groups(_rows("5.25", [7, 7, 7]) + _rows("5.25", [0], "uniform", False) + _rows("5.25", [0], "key_only", False))
    for call in (lambda x: C.call(x, "margin"), lambda x: C.call(x, "range")):
        try:
            call(g)
        except ValueError as e:
            assert "refuse to call" in str(e)
        else:
            raise AssertionError("falsifier 2: a 1-seed stochastic group returned a call")


def test_the_two_calls_are_never_merged_and_never_agree_everywhere():
    g = C.groups(C.merged())
    m, r = C.call(g, "margin"), C.call(g, "range")
    assert m.keys() == r.keys() and len(m) == 8
    assert all(m[k]["call"] == "margin" and r[k]["call"] == "range" for k in m)
    assert {k[0] for k, v in m.items() if v["verdict"] == "inside-noise"} == {"5.25", "7.25"}
    assert [k for k, v in r.items() if v["verdict"] == "inside-noise"] == [("5.25", "kl")]
    assert [k for k in m if (m[k]["verdict"] == "inside-noise") != (r[k]["verdict"] == "inside-noise")]


def test_reader_equals_the_hand_table_cell_for_cell():
    """The parent's arithmetic, written out longhand over the same twelve rows."""
    g = C.groups(C.merged())
    m, r = C.call(g, "margin"), C.call(g, "range")
    hand_margin = {("4.25", "agree"): (-0.07959, 0.020508), ("4.25", "kl"): (-0.470127, 0.179178),
                   ("5.25", "agree"): (0.027832, 0.04248), ("5.25", "kl"): (0.125137, 0.2494),
                   ("6.25", "agree"): (0.051758, 0.029175), ("6.25", "kl"): (0.154396, 0.149022),
                   ("7.25", "agree"): (0.009033, 0.019043), ("7.25", "kl"): (0.01424, 0.06055)}
    for k, (marg, half) in hand_margin.items():
        assert (m[k]["margin"], m[k]["half_range"]) == (marg, half), k
    assert abs(m[("6.25", "kl")]["margin"] - m[("6.25", "kl")]["half_range"] - 0.005374) < 5e-7  # the near case
    assert r[("7.25", "agree")]["key_only"] == 0.883300781 > r[("7.25", "agree")]["max"]  # falsifier 5


def test_falsifier_3_the_emitted_file_carries_the_deterministic_arms_as_rows(tmp_path=None):
    """Writes into a throwaway dir: run() used to rewrite the TRACKED dataset under the repo."""
    with tempfile.TemporaryDirectory() as td:
        C.run(out=tmp_path or td)
        rs = [json.loads(l) for l in open(os.path.join(tmp_path or td, "cells.jsonl"))]
    assert sum(1 for x in rs if x["arm"] == "uniform") == 4
    assert sum(1 for x in rs if x["arm"] == "key_only") == 4
    assert all(x["seed"] == 0 and x["n"] == 1 and x["arm_is_stochastic"] is False
               for x in rs if x["arm"] in ("uniform", "key_only"))
    assert len({x["seed"] for x in rs if x["arm"] == "random"}) == 3


def test_the_declared_adopted_margin_is_the_full_min_max_not_the_half_range():
    """PASS 8 item 3: the config cell p3 cites declares MARGIN against the FULL min-max
    (osc_band_call2 band() = max-min). The reader now emits that call by name, so the reader and
    the cell judge by ONE denominator, and the two 6.25 cells the half-range calls 'win' are
    inside-noise under the adopted rule."""
    g = C.groups(C.merged())
    m, mf = C.call(g, "margin"), C.call(g, "margin_full")
    assert m[("6.25", "agree")]["verdict"] == "win" and mf[("6.25", "agree")]["verdict"] == "inside-noise"
    assert m[("6.25", "kl")]["verdict"] == "win" and mf[("6.25", "kl")]["verdict"] == "inside-noise"
    assert {k[0] for k, v in mf.items() if v["verdict"] == "inside-noise"} == {"5.25", "6.25", "7.25"}
    for k, v in mf.items():
        assert v["call"] == "margin_full" and abs(v["band"] - 2 * v["half_range"]) < 2e-6  # both fields are rounded to 6dp


def test_each_call_refuses_only_the_arms_its_own_branch_reads():
    """PASS 8 item 4: the RANGE branch never reads uniform, so a random+key_only group is a
    computable call, not a refusal; the MARGIN branch does read it, so it is refused."""
    g = C.groups(_rows("5.25", [7, 21, 99]) + _rows("5.25", [0], "key_only", False))
    assert C.call(g, "range")[("5.25", "agree")]["call"] == "range"
    for kind in ("margin", "margin_full"):
        try:
            C.call(g, kind)
        except ValueError as e:
            assert "refuse to call" in str(e) and "uniform" in str(e)
        else:
            raise AssertionError("a margin call with no uniform arm returned a call")


def test_falsifier_4_an_unnamed_kind_is_refused_not_answered_with_the_range_call():
    """The old `if kind == "margin": ... else:` made every typo a RANGE call. Now it raises."""
    g = C.groups(C.merged())
    for kind in ("typo", "INSIDE?", "", None, "MARGIN", "margin "):
        try:
            C.call(g, kind)
        except ValueError as e:
            assert "refuse to call" in str(e) and repr(kind) in str(e), kind
        else:
            raise AssertionError("falsifier 4: kind %r silently returned a call" % (kind,))
    assert C.call(g, "range")[("5.25", "kl")]["call"] == "range"


def test_falsifier_6_a_budget_with_no_random_group_is_refused_not_empty():
    """uniform+key_only only: the old reader returned {} -- downstream, 'nothing to decide'."""
    g = C.groups(_rows("4.25", [0], "uniform", False) + _rows("4.25", [0], "key_only", False))
    for kind in C.KINDS:
        try:
            C.call(g, kind)
        except ValueError as e:
            assert "refuse to call" in str(e) and "4.25" in str(e) and "random" in str(e)
        else:
            raise AssertionError("falsifier 6: a control-less budget returned a call")
    # and a budget that DOES carry its random arm is still called -- the hand table is unmoved
    m = C.call(C.groups(C.merged()), "margin")
    assert {k for k, v in m.items() if v["verdict"] == "inside-noise"} == {("5.25", "agree"), ("5.25", "kl"),
                                                                          ("7.25", "agree"), ("7.25", "kl")}


def test_the_row_contract_is_a_config_cell_cited_not_a_script_literal():
    c = C.contract()
    assert set(c["fields"]) <= set(C.merged()[0])
    assert "DISTINCT seeds" in c["text"] and "MARGIN" in c["text"] and "RANGE" in c["text"]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn(None); print("ok", name)
