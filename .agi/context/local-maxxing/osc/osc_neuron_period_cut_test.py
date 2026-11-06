"""Tests for osc_neuron_period_cut.py (goal:g5.36). CPU, seconds; never reads the trained checkpoint beyond its sha256
(the solve is checked on synthetic data and on an UNTRAINED net, so no test peeks at the measured numbers)."""
import json
import os
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_cut as Z  # noqa: E402
import osc_neuron_period_pc as S  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_neuron_period_cut_dir"), "params.json")))


def test_1_params_are_pinned():
    ck = P["checkpoint"]
    assert Z.F.sha(ck["path"]) == ck["sha256"] and ck["sha256"].startswith("8e174e98") and ck["train_seed"] == 0
    assert P["n_grid"] == [8, 16, 24, 32, 48, 64] and P["n_grid_random_extra"] == [96, 128]
    assert P["random_seeds"] == [0, 1, 2, 3, 4] and P["twin_seed"] == 1001 and P["split_seed"] == 0
    assert P["acc_threshold"] == 0.99 and P["mutant_max_acc"] == 0.5 and P["threads"] == 1 and P["wall_cap_s"] == 1200


def test_2_freq_pick_is_round_robin_by_peakiness_and_skips_a_spent_family():
    pk = np.array([0.1, 0.9, 0.5, 0.8, 0.7, 0.2, 0.6])
    fams = {5: [0, 1, 2], 1: [3, 4], 45: [5, 6]}   # family order = size order, as T.families returns it
    assert Z.freq_pick(pk, fams, 3) == [1, 3, 6]
    assert Z.freq_pick(pk, fams, 6) == [1, 3, 6, 2, 4, 5]
    assert Z.freq_pick(pk, fams, 99) == [1, 3, 6, 2, 4, 5, 0]   # 5's last neuron once 1 and 45 are spent
    assert fams == {5: [0, 1, 2], 1: [3, 4], 45: [5, 6]}   # the input is not consumed


def test_3_random_picks_are_nested_seeded_and_replayable():
    for s in P["random_seeds"]:
        a, b = Z.rand_pick(512, s, 8), Z.rand_pick(512, s, 128)
        assert a == b[:8] and len(set(b)) == 128 and a == [int(i) for i in np.random.default_rng(s).permutation(512)[:8]]
    assert Z.rand_pick(512, 0, 64) != Z.rand_pick(512, 1, 64)


def test_4_the_solve_recovers_an_exact_readout_in_the_residual_stream():
    g = torch.Generator().manual_seed(0)
    h = torch.relu(torch.randn(400, 20, generator=g, dtype=torch.float64))
    U = torch.randn(113, 128, generator=g, dtype=torch.float64)
    Wt, bt, rest = torch.zeros(20, 128, dtype=torch.float64), torch.randn(128, generator=g, dtype=torch.float64), torch.randn(400, 113, generator=g, dtype=torch.float64)
    keep = [2, 5, 11, 17]
    Wt[keep] = torch.randn(4, 128, generator=g, dtype=torch.float64)   # only the kept neurons carry signal
    target = rest + (h @ Wt + bt) @ U.T
    W, uerr = Z.solve(h, rest, target, keep, U)
    pred = rest + (h[:, keep] @ W[:-1] + W[-1]) @ U.T
    assert W.shape == (5, 128) and uerr < 1e-9 and float((pred - target).abs().max()) < 1e-8
    W2, _ = Z.solve(h, rest, target, [0, 1], U)   # the wrong neurons cannot fit it
    assert float((rest + (h[:, [0, 1]] @ W2[:-1] + W2[-1]) @ U.T - target).abs().max()) > 1.0


def test_5_install_rewrites_w_out_and_all_512_reproduce_an_untrained_net():
    model, (X, y, tr, te) = S.make(P, 7).eval(), S.data(P)
    with torch.no_grad():
        target = model(X[tr]).double()
    r, m = Z.arm(model, list(range(512)), X, y, tr, te, target)
    with torch.no_grad():
        d = float((m(X[te]).double() - model(X[te]).double()).abs().max())
    assert d < 1e-3 and r["u_err"] < 1e-6 and abs(r["test_acc"] - S.evaluate(model, X[te], y[te])[1]) <= P["self_tol"]
    r8, m8 = Z.arm(model, [3, 1, 4, 159, 26, 5, 35, 89], X, y, tr, te, target)
    nz = torch.nonzero(m8.w_out.weight.abs().sum(0))[:, 0].tolist()
    h, _ = Z.feats(model, X[tr])
    dead = [i for i in [3, 1, 4, 159, 26, 5, 35, 89] if float(h[:, i].abs().max()) == 0.0]   # min-norm lstsq gives a dead neuron 0
    live = torch.nonzero(m8.w_out.weight.abs().sum(0) > 1e-6)[:, 0].tolist()
    assert set(nz) <= {3, 1, 4, 159, 26, 5, 35, 89} and sorted(live) == sorted({3, 1, 4, 159, 26, 5, 35, 89} - set(dead)) and len(live) >= 4
    assert r8["n"] == 8
    assert torch.equal(model.w_out.weight, S.make(P, 7).w_out.weight)   # the original is never edited


def test_6_verdict_reads_proved_red_and_the_mutant_gate():
    acc = lambda hits: {n: (0.995 if n >= hits else 0.5) for n in P["n_grid"] + P["n_grid_random_extra"]}
    never = {n: 0.3 for n in P["n_grid"] + P["n_grid_random_extra"]}
    rand = lambda *hs: {s: (acc(h) if h else never) for s, h in enumerate(hs)}
    V = Z.verdict(acc(16), rand(None, 64, 32, None, 96), 0.05, P)
    assert V["proved"] and V["N_f"] == 16 and V["N_r"] == 32 and V["mutant_red"]   # N_r = 2 x N_f is enough
    V = Z.verdict(acc(16), rand(None, 24, None, None, None), 0.05, P)
    assert not V["proved"] and V["N_r"] == 24   # RED: one random seed reaches 0.99 below 2 x N_f
    V = Z.verdict(acc(96), rand(None, None, None, None, None), 0.05, P)
    assert not V["proved"] and V["N_f"] is None   # RED: N_f > 64 (96 is not on the scored grid)
    V = Z.verdict(acc(64), rand(None, None, None, None, None), 0.05, P)
    assert V["proved"] and V["N_r"] is None
    V = Z.verdict(acc(64), rand(None, None, None, None, 128), 0.05, P)
    assert V["proved"] and V["N_r"] == 128
    assert not Z.verdict(acc(8), rand(None), 0.5, P)["mutant_red"]   # the mutant at 0.5 is not RED -> main voids


def test_7_everything_is_imported_not_copied():
    src = open(Z.__file__).read()
    for imp in ("import osc_neuron_period_pc as S", "import osc_neuron_period_seeds as T", "import osc_neuron_period_p4fair as F"):
        assert imp in src, imp
    for name in ("dpeak", "detrended_null", "def train", "def sweep", "def stat", "def null", "def evaluate", "def data",
                 "def make", "class OneLayer", "def families", "def sha", "optim"):
        assert name not in src, name
    for fn in ("S.sweep", "S.stat", "S.null", "S.evaluate", "S.data", "S.make", "T.families", "F.sha", "F.rp"):
        assert fn in src, fn
    assert ".step()" not in src and "backward" not in src   # 0 gradient steps
