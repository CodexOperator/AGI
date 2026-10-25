---
id: goal:g7.16.1.11.46.25
mint_id: 83498f2d1cb944608363ebb0949ec4c6
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.25
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - M9
season: 3
status: active
title: "G7.16.1.11.46.25: M9 -- a summary tree and a bounded view in agi-brief; the compactor is a pull:none kid, a stub until C1-C3 go live"
town: local-maxxing
---
# goal:g7.16.1.11.46.25

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §40, §11. Split from V4 + M9 + M10 (sp 6). Spend: the compactor rides the credits lane only after C1-C3 go live; until then a stub endpoint, as M2 (goal:g7.16.1.11.46.3).

## Target end-state
- agi-brief renders a bounded view from a summary tree over the M6 store.
- The compactor is a `pull: none` kid on a stub endpoint until credits_live is true.

## Invariants
- No model call is spent while credits_live is not true.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/mem-summary.t.sh` exits 0 on the stub endpoint: the view stays under its bound for a store of any size; mutant: an unbounded view reads RED.
2. Negative: with credits_live false, the stub receives every compactor request and the real endpoint receives 0.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
