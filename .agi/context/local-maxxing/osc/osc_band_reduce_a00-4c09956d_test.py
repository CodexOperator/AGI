#!/usr/bin/env python3
"""Model-free acceptance for osc_band_reduce_a00-4c09956d.py.

T9 is the falsifier-10 gate: a band from three IDENTICAL draws must be REFUSED,
and the refusal must say WHICH quantity was short. T10 proves it under `python -O`.
T11/T12 are the reducer's aggregation shape: the ALLOCATION band (one mean per
seed) must not swallow the per-prompt SAMPLING spread.
"""
import importlib.util, os, subprocess, sys, textwrap
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]

def _mod(name):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    h = importlib.util.module_from_spec(s); s.loader.exec_module(h); return h

h = _mod("osc_band_reduce_a00-4c09956d")

def rows(pairs, budget=4.125):
    return [dict(model="qwen3", np=64, budget=budget, cell="%s/%s/%s" % (budget, a, s), arm=a, seed=s,
                 n=1 if a != "random" else 3, arm_is_stochastic=(a == "random"), prompt=i, widths=[1],
                 agree=g, kl=0.5) for (a, s, g) in pairs for i, g in enumerate([g, g])]

def test_t9_distinct_value_gate():
    """T9: band([0.30]*3) is REFUSED and the message names DISTINCT, not n."""
    for bad in ([0.30, 0.30, 0.30], [0.3, 0.3, 0.3000000000001]):
        try:
            h.band(bad); assert False, "band emitted from %r" % bad
        except ValueError as e:
            assert "DISTINCT" in str(e) and "n=3" in str(e), e
    # the n= refusal keeps its OWN wording, so the two are never confused
    try:
        h.band([0.1, 0.2]); assert False
    except ValueError as e:
        assert "n=2" in str(e) and "DISTINCT" not in str(e), e
    assert h.band([0.1, 0.2, 0.3]) == round(0.3 - 0.1, 9)

def test_t10_gate_survives_O():
    """T10: the refusal still raises under `python -O`, and cannot be caught to 0.0."""
    src = textwrap.dedent("""
        import importlib.util, os, sys
        HERE = %r
        sys.path[:0] = [os.path.join(os.getcwd(), ".agi/context/local-maxxing"), HERE]
        s = importlib.util.spec_from_file_location("h", os.path.join(HERE, "osc_band_reduce_a00-4c09956d.py"))
        h = importlib.util.module_from_spec(s); s.loader.exec_module(h)
        print("band", h.band([0.30, 0.30, 0.30]))
    """ % HERE)
    r = subprocess.run([sys.executable, "-O", "-c", src], capture_output=True, text=True, cwd=os.getcwd())
    assert r.returncode != 0 and "DISTINCT" in r.stderr, ("-O stripped or softened the gate", r.stdout, r.stderr)

def test_t11_allocation_band_is_per_seed():
    """T11: the allocation band is the spread of SEED MEANS; per-prompt spread is not folded in."""
    r = rows([("random", 7, 0.60), ("random", 21, 0.65), ("random", 99, 0.62),
              ("key_only", 0, 0.63), ("uniform", 0, 0.61)])
    sm = h.seed_means(r)
    assert sm == {7: 0.60, 21: 0.65, 99: 0.62}, sm
    assert h.band(list(sm.values())) == round(0.05, 9)

def test_t12_contract_rows_and_call_rule():
    """T12: per-prompt rows aggregate into the contract row, and call2 judges the aggregate."""
    r = rows([("random", 7, 0.60), ("random", 21, 0.65), ("random", 99, 0.62),
              ("key_only", 0, 0.66), ("uniform", 0, 0.61)])
    agg = h.aggregate(r)
    assert len(agg) == 5, agg
    for a in agg:
        assert (a["n"] == 3) if a["arm"] == "random" else (a["n"] == 1), a
        assert "arm_is_stochastic" in a and "widths" in a
    verdicts = h.c2.judge([a for a in agg if a["arm"] != "random" or a["budget"] == 4.125], "key_only", "uniform")
    w = [v for k, v in verdicts.items() if k[2] == 4.125 and k[5] == "agree"]
    assert w and w[0][0] in ("win", "loss", "inside-noise"), verdicts

def test_t13_stub_arm_is_refused_end_to_end():
    """T13: a jsonl whose three random seeds returned the SAME agree refuses to band."""
    r = rows([("random", 7, 0.60), ("random", 21, 0.60), ("random", 99, 0.60),
              ("key_only", 0, 0.63), ("uniform", 0, 0.61)])
    band, why = h.c2.band(h.c2.cells(h.aggregate(r))[(("qwen3", 64, 4.125))], "agree")
    assert band is None and "degenerate" in why, (band, why)
    try:
        h.band(list(h.seed_means(r).values())); assert False
    except ValueError as e:
        assert "DISTINCT" in str(e)
