---
id: experiment:a01-2cd07894-22e52d
mint_id: 2a1d3d5606694388a72ad9b00d17c343
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.7
edited_by: season.py
scaffold_hash: 46690b77cea3ff45
season: 1
thought_session: season
title: A01 2cd07894 22e52d
verdict: inconclusive_lean_disproved:70
---
# experiment:a01-2cd07894-22e52d

## Experiment

Checked whether `cli.py` / `dispatch.py` / `zoom.py` actually format iteration
ids as `L<loop>.<nn>` (the hypothesis's testable claim) and whether the
directory allocator can clobber an existing manifest.

```
grep -n "iter-" extensions/agi/{driver.sh,bin/cli.py,bin/dispatch.py,bin/zoom.py}
```
found three call sites in the four files grepped, all of the same shape:
- `cli.py:521` `iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"`
- `dispatch.py:314` same pattern
- `zoom.py:462` same pattern

**Reviewer correction (parent a00-26a8af2c):** these are not *all* the call
sites in the engine — the grep was scoped to four files. `grep -rn "iter-{"
extensions/agi/bin/*.py` finds four more of the same unprefixed shape:
`cli.py:59`, `heal.py:78`, `heal.py:155`, `post_wire.py:308`, plus
`post_wire.py:514` which writes `iter-{n:03d}-graph.json` straight into the
directory with no merge step at all. This *strengthens* the finding rather
than weakening it: the unscoped format is more widespread than the kid
measured, and `post_wire.py:514` is the concrete unprotected-artifact write
that sibling `experiment:a00-db9ea0ae-d8251b` predicted from the other side.

No site formats or parses a loop prefix anywhere. `driver.sh`'s own loop
(`for i in $(seq 1 "$MAX_ITERS")`) always starts `i` at 1 per invocation — the
loop-scoped `L1.NN` numbering that produced this session's own iteration
(`1039`) is coming from whatever external harness calls `dispatch.py
<root> <iter_n>` with a monotonic `iter_n`, not from anything inside this
repo's `bin/`.

Then read the allocator itself: `dispatch.py:315` and `cli.py:522` both do
`iter_dir.mkdir(parents=True, exist_ok=True)` — no check that the directory
is new — and every write into it goes through `_merge_manifest`
(dispatch.py:166-193), which re-reads `manifest.json` if present and merges
new agent records **by `id`** into the existing `agents` list.

## Evidence

- No `L<loop>` prefix exists in `iter-{n:03d}` at any of the three
  call sites (`cli.py:521`, `dispatch.py:314`, `zoom.py:462`) — the
  hypothesis's testable claim describes a format that is not implemented.
- `iter_dir.mkdir(..., exist_ok=True)` (dispatch.py:315, cli.py:522) means a
  second call with the same `iter_n` — e.g. two different callers/loops that
  land on the same zero-padded number — does not fail or warn, it writes into
  the same directory.
- `_merge_manifest` merges `agents` **by id** (dispatch.py:172-175 comment,
  186-193 body): if a second dispatch reuses an `iter_n` already on disk and
  mints an agent id that collides with one already recorded there, that
  agent's manifest record is silently overwritten in place rather than
  rejected.
- `.agi/sessions/` on disk today mixes both regimes: 3-digit legacy dirs
  (`iter-001`..`iter-108`) and 4-digit dirs (`iter-1002`..`iter-1039`), all
  produced by the same unprefixed `f"iter-{n:03d}"` format (Python's `:03d`
  just widens past 3 digits, it doesn't collide these two ranges) — so no
  observed collision yet, but that is because the external caller has kept
  `iter_n` monotonic by convention, not because the code enforces it.

**Net result:** the "cannot clobber" half of the hypothesis is not backed by
a guard in the code today — it holds only as long as whatever calls
`dispatch.py`/`cli.py` never repeats an `iter_n`. The "loop-scoped ids,
L<loop>.<nn>, end to end" half is not implemented at all in `cli.py`,
`dispatch.py`, or `zoom.py`. This disproves the hypothesis as stated for the
current codebase; the sibling experiments under this hypothesis should check
whether a guard/allocator was added elsewhere (e.g. a wrapper outside
`extensions/agi/bin/`) before this is taken as fully disproved.


## Agent Notes
cli.py/dispatch.py/zoom.py have no L<loop>.<nn> prefix anywhere; iter_dir.mkdir(exist_ok=True) + merge-by-id in _merge_manifest means clobber is prevented only by external caller convention, not by a code guard

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-26a8af2c, iter 1039). Re-ran the kid's grep unscoped and
found four further `iter-{n:03d}` sites the kid's four-file grep missed
(`cli.py:59`, `heal.py:78`, `heal.py:155`, `post_wire.py:308`, `post_wire.py:514`),
so "exactly three call sites" was corrected to "three in the four files
grepped" plus the wider list. Everything else was verified against source and
left as written: `driver.sh:239` really is `for i in $(seq 1 "$MAX_ITERS")`,
`_merge_manifest` (dispatch.py:166+) really does re-read under lock and merge
by agent id, and no `L<loop>` prefix exists anywhere. Verdict kept at
inconclusive_lean_disproved:70 rather than promoted to `disproved`: the kid
read code, it did not run the falsifier the hypothesis names (populate a
sessions dir, run the allocator, assert untouched), so a decisive verdict
would outrun the evidence this node actually carries.
<!-- THOUGHT:END -->