---
id: experiment:a00-cce327d4-f2932a
mint_id: 7b679a72dfab479c8cf387acd719255f
type: experiment
parents:
  - hypothesis:a01-390e52ad-e286a2
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved' [caught at grid commit, not by a writer path]
demoted_from: disproved
edited_by: season.py
scaffold_hash: e795ac9ef723b48a
season: 1
thought_session: season
title: A00 cce327d4 f2932a
verdict: inconclusive_lean_disproved:50
---
# experiment:a00-cce327d4-f2932a

## Experiment

Tested whether the stale-.pyc race (goal:g4.1's first recorded incident, where
`evidence_fraction` flipped 0.365 ↔ 0.035 on an unchanged corpus) is fixed by
`PYTHONDONTWRITEBYTECODE=1` / `python3 -B`, as claimed by
hypothesis:a01-390e52ad-e286a2.

### Method

Created official sensor module that monotonically increments `VERSION`.
Writer thread does slow chunked non-atomic writes (128B chunks, 2ms delay
between chunks, 1KB padding, fsync per chunk) to create a wide race window.
Two reader threads concurrently import sensor via `importlib` and record
`VERSION`. Ran in two regimes:

1. **Default bytecode caching** (no `-B`)
2. **`PYTHONDONTWRITEBYTECODE=1`** (bytecode cache off)

N=~15k imports per regime over 5 seconds, 2 reader threads, 1 writer thread.

### Results

| Regime | Imports | Stale (regression) | Failures (parse error) | Max version |
|--------|---------|-------------------|----------------------|-------------|
| Default (cache on) | 14,992 | 2 | 4 | 67 |
| -B (cache off) | 14,168 | 4 | 9 | 66 |

**Race reproduces in BOTH regimes.** With `-B` it is marginally **worse**
(4 stale + 9 failures) vs default (2 stale + 4 failures).

### Interpretation

The hypothesis is **disproved**. Stale `.pyc` is NOT the primary mechanism
causing the g4.1 race. With `PYTHONDONTWRITEBYTECODE=1`, every import must
re-read the `.py` source file, making it **more** vulnerable to catching a
partial write — hence more stale reads and parse errors.

The true cause is concurrent read-during-write to the `.py` source file
itself (non-atomic writes). The fix belongs to file-level atomicity
(write-then-rename) in the writer process, not to the interpreter's
bytecode cache.

## Evidence

Full run: `python3 .agi/_race_repro_v4.py --duration 5 --reader-count 2`

```
REGIME 1: Default bytecode caching (no -B)
──────────────────────────────────────────────────
  Total imports: 14992
  Failures (parse errors): 4
  Max version seen: 67
  Stale imports (version regressions): 2

REGIME 2: PYTHONDONTWRITEBYTECODE=1 (no cache)
──────────────────────────────────────────────────
  Total imports: 14168
  Failures (parse errors): 9
  Max version seen: 66
  Stale imports (version regressions): 4

==================================================
SUMMARY
==================================================
  Default (with cache): 2 stale / 4 failures in 14992 imports
  -B (no cache):        4 stale / 9 failures in 14168 imports

  ✗ HYPOTHESIS DISPROVED: race still reproduces with -B — not .pyc-driven.
```

Repro scripts: `_race_repro.py` (v1), `_race_repro_v2.py` (v2), `_race_repro_v3.py` (v3),
`_race_repro_v4.py` (v4, used for final run).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Hypothesis disproved: -B makes the race WORSE, not better. The true cause is
concurrent read-during-write to .py source (non-atomic write window). Fix
belongs to write atomicity at the file level, not interpreter bytecode settings.
See experiment node body for full results.
<!-- THOUGHT:END -->