---
id: experiment:a00-c956a54b-15cb30
mint_id: 67c5e25a4a1b4c3981ab7f4a2001addd
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.7
scaffold_hash: 44bb05daa4b39bff
title: A00 c956a54b 15cb30
verdict: inconclusive_lean_disproved:70
---
# experiment:a00-c956a54b-15cb30

## Experiment

Dynamic validation of the `claim_iteration` allocator added in L1.10b (commit `b45fdcaca`), plus spot-check of the two stale gaps the prior experiments identified.

### Part 1 — allocator dynamic test (7 checks)

Wrote a self-contained Python script that calls `claim_iteration()` from the current `locations.py` in a tmpdir sandbox. All 7 checks passed:

**Check 1:** first claim in loop-scoped scheme (`L1`) returns `L1.01`, creates the directory.
**Check 2:** second claim auto-increments to `L1.02`.
**Check 3:** explicit `--iter L1.01` on an empty dir reclaims it (by design — empty is free).
**Check 4:** explicit `--iter L1.01` after placing a manifest file raises `IterationOccupied` — *the guard the hypothesis claimed did not exist, now exists and works.*
**Check 5:** numeric scheme (`loop=None`) independently allocates `1`.
**Check 6:** both `L1.01`, `L1.02` and `1` appear in `list_iterations()` — schemes coexist.
**Check 7:** `next_free_iteration` reports `L1.03` after `L1.01` (occupied) and `L1.02` (claimed).

### Part 2 — stale-gap re-check

**`driver.sh:239`** still counts via `for i in $(seq 1 "$MAX_ITERS"); iter_run "$i"`. There are zero calls to `claim_iteration`, `next_free_iteration`, or `locations.py --claim-iter` in the driver. The dispatch.py line 8 comment "caller allocates one (`driver.sh` via `locations.py --claim-iter`)" describes an aspiration, not the current wiring.

**`post_wire.py:533`** still writes graph.json via plain `graph_path.write_text(json.dumps(...))` — no read-merge, no protection against a second dispatch overwriting the first run's graph snapshot. Confirmed by `experiment:a00-dce9d5da-377c4d` dynamic test (already in the graph).

### Part 3 — test coverage gap

`grep -rn "claim_iter\|next_free_iter\|IterationOccupied" extensions/agi/tests/` returns zero matches. The allocator has no test coverage at all.

## Evidence

### Part 1 output
```
tmpdir: /tmp/tmp_vzb1dd5-claim-test
Test 1: first claim (loop L1) -> L1.01
  PASS: dir created empty
Test 2: second claim -> L1.02
  PASS: auto-incremented
Test 3: explicit claim of empty dir -> L1.01 (reclaimable)
  PASS: empty dir is reclaimable
Test 4: explicit claim of occupied dir -> IterationOccupied
  PASS: occupied guard works with content
Test 5: numeric scheme -> 1
  PASS: numeric scheme works
Test 6: both schemes coexist
  PASS: both schemes coexist
Test 7: next_free_iteration(L1) -> L1.03
  PASS: next free computed correctly
```

### Code verification

```
# driver.sh:239 — still seq 1, no claim_iter
for i in $(seq 1 "$MAX_ITERS"); do
  iter_run "$i"
done

# post_wire.py:533 — plain overwrite, no merge
graph_path.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")

# Test coverage: zero
grep -rn "claim_iter\|next_free_iter\|IterationOccupied" tests/ → (no output)
```

### Key finding

The hypothesis was "disproved" by prior experiments that predated the L1.10b code. The verdict was *technically correct* at the time (no allocator existed). Today the allocator DOES exist and works correctly — 7/7 checks pass — but it's disconnected from the loop entry point (`driver.sh`) and the graph.json overwrite is still unprotected. The hypothesis's specific claim ("loop-scoped iteration ids cannot clobber") is still false as a description of *deployed* behavior (because the allocator isn't wired to the entry point), but the *mechanism* it called for now exists, works, and is testable.

This makes the original verdict stale. A fresh experiment re-reading the codebase would find `claim_iteration` present and working but unused — changing the evidence, not the verdict.


## Agent Notes
Dynamic test: claim_iteration allocator verified working (7/7 checks) but driver.sh:239 still uses seq 1 N without wiring; post_wire.py:533 graph.json plain overwrite still unprotected; allocator has zero test coverage. Prior disproved verdict is stale for mechanism (which now exists) but correct for deployed behavior.
