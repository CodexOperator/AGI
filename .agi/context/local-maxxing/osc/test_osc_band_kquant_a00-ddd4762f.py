#!/usr/bin/env python3
"""Selftests for osc_band_kquant_a00-ddd4762f.py (fixtures + a tiny Qwen2).

Run: "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest \
  .agi/context/local-maxxing/osc/test_osc_band_kquant_a00-ddd4762f.py -q
"""
import importlib.util
import os
import sys

import pytest  # skip-by-name: this module cannot run without numpy, torch
np = pytest.importorskip('numpy')
torch = pytest.importorskip('torch')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
MOD = os.path.join(HERE, "osc_band_kquant_a00-ddd4762f.py")
spec = importlib.util.spec_from_file_location("kq", MOD)
kq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kq)


def tiny():
    from transformers import Qwen2Config, Qwen2ForCausalLM
    cfg = Qwen2Config(vocab_size=64, hidden_size=128, intermediate_size=256,
                      num_hidden_layers=2, num_attention_heads=4,
                      num_key_value_heads=2, max_position_embeddings=64)
    return Qwen2ForCausalLM(cfg).eval()


def run(mod, ids):
    kq.CAP.clear()
    with torch.no_grad():
        return mod(torch.tensor([ids])).logits


def test_bits_accounting_counts_scales():
    assert kq.avg_bits([8, 24], [4, 2]) == 3.0
    assert kq.avg_bits([4, 12, 16], [5, 3, 2]) == 3.5
    assert kq.avg_bits([8, 8, 16], [4, 3, 2]) == 3.5
    assert kq.uniform_bits(32, 3) == 3.5
    assert kq.uniform_bits(16, 2) == 3.0
    # scales are 16 bits each, so a 2-class budget is NOT just 2*bits
    assert kq.avg_bits([32], [3]) == (64 * 3 + 16) / 64.0


def test_expand_classes_pairs_p_and_p_plus_npair():
    cls = np.zeros(32, dtype=np.int64)
    cls[7] = 1
    e = kq.expand_classes(cls, 32)
    assert set(np.where(e == 1)[0].tolist()) == {7, 39}
    # the WRONG (consecutive-dims) allocation would light {14,15}
    wrong = np.repeat(cls, 2)
    assert set(np.where(wrong == 1)[0].tolist()) != {7, 39}


def test_classed_from_rank_sizes_and_order():
    rank = np.arange(31, -1, -1)          # pair 31 best
    cls = kq.classed_from_rank(rank, [4, 12, 16])
    assert cls[31] == 0 and cls[28] == 0 and cls[27] == 1 and cls[16] == 1
    assert cls[15] == 2 and cls[0] == 2
    assert sorted(np.bincount(cls).tolist(), reverse=True) == [16, 12, 4]


def test_16bit_reproduces_and_2bit_is_lossy():
    x = torch.randn(2, 2, 8, 64)
    hi = kq.quant_block(x, 64, 16)
    lo = kq.quant_block(x, 32, 2)
    assert (hi - x).abs().max() / x.abs().max() < 1e-3
    assert (lo - x).abs().max() > (hi - x).abs().max() * 100


def test_hook_quantizes_k_after_rope_and_leaves_q():
    import transformers.models.qwen2.modeling_qwen2 as M
    mod = tiny()
    ids = list(range(16))
    orig = M.apply_rotary_pos_emb
    try:
        kq.install(mod)
        kq.QCFG["fn"] = None
        ref_logits = run(mod, ids)
        q0 = kq.CAP["q"].clone()
        kpre0 = kq.CAP["k_pre"].clone()
        assert torch.equal(kpre0, kq.CAP["k_post"])
        kq.QCFG["fn"] = kq.make_qfn(block=32, ubits=2)
        run(mod, ids)
        assert torch.equal(kq.CAP["q"], q0)                      # q untouched
        assert not torch.equal(kq.CAP["k_post"], kq.CAP["k_pre"])
        assert torch.allclose(kq.CAP["k_post"],
                              kq.quant_block(kq.CAP["k_pre"], 32, 2))
        # 16-bit path reproduces the reference logits within fp tolerance
        kq.QCFG["fn"] = kq.make_qfn(block=32, ubits=16)
        lg = run(mod, ids)
        assert (lg - ref_logits).abs().max() < 1e-3
        # classwise path uses the (p, p+npair) map, not consecutive dims
        cls = np.ones(16, dtype=np.int64)
        cls[7] = 0
        cm = [[cls.copy(), cls.copy()] for _ in range(2)]
        kq.QCFG["fn"] = kq.make_qfn(cm, bits=[5, 2])
        run(mod, ids)
        assert torch.allclose(kq.CAP["k_post"],
                              kq.quant_classwise(kq.CAP["k_pre"], cls, [5, 2], 16))
    finally:
        M.apply_rotary_pos_emb = orig


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"{len(fns)} selftests passed")