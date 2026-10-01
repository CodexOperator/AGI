"""Tests for osc_neuron_period_p4fair.py (hypothesis:lm-neuron-periodicity-fair-p4-every-seed-has-a-load-bearing-family TESTS 1-6).
CPU, seconds. Same pytest borrow as osc_neuron_period_seeds_test.py."""
import json
import os
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_p4fair as F  # noqa: E402
import osc_neuron_period_pc as S  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_neuron_period_p4fair_dir"), "params.json")))
n = P["model"]["d_mlp"]


def test_1_checkpoint_shas_are_pinned_and_match():
    assert sorted(P["checkpoints"]) == ["0", "1", "2"] and P["model_seeds"] == [0, 1, 2]
    for ck in P["checkpoints"].values():
        assert len(ck["sha256"]) == 64 and F.sha(ck["path"]) == ck["sha256"]
    assert P["checkpoints"]["0"]["sha256"].startswith("8e174e98") and P["checkpoints"]["1"]["sha256"].startswith("7a2d0bdb")
    assert P["checkpoints"]["2"]["sha256"].startswith("51bf7db6")
    assert P["n_sets"] == 200 and P["percentile"] == 0.99 and P["norm_window"] == 0.02 and P["max_draws"] == 20000


@pytest.mark.parametrize("m", [20, 51, 176])
def test_2_u_sets_are_size_matched_and_seed_deterministic(m):
    mk = lambda: F.u_sets(n, m, np.random.default_rng([P["u_seed"], 1, 5]), 200)
    a, b = mk(), mk()
    assert a == b and len(a) == 200
    assert all(len(s) == m == len(set(s)) and max(s) < n for s in a) and len({tuple(s) for s in a}) > 190


def test_3_n_sets_sit_inside_the_window_and_an_impossible_window_is_untestable():
    cn = np.random.default_rng(0).uniform(1.0, 2.0, n)
    ok = F.n_sets(cn, 40, float(cn.mean()), np.random.default_rng(1), 200, P["norm_window"], P["max_draws"])
    assert len(ok) == 200 and all(abs(cn[s].mean() - cn.mean()) <= P["norm_window"] and len(s) == 40 for s in ok)
    assert F.n_sets(cn, 40, 5.0, np.random.default_rng(1), 200, P["norm_window"], 500) == []   # nothing near 5.0
    assert F.judge(0.9, [0.1] * 200, [], 0.99, 200) == {"load_bearing": False, "n_untestable": True}


def test_4_ablating_zero_neurons_leaves_accuracy_bit_identical():
    model, (X, y, tr, te) = S.make(P, 1).eval(), S.data(P)
    S.evaluate(model, X, y)
    means, mask = model.seen.mean(0), torch.isin(torch.arange(n), torch.tensor([], dtype=int))
    assert S.evaluate(model, X[te], y[te], (mask, means)) == S.evaluate(model, X[te], y[te])


def test_5_percentile_rule_on_a_synthetic_null():
    null = list(np.linspace(0.0, 0.2, 200))
    assert F.judge(0.3, null, null, 0.99, 200)["load_bearing"]                      # above all 200
    assert not F.judge(0.1, null, null, 0.99, 200)["load_bearing"]                  # median
    assert not F.judge(0.3, null, [0.5] * 200, 0.99, 200)["load_bearing"]           # beats U, not N: the AND
    assert not F.judge(0.3, [0.5] * 200, null, 0.99, 200)["load_bearing"]
    assert F.pct(0.3, null) == 100.0 and F.pct(-1.0, null) == 0.0 and F.pct(0.1, null) == pytest.approx(50.0, abs=1)


def test_6_everything_is_imported_not_copied():
    src = open(F.__file__).read()
    assert "import osc_neuron_period_pc as S" in src and "import osc_neuron_period_seeds as T" in src
    for name in ("dpeak", "detrended_null", "def train", "def sweep", "def stat", "def null", "def evaluate", "def data",
                 "def make", "class OneLayer", "def families", "rfft"):
        assert name not in src, name
    for fn in ("S.sweep", "S.stat", "S.null", "S.evaluate", "S.data", "S.make", "T.families"):
        assert fn in src, fn
