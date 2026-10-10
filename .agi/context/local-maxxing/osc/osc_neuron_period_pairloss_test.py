"""Tests for osc_neuron_period_pairloss.py (hypothesis:lm-neuron-periodicity-single-failing-frequencies-are-redundant-carriers-on-loss
TESTS 1-6). CPU, seconds. Same pytest borrow as osc_neuron_period_freqabl_test.py."""
import json
import os
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_pairloss as Z  # noqa: E402
import osc_neuron_period_pc as S  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_neuron_period_pairloss_dir"), "params.json")))
p = P["p"]
Bm = Z.Q.basis(p)


def cyc(freqs, amp, y):   # logits whose row i is sum_f amp * cos(2 pi f (c - y_i) / p): the label is carried by every frequency in freqs
    c = np.arange(p)
    return torch.from_numpy(sum(amp * np.cos(2 * np.pi * f * (c[None, :] - y[:, None]) / p) for f in freqs))


def test_1_checkpoint_shas_are_pinned_and_match():
    assert sorted(P["checkpoints"]) == ["0", "1", "2"] and P["model_seeds"] == [0, 1, 2]
    for ck in P["checkpoints"].values():
        assert len(ck["sha256"]) == 64 and Z.F.sha(ck["path"]) == ck["sha256"]
    assert P["checkpoints"]["0"]["sha256"].startswith("8e174e98") and P["checkpoints"]["1"]["sha256"].startswith("7a2d0bdb")
    assert P["checkpoints"]["2"]["sha256"].startswith("51bf7db6")
    assert P["base_min_acc"] == 0.99 and P["recon_tol"] == 1e-9 and P["wall_cap_s"] == 1200 and P["threads"] == 1


def test_2_ablating_no_frequency_leaves_ce_and_accuracy_bit_identical():
    model, (X, y, tr, te) = S.make(P, 1).eval(), S.data(P)
    with torch.no_grad():
        L = model(X[te]).double()
    L0 = Z.Q.ablate(L, Bm, [])
    assert torch.equal(L0, L) and Z.ce(L0, y[te]) == Z.ce(L, y[te]) and Z.Q.acc(L0, y[te]) == Z.Q.acc(L, y[te])
    assert Z.dce(L, y[te], Bm, [], Z.ce(L, y[te])) == 0.0


def test_3_a_pure_frequency_7_plus_a_constant_has_dce_7_positive_and_dce_8_zero():
    y = torch.arange(0, p, 3)
    L = cyc([7], 3.0, y.numpy()) + 2.0
    c0 = Z.ce(L, y)
    assert Z.dce(L, y, Bm, [7], c0) > 0.1 and abs(Z.dce(L, y, Bm, [8], c0)) < 1e-12


def test_4_the_redundancy_detector_fires_on_a_known_redundant_pair():
    y = torch.arange(p)
    L = cyc([5, 9], 3000.0, y.numpy())   # the label sits in BOTH frequency 5 and frequency 9
    c0 = Z.ce(L, y)
    nk = [k for k in range(1, 57) if k not in (5, 9)]
    assert Z.dce(L, y, Bm, [5], c0) < 0.5 and Z.dce(L, y, Bm, [9], c0) < 0.5
    assert Z.dce(L, y, Bm, [5, 9], c0) - Z.dce(L, y, Bm, [9], c0) > 3.0
    row = Z.pair_table(L, y, Bm, 5, [5, 9], nk, c0)[9]
    assert row["beats"] and row["marginal"] > 3.0 and abs(row["null_max"]) < 1e-9 and row["gap"] > 3.0
    assert Z.cols([9, 9, 5]) == Z.cols([5, 9])   # a repeated frequency is merged, never projected twice


def test_5_t_is_computed_from_the_scores_not_typed():
    d1 = {1: 0.1, 2: 0.9, 3: 0.2, 4: 0.5}
    assert Z.target_set(d1, [1, 2, 3], [4, 3]) == [1, 3]
    assert Z.target_set(d1, [1, 2, 3], [4, 2]) == [1, 2, 3] and Z.target_set(d1, [1, 2, 3], [4, 3, 2]) == [1, 2, 3]   # a higher null max admits more targets
    assert Z.target_set({**d1, 1: 0.6}, [1, 2, 3], [4, 3]) == [3] and Z.target_set(d1, [1, 2, 3], [1]) == [1]
    assert Z.target_set(d1, [2], [4]) == []   # a family frequency that beats the null alone is not a target


def test_6_everything_is_imported_not_copied():
    src = open(Z.__file__).read()
    for imp in ("import osc_neuron_period_freqabl as Q",):
        assert imp in src, imp
    for name in ("dpeak", "detrended_null", "def train", "def sweep", "def stat", "def null", "def evaluate", "def data",
                 "def make", "class OneLayer", "def families", "def sha", "def basis", "def ablate", "def pair(", "def acc"):
        assert name not in src, name
    for fn in ("S.sweep", "S.stat", "S.null", "S.evaluate", "S.data", "S.make", "T.families", "F.sha", "F.rp", "Q.basis", "Q.ablate", "Q.pair"):
        assert fn in src, fn
