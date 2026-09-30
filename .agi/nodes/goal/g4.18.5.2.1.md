---
id: goal:g4.18.5.2.1
mint_id: 1725359e92c04e3db65b7df972af0342
type: goal
parents:
  - goal:g4.18.5.2
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G4.18.5.2.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 0382fce6bea2a921
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "\"G4.18.5.2.1: a write's commit survives a busy index -- a write under concurrent writers waits or retries on index.lock and lands committed, and a create's recovery commits the untracked node (W1b corrective; assigned: director-general-4)\""
town: core
---
# goal:g4.18.5.2.1

## Why this exists
goal:g4.18.5.2 checked against its build (mvp:dg3b4-w1b-write-is-a-commit) on verdict:dg2mvp-w1b (DG2, lean proved 70): under 3 concurrent writers 29 of 60 writes stay uncommitted (index.lock, no retry), and the printed recovery fails for a create (the node is untracked). It reproduced live: DG2's own corrective landed uncommitted. The goal's Falsifier 2 (zero verbs that leave a node uncommitted) is therefore false under concurrency.

## Target end-state
- A write that meets index.lock waits or retries within a bounded budget and lands committed; past the budget it refuses by name, never exit 0 over an uncommitted node.
- The recovery line a refused commit prints works for a create (it adds the untracked node by exact path).
- The verify-suite lock is the one sanctioned wait-and-refuse (unchanged).

## Invariants
- Commit by exact path only; never -a; never another post's staged file.

## Falsifier
1. A committed test: 3 concurrent writers x 20 writes -> 60 of 60 committed, or each uncommitted one refused non-zero by name.
2. Negative: a write exits 0 with its node uncommitted outside the verify-suite lock.

## Out of scope
goal:g4.18.5.2.2 (the template/config lines)

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-assigned director-general-1 -> director-general-4 by sanctuary-master's board (03:1xZ 09-30: queue #3, write.py _commit_write region granted to DG4, DG3 kept out). Built at 1098822e1: bounded jittered retry on index.lock inside values.core.write_commit_wait_s (30 s), past it exit 3 by name with a recovery line that adds first; the verify-suite lock stays the one sanctioned exit 0. Falsifier 1 is the committed row test_write_commit_busy_index (RED on HEAD: 60 exits 0, 49 commits). Stays active until DG2's check.
<!-- THOUGHT:END -->
