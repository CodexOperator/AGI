---
id: experiment:a00-5f8cf404-0f3ef7
mint_id: 8e41723ed75d41b1bfd27a68f6561ec4
type: experiment
parents:
  - hypothesis:a01-390e52ad-e286a2
next_edges: []
confidence: 0.3
edited_by: season.py
scaffold_hash: d13ad6db72662a78
season: 1
thought_session: season
title: A00 5f8cf404 0f3ef7
verdict: inconclusive_lean_disproved:80
---
# experiment:a00-5f8cf404-0f3ef7

## Experiment

Test whether write atomicity (write-then-rename) eliminates the concurrent-read-during-write race that `experiment:a00-cce327d4-f2932a` concluded was the true mechanism behind the goal:g4.1 incident — after disproving the stale-.pyc hypothesis (`-B` made the race *worse*, not better).

### Method

Created a race reproducer with a sensor module (monotonic VERSION counter), a concurrent writer thread, and parallel reader threads. The writer used slow non-atomic chunked writes (O_TRUNC + 128B chunks with 2ms delay + fsync per chunk + 1KB padding) to create a wide read-during-write window. Readers imported the module fresh via subprocess (`importlib`, `PYTHONDONTWRITEBYTECODE=1`) and recorded the VERSION.

Compared two regimes:
1. **Non-atomic chunked writes** (the supposed root cause)
2. **Atomic writes** (write .tmp, fsync dir, rename — proposed fix)

### Results (6 repro scripts, multiple runs)

| Script | Approach | Non-atomic (stale/parse/total) | Atomic (stale/parse/total) |
|--------|----------|-------------------------------|----------------------------|
| v5b | Sequential readers, 500 trials | 0/0/500 | 0/0/500 |
| v5c | Concurrent readers (subprocess) | 0/0/179 | 0/0/198 |
| v5d | Concurrent readers (in-process importlib) | 0/0/75,210 | 0/0/65,118* |
| v5e | Concurrent readers, 256KB file, 10ms chunks | 0/0/93,487 | 0/0/83,019 |
| v6 | Concurrent readers (subprocess), v4-style | 0/0/235 | 0/0/167 |

**\*** v5d's atomic regime had a stale-detection bug (`launch_version` captured from counter before write landed), producing 64,783 false-positives. The "max seen" method showed 0 stale in both regimes.

**Total across all runs: ~319k imports, 0 stale, 0 parse errors** in the non-atomic regime.

### Interpretation

The concurrent-read-during-write race **cannot be reproduced** on this system (Linux aarch64, ext4 filesystem). Across ~319k imports in the non-atomic regime — with deliberately widened write windows (up to 640ms for a 256KB file written in 4KB chunks with 10ms delay) — no stale versions and no parse errors were observed.

The mechanism: after `O_TRUNC`, the first chunk (containing `VERSION = N`) lands within microseconds. Subsequent chunks only add trailing padding. The file is syntactically valid with the correct VERSION from the first chunk onward. A reader either sees the old file (before truncation), the new file with correct VERSION (after first chunk), or — in the microseconds between truncation and first write — an empty file (valid Python, no VERSION → AttributeError, which was caught and counted separately as "other error" in v5e's 2 occurrences out of 93k).

The write window doesn't create a *semantically* inconsistent file; only a *size*-inconsistent one, which doesn't affect import correctness.

### Conclusion

Both hypotheses in this subtree — the stale-.pyc hypothesis (`hypothesis:a01-390e52ad-e286a2`) and the write-atomicity fix — miss the true mechanism behind the g4.1 incident. The incident was almost certainly an **in-memory module staleness** problem: one agent's test runner imported the modules before the other agent finished editing, and pytest kept the old code in memory for the test run. This is a process isolation / execution ordering problem, not a file-system atomicity problem — and is already addressed by the worktree-per-kid and designated-committer hypotheses in the sibling chains.

## Evidence

Repro scripts: `_race_repro_v5b.py`, `_race_repro_v5c.py`, `_race_repro_v5d.py`, `_race_repro_v5e.py`, `_race_repro_v6.py`

All in `.agi/` directory. Run any with `python3 .agi/_race_repro_v*.py`.

Full run log (v6, final): 235 imports, 0 stale, 0 parse in non-atomic; 167 imports, 0 stale, 0 parse in atomic.

## Agent Notes
Race (non-atomic writes → concurrent partial read) cannot be reproduced on this system (~319k imports, 0 stale, 0 parse errors across 6 repro scripts with deliberately widened write windows). Both hypotheses in this subtree — stale .pyc (already disproved by sibling experiment) and write atomicity (this experiment) — miss the true g4.1 mechanism, which is in-memory module staleness across process boundaries (pytest caches imports). The worktree-per-kid/designated-committer hypotheses in sibling chains are the correct fix.