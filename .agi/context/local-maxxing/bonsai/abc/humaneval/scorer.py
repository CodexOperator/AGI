#!/usr/bin/env python3
"""Score HumanEval arms: pass@1 per arm, paired discordant tables, McNemar exact p.

Usage: scorer.py <tag> [<tag> ...]

Reads <OUTDIR>/<tag>.completions.jsonl. OUTDIR = $ABC_OUTDIR, else the directory
this script lives in. Dataset = the installed `human_eval` package ($HUMANEVAL
overrides). Optional: $ABC_SCORES_JSON writes the full scores.json.
"""
import json, math, os, sys
from human_eval.data import read_problems
from human_eval.execution import check_correctness

OUTDIR = os.environ.get("ABC_OUTDIR", os.path.dirname(os.path.abspath(__file__)))

def load(tag):
    rows = []
    with open(os.path.join(OUTDIR, tag + ".completions.jsonl")) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return {r["task_id"]: r for r in rows}

def per_problem(tag, probs):
    out = {}
    for r in load(tag).values():
        p = probs[r["task_id"]]
        ok = check_correctness(p, r["completion"], timeout=10.0,
                               completion_id=0)["passed"]
        out[r["task_id"]] = bool(ok)
    return out

def mcnemar_exact(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n) * 2)

if __name__ == "__main__":
    tags = sys.argv[1:]
    probs = read_problems()
    print("=== per-arm pass@1 ===")
    maps = {}
    for t in tags:
        m = per_problem(t, probs)
        maps[t] = m
        n = len(m); passed = sum(m.values())
        print(f"{t}: {passed}/{n} = {passed/n*100:.1f}%")
    print("=== paired discordant + McNemar ===")
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            a, b = tags[i], tags[j]
            common = sorted(set(maps[a]) & set(maps[b]))
            b_only = sum(1 for k in common if maps[b][k] and not maps[a][k])
            a_only = sum(1 for k in common if maps[a][k] and not maps[b][k])
            pa = sum(maps[a][k] for k in common)
            pb = sum(maps[b][k] for k in common)
            print(f"{a} vs {b}: n={len(common)} {a}={pa/len(common)*100:.1f}% "
                  f"{b}={pb/len(common)*100:.1f}% b={b_only} c={a_only} "
                  f"diff={(pb-pa)/len(common)*100:+.1f}pp "
                  f"McNemar_p={mcnemar_exact(b_only,a_only):.4f}")
