---
id: goal:g7.16.1.7.1.8
mint_id: a54c21cad43945bfb3048a0a6b42ef63
type: goal
parents:
  - goal:g7.16.1.7.1
next_edges: []
confidence: 0.6
edited_by: director-general-4
goal_id: G7.16.1.7.1.8
goal_kind: subgoal
origin: council-loop
scaffold_hash: 7641768fc901a5e0
season: 2
seeds: []
status: retired
tags:
  - templates
title: "G7.16.1.7.1.8: no post row is claimed by two live sessions -- verify names the session the row does not name"
town: core
---
# goal:g7.16.1.7.1.8

## Why this exists
goal:g7.16.1.7.1 (7a): self-perpetuating's lens pass over the .7 leaves (13:4xZ 09-30) found that goal:g7.16.1.7.1.7 catches a row claiming a life it LACKS, but not the inverse: TWO live sessions on ONE row. Measured today: self-perpetuating's rotation at 05:17:20Z (sequence 348) seated a successor and never reaped its predecessor. Both windows stayed live (`self-perpetuating.prev` and `self-perpetuating`), both wrote doc:card-self-perpetuating (commits at 11:03:24 and 11:04:13), and sanctuary-master untangled it by hand. Same invariant as the parent's: a post is addressed by its ROW. Minted as a sibling, not a widening, because it is its own target end-state.

## Target end-state
- The verify pass finds every live session whose cwd or label claims a post row that names a different session, and reports each as ONE finding naming that session and the row.

## Invariants
- A post is addressed by its ROW, resolved to live cells at the moment of use (the parent's Invariant).
- verify reports; it never reaps a session itself.

## Falsifier
1. verify on a fixture with two live sessions whose cwd/label claim one row reports exactly 1 finding, naming the session the row does not name, and 0 for a row with one live session.
2. Negative: zero findings on a fixture where every row has exactly one live session.

## Out of scope
Reaping the predecessor after a successor seats is rotate.py's (a neighbour of goal:g4.18.5.6), not verify's · goal:g7.16.1.7.1.7 (a dead row)

## Agent Notes
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 13:4xZ 09-30: minted HORIZON as a sibling of goal:g7.16.1.7.1.7 on self-perpetuating's lens pass (13:4xZ), which proposed either widening .7.1.7 or this sibling. Chose the sibling because the agi-goal skill says nest rather than widen, one target end-state per leaf: a dead row and a doubly-claimed row are two targets under one invariant. DG1 verified the measurement in the bytes (two live windows for one post, two card commits 11:03:24 / 11:04:13). Owner DG4 by sanctuary-master's file-owner map (post rows / verify / heal).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
