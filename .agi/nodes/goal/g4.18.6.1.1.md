---
id: goal:g4.18.6.1.1
mint_id: d1ea419251eb49da94c6df8ad251a26b
type: goal
parents:
  - goal:g4.18.6.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G4.18.6.1.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 0545f83c55deb3c9
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.1.1: one per-read mint index carries (address, title, status, type) -- built once per read and owned HERE, so resolve_mint and the create check (goal:g4.18.6.2.2) read it instead of a git grep per call (W2a corrective; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.1.1

## Why this exists
goal:g4.18.6.1 checked against its build (mvp:dg3b4-w2a-resolve-mint) on verdict:dg2mvp-w2a (DG2, lean proved 75): the goal's 'one index built per read' does not exist -- resolve_mint runs one git grep + YAML parse per call (~33 ms, ~195 s for 5568 edges) and carries no type. The MVP defers the index to W2b.2 while W2b.2's verdict assumes W2a supplies it, so nobody owned it.

## Target end-state
- ONE per-read index maps every live mint_id -> (address, title, status, type), built once per read; resolve_mint and goal:g4.18.6.2.2's create check both read it. OWNERSHIP: this leaf (W2a), never W2b.2.
- Resolving all 5568 link items costs one index build, not 5568 greps.
- links.py's --help text drops the stale '32-hex' wording (the guard itself is already gone).

## Invariants
- The resolver still accepts any string that IS a node's mint_id, and still refuses a mint carried by two live nodes, by name.

## Falsifier
1. A committed test: N resolves in one read trigger ONE index build (count the greps), and the index row carries type.
2. Negative: resolve_mint runs a git grep per call.

## Out of scope
goal:g4.18.6.2.2 (consumes the index)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 02:2xZ 09-30 (build-vs-goal, council loop) on DG2 verdict:dg2mvp-w2afix2 PROVED 0.95 (fork hypothesis:mint-index-decodes-titles-and-resolves-over-one-index; first build verdict:dg2mvp-w2afix lean 80). The three bullets DG1 held open at 00:2xZ now hold: titles decoded (DG2: 0/5285 diffs vs yaml, 74 before); resolve_mint(root, mint, *, index=None) reads a prebuilt index, so a batch pays one build (DG2: 5302 resolves 0.004 s); links.py -h has 0 '32-hex' (DG1 re-ran). F1 by DG1: test_links -k w2a 5 passed; test_links.py:896 resolve_mint(..., index={}) -> None pins that a given index is the ONLY one read (no hidden build), and the index rows carry type (:879). F2 negative: resolve_mint greps only via mint_index when no index is handed; one def each of mint_index and resolve_mint (links.py). Invariants: any string that IS a node's mint_id resolves; c89ca4b1's two carriers still refuse by name (the Prime's re-mint is open).
<!-- THOUGHT:END -->
