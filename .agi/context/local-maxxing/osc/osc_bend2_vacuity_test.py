"""Tests for osc_bend2_vacuity.py (goal:g5.50). Synthetic lines and a shrunk n only: no test reads o_table.json or runs
the round's law files (that is the run). The bend tests need the private install; they skip without it."""
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_bend2_vacuity as A  # noqa: E402

BEND = "/data/scratch/director-thought-1/bend/bin/bend"
needs_bend = pytest.mark.skipif(not os.path.exists(BEND), reason="no private bend install")


def test_1_the_rule_reads_m_from_the_code():
    d1 = "noise = rng.normal(0.0, sigma, size=(1 if frozen else n, h.shape[1]))"
    assert A.m_draws(d1, "sample_p(net, c, sg, n_s, r, frozen=True)") == 1 and A.m_draws(d1, "sample_p(net, c, sg, n_s, r)") == "n"
    assert A.m_draws("m = 1 if fixed else n", "x(fixed=True)") == 1
    assert A.m_draws("code = code_table(dim)[ci % mod if mod else ci]", "sample_code(net, c, n_s, arm, r, mod=8)") == 8
    assert A.m_draws("a = (h > 0).astype(np.float64)", "sample_s(net, c, n_s, None, frozen=True)") == 1
    assert A.m_draws("z = rng.normal(0.0, 1.0, size=(n, d))", "sample_cv(net, c, k, r)") == "n"
    assert A.m_draws("lines, _ = G.make_lines(r, n_s, 8)", "same") == "n"
    with pytest.raises(AssertionError):
        A.m_draws("a = (h > 0).astype(np.float64)", "sample_s(net, c, n_s, r)")   # R3 without a frozen call
    with pytest.raises(AssertionError):
        A.m_draws("x = rng.choice(pool)", "f()")                                  # no rule: VOID


def test_2_the_class_needs_a_deterministic_decoder():
    lines = {"draw": "m = 1 if fixed else n", "call": "f(fixed=True)", "dec": "return ((a @ w2 + b2) > 0).astype(np.float64)"}
    assert A.o_class(lines) == ("one_class", 1)
    assert A.o_class({**lines, "dec": "return (rng.random(size=s) < sigmoid(a @ w2)).astype(float)"})[0] == "all"
    assert A.o_class({**lines, "call": "f()"})[0] == "all"
    assert A.kind_of("dist_le", "cap8", 64) == "dist8" and A.kind_of("dist_le", "all", 512) == "dist512"


def test_3_the_integer_bounds_hold_on_every_histogram():
    for o in A.space("all"):
        s = A.true_score(o)
        assert float(A.lo(o)) <= s + 1e-12 and s <= float(A.hi(o)) + 1e-12, o
    assert all(A.hi(o) == 0 for o in A.space("one_class"))


def test_4_reference_calls():
    one = {"id": "x", "conj": [("score_le", "one_class", 1, 20)]}
    allg = {"id": "y", "conj": [("score_le", "all", 1, 20)]}
    assert A.gate_ref(one)["call"] == "vacuous"
    r = A.gate_ref(allg)
    assert r["call"] == "non_vacuous" and A.lo(tuple(r["witness"][1][0])) > A.Fr(1, 20)
    assert A.gate_ref({"id": "t", "conj": [("valid_ge", "all", 0, 1)]})["call"] == "vacuous"
    assert A.gate_ref({"id": "d", "conj": [("dist_le", "dist8", 15)]})["call"] == "vacuous"
    assert A.gate_ref({"id": "e", "conj": [("dist_ge", "dist512", 150)]})["witness"] == (0, 0)


def run(d):
    p = subprocess.run([BEND, "PROOF.bend", "--check-only"], cwd=d, env={**os.environ, "BEND_NO_TELEMETRY": "1"}, capture_output=True, text=True, timeout=300)
    out = p.stdout + p.stderr
    return "check" if "ALL PROOFS CHECK" in out else "fail" if "SOME PROOFS FAIL" in out and "{==}" in out else out


@needs_bend
def test_5_the_kernel_reads_every_form_as_wanted(tmp_path, monkeypatch):
    """n shrunk to 8: one vacuous and one non-vacuous gate of each reading, every form, as law_sets wants it."""
    monkeypatch.setattr(A, "N", 8)
    gs = [{"id": f"{r}_{k}", "conj": [(r, k, *th)]} for r, th in (("score_le", (1, 20)), ("score_ge", (9, 10)), ("valid_le", (1, 10)))
          for k in ("one_class", "all")] + [{"id": "P_taut", "conj": [("valid_ge", "all", 0, 1)]},
                                            {"id": "dle", "conj": [("dist_le", "dist8", 15)]}, {"id": "dge", "conj": [("dist_ge", "dist8", 5)]},
                                            {"id": "and", "conj": [("score_le", "one_class", 1, 20), ("dist_le", "dist8", 4)]}]
    got = {}
    for name, (g, form, wit, want, _) in A.law_sets(gs).items():
        d = tmp_path / name
        A.L.write_dir(str(d), A.law_files(g, form, wit))
        got[name] = (run(str(d)), want)
    assert all(g == w for g, w in got.values()), {k: v for k, v in got.items() if v[0] != v[1]}


def test_6_score_reads_the_falsifier():
    gs = [{"id": "g1", "review": "vacuous", "conj": [("score_le", "one_class", 1, 20)]},
          {"id": "g2", "review": "non_vacuous", "conj": [("score_le", "all", 1, 20)]},
          {"id": "P_taut", "conj": [("valid_ge", "all", 0, 1)]}, {"id": "P_strong", "conj": [("score_le", "all", 1, 20)]}]
    S = A.law_sets(gs)
    F = {"sets": {k: {"gate": v[0]["id"], "form": v[1], "want": v[3]} for k, v in S.items()},
         "python_ref": {g["id"]: {**A.gate_ref(g), "review": g.get("review")} for g in gs}}
    ok = lambda s: {"status": s, "wall_s": 0.2, "peak_rss_mib": 80}
    C = {"sets": {k: {**ok(v[3]), **({"verdict": ok("check")} if v[3] == "check" else {})} for k, v in S.items()}}
    V = A.score(F, C, 60)
    assert V["void"] == [] and V["line1"] == "proved" and V["line2_counterproofs"] == "proved"
    C["sets"]["g2_vac_opp"]["status"] = "check"                 # the for-all accepted on a non-vacuous gate
    assert A.score(F, C, 60)["line1"] == "disproved"
    C["sets"]["g2_vac_opp"]["status"] = "fail"
    C["sets"]["P_taut_vac"]["status"] = "fail"                  # the planted tautology not certified -> VOID
    assert A.score(F, C, 60)["line1"] == "void"
