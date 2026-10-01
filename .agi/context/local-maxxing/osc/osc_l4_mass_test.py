"""Tests for osc_l4_mass.py (hypothesis:lm-l4-outside-window-mass-picks-the-heads-to-window TESTS 1-4). No model load.

Run (the torch venv has no pytest; borrow the user site's):
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):$(python3 -m site --user-site)" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_l4_mass_test.py -q --basetemp /tmp/<dir>
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
import osc_l4_mass as X  # noqa: E402
import osc_l4_distance as D  # noqa: E402
import osc_l4_window as W  # noqa: E402
import paths  # noqa: E402

M = pytest.importorskip("transformers.models.qwen2.modeling_qwen2")
W.install(M)
NQ, NKV, G, HD = 14, 2, 7, 16
RUN1_COMMIT, RUN2_COMMIT = "378a3c3eaf", "e18b2e41dd"


def causal(T):
    m = torch.zeros(1, 1, T, T)
    return m.masked_fill(torch.ones(T, T, dtype=torch.bool).triu(1), torch.finfo(torch.float32).min)


def uniform(T):
    w = torch.tril(torch.ones(T, T))
    return (w / w.sum(-1, keepdim=True))[None]


def test_1_head_inside_sinks_and_window_has_zero_mass():
    T, Wn, s = 300, 128, 4
    w = torch.zeros(1, T, T)
    for t in range(T):
        keep = [j for j in range(t + 1) if j < s or j > t - Wn]
        w[0, t, keep] = 1.0 / len(keep)
    assert torch.equal(X.mass_outside(w, W.disallow(T, Wn, s), 140, T), torch.zeros(1, dtype=torch.float64))
    w[0, 200, 50] += 0.25                      # one dropped key (4 <= 50 <= 200 - 128) at one row
    assert X.mass_outside(w, W.disallow(T, Wn, s), 200, 201).item() == pytest.approx(0.25, abs=1e-7)


def test_2_uniform_head_gets_the_analytic_mass_and_the_averaging_is_over_query_rows():
    P = X.load_params(paths.get_local("osc_band_l4_mass_dir"))
    L, Wn, s, lo, hi = P["L"], P["W"], P["sinks"], P["score_lo"], P["score_hi"]
    w, bad = uniform(L), W.disallow(L, Wn, s)
    assert X.mass_outside(w, bad, L - 1, L).item() == pytest.approx((L - Wn - s) / L, abs=1e-6)   # (L - 132) / L
    avg = sum(max(t - Wn - s + 1, 0) / (t + 1) for t in range(lo, hi)) / (hi - lo)
    assert X.mass_outside(w, bad, lo, hi).item() == pytest.approx(avg, abs=1e-6)
    assert lo >= Wn + s                        # every averaged row has the window binding


def test_2b_hook_matches_hand_on_real_attention_and_leaves_output_unchanged():
    T, g = 12, torch.Generator().manual_seed(3)
    q, k, v = torch.randn(1, NQ, T, HD, generator=g), torch.randn(1, NKV, T, HD, generator=g), torch.randn(
        1, NKV, T, HD, generator=g)
    mod = types.SimpleNamespace(layer_idx=0, num_key_value_groups=G, training=False)
    W.S.update(win={}, dist=None, bad=W.disallow(T, 3, 2), lo=6, hi=12)
    X.MASS.update(on=True, m={})
    out, w = X.attn(mod, q, k, v, causal(T), HD ** -0.5)
    X.MASS["on"] = False
    ref, _ = W.ORIG["eager"](mod, q, k, v, causal(T), HD ** -0.5)
    assert torch.equal(out, ref)
    t, j = torch.arange(6, 12)[:, None], torch.arange(T)[None, :]
    hand = (w[0, :, 6:12].double() * ((j >= 2) & (j <= t - 3)).double()).sum(-1).mean(-1)
    assert torch.allclose(X.MASS["m"][0], hand, atol=1e-7)


def tiny_model():
    cfg = M.Qwen2Config(vocab_size=64, hidden_size=NQ * 8, intermediate_size=64, num_hidden_layers=2,
                        num_attention_heads=NQ, num_key_value_heads=NKV, max_position_embeddings=64)
    cfg._attn_implementation = "eager"
    torch.manual_seed(0)
    return M.Qwen2ForCausalLM(cfg).eval()


def test_3_direct_per_head_kl_is_exactly_zero_when_W_ge_L():
    model, T, lo, hi = tiny_model(), 32, 16, 32
    M.eager_attention_forward = X.attn
    ids = torch.randint(0, 64, (1, T), generator=torch.Generator().manual_seed(1))
    W.S.update(win={}, dist=None, bad=W.disallow(T, T, 4), lo=lo, hi=hi)
    h = X.hidden(model, ids, lo, hi)
    for head in range(2 * NKV):                # every KV head alone, window W = L
        assert X.scored(model, h, ids, [head], NKV, lo, hi, 8) == (1.0, 0.0)
    W.S["bad"] = W.disallow(T, 4, 2)           # a window that bites gives KL > 0
    assert X.scored(model, h, ids, [0, 1, 2, 3], NKV, lo, hi, 8)[1] > 0
    assert torch.equal(X.hidden(model, ids, lo, hi), h)   # the full pass resets the window


def test_3b_grid_inherited_not_retyped_and_kept_equals_runs_1_2():
    out = paths.get_local("osc_band_l4_mass_dir")
    P, raw = X.load_params(out), json.load(open(os.path.join(out, "params.json")))
    B1 = json.load(open(os.path.join(paths.get_local("osc_band_l4_dir"), "params.json")))
    B2 = json.load(open(os.path.join(paths.get_local("osc_band_l4_distance_dir"), "params.json")))
    assert all(P[k] == B1[k] for k in P["inherit"]) and all(P[k] == B2[k] for k in P["inherit_run2"])
    assert not {"eval_docs", "budgets", "k", "W", "sinks", "seeds", "calib_docs"} & set(raw)
    assert [d for d, _ in P["calib_docs"]] == [12, 16, 18]
    assert not {d for d, _ in P["calib_docs"]} & ({d for d, _ in P["eval_docs"]} | set(P["exclude_docs"]))
    R1 = json.load(open(os.path.join(paths.get_local("osc_band_l4_dir"), "results.json")))
    for b, k in zip(P["budgets"], P["k"]):
        assert W.kept_fraction(k, P["W"], P["sinks"], P["L"], 48) == R1["table"][str(b)]["kept"]


def test_4_run1_run2_imported_not_copied_and_unchanged():
    src = inspect.getsource(X)
    for name in ("disallow", "window_mask", "kept_fraction", "load_docs", "score", "as_win", "install", "spearman",
                 "ranking", "sink_free_distance"):
        assert f"def {name}(" not in src
    for name in ("disallow", "kept_fraction", "load_docs", "score", "as_win", "install", "attn"):
        assert f"W.{name}(" in src
    for name in ("spearman", "ranking", "load_params"):
        assert f"D.{name}(" in src
    assert X.W is W and X.D is D and D.W is W
    for f, c in (("osc_l4_window.py", RUN1_COMMIT), ("osc_l4_distance.py", RUN2_COMMIT)):
        for rev in (c, "HEAD"):
            r = subprocess.run(["git", "-C", HERE, "diff", "--quiet", rev, "--", os.path.join(HERE, f)])
            assert r.returncode == 0, (f, rev)
