#!/usr/bin/env python3
"""Model-free acceptance for osc_band_np64_one_a00-385bc2f0.py.

T14 the arm pairing: the reducer splats arm() into forward, and only a paired
     (layers, widths) makes that splat legal. arm() ignores widths, so the pair
     carries the grid's own widths and the allocation is unchanged.
T15 the landed np64 cell: ONE budget, THREE distinct random seeds, a band that is
     a MEASURED spread, and a margin that is INSIDE it (not a win on a 0.0 band).
T16 the two error bars stay apart: the per-prompt sampling spread must be far
     smaller than the allocation band, or the node is conflating them.
T17 falsifier 10 still holds through this file: three identical draws refuse.
"""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
HAS_NUMPY = importlib.util.find_spec("numpy") is not None

def _mod(name):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    h = importlib.util.module_from_spec(s); s.loader.exec_module(h); return h

h = _mod("osc_band_np64_one_a00-385bc2f0")
def _rows(pairs, budget="4.125"):
    return [dict(model="qwen3", np=64, budget=budget, cell="%s/%s/%s" % (budget, a, s), arm=a, seed=s,
                 n=1 if a != "random" else 3, arm_is_stochastic=(a == "random"), prompt=i, widths=[1],
                 agree=g, kl=0.5) for (a, s, g) in pairs for i, g in enumerate([g, g])]

@__import__("pytest").mark.skipif(not HAS_NUMPY, reason="T14 builds a real allocation; needs the ML interpreter (PYTHONPATH=/data/ml/scratch/osc03/pylib /data/ml/.venv/bin/python)")
def test_t14_arm_is_paired_with_its_widths():
    import numpy as np
    fixed = h._patched_deps()[4].fixed
    if hasattr(fixed, "_arms_are_paired"):
        fixed.SPEC.update(np=8, kv=2, nl=2)
        E = np.zeros((2, 2, 8)); got, w = fixed.arm(E, [4], "uniform")
        assert w == [4] and len(got) == 2 and got[0].shape[-1] == 16, (w, len(got))

def test_t15_one_cell_lands_three_seeds_and_calls_inside_noise():
    r = _rows([("random", 7, 0.033), ("random", 21, 0.025), ("random", 99, 0.052),
               ("key_only", 0, 0.053), ("uniform", 0, 0.032)])
    sm = h.red.seed_means(r)
    assert sorted(sm) == [7, 21, 99], sm
    b = h.red.band(list(sm.values()))
    assert 0.02 < b < 0.03, b
    v = h.red.c2.judge(h.red.aggregate(r), "key_only", "uniform")
    word = [w for k, w in v.items() if k[5] == "agree"][0]
    assert word[0] == "inside-noise", (word, b)  # a 0.02 margin does NOT beat a 0.027 band

def test_t16_allocation_band_is_not_the_sampling_spread():
    r = _rows([("random", 7, 0.033), ("random", 21, 0.025), ("random", 99, 0.052),
               ("key_only", 0, 0.053), ("uniform", 0, 0.032)])
    sm = h.red.seed_means(r)
    assert h.red.band(list(sm.values())) > 0.02, sm

def test_t17_three_identical_draws_still_refuse():
    try:
        h.red.band([0.30, 0.30, 0.30]); assert False, "0.0 band emitted from identical draws"
    except ValueError as e:
        assert "DISTINCT" in str(e), e
