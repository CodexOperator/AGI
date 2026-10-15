---
id: goal:g7.16.1.12
mint_id: 288c744fc2ae4348abf1142a1642237b
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G7.16.1.12
goal_kind: subgoal
origin: goal
seeds: []
tags: []
season: 3
status: retired
title: "G7.16.1.12: COUNCIL BUNDLE season 3 (core town) -- a FRESH bundle, cut by the council over its first season-3 rounds; season3/main carries season 2's progress until the rollover"
town: core
---
# goal:g7.16.1.12

## OWNER 2026-10-14 14:4xZ, verbatim
"Yes record but not cut it yet we need to reset the town bundle to a fresh bundle for the next season we will need a few rounds on it next season."

## OWNER 2026-10-14 14:5xZ, verbatim
"Let’s start the core/season3 branch now or if there is one already let’s overwrite it now and reset it to what we have now on this branch. Then also start a origin/season3/main branch and put progress so far into it. Then add the season3 core town bundle to it as we work on finishing season 2."

## Why this exists
goal:g7.16.1 (the council loop: directors build, a sanctuary master reviews, a three-lens council re-bundles): bundles 1-11 are its season-1/2 bundles (.11 = the season-2 radically-simple-engine bundle, 13 g7.16.1 leaves still active at 14:4xZ 10-14). The owner named a FRESH bundle for season 3, built on season3/main while season 2 finishes. Measured 14:5xZ 10-14: origin core/season3/main and season3/main = a837dbe882 (the season-2 trunk tip); the old core/season3/main tip 4b8f28b5e1 (DG4's raw-shell work, 10-06, 1853 commits not on the trunk) is kept as origin archive/core-season3-main-pre-20261014.

## Target end-state
- The season-3 core-town bundle is cut fresh by the council, its leaves nested under this node over its first rounds; nothing is cut before the owner's word opens them.
- season3/main holds season 2's progress (each season-2 landing merged in, never a rewrite) until the rollover, then becomes the season-3 trunk.
- Carried leaves: goal:g7.16.1.11.44.8 (town start / stop from the matrix: agi-start / agi-stop), re-parented here at the cut.

## Invariants
- Retire, never delete: the old season-3 tip stays on its archive branch.
- Season 2 closes on its own trunk; this bundle never gates the season-2 close.

## Falsifier
Draft, on the owner's word; the council cuts the real ones in season 3.
1. `git merge-base --is-ancestor <season-2 trunk at the rollover> season3/main` exits 0, and this node has >= 1 child leaf cut by the council.
2. Negative: 0 commits on season3/main that rewrite history (every push a fast-forward or a merge).

## Out of scope
goal:g7.16.1.11 (the season-2 bundle) · the rollover runner itself (skill agi-master-gate ROLLOVER RULE)

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (belam 15:0xZ 10-14): RETIRED in place, never deleted. Owner 15:0xZ: 'the bundles slash town boards, those nodes, they don't really exist as like sub goals or anything ... parented from like, say, visions'. A bundle is a town board (town:core, parents vision:the-living-being + goal:g26.towns), loose over goals; this node was the wrong shape (a subgoal under goal:g7.16.1). The season-3 bundle now lives in town:core's GOAL BUNDLE section on season3/main, with the owner's words.
<!-- THOUGHT:END -->
