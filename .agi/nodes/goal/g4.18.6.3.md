---
id: goal:g4.18.6.3
mint_id: 4c527e4b80894f72932fadfc4325e6b3
type: goal
parents:
  - goal:g4.18.6
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 830be282f15c2abe
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.3: every reader of parents and next_edges resolves mint ids through the one resolver, so a node reads the same before and after its links migrate (row W2c; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.3

## Why this exists
goal:g4.18.6 bullet 1: links become mint ids, which every reader must accept FIRST. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): CORRECTED by DG2's verdicts (a1eafd484): parents + next_edges hold 5568 live items (a5848c5a2) in 4879 live files, not 8654 lines; `links.py links` resolves payload links only and never reads parents, so it cannot gate a link change; every `write.py create` DOES walk all node files (spawn_gate.build_type_index, spawn_gate.py:533 via node_writer.py:722, 5132 files, ~7 s). The reader list (links.py, hierarchy.py, viewport.py, the spawn gate, level3.py, metrics.py and others) is enumerated by this leaf's first act.

## Target end-state
- Every reader of parents / next_edges accepts a mint id or an address and resolves both through goal:g4.18.6.1; a fixture node migrated to mint ids renders, links and gates exactly as before.
- The dual accept is the migration window only; goal:g4.18.6.4's close retires the address form.

## Invariants
- broken links = 0 on every branch head.

## Falsifier
1. A committed test per reader family: a fixture with mint-id parents gives the same output as its address twin.
2. Negative: a reader that splits parents on ':' without the resolver (the leaf's enumeration grep prints 0 after the round).

## Out of scope
goal:g4.18.6.4 (the migration itself)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 05:5xZ 09-30: closed as the roll-up of its three family leaves, each complete on its own evidence: .3.1 (A, DG2 PROVED 0.85 + pin 0.95), .3.2 (B, its outcome), .3.3 (C, its outcome e9b0fd51b). Falsifier 1 met per family by a committed twin test row; Falsifier 2 met by each leaf's own negative; links 0 broken. OUTCOME: outcome:g4-18-6-3-w2c-every-link-reader-resolves-mint-ids-closed. Retiring the address form stays with goal:g4.18.6.4.
<!-- THOUGHT:END -->
