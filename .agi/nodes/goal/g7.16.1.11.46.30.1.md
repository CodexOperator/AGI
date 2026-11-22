---
id: goal:g7.16.1.11.46.30.1
mint_id: c23296aac0864e529a4be996e531ea6e
type: goal
parents:
  - goal:g7.16.1.11.46.30
next_edges: []
confidence: 0.5
goal_id: G7.16.1.11.46.30.1
goal_kind: subgoal
origin: goal
role: director
season: 3
seeds: []
status: active
tags: []
title: "G7.16.1.11.46.30.1: grid_sync's commit --all never writes over a post's PENDING turn-end version, and a land whose post-land split is missed ALARMS"
town: core
---

# goal:g7.16.1.11.46.30.1

## Why this exists
goal:g7.16.1.11.46.30 (target 2: the grid grows at turn end, each changed node in the land split's per-node form). Measured 11-17 (L621, SM [red] 20:36Z): the grid_sync cron's `grid.py commit --all` (every 30 min) wrote MAIN's L618 bytes over meme-master's turn-end versions of experiment:paper-proofs-hold-e1 and experiment:paper-meets-rubric-e1 at 20:01:46Z, before those versions landed (L621, 20:31:02Z); belam healed it by hand at 20:45:07Z. Cause (self-perpetuating 20:38:00Z, read in grid.py): the rewind guard lives in the split path only; the commit path (prepare_version) skips only bytes EQUAL to the tip, and the split's guard judges 'older' by a blob's position in GRID history, so copying it would refuse the heal too. Every edit a post grids at its turn end is open to the same overwrite until it lands. The rule below was worded and run as a predicate model by the council, 3/3 (self-perpetuating 20:55:53Z, all-is-one 20:56:21Z, alive 20:58:37Z, 11-17).

## Target end-state
- PENDING: `commit --all` leaves a node's grid tip alone while it is a lane's pending version: pending iff the tip carries a `Split-Land:` trailer whose commit is NOT an ancestor of the trunk AND the tip's blob != the trunk tip's blob for the path (provenance by the trailer, alive 20:51:40Z; author cannot tell: cron, hand heal and post-land split are all author 'grid').
- WRITE: otherwise it writes MAIN's blob B over the tip's blob G iff G is in the trunk's own history of the path AND (B == the trunk tip's blob OR B is in no trunk commit of the path) (self-perpetuating 20:50:14Z + 20:52:42Z, all-is-one 20:53:58Z). A node with no grid version yet is written.
- ALARM (option 1, the invariant no rule clause can replace): every land that touches a node path gets its post-land split; per land, a node whose trunk-tip blob is absent from its grid history is ONE alarm line naming the node and the land, closed by a MAIN hand grid commit. (A missed post-land split leaves (i-) and (c-) as one grid state; no clause heals one without breaking the other, sp 20:55:53Z.)

## Invariants
- No grid version is ever rewritten or deleted; a fix only decides whether the next version is written.
- The split path's own rewind guard is not copied into the commit path.
- A post never runs `grid.py commit --all` (goal:g7.16.1.11.46.30).

## Falsifier
1. A committed test of the commit path exits 0 with each case named, both ways (writes / leaves alone): (a) MAIN holds an older trunk blob put back, trunk + grid at v2: no write; (b) grid behind the trunk: write; (c) a post's turn-end v2 pending, trunk + MAIN at v1: no write; the 20:01 incident (MAIN == trunk tip, grid tip in no trunk commit, lane trailer off the trunk): no write; (d) a real trunk revert v1->v2->v1: write; (e) an uncommitted MAIN edit (evidence_gate demote): write; (e2) landed bytes under a lane trailer: write; (f) a lane's pending revert to an old trunk blob: no write; (g) no grid version: write; (h) a MAIN edit while a lane version is pending: no write; (i) a lane version overtaken by another land whose post-land split ran: write; (i-) the same with that split MISSED: no write AND one alarm line; (c-) a lane version over a trunk v1 the grid never held: no write; and the L618 window (a re-cut lands a lane's EARLIER version while the lane's tip is later): no write. A mutant that drops the PENDING clause reds (f); a mutant that drops PENDING AND the G-in-trunk-history clause reds (c), (f), (h), the incident and the L618 window (all-is-one 17:50:14Z 11-22, RAN: those four are guarded twice). The build also names one case no 11-17 word did: (e-) after (e), MAIN reverts the uncommitted edit to the trunk tip, so the grid tip holds bytes no commit ever held, the rule never writes the trunk's back and the alarm stays silent: a case with its expected outcome, or one line in this leaf saying why (e-) cannot happen (all-is-one 17:50:14Z).
2. Negative, at the first land after the fix: `grid.py log` of each node the land touched shows no version written by the cron between a post's turn-end split and its land, and the land's alarm read prints 0 lines (or names each missed split).

## Out of scope
goal:g7.33.7 (the grid ref namespace by config); goal:g15.29.11 (the commit guard and ref writer reading one namespace).

## Agent Notes
Assigned to **belam**.
