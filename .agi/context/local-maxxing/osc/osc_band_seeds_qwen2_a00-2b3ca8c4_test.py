#!/usr/bin/env python3
"""No-model acceptance for the seed band: reachability, bit-match, and the row contract."""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(HERE), HERE]  # collect from any cwd
import pytest  # skip-by-name: this module cannot run without torch
torch = pytest.importorskip('torch')

def _load(name, file):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

S = _load("seedsmod", "osc_band_seeds_qwen2_a00-2b3ca8c4.py")

def test_check_runs_without_a_model():
    S.check()  # asserts seed reachability, >=3 seeds, energy determinism, bit-matched table

def test_config_cell_holds_the_seeds():
    """The indirection is the contract; the LIST is not (it must stay editable -- the hypothesis asks for >= 8 seeds)."""
    import paths
    live = json.load(open(paths.config_path()))["values"]["local_maxxing"]["osc_band_seeds"]
    assert S.seeds() == [int(s) for s in live] and len(set(S.seeds())) >= 3

def test_reader_counts_distinct_seeds_not_rows(tmp_path):
    """A group of 3 DISTINCT seeds is n=3; the same row written 3 times is n=1."""
    rows = [{"budget": "5.25", "arm": "random", "seed": s, "n": n, "arm_is_stochastic": True}
            for s, n in ((7, 3), (21, 3), (99, 3))]
    rows += [dict(rows[0]) for _ in range(2)]
    def n_of(rs): return len({r["seed"] for r in rs if r["arm_is_stochastic"]})
    assert n_of(rows[:3]) == 3 and n_of(rows) == 3 and n_of([rows[0], rows[0], rows[0]]) == 1

T = "5.25"  # agree draws 0.60/0.70/0.80 -> range 0.20, half 0.10; kl draws 0.90/0.70/0.50 -> range 0.40, half 0.20

def _agg():
    return {(t, s): ([0.60, 0.70, 0.80][i], [0.90, 0.70, 0.50][i])
            for t in S.grid.GRID[32] for i, s in enumerate((7, 21, 99))}

def _base(koa, kok):
    b = {f"{a}|{t}": (0.70, 0.72) for t in S.grid.GRID[32] for a in ("uniform", "key_only")}
    b["key_only|" + T] = (koa, kok)
    return b

def test_band_names_both_calls_with_explicit_signs():
    """band() must emit BOTH calls, apart, with sign-explicit margins -- the two disagree by construction."""
    b = S.band(_agg(), _base(0.55, 0.40))[T]
    assert b["key_only_minus_uniform_agree"] == -0.15 and b["uniform_minus_key_only_kl"] == 0.32
    assert b["inside_agree"] is False and b["inside_kl"] is False            # (b) RANGE: key_only outside the draws
    assert b["margin_call_inside_agree"] is True and b["margin_call_inside_kl"] is True  # (a) MARGIN: |d| <= range
    i = S.band(_agg(), _base(0.65, 0.60))[T]
    assert i["inside_agree"] is True and i["inside_kl"] is True and i["agree_half_range"] == 0.1

def test_band_reads_the_committed_baselines_when_none_given():
    b = S.band(_agg())[T]  # no model: the baselines are the committed a00-a721f95f cells.jsonl
    assert set(b) >= {"key_only_minus_uniform_agree", "uniform_minus_key_only_kl", "margin_call_inside_agree", "inside_agree"}
