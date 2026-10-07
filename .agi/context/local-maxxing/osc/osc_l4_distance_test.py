"""Tests for osc_l4_distance.py (hypothesis:lm-l4-measured-distance-heads-keep-a-recent-window TESTS 1-4). No model load.

Run (the torch venv has no pytest; borrow the user site's):
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):$(python3 -m site --user-site)" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_l4_distance_test.py -q --basetemp /tmp/<dir>
"""
import inspect
import json
import os
import subprocess
import sys
import types

import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import osc_l4_distance as D  # noqa: E402
import osc_l4_window as W  # noqa: E402
import paths  # noqa: E402

M = pytest.importorskip("transformers.models.qwen2.modeling_qwen2")
W.install(M)
NQ, NKV, G, HD = 14, 2, 7, 16


def causal(T):
    m = torch.zeros(1, 1, T, T)
    return m.masked_fill(torch.ones(T, T, dtype=torch.bool).triu(1), torch.finfo(torch.float32).min)


def params():
    return D.load_params(paths.get_local("osc_band_l4_distance_dir"))


def run1(name):
    return json.load(open(os.path.join(paths.get_local("osc_band_l4_dir"), name)))


def test_1_sink_keys_contribute_zero_distance():
    T, s = 12, 4
    sink_only = torch.zeros(1, T, T)
    sink_only[0, :, 0] = 0.5
    sink_only[0, :, 3] = 0.5                  # all mass on sinks 0 and 3
    assert torch.equal(D.sink_free_distance(sink_only, 6, 12, s), torch.zeros(1, dtype=torch.float64))
    mixed = sink_only.clone() * 0.8
    for t in range(T):
        mixed[0, t, max(t - 5, 0)] += 0.2     # 0.2 of the mass at distance 5 (a sink key for t < 9)
    hand = sum(0.2 * 5 * (t - 5 >= s) for t in range(6, 12)) / 6
    assert D.sink_free_distance(mixed, 6, 12, s).item() == pytest.approx(hand, abs=1e-6)
    # run 1's hook counts the sinks: its distance for the sink-only head is > 0
    assert (sink_only[0, 6:12] * (torch.arange(6, 12)[:, None] - torch.arange(T)).clamp_min(0)).sum(-1).mean() > 0


def test_1b_hook_matches_hand_on_real_attention_and_leaves_output_unchanged():
    T, g = 10, torch.Generator().manual_seed(1)
    q, k, v = torch.randn(1, NQ, T, HD, generator=g), torch.randn(1, NKV, T, HD, generator=g), torch.randn(
        1, NKV, T, HD, generator=g)
    mod = types.SimpleNamespace(layer_idx=0, num_key_value_groups=G, training=False)
    W.S["win"], W.S["dist"] = {}, None
    D.DIST.update(on=True, sinks=2, lo=5, hi=10, d={})
    out, w = D.attn(mod, q, k, v, causal(T), HD ** -0.5)
    D.DIST["on"] = False
    ref, _ = W.ORIG["eager"](mod, q, k, v, causal(T), HD ** -0.5)
    assert torch.equal(out, ref)
    t, j = torch.arange(5, 10)[:, None], torch.arange(T)[None, :]
    hand = (w[0, :, 5:10].double() * ((t - j).clamp_min(0) * (j >= 2)).double()).sum(-1).mean(-1)
    assert torch.allclose(D.DIST["d"][0], hand, atol=1e-6)


def test_2_averaged_ranking_is_deterministic_and_ties_break_by_index():
    rng = torch.Generator().manual_seed(0)
    dists = torch.rand(3, 48, generator=rng).tolist()
    r1, m1 = D.ranking(dists)
    r2, m2 = D.ranking(json.loads(json.dumps(dists)))
    assert r1 == r2 and m1 == m2 and sorted(r1) == list(range(48))
    assert all(m1[a] <= m1[b] for a, b in zip(r1, r1[1:]))
    assert m1[5] == pytest.approx(sum(d[5] for d in dists) / 3, abs=1e-12)
    assert D.ranking([[2.0, 1.0, 1.0, 0.5], [2.0, 1.0, 1.0, 0.5], [2.0, 1.0, 1.0, 0.5]])[0] == [3, 1, 2, 0]
    assert D.spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert D.spearman([1, 2, 3, 4], [4, 3, 2, 1]) == pytest.approx(-1.0)


def test_3_kept_fractions_equal_run1_and_grid_is_inherited_not_retyped():
    P, B, R = params(), run1("params.json"), run1("results.json")
    for key in P["inherit"]:
        assert P[key] == B[key]
    raw = json.load(open(os.path.join(paths.get_local("osc_band_l4_distance_dir"), "params.json")))
    assert not {"eval_docs", "budgets", "k", "W", "sinks"} & set(raw)
    for b, k in zip(P["budgets"], P["k"]):
        assert W.kept_fraction(k, P["W"], P["sinks"], P["L"], 48) == R["table"][str(b)]["kept"]


def test_3b_calibration_docs_disjoint_from_eval_and_excluded():
    P = params()
    cal = {d for d, _ in P["calib_docs"]}
    assert len(cal) == 3 and not cal & {d for d, _ in P["eval_docs"]} and not cal & set(P["exclude_docs"])
    assert 13 in P["exclude_docs"]


def test_4_run1_functions_are_imported_not_copied_and_run1_unchanged():
    src = inspect.getsource(D)
    for name in ("disallow", "window_mask", "kept_fraction", "load_docs", "score", "as_win", "install"):
        assert f"def {name}(" not in src
    for name in ("disallow", "kept_fraction", "load_docs", "score", "as_win", "install", "attn"):
        assert f"W.{name}(" in src            # W.attn applies run 1's window_mask
    assert D.W is W
    f = os.path.join(HERE, "osc_l4_window.py")
    assert subprocess.run(["git", "-C", HERE, "diff", "--quiet", "HEAD", "--", f]).returncode == 0
