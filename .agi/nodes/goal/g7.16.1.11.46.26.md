---
id: goal:g7.16.1.11.46.26
mint_id: ef1b16267d284293b00decc319084b55
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.26
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - M10
season: 3
status: active
title: "G7.16.1.11.46.26: M10 -- an OWNER block in a goal cites the chunk id(s) of the owner's words"
town: local-maxxing
---
# goal:g7.16.1.11.46.26

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §40. Split from V4 + M9 + M10 (sp 6). Builds on M7's chunk->atom edge (goal:g7.16.1.11.46.14).

## Target end-state
- Every `## OWNER ... verbatim` block written after this leaf lands cites the chunk id(s) of the owner's words in the M6 store.

## Invariants
- Blocks written before this leaf are grandfathered and named as such, never rewritten.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/owner-cite.t.sh` exits 0: a new OWNER block with a valid chunk id passes; mutant: an OWNER block with no chunk id reads RED; a cited id absent from the store reads RED.
2. Negative: the check's grandfather list is a committed file of node ids, never a pattern.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
