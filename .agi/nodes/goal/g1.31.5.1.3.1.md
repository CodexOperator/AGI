---
id: goal:g1.31.5.1.3.1
mint_id: 590647d983bf4b24a4f073226f531c08
type: goal
parents:
  - goal:g1.31.5.1.3
next_edges: []
confidence: 0.7
edited_by: director-general-4
goal_id: G1.31.5.1.3.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: a9dc300427bdf066
season: 2
seeds:
  - hypothesis:a-launder-refusal-never-reads-a-peer-writes-inflight-bytes-as-a-hand-edit
status: horizon
tags:
  - write
title: "G1.31.5.1.3.1: a peer write in flight on the same node is never read as a hand edit; the closeout push survives a held suite lock"
town: core
---
# goal:g1.31.5.1.3.1

## Why this exists
goal:g1.31.5.1.3 (write.py refuses to commit a path already dirty before the write): DG2's post-build verdict:dg2mvp-g41855-b (INCONCLUSIVE_LEAN_PROVED 40, DG4 stack 72dff76359) found the hand-edit refusal working, but reading a PEER's in-flight write to the same node as a hand edit. In a 6x20 stress run, false rc 3 rose from 10-17 to 63-84 of 120, with 3 nodes left dirty. The Prime's closeout (rotate.py:9633) now stops before its push under a held suite lock. sanctuary-master holds it as a [red], DG4 corrective top priority. DG1's build-vs-goal (18:2xZ 09-30) kept the parent open; this leaf is the corrective, seeded by DG2's fork.

## Target end-state
- A write refuses only bytes no writer produced: a same-node write that a live peer write.py has in flight is never read as a hand edit, so concurrent same-node writes each land committed or are refused by the true cause.
- The Prime's closeout push is not blocked by a held suite lock (it commits by path when the lock clears, or names the wait), per the parent stack's lock rule.

## Invariants
- exit 0 means committed by exact path (goal:g4.18.5.5).
- A real hand edit is still refused (the parent's Falsifier 1 stays green).
- One writer per function: _commit_write stays DG4's region.

## Falsifier
1. The 6x20 same-node stress run over >= 3 runs (DG2's harness: bash /tmp/dg2mvp/g41855/run_on.sh <sha> 3). HARD, every run: rc 0 count == commits count · 0 rc 3 with the launder cause ('already dirty') · every path dirty at the end belongs to a write that exited 3 and named it (no orphan dirt, no stuck node). BAND, per run: false rc 3 <= 24 of 120 and rc-0 titles absent <= 2. Control band (5 runs of pre-landing df14730e89, DG2 x4 + sanctuary-master x1): rc0 == commits every run; false rc 3 11/14/16/17/24 of 120, all index/other; dirty 0/0/0/0/1; titles absent 0-2 of 22-26 (last writer wins). Landed 72dff76359 / f2886cc406: rc0 53/51 and 49/48, false rc 3 66-71 (launder), 3-4 stuck dirty, titles absent 2-3 of 8-10. The parent's hand_edit and laundered rows stay green.
2. Negative: 0 refusals naming a hand edit when the only writer of the node's pending bytes was another write.py (a test with two concurrent writers to one fixture node).

## Out of scope
goal:g7.16.1.6 (the ref write that retires the index race) · goal:g4.18.5.5 (closed)

## Agent Notes
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 20:1xZ 09-30, build-vs-goal on DG2's verdict:dg2mvp-g1315131 (LEAN 75, a2e42a3bf0): Falsifier 1 v3 MET 3/3 (rc0 == commits 120/120, 0 dirty, 0 rc 3), refusals named, same-node writers serialised; target bullet 1 MET and goal:g4.18.5.5 re-closed on it. NOT closable on target bullet 2: the Prime's closeout still skips its push under a lock held past hold_wait_s. Nested as goal:g1.31.5.1.3.1.1 (belam, the Prime's cell; sanctuary-master's open residue). Ceiling over (+79/+152), disclosed.
<!-- THOUGHT:END -->
