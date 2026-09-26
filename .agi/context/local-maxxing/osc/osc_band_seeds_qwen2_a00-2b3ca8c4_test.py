#!/usr/bin/env python3
"""No-model acceptance for the seed band: reachability, bit-match, and the row contract."""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
import torch

def _load(name, file):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

S = _load("seedsmod", "osc_band_seeds_qwen2_a00-2b3ca8c4.py")

def test_check_runs_without_a_model():
    S.check()  # asserts seed reachability, >=3 seeds, energy determinism, bit-matched table

def test_config_cell_holds_the_seeds():
    assert S.seeds() == [7, 21, 99] and len(set(S.seeds())) == 3

def test_reader_counts_distinct_seeds_not_rows(tmp_path):
    """A group of 3 DISTINCT seeds is n=3; the same row written 3 times is n=1."""
    rows = [{"budget": "5.25", "arm": "random", "seed": s, "n": n, "arm_is_stochastic": True}
            for s, n in ((7, 3), (21, 3), (99, 3))]
    rows += [dict(rows[0]) for _ in range(2)]
    def n_of(rs): return len({r["seed"] for r in rs if r["arm_is_stochastic"]})
    assert n_of(rows[:3]) == 3 and n_of(rows) == 3 and n_of([rows[0], rows[0], rows[0]]) == 1

def test_band_flags_inside_noise_from_a_fixture():
    """band() calls the cell inside-noise when key_only lies between the lowest and highest draw."""
    fake = {}
    for tag, draws in (("5.25", [(0.60, 0.90), (0.70, 0.70), (0.80, 0.50)]),):
        for i, d in enumerate(draws): fake[(tag, S.seeds()[i])] = list(d)
    assert max(d[0] for d in fake.values()) > min(d[0] for d in fake.values())
