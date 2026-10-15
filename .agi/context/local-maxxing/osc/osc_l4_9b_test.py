"""Tests for osc_l4_9b.py (hypothesis:lm-l4-direct-head-windows-hold-on-the-served-9b). No model is loaded.

(1) head-window.patch applies cleanly to the pinned llama.cpp commit; (2) a synthetic mask for one windowed KV head
allows exactly {0..3} U {t-127..t} and leaves the other heads full causal, and the patch carries the same rule;
(3) the fresh-doc picker excludes the calibration docs and every runs 1-4 doc; (4) the KL parser reads
llama-perplexity's --kl-divergence output format.
"""
import json, os, subprocess, sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import osc_l4_9b as M  # noqa: E402

OUT = M.paths.get_local("osc_l4_9b_dir")
P = json.load(open(os.path.join(OUT, "params.json")))
PATCH = os.path.join(OUT, "head-window.patch")


def test_1_patch_applies_to_pinned_commit(tmp_path):
    repo = os.path.join(P["scratch"], "llama.cpp")
    if not os.path.isdir(repo):
        pytest.skip("no llama.cpp clone under params scratch (run build.sh)")
    src = subprocess.run(["git", "-C", repo, "show", f"{P['llama_cpp_sha']}:src/llama-graph.cpp"],
                         capture_output=True, check=True).stdout
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "llama-graph.cpp").write_bytes(src)
    r = subprocess.run(["git", "apply", "--check", "-v", PATCH], cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    r = subprocess.run(["git", "apply", PATCH], cwd=tmp_path, capture_output=True, text=True)
    assert r.returncode == 0 and b"head_window_cfg" in (tmp_path / "src" / "llama-graph.cpp").read_bytes()


def head_mask(n, windowed_kv, n_kvh, r, W, sinks):   # [q head][t] -> allowed key set, query head h reads KV h // r
    return [[{j for j in range(n) if (M.allowed(t, j, W, sinks) if h // r in windowed_kv else j <= t)}
             for t in range(n)] for h in range(n_kvh * r)]


def test_2_one_windowed_head_mask():
    n, W, s, nkv, r = 300, P["W"], P["sinks"], P["n_kv_heads"], 4
    m = head_mask(n, {1}, nkv, r, W, s)
    for h in range(nkv * r):
        for t in range(n):
            full = set(range(t + 1))
            want = (set(range(min(s, t + 1))) | set(range(max(0, t - W + 1), t + 1))) if h // r == 1 else full
            assert m[h][t] == want, (h, t)
    assert m[4][299] == {0, 1, 2, 3} | set(range(172, 300)) and len(m[4][299]) == 132
    assert m[0][299] == set(range(300)) and m[4][131] == set(range(132))
    text = open(PATCH).read()   # the patch implements the same rule and the same q-head -> KV-head grouping
    assert "(j < cfg.sinks || t - j < cfg.w) ? 0.0f : -INFINITY" in text
    assert "head_window().heads.count({il, (int) g})" in text and "g*r*kq->nb[2]" in text
    assert "int32_t w     = 128;" in text and "int32_t sinks = 4;" in text
    assert M.spec([0, 5, 31], P) == "3:0,7:1,31:3"
    assert P["n_heads"] == len(P["full_layers"]) * P["n_kv_heads"] == 32
    assert P["full_layers"] == [il for il in range(32) if (il + 1) % 4 == 0]


def test_3_picker_excludes_calibration_and_prior_docs():
    lens = [3000] * 40
    lens[2] = 100
    assert M.pick(lens, {0, 1, 12, 16, 18}, 3, 2064) == [3, 4, 5]
    assert M.pick(lens, set(range(40)), 3, 2064) == []
    ex = M.exclusions(P)
    assert set(P["calib_ids"]) <= ex and {0, 1, 3, 4, 5, 6, 7, 10, 13, 20, 21, 22, 24, 25, 28, 29, 31} <= ex
    assert M.pick([5000] * 60, ex, 3, 2064) == [i for i in range(60) if i not in ex][:3]
    if "fresh_docs" in P:
        F = [d for d, *_ in P["fresh_docs"]]
        assert not set(F) & ex and len(set(F)) == len(F) == P["n_fresh"]
        assert all(n >= P["ctx"] + P["margin"] for *_, n in P["fresh_docs"] + P["calib_docs"])
        A = M.articles(P)
        assert all(A[d][0] == t for d, t, _ in P["fresh_docs"] + P["calib_docs"])


SAMPLE = """chunk             PPL               ln(PPL(Q)/PPL(base))          KL Divergence              Δp RMS            Same top p
   1       7.2178 ±    0.2669       0.00412 ±    0.00118       0.00911 ±    0.00041     2.512 ±  0.109 %    96.774 ±  0.553 %

====== Perplexity statistics ======
Mean PPL(Q)                   :   7.217795 ±   0.266893
Mean PPL(base)                :   7.188108 ±   0.265427
Cor(ln(PPL(Q)), ln(PPL(base))):  99.83%
Mean ln(PPL(Q)/PPL(base))     :   0.004121 ±   0.001184

====== KL divergence statistics ======
Mean    KLD:   0.009110 ±   0.000410
Maximum KLD:   0.732611
99.9%   KLD:   0.412337

====== Token probability statistics ======
Same top p: 96.774 ± 0.553 %
"""


def test_4_kl_parser():
    assert M.parse_kl(SAMPLE) == {"kl": 0.00911, "same_top": 0.96774}
    assert M.parse_kl(SAMPLE.replace("0.009110", "-0.000000"))["kl"] == 0.0
    assert M.DONE.search(SAMPLE) and M.DONE.search("Final estimate: PPL = 7.1881 +/- 0.26543")
    assert not M.DONE.search("perplexity: calculating perplexity over 1 chunks")
    log = os.path.join(P["scratch"], "logs", f"zero_kl_{P['calib_ids'][0]}.log")
    if os.path.exists(log) and M.DONE.search(open(log, errors="ignore").read()):   # the real format, once run
        assert M.parse_kl(open(log, errors="ignore").read())["kl"] >= 0
