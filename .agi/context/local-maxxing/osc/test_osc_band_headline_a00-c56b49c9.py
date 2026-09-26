"""Acceptance for the ONE-command band headline (hypothesis:band-headline-reproducer).
Zero model, zero torch, zero network: system python3 only."""
import importlib.util
import os
from collections import Counter

import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]   # collect from any cwd


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m = _load("osc_band_headline_a00-c56b49c9")

BUDGETS = ("4.25", "5.25", "6.25", "7.25")


def _words(h, comp, metric):
    return {b: h[comp][(b, "key_only", comp, metric)][0] for b in BUDGETS}


def test_join_shape_is_the_pre_registered_one():
    rows = m.join()
    assert len(rows) == 12 + 12  # 16 grid rows - 4 unseeded random, + 12 seeded
    randoms = [d for d in rows if d["arm"] == "random"]
    assert len(randoms) == 12 and {d["seed"] for d in randoms} == {7, 21, 99}
    assert all("seed" in d for d in randoms)


def test_key_only_vs_uniform_is_0_win_1_loss_3_inside_noise_on_both_metrics():
    h = m.headline()
    for metric in ("agree", "kl"):
        c = Counter(_words(h, "uniform", metric).values())
        assert c == Counter({"inside-noise": 3, "loss": 1}), (metric, c)
        assert _words(h, "uniform", metric)["4.25"] == "loss"


def test_key_only_vs_random_agree_wins_at_4p25_6p25_7p25():
    w = _words(m.headline(), "random", "agree")
    assert [b for b in BUDGETS if w[b] == "win"] == ["4.25", "6.25", "7.25"]


def test_no_cell_is_unresolved_in_either_comparator():
    t = m.tally(m.headline())
    for comp in ("uniform", "random"):
        assert t[comp]["unresolved"] == 0, (comp, t[comp])


def test_dropping_the_unseeded_row_is_what_makes_the_band_earnable():
    """Falsifier for the join: keep the grid's n=1 random row and every cell refuses."""
    root = m.paths.get_local("osc_band_qknorm_dir")
    grid = m.rows(root, m.GRID_RUN)
    kept = grid + m.rows(root, m.SEEDS_RUN)
    j = m.rule().judge(kept, "key_only", "uniform")
    assert {v[0] for v in j.values()} == {"unresolved"}
    assert all("no seed" in v[1] for v in j.values()), j


def test_the_module_stays_zero_model():
    src = open(os.path.join(HERE, "osc_band_headline_a00-c56b49c9.py")).read()
    for bad in ("torch", "transformers", "urllib", "requests", "http"):
        assert bad not in src, bad
    assert m.join() and m.tally(m.headline())
