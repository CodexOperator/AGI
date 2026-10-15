"""Tests for osc_neuron_period_freqabl.py (hypothesis:lm-neuron-periodicity-every-family-frequency-is-load-bearing-in-logit-space
TESTS 1-6). CPU, seconds. Same pytest borrow as osc_neuron_period_p4fair_test.py."""
import json
import os
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_freqabl as Q  # noqa: E402
import osc_neuron_period_pc as S  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_neuron_period_freqabl_dir"), "params.json")))
p = P["p"]
Bm = Q.basis(p)


def test_1_checkpoint_shas_are_pinned_and_match():
    assert sorted(P["checkpoints"]) == ["0", "1", "2"] and P["model_seeds"] == [0, 1, 2]
    for ck in P["checkpoints"].values():
        assert len(ck["sha256"]) == 64 and Q.F.sha(ck["path"]) == ck["sha256"]
    assert P["checkpoints"]["0"]["sha256"].startswith("8e174e98") and P["checkpoints"]["1"]["sha256"].startswith("7a2d0bdb")
    assert P["checkpoints"]["2"]["sha256"].startswith("51bf7db6")
    assert P["c2_min_fraction"] == 0.5 and P["recon_tol"] == 1e-9 and P["base_min_acc"] == 0.99 and P["wall_cap_s"] == 1200


def test_2_basis_is_orthonormal_and_the_constant_plus_56_pairs_reconstruct_any_vector():
    assert Bm.shape == (p, p) and float((Bm.T @ Bm - torch.eye(p, dtype=torch.float64)).abs().max()) < 1e-12
    v = torch.from_numpy(np.random.default_rng(0).normal(size=(5, p)))
    assert float(((v @ Bm) @ Bm.T - v).abs().max()) < 1e-9
    assert float(((v @ Bm[:, [0] + sum((Q.pair(k) for k in range(1, 57)), [])]) @ Bm[:, [0] + sum((Q.pair(k) for k in range(1, 57)), [])].T - v).abs().max()) < 1e-9


def test_3_ablating_no_frequency_is_bit_identical_to_the_unablated_accuracy():
    model, (X, y, tr, te) = S.make(P, 1).eval(), S.data(P)
    with torch.no_grad():
        L = model(X[te]).double()
    assert torch.equal(Q.ablate(L, Bm, []), L) and Q.acc(Q.ablate(L, Bm, []), y[te]) == Q.acc(L, y[te]) == S.evaluate(model, X[te], y[te])[1]


def test_4_a_pure_frequency_7_logit_is_zeroed_by_ablating_7_and_untouched_by_ablating_8():
    c = np.arange(p)
    L = torch.from_numpy(np.stack([np.cos(2 * np.pi * 7 * c / p + ph) for ph in (0.0, 0.7, 2.1)]))
    assert float(Q.ablate(L, Bm, Q.pair(7)).abs().max()) < 1e-12
    assert float((Q.ablate(L, Bm, Q.pair(8)) - L).abs().max()) < 1e-12


def test_5_the_c2_fraction_is_1_for_a_synthetic_d_in_b_k_and_about_2_over_113_for_white_noise():
    g = np.random.default_rng(1)
    D = torch.from_numpy(g.normal(size=(300, 2))) @ Bm[:, Q.pair(19)].T + 3.0   # inside B_19 (+ a constant the centring removes)
    fr = Q.energy(D, Bm, p)
    assert fr[18] == pytest.approx(1.0, abs=1e-9) and int(fr.argmax()) == 18 and fr.sum() == pytest.approx(1.0, abs=1e-9)
    fr = Q.energy(torch.from_numpy(g.normal(size=(20000, p))), Bm, p)
    assert fr.mean() == pytest.approx(2 / 113, abs=0.001) and fr.max() < 0.03 and fr.sum() == pytest.approx(1.0, abs=1e-9)   # fractions of the CENTRED energy: 2/112 each, ~2/113


def test_6_everything_is_imported_not_copied():
    src = open(Q.__file__).read()
    for imp in ("import osc_neuron_period_p4fair as F", "import osc_neuron_period_pc as S", "import osc_neuron_period_seeds as T"):
        assert imp in src, imp
    for name in ("dpeak", "detrended_null", "def train", "def sweep", "def stat", "def null", "def evaluate", "def data",
                 "def make", "class OneLayer", "def families", "def sha", "def n_sets", "def u_sets"):
        assert name not in src, name
    for fn in ("S.sweep", "S.stat", "S.null", "S.evaluate", "S.data", "S.make", "T.families", "F.sha", "F.rp"):
        assert fn in src, fn
