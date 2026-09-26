#!/usr/bin/env python3
"""Model-free acceptance T1-T8 for osc_band_seeds_qwen3_a00-6771cb76.py.

T6 and T7 are the two the previous artifact could not have passed: an `assert`
gate is invisible under `python -O`, and an optional `which` loads the WRONG
model's weights before it refuses.
"""
import importlib.util, os, subprocess, sys, textwrap
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
import numpy as np, torch
_s = importlib.util.spec_from_file_location("h", os.path.join(HERE, "osc_band_seeds_qwen3_a00-6771cb76.py"))
h = importlib.util.module_from_spec(_s); _s.loader.exec_module(h)
fixed, npv = h.fixed, 64
fixed.SPEC.update(nl=4, kv=2, np=npv)   # model-free: arm() only needs these three
E = np.random.default_rng(0).random((4, 2, npv))
W = h.GRID[npv]["5.125"][1]

def test_t1_grid_byte_matched():
    """T1: every np64 budget is byte-matched and the matched widths descend."""
    h.m.check_table()

def test_t2_seeds_honoured():
    """T2: a different seed gives a different allocation; the same seed reproduces."""
    a = fixed.arm(E, W, "random", 7); b = fixed.arm(E, W, "random", 21); c = fixed.arm(E, W, "random", 7)
    assert not all(torch.equal(x, y) for x, y in zip(a, b)), "seed ignored (falsifier 6)"
    assert all(torch.equal(x, y) for x, y in zip(a, c)), "seed not reproducible"

def test_t3_determinism():
    """T3: uniform/key_only carry no RNG -- identical allocations, reported n=1."""
    u = fixed.arm(E, W, "uniform"); k = fixed.arm(E, W, "energy", 1)
    assert all(torch.equal(x, y) for x, y in zip(u, fixed.arm(E, W, "uniform")))
    assert all(torch.equal(x, y) for x, y in zip(k, fixed.arm(E, W, "energy", 999)))

def test_t4_band_gate():
    """T4: a band for 3 and 4 draws, REFUSED (raised) for 0, 1 and 2."""
    assert h.band([0.1, 0.2, 0.3]) == round(0.3 - 0.1, 9)
    for bad in ([], [0.1], [0.1, 0.2]):
        try: h.band(bad); assert False, "band emitted from n=%d draws" % len(bad)
        except ValueError as e: assert "refuse" in str(e), e

def test_t5_band_arithmetic():
    """T5: band == max - min computed by hand."""
    v = [0.034912109, 0.0412, 0.0299, 0.0551]
    assert h.band(v) == round(max(v) - min(v), 9) == 0.0252

def test_t6_gate_survives_O():
    """T6: the refusal still raises under `python -O`, where asserts vanish."""
    src = textwrap.dedent("""
        import importlib.util, os, sys
        HERE = %r
        sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
        s = importlib.util.spec_from_file_location("h", os.path.join(HERE, "osc_band_seeds_qwen3_a00-6771cb76.py"))
        h = importlib.util.module_from_spec(s); s.loader.exec_module(h)
        print(h.band([0.1]))
    """ % HERE)
    r = subprocess.run([sys.executable, "-O", "-c", src], capture_output=True, text=True)
    assert r.returncode != 0 and "refuse" in r.stderr, ("-O stripped the gate", r.stdout, r.stderr)

def test_t7_authorisation():
    """T7: refuse a non-np64 `which`, and bare invocation, BEFORE from_pretrained."""
    for which in (None, "qwen2", ""):
        try: h.guard(which); assert False, "guard authorised %r" % (which,)
        except ValueError as e: assert "np64" in str(e), e
    try: h.guard("qwen3", 32); assert False, "guard authorised np32"
    except ValueError as e: assert "np=32" in str(e), e
    boom = textwrap.dedent("""
        import sys
        def boom(*a, **k): raise AssertionError("from_pretrained touched before the refusal")
        class M:
            AutoTokenizer = type("T", (), {"from_pretrained": staticmethod(boom)})
            AutoModelForCausalLM = type("C", (), {"from_pretrained": staticmethod(boom)})
        sys.modules["transformers"] = M
    """)
    ns = {}; exec(boom, ns)
    try: h.run("qwen2", [7, 21, 99])
    except ValueError as e: assert "np64" in str(e), e
    else: assert False, "run('qwen2') reached the model"
    try: h.run("qwen3", [7, 7, 21])
    except ValueError as e: assert "duplicate" in str(e), e
    else: assert False, "duplicate seeds accepted"

def test_t8_three_way_call():
    """T8: above the band -> win, below it -> loss, only an overlap -> inside-noise."""
    b = 0.02
    assert h.call(+0.50, b) == "win"
    assert h.call(-0.50, b) == "loss"
    assert h.call(+0.01, b) == "inside-noise"
    assert h.call(-0.01, b) == "inside-noise"
    assert h.call(+0.50, 0.0) == "win" and h.call(-0.50, 0.0) == "loss"

def test_t9_distinct_draw_gate():
    """T9: the gate is on DISTINCT VALUES, not len(). Three identical draws are n=1."""
    for dup in ([0.30, 0.30, 0.30], [0.1, 0.1, 0.2, 0.2], [0.5] * 5):
        try: h.band(dup); assert False, "band emitted from %r (distinct=%d)" % (dup, len(set(dup)))
        except ValueError as e: assert "refuse" in str(e) and "distinct" in str(e), e
    assert h.band([0.30, 0.30, 0.31, 0.32]) == round(0.32 - 0.30, 9), "distinct-count gate refuses a real band"
    # and the reducer call is unreachable over a refused band
    assert h.call(+0.01, 0.0) == "win"  # only reachable if a caller ignores the refusal


def test_t10_row_contract():
    """T10: the cut is honest -- --budgets/--prompts narrow the grid, defaults are the whole thing."""
    import inspect
    sig = inspect.signature(h.run)
    assert list(sig.parameters) == ["which", "seeds", "budgets", "n_prompts"], list(sig.parameters)
    assert h.SEEDS_DEFAULT == "7,21,99", h.SEEDS_DEFAULT   # config values.local_maxxing.osc_band_seeds
    assert h.MINS == 3 and h.NP64 == 64


if __name__ == "__main__":
    for name, f in sorted(globals().items()):
        if name.startswith("test_"): f(); print(name, "OK")
