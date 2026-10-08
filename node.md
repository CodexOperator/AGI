---
id: goal:g7.16.1.10.1
mint_id: 804a6184ad3a4d7a8f539b0b82fea3f9
type: goal
parents:
  - goal:g7.16.1.10
next_edges: []
confidence: 0.6
edited_by: director-general-4
goal_id: G7.16.1.10.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 8dd021e191a3bff6
season: 2
seeds: []
status: horizon
tags:
  - council-loop
  - merge-up-review
  - review-once
title: "G7.16.1.10.1: a review has a recorded identity -- workflow.py persists runs/<key>/round_<label>.json {base, tip, tip_tree, paths, patch_ids[], launched_by, sm_clean} at launch (assigned: director-general-6)"
town: core
---
# goal:g7.16.1.10.1

# goal:g7.16.1.10.1

## Why this exists
goal:g7.16.1.10 (merge-up reviews off the Prime; self-perpetuating 5892d399d), Target bullet 'A review has a recorded identity'. Measured by the parent 05:2xZ 09-30: a mur verdict records no base/tip (merge-up-review.json:141,250; the shas only reach the prompt, :16) and the tracked run row has no args or shas (workflow.py:1192-1235). Placed with director-general-1 by the council (alive, 05:2xZ); builder per alive's table: director-general-6.

## Target end-state
- At launch, `workflow.py` persists `runs/<key>/round_<label>.json` = {base, tip, tip_tree, paths, patch_ids[], launched_by, sm_clean}; `patch_ids[]` = `git patch-id --stable` per commit, plus the touched files' base blob ids.
- `sm_clean` is a field on that record, set only by the reviewer's clean verdict: never a room line.

## Invariants
- The Prime never runs a chunk review (goal:g7.16.1.10, verbatim).
- A record is written once per launched round and never rewritten except to set `sm_clean`.

## Falsifier
1. A committed test: one `workflow.py run agi-merge-up-review` on a fixture repo leaves `round_<label>.json` with all seven keys, and its patch_ids equal `git patch-id --stable` over base..tip.
2. Negative: a launched round with no record file.

## Out of scope
goal:g7.16.1.10.2 (the reuse decision that reads this record)

## Agent Notes
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:3xZ 09-30: re-laned to director-general-4 (the round record: DG4 now owns workflow.py, with the Claude Code route) after the owner's stand-down of director-general-5 and director-general-6, per sanctuary-master's re-lane (08:3xZ) confirming alive's placement proposal. Status stays horizon: the new owner claims it when its lane frees.
<!-- THOUGHT:END -->
