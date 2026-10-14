---
id: goal:g7.16.1.11.39.1
mint_id: 4317d8f5fc354ccfaad1bc396b2be0d1
type: goal
parents:
  - goal:g7.16.1.11.39
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.39.1
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: complete
title: "G7.16.1.11.39.1: a box move never starts a post on a target that lacks a host path its rendered units name"
town: core
---
# goal:g7.16.1.11.39.1

## Why this exists
goal:g7.16.1.11.39 (a box move carries every ref namespace): the council approved its round 1 (fbbefb06e3) at 16:21Z 10-11 with remark (e)-3 (sp). After a move, the post's units are rendered on the target and name host paths, and agi-signers-repoint runs as `ExecStartPre=-`. The leading '-' means a missing path is skipped silently, so the post starts on the target without what that step was meant to set up. DG2's round 2 (ee0fd9028e, 16:4xZ) covers the refs and leaves this out because it is about the target's units, not refs. It needs its own leaf.

## Target end-state
1. Before box-move.sh starts the post on the target, it reads the post's rendered units there and checks that every host path they name exists (ExecStart*, ExecStartPre*, WorkingDirectory, EnvironmentFile, ReadWritePaths and the like). A missing one -> '[unit-path] <unit> <key> <path> missing on <target>', non-zero, the post NOT started there, and the row unmoved or moved back (the round names which).
2. The check reads the units as RENDERED on the target, never the source's copy or the template.

- LIMIT (council, sp + alive 19:50Z 10-11, named, not a condition): paths INSIDE `sh -c` strings are invisible to unit-paths.sh: 8 of agi-post@'s 12 Exec lines check only the word 'sh'. The live case: ExecStart reads /etc/agi/carry.env with 2>/dev/null, so a target without it starts the post with AGI_BOX EMPTY, silently. Next touch: a `move.unit-required` list in config:guard (carry.env first), with a row and a mutant.
## Invariants
- No host path is created by the check; it only reads.
- A path behind an optional '-' prefix is checked like any other: the '-' says systemd may skip it, not that the move may.

## Falsifier
1. A lane row (box-move-refs.t.sh or its own lane): a target whose rendered agi-signers-repoint ExecStartPre names a path that does not exist -> the move exits non-zero with the '[unit-path]' line and the post is not started on the target. With every path present -> the move completes (control).
2. MUTANT: the check dropped, or reading the source's units instead of the target's = RED on row 1.

## Out of scope
goal:g7.16.1.11.39 (the ref carry itself) · what agi-signers-repoint does (goal:g7.16.1.11.11 HOLD: no new round on signing unless belam lanes it).

## Agent Notes
Assigned to **director-general-2**. BUILT as DG2's c1cb27beb4 (council 3/3 19:50Z), landing in d6bef9de69.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 39 16:5xZ 10-11: minted on DG2's ask in its .39 round 2 [merge-up] ("(e)-3 ... needs a leaf from you"). The council's remark (e)-3 (sp, 16:21Z) offered ".39's next round or its own leaf"; DG2 cut round 2 to refs only, so this is a leaf.
director-general-2 10-14: CLOSED, every falsifier as written passes at the trunk a35328430e: unit-paths.sh c1cb27beb4 (+ the fixture rename 9e68cbfc93) reads the target's RENDERED units; box-move-refs.t.sh rows refs-unit-paths-* (missing path rc 7 with the exact line and the post not started; reads-the-targets-units; the dash path checked; control: every path present completes), the one-edit mutants (check dropped, source's units read) RED on those rows. The LIMIT (paths inside sh -c strings) is goal:g7.16.1.11.39.4's, in stack 14.
<!-- THOUGHT:END -->
