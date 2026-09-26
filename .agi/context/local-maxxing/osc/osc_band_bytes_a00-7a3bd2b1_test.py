"""Emitted-bit audit tests: the count is taken from the real quant() call."""
import importlib.util, os
import numpy as np, torch
P = os.path.dirname(os.path.abspath(__file__))
def _load(name, fn):
    s = importlib.util.spec_from_file_location(name, os.path.join(P, fn))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
fixed = _load("fixed", "osc_band_kquant_qknorm_a00-bcb6c85e.py")
b = _load("bytes", "osc_band_bytes_a00-7a3bd2b1.py")

def spec(np_=32, kv=2, nl=1):
    S = {"np": np_, "kv": kv, "nl": nl, "nh": 8, "group": 4}
    fixed.SPEC = b.fixed.SPEC = S

def test_emitted_bits_equal_bits_for_every_grid_arm_at_both_np():
    for np_ in (32, 64):
        spec(np_)
        g = b.grid()
        for name, w in g.items():
            rows = b.audit(torch.randn(1, 2, 2, 2 * np_), fixed.arm(np.ones((1, 2, np_)), w)[0], w)
            assert all(r["emitted_bits"] == fixed.bits(w) * 2 * np_ for r in rows), (np_, name, rows[0])
        for w in ([3], [2], [9]):
            rows = b.audit(torch.randn(1, 2, 2, 2 * np_), fixed.arm(np.ones((1, 2, np_)), w, "uniform")[0], w)
            assert rows[0]["emitted_bits"] == fixed.bits(w) * 2 * np_ and rows[0]["n_scales"] == 1

def test_narrow_class_carries_32_payload_bits_under_one_16_bit_scale():
    spec()
    w = [4, 4, 3, 3]                       # the band arm at the np32 4.25 budget
    assert round(fixed.bits(w), 4) == 4.25
    r = b.audit(torch.randn(1, 2, 2, 64), fixed.arm(np.ones((1, 2, 32)), w)[0], w)[0]
    # the mask spans the FULL head_dim (2*np channels, a RoPE pair per half), so a
    # nominal class of 4 pairs shows up as 8 channels and costs 8*4 = 32 payload bits.
    assert r["n_scales"] == 4 and r["emitted_bits"] == 4.25 * 64
    assert r["class_channels"] == [8, 8, 16, 32] and r["class_channels"][0] * 4 == 32
    u = b.audit(torch.randn(1, 2, 2, 64), fixed.arm(np.ones((1, 2, 32)), [2], "uniform")[0], [2])[0]
    assert round(100 * 16 * u["n_scales"] / (u["emitted_bits"] - 16), 4) == 12.5   # np32 uniform 2-bit
    spec(64)
    u64 = b.audit(torch.randn(1, 2, 2, 128), fixed.arm(np.ones((1, 2, 64)), [2], "uniform")[0], [2])[0]
    assert round(100 * 16 / (u64["emitted_bits"] - 16), 4) == 6.25                # the 6.25 pct reference

def test_an_empty_class_is_counted_as_no_scale_not_as_a_nominal_one():
    spec()
    dm = torch.zeros((1, 32), dtype=torch.long)   # every channel in class 0: classes 1..3 empty
    r = b.audit(torch.randn(1, 2, 2, 64), dm, [3, 3, 3, 3])[0]
    assert r["n_scales"] == 1 and r["emitted_bits"] == 32 * 3 + 16
    assert r["emitted_bits"] != fixed.bits([3, 3, 3, 3]) * 64     # bits() would have said 4.00

def test_counter_wraps_the_shipped_quant_without_replacing_it():
    spec()
    real = b.fixed.quant
    wrapped = b.instrument()
    assert b.fixed.quant is not real and wrapped is real
    k = torch.randn(1, 2, 2, 64); a = b.fixed.arm(np.ones((1, 2, 32)), [4, 4, 3, 3])[0]
    b.STATE["rows"] = []
    out = b.fixed.quant(k, a, [4, 4, 3, 3])
    assert out.shape == k.shape and b.STATE["rows"] and b.STATE["rows"][0]["emitted_bits"] == 4.25 * 64
    b.fixed.quant = real
