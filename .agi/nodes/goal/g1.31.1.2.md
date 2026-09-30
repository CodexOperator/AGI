---
id: goal:g1.31.1.2
mint_id: bbe3ff956d8e4d3c9146d682f3e35c73
type: goal
parents:
  - goal:g1.31.1
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.1.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 8c62844912769c92
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - residue
  - engine-delta-1
  - engine-delta-5
  - goals-md
  - retire
title: "G1.31.1.2: the tracked .agi/nodes/.geometry/commands.md.bak (second carrier of command:commands' mint id) is retired by a move to deprecated/"
town: core
---
# goal:g1.31.1.2

## Why this exists
goal:g1.31.1: PASS B3 round `engine-delta-1` (demote; `.agi/sessions/workflows/runs/mur-pb3chunk1of20/verify_engine-delta-1.json`) upheld item #4 (g1.31 LANES #21): a tracked second copy of the commands node. Its GOALS.md siblings (ed-1 #5, ed-5 #3 = LANES #22 #25) are CLOSED at b8d232fc6 (unify.py, verify_unified.py, publish-engine.sh = 0 tracked files at HEAD). Measured at HEAD ff09c6101, 1 item open:
```
.agi/nodes/.geometry/commands.md.bak   tracked (git ls-files: 1)   :2 id: command:commands   :3 mint_id b7e4f0a9…  == commands.md:2-3
                                       :26 goals-check  :134 - goals-check   (GOALS.md retired, goal:g7.16.1.4.1)
mint collision (verifier's upgrade)    neutralised at HEAD: grep_live reads *.md only (rotation_record.py:52,:61; test_links.py:840-845)
```

## Target end-state
- `.agi/nodes/.geometry/commands.md.bak` is not tracked at that path: it is retired by a move, never `git rm` (CLAUDE.md "Retire, never delete") -- `git mv` to `.agi/nodes/deprecated/command/commands.md.bak`, bytes unchanged; not a `*.md` node file, so no node counter moves and it carries no mint (rotation_record.py:52).
- No tracked `.agi/nodes/.geometry/` file carries the retired `goals-check` command (today only commands.md.bak:26, :134).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Nothing under `.agi/nodes` is `git rm`'d; `active_node_count + deprecated_node_count` never drops.
- `python3 extensions/agi/bin/links.py links` broken = 0.

## Falsifier
1. `test -z "$(git ls-files .agi/nodes/.geometry/commands.md.bak)" && test -n "$(git ls-files .agi/nodes/deprecated/command/commands.md.bak)" && ! git grep -qn 'goals-check' -- .agi/nodes/.geometry`
2. Negative: `git grep -n 'goals-check' -- .agi/nodes/.geometry` returns zero hits.

## Out of scope
goal:g1.31.1.1 · goal:g1.31.2 · the other goal:g1.31.* leaves · goal:g1.30 · goal:g1.29. The GOALS.md scripts (closed at b8d232fc6). Historical prose naming the retired scripts (crons.md:106, :132; metrics.py, level3.py comments) -- a record, not a caller.

## Agent Notes
Assigned to **director-general-6**.
