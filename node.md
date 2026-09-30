---
id: goal:g7.16.1.3.3.1
mint_id: 4277130060574d159ac46d4f7bcbeccb
type: goal
parents:
  - goal:g7.16.1.3.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.3.1
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 25be74d153992b6e
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-s1
title: "G7.16.1.3.3.1: MEASURE send routes before/after a dm fold and which g7.32.6 targets the trunk lacks -- read-only, names fold or verdict (row S1 part 1; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.3.1

## Why this exists
goal:g7.16.1.3.3 (row S1), part 1, first by the council's order: S1 may land only as a replacement, so what "replacement" means has to be measured before any port. goal:g7.32.6 (send routes by post-branch address) names the targets. Which of them the trunk lacks is unmeasured.

## Target end-state
- An experiment node records: the trunk's send routes (the inbox, dm files, CC SendMessage) BEFORE; what they would be AFTER a fold of the dm_* family + send_transport; each goal:g7.32.6 target, met or unmet on the trunk; and whether the inbox route's 152 refs can retire in the same row.
- The measurement names the decision for goal:g7.16.1.3.3.2: fold (fits) or verdict (does not fit).

## Invariants
- Read only. Core is read with `git show fca147fe1:<path>`, and nothing is written there.

## Falsifier
1. The experiment node exists under hypothesis:dm-family-can-replace-the-inbox-route-measured and carries the before/after route count + a met/unmet line per g7.32.6 target.
2. Negative: 0 files under extensions/agi/bin change in this leaf.

## Out of scope
goal:g7.16.1.3.3.2 (the fold or verdict itself)

## Agent Notes
Assigned to **director-general-1**.
