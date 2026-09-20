#!/usr/bin/env python3
"""Score HumanEval arms: pass@1 per arm, paired discordant tables, McNemar exact p."""
import json, math, os, sys
from human_eval.evaluation import evaluate_functional_correctness

OUTDIR = "/data/ml/models/bonsai/abc_humaneval"
PROBLEM_FILE = os.path.join(OUTDIR, "problems.jsonl")

def load(tag):
    rows = []
    with open(os.path.join(OUTDIR, tag + ".completions.jsonl")) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return {r["task_id"]: r for r in rows}

def write_problems():
    from human_eval.data import read_problems
    probs = read_problems()
    with open(PROBLEM_FILE, "w") as f:
        for tid, p in probs.items():
            f.write(json.dumps({"task_id": tid, "prompt": p["prompt"],
                                "canonical_solution": p["canonical_solution"],
                                "test": p["test"], "entry_point": p["entry_point"]}) + "\n")

def passmap(tag):
    # evaluate_functional_correctness reads our file and returns pass/fail per task
    res = evaluate_functional_correctness(
        os.path.join(OUTDIR, tag + ".completions.jsonl"),
        problem_file=PROBLEM_FILE, k=[1], n_workers=8, timeout=10)
    return res  # {"pass@1": x}; need per-problem -> use detailed

def per_problem(tag):
    from human_eval.evaluation import estimate_pass_at_k  # noqa
    # run through the same machinery but collect booleans by re-implementing the check loop
    from human_eval.data import read_problems
    from human_eval.execution import check_correctness
    probs = read_problems()
    out = {}
    for r in load(tag).values():
        tid = r["task_id"]
        p = probs[tid]
        ok = check_correctness(p, r["completion"], timeout=10.0, completion_id=0)["passed"]
        out[tid] = bool(ok)
    return out

def mcnemar_exact(b, c):
    # two-sided exact McNemar
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n) * 2
    return min(1.0, p)

if __name__ == "__main__":
    tags = sys.argv[1:]
    print("=== per-arm pass@1 ===")
    maps = {}
    for t in tags:
        m = per_problem(t)
        maps[t] = m
        n = len(m); passed = sum(m.values())
        print(f"{t}: {passed}/{n} = {passed/n*100:.1f}%")
    print("=== paired discordant + McNemar ===")
    for i in range(len(tags)):
        for j in range(i + 1, len(tags)):
            a, b = tags[i], tags[j]
            common = sorted(set(maps[a]) & set(maps[b]))
            b_only = sum(1 for k in common if maps[b][k] and not maps[a][k])  # b beats a
            a_only = sum(1 for k in common if maps[a][k] and not maps[b][k])
            pa = sum(maps[a][k] for k in common)
            pb = sum(maps[b][k] for k in common)
            print(f"{a} vs {b}: n={len(common)} {a}={pa/len(common)*100:.1f}% {b}={pb/len(common)*100:.1f}% "
                  f"b={b_only} c={a_only} diff={(pb-pa)/len(common)*100:+.1f}pp McNemar_p={mcnemar_exact(b_only,a_only):.4f}")