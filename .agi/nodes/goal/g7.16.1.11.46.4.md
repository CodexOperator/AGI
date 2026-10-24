---
id: goal:g7.16.1.11.46.4
mint_id: 0ac92fca87e84493ada2e07243b7bb94
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-2
goal_id: G7.16.1.11.46.4
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - M3
season: 3
status: complete
title: "G7.16.1.11.46.4: M3 -- agi-atom move hands a director's atoms to a flow: the slices land byte-equal in the flow's ARGS and the rows close as moved:<flow> in ONE commit; the atoms: MANIFEST line is specified"
town: local-maxxing
---
# goal:g7.16.1.11.46.4

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §39 (routing down the tree). The pack route itself is U3 (wave 2); this leaf lands the shape so U3 only wires it. Doc sections implemented: §39 (routing down the tree) (doc:brainstorm-unify is reference, never placement).

## Target end-state
- `agi-atom move <a-ids> <flow>` writes the slices into the flow step's ARGS verbatim and closes each row as moved:<flow> in the same commit; moved:<flow> joins the closed state set.
- The capsule MANIFEST spec names an `atoms:` section (one line per moved atom: id, src, slice hash); U3 (wave 2) fills it from the pack route.

## Invariants
- An atom is in exactly one place at any commit: a §7 row or a flow's ARGS.

## Falsifier
1. `sh extensions/agi/tests/agi-atom-move.t.sh` exits 0 on a scratch card + flow: §7 shrinks by k, ARGS gain the same k slices byte-equal, the commit count is 1; mutant m (move without the close) reads RED as "atom in both places".
2. Negative: on the scratch tree after the move, `grep -c` of each moved slice over §7 prints 0.

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-2 10-24 (CLOSE; SM [landed] L90 89a1dd7589, standing close form) falsifiers RE-RUN as written at trunk 48cb160d02: F1 `sh extensions/agi/tests/agi-atom-move.t.sh` exits 0 (15 lanes ok: section 7 shrinks by k, ARGS gain the same k slices byte-equal, the commit count is 1; mutant m, move without the close, reads RED as "atom in both places"). F2 negative (the moved slice over section 7 = 0 hits) is a lane of the same script, ok. Deviation recorded at the merge-up: a moved row keeps its id, src and state moved:<flow> but its slice becomes "sha:<12 hex>", so the slice lives in ARGS only. Piece: agi-atom move in engine-post.md (with agi-atom, 5384 B).
<!-- THOUGHT:END -->
