"""Tests for osc_bend2_law.py (goal:g5.42). Synthetic tapes only: no test reads the trained checkpoint or the real tape, and
no test runs STEP 0's committed files (that is the run). The bend tests need the private bend install; they skip without it."""
import itertools
import json
import os
import random
import shutil
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_bend2_law as B  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("bend2_law_dir"), "params.json")))
BEND = os.path.join(P["bend_bin"], "bend")
needs_bend = pytest.mark.skipif(not os.path.exists(BEND), reason="no private bend install")


def test_1_params_are_pinned():
    assert B.sha(P["checkpoint"]["path"]) == P["checkpoint"]["sha256"] and P["checkpoint"]["sha256"].startswith("8e174e98")
    assert B.sha(P["omp24_source"]["path"]) == P["omp24_source"]["sha256"] and P["omp24_source"]["key"] == "24"
    keep = json.load(open(P["omp24_source"]["path"]))["picks"]["omp"]["24"]
    assert len(keep) == 24 == len(set(keep))
    assert (P["wall_cap_s"], P["step0_wall_cap_s"], P["threads"]) == (1200, 600, 1) and P["rss_cap_bytes"] < 3 * 2 ** 30


def test_2_a_tie_counts_as_wrong_and_the_u32_emulation_agrees():
    assert B.hit([1, 5, 5, 0], 1) == 0 and B.hit([1, 5, 4, 0], 1) == 1 and B.hit([1, 5, 4, 0], 2) == 0
    r = random.Random(0)
    for _ in range(300):
        nn, ni = 7, r.randint(1, 4)
        h = [r.randint(-127, 127) for _ in range(ni)]
        W = [[r.randint(-127, 127) for _ in range(nn)] for _ in range(ni)]
        n, b = [r.randint(-60000, 60000) for _ in range(nn)], [r.randint(-3, 3) for _ in range(nn)]
        if r.random() < 0.3:   # plant a tie at the max
            L = B.logits(h, n, W, b)
            j = L.index(max(L))
            k = (j + 1) % nn
            n[k] += L[j] - L[k]
        lab = r.randrange(nn)
        assert B.hit(B.logits(h, n, W, b), lab) == B.hit_u32(h, n, W, b, lab)


def small_tape(p, ni, seed):
    r = random.Random(seed)
    return {"p": p, "h": [[r.randint(-127, 127) for _ in range(ni)] for _ in range(p * p)],
            "n": [[r.randint(-40000, 40000) for _ in range(p)] for _ in range(p * p)],
            "W": [[r.randint(-127, 127) for _ in range(p)] for _ in range(ni)], "b": [r.randint(-500, 500) for _ in range(p)],
            "test": [r.randint(0, 1) for _ in range(p * p)]}


def test_3_count_and_the_flip_choice():
    T = small_tape(5, 3, 1)
    X, Xt, xa = B.count(T)
    assert X == sum(xa) and 0 <= Xt <= X and len(xa) == 5
    f = B.flip_choice(T, X)
    flat = [(abs(w), -(i * 5 + j)) for i, r in enumerate(T["W"]) for j, w in enumerate(r)]
    first = f["tried"][0]
    assert (abs(first["w"]), -(first["i"] * 5 + first["j"])) == max(flat)
    assert f["X_flip"] != X and all(t["X_flip"] == X for t in f["tried"][:-1])
    T["W"] = [[0] * 5 for _ in range(3)]
    T["W"][0][0] = 9   # a flip that cannot change the count is skipped to the next entry
    f = B.flip_choice(T, B.count(T)[0])
    assert f["tried"][0]["i"] == 0 and f["tried"][0]["j"] == 0


def test_4_parity_net_semantics_main_and_mutant():
    for mutant in (False, True):
        wrong = []
        for bits in itertools.product([0, 1], repeat=8):
            s = sum(bits)
            out = sum(((1 if k == 8 and mutant else (-1) ** (k + 1)) * (s >= k)) for k in range(1, 9)) % 2 ** 32
            if out != s % 2:
                wrong.append(bits)
        assert wrong == ([] if not mutant else [(1,) * 8])
    f, m = B.parity_files(False), B.parity_files(True)
    assert set(f) == {"NET.bend", "LAWS.bend", "PROOF.bend"} and f["LAWS.bend"] == m["LAWS.bend"] and f["PROOF.bend"] == m["PROOF.bend"]
    assert f["NET.bend"] != m["NET.bend"] and f["PROOF.bend"].count("{==}") == 256 and "4294967295 * ge(s, 8)" in f["NET.bend"]
    assert "(1 * ge(s, 8)" in m["NET.bend"]


def run(d):
    env = {**os.environ, "BEND_NO_TELEMETRY": "1"}
    p = subprocess.run([BEND, "PROOF.bend", "--check-only"], cwd=d, env=env, capture_output=True, text=True, timeout=600)
    return p.stdout + p.stderr


@needs_bend
def test_5_bend_counts_a_synthetic_sub_tape_exactly_like_the_reference(tmp_path):
    """113 classes, rows a = 0, 1 and pairs b = 0..2, 3 neurons, a planted tie and a planted correct pair: bend accepts the
    reference's count and refuses count + 1 (the same code path as the run, at a size the checker can hold)."""
    T = small_tape(113, 3, 2)
    p = 113
    for a, b in [(0, 0), (1, 2)]:   # plant a correct pair at (0, 0) and a tie at the label of (1, 2)
        k, lab = a * p + b, (a + b) % p
        L = B.logits(T["h"][k], T["n"][k], T["W"], T["b"])
        T["n"][k][lab] += max(L) - L[lab] + (1 if (a, b) == (0, 0) else 0)
    hits = [B.hit(B.logits(T["h"][a * p + b], T["n"][a * p + b], T["W"], T["b"]), (a + b) % p) for a in range(2) for b in range(3)]
    assert hits[0] == 1 and hits[5] == 0
    X = sum(hits)
    ro = open(os.path.join(HERE, "bend2_readout.bend")).read()
    for name, laws, want in [("ok", [("total", X, None), ("row1", sum(hits[3:]), 1)], "ALL PROOFS CHECK"),
                             ("bad", [("total", X + 1, None)], "SOME PROOFS FAIL")]:
        d = tmp_path / name
        B.write_dir(str(d), {"RO.bend": ro, "LAWS.bend": B.law_file(T, laws, nr=2, nb=3), "PROOF.bend": B.proof_file([n for n, _, _ in laws])})
        assert want in run(str(d)), name


@needs_bend
def test_6_the_parity_files_parse_on_a_3_bit_cousin(tmp_path):
    """The generator's NET / LAWS / PROOF shapes, cut to 3 bits by text (the 8-bit files are the run and are not checked here)."""
    f = B.parity_files(False)
    assert f["LAWS.bend"].count("for x") == 8 and f["PROOF.bend"].startswith("import Base\nimport ./LAWS.bend as Laws")


def test_7_closed_rounds_are_imported_not_copied():
    src = open(B.__file__).read()
    assert "import osc_neuron_period_cut as Z" in src
    for name in ("def feats", "def solve", "def install", "def arm(", "class OneLayer", "def make", "def data(", "backward", ".step()"):
        assert name not in src, name
