---
id: goal:g4.18.6
mint_id: 42b7cca41632462999d8d20d2bca3092
type: goal
parents:
  - goal:g4.18
next_edges: []
confidence: 0.75
edited_by: belam
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
title: "G4.18.6: links are checked by the write over its neighbourhood -- outbound ids resolve, inbound referrers re-pointed in the same commit; the full walk only at merge gates, over the changed nodes"
town: core
---
# goal:g4.18.6

# goal:g4.18.6

## OWNER 2026-09-29 17:4xZ, verbatim (Prime pane)
"Can links be simplified to not need a separate run? It also walks the entire graph when it really just needs to walk the neighborhood of the new nodes no? Idk couldn't write set parents/links as part of write and save all that graph walking since we know what node we are writing and under which parent node it's nested or chained off from"

## Why this exists
goal:g4.18: write.py is the one writer, so it knows the node, its parents and the ids its body names at the moment of the write. Measured 09-29: `links.py links` walks every node (4966 resolved, 42.1 s inside PASS B2's verify), while one write changes only one node's neighbourhood. The spawn gate already resolves parent TYPES at create (SPAWN-GATE APPROVED … allowed_parents), so outbound resolution at write time exists in part.

## Target end-state
- Every write validates its NEIGHBOURHOOD in the same step: its outbound ids (parents, next_edges, ids named in the body) resolve; a retire, move or renumber finds its inbound referrers (`git grep` on the id) and re-points them in the same commit, or refuses by name.
- The whole-graph walk leaves the per-write path: it runs only at merge gates (PASS, master gate), and only over the merge's changed nodes plus their inbound referrers.

## Invariants
- broken links = 0 on every branch head; a write that would break one is refused, never committed.

## Falsifier
1. A committed test: a write naming a missing parent is refused; a retire of a node with a live referrer re-points it or is refused; neither walks nodes outside the neighbourhood (count the reads).
2. Negative: no verify level runs `links.py links` over the full graph per write.

## Out of scope
goal:g4.18.5 (rows + a write is a commit: this leaf rides on it) · goal:g4.18.3 · goal:g4.18.4.

## Agent Notes
Assigned to **director-engine**.
