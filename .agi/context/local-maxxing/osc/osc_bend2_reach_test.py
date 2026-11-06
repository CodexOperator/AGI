"""Tests for osc_bend2_reach.py (goal:g5.51). Synthetic rows only: no test runs a round's code or reads the run's draws
(that is the run). The bend test needs the private install; it skips without it."""
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_bend2_reach as R  # noqa: E402

BEND = "/data/scratch/director-thought-1/bend/bin/bend"
needs_bend = pytest.mark.skipif(not os.path.exists(BEND), reason="no private bend install")
cue = lambda ab, score, valid=None: {"ab": ab, "score": score, "valid": sum(ab) / 64 if valid is None else valid, "coverage": 0.0}


def test_1_readings_follow_the_gates_text():
    as_req = {"true": [cue([32, 32], 1.0), cue([32, 32], 1.0)], "coin": [cue([0, 0], 0.0), cue([0, 0], 0.0)]}
    assert R.reached("g539_M2", as_req) is None
    assert R.reached("g539_M2", {**as_req, "true": [cue([32, 32], 1.0), cue([60, 0], 0.0)]}) == 0   # mean score 0.5 < 0.9
    assert R.reached("g539_M2", {**as_req, "coin": [cue([4, 4], 0.1), cue([4, 4], 0.1)]}) == 1      # valid 0.125 > 0.05
    assert R.reached("g546_MK", {"test": [cue([0, 0], 0.0)] * 2, "rich": [0, 17]}) == 1             # distinct 17 > 16
    assert R.reached("g546_MC", {"mc": [200, 149]}) == 0                                           # min 149 < 150


def test_2_the_first_reached_draw_in_seed_order_is_the_witness():
    rows = [{"seed": 1, "test": [cue([64, 0], 0.0)] * 2}, {"seed": 2, "test": [cue([30, 34], 0.99)] * 2},
            {"seed": 3, "test": [cue([32, 32], 1.0)] * 2}]
    i, r, k = R.first_witness("U_synth", rows)
    assert (i, r["seed"], k) == (1, 2, 0)
    assert R.first_witness("U_synth", rows[:1]) is None


def test_3_seeds_are_disjoint_from_every_rounds():
    for rnd in R.ROUNDS:
        p, _ = R.committed(rnd)
        assert not set(p["seeds"]) & set(range(R.SEED0, R.SEED0 + 100000))


def run(d):
    p = subprocess.run([BEND, "PROOF.bend", "--check-only"], cwd=d, env={**os.environ, "BEND_NO_TELEMETRY": "1"}, capture_output=True, text=True, timeout=120)
    out = p.stdout + p.stderr
    return "check" if "ALL PROOFS CHECK" in out else "fail" if "SOME PROOFS FAIL" in out and "{==}" in out else out


@needs_bend
@pytest.mark.parametrize("gid,row,k", [
    ("U_synth", {"test": [cue([30, 34], 0.99), cue([33, 31], 0.99)]}, 0),
    ("g539_M2", {"true": [cue([32, 32], 1.0), cue([60, 0], 0.0)], "coin": [cue([0, 0], 0.0)] * 2}, 0),
    ("g539_M2", {"true": [cue([32, 32], 1.0)] * 2, "coin": [cue([4, 4], 0.1), cue([4, 4], 0.1)]}, 1),
    ("g546_MK", {"test": [cue([0, 0], 0.0)] * 2, "rich": [0, 17]}, 1),
    ("g546_MC", {"mc": [200, 149]}, 0),
])
def test_4_a_reached_witness_checks_and_its_opposite_fails(tmp_path, gid, row, k):
    lit, wit, vac = R.wit_law(gid, row, k)
    for name, expr, want in (("wit", wit, "check"), ("vac", vac, "fail")):
        d = tmp_path / name
        R.L.write_dir(str(d), R.law_dir_files(lit, expr, name))
        assert run(str(d)) == want, (gid, name)


def test_5_score_reads_the_falsifier():
    P = {"N": {g: 10 for g in R.GATES}, "predicted": {**{g: "UNKNOWN" for g in R.GATES}, "U_synth": "WITNESSED",
                                                     "U_z3enum": "WITNESSED", **{v: "VACUOUS" for v in R.VACUOUS}}}
    fid = {g: {"exact": True} for g in R.GATES}
    ok = lambda s: {"status": s, "wall_s": 0.2, "peak_rss_mib": 80, "verdict": {"status": "check", "wall_s": 0.3}}
    sets, res = {}, {}
    for g in ("U_synth", "U_z3enum"):
        sets[f"{g}_wit"], res[f"{g}_wit"] = {"want": "check"}, ok("check")
        sets[f"{g}_vac_opp"], res[f"{g}_vac_opp"] = {"want": "fail"}, ok("fail")
    for v in R.VACUOUS:
        sets[f"{v}_vac_recheck"], res[f"{v}_vac_recheck"] = {"want": "check"}, ok("check")
        sets[f"{v}_vac_inserted"], res[f"{v}_vac_inserted"] = {"want": "fail"}, ok("fail")
    F = {"sets": sets, "witness": {g: ({"draw": 0, "seed": R.SEED0, "conjunct": 0} if g.startswith("U_") else None) for g in R.GATES}}
    V = R.score(P, fid, F, {"sets": res}, 60)
    assert V["void"] == [] and V["H_REACH"] == "proved" and V["predicted_right"] == V["n_calls"]
    F2 = {**F, "witness": {**F["witness"], "U_z3enum": None}}                    # a control never reached: UNKNOWNs VOID
    assert R.score(P, fid, F2, {"sets": res}, 60)["H_REACH"] == "void"
    F3 = {**F, "witness": {**F["witness"], "O_one_image": {"draw": 0, "seed": 1, "conjunct": 0}}}   # M-OVER witnessed
    assert R.score(P, fid, F3, {"sets": res}, 60)["H_REACH"] == "void"
    res2 = {**res, "g539_M1_vac_inserted": ok("check")}                          # a vacuity that holds an inserted witness
    assert R.score(P, fid, F, {"sets": res2}, 60)["H_REACH"] == "disproved"
    assert R.score(P, {**fid, "g546_MK": {"exact": False}}, F, {"sets": res}, 60)["H_REACH"] == "void"
