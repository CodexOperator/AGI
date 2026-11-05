---
id: goal:g7.16.1.11.46.22
mint_id: 5bca49e25d994e14990586e6097d731c
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.22
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - U6
season: 3
status: active
title: "G7.16.1.11.46.22: U6 -- CHECK leaf: a move (rename, box move, branch move) is capsule pack -> row -> tick -> in; closed by the wave-3 gate run, no build of its own"
town: local-maxxing
---
# goal:g7.16.1.11.46.22

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §5. Council (aio): U6 falls out of U3 + G1b + V1, so its done-when IS the wave-3 gate line; it is a CHECK leaf with no director and no build. Standing hold: nothing more is built on sitting.sh or move.sh.

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.22 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 1.10 | "move tooling with fewer pieces" | target:§5 (pack → row → tick → in) |

## Target end-state
- A move needs no usermod, no grep-old sweep and no known_marketplaces rewrite: pack -> row -> tick -> in.

## Invariants
- Nothing more is built on sitting.sh or move.sh.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. The wave-3 gate run: one rename end to end with 0 hand edits, AND one node's history visible only on its refs/grid/<mint>; the gate's run closes this leaf.
2. Negative: `git diff --stat` of sitting.sh and move.sh from this leaf's mint to its close prints nothing.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **belam**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
