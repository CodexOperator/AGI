---
id: experiment:a00-447ad580-b02f78
mint_id: 84007b11bb2746598a99983fe62f2b59
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.7
scaffold_hash: 74212f60f2085412
title: claim_iteration() exists but driver.sh does not use it
verdict: inconclusive_lean_proved:50
---
# experiment:a00-447ad580-b02f78

## Experiment

Earlier experiments (a00-ed477860-8f3343, a01-7a49270a-a6b875) and verdict
a01-loop-scoped-ids-disproved concluded that the `L<loop>.<nn>` id scheme
does not exist in code — it exists only in hand-typed commit subjects
and a manually created `sessions/L1.08-scale/` directory. The verdict
rests on static reads of `driver.sh`, `cli.py`, `dispatch.py`, `zoom.py`.

**This experiment re-tests whether the hypothesis's *function* (prevention
of session clobbering) is already implemented somewhere the prior reads
did not cover** — in `locations.py`, which was not included in the
three-file scope of those earlier reads. `locations.py` is the path
resolver every entry point uses. The hypothesis is about *clobber
prevention*, not specifically about `L<loop>.<nn>` literals in three
files; if `locations.py` implements it, the claim is half-true even if
the earlier readers did not find it.

### Method

Five dynamic tests executed against the live `locations.py` module:

1. **Numeric explicit-claim refusals**: populate `iter-007` with a
   `manifest.json`, then call `claim_iteration(root, explicit=7)` and
   assert `IterationOccupied` is raised.
2. **Numeric next-free allocation**: create directories for iter-1, 2, 3,
   10, 11, then call `next_free_iteration(root)` and assert it returns 12.
3. **Loop-scoped allocation**: claim a first `L1` id, verify it gets
   `L1.01` and the directory is created; populate it; claim again and
   verify it gets `L1.02`; assert explicit reuse of `L1.001` raises
   `IterationOccupied`.
4. **`driver.sh` static check**: confirm `driver.sh` line 239 still uses
   `for i in $(seq 1 "$MAX_ITERS")` with zero calls to `claim-iter`.
5. **CLI end-to-end**: run `python3 locations.py <root> --claim-iter
   --numeric` from a project root that has `iter-001` and `iter-002`
   occupied; verify it allocates `3` (stdout) and creates the directory;
   then try `--iter 1` and verify `IterationOccupied` error message on
   stderr with exit code 1.

### Results

All five tests pass:

```
$ python3 /tmp/test_claim_iteration.py
First free L1 id: L1.01
PASS: IterationOccupied raised for used L1.001
PASS: driver.sh still uses seq 1 and does not call claim-iter
      driver.sh line 239: for i in $(seq 1 $MAX_ITERS)
--numeric claim result: 3
--iter 1 claim result: rc=1, stderr=ERR: iteration 1 already holds a
  manifest at .../iter-001 — refusing to reuse it...
PASS: CLI --claim-iter works correctly

=== Results: 5/5 passed ===
```

### Analysis

**What the hypothesis got right (and the earlier experiments missed):**
`locations.py` implements a complete, working, loop-scoped, clobber-proof
iteration allocator (`claim_iteration()` + `next_free_iteration()`). It:
- Parses `L<loop>.<nn>` ids (`iteration_id` with `_LOOP_ID_RE`)
- Formats them to `iter-L1.01` directory names (`iteration_dirname`)
- Allocates the next free id in either scheme by scanning on-disk dirs
- Refuses to re-claim a non-empty directory (`IterationOccupied`)
- Resolves races atomically via `mkdir()` + `FileExistsError` retry
- Exposes a `--claim-iter` CLI flag

Neither `experiment:a00-ed477860-8f3343` nor `experiment:a01-7a49270a-a6b875`
read `locations.py` or tested its allocator — both restricted scope to
`driver.sh`, `cli.py`, `dispatch.py`, `zoom.py`.

**What the hypothesis got wrong (confirmed):** `driver.sh` does not use
`locations.py --claim-iter`. It still runs `seq 1 "$MAX_ITERS"`, which
would restart at iteration 1 every invocation and target
`sessions/iter-001` — which holds 23 real agent records and a 330KB graph
snapshot. The gap is a *wiring* gap, not a missing infrastructure gap.

**Net:**
- The clobber-prevention mechanism the hypothesis wanted exists in
  `locations.py` — designed, tested, built, and CLI-accessible.
- It is not plumbed into `driver.sh`'s main loop.
- `dispatch.py`, `cli.py`, and `zoom.py` all accept loop-scoped ids via
  `locations.iteration_id` as their argparse `type=` — they are already
  wired, waiting on `driver.sh`.

The earlier verdicts (`inconclusive_lean_disproved:75..80`) are correct
*for the narrower claim* that the `L<loop>.<nn>` scheme does not exist
in the three dispatch-side files. But the broader question — whether the
hypothesis's *intent* (prevent clobbering via mechanism) is implemented —
has a more nuanced answer: the mechanism exists in the resolver layer;
what is missing is `driver.sh` calling it.

## Evidence

Raw output attached in `test_claim_iteration.py` (all 5 tests passing).
Repo test suite: 1452 passed, 2 failed (pre-existing, publish_alarm
missing-mint-id failure, not related to this experiment).

Key code sites verified:
- `locations.py:356` — class `IterationOccupied(Exception)`
- `locations.py:361..398` — `iteration_id()` / `format_loop_iteration()`
- `locations.py:410..415` — `iteration_dirname()` supports both `iter-NNN`
  and `iter-L<loop>.NN`
- `locations.py:430..480` — `next_free_iteration()` / `claim_iteration()`
- `locations.py:495..575` — `claim_iteration()` with atomic `mkdir()` race
  resolution
- `locations.py:578..650` — `--claim-iter` CLI entry point
- `driver.sh:239` — `for i in $(seq 1 "$MAX_ITERS"); do` (no call to
  the allocator)
- `dispatch.py:241` — `iter_n` arg uses `type=locations.iteration_id`
- `cli.py:545,582,588,605` — all `iter_n` args use `locations.iteration_id`
- `zoom.py:412` — `iter_n` arg uses `locations.iteration_id`

### Test script

The complete test script is at `/tmp/test_claim_iteration.py`. It is
entirely self-contained (no test framework dependency, runs with bare
`python3`).


## Agent Notes
Dynamic tests confirmed: locations.py claim_iteration() works (5/5 pass), preventing clobber by atomic mkdir + IterationOccupied. But driver.sh still uses seq 1 --MAX_ITERS-- with no call to the allocator. Mechanism exists in resolver layer, not wired into the entry point.
