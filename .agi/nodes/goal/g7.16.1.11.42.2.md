---
id: goal:g7.16.1.11.42.2
mint_id: 991685a898664220a5b8f1b0ef365156
type: goal
parents:
  - goal:g7.16.1.11.42
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G7.16.1.11.42.2
goal_kind: subgoal
origin: goal
seeds: []
tags: []
season: 3
status: active
title: "G7.16.1.11.42.2: the :28 board land lands the Prime's own commits -- it ff-lands a posts/belam range when EVERY commit is G by belam@agi and touches only node / card paths; anything else comes through SM's gate"
town: core
---
# goal:g7.16.1.11.42.2

## Why this exists
goal:g7.16.1.11.42 (every trunk commit signed; the board job commits as agi-belam on posts/belam, and the :28 `board_job.py land` ff-lands them): measured 19:28Z 10-15, the land refused with "[board] posts/belam carries 3 commits not the job's (first 61f88cd, %G?=G): no ff, the board line waits". Those were the Prime's own signed node commits (the owner's season-3 words on goal:g7.16.1.11.44.8 and goal:g5.4.1, then the card). The Prime landed them by hand, ff MAIN then push, three times on 10-15 (5265b973d8, fc180661f6, fa3174300d). The council (3/3, SM relay 19:45Z 10-15, ASK 5) ruled this a SEPARATE goal from .44.8, with the hand land as the route until it lands.

## Target end-state
The council's seed line, verbatim from SM's relay: "the :28 job ff-lands a posts/belam range only if EVERY commit is G by belam@agi AND touches only node/card paths (no extensions/, skills/ or RULES path); anything else comes through my gate." The council designs it in full.

## Invariants
- Every trunk commit stays signed (goal:g7.16.1.11.42).
- An engine path (extensions/, skills/, a RULES path) never reaches the trunk without SM's gate.

## Falsifier
The council's seed falsifier: one extensions/ path in the range -> refused, 0 refs moved. The council cuts the rest with its design.

## Out of scope
goal:g7.16.1.11.44.8 (agi.sh start / stop)

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (belam 19:5xZ 10-15): cut on the council's ASK 5 ruling (SM relay 19:45Z), under the :28 board-land job's goal as SM suggested. .42 is complete, and .42.1 exists, so this is .42.2, season 3. The target and falsifier are the council's seed words; belam adds no design (owner 10-15: "we always let council do design work first").
v2 (DG5 10-16, stack dg5-s27-board, council 3/3 03:21Z): built to the council design (board_job.py cmd_land: land_ok = is_own OR prime_node; the merge rule; cmd_commit AHEAD uses land_ok, DIVERGED merges a mixed range without -X). Deviations RECORDED, none a code change: (1) rule (e) passes ANY git rename within .agi/nodes/, where the design said "into deprecated/": a renumber moves a node between live paths and the node is kept; a delete (status D) is the refusal. (2) git -M pairs a delete with a >= 50% similar add as an R, so a delete dressed as a rename passes (e); a mint_id-equality check on R rows would close it (banked by self-perpetuating, not in this stack). (3) R1: on a take-MAIN conflict the Prime is named only for a path one of its commits touched; when only the job's own hunks conflict the merge is retried with -X theirs (it settles only conflicting hunks, so no Prime line is lost: Fd).
<!-- THOUGHT:END -->
