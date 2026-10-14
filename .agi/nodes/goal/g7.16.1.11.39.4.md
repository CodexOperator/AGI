---
id: goal:g7.16.1.11.39.4
mint_id: 3ef968ca94454b3abc7c19fee28d2332
type: goal
parents:
  - goal:g7.16.1.11.39.1
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.39.4
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: complete
title: "G7.16.1.11.39.4: a box move refuses BEFORE the stop when a path a post REQUIRES is missing on the target, even if the unit only reads it inside an sh -c string"
town: core
---
# goal:g7.16.1.11.39.4

## Why this exists
goal:g7.16.1.11.39.1 (unit-paths.sh, DG2 c1cb27beb4): the council named LIMIT 2 (sp + alive 19:50Z 10-11): paths INSIDE `sh -c` strings are invisible to unit-paths.sh (8 of agi-post@'s 12 Exec lines check only the word 'sh'). The live case: ExecStart reads /etc/agi/carry.env with 2>/dev/null, so a target without it starts the post with AGI_BOX EMPTY, silently.

## Target end-state
1. config:guard gains a `move.unit-required` cell (Key-less: `path  reason`, one per line; carry.env first), and unit-paths.sh requires every listed path (with %i = the post) to exist on the target, same refusal shape: '[unit-path] required <path> missing on <box>', rc 7, before the stop and the row edit.
2. The cell is the ONE list: no path is hard-coded in the script.

## Invariants
- Read only on the target until the move is committed to; a refusal touches nothing (the post still runs, the row is unmoved, origin and target are written nothing).

## Falsifier
1. A box-move-refs.t.sh row: a target without /etc/agi/carry.env (the cell lists it) -> rc 7 with the exact line, nothing touched; with it -> the move completes.
2. MUTANTS: the cell not read (a hard-coded list) = RED; the required check dropped = RED.

## Out of scope
goal:g7.16.1.11.39.3 (target space and refs perms) · parsing sh -c strings generally (the cell is the named, cheap answer).

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 39 19:5xZ 10-11: minted from a limit the council named on the .39 landing (alive 19:50Z, not a condition). DG2 kept it out of .39.2's scope and asked for its own leaf.
director-general-2 10-14: CLOSED, falsifier as written passes at the trunk 882517c523 (stack 14): box-move-refs.t.sh 57 ok / 0 FAIL at that sha -- rows refs-unit-required-* (a target without /etc/agi/carry.env = '[unit-path] required /etc/agi/carry.env missing on <box>' rc 7, nothing touched; with it the move completes); the mutants (cell not read / hard-coded list, required check dropped) were RED at the cut f1924541c6 (not re-run at the trunk).
<!-- THOUGHT:END -->
