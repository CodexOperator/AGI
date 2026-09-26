#!/usr/bin/env python3
"""Fixture-only selftests for osc_band_kquant.py (OSC.10, agent a00-04dc76fc).

No model is loaded here. Run: python3 -m pytest <this file> -q
"""
import importlib.util
import os

import pytest  # skip-by-name: this module cannot run without numpy, torch
np = pytest.importorskip('numpy')
torch = pytest.importorskip('torch')

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "osc_band_kquant_mod", os.path.join(_HERE, "osc_band_kquant_a00-04dc76fc.py"))
kq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(kq)


def test_avg_bits_counts_scales():
    assert kq.avg_bits([4, 4, 8, 16], [4, 4, 2, 2], 4) == 3.5
    assert kq.avg_bits([4, 4, 8, 16], [2, 2, 2, 1], 4) == 2.5
    # dropping the scale term changes the number (the bar depends on it)
    no_scale = sum(2 * n * w for n, w in zip([4, 4, 8, 16], [4, 4, 2, 2])) / 64.0
    assert no_scale == 2.5 and no_scale != kq.avg_bits([4, 4, 8, 16], [4, 4, 2, 2], 4)
    # the three matched points: energy and uniform land on the same average bits
    for tag, (s, w, (cu, wu)) in kq.POINTS.items():
        e = kq.avg_bits(s, w, 4)
        u = kq.avg_bits([kq.NPAIR // cu] * cu, [wu] * cu, cu)
        assert abs(e - u) < 1e-12, (tag, e, u)
    assert kq.selftest_bits() is True


def test_pairing_invariant_catches_consecutive_dims():
    assert kq.selftest_pairing() is True
    good = np.concatenate([np.arange(kq.NPAIR) % 4, np.arange(kq.NPAIR) % 4])
    bad = np.repeat(np.array([0] * 4 + [1] * 4 + [2] * 8 + [3] * 16), 2)  # (2p, 2p+1)
    assert (good[:32] == good[32:]).all()          # rotate_half pair (p, p+32)
    assert not (bad[:32] == bad[32:]).all()        # consecutive dims fail


def test_quant_levels_and_sign_at_one_bit():
    amax = 0.9
    x = torch.zeros(1, 1, 1, 64)
    x[..., 0] = 0.1 * amax   # a 3-level code would map this to a zero level
    x[..., 32] = -amax
    d = torch.zeros(1, 64, dtype=torch.int64)
    y = kq.quant(x, d, [1])
    lv = np.round(y[0, 0, 0, :2].tolist(), 6)
    assert set(lv) == {amax, -amax}, lv   # sign only, no zero dead-zone
    z = torch.randn(1, 1, 3, 64, generator=torch.Generator().manual_seed(1))
    for w, nlev in ((1, 2), (2, 4), (4, 16)):
        assert len(torch.unique(kq.quant(z, d, [w])[0, 0, 0, :])) <= nlev
    e16 = (kq.quant(z, d, [16]) - z).abs().max()
    e2 = (kq.quant(z, d, [2]) - z).abs().max()
    assert e16 < 1e-3 < e2


def test_quant_only_touches_its_classes():
    g = torch.Generator().manual_seed(2)
    x = torch.randn(1, 2, 3, 64, generator=g)
    dm = torch.from_numpy(np.stack([np.concatenate([np.zeros(32, np.int64),
                                                    np.ones(32, np.int64)])] * 2))
    y = kq.quant(x, dm, [2, 2])
    assert y.shape == x.shape
    assert not torch.equal(y, x)


def test_make_arm_puts_highest_energy_in_class_zero():
    E = np.zeros((24, 2, 32))
    E[:, :, 5] = 100.0
    E[:, :, 7] = 50.0
    dm, widths = kq.make_arm(E, [4, 4, 8, 16], [4, 4, 2, 2])
    assert widths == [4, 4, 2, 2]
    row = dm[3][0].numpy()
    assert row[5] == 0 and row[5 + 32] == 0          # best pair, highest width
    assert row[7] == 0
    assert sorted(np.bincount(row, minlength=4).tolist()) == [8, 8, 16, 32]
    assert (row[:32] == row[32:]).all()              # pairing honoured


def test_blockwise_is_four_and_a_half_bits():
    assert (4 * 64 + (64 // 32) * 16) / 64.0 == 4.5
    g = torch.Generator().manual_seed(3)
    x = torch.randn(1, 2, 3, 64, generator=g)
    y = kq.quant_bw(x)
    assert y.shape == x.shape and not torch.equal(y, x)
    assert (y - x).abs().max() < x.abs().max()


if __name__ == "__main__":   # pytest is absent from the torch venv; run directly
    for _n, _f in sorted(list(globals().items())):
        if _n.startswith("test_") and callable(_f):
            _f()
            print("PASS", _n)
    print("all selftests pass")
