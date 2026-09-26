"""Acceptance tests for byte-matched uniform and mirrored band allocations."""
import importlib.util, os
import numpy as np
P = os.path.dirname(__file__)
S = importlib.util.spec_from_file_location("matched", os.path.join(P, "osc_band_matched_uniform_a00-a721f95f.py"))
m = importlib.util.module_from_spec(S); S.loader.exec_module(m)

def test_budget_table_is_equal_and_energy_order_is_descending(capsys):
    m.check_table()
    out = capsys.readouterr().out
    assert out.count("OK") == 8

def test_inverse_energy_is_mirror_complement_and_uniform_is_one_class():
    m.fixed.SPEC = {"nl": 1, "kv": 1, "np": 8}
    E = np.arange(8, dtype=float)[None, None, :]
    a = m.fixed.arm(E, [2, 2, 1, 1], "energy", 1)[0].numpy()
    inv = m.fixed.arm(-E, [2, 2, 1, 1], "energy", 1)[0].numpy()
    assert np.array_equal(a[:, ::-1], inv)
    u = m.fixed.arm(E, [2], "uniform")[0].numpy()
    assert u.shape == (1, 16) and np.all(u == 0)
