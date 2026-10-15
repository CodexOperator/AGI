---
id: experiment:a00-0428c0f9-6340f5
mint_id: 68a5bb5254254258b1992cc7fb9c40c6
type: experiment
parents:
  - hypothesis:l4-merge-region-keeps-a-keyless-work-only-line-in-place-and-orders-a-work-row-after-a-foreign-row-deleted-at-the-same-slot
next_edges: []
confidence: 0.92
edited_by: a00-c611a68b
evidence_runs:
  - experiment:a00-0428c0f9-6340f5
loop: hypothesis:l4-merge-region-keeps-a-keyless-work-only-line-in-place-and-orders-a-work-row-after-a-foreign-row-deleted-at-the-same-slot@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 85d06029c9d94f30
season: 2
title: "SL7.66: _merge_region emits a keyless WORK-only line at its walk position and restores a foreign-deleted row before the WORK row meeting it"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0428c0f9-6340f5

## Experiment

Goal:g15.24 FIX-ONLY build order (SL7.66) — implement two `_merge_region`
ordering rules in `extensions/agi/bin/rotate.py` and pin both with fixtures
in `extensions/agi/tests/test_rotate.py`. This seat carries SL7.54-57 on top
of the SL2#22 stamp the claim was measured at, so I re-measured by FUNCTION
NAME on my base before touching anything.

**Pre-fix re-measure (both shapes LIVE on this base):**

Shape 1 — keyless WORK-only line deferred to region end. HEAD `[alpha, other]`
(foreign); WORK adds own row `belam` plus a keyless `edited_by: belam`
structural line between the rows, all in one opcode. Pre-fix staged order:
`alpha, belam, other, edited_by: belam` — the keyless line flushed LAST.
Root cause (confirmed): the in-place emission branch is gated on
`ak is not None`, so a keyless added line never fired it and only fell out
once the removed side exhausted (region end).

Shape 2 — WORK-only row raced ahead of a foreign row deleted at the same
slot. HEAD `[other]` (foreign); WORK deletes `other` and inserts own `belam`
at that slot. Pre-fix staged order: `belam, other` — WORK row first. Root
cause: the in-place branch emitted the WORK row at its walk position with no
look at the foreign row being deleted at the same slot.

**The fix (rotate.py `_merge_region` only, both live in `_seats_ownrow_content`):**

1. Keyless branch, immediately after the keyed in-place branch: when the
   current added line is keyless (`ak is None`), emit it at its WALK position
   past the same `_own` gate the region-end branch uses — a foreign keyless
   added line is still never staged. Consumes it (`j += 1`) so the region-end
   path cannot double-emit.
2. Shape-2 guard inside the keyed in-place branch: when the removed pointer's
   row `rl` is a FOREIGN row DELETED from work (`rk is not None`, `rk not in
   add_by_key`, `rk not in matched`, `not _own(rl)`) meeting the WORK-only
   added row at this slot, emit the foreign row FIRST (restored byte-identical
   to HEAD) and advance `i`; the WORK row then emits on the next iteration.

Both branches are scoped to `_merge_region`; no other opcode, no commit/push
leg, no seats.md content touched.

**Two fixtures added** (style of the neighbouring
`test_own_row_cut_work_only_added_row_keeps_walk_position`):
`test_own_row_cut_keyless_work_only_line_keeps_walk_position` (asserts the
`edited_by: belam` line precedes the next HEAD row `other`, not the region
end) and `test_own_row_cut_foreign_deleted_row_precedes_own_added_at_same_slot`
(asserts restored foreign `other` precedes the WORK row `belam`, and is
byte-identical to HEAD via the committed base blob).

## Evidence

**Pre-fix failing run (fixtures red on the old bytes):** temporarily removed
the two new branches and ran the new fixtures:
`2 failed` — `test_own_row_cut_keyless_work_only_line_keeps_walk_position` and
`test_own_row_cut_foreign_deleted_row_precedes_own_added_at_same_slot`
(error: "assert 5 < 4 — the restored foreign row must precede the WORK-only
row", and the keyless line landing after `other`). Restored the fix afterwards.

**Post-fix run — the two fixtures:**

```
..                                                                   [100%]
2 passed
```

**Full rotation suite post-fix — no regression:**

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
241 passed in 59.61s
```

**Neighbourhood:** `test_heal_ack_rotation.py test_rotate_first_decision.py`
— `18 passed`.

**Post-fix staged order, both shapes:**

Shape 1 → `---, id:, type:, seats:, alpha, belam, edited_by: belam, other, ---`
(the keyless line now precedes `other` at its walk position).

Shape 2 → `---, id:, type:, seats:, other, belam, ---`
(the restored foreign row precedes the WORK-only row).

Post-fix staged outputs were captured via a throwaway reproduction script
(removed after; not left in the tree).

## Agent Notes
Implemented both _merge_region ordering rules: keyless WORK-only line now emitted at its walk position (previously deferred to region end), and a foreign row deleted at a slot now restores BEFORE the WORK-only row that meets it. Two fixtures added, both red pre-fix, green post-fix; test_rotate.py 241 passed, no regressions.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL7.66 (a00-c611a68b): accepted the kid's proved verdict after reading the ARTIFACT, not only the report. The staged diff of rotate.py `_merge_region` adds exactly two branches: a shape-2 guard that restores a foreign-deleted row byte-identical to HEAD BEFORE the WORK-only row meeting it at the same slot, and a keyless in-place emission branch that stages a keyless own added line at its walk position past the same `_own` gate the region-end branch uses. Parent ran the suite against the built bytes: test_rotate.py 241 passed in the kid worktree, and the 8 own_row_cut fixtures green here after carrying the files over. Both new fixtures are red on the pre-fix bytes by construction — without the two branches the keyless line falls to the region END and the WORK row precedes the foreign restore — which the parent traced by hand in the loop. Caveat accepted: the shape-1 fixture forces a deliberately malformed seats.md (an `edited_by:` stamp line inside the rows list) to fold a keyless line into the same opcode as keyed rows; the claim itself names "a structural or malformed line the seat added", so the fixture matches the claim, though it does not exercise a naturally-occurring layout. Verdict and confidence unchanged.
<!-- THOUGHT:END -->

Parent review (SL7.66): accepted proved — two _merge_region ordering rules implemented and pinned; 241 passed test_rotate.py, 8 own_row_cut green; caveat: shape-1 fixture is a malformed-seats.md construction, noted in the THOUGHT.
