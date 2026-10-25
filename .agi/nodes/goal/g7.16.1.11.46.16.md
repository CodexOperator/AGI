---
id: goal:g7.16.1.11.46.16
mint_id: 785a56ca1046434badd968bce6a1719e
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.16
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - G1a
season: 3
status: active
title: "G7.16.1.11.46.16: G1a -- ONE grid namespace refs/grid/node/<mint>, written additively: each diverged pair merged with the live tree, the writer re-pointed in the same land, a five-number census cell"
town: local-maxxing
---
# goal:g7.16.1.11.46.16

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §25, §34.5. Box readings at d2ab3c19b8: 6010 refs under refs/grid/local-maxxing/node and 3807 under refs/grid/node; every one of the 3807 also has a local-maxxing ref, and ALL 3807 pairs have DIVERGED (0 share a tip, neither side is an ancestor); over all 3807, 2073 pairs have equal trees and 1734 do not; refs/grid/node/* has been frozen since 09-21 11:47Z, while local-maxxing is the live writer (newest 10-25 17:32Z); a ref named TBD exists in both namespaces (K2, sp G1a-T). K3: 22 local-maxxing mints have no mint_id in any trunk node file, where the brief says 46. Council picks 3/3: ADDITIVE only (sp 1 over aio's archive move: a move is a delete on the remote); G1a-T and G1a-W (sp).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.16 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 8.1 | "seat_status.py retire" | target:the §34.5 census-cell leaf (wave 2) |
| 4.3 | "census: count tips; old versions as deprecated?" | target:§34.5 (tips yes; versions are commits, not deprecated nodes) |

## Target end-state
- refs/grid/node/<mint> is the one namespace: per mint, its tip is a two-parent merge whose ancestors include BOTH old tips, and whose tree is the local-maxxing tip's tree (the live side).
- grid.py commit and grid_sync's push write refs/grid/node/<mint>, re-pointed IN THE SAME LAND as the merge.
- The census cell carries five numbers (mints · live · retired · versions · orphans), each one git command; the TBD ref is named, and 22 vs 46 orphans is reconciled by ONE pinned command before the cell is trusted.
- refs/grid/local-maxxing/* stays READ-ONLY: no delete is pushed. Its removal is an OWNER act, banked in card-belam §6.
- seat_status.py is retired (owner atom 8.1; status deprecated, moved under deprecated/, never deleted) once the census cell answers what it answered.

## Invariants
- Delete 0: no grid ref is deleted locally or on the remote by this leaf.
- A grid ref outlives its file (CLAUDE.md): retired nodes' refs merge like live ones.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/grid-namespace.t.sh` exits 0: per mint, both old tips are ancestors of the new tip, `rev-list --count` new >= max(old), tree(new tip) == tree(local-maxxing tip at the merge), m/m; mutant: one version dropped makes the census differ, RED; mutant: one 09-21 tree carried on an unequal pair, RED.
2. Read one hour after the land: refs under refs/grid/local-maxxing whose tip changed since the land = 0, and the land's probe edit is ONE commit on refs/grid/node/<mint>; mutant: the writer left alone -> 1 changed, RED.
3. The census cell prints five numbers; a failed git command prints `unread`, never 0; either namespace listing 0 refs prints `unread`, rc 1.
4. Negative: `git push --dry-run` of the land's refspecs lists 0 deletes.

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
<!-- THOUGHT:END -->
