"""Tests for osc_neuron_period_phase.py (goal:g5.38). CPU, seconds; synthetic data and UNTRAINED nets only: no test reads a
trained checkpoint beyond its sha256, so none peeks at the measured numbers."""
import json
import os
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_phase as Q  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_neuron_period_phase_dir"), "params.json")))
p = P["p"]


def test_1_params_and_checkpoints_are_pinned():
    for ck in P["checkpoints"].values():
        assert Q.F.sha(ck["path"]) == ck["sha256"]
    assert P["checkpoints"]["pc"]["sha256"].startswith("8e174e98") and P["checkpoints"]["s3"]["sha256"].startswith("04f96cc8")
    assert P["n_grid"] == [8, 16, 24, 32] and P["n_grid_random_extra"] == [48, 64] and P["write_m"] == [2, 4, 6, 8]
    assert P["random_seeds"] == [0, 1, 2, 3, 4] and P["twin_seed"] == 1001 and P["threads"] == 1
    assert (P["m2_max_acc"], P["m3_max_acc"], P["m4_keep_frac"], P["acc_threshold"]) == (0.5, 0.5, 0.99, 0.99)


def test_2_phases_recover_a_planted_neuron():
    a, b = np.meshgrid(np.arange(p), np.arange(p), indexing="ij")
    for k, ph, ps in [(5, 0.7, -2.1), (34, -1.3, 2.9)]:
        A = np.maximum(0, np.cos(2 * np.pi * k * a / p + ph) + np.cos(2 * np.pi * k * b / p + ps))
        fa, fb = Q.phases(A, k)
        assert abs(np.angle(np.exp(1j * (fa - ph)))) < 1e-6 and abs(np.angle(np.exp(1j * (fb - ps)))) < 1e-6


def test_3_resultant_and_quotas():
    assert Q.R([0.3] * 5) == pytest.approx(1.0) and Q.R(list(2 * np.pi * np.arange(4) / 4)) < 1e-12 and Q.R([]) == 0.0
    c = {5: 151, 1: 133, 45: 128, 34: 84}
    for n in (8, 16, 24, 32):
        q = Q.quotas(c, n)
        assert sum(q.values()) == n and list(q) == [5, 1, 45, 34]
    assert Q.quotas(c, 8) == {5: 3, 1: 2, 45: 2, 34: 1}   # 2.44 2.15 2.06 1.35 -> floors 2 2 2 1, the one seat to 5 (0.44)
    assert Q.quotas({1: 1, 2: 1}, 1) == {1: 1, 2: 0}   # a tie goes to family order


def test_4_joint_greedy_spreads_and_the_m1_twin_collapses():
    rng = np.random.default_rng(0)
    ph = {i: (float(t), float(s)) for i, (t, s) in enumerate(rng.uniform(-np.pi, np.pi, (40, 2)))}
    ph.update({100 + i: (0.5, 0.5) for i in range(10)})   # ten exact phase twins
    cands = list(ph)
    j = Q.greedy_family(cands, ph, 8, Q.joint)
    t = Q.greedy_family(cands, ph, 8, Q.twin_sum)
    Pj, Pt = [ph[i] for i in j], [ph[i] for i in t]
    assert Q.joint(Pj) < 0.2 and Q.R([a + b for a, b in Pt]) > 0.99 and len(set(j)) == 8
    assert j[0] == 0   # all tie at R = 1 on the first pick -> smallest index
    assert Q.greedy_family(cands, ph, 8, Q.joint) == j   # deterministic


def test_5_omp_finds_a_planted_support_and_skips_dead_columns():
    g = torch.Generator().manual_seed(0)
    h = torch.relu(torch.randn(500, 60, generator=g, dtype=torch.float64))
    h[:, 7] = 0.0
    h[:, 9] = h[:, 3]   # a duplicate column
    W = torch.zeros(60, 113, dtype=torch.float64)
    W[[3, 11, 42]] = torch.randn(3, 113, generator=g, dtype=torch.float64) * 5
    y = h @ W + 1.0
    o = Q.omp(h, y, 5)
    assert sorted(o[:3]) == [3, 11, 42] and 7 not in o and 9 not in o and len(set(o)) == 5


def test_6_torus_and_the_equal_phase_mutant():
    pts = Q.torus(8)
    assert len(pts) == 8 and len({(round(a, 9), round(b, 9)) for a, b in pts}) == 8
    assert Q.R([a + b for a, b in pts]) < 0.5 and Q.R([a - b for a, b in pts]) < 0.5
    assert Q.torus(8, equal=True) == [(0.0, 0.0)] * 8
    assert [Q.lattice_g(m) for m in (2, 4, 6, 8)] == [1, 3, 5, 5]   # council pin 11:14Z
    assert [round(b / (2 * np.pi) * 8) for _, b in pts] == [(5 * j) % 8 for j in range(8)]


def test_7_write_and_resid_in_on_an_untrained_net():
    S = Q.S
    model, (X, y, tr, te) = S.make(P, 7).eval(), S.data(P)
    r = Q.resid_in(model, X[tr[:50]])
    assert r.shape == (50, P["model"]["d_model"]) and r.dtype == torch.float64
    mw, ids, r2 = Q.write(model, X, tr, [5, 1], 2, p)
    assert ids == [0, 1, 2, 3] and len(r2) == 4 and all(-1e-9 <= v <= 1 + 1e-9 for v in r2)
    assert not torch.equal(mw.w_in.weight[:4], model.w_in.weight[:4]) and torch.equal(mw.w_in.weight[4:], model.w_in.weight[4:])
    assert torch.equal(model.w_in.weight, S.make(P, 7).w_in.weight)   # the original is never edited


def test_8_verdicts_read_each_claim_and_each_mutant_gate():
    g = P["n_grid"] + P["n_grid_random_extra"]
    step = lambda hit: {n: (0.995 if hit is not None and n >= hit else 0.4) for n in g}
    base = lambda **kw: {"rand": {s: step(None) for s in range(5)}, "joint": step(16), "m1": step(None), "omp": step(32),
                         "write": step(None), "m2_max": 0.05, "m3": 0.1, "m4_max_frac": 0.3, **kw}
    V = Q.verdicts(base(), P)
    assert (V["H1"], V["H2"], V["H3"], V["N_b"], V["N_r"]) == ("proved", "not_red", "disproved", 16, None)
    V = Q.verdicts(base(rand={0: step(24), **{s: step(None) for s in range(1, 5)}}), P)
    assert V["H1"] == "disproved" and V["N_r"] == 24   # one random seed below 2 x N_b
    assert Q.verdicts(base(rand={0: step(32), **{s: step(None) for s in range(1, 5)}}), P)["H1"] == "proved"   # = 2 x N_b
    assert Q.verdicts(base(m1=step(32)), P)["H1"] == "void"
    assert Q.verdicts(base(m4_max_frac=0.995), P)["H1"] == "void"
    V = Q.verdicts(base(m2_max=0.5), P)
    assert V["H1"] == "void" and V["H2"] == "void" and V["H3"] == "disproved"
    assert Q.verdicts(base(omp=step(8)), P)["H2"] == "red"
    assert Q.verdicts(base(joint=step(None), omp=step(32)), P)["H2"] == "red"   # N_b > 32
    assert Q.verdicts(base(joint=step(None), omp=step(None)), P)["H2"] == "no_verdict"   # council pin (3)
    assert Q.verdicts(base(m3=0.9), P)["H1"] == "proved"   # M3 gates H3 only
    V = Q.verdicts(base(write=step(24)), P)
    assert V["H3"] == "proved" and V["N_w_hits"] == [24]   # OMP < 0.99 at 24
    assert Q.verdicts(base(write=step(32)), P)["H3"] == "disproved"   # OMP also reaches 0.99 at 32
    assert Q.verdicts(base(write=step(24), m3=0.5), P)["H3"] == "void"


def test_9_g5_36_modules_are_imported_not_copied():
    src = open(Q.__file__).read()
    assert "import osc_neuron_period_cut as Z" in src
    for name in ("def feats", "def solve", "def install", "def arm(", "def rand_pick", "def sweep", "def stat", "def families",
                 "class OneLayer", "def make", "def data", "def evaluate", "backward", ".step()", "optim"):
        assert name not in src, name
    for fn in ("Z.feats", "Z.arm", "Z.rand_pick", "S.sweep", "S.stat", "S.null", "T.families", "F.sha"):
        assert fn in src, fn
