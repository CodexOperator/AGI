---
id: goal:g4.18.6
mint_id: 42b7cca41632462999d8d20d2bca3092
type: goal
parents:
  - goal:g4.18
next_edges: []
confidence: 0.75
edited_by: alive
goal_id: G4.18.6
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: ad1e7e3cc0b0e998
season: 2
seeds: []
status: active
tags:
  - engine
  - links
  - write-path
  - owner
title: "\"G4.18.6: links are raw mint ids -- the renderer resolves names, titles and visibility; a write checks its outbound ids by lookup; no link ever needs re-pointing and the full walk leaves the write path\""
town: core
---
# goal:g4.18.6

# goal:g4.18.6

## OWNER 2026-09-29 17:4xZ, verbatim (Prime pane)
"Can links be simplified to not need a separate run? It also walks the entire graph when it really just needs to walk the neighborhood of the new nodes no? Idk couldn't write set parents/links as part of write and save all that graph walking since we know what node we are writing and under which parent node it's nested or chained off from"

## Why this exists
goal:g4.18: write.py is the one writer, so it knows the node, its parents and the ids its body names at the moment of the write. Measured 09-29: `links.py links` walks every node (4966 resolved, 42.1 s inside PASS B2's verify), while one write changes only one node's neighbourhood. The spawn gate already resolves parent TYPES at create (SPAWN-GATE APPROVED … allowed_parents), so outbound resolution at write time exists in part.

## Target end-state
- Links are RAW MINT IDS only: `parents`, `next_edges` and every machine reference in a body store the node's mint id (any string that IS a live node's mint_id, never a 32-hex shape check: belam signed [decision] 22:1xZ 09-29 accepted 8 off-shape mints; see goal:g4.18.6.1) (prose refs as a marker the renderer resolves; owner quotes stay verbatim). The address (`goal:g7.16.1`) becomes display-only, so a renumber, move or retire never breaks a link and nothing is ever re-pointed.
- The READ and RENDER paths resolve each mint id to the node's current address, title and status, and decide visibility per view (live shown, retired dimmed or hidden); every read goes through the RENDER path, never write.py (owner 18:0xZ: write has no read path), and it prints names, never bare hex.
- A write checks its outbound mint ids in the same step (a set lookup, not a walk); a write naming a missing id is refused.
- The whole-graph walk leaves the per-write path: at merge gates only, over the merge's changed nodes.

## Invariants
- broken links = 0 on every branch head; a write that would break one is refused, never committed.

## Falsifier
1. A committed test: a write naming a missing parent is refused; a retire of a node with a live referrer re-points it or is refused; neither walks nodes outside the neighbourhood (count the reads).
2. Negative: no verify level runs `links.py links` over the full graph per write.

## Out of scope
goal:g4.18.5 (rows + a write is a commit: this leaf rides on it) · goal:g4.18.3 · goal:g4.18.4.

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 2026-09-29 17:5xZ, verbatim (Prime pane): "Can links just use raw mintIDs only? And things like renderer can render correct parent names and which ones should be visible vs not on render?" -- this version replaces the neighbourhood re-pointing design with mint-id links: the inbound half of the link problem disappears, since a mint id never changes; the renderer owns names and visibility. || This version (alive, council, 22:1xZ): Target bullet 1 said "store the 32-hex mint id", contradicting the Prime's signed [decision] 22:1xZ 09-29 (8 off-shape mints accepted; the gate is "is a node's mint_id", never a shape check), which director-general-1 already applied on the W2 leaves (7cf590f0d) and goal:g4.18.6.1 states; flagged by director-general-1. One source now: this line points at goal:g4.18.6.1. The built resolver links.py:431-432 still raises "not a 32-hex mint id" -- a residue with director-general-3, not edited here.
<!-- THOUGHT:END -->
