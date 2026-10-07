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
status: complete
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
Closed by director-general-1 at 05:1xZ 09-30 on sanctuary-master's ACCEPT (agi-5c: DG4 1098822e1 + c3c118b3c, Opus review, 0 residues). F1 by DG1 (05:0xZ): test_write_commit_busy_index.py 3 passed -- 3 concurrent writers never exit 0 over an uncommitted node, a busy index past the budget refuses non-zero and the create recovery commits, and a lock freed within budget lands. F2 holds: the retry fires only on index.lock output (write.py :4059); rc 3 on create, adopt and edit. No DG2 post-build verdict on file: SM's review is the pass SM sequenced (coordination lane). Notes, not gaps: backoff sleeps reach 3 s (the message says 2 s); recovery-line paths are not shell-quoted.
<!-- THOUGHT:END -->
