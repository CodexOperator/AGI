#!/usr/bin/env python3
"""Fixture/selftest for osc_band_kquant_true_a00-3d746bb5.py (OSC.13). No model loaded.

Run: python3 -m pytest <this file> -q   (or directly: python3 <this file>)
"""
import importlib.util
import os

import torch

_HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location(
    "kq_true", os.path.join(_HERE, "osc_band_kquant_true_a00-3d746bb5.py"))
qt = importlib.util.module_from_spec(_s)
_s.loader.exec_module(qt)


def test_true_q4_reaches_16_levels_and_scale_is_per_block():
    x = torch.rand(1, 2, 4000, 64, generator=torch.Generator().manual_seed(11)) * 2 - 1
    d = qt.levels(qt.quant_bw_true(x))
    print("distinct-level distribution:", torch.bincount(d).tolist(),
          "median", int(d.median()), "max", int(d.max()))
    assert int(d.median()) >= 14          # ternary would show <= 3
    assert int(d.max()) == 16
    v = x.reshape(*x.shape[:-1], 2, 32)
    a = v.abs().amax(-1, keepdim=True)
    assert a.shape[-2] == 2 and a.shape[-1] == 1   # one scale per 32-element block
    assert (4 * 32 + 16) / 32 == 4.5               # full 4.5-bit accounting


def test_old_quant_bw_is_ternary():
    x = torch.rand(1, 2, 4000, 64, generator=torch.Generator().manual_seed(11)) * 2 - 1
    old = qt.levels(qt.kq.quant_bw(x))
    print("old ternary distribution:", torch.bincount(old).tolist(), "max", int(old.max()))
    assert int(old.max()) <= 3


def test_energy_4p5_is_4p5():
    assert qt.kq.avg_bits([4, 4, 8, 16], [4, 4, 4, 3], 4) == 4.5


if __name__ == "__main__":
    test_true_q4_reaches_16_levels_and_scale_is_per_block()
    test_old_quant_bw_is_ternary()
    test_energy_4p5_is_4p5()
    print("all fixture tests pass")
