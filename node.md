---
id: goal:g7.16.1.11.37
mint_id: 83524e9705aa48f6b913d99f71697031
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.37
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: c79775bfb5f9e079
season: 2
status: active
title: "G7.16.1.11.37: AGI_SEAT is retired -- a post unit carries AGI_POST and AGI_BOX from its row, and every reader takes AGI_POST"
town: core
---
# goal:g7.16.1.11.37

# G7.16.1.11.37: AGI_SEAT is retired -- a post unit carries AGI_POST and AGI_BOX from its row, and every reader takes AGI_POST

## Why this exists
OWNER, verbatim (02:4xZ 10-11, via belam-s2-III): "Bad we fix the post issue agi seat shouldn't be used anymore unless absolutely needed. The post should include all relevant info including box location".
Cause (belam): the live /run/systemd/system/agi-post@.service is agi-boot's 10-01 render and sets AGI_SEAT=%i only; engine-root.md's AGI_POST=%i was never re-rendered. So agi-at / agi-turn (which need AGI_POST) printed [no-branch] in every pane (sanctuary-master 83x, DG3 55x), and box needed a hand-set AGI_POST. The live half is belam's host act, already done: the drop-in agi-post@.service.d/52-post-env.conf = Environment=AGI_POST=%i (299337b255, extensions/agi/guard/post-env), with each post restarted while idle. This leaf is the CODE half. belam placed it with sanctuary-master ("YOURS TO PLACE"), which lanes it under the g7.16.1.11.11 HOLD (identity). As usual, the council approves the landing.

## Target end-state (counts measured on 299337b255)
1. THE UNIT: engine-root.md's agi-post@ unit (:28 already sets AGI_SEAT=%i AGI_POST=%i; the live RENDER is what is stale) drops AGI_SEAT. AGI_BOX keeps ONE source, this box's own env file (boxes.py:7: AGI_BOX names THIS box; rotate stamps the row from it). The unit compares it with the post's config:posts row `box` and REFUSES on a mismatch with `[wrong-box] row=<x> here=<y>`; it never sets AGI_BOX from the row. Retiring 52-post-env = two GOs in order (belam's host acts): re-render the unit, read a running post's env and run the (4) lane in it, THEN retire the drop-in. Never the drop-in first: a gap repeats the [no-branch] blackout.
2. THE ENGINE PIECES read $AGI_POST with NO fallback (they run only inside a v5 unit): engine-post agi-captive (:23 p=$AGI_SEAT), agi-out (:153), engine-wrap agi-run (:23 :25 :26 :28; :26 and :28 already read ${AGI_POST:-$AGI_SEAT}), the pi extension (:44 :45), and the kid line (:70 sets both). The prose history rows (engine-wrap :92 :93) stay as written.
3. PYTHON reads AGI_POST first and falls back to AGI_SEAT only for a v4 row, through ONE named helper. Today there are 56 AGI_SEAT hits in 13 non-test files: adapters/claude_code_adapter 2, commands 1, dispatch 12, geometry_config 8, last_act 3, rotate 15, season 1, send 4, suite_guards 1, verification 1, viewport 1, write 3, hooks/rotation_alert 4 (the hook belam's list did not name). The fallback is retired in the commit that moves the last v4 row to v5.
4. A LANE: a post started with AGI_POST (+ AGI_BOX) only, and no AGI_SEAT in its env, runs box, agi-at, agi-turn, agi-captive and agi-out green.
5. (moved 10-11 by the council, alive 02:5xZ 3/3: the agi-flush strand is its own leaf, goal:g7.16.1.11.38, outside this HOLD)

## Invariants
- A v4 row keeps working until it moves: the fallback lives in the one helper and nowhere else.
- No new round on key / signing / rotate / spawn-row / write-gate rides this leaf (the g7.16.1.11.11 HOLD). Only the env name changes.
- A host act (the unit re-render, the drop-in retire, restarts) = belam's GO per act.

## Falsifier
1. The fenced pieces of `.agi/nodes/.geometry/engine*.md` contain 0 hits for `AGI_SEAT` (the prose rows are not counted).
2. `git grep -n AGI_SEAT -- 'extensions/agi/bin/*.py' 'extensions/agi/bin/adapters/*.py' 'extensions/agi/hooks/*.py'` hits only the one helper, plus its v4-row comment.
3. The lane in (4) goes RED under each mutant: the helper reads AGI_SEAT first; agi-captive's p= reads AGI_SEAT again; the unit sets no AGI_BOX; the row's box != this box and the post starts anyway.
4. With AGI_SEAT unset, `box read` as a post works with no hand-set AGI_POST.
5. (moved to goal:g7.16.1.11.38)
6. (host read, belam's) the live agi-post@ unit + its drop-ins == the render of engine-root.md. The cause here is a class: a rendered host unit drifted from its node.

## Out of scope
Renaming seat-era python identifiers (`seat` variables) beyond the env read · the v4 -> v5 row moves themselves · goal:g7.16.1.11.20.1 (the alert's receiver rule).

## Agent Notes
sanctuary-master gen 35 10-11: landed in 889a29eec4 (council alive 02:4xZ, 3/3), placed with DG4. This version folds in the council's remarks: one python helper; shell with no fallback; AGI_BOX from this box with a [wrong-box] refusal (all-is-one and alive, independently: setting it from the row makes two sources that point at each other, wrong mid box-move); the drop-in retire as two ordered GOs; the unit == render falsifier (self-perpetuating); Target 1's :28 cite corrected.
