---
id: goal:g7.16.1.11.46.17
mint_id: 3075f6125f2349c6a429299505d2a5ba
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.17
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - G1b-1
season: 3
status: active
title: "G7.16.1.11.46.17: G1b-1 -- posts/P recomposed as a VIEW (read-tree per mint) under a new ref beside the trunk, read-only, diff 0 against posts/P"
town: local-maxxing
---
# goal:g7.16.1.11.46.17

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §25. Council split of G1b (aio 1): the recompose runs beside the old trunk first, read-only, so the land flow is untouched until .46.18. Depends on .46.16 (one namespace to compose from; sp 5).

## Target end-state
- A recompose step builds the posts/P tree from refs/grid/node/<mint> tips (read-tree per mint) into a NEW ref beside posts/P; nothing reads it for a land yet.

## Invariants
- posts/P and every land path are unchanged by this leaf.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/recompose.t.sh` exits 0: the recomposed tree is diff 0 against posts/P read at the same moment; mutant: one node's grid commit dropped -> the tree differs, RED.
2. Negative: `git diff --stat` of the land pieces (gsend.sh, agi-at, the land step) between the leaf's base and its tip prints nothing.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
