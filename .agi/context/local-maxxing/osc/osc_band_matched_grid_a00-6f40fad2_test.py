#!/usr/bin/env python3
"""Regression: the 64-pair key-only allocator must use all RoPE pairs."""
import importlib.util, os
import numpy as np

HERE = os.path.dirname(__file__)
spec = importlib.util.spec_from_file_location("sweep", os.path.join(HERE, "osc_band_sweep_a00-31ae16be.py"))
sweep = importlib.util.module_from_spec(spec); spec.loader.exec_module(sweep)


def test_qwen3_key_only_beats_random_on_energy_proxy():
    rng = np.random.default_rng(7)
    E = np.sort(rng.random((1, 1, 64)), axis=2)[:, :, ::-1]
    classes, widths = sweep.arms(E)["7p75"]
    p = classes[0][0].numpy()
    # The 64 RoPE pairs must all be represented by the four budget classes.
    assert np.bincount(p, minlength=4).tolist() == [16, 16, 32, 64]
    score = E[0, 0] / (1.0 + np.asarray(widths)[p])
    random_score = E[0, 0] / (1.0 + np.asarray(widths)[rng.integers(0, 4, 64)])
    assert score.sum() <= random_score.sum()
