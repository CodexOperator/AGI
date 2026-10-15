"""Tests for osc_neuron_period2.py (hypothesis:lm-neuron-periodicity-detrended-families-carry-addition TESTS 1-4,
plus the scorer, the stratified tail and the pre-registration). No model weights load: a tiny random Qwen2.

Run (the torch venv has no pytest; borrow the user site's):
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):$(python3 -m site --user-site)" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_neuron_period2_test.py -q --basetemp /tmp/<dir>
"""
import itertools
import json
import os
import shutil
import sys

import pytest

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")
Q = pytest.importorskip("transformers.models.qwen2.modeling_qwen2")
from transformers import Qwen2Config  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import osc_neuron_period as S1  # noqa: E402
import osc_neuron_period2 as S  # noqa: E402
import paths  # noqa: E402

WIDTH, LAYERS = 48, 3
a = np.arange(100)


def tiny(vocab=64):
    torch.manual_seed(0)
    cfg = Qwen2Config(vocab_size=vocab, hidden_size=32, intermediate_size=WIDTH, num_hidden_layers=LAYERS,
                      num_attention_heads=4, num_key_value_heads=2, max_position_embeddings=128)
    return Q.Qwen2ForCausalLM(cfg).eval()


def test_1_detrend_removes_an_exact_ramp():
    ramp = (3.0 * a - 7.0)[:, None]
    assert S1.peakiness(ramp)[0][0] == pytest.approx(0.608, abs=1e-3)   # run 1's fragility: a raw ramp scores 0.608
    assert np.abs(S.detrend(ramp)).max() == 0.0 and S.dpeak(ramp)[0][0] == 0.0   # exact ramp -> residual 0
    assert S.dpeak(np.ones((100, 1)) * 5)[0][0] == 0.0 and S.dpeak(np.zeros((100, 1)))[0][0] == 0.0
    noise = np.random.default_rng(0).standard_normal((100, 2000))
    noisy = S.dpeak(ramp * 10 + noise)[0]                  # ramp + noise -> the noise's own peakiness level
    assert noisy.mean() < 0.15 and abs(noisy.mean() - S.dpeak(noise)[0].mean()) < 0.01
    X = np.random.default_rng(1).standard_normal((100, 5))
    R = S.detrend(X)
    A = np.stack([np.ones(100), a], 1)
    assert np.allclose(R, X - A @ np.linalg.lstsq(A, X, rcond=None)[0], atol=1e-12)   # = least-squares residual


@pytest.mark.parametrize("period", [2, 5, 10])
def test_2_a_sinusoid_keeps_its_period_after_detrend(period):
    x = np.cos(2 * np.pi * a / period + 0.4)[:, None] + 0.05 * a[:, None] + 3.0   # oscillation riding on a ramp
    pk, kb = S.dpeak(x)
    assert 100 / kb[0] == period and pk[0] > 0.9
    assert period == 2 or 100 / S1.peakiness(x)[1][0] == 100   # without detrend the ramp wins (k = 1)


def test_3_layer_matched_sampler_reproduces_per_layer_counts():
    W, L = 50, 4
    fam = [3, 7, 11, 60, 61, 199, 150, 151, 152]   # layers 0 x3, 1 x2, 2 x1, 3 x3
    want = np.bincount(np.array(fam) // W, minlength=L)
    seen = []
    for s in range(5):
        r = S.layer_matched(fam, W, L, s)
        assert np.array_equal(np.bincount(np.array(r) // W, minlength=L), want) and len(set(r)) == len(fam)
        assert not set(r) & set(fam) and r == S.layer_matched(fam, W, L, s)   # disjoint, seed-deterministic
        seen.append(tuple(r))
    assert len(set(seen)) == 5 and S.layer_matched([], W, L, 0) == []


def test_4_mean_ablation_replaces_with_the_calibration_mean_and_nothing_else():
    model = tiny()
    N = S.Neurons2(model)
    calib = torch.randint(0, 64, (10, 6), generator=torch.Generator().manual_seed(1))
    means = torch.from_numpy(N.read(model, calib, S1.last_token).mean(0).reshape(LAYERS, WIDTH)).float()
    ids = torch.randint(0, 64, (3, 8), generator=torch.Generator().manual_seed(2))
    every = lambda x: x.numpy().copy()   # all positions
    base = N.read(model, ids, every)
    flat = [1 * WIDTH + 5, 1 * WIDTH + 9, 2 * WIDTH + 0]
    N.means = means
    N.ablate(flat)
    got = N.read(model, ids, every)
    for f in flat:   # the ablated neuron = its calibration mean at every position
        assert np.allclose(got[..., f], float(means[f // WIDTH, f % WIDTH]), atol=0)
    keep = [i for i in range(WIDTH * 2) if i not in flat]   # layers 0-1: every other neuron untouched
    assert np.array_equal(got[..., keep], base[..., keep])
    N.means = None
    N.ablate(flat)   # zero mode == run 1's zero-ablation
    z = N.read(model, ids, every)
    ref_model = tiny()   # same seed -> same weights
    ref = S1.Neurons(ref_model)
    ref.ablate(flat)
    assert np.array_equal(z, ref.read(ref_model, ids, every)) and all(np.all(z[..., f] == 0) for f in flat)
    N.ablate([])
    assert np.array_equal(N.read(model, ids, every), base)   # ablate([]) restores exactly


def test_gold_logp_matches_unbatched_teacher_forcing(tmp_path, allow_model_load):
    for f in ("tokenizer.json", "tokenizer_config.json"):   # tokenizer files only, into a declared tmp dir
        shutil.copy(os.path.join(paths.get("osc03_hf_dir"), f), tmp_path / f)
    allow_model_load(tmp_path)
    tok = pytest.importorskip("transformers").AutoTokenizer.from_pretrained(str(tmp_path))
    model = tiny(vocab=len(tok))
    texts, gold = ["12+35=47\n9+9=", "12+35=47\n5+5=", "12+35=47\n1+1="], ["18", "10", "2"]
    got = S.gold_logp(model, tok, texts, gold, bs=2)
    for t, g, v in zip(texts, gold, got):
        p, q = tok(t)["input_ids"], tok(g)["input_ids"]
        with torch.no_grad():
            lp = torch.log_softmax(model(input_ids=torch.tensor([p + q])).logits[0], -1)
        assert v == pytest.approx(sum(float(lp[len(p) - 1 + j, q[j]]) for j in range(len(q))), abs=1e-4)


def test_stratified_tail_matches_brute_force():
    N, K_l, n_l = 6, [2, 3], [2, 3]
    pairs = [(set(A), set(B)) for A in itertools.combinations(range(N), n_l[0])
             for B in itertools.combinations(range(N), n_l[1])]   # successes = ids < K_l
    for x in range(6):
        brute = sum(len([i for i in A if i < K_l[0]]) + len([i for i in B if i < K_l[1]]) >= x
                    for A, B in pairs) / len(pairs)
        assert S.strat_sf(x, n_l, K_l, N) == pytest.approx(brute, rel=1e-9)


def test_detrended_null_permutes_then_detrends():
    acts = np.random.default_rng(4).standard_normal((100, 30)) + a[:, None] * np.arange(30)
    null = S.detrended_null(acts, 5, 0, 1e-9)
    rng = np.random.default_rng(0)
    for r in range(5):
        assert np.array_equal(null[r], S.dpeak(acts[rng.permutation(100)])[0])


def test_number_mask_takes_the_unmasked_mean():
    toks = ["a", "1", "b", "c", "23", "d", "e"]
    take, nm = S.num_mask_take(1, toks, np.arange(7), 1e-9)
    x = torch.arange(14, dtype=torch.float32).reshape(1, 7, 2) ** 2
    assert nm == 2 and take(x).shape == (1, 2)
    s = x[0, 1:].numpy().astype(np.float64)
    s[[0, 3]] = s[[1, 2, 4, 5]].mean(0)
    assert np.array_equal(take(x)[0], S.dpeak(s)[0])


def test_params_pre_registered():
    P = json.load(open(os.path.join(paths.get_local("osc_neuron_period2_dir"), "params.json")))
    assert P["families"] == {"T2": [50], "T5_10": [10, 20]} and P["random_seeds"] == [0, 1, 2, 3, 4]
    assert P["d1_min_fraction"] == 0.005 and P["null_quantile"] == 0.999 and P["null_permutations"] == 20
    assert P["model_cell"] == "osc03_hf_dir" and P["family_min_size_flag"] == 10
    P1 = json.load(open(os.path.join(paths.get_local("osc_neuron_period_dir"), "params.json")))
    assert os.path.join(paths.get_local("osc_neuron_period_dir"), "params.json").endswith(P["run1_params"])
    texts, gold = S1.c2_problems(P1)
    assert len(texts) >= 200 and len(set(map(len, texts))) == 1
