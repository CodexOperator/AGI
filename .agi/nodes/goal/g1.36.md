---
id: goal:g1.36
mint_id: 82e54d4e286749b1951cd0edf44144a9
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G1.36
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 8a6a27ff4abbd5b0
season: 2
seeds:
  - goal:g1
status: horizon
tags:
  - spawn-gate
  - evidence
  - verdict
title: "G1.36: write.py create refuses a verdict node that needs evidence_runs and has none, with one source for the rule"
town: core
---
# goal:g1.36

## Why this exists
goal:g1 (the engine's own fixes): mur-de-base-dg2-1 verify (defect 1 STANDS) found DG2 mint `verdict:dg2-g1-send-unreadable` with `verdict=proved` and NO `evidence_runs`; DG2 added the runs by hand afterwards. SM measured on trunk 37cf1f557: `extensions/agi/bin/spawn_gate.py` names `evidence_runs` once, in a comment (:984), and `check_spawn` (:966) has no evidence_runs rule; `node_writer.py` gates on `gate_fm = fm_for_gate if fm_for_gate is not None else (extra_fm or {})` (:753), so `write.py create verdict ... --set verdict=proved` lands with none. Only the grid cron's `evidence_gate` demotes such a node later, at grid-commit time, after the node is already written and visible.

## Target end-state
- `write.py create <type> ... --set verdict=<proved|disproved|...>` applies the SAME evidence rule the grid `evidence_gate` applies later: a verdict that needs evidence and carries no `evidence_runs` is refused (or created as unreviewed with a named WARN -- the round decides which, by measuring what the grid gate does today), never silently written as proved.
- The rule has ONE source: `spawn_gate.check_spawn` calls the same normalizer the grid gate uses (`evidence_gate.normalize_evidence_runs`), no second copy.
- The same class is audited: every other write path that can set a verdict (`set verdict`, `--answers`) goes through that rule; the round lists each path by file:line.

## Invariants
- Existing nodes are never rewritten or demoted by this change (the grid gate keeps doing that).
- `--no-evidence-gate` stays the only bypass and is still stamped unreviewed.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_spawn_gate.py -q -k evidence_runs` passes with >= 3 rows: proved + no runs -> refused/flagged; proved + runs -> created; pending + no runs -> created.
2. Negative: `git grep -n "evidence_runs" -- extensions/agi/bin/spawn_gate.py` shows ONLY the comment today (1 hit at :984); after the round it must show a code hit, and `git grep -n "def normalize_evidence_runs" -- extensions` stays at exactly 1 definition.

## Out of scope
goal:g1.34 · goal:g1.35 · retro-demoting existing proved nodes · the grid cron's own schedule.

## Agent Notes
Assigned to **director-general-1**.
