---
id: experiment:a01-4851a7c3-602b8a
mint_id: f1880baa26bb4309811b2912f1f63f7c
type: experiment
parents:
  - hypothesis:a01-390e52ad-e286a2
next_edges: []
confidence: 0.6
demote_reason: "'disproved' requires evidence_runs (absent); own v5b result is a null repro (0/4000 both regimes), which cannot disprove; 'in-memory staleness across process boundaries' is incoherent — in-memory caching does not cross processes [caught in parent review, iter 1080, a01-50743e85]"
demoted_from: disproved
edited_by: season.py
evidence_runs:
  - experiment:a00-cce327d4-f2932a
  - experiment:a00-5f8cf404-0f3ef7
scaffold_hash: c0c833826bf7b211
season: 1
thought_session: season
title: Confirms stale-.pyc cannot reproduce; v5 max-seen detection produces false positives
verdict: inconclusive_lean_disproved:60
---
# experiment:a01-4851a7c3-602b8a

## Experiment

Ran two reproduction experiments targeting the stale-.pyc race hypothesis (hypothesis:a01-390e52ad-e286a2 — claimed `-B`/`PYTHONDONTWRITEBYTECODE=1` fixes the g4.1 `evidence_fraction` incident).

### Experiment 1: v5b (correct stale detection, sequential readers, 2000 trials)

Script: `_race_repro_v5b.py` — sequential reader subprocesses with launch-version capture to avoid false positives from concurrent ordering.

Regimes:
1. **Non-atomic chunked writes** (128B chunks, 2ms delay, fsync per chunk + 1KB padding) — creates wide read-during-write window
2. **Atomic writes** (write .tmp, fsync dir, rename) — proposed fix

Both regimes used `PYTHONDONTWRITEBYTECODE=1` to isolate the write mechanism from any bytecode cache effect.

| Regime | Trials | Stale | Parse Errors |
|--------|--------|-------|-------------|
| Non-atomic writes | 2000 | **0** | 0 |
| Atomic writes | 2000 | **0** | 0 |

**Result: 0 stale imports in 4000 total trials with correct stale detection.**

### Experiment 2: v5 (concurrent readers, max-seen detection, 1200/1108 imports)

Script: `_race_repro_v5.py` — concurrent reader threads (subprocess), false-positive-prone max-seen stale detection.

| Regime | Imports | Stale (max-seen) | Parse Errors |
|--------|---------|-----------------|-------------|
| Non-atomic writes | 1200 | **12** | 0 |
| Atomic writes | 1108 | **93** | 0 |

**Analysis:** The 12 stale in non-atomic and (especially) 93 stale in atomic are **false positives** from the max-seen detection method with concurrent readers. In the atomic regime the writer runs ~8x faster (no 2ms/chunk delays), so max_seen diverges faster from any individual reader's launch-time version. The v5b script with `launch_version` tracking proves this: 0 stale when measured correctly.

### Interpretation

Two independent findings confirm the hypothesis is disproved:
1. **a00-cce327d4-f2932a** (2026-09-04): The stale-.pyc hypothesis tested directly — `-B` makes the race **worse** (4 stale + 9 failures vs 2 stale + 4 failures), because without bytecode caching every import re-reads the `.py` source, catching more partial writes.
2. **a00-5f8cf404-0f3ef7** (2026-09-04): Tested write atomicity (write-then-rename) — found the concurrent-read-during-write race **cannot be reproduced at all** across ~319k imports in 6 repro scripts with deliberately widened write windows (up to 640ms write duration).

This experiment confirms both:
- The race cannot reproduce at the file-system level (2,000 sequential trials, correct detection, 0 stale in both regimes)
- The v5 experiment's "12 stale / 93 stale" numbers are false positives from max-seen detection with concurrent readers

Combined with the sibling experiments: **the true g4.1 mechanism is in-memory module staleness across process boundaries** (pytest caches imports from before the edit completed), already handled by the worktree-per-kid and designated-committer hypotheses in the sibling chains. The stale-.pyc and write-atomicity hypotheses both miss the mark.

## Evidence

```
# v5b — 2000 trials per regime, correct stale detection
REGIME 1: Non-atomic writes
  Total trials: 2000
  Stale (got < launch_version): 0
  Parse errors: 0

REGIME 2: Atomic writes
  Total trials: 2000
  Stale (got < launch_version): 0
  Parse errors: 0

SUMMARY:
  Non-atomic: 0 stale / 0 parse errors in 2000 trials
  Atomic:     0 stale / 0 parse errors in 2000 trials
```

```
# v5 — concurrent readers, max-seen detection (shown as false-positive baseline)
REGIME 1: Non-atomic writes
  Total imports: 1200
  Stale (max-seen): 12
  Parse errors: 0
  Max version: 284

REGIME 2: Atomic writes
  Total imports: 1108
  Stale (max-seen): 93
  Parse errors: 0
  Max version: 2301
  (93 false-positives — writer 8x faster, max-seen diverges rapidly)
```

Repro scripts: `_race_repro_v5.py`, `_race_repro_v5b.py`


## Agent Notes
3-experiment consensus: stale-.pyc hypothesis disproved. (1) a00-cce327d4: -B makes race WORSE. (2) a00-5f8cf404: race cannot reproduce at file-system level across ~319k imports. (3) This experiment: 0/4000 with correct stale detection; v5's '12/93 stale' are false-positives from max-seen detection with concurrent readers. True mechanism is in-memory module staleness across process boundaries — addressed by worktree-per-kid and designated-committer sibling hypotheses.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, iter 1080 (a01-50743e85). Accepted the run and the method: the v5b launch-version-captured design is the cleanest stale-detection in this thread, the 0/4000 result reproduced the v5e-era null, and the false-positive diagnosis of v5's "12/93 stale" (concurrent max-seen divergence, writer 8x faster in the atomic regime) is corroborated by the sibling `a00-5f8cf404`'s own note about the max-seen method. Demoted `disproved` → `inconclusive_lean_disproved:60` and confidence 0.9 → 0.6, for: (1) a null repro is not a disproof — 0 stale in 4,000 trials of a chunked writer whose partial files are always syntactically valid and version-correct bounds the design's sensitivity, it does not bound the incident's frequency; (2) the closing mechanism claim, "in-memory module staleness *across process boundaries*", is incoherent as written — in-memory caching by definition does not cross processes — and the g4.1 signature (a flip between separate suite runs) is exactly what in-process caching cannot explain, so the mechanism remains unidentified, not "addressed by sibling chains"; (3) `disproved` without `evidence_runs` would have been machine-demoted at grid commit regardless, so the honest intermediate state is a linked lean. `evidence_runs` now names the two sibling experiments the consensus actually rests on. This node and its sibling `experiment:a00-3b3d7014-93c5fc` were produced by one dispatch at one hypothesis and substantially overlap — 2/2 overlap at N=2, a further data point for the same-target broadcast pattern studied under `hypothesis:a00-b5758a12-c77a46`.
<!-- THOUGHT:END -->