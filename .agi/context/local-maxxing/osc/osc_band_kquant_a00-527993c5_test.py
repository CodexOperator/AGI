"""Selftests for osc_band_kquant_a00-527993c5.py -- fixtures only, no model load.

Run (the torch venv has no pytest):  V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" osc_band_kquant_a00-527993c5_test.py
Pytest-compatible too: every check is a function named test_*.
"""
import importlib.util
import os
import sys

import pytest  # skip-by-name: this module cannot run without numpy, torch
np = pytest.importorskip('numpy')
torch = pytest.importorskip('torch')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import osc_band_measure as obm  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "kq", os.path.join(HERE, "osc_band_kquant_a00-527993c5.py"))
kq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kq)


def test_head_var_selftest_passes():
    assert obm.selftest_head_var()


def test_16bit_quantizer_reproduces_logits():
    kq.CANDS = kq.candidates()
    torch.manual_seed(0)
    q, k = torch.randn(1, 2, 8, 64), torch.randn(1, 2, 8, 64)
    ref = q @ k.transpose(-1, -2)
    cls = np.zeros(kq.NPAIR, dtype=np.int64)
    kqk = kq.quantize_heads(k, [("pair", cls, [16])] * kq.KVD)
    rel = float((q @ kqk.transpose(-1, -2) - ref).abs().max() / ref.abs().max())
    assert rel < 1e-3, rel


def test_bits_accounting_toy():
    kq.CANDS = kq.candidates()
    c1 = [c for c in kq.CANDS if c["C"] == 1 and c["sizes"] == (32,) and c["widths"] == (4,)][0]
    assert abs(c1["bits"] - (c1["data"] + 0.25)) < 1e-12
    assert abs(c1["bits"] - (2 * 32 * 4 + 16) / 64.0) < 1e-12
    c2 = [c for c in kq.CANDS if c["sizes"] == (16, 16) and c["widths"] == (3, 2)][0]
    assert c2["C"] == 2
    assert abs(c2["data"] - 2.5) < 1e-12
    assert abs(c2["bits"] - (2 * (3 * 16 + 2 * 16) + 16 * 2) / 64.0) < 1e-12


def test_hook_quantizes_k_after_rope_q_untouched():
    seen = {}

    def fake_orig(q, k, cos, sin, unsqueeze_dim=1):
        seen["args"] = (q, k, unsqueeze_dim)
        return q, k

    rope = kq.make_rope(fake_orig)
    q, k = torch.randn(1, 2, 8, 64), torch.randn(1, 2, 8, 64)
    cls = np.zeros(kq.NPAIR, dtype=np.int64)
    alloc = [[("pair", cls, [2])] * kq.KVD]
    kq.CUR["l"] = 0
    kq.ALLOC["a"] = alloc
    qq, kk = rope(q, k, None, None)
    assert torch.equal(qq, q), "q was modified by the k-quant hook"
    assert not torch.equal(kk, k), "k was not quantized"
    assert seen["args"][0] is q and seen["args"][2] == 1
    kq.ALLOC["a"] = None
    _, kk2 = rope(q, k, None, None)
    assert torch.equal(kk2, k), "unquantized path changed k"


def test_wrong_pairing_is_caught():
    v = torch.arange(64).float().view(1, 1, 1, 64)
    pv = kq.pair_view(v)
    for p in range(kq.NPAIR):
        assert float(pv[0, 0, 0, p, 0]) == p
        assert float(pv[0, 0, 0, p, 1]) == p + kq.NPAIR
    # a consecutive-dims pairing would put dims (2p, 2p+1) together -> differs
    assert not torch.equal(pv[0, 0, 0, :, 0], v[0, 0, 0, 0::2])


def test_profiles_and_model_sha256():
    prov, rever, prof = kq.verify_hashes()
    assert prof == kq.PROF_SHA
    assert all(rever.values()), rever


if __name__ == "__main__":
    for name in sorted(n for n in globals() if n.startswith("test_")):
        print("==", name)
        globals()[name]()
    print("ALL SELFTESTS PASS")
