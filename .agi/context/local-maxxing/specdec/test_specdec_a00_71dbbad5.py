#!/usr/bin/env python3
"""Selftest for specdec_a00_71dbbad5.py -- fixtures only, no GPU, no server.
Covers: the prompt builder's determinism, the paired speedup/interval math on a toy table, the
divergence finder on toy token strings, and the arm invariant (each --spec-type arm differs from
none ONLY in server flags/name/log path, never in the request body)."""
import hashlib
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".agi/config.json")): ROOT = os.path.dirname(ROOT)
spec = importlib.util.spec_from_file_location("sdr", os.path.join(HERE, "specdec_a00_71dbbad5.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)


def test_prompts_deterministic_and_committed():
    a = mod.prompts_jsonl(); b = mod.prompts_jsonl()
    assert a == b and len(a.splitlines()) == 24
    p = mod.OUT + "/prompts.jsonl"
    if os.path.exists(p):   # byte-identical to the committed artifact
        assert hashlib.sha256(open(p, "rb").read()).hexdigest() == hashlib.sha256(a.encode()).hexdigest()


def test_paired_math_on_toy_table():
    base = [{"decode_tps": 100.0} for _ in range(24)]
    faster = [{"decode_tps": 130.0} for _ in range(24)]
    r = mod.paired(base, faster)
    assert r["n"] == 24 and r["median_speedup"] == 1.3 and r["clears_one"] and r["reaches_1p3"]
    same = mod.paired(base, [{"decode_tps": 100.0} for _ in range(24)])
    assert same["median_speedup"] == 1.0 and not same["clears_one"] and not same["reaches_1p3"]
    noisy = mod.paired(base, [{"decode_tps": 100.0 + (10 if i % 2 else -10)} for i in range(24)])
    assert noisy["speedup_lo"] < 1.0 < noisy["speedup_hi"]
    assert mod.paired(base[:1], faster[:1])["error"] == "too few"


def test_divergence_finder():
    assert mod.fdiff("abc", "abc") == -1
    assert mod.fdiff("abc", "abd") == 2
    assert mod.fdiff("abc", "abcd") == 3


def test_arms_differ_only_in_flags():
    n = mod.cargs("none", 19000); s = mod.cargs("ngram-simple", 19000)
    d = [i for i, (x, y) in enumerate(zip(n, s)) if x != y]
    assert [n[i] for i in d] == ["sd_none", "none", "/out/logs/sd_none.log"]      # name, spec-type, log
    assert [s[i] for i in d] == ["sd_ngram-simple", "ngram-simple", "/out/logs/sd_ngram-simple.log"]
    assert n[n.index("--spec-type") + 1] == "none" and s[s.index("--spec-type") + 1] == "ngram-simple"
    b = mod.rbody("prompt text", 64)   # no arm parameter exists: the request body is arm-invariant
    assert b == mod.rbody("prompt text", 64) and b["temperature"] == 0
    assert b["chat_template_kwargs"] == {"enable_thinking": False} and b["model"] == "Qwen3.5-9B-Q4_K_M"


if __name__ == "__main__":
    for k, v in sorted(globals().items()):
        if k.startswith("test_"): v(); print("ok", k)
