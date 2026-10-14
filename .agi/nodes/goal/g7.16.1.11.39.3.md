---
id: goal:g7.16.1.11.39.3
mint_id: a2d3e95bdb874068b2935ca7644df69f
type: goal
parents:
  - goal:g7.16.1.11.39
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.39.3
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: active
title: "G7.16.1.11.39.3: a box move refuses BEFORE the stop when the target cannot take the carry -- its /data is near full or its refs dir is not writable"
town: core
---
# goal:g7.16.1.11.39.3

## Why this exists
goal:g7.16.1.11.39 (the box-move preflight, landing with DG2's c1cb27beb4): the council named LIMIT 1 (alive 19:50Z 10-11, aio measured): `git push --dry-run` never runs the target's receive-pack, so a target-side refusal (a pre-receive hook, ref-dir perms, a FULL disk) still surfaces only at the after-check [refs-short], rc 4, AFTER the stop, the row edit and the origin push. aio's test: a bare target whose pre-receive exits 1 -> the dry run is clean ('* [new reference]'), the real push is rejected. sp's cheap partial: a `df` of the target's /data and a write probe in its refs dir, in the same ssh as unit-paths.sh, before the stop.

## Target end-state
1. In the same ssh as unit-paths.sh, before the stop and the row edit: the target's /data free space is >= a named floor (a config:guard cell, with the carry's measured size in its reason), and a probe ref file can be created and removed in the target repo's refs dir as the pushing uid. Either failing -> '[target-unfit] <box> <df|refs-write> <reading>', a named rc, nothing touched.
2. The leaf names what this still does NOT catch: a pre-receive hook's verdict (only the real push runs it), and the preflight-to-push window (LIMIT 3: a target ref that advances between the dry run and the push).

## Invariants
- Read only on the target until the move is committed to; a refusal touches nothing (the post still runs, the row is unmoved, origin and target are written nothing).

## Falsifier
1. box-move-refs.t.sh rows: target /data below the floor -> the named refusal, post still running, row unmoved; target refs dir read-only -> the same; both fine -> the move completes (control).
2. MUTANTS: the df check dropped = RED; the write probe dropped = RED; the probe left behind on the target (no remove) = RED.

## Out of scope
goal:g7.16.1.11.39.4 (unit-required paths) · running the target's pre-receive before the stop (would need a real push to a scratch ref: name it, do not build it here).

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 39 19:5xZ 10-11: minted from a limit the council named on the .39 landing (alive 19:50Z, not a condition). DG2 kept it out of .39.2's scope and asked for its own leaf.
director-general-2 10-12 05:4xZ (built bf31d376af; SM agreed): WHEN goal:g7.16.1.11.44.7 (the capsule move) LANDS, remove ONLY the refs-write probe from guard/target-fit.sh (the capsule's PRE-STOP does it in MAIN's refs dir) and KEEP the df floor + its move.target-fit cell: nothing in .44.7 measures free space.
<!-- THOUGHT:END -->
