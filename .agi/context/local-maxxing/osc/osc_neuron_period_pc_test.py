"""Tests for osc_neuron_period_pc.py (hypothesis:lm-neuron-periodicity-pipeline-finds-the-known-mod-p-circuit TESTS
1-4, plus the import-not-copy rule, the null shape and checkpoint resume). CPU, a few seconds.

Run (the torch venv has no pytest; borrow the user site's):
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):$(python3 -m site --user-site)" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_neuron_period_pc_test.py -q --basetemp /tmp/<dir>
"""
import json
import os
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period2 as R2  # noqa: E402
import osc_neuron_period_pc as S  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_neuron_period_pc_dir"), "params.json")))
p = P["p"]


def test_1_split_is_deterministic_disjoint_and_complete():
    X, y, tr, te = S.data(P)
    X2, y2, tr2, te2 = S.data(P)
    assert torch.equal(tr, tr2) and torch.equal(te, te2) and torch.equal(X, X2)
    assert len(tr) == int(0.3 * p * p) == 3830 and len(te) == p * p - 3830
    assert not set(tr.tolist()) & set(te.tolist())
    assert sorted(tr.tolist() + te.tolist()) == list(range(p * p))
    assert X.shape == (p * p, 3) and bool((X[:, 2] == p).all())
    assert torch.equal(y, (X[:, 0] + X[:, 1]) % p)
    assert not torch.equal(tr, S.data({**P, "split_seed": 1})[2])


@pytest.mark.parametrize("k", [2, 4, 14, 35, 41, 52, 56])
@pytest.mark.parametrize("phase", [0.0, 0.7, np.pi / 2])
def test_2_imported_peakiness_recovers_the_frequency_of_a_pure_sinusoid(k, phase):
    a = np.arange(p)
    x = np.cos(2 * np.pi * k * a / p + phase)[:, None]
    pk, kb = R2.dpeak(x, P["detrend_tol"])
    assert kb[0] == k and pk[0] > 0.8   # a sine leaks into the linear detrend: k=2 at phase pi/2 -> 0.848
    # through the pipeline: 5 b, phase shifted by b (the mod-p structure), plus a ReLU (harmonics)
    acts = np.stack([np.maximum(np.cos(2 * np.pi * k * (a[:, None] + b) / p + phase), 0) for b in P["b_set"]])
    spk, skb = S.stat(acts, P["detrend_tol"])
    assert skb[0] == k and spk[0] > 0.4


def test_2_k1_is_the_imported_detrend_blind_spot():
    # recorded, not fixed (the pipeline is imported unchanged): the linear detrend eats most of a k=1 sine
    a = np.arange(p)
    pk, kb = R2.dpeak(np.sin(2 * np.pi * a / p)[:, None], P["detrend_tol"])
    assert kb[0] == 1 and pk[0] < 0.5
    assert R2.dpeak(np.cos(2 * np.pi * a / p)[:, None], P["detrend_tol"])[0][0] > 0.9


def test_2b_pipeline_is_imported_not_copied():
    src = open(S.__file__).read()
    assert "rfft" not in src and "def detrend" not in src and "def peakiness" not in src
    assert "R2.dpeak" in src and "R2.detrended_null" in src


def test_null_shape_and_mode_rule():
    rng = np.random.default_rng(0)
    acts = rng.normal(size=(5, p, 7))
    nl = S.null(acts, P)
    assert nl.shape == (P["null_permutations"], 7) and nl.max() < 0.5
    expect = np.mean([R2.detrended_null(x, 20, P["null_seed"], P["detrend_tol"]) for x in acts], 0)
    assert np.array_equal(nl, expect)
    a = np.arange(p)
    col = lambda k: np.cos(2 * np.pi * k * a / p)
    acts = np.stack([np.stack([col(k)], 1) for k in (9, 3, 9, 3, 5)])
    assert S.stat(acts, P["detrend_tol"])[1][0] == 3   # tie 3 vs 9 -> smallest


def test_3_mean_ablation_of_zero_neurons_changes_nothing():
    model, (X, y, tr, te) = S.make(P, 0).eval(), S.data(P)
    n = P["model"]["d_mlp"]
    S.evaluate(model, X, y)
    means = model.seen.mean(0)
    mask = lambda ids: torch.isin(torch.arange(n), torch.tensor(ids, dtype=int))
    assert S.evaluate(model, X[te], y[te], (mask([]), means)) == S.evaluate(model, X[te], y[te])
    with torch.no_grad():
        base = model(X[te]).clone()
        model.abl = (mask([]), means)
        assert torch.equal(model(X[te]), base)
        h0 = model.seen.clone()
        model.abl = (mask([3, 77]), means)
        model(X[te])
        model.abl = None
    h = model.seen
    assert torch.equal(h[:, [3, 77]], means[[3, 77]].expand(len(te), 2))
    keep = [i for i in range(n) if i not in (3, 77)]
    assert torch.equal(h[:, keep], h0[:, keep])
    assert model.abl is None


def test_4_twin_is_the_same_architecture_with_a_recorded_seed():
    assert isinstance(P["twin_seed"], int) and P["twin_seed"] not in (P["train_seed"], P["fallback_seed"])
    t, t2, m = S.make(P, P["twin_seed"]), S.make(P, P["twin_seed"]), S.make(P, P["train_seed"])
    sd, sd2, sdm = t.state_dict(), t2.state_dict(), m.state_dict()
    assert {k: v.shape for k, v in sd.items()} == {k: v.shape for k, v in sdm.items()}
    assert all(torch.equal(sd[k], sd2[k]) for k in sd)
    assert not torch.equal(sd["E"], sdm["E"])
    assert sd["w_in.weight"].shape == (512, 128) and sd["E"].shape == (114, 128) and sd["U.weight"].shape == (113, 128)
    assert S.sweep(t.eval(), P).shape == (5, p, 512)


def test_train_resumes_exactly_from_a_checkpoint(tmp_path):
    X, y, tr, te = S.data(P)
    torch.set_num_threads(2)
    Q = {**P, "step_cap": 200, "checkpoint_every": 100}
    (tmp_path / "a").mkdir(), (tmp_path / "b").mkdir()
    ma, ra = S.train(Q, str(tmp_path / "a"), 0, X, y, tr, te, print)
    S.train({**Q, "step_cap": 100}, str(tmp_path / "b"), 0, X, y, tr, te, print)
    mb, rb = S.train(Q, str(tmp_path / "b"), 0, X, y, tr, te, print)
    assert ra["steps"] == rb["steps"] == 200 and not ra["grokked"]
    assert [r[0] for r in rb["curve"]] == [0, 100, 200]
    assert all(torch.allclose(ma.state_dict()[k], mb.state_dict()[k], atol=1e-6) for k in ma.state_dict())
    assert ra["curve"][-1][2] == pytest.approx(rb["curve"][-1][2], abs=1e-3)
    assert ra["curve"][-1][1] < ra["curve"][0][1]   # it learns
