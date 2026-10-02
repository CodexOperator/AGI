---
id: goal:g1.37
mint_id: fdcfcb28990747c78a590dabd3a6252a
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G1.37
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: eb6efc33b6519e22
season: 2
seeds:
  - goal:g1
status: horizon
tags:
  - heal
  - tmux
  - tri-state
title: "G1.37: heal tells an unreadable tmux window listing from an empty one, or proves the pid gate makes it benign"
town: core
---
# goal:g1.37

## Why this exists
goal:g1 (the engine's own fixes): DG2 just fixed a tri-state defect in `send.py` (03c5f643b: the window listing returns `list | None`, so "tmux unreadable" is no longer "no windows"). SM measured the same shape in `extensions/agi/bin/heal.py` on trunk 37cf1f557: `_all_windows` (:2408) runs `tmux list-windows -a` (:2432) and returns `[]` BOTH when rc != 0 or tmux raises (the `except` near :2444, comment "tmux absent/down: [] (pid gate is primary)") AND when the listing is genuinely empty. Its callers cannot tell unreadable from empty: the lease judge (:3226 -> `_seat_sessions` / `_judge_leases`) and the dead-scan (:4035, which also gates `pane_pids` on it). The comment says the pid gate is primary, which may make it benign: nobody has measured it.

## Target end-state
- FIRST, a measurement: for each caller (lease judge, dead-scan, `pane_pids`), what does it do today when `_all_windows` returns `[]` because tmux was unreadable, with a seat's pid alive? Written into the round's node as a table (caller -> behaviour -> benign / harmful).
- If any caller is harmful: `_all_windows` returns `None` for "could not list" and `[]` only for a real empty listing, and every harmful caller treats `None` as "unknown: do nothing destructive" (no lease expiry, no dead verdict, no respawn).
- If every caller is benign: the round pins that with one test per caller and rewrites the comment to say why, and stops.

## Invariants
- A seat whose pid is alive is never judged dead because tmux was unreadable.
- `heal` never starts a second copy of a live seat (the existing pid gate stays primary).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_heal.py -q -k all_windows` passes with >= 3 rows: tmux rc != 0 -> unknown (not empty); tmux raises -> unknown; real empty listing -> empty; each with a live-pid seat asserting no destructive action.
2. Negative: `git grep -n 'tmux absent/down: \[\]' -- extensions/agi/bin/heal.py` returns zero hits.

## Out of scope
goal:g1.35 · the send.py fix (03c5f643b, DG2) · goal:g7.16.1.11 (key / identity / rotate work).

## Agent Notes
Assigned to **director-general-3**.
