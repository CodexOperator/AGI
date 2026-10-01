---
id: goal:g7.16.1.11.3
mint_id: 4e6fd028527d411ab7851f14f3956387
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.3
goal_kind: subgoal
origin: owner
scaffold_hash: ab651364d4e6d46e
season: 2
seeds: []
status: active
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.3: stages 1-2.5: the new engine runs a LIVE post -- S1 PASS, S2 PASS 7/7, DG5 up on pi-free with the parity table 55 rows matched-or-better"
town: core
---
# goal:g7.16.1.11.3

## Why this exists
Parent goal:g7.16.1.11: DG3's stages on goal:g7.16.1.11: S1 PASS, S2 7/7 (doc:g716111-stage2-rootplan), 2.5 Phase A/A' (doc:g716111-stage25-rootplan, engine v4c landed by belam e1e0dbaaf).
## Target end-state
stages 1-2.5: the new engine runs a LIVE post -- S1 PASS, S2 PASS 7/7, DG5 up on pi-free with the parity table 55 rows matched-or-better.
## Invariants
every root act has an undo + proof; one-command rollback per post; config:engine byte-exact with the fenced source it was landed from.
## Falsifier
1. the DG5 post unit is active AND `grep -c 'MISSING' .agi/nodes/doc/g716111-stage25-parity.md` prints 0
2. negative: a post of the new engine reading .env: zero hits
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"DG5 yes in pi free lane" (owner 07:0xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.
