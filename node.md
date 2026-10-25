---
id: goal:g7.16.1.11.46.24
mint_id: a4225584dfb046e49a8ed70f26ffbc72
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.24
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - V4
season: 3
status: active
title: "G7.16.1.11.46.24: V4 -- mem: horizons on the M6 store, claude-code adapter only: a new goal resets a director's store and the old one becomes a nest: container"
town: local-maxxing
---
# goal:g7.16.1.11.46.24

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §40, §11. Split from V4 + M9 + M10 (sp 6: agi-goal §3 asks for ONE target end-state per leaf, and the gating differs). Builds on M6 (goal:g7.16.1.11.46.13) and M7 (goal:g7.16.1.11.46.14). The pi adapter stays wave 4. Owner atom 10.1 (the adapter half) closes on this leaf.

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.24 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 10.1 | "the owner-facing post gets a full optmem/chat memory beside the atoms (via pi-optchat or UniiChat if needed)" | target:§40 V4 pulled forward, claude-code adapter (W2); no routing: the store is ours, harnesses are adapters |

## Target end-state
- The `mem:` cell carries horizons in OptChat's shape on the M6 store, through the claude-code adapter.
- A director's store resets at a new goal; the old store is a `nest:` container, still readable.

## Invariants
- The store is ours; a harness is an adapter (no routing).
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/mem-horizon.t.sh` exits 0: a goal change resets the store and nests the old one, whose tip is unchanged; mutant: a reset that drops the old store reads RED.
2. Negative: no pi adapter file is added by this leaf.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
