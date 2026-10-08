---
id: goal:g7.16.1.11.6
mint_id: 86bb96dc51564583af3ce35d14aed5a1
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.6
goal_kind: subgoal
origin: owner
scaffold_hash: 7a0a0fb84078f21d
season: 2
seeds: []
status: active
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.6: ROUND 6: the SEED = one script <= 1,024 B + one expansion matrix; local first, a timed remote sync, conflicts to the Prime, no remote = local read-only + a first-boot owner greeting"
town: core
---
# goal:g7.16.1.11.6

## Why this exists
Parent goal:g7.16.1.11: §S (4542be3cc) + §T (c3e43efc3) of doc:radically-simple-engine: script 1,019 B, matrix 100 B, P2-P5 PASS on scratch.
## Target end-state
ROUND 6: the SEED = one script <= 1,024 B + one expansion matrix; local first, a timed remote sync, conflicts to the Prime, no remote = local read-only + a first-boot owner greeting.
## Invariants
the seed runs fetched code only after verify-commit against the anchor; HEAD is never moved by a conflicting merge.
## Falsifier
1. DG5 boots from the seed alone (T6) and the four paths re-run PASS
2. negative: an unsigned tip merged: zero
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"So first a local check to have something at least then it initiates a remote sync on local with timeout, and hands sync conflicts to prime post once it's up." (owner 06:2xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.
