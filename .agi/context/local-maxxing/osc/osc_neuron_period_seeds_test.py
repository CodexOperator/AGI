"""Tests for osc_neuron_period_seeds.py (hypothesis:lm-neuron-periodicity-control-replicates-across-training-seeds
TESTS 1-5). CPU, a few seconds. The torch venv has no pytest; borrow one:
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):<a site dir with pytest>" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_neuron_period_seeds_test.py -q --basetemp /tmp/<dir>
"""
import json
import os
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_pc as S  # noqa: E402
import osc_neuron_period_seeds as T  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_neuron_period_seeds_dir"), "params.json")))
PC = json.load(open(os.path.join(paths.get_local("osc_neuron_period_pc_dir"), "params.json")))
n = P["model"]["d_mlp"]


def test_1_params_differ_from_the_pc_only_in_the_declared_keys():
    diff = {k for k in set(P) | set(PC) if P.get(k) != PC.get(k)}
    declared = {"hypothesis", "run", "train_seed", "train_seeds", "fallback_seed", "fallback", "wall_cap_s",
                "wall_cap_note", "threads", "threads_note", "box_min_avail_mib", "box_min_avail_note", "random_seeds", "family_floor", "p3_def", "p4_def", "verdict_rule", "unscored", "resume"}
    assert diff <= declared, sorted(diff - declared)
    assert P["train_seeds"] == [1, 2, 3] and P["fallback_seed"] is None and P["twin_seed"] == PC["twin_seed"]
    for k in ("p", "model", "optimizer", "split_seed", "train_fraction", "step_cap", "grok_threshold", "grok_hold_steps",
              "b_set", "null_seed", "null_quantile", "p1_min_fraction", "p2_max_freqs", "p2_cover"):
        assert P[k] == PC[k], k
    assert len(P["random_seeds"]) == 20 and P["family_floor"] == 20 and P["wall_cap_s"] * 3 <= 8100 and P["threads"] == 1 and P["box_min_avail_mib"] == 4000


@pytest.mark.parametrize("size", [20, 33, 80])
def test_2_random_sets_are_size_matched_disjoint_and_seed_deterministic(size):
    fam = sorted(np.random.default_rng(9).choice(n, size, replace=False).tolist())
    a, b = T.random_sets(n, fam, P["random_seeds"]), T.random_sets(n, fam, P["random_seeds"])
    assert a == b and list(a) == P["random_seeds"]
    assert all(len(v) == size == len(set(v)) and not set(v) & set(fam) and max(v) < n for v in a.values())
    assert len({tuple(v) for v in a.values()}) == len(a)   # the 20 sets differ


def test_3_ablating_zero_neurons_is_bit_identical_through_the_imported_evaluate():
    model, (X, y, tr, te) = S.make(P, 1).eval(), S.data(P)
    S.evaluate(model, X, y)
    means = model.seen.mean(0)
    mask = torch.isin(torch.arange(n), torch.tensor([], dtype=int))
    assert S.evaluate(model, X[te], y[te], (mask, means)) == S.evaluate(model, X[te], y[te])


def test_4_a_family_below_the_floor_is_skipped_and_the_tally_is_recorded():
    kb = np.array([5] * 25 + [7] * 19 + [3] * 2 + [9] * 6)
    pk = np.ones(len(kb))
    p1, ks, cnt, fams = T.families(pk, kb, 0.5, 0.5, P["family_floor"])
    assert list(fams) == [5] and len(fams[5]) == 25 and len(p1) == 52
    assert list(ks) == [5, 7, 9, 3] and list(cnt) == [25, 19, 6, 2]   # count desc
    kb2 = np.array([4] * 20 + [2] * 20)   # a tie -> smallest k first; both at the floor
    _, ks2, _, fams2 = T.families(np.ones(40), kb2, 0.5, 0.5, 20)
    assert list(ks2) == [2, 4] and sorted(fams2) == [2, 4]
    assert not T.families(np.ones(10), np.zeros(10, dtype=int), 0.5, 0.5, 20)[3]   # none at the floor -> P4 cannot pass


def test_5_everything_is_imported_not_copied():
    src = open(T.__file__).read()
    assert "import osc_neuron_period_pc as S" in src
    for name in ("dpeak", "detrended_null", "def train", "def sweep", "def stat", "def null", "def evaluate", "def data",
                 "def make", "class OneLayer", "def peakiness", "def detrend"):
        assert name not in src, name
    for fn in ("S.train", "S.sweep", "S.stat", "S.null", "S.evaluate", "S.data", "S.make"):
        assert fn in src, fn


def test_verdict_order_void_before_disproved_before_proved():
    ok = lambda g, a=True: {"train": {"grokked": g}, "analysis": {"shape_ok": True, "match_ok": True,
                            "p1": {"pass": True}, "p2": {"pass": True}, "p4": {"pass": a}} if g else None}
    assert T.verdict([ok(True), ok(True), ok(True)], P) == "proved"
    assert T.verdict([ok(True), ok(True), ok(False)], P) == "proved"
    assert T.verdict([ok(True), ok(True, False), ok(True)], P) == "disproved"
    assert T.verdict([ok(True, False), ok(False), ok(False)], P) == "void"
