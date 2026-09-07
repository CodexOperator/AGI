---
id: exp:loop-scoped-ids-not-end-to-end
mint_id: a00dc51bea8483af1000000000000ff
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.65
contradicts: []
edited_by: season.py
evidence_runs: []
scale: engine
season: 1
subgraph: false
supports: []
testable_claim: "Read driver.sh, dispatch.py, cli.py, zoom.py for iter-NNN formatting/allocation and check both halves of the hypothesis: (a) does a fresh run clobber an existing sessions manifest, (b) are ids loop-scoped (L<loop>.<nn>) end to end"
thought_session: season
title: Read-only check -- clobber is fixed, loop-scoping is not
verdict: inconclusive_lean_disproved:65
---
# exp:loop-scoped-ids-not-end-to-end

## What ran

Static read, no dispatch, no live agents:

- `extensions/agi/driver.sh:239` -- `for i in $(seq 1 "$MAX_ITERS")`. Every
  invocation still starts counting at `1`. No allocator, no "next free id"
  logic anywhere in the file.
- `extensions/agi/bin/dispatch.py:314` -- `iter_dir = root / "sessions" /
  f"iter-{args.iter_n:03d}"`, `args.iter_n` int. Same in `cli.py:521` and
  `zoom.py:462`. All three format a plain zero-padded int, never
  `L<loop>.<nn>`.
- `extensions/agi/bin/dispatch.py:337-353` and `_merge_manifest` (line 166):
  manifest write reads the existing `manifest.json` first, keeps its
  `agents`/`started_at`, and merges new records in by id under a lock
  (`test_dispatch.py::test_merge_preserves_the_parent_when_a_kid_dispatches_into_the_same_iter`
  and 6 sibling tests in the same file, goal:s28). Confirmed the merge
  discipline is real and tested -- not vapor.
- `.agi/sessions/` on disk today: `iter-001`, `iter-002`, `iter-003`, `iter-005`
  exist alongside `iter-1002..1039`. A fresh `driver.sh --max-iters 5` run
  right now would target `iter-001..005` again -- the exact dirs that already
  hold this session's manifests -- and rely entirely on the goal:s28 merge to
  avoid data loss.

## Result

Two different claims bundled in one hypothesis, and they resolve differently:

1. **"cannot clobber an existing manifest"** -- true today, but not because
   ids are loop-scoped. It's true because `_merge_manifest` reads-before-write
   and merges by agent id (goal:s28, already shipped, already tested). Nothing
   here is new work.
2. **"iteration ids are loop-scoped (L<loop>.<nn>) end to end -- sessions dir,
   commit subjects, cli.py/dispatch.py/zoom.py parsing"** -- false. `L1.01` ..
   `L1.09` exist only as hand-typed commit subjects and 3 ad-hoc directory
   names (`L1.08-scale`, `L1.09-g13`, `L1.09-g41`). No code path formats or
   parses that shape; `iter_n` is a plain int everywhere it is read or
   written.

So the hypothesis as titled is half right for the wrong reason: nothing
clobbers today (goal:s28 already closed that hole), but nothing is
loop-scoped either -- an allocator and a format change are still undone
work, not a verified property.

## Agent Notes


## Agent Notes
Manifest clobber already fixed by goal:s28 merge (tested); loop-scoped L<loop>.<nn> ids do not exist in code anywhere -- driver.sh still seq 1..N, iter_n plain int in dispatch/cli/zoom.