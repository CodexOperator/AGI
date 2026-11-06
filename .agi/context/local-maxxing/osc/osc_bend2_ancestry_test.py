"""Tests for osc_bend2_ancestry.py (goal:g5.47). A synthetic commit graph only: no test reads records.json or runs the
round's law files (that is the run). The bend tests need the private install; they skip without it."""
import os
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_bend2_ancestry as A  # noqa: E402

BEND = "/data/scratch/director-thought-1/bend/bin/bend"
needs_bend = pytest.mark.skipif(not os.path.exists(BEND), reason="no private bend install")
h = lambda n: f"{n:040x}"
#      g (root)
#     / \
#    a   b      m = merge(c, b); x = child of m; y = side branch off a, never merged
#    |   |
#    c   |
#     \ /
#      m -> x
PAR = {h(1): [], h(2): [h(1)], h(3): [h(1)], h(4): [h(2)], h(5): [h(4), h(3)], h(6): [h(5)], h(7): [h(2)]}
G, AA, B, C, M, X, Y = (h(i) for i in range(1, 8))


def test_1_levels_are_generation_numbers():
    lev = A.levels(PAR)
    assert lev == {G: 1, AA: 2, B: 2, C: 3, M: 4, X: 5, Y: 3}
    assert all(lev[p] < lev[c] for c, ps in PAR.items() for p in ps)   # strictly falling along every edge


def test_2_prover_paths_and_closures_agree():
    lev = A.levels(PAR)
    assert A.shortest_path(PAR, lev, X, B) == [X, M, B]   # the merge's second parent
    assert A.shortest_path(PAR, lev, X, Y) is None
    R = A.closure(PAR, lev, X, Y)
    assert R[0] == X and set(R) == {X, M, C} and Y not in R   # level >= 3 only: a and b sit below the cutoff
    assert B in A.closure(PAR, lev, X, B)
    off = A.offered_path(PAR, lev, X, Y)
    assert off[0] == X and off[-1] == Y and Y not in PAR[off[-2]]


def test_3_words_is_the_sha_in_five_u32():
    assert A.words("00000001" * 5) == "[1, 1, 1, 1, 1]" and A.words("ffffffff" + "0" * 32) == "[4294967295, 0, 0, 0, 0]"
    with pytest.raises(AssertionError):
        A.words("abc")


def synthetic_R():
    lev = A.levels(PAR)
    pairs = []
    for key, x, y in (("anc", X, B), ("non", X, Y)):
        anc = A.shortest_path(PAR, lev, x, y) is not None
        pairs.append({"key": key, "x": x, "y": y, "git_ancestor": anc, "level_y": lev[y], "R": A.closure(PAR, lev, x, y),
                      "path": A.shortest_path(PAR, lev, x, y), "offered_path": None if anc else A.offered_path(PAR, lev, x, y)})
    return {"pairs": pairs, "records": {c: {"level": lev[c], "parents": [[p, lev[p]] for p in PAR[c]]} for c in PAR}}


def test_4_law_sets_cover_every_role():
    S = A.law_sets(synthetic_R())
    roles = sorted((k, v[3], v[2]) for k, v in S.items())
    assert ("anc_proof", "honest", "check") in roles and ("non_disproof", "honest", "check") in roles
    assert {r for _, r, _ in roles} == {"honest", "opposite", "Me1a", "Me1b", "Me2", "Me3", "Me4", "reported"}
    assert all(w == "fail" for _, r, w in roles if r.startswith("Me") or r == "opposite")


def run(d):
    p = subprocess.run([BEND, "PROOF.bend", "--check-only"], cwd=d, env={**os.environ, "BEND_NO_TELEMETRY": "1"}, capture_output=True, text=True, timeout=120)
    return "check" if "ALL PROOFS CHECK" in p.stdout + p.stderr else "fail" if "SOME PROOFS FAIL" in p.stdout + p.stderr else p.stdout + p.stderr


@needs_bend
def test_5_the_kernel_reads_every_synthetic_set_as_wanted(tmp_path):
    """Honest sets check; every opposite and mutant FAILS; P_omit (a parent dropped from a record) CHECKS: the kernel
    certifies the logic over the records, never their provenance -- stated, not hidden."""
    got = {}
    for name, (kind, lit, want, role, _) in A.law_sets(synthetic_R()).items():
        d = tmp_path / name
        A.L.write_dir(str(d), A.law_files(kind, lit))
        got[name] = (run(str(d)), want)
    assert all(g == w for g, w in got.values() if w != "reported"), got
    assert got["anc_P_omit"][0] == "check"


@needs_bend
def test_6_a_dropped_closure_member_is_refused(tmp_path):
    """Me4 at depth: drop an INTERIOR member (c) of an honest non-ancestor closure, its edge from m still listed."""
    lev = A.levels(PAR)
    recs = [(c, lev[c], [(p, lev[p]) for p in PAR[c]]) for c in A.closure(PAR, lev, X, Y) if c != C]
    A.L.write_dir(str(tmp_path), A.law_files("disproof", A.lit_disproof(X, Y, lev[Y], recs)))
    assert run(str(tmp_path)) == "fail"


def test_7_score_reads_the_falsifier():
    R = synthetic_R()
    S = A.law_sets(R)
    F = {"sets": {k: {"kind": v[0], "want": v[2], "role": v[3], "pair": v[4], "literal_bytes": len(v[1])} for k, v in S.items()}}
    ok = lambda st: {"status": st, "wall_s": 0.2, "peak_rss_mib": 80}
    C = {"sets": {k: {**ok("check" if v[2] in ("check", "reported") else "fail"), **({"verdict": ok("check")} if v[3] == "honest" else {})} for k, v in S.items()}}
    V = A.score(F, C, R, 60)
    assert V["void"] == [] and V["line1"] == "proved" and all(v["agrees"] for v in V["kernel_vs_git"].values())
    C["sets"]["anc_disproof_opp"]["status"] = "check"   # an accepted opposite: unsound -> RED
    assert A.score(F, C, R, 60)["line1"] == "disproved"
    C["sets"]["anc_disproof_opp"]["status"] = "fail"
    C["sets"]["non_Me3"]["status"] = "check"            # a mutant that passes -> VOID
    assert A.score(F, C, R, 60)["line1"] == "void"
    C["sets"]["non_Me3"]["status"] = "fail"
    C["sets"]["anc_proof"]["wall_s"] = 61.0             # over the cap -> VOID
    assert A.score(F, C, R, 60)["void"]
