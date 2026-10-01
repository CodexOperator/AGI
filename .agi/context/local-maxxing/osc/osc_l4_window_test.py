"""Tests for osc_l4_window.py (hypothesis:lm-l4-local-heads-keep-a-recent-window TESTS 1-4). No model load.

Run (the torch venv has no pytest; borrow the user site's):
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):$(python3 -m site --user-site)" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_l4_window_test.py -q --basetemp /tmp/<dir>
"""
import json
import os
import sys
import types

import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import osc_l4_window as W  # noqa: E402
import paths  # noqa: E402

M = pytest.importorskip("transformers.models.qwen2.modeling_qwen2")
W.install(M)
EAGER = W.ORIG["eager"]
NQ, NKV, G, D = 14, 2, 7, 16


def causal(T):
    m = torch.zeros(1, 1, T, T)
    return m.masked_fill(torch.ones(T, T, dtype=torch.bool).triu(1), torch.finfo(torch.float32).min)


def qkv(T, seed=0):
    g = torch.Generator().manual_seed(seed)
    return (torch.randn(1, NQ, T, D, generator=g), torch.randn(1, NKV, T, D, generator=g),
            torch.randn(1, NKV, T, D, generator=g))


def mod(layer=0):
    return types.SimpleNamespace(layer_idx=layer, num_key_value_groups=G, training=False)


def run(T, win, Wn, sinks, seed=0):
    q, k, v = qkv(T, seed)
    W.S["win"], W.S["bad"], W.S["dist"] = win, W.disallow(T, Wn, sinks), None
    out, _ = W.attn(mod(), q, k, v, causal(T), D ** -0.5)
    W.S["win"] = {}
    ref, _ = EAGER(mod(), q, k, v, causal(T), D ** -0.5)
    return out, ref


def test_1_window_ge_L_is_exact_full_attention():
    for Wn in (32, 40):
        out, ref = run(32, {0: [0, 1]}, Wn, 4)
        assert torch.equal(out, ref)


def test_2_window_changes_exactly_positions_beyond_W_plus_sinks():
    T, Wn, s = 24, 4, 2
    out, ref = run(T, {0: [0]}, Wn, s, seed=3)   # out: (B, T, NQ, D)
    assert torch.equal(out[:, :, G:], ref[:, :, G:])          # kv head 1's group untouched
    assert torch.equal(out[:, :Wn + s, :G], ref[:, :Wn + s, :G])   # rows t < W + sinks untouched
    diff = (out[0, Wn + s:, :G] - ref[0, Wn + s:, :G]).abs().amax(-1)
    assert bool((diff > 1e-6).all())                          # every later row of every group head moves


def test_2b_mask_is_shared_by_the_whole_gqa_group():
    m = W.window_mask(causal(10), [1], NQ, G, W.disallow(10, 3, 1))
    assert all(torch.equal(m[0, G], m[0, h]) for h in range(G, NQ))
    assert all(torch.equal(m[0, 0], m[0, h]) for h in range(G))
    assert not torch.equal(m[0, 0], m[0, G])


@pytest.mark.parametrize("k,expect", [(13, 0.7466), (21, 0.5907), (26, 0.4933)])
def test_3_kept_fraction_matches_counted_unmasked_pairs(k, expect):
    L, Wn, s, nl = 2048, 128, 4, 24
    n = nl * NKV
    heads = list(range(0, 2 * k, 2))[:k] if 2 * k <= n else list(range(k))
    win, bad, kept = W.as_win(heads, NKV), W.disallow(L, Wn, s), 0
    base = causal(L)
    for layer in range(nl):
        m = W.window_mask(base, win.get(layer, []), NQ, G, bad)
        last = m[0, :, L - 1] > torch.finfo(torch.float32).min   # the KV each head still holds at t = L-1
        kept += sum(int(last[g * G].sum()) for g in range(NKV))
    assert kept / (n * L) == pytest.approx(W.kept_fraction(k, Wn, s, L, n), abs=1e-12)
    assert W.kept_fraction(k, Wn, s, L, n) == pytest.approx(expect, abs=1e-4)   # node rounds 0.493245 up to 0.4933


def test_3b_params_k_are_within_half_a_head_of_budget():
    P = json.load(open(os.path.join(paths.get_local("osc_band_l4_dir"), "params.json")))
    n = 48
    tol = 0.5 * (1 - (P["W"] + P["sinks"]) / P["L"]) / n
    for b, k in zip(P["budgets"], P["k"]):
        assert abs(W.kept_fraction(k, P["W"], P["sinks"], P["L"], n) - b) <= tol


def test_4_ranking_is_deterministic_from_profiles():
    P = json.load(open(os.path.join(paths.get_local("osc_band_l4_dir"), "params.json")))
    prof = json.load(open(os.path.join(paths.get_local(P["profiles_cell"]), P["profiles_file"])))["heads"]
    o1, s1 = W.kv_ranking(prof, P["high_pairs"], 24, NKV, G)
    o2, s2 = W.kv_ranking(json.loads(json.dumps(prof)), P["high_pairs"], 24, NKV, G)
    assert o1 == o2 and s1 == s2 and sorted(o1) == list(range(48))
    assert all(s1[a] >= s1[b] for a, b in zip(o1, o1[1:]))
    hand = sum(sum(prof[f"L7H{7 + j}"]["profile_pooled"][p] for p in P["high_pairs"]) for j in range(G)) / G
    assert s1[7 * NKV + 1] == pytest.approx(hand, abs=1e-12)


def test_dist_hook_measures_mean_attention_distance():
    T = 8
    q, k, v = qkv(T)
    W.S["win"], W.S["dist"], W.S["lo"], W.S["hi"] = {}, {}, 4, 8
    _, w = W.attn(mod(), q, k, v, causal(T), D ** -0.5)
    t = torch.arange(4, 8)[:, None].float()
    hand = (w[0, :, 4:8] * (t - torch.arange(T)[None, :]).clamp_min(0)).sum(-1).mean(-1)
    assert torch.allclose(W.S["dist"][0].float(), hand, atol=1e-6)
    W.S["dist"] = None
