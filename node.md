---
id: goal:g4.18.6.4
mint_id: 3e9ff27780dc4dba9529706c07609ad4
type: goal
parents:
  - goal:g4.18.6
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.4
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: c24daa52235904bc
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.4: the link lines store mint ids -- a counted migration, one type dir per round, links 0 broken after each, owner quotes and prose untouched (row W2d; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.4

## Why this exists
goal:g4.18.6 bullet 1. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): CORRECTED by DG2's verdicts (a1eafd484): parents + next_edges hold 5568 live items (a5848c5a2) in 4879 live files, not 8654 lines; `links.py links` resolves payload links only and never reads parents, so it cannot gate a link change; every `write.py create` DOES walk all node files (spawn_gate.build_type_index, spawn_gate.py:533 via node_writer.py:722, 5132 files, ~7 s).

## Target end-state
- Every parents / next_edges item and every machine reference stores the node's mint id as found (the 8 off-shape mints accepted, belam [decision] 22:1xZ: a gate checks 'is a node's mint_id', never a 32-hex shape); prose references and owner quotes stay verbatim.
- Prerequisites: goal:g4.18.6.4.1 (data repair) and goal:g4.18.6.4.2 (the writers). One type dir per round, each with a before/after count gate and a parents-aware unresolved count (baseline 1, 0 after goal:g4.18.6.4.1); after the last round the address form in link fields is retired (goal:g4.18.6.3's dual accept closes).

## Invariants
- active + deprecated node count never drops; the parents-aware unresolved count never rises after a round.

## Falsifier
1. The parents-aware unresolved count does not rise after each round (links.py never reads parents), and the round's count gate matches (link lines before = mint-id lines after, for that dir).
2. Negative: a parents / next_edges item in `.agi/nodes` that is not a node's mint_id after the last round.

## Out of scope
goal:g4.18.6.5 (the re-point rule retires after this)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-scoped by director-general-1 (20:5xZ 09-29) on verdict:dg2b4-w2d: the count is 5568 live items, not 8654 lines, and links.py never reads parents, so the gate is a parents-aware unresolved count (baseline 1). Conjunct (4) moved to two prerequisite leaves, goal:g4.18.6.4.1 (data repair: 1 dangling item, 8 off-shape or duplicated mint_ids) and goal:g4.18.6.4.2 (the 5 address-minting writers). Hypothesis: link-lines-migrate-to-mint-ids-counted.
<!-- THOUGHT:END -->
