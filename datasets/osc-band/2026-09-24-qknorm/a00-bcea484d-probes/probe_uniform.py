#!/usr/bin/env python3
"""PARENT PROBE 1 (cheap, no model): the uniform arm is E-independent and byte-matched.

Refutes the near-miss "a relabelled band arm carrying the uniform label".
"""
import importlib.util, json, os, sys

def _repo_root():
    """Walk up from this file to the dir holding BOTH .agi/ and datasets/ (PASS 8 item 5).

    Derived, not declared: the gitignored worktree path this probe used to
    hardcode does not exist on a fresh clone, so the probe died at import.
    """
    p = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(p, ".agi")) and os.path.isdir(os.path.join(p, "datasets")):
            return p
        n = os.path.dirname(p)
        if n == p:
            raise SystemExit("no repo root (.agi/ + datasets/) above " + os.path.abspath(__file__))
        p = n

ROOT = _repo_root()
HERE = os.path.join(ROOT, ".agi/context/local-maxxing/osc")
sys.path[:0] = [os.path.join(ROOT, ".agi/context/local-maxxing"), HERE]
import numpy as np, torch
s = importlib.util.spec_from_file_location("fixed", HERE + "/osc_band_kquant_qknorm_a00-bcb6c85e.py")
fixed = importlib.util.module_from_spec(s); s.loader.exec_module(fixed)

D = os.path.join(ROOT, "datasets/osc-band/2026-09-24-qknorm")
rows = []
for w in ("qwen2", "qwen3"):
    with open(f"{D}/a00-a721f95f-{w}/cells.jsonl") as f:
        rows += [json.loads(x) for x in f if x.strip()]

# (a) byte equality recomputed from the cells' OWN width lists
bad = []
fixed.SPEC["np"] = rows[0]["np"]
for r in rows:
    fixed.SPEC["np"] = r["np"]
    if r["arm"] == "uniform":
        continue
    for u in rows:
        if u["arm"] == "uniform" and u["budget"] == r["budget"] and u["model"] == r["model"]:
            bu, bm = fixed.bits(u["widths"]), fixed.bits(r["widths"])
            if not (bu == bm == float(r["budget"])):
                bad.append((r["cell"], bu, bm))
print("A byte-match violations:", bad)

# (b) the uniform arm ignores the energy profile entirely
for npv in (32, 64):
    fixed.SPEC["np"] = npv; fixed.SPEC["nl"] = 2; fixed.SPEC["kv"] = 2
    E1 = np.random.default_rng(0).random((2, 2, npv))
    E2 = np.random.default_rng(1).random((2, 2, npv))
    u1 = fixed.arm(E1, [4], "uniform"); u2 = fixed.arm(E2, [4], "uniform")
    same = all(torch.equal(a, b) for a, b in zip(u1, u2))
    classes = sorted({int(x) for L in u1 for x in L.flatten().tolist()})
    print(f"B np={npv} uniform arm E-independent={same} pair-classes={classes} "
          f"(0 == every pair at the single uniform width)")
