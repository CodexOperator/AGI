---
id: goal:g1.34
mint_id: 890bad276a59480ca0cb3919d5cd0d70
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G1.34
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: ecd8f189e0c0d113
season: 2
seeds:
  - goal:g1
status: retired
tags:
  - tier-gate
  - conftest
  - fail-closed
title: "G1.34: the kid tier gate fails closed on an unreadable directory inside a sessions root, not only on a worktrees entry"
town: core
---
# goal:g1.34

## Why this exists
goal:g1 (the engine's own fixes): mur-dg1-5 / dg102-c1 (10-01, DG1.02 round) found the kid tier gate fail-open on ONE shape the round banked: `extensions/agi/tests/conftest.py` `_running_record_tiers` walks a sessions root with `Path(root).rglob("agent.json")` (:92), and on python 3.12 `rglob` swallows PermissionError, so an unreadable SUBDIR inside a readable root contributes no record; the tier then falls to the caller-controlled `AGI_TIER` (the same hole DH.DG1.02/.05 closed for an unreadable worktrees entry and DIR, `_WORKTREES_ENTRY_DROPPED`). Banked by the director, not fixed in that round: closing it replaces the traversal (os.walk with onerror), a behaviour change over that round's ceiling.

## Target end-state
- `_running_record_tiers` reports an unreadable directory under a sessions root (it no longer drops it silently), and `_effective_tier` treats it exactly like a dropped worktrees entry: no matching running record + an unreadable directory = the restrictive tier (`kid`), never `AGI_TIER`.
- A readable matching record still wins; a readable tree with no unreadable directory behaves byte-for-byte as today.
- The refusal text names the real cause when it came from an unreadable directory (today it always says `AGI_TIER=kid`).

## Invariants
- Collection never raises on an unreadable directory (it fails closed, not loud).
- The traversal still ignores phantom (dead-pid) records exactly as today.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_tier_gate.py -q -k sessions_subdir` passes with >= 3 rows: unreadable subdir + no record -> kid with `AGI_TIER=director` in the env; unreadable subdir + readable kid record -> kid; readable tree, no unreadable dir -> unchanged.
2. Negative: `git grep -n 'rglob("agent.json")' -- extensions/agi/tests/conftest.py` returns zero hits.

## Out of scope
goal:g1.31.5.1.3 and the worktrees-entry/dir arms (landed in d32ef0038, DH.DG1.02/.05) · the context suite's own conftest (it has no tier gate).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
