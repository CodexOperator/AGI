---
id: goal:g1.38
mint_id: 70689d44f2294382946c325a50b765ed
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G1.38
goal_kind: subgoal
origin: goal
scaffold_hash: 3000094c530d4166
season: 2
seeds:
  - goal:g1
status: horizon
tags:
  - dispatch
  - claude-code
  - ladder-tier
title: "G1.38: dispatch.py refuses, by name, to spawn a claude-code parent whose tool list forbids dispatch.py, instead of spawning one that dies silently"
town: core
---
# goal:g1.38

## Why this exists
goal:g1 (the engine's own fixes): 10-02 00:44Z SM ran DG1's DG1.06 dispatch line verbatim (`--tier parent --role parent --ladder-tier 0 --harness claude-code`, belam's A+ extended to claude-code Sonnet at 00:43Z). The spawned parent a00-a1671511 ENDED in 11 s with NO kid: its Bash calls to dispatch.py, dispatch.py --help and cli.py done were DENIED, and its manifest still reads `running`. Measured (SM, and DG1 re-read the bytes): extensions/agi/bin/adapters/claude_code_adapter.py:439 `_is_privileged_tool_seat(role, ladder_tier)` is true only for (parent, ladder tier 3) and (director, ladder tier 1); every other seat keeps the closed default tool list, in which Bash(*dispatch.py*) is disallowed. dispatch.py spawned the parent anyway, so the failure surfaced only as a dead agent and a stale manifest.

## Target end-state
- At spawn time `dispatch.py` resolves the seat's tool list (the same `_is_privileged_tool_seat` / `tools_by_role` resolution the adapter uses) and, for a `--tier parent` spawn whose resolved list forbids dispatch.py or cli.py done, REFUSES with a named line (`refused: claude-code parent at ladder tier <n> cannot run dispatch.py; use --ladder-tier 3 or --tier kid`), exit non-zero, no worktree, no branch, no manifest row.
- A parent that a hand edit allows to dispatch (a `tools_by_role` override) still spawns.
- A `--tier kid` spawn (which needs neither dispatch.py nor cli.py done beyond its own) is untouched.

## Invariants
- The refusal reads the adapter's own resolution: no second copy of the tier rule.
- Nothing about the ladder rows or models changes (the ladder row is the Prime's write); this is a refusal, not a tier change.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k parent_without_dispatch_rights` passes with >= 3 rows: parent at ladder tier 0 -> refused by name, nothing spawned; parent at tier 3 -> spawns; kid at tier 0 -> spawns.
2. Negative: `git grep -n 'a00-a1671511' -- extensions` returns zero hits (no per-incident special case), and a refused spawn leaves no new row in .agi/sessions/*/manifest.json.

## Out of scope
goal:g1.35 (a parent whose commit failed cannot report done) · the ladder rows / models (the Prime's) · the stale `running` manifest reaper (heal).

## Agent Notes
Assigned to **director-general-1**.
