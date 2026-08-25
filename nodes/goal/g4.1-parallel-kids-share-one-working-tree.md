---
confidence: 1.0
goal_id: G4.1
goal_kind: subgoal
id: "goal:g4.1"
mint_id: 0ce6a836334e430a9f4a0f59c37ec82a
origin: goals-doc
parents:
  - goal:g4
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G4.1: Parallel kids share one working tree and collide"
type: goal
---

Observed live 2026-08-22, by both kids of the same iteration independently.
Two kids doing **engine** work ran concurrently in one checkout: one was
rewriting `evidence_gate.py`, `metrics.py`, `cli.py` and `post_wire.py` while
the other was running the test suite against them. Consequences seen: the test
suite failed for several minutes on code neither kid had broken, and
`evidence_fraction` flipped between 0.365 and 0.035 on an unchanged corpus —
a stale-`.pyc` race against a file being rewritten underneath the interpreter.

Both kids diagnosed it correctly and neither corrupted anything, so the cost
this time was wasted motion and a briefly false test signal. **The failure
mode is that a kid reports a red suite it did not cause, or a green one it did
not earn.**

Kids writing *nodes* are naturally isolated — one file each. Kids writing
*engine code* are not isolated at all, and the closed loop (G6) makes engine
work the normal case rather than the exception.

Options, undecided: give each engine-writing kid its own worktree
(`isolation: worktree` already exists in the dispatch layer); serialise
engine-writing kids within an iteration; or partition by file ownership
declared in the brief. Measure before choosing — the worktree option costs a
checkout per kid and may not be worth it at two kids.

**Partial result, 2026-08-22:** file ownership declared explicitly in the brief
was tried across two iterations of two kids each. No collisions, and both kids
correctly attributed sibling breakage instead of claiming it. That is one
data point at two kids on disjoint files, not a solution — it says nothing
about kids that genuinely need the same file.
