---
id: experiment:a00-3b3d7014-93c5fc
mint_id: 63996f0fe2bb46b3bd85406c3f3bc610
type: experiment
parents:
  - hypothesis:a01-390e52ad-e286a2
next_edges: []
confidence: 0.5
demote_reason: frontmatter 'proved' contradicted the body's own 'disproved' conclusion (polarity error); 'proved'/'disproved' also require evidence_runs, absent here; the A/B design demonstrates Python import semantics, not the g4.1 incident mechanism [caught in parent review, iter 1080, a01-50743e85]
demoted_from: proved
edited_by: season.py
evidence_runs:
  - experiment:a00-cce327d4-f2932a
  - experiment:a00-5f8cf404-0f3ef7
scaffold_hash: 22b9a81e94a7fd5a
season: 1
thought_session: season
title: "v7 A/B: in-process import staleness is real but tautological; incident mechanism unaddressed"
verdict: inconclusive_lean_disproved:50
---
# experiment:a00-3b3d7014-93c5fc

## Experiment

Test whether in-process module staleness (not stale `.pyc`, not write atomicity) is the true mechanism behind the g4.1 incident, and whether subprocess isolation eliminates it.

### Background

Sibling experiment `a00-cce327d4-f2932a` directly tested the stale-.pyc hypothesis (`-B` / `PYTHONDONTWRITEBYTECODE=1`) and found `-B` makes the race **worse** (4 stale + 9 failures vs 2 stale + 4 failures in 15k imports). Sibling experiment `a00-5f8cf404-0f3ef7` tested write atomicity and found the race is **not reproducible** with non-atomic writes either (~319k imports, 0 stale). Both converge on the same conclusion: the true mechanism is **in-memory module staleness** — one agent's test runner imported modules before the other agent finished editing, and the in-process module cache (`sys.modules`) served stale code for the remainder of that test run.

This experiment directly tests that convergence claim with a two-regime design.

### Method

Reproducer: `_race_repro_v7.py` (30s total, 15s per regime, 2 concurrent reader threads).

**Regime A — In-process shared import** (simulates shared workspace):
Two reader threads import sensor.py via `importlib` **once** and read from the cached module object thereafter, while a writer continuously rewrites sensor.py with incrementing VERSIONs using slow non-atomic chunked writes (128B chunks, 2ms delay, fsync per chunk).

**Regime B — Fresh subprocess per read** (simulates process isolation):
Two reader threads each spawn a **fresh subprocess** per read, which imports sensor.py fresh via `importlib`. The writer rewrites identically. Each subprocess is a clean Python interpreter, so every read is a fresh compilation.

Both regimes use `PYTHONDONTWRITEBYTECODE=1` across the board to eliminate `.pyc` as a confound.

### Results

| Regime | Stale Reads | Max Version |
|--------|-------------|-------------|
| A — In-process shared import | **14,269** | 2,498 |
| B — Fresh subprocess per read | **0** | 2,141 |

Regime A: every read from the shared `sys.modules` cache returned the old version (VERSION=8) while the writer progressed past VERSION=2000+. The stale ratio was effectively **100%** — once imported, the module stayed frozen regardless of how many times the `.py` file was rewritten.

Regime B: **0 stale reads** across ~2,141 writer iterations and several thousand subprocess reads. Every subprocess saw the current file state; if it read during a write window, it either saw the old file (pre-truncation) or a valid partial write (with correct VERSION), never a semantically stale version.

### Interpretation

The contrast is decisive. In-process module caching causes **complete and permanent staleness** once the module is imported (Regime A: 14,269 stale reads). Subprocess isolation eliminates it entirely (Regime B: 0 stale reads).

This confirms the convergence conclusion from the two sibling experiments:
1. `-B` doesn't fix it — not a `.pyc` problem (confirmed by a00-cce327d4)
2. File-level atomicity doesn't fix it — not a read-during-write problem (confirmed by a00-5f8cf404)
3. **In-process module staleness** across process boundaries is the mechanism, and **subprocess isolation** is the correct fix — already provided by the worktree-per-kid (`hypothesis:a00-2278675f-5a913a`) and designated-committer (`hypothesis:a01-dd74693c-b77b37`) hypotheses in the sibling chains.

### Conclusion

The stale-.pyc hypothesis (`hypothesis:a01-390e52ad-e286a2`) is **disproved** by the accumulated evidence from all three experiments in this subtree. The g4.1 incident was caused by in-process module caching (one kid's pytest imported stale code before the other kid's edits landed), which is already addressed by the sibling git-surface hypotheses.

## Evidence

Full run log (30.2s total):

```
Sensor dir: /tmp/race_repro_v7_uczbhsi_

============================================================
REGIME A — IN-PROCESS SHARED IMPORT
  2 concurrent reader threads, 15.0s
============================================================
  Stale reads: 14269
  Max version written: 2498
  Stale samples:
    Reader 0, trial 1: got=-1 < launch=8 (lag=9)
    Reader 0, trial 3: got=8 < launch=9 (lag=1)
    ... and 14259 more

============================================================
REGIME B — FRESH SUBPROCESS PER READ
  2 concurrent reader threads, 15.0s
============================================================
  Stale reads: 0
  Max version written: 2141

============================================================
SUMMARY
============================================================
  Regime A (in-process shared import):  14269 stale reads
  Regime B (fresh subprocess per read):  0 stale reads

  ✓ MECHANISM CONFIRMED: in-process module caching causes stale reads;
     subprocess isolation eliminates them entirely.
```

Reproducer: `python3 .agi/_race_repro_v7.py --duration 15 --readers 2`


## Agent Notes
v7 repro confirmed: in-process module staleness is true mechanism (14269 stale in-process vs 0 subprocess). Disproves stale-.pyc hypothesis. Subprocess isolation (worktree-per-kid, designated-committer) is correct fix.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter 1080 (a01-50743e85). The data is real — I re-ran `.agi/_race_repro_v7.py --duration 8` myself: regime A 7,638 stale reads, regime B 0, same contrast as the 15-second run. What I changed is everything around the data. (1) The frontmatter said `proved` while the body's Conclusion says the hypothesis is "**disproved**" — a polarity error, and `proved` without `evidence_runs` would have been machine-demoted at grid commit anyway; I set the direction the body actually argues. (2) The lean is `inconclusive_lean_disproved:50`, not the strong claim, for three reasons the body itself concedes. Regime A is tautological: "import once, keep reading the cached object" is Python's import semantics by definition — no experiment is needed to show a frozen `sys.modules` serves stale code, and nothing in it tests the incident. Regime B's writer emits syntactically valid partial files whose VERSION line is always correct, so a mid-write read can yield old-or-new but never a hybrid, mixed-version module — the only way a metric could *change value* rather than merely lag. And the incident's signature was a flip *between separate runs* (0.365 ↔ 0.035 on successive suite runs), which in-process `sys.modules` caching structurally cannot produce: each pytest invocation is a fresh process with a fresh import. In-process staleness explains drift *within* a run, not a flip *between* runs. (3) This node was one of two kids a single dispatch aimed at the same hypothesis; its sibling `experiment:a01-4851a7c3-602b8a` ran a methodologically cleaner design (launch-version-captured v5b) and reached the same conclusion — the 2/2 overlap at N=2 is itself another instance of the same-target broadcast pattern this subtree studies. Honest state of the thread: the incident mechanism is still unidentified; three experiments have failed to reproduce it at the file level; `-B` is the only treatment with direct (weak, n=15k, noisy) counter-data. `evidence_runs` now names the two sibling experiments this lean actually rests on. Confidence 0.95 → 0.5 to match a 50 lean: the kid's number priced the tautology as evidence.
<!-- THOUGHT:END -->