"""Tests for osc_bend2_graph.py (goal:g5.45). Synthetic lines and values only: no test reads census.json's committed
counts or runs the round's law files (that is the run). The bend tests need the private install; they skip without it."""
import json
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_bend2_graph as G  # noqa: E402

BEND = "/data/scratch/director-thought-1/bend/bin/bend"
needs_bend = pytest.mark.skipif(not os.path.exists(BEND), reason="no private bend install")
V = lambda n: ("var", n)
LINE = {"id": "syn_l1", "goal": "goal:synthetic", "line": 1, "cite": "PROVED iff N_f <= 64 AND N_r >= 2 x N_f",
        "proved": ("and", ("le", V("syn_nf"), 64), ("ge", V("syn_nr"), ("mul", 2, V("syn_nf")))), "void": ("ge", V("syn_m"), 50)}


def test_1_the_dsl_evaluates_and_prints_the_same_tree():
    env = {"syn_nf": 16, "syn_nr": 32, "syn_m": 1}
    assert G.verdict_one(LINE, env) == "proved"
    assert G.verdict_one(LINE, {**env, "syn_nr": 31}) == "disproved"
    assert G.verdict_one(LINE, {**env, "syn_m": 50}) == "void"   # the void gate is read first
    assert G.verdict_bend(LINE) == "G.code(U32.is_ge(V.syn_m(), 50), (U32.is_le(V.syn_nf(), 64) && U32.is_ge(V.syn_nr(), (2 * V.syn_nf() : U32))))"
    with pytest.raises(AssertionError):
        G.bend(-1)   # a negative literal cannot be a U32 count


def test_2_read_takes_committed_integers_only():
    src = {"a": {"x": 44, "f": 0.22, "nul": None, "l": [3, 5]}, "seeds": [{"n": 128, "inv": 120}, {"n": 128, "inv": 126}]}
    assert G.read(src, "int", ["a.x"]) == 44 and G.read(src, "notnull", ["a.nul"]) == 0 and G.read(src, "int_or0", ["a.nul"]) == 0
    assert G.read(src, "len", ["a.l"]) == 2 and G.read(src, "sum", ["seeds.0.n", "seeds.1.n"]) == 256
    assert G.read(src, "sum_diff", ["seeds.0.n", "seeds.1.n", "seeds.0.inv", "seeds.1.inv"]) == 10
    with pytest.raises(AssertionError):
        G.read(src, "int", ["a.f"])   # a float is never read as a count


def run(d):
    p = subprocess.run([BEND, "PROOF.bend", "--check-only"], cwd=d, env={**os.environ, "BEND_NO_TELEMETRY": "1"}, capture_output=True, text=True, timeout=120)
    return p.stdout + p.stderr


@needs_bend
@pytest.mark.parametrize("env,claim,want", [
    ({"syn_nf": 16, "syn_nr": 32, "syn_m": 1}, "proved", "ALL PROOFS CHECK"),
    ({"syn_nf": 16, "syn_nr": 32, "syn_m": 1}, "disproved", "SOME PROOFS FAIL"),
    ({"syn_nf": 16, "syn_nr": 31, "syn_m": 1}, "disproved", "ALL PROOFS CHECK"),
    ({"syn_nf": 16, "syn_nr": 31, "syn_m": 1}, "proved", "SOME PROOFS FAIL"),
    ({"syn_nf": 16, "syn_nr": 32, "syn_m": 50}, "void", "ALL PROOFS CHECK"),
    ({"syn_nf": 16, "syn_nr": 32, "syn_m": 50}, "proved", "SOME PROOFS FAIL"),
])
def test_3_the_kernel_reads_the_numbers_like_python(tmp_path, env, claim, want):
    assert (G.verdict_one(LINE, env) == claim) == (want == "ALL PROOFS CHECK")
    G.L.write_dir(str(tmp_path), G.files_for([LINE], env, {"syn_l1": claim}))
    assert want in run(str(tmp_path))


FREE = {"id": "syn_l2", "goal": "goal:synthetic", "line": 2, "cite": "PROVED iff valid >= 0.5 AND delta > 0 (float)",
        "proved": ("and", ("ge", ("mul", 2, V("syn_valid")), V("syn_total")), ("free", "r_delta"))}


def test_4_a_free_clause_is_quantified_and_decides_only_when_invariant():
    assert G.frees(FREE) == ["r_delta"]
    assert G.verdicts_all(FREE, {"syn_valid": 10, "syn_total": 640}) == {"disproved"}   # integer clause fails: RED whatever r is
    assert G.verdicts_all(FREE, {"syn_valid": 400, "syn_total": 640}) == {"proved", "disproved"}   # not integer-exact here
    assert G.binom_band(200, 0.2, 0.05) == 50   # g5.35's band from its prereg parameters
    assert G.dig({"GC": {"4.0": {"n": 7}}}, "GC.4\\.0.n") == 7


@needs_bend
@pytest.mark.parametrize("vals,claim,want", [({"syn_valid": 10, "syn_total": 640}, "disproved", "ALL PROOFS CHECK"),
                                             ({"syn_valid": 10, "syn_total": 640}, "proved", "SOME PROOFS FAIL"),
                                             ({"syn_valid": 400, "syn_total": 640}, "proved", "SOME PROOFS FAIL"),
                                             ({"syn_valid": 400, "syn_total": 640}, "disproved", "SOME PROOFS FAIL")])
def test_5_the_kernel_proves_a_verdict_for_every_value_of_the_free_clause(tmp_path, vals, claim, want):
    G.L.write_dir(str(tmp_path), G.files_for([FREE], vals, {"syn_l2": claim}))
    assert want in run(str(tmp_path))


def test_6_law_sets_build_counter_proofs_mb_and_mc():
    lines = [{**LINE, "integer_exact": True, "committed": "disproved"},
             {"id": "g535_l2", "goal": "goal:g5.35", "line": "2", "cite": "x", "integer_exact": True, "committed": "proved",
              "proved": ("ge", V("g535_salt_hits"), V("g535_band")), "void": ("lt", V("g535_salt_hits"), V("g535_band"))},
             {"id": "g535_l1", "goal": "goal:g5.35", "line": "1", "cite": "y", "integer_exact": False},
             {"id": "g541_l1", "goal": "goal:g5.41", "line": "1", "cite": "z", "integer_exact": False},
             {"id": "g541_l2", "goal": "goal:g5.41", "line": "2", "cite": "w", "integer_exact": False}]
    vals = {"syn_nf": 16, "syn_nr": 31, "syn_m": 1, "g535_null_hits": 44, "g535_salt_hits": 200, "g535_band": 50,
            "g541_blend0": 41, "g541_invalid0": 504, "g541_s_valid": 10, "g541_s_total": 640}
    C = {"lines": lines, "mc": {"fallback": G.mc_pick(lines)["id"]}}
    assert C["mc"]["fallback"] == "g535_l2"   # LINE has 3 comparisons; g535_l2 is the first single-comparison line
    s = G.law_sets(C, vals)
    assert {"C_syn_l1", "C_syn_l1_not_proved", "C_syn_l1_not_void", "C_g535_l2_not_disproved", "MC_g535_l2", "MC_g535_l2_unflipped"} <= set(s)
    mb = {k: v for k, v in s.items() if k.startswith("MB_")}
    assert {k: [x for x in v[2].items() if vals.get(x[0]) != x[1]] for k, v in mb.items()} == {
        "MB_b_g535_f1_null": [("g535_null_hits", 50)], "MB_b_g535_f2_salt": [("g535_salt_hits", 49)],
        "MB_b_g541_smech": [("g541_blend0", 252)], "MB_b_g541_sout": [("g541_s_valid", 320)]}   # the leaf's four mutants
    assert all(v[4] == "fail" for v in mb.values()) and s["MC_g535_l2"][2]["g535_band"] == 201 and s["MC_g535_l2"][3] == {"g535_l2_mc": "void"}
    assert s["B_proved_pair_g535_r2"][4] == "check" and len(s["B_proved_pair_g535_r2"][1]) == len(s["B_disproved_pair_g541"][1]) == 2


def test_7_g5_42_module_imported_not_copied():
    src = open(G.__file__).read()
    assert "import osc_bend2_law as L" in src
    for name in ("def run_bend", "def tree_rss", "def law_file", "def proof_file", "def write_dir", "def hit(", "def logits("):
        assert name not in src, name
