"""Tests for osc_neuron_period.py (hypothesis:lm-neuron-periodicity-map-finds-function-neurons TESTS 1-4). No weights
load: a tiny random Qwen2 built from a config in-process.

Run (the torch venv has no pytest; borrow the user site's):
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):$(python3 -m site --user-site)" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_neuron_period_test.py -q --basetemp /tmp/<dir>
"""
import copy
import json
import math
import os
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")
Q = pytest.importorskip("transformers.models.qwen2.modeling_qwen2")
from transformers import Qwen2Config  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import osc_neuron_period as S  # noqa: E402
import paths  # noqa: E402

WIDTH, LAYERS = 48, 3


def tiny():
    torch.manual_seed(0)
    cfg = Qwen2Config(vocab_size=64, hidden_size=32, intermediate_size=WIDTH, num_hidden_layers=LAYERS,
                      num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=64)
    return Q.Qwen2ForCausalLM(cfg).eval()


def test_1_peakiness_sinusoid_is_one_and_noise_is_flat():
    N = 100
    a = np.arange(N)
    for k in (1, 10, 20, 50):
        pk, kb = S.peakiness(np.cos(2 * np.pi * k * a / N + 0.3)[:, None] * 3.0 + 7.0)
        assert pk[0] == pytest.approx(1.0, abs=1e-12) and kb[0] == k
    X = np.random.default_rng(0).standard_normal((N, 20000))
    P = np.abs(np.fft.rfft(X, axis=0)[1:]) ** 2
    share = P / P.sum(0)
    assert share.mean() == pytest.approx(2 / N, rel=1e-9)   # 50 non-DC bins: mean share 1/50 = 2/N exactly
    pk = S.peakiness(X)[0]
    assert 2 / N < pk.mean() < 0.15                       # the max of 50 shares: ~H_50/50 = 0.09, far from 1
    assert S.peakiness(np.ones((N, 2)))[0].tolist() == [0.0, 0.0]   # constant series: zero power -> 0


def test_2_hook_reads_exactly_the_down_proj_input():
    model = tiny()
    N = S.Neurons(model)
    seen = {}
    for i, layer in enumerate(model.model.layers):   # the MLP's own input, to recompute act(gate(x)) * up(x)
        layer.mlp.register_forward_pre_hook(lambda m, a, i=i: seen.__setitem__(i, a[0].detach()))
    ids = torch.randint(0, 64, (5, 9), generator=torch.Generator().manual_seed(1))
    acts = N.read(model, ids, S.last_token, bs=2)
    assert acts.shape == (5, LAYERS * WIDTH)
    _ = N.read(model, ids, S.last_token, bs=5)   # seen <- the whole batch
    for i, layer in enumerate(model.model.layers):
        m = layer.mlp
        want = (m.act_fn(m.gate_proj(seen[i])) * m.up_proj(seen[i]))[:, -1]
        assert torch.allclose(torch.from_numpy(acts[:, i * WIDTH:(i + 1) * WIDTH]), want, atol=1e-6)


def test_3_zero_ablation_acts_only_through_that_neurons_down_proj_column():
    model = tiny()
    ref = copy.deepcopy(model)
    N = S.Neurons(model)
    ids = torch.randint(0, 64, (2, 7), generator=torch.Generator().manual_seed(2))
    with torch.no_grad():
        base = model(input_ids=ids).logits
        for flat in ([1 * WIDTH + 5], [0 * WIDTH + 3, 2 * WIDTH + 47]):
            N.ablate(flat)
            abl = model(input_ids=ids).logits
            N.ablate([])
            col = copy.deepcopy(ref)
            for f in flat:
                col.model.layers[f // WIDTH].mlp.down_proj.weight[:, f % WIDTH] = 0.0
            assert torch.allclose(abl, col(input_ids=ids).logits, atol=1e-6)
            assert not torch.allclose(abl, base, atol=1e-6)
        assert torch.equal(model(input_ids=ids).logits, base)   # ablate([]) restores the forward exactly


def test_3b_greedy_matches_full_recompute_argmax():
    model = tiny()
    ids = torch.randint(0, 64, (3, 6), generator=torch.Generator().manual_seed(3))
    got, x = S.greedy(model, ids, 4), ids
    with torch.no_grad():
        for _ in range(4):
            x = torch.cat([x, model(input_ids=x).logits[:, -1:].argmax(-1)], 1)
    assert torch.equal(got, x[:, 6:])


def test_4_shuffled_null_keeps_the_activation_multiset():
    acts = np.random.default_rng(4).standard_normal((100, 30)) * np.arange(1, 31)
    null = S.shuffled_null(acts, 20, 0)
    rng = np.random.default_rng(0)
    for r in range(20):
        perm = acts[rng.permutation(100)]
        assert np.array_equal(np.sort(perm, 0), np.sort(acts, 0))   # same values per neuron, a-order only
        assert np.array_equal(null[r], S.peakiness(perm)[0])
    assert null.shape == (20, 30)


def test_hypergeometric_tail_matches_brute_force():
    N, K, n = 60, 9, 12
    for x in range(0, 10):
        brute = sum(math.comb(K, i) * math.comb(N - K, n - i) for i in range(x, min(K, n) + 1)) / math.comb(N, n)
        assert S.hyper_sf(x, N, K, n) == pytest.approx(brute, rel=1e-9)
    assert S.hyper_sf(0, 116736, 0, 1167) == pytest.approx(1.0)


def test_params_pre_registered():
    P = json.load(open(os.path.join(paths.get_local("osc_neuron_period_dir"), "params.json")))
    assert P["c1_a"] == [0, 100] and P["c1_null_permutations"] == 20 and P["c1_null_quantile"] == 0.999
    assert P["c1_min_fraction"] == 0.005 and P["c2_k"] == 64 and len(P["c2_random_seeds"]) == 5
    assert P["c2_problems"] >= 200 and P["c2_min_baseline"] == 0.5 and P["c3_alpha"] == 0.01
    assert P["c3_doc"][0] not in (0, 1, 3, 4, 5, 6, 7, 10, 12)   # held out from every L4 doc
    texts, gold = S.c2_problems(P)
    assert len(set(map(len, texts))) == 1 and all(g == str(int(t.split("\n")[-1][:2]) + int(t.split("\n")[-1][3:5]))
                                                  for t, g in zip(texts, gold))
