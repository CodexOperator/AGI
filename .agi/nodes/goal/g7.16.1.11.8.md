---
id: goal:g7.16.1.11.8
mint_id: 913dfa27239b46dfa8f39333e92538ad
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.8
goal_kind: subgoal
origin: owner
scaffold_hash: 9ccf9843db930b04
season: 2
seeds: []
status: active
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.8: ROUND 7: GROWTH ORDER kept by the new engine itself -- node keys from the schemas' parent shapes, a captive fill window, row-by-row checks, local models under a schema grammar"
town: core
---
# goal:g7.16.1.11.8

## Why this exists
Parent goal:g7.16.1.11: belam measured 07:1xZ: parity row 20 (spawn gate, schemas) is MATCH only because the old write.py runs in the clone -- so this leaf gates phase 3.
## Target end-state
ROUND 7: GROWTH ORDER kept by the new engine itself -- node keys from the schemas' parent shapes, a captive fill window, row-by-row checks, local models under a schema grammar.
## Invariants
a node add out of schema order is refused by the engine, without the old Python.
## Falsifier
1. parity row 20 reads MATCH with write.py absent from the clone
2. negative: a node minted out of order: zero
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"we should make sure the engine still maintains graph growth order so posts can't just grow nodes without respecting order" (owner 07:1xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **council**.

belam-s2-II 08:3xZ 10-10 LANE (Prime, write-gate class): DG2 08:25Z bytes -- on v5 the plain path (Write/Edit + agi-turn/agi-at) has NO growth-order gate (spawn_gate.check_spawn runs only inside write.py/cli.py create; an out-of-order build node was accepted). DG3 builds the check into agi-turn for NEW node files only (reuse check_spawn; edits never gated); DG2 rows (refuse / legal control / edit control). After the season-close leaves.
