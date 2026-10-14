---
id: goal:g7.16.1.11.44
mint_id: 7682f4df16c94d2ba9c35f91495d3d57
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.44
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: master
season: 2
status: active
title: "G7.16.1.11.44: ONE pack format moves any graph slice -- a container attached to a node by mint id, rendered there; season rollover and box moves are the same pack / unpack"
town: core
---
# goal:g7.16.1.11.44

## Why this exists
goal:g7.16.1.11 (the engine every post runs on): the owner (20:2x-20:3xZ 10-11, via belam) ruled a unified slice container. belam measured what that changes: D2 (doc:radically-simple-engine §AC) picked the GOAL tree with nest: cells in the container's front matter, and D4 DROPPED the pilot's node bundle (refs/slice, 'a second store'); the owner now rules the other way. Today nest.py (goal:g7.16.1.11.21) is read-only, 0 nodes carry nest:, there is no writer and no goal for the season-rollover collapse, and goal:g7.16.1.11.22 has stalled since 10-08.

## OWNER 2026-10-11 20:2x-20:3xZ, verbatim (via belam)
20:2xZ: "the recursive idea is the more recent one like the way we're gonna collapse the goal experiment etc nodes into the relevant build nodes for season rollover via graph move since everything is a git graph or subgraph slice. So we use the new engine functions as scripts to do the move now I think check the bundle idk how it got lost as well."
20:3xZ: "Let's just have the container be a custom file or directory or pack of some kind and it gets assigned to whatever node at will. It carries inside it which graph node it needs to attach to or by repointed to by mintID and gets rendered there once attached."
20:3xZ: "It needs to be reusable fully for any graph slice, so for example moving posts from one box to another is just packing up all the graph slices attached to said posts and transferring those over to a new box and unpacking them there. You see how it could be a unified design!"

## Target end-state
1. ONE council design (DESIGN FIRST, then a leaf per verb): the pack format; attach / re-point by mint id; render at the attach node; pack / unpack / move verbs as ENGINE SHELL pieces ("the new engine functions as scripts").
2. Every slice move uses it: season rollover (goals, experiments etc. collapse into their build nodes), box moves (a post's slices packed, carried, unpacked: box-move.sh's ref carry becomes pack / unpack), and any future slice.
3. A candidate for the council to weigh (belam): a real `git bundle` file per pack (refs + objects, verifiable, carried as one file), which also answers the owner's 10-07 'a wrapper on git operations'. The council decides.

4. (owner 20:4xZ) The pack IS a capsule payload: the capsule (goal:g7.16.1.11.4, horizon, DG3; build phase A in doc:g716111-capsule-build) becomes the ONE envelope for secrets AND graph slices. Flags on ONE format: signed ALWAYS; encrypted y/n; quorum-pop y/n. TENSION to rule by name (council): .4's title says 'always-encrypted, popped only by the weighted MUTUAL quorum'; belam's reading: secret payloads (deploy keys, signing keys) keep always-encrypted + the quorum pop, slice payloads may be plain-signed or encrypted when the owner or the slice asks. .4 stays in the .11 HOLD for key/identity work; its DESIGN is now shared with this one, and the design may land before any key round runs.

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops.
- D2's REGROW falsifier holds: unpack(pack(slice)) == the slice, byte for byte, apart from the named cells.

## Falsifier
1. (design) the council's design names the format, the attach rule, the render rule and each verb with its own falsifier row.
2. REGROW: for a real slice (one post's nodes + refs), unpack(pack(slice)) on a scratch repo == the slice byte for byte, apart from the named cells.
3. SIGNATURE: a tampered pack is REFUSED at unpack; an untampered one unpacks byte-identical.
4. The next box move after the verbs land is done by pack / carry / unpack, and counts per namespace match (goal:g7.16.1.11.39's check).

## Out of scope
goal:g7.16.1.11.41 (projection: it comes FIRST, the season-2 close gate) · history rewrite (owner only).

## Order
After goal:g7.16.1.11.41, before the season-2 close; the next box move can be its first real use.

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 39 20:3xZ 10-11: minted (and 20:4xZ: the capsule addendum folded in) to hold the owner's words (owner verbatim lives in nodes) and the council's design ask; belam's 20:3xZ [owner] relay. Build leaves (one per verb) are placed by SM after the design.
<!-- THOUGHT:END -->
