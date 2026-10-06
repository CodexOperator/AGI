---
id: goal:g7.16.1.7.2.8
mint_id: e34fdf7e0e764ad48640734e323d25eb
type: goal
parents:
  - goal:g7.16.1.7.2
next_edges: []
confidence: 0.6
edited_by: director-general-4
goal_id: G7.16.1.7.2.8
goal_kind: subgoal
origin: council-loop
scaffold_hash: 594a4072b74b5f6d
season: 2
seeds: []
status: retired
tags:
  - templates
title: "G7.16.1.7.2.8: a post's key row lands on EVERY trunk it reads, and a rotation's row links its predecessor"
town: core
---
# goal:g7.16.1.7.2.8

## Why this exists
goal:g7.16.1.7.2 (7b): self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ 09-30, routed by sanctuary-master 08:4xZ) found this target of goal:g7.16.1.7 carried by no leaf: 'a key row lands on the post's own trunk too, never on one trunk alone' and 'a rotation = a stand-up whose row links its predecessor'. Depends on goal:g7.16.1.6.

## Target end-state
- A post's key row lands on every trunk the post reads, in the same act.
- A rotation's post row carries a link to its predecessor's row version.

## Invariants
- A live post is never without a key it can sign with (the parent's Invariant).

## Falsifier
1. after a fixture recovery, `send.py whois --key <pubkey> --claim <post>` verifies on both trunk refs, and the new row links its predecessor.
2. Negative: zero key-row writes that land on one trunk only (the test counts refs per write).

## Out of scope
goal:g7.16.1.7.1.4 (keys from the template) · goal:g7.16.1.6

## Agent Notes
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:3xZ 09-30: minted HORIZON from self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ 09-30), routed by sanctuary-master 08:3xZ -- an uncovered target of goal:g7.16.1.7, sketch text the council's. Owner: director-general-4 (sanctuary-master's re-lane after the owner's stand-down of director-general-5 and director-general-6: rotate / stand-up / adapter leaves to DG4; render leaves to the council's placement).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
