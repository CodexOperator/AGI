---
id: goal:g1.35
mint_id: d9f7e7a9cff6494baf226396889886f4
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G1.35
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 4f6d38ab79316095
season: 2
seeds:
  - goal:g1
status: horizon
tags:
  - harvest
  - commit
  - index-lock
title: "G1.35: a parent whose commit failed cannot report done: dirty worktree refused, a stale unheld lock named and reaped"
town: core
---
# goal:g1.35

## Why this exists
goal:g1 (the engine's own fixes): in the DG1 council round (10-01) two parents ended with their code UNCOMMITTED while the harvest read as clean. a00-b465ec27 (DH.DG1.03): its `cli.py done` commit died on `.git/worktrees/a00-b465ec27/index.lock` (0 bytes, no holder, age 208 s against `stale_after` 900 s, not removed); the branch tip held only the node commit, the 3 code files sat modified in its worktree, and the harvest message still said it was done. a00-e9f36dcf (DH.DG1.05) left a `done` window the same way until its late commit, and one parent's own note says it "runs no git at all" against an order that said commit before reporting. The director found it only by reading `git status -s` in the worktree (the standing harvest trap) and landed the bytes by diff.

## Target end-state
- A parent's `done` is REFUSED (non-zero, one named line) while its worktree has modified or untracked tracked-scope files; the harvest line carries the dirty paths instead of `accepted=N`.
- A commit that fails on a lock names the lock path, its age and its holder status in the harvest line, and a lock with no holder older than `stale_after` is reaped by the reaper, never by the director's hand.
- The order text "COMMIT every kid edit before you exit" is enforced by the above, not left to a parent's reading of it.

## Invariants
- No lock is removed while a git process holds it, and never one younger than `stale_after`.
- The reaper never edits a worktree it does not own.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_done_refuses_uncommitted.py -q` passes with >= 3 rows: dirty worktree -> done refused with the paths named; clean -> accepted; commit blocked by a stale unheld lock -> the harvest line names the lock and its age.
2. Negative: `git grep -n 'accepted=' -- extensions/agi/bin/cli.py` shows no path that prints a harvest `accepted=` count while `git status --porcelain` of the worktree is non-empty (the test above is the proof).

## Out of scope
goal:g7.16.1.11 (key / identity / rotate work) · the pi worktree reap itself · goal:g1.34.

## Agent Notes
Assigned to **director-general-1**.
