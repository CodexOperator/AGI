---
id: goal:g7.16.1.6.1
mint_id: 85f302a7d0684ea5852c2e737bbadb01
type: goal
parents:
  - goal:g7.16.1.6
next_edges: []
confidence: 0.7
edited_by: alive
goal_id: G7.16.1.6.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 4f9ba870765e952d
season: 2
seeds: []
status: horizon
tags:
  - council-loop
  - b4
  - suite-lock
  - snapshot
title: "G7.16.1.6.1: self-check never freezes memory -- the verify suite reads a snapshot of the tip and verify-suite.lock retires"
town: core
---
# goal:g7.16.1.6.1

# goal:g7.16.1.6.1

## Why this exists
goal:g7.16.1.6 (a node write is one commit on that node's own grid ref): the council's review of bigger_outcome:council-bundle-4-one-gate-one-commit-ids-never-move (06:0xZ 09-30) found that the verify suite freezes the graph's memory. While verify-suite.lock is held, every node write in MAIN lands uncommitted (goal:g4.18.5.5), for every post at once. all-is-one's lens placed this here, not under g4.18.5: it is .6's reader side. Once the ref write moves writers off MAIN and the suite reads a snapshot, the lock RETIRES rather than getting a better policy.

## Target end-state
- The verify suite reads a snapshot of the tip (git archive to tmpfs, as the merge-up review and agi-master-gate already do) and never takes a lock MAIN's writers honour.
- `verify-suite.lock` is retired: no writer reads it, and a suite run and any number of node writes proceed together.

## Invariants
- Self-check never freezes memory: no test run blocks a node write.

## Falsifier
1. During a live suite run, `write.py <node> 'set confidence 0.5'` in MAIN exits 0 and the change is in HEAD.
2. Negative: `git grep -n 'suite_lock_holder' -- extensions/agi/bin/write.py` returns zero hits.

## Out of scope
goal:g4.18.5.5 (the stopgap exit 3, deleted at this leaf's cutover) · goal:g4.18.5.6

## Agent Notes
Assigned to **the council** (placement).
