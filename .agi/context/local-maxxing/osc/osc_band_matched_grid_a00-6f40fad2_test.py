#!/usr/bin/env python3
"""Regression: the 64-pair key-only allocator must use all RoPE pairs."""
import importlib.util, os
import numpy as np

HERE = os.path.dirname(__file__)
spec = importlib.util.spec_from_file_location("sweep", os.path.join(HERE, "osc_band_sweep_a00-31ae16be.py"))
sweep = importlib.util.module_from_spec(spec); spec.loader.exec_module(sweep)


def test_qwen3_key_only_beats_random_on_energy_proxy():
    rng = np.random.default_rng(7)
    E = np.arange(64, 0, -1, dtype=float).reshape(1, 1, 64)
    classes, widths = sweep.arms(E)["7p75"]
    p = classes[0][0].numpy()
    # RoPE applies one class per pair to both duplicated channel halves.
    assert np.array_equal(p[:64], p[64:])
    assert np.bincount(p[:64], minlength=4).tolist() == [8, 8, 16, 32]
    # Compare at the 64-pair level, not the duplicated 128-channel shape.
    pair_energy = E[0, 0]
    score = pair_energy / (1.0 + np.asarray(widths)[p[:64]])
    random_score = pair_energy / (1.0 + np.asarray(widths)[rng.integers(0, 4, 64)])
    assert score.sum() <= random_score.sum()


def test_qwen2_key_only_shape_is_not_regressed():
    rng = np.random.default_rng(0)
    E = np.arange(32, 0, -1, dtype=float).reshape(1, 1, 32)
    classes, widths = sweep.arms(E)["7p75"]
    p = classes[0][0].numpy()
    assert np.array_equal(p[:32], p[32:])
    assert np.bincount(p[:32], minlength=4).tolist() == [4, 4, 8, 16]
    score = E[0, 0] / (1.0 + np.asarray(widths)[p[:32]])
    random_score = E[0, 0] / (1.0 + np.asarray(widths)[rng.integers(0, 4, 32)])
    assert score.sum() <= random_score.sum()
