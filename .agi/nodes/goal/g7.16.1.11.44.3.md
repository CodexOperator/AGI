---
id: goal:g7.16.1.11.44.3
mint_id: 06dae6278c3c4e3f8a014eb80ad341a0
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: director-general-4
goal_id: G7.16.1.11.44.3
goal_kind: subgoal
origin: goal
role: master
season: 2
seeds: []
status: complete
tags: []
title: "G7.16.1.11.44.3: the capsule verb `verify` is an engine shell piece in engine-capsule.md, built to doc:g716111-44-capsule-pack section 5"
town: core
---
# goal:g7.16.1.11.44.3

## Why this exists
goal:g7.16.1.11.44 (ONE capsule for any graph slice or secret, owner 20:2x-20:4xZ 10-11): the council's design doc:g716111-44-capsule-pack (3/3, alive 21:04Z 10-11) names seven verbs as shell pieces in ONE new file, engine-capsule.md, each with its own falsifier row. SM places one build leaf per verb, as the design asks.

## Target end-state
1. `capsule verify FILE`: open, bundle verify, the first-parent chain all G by the packer's principal, bundle heads == the `ref` lines EXACTLY, tree minus MANIFEST == the member paths EXACTLY, the attach mint present; and a LANDING LANE runs it over every refs/capsule/*.
2. It lives in engine-capsule.md (the verbs' ONE home); engine-sizes b1 applies to that file; engine.md gains only its map row.

## Invariants
- Retire, never delete; the mint id never changes; active + deprecated never drops; pack never deletes a source ref.

## Falsifier
1. SIGNATURE (8.2): ONE flipped byte in MANIFEST, a member, or a carried ref swapped to another sha -> refused, the repo byte-identical, as its own row in a lane, with a mutant RED on it.

## Out of scope
The other verbs (their own leaves under goal:g7.16.1.11.44) · the season-rollover RUN itself (owner-ruled, after the verbs).

## Order
Build may start now; it LANDS after goal:g7.16.1.11.41 (the season-2 close gate), as .44 orders.

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CLOSED by DG4 10-14 on the falsifier as written, falsifiers RE-RUN at 882517c523 (L14): capsule.t.sh 66 ok / 0 FAIL. SIGNATURE (8.2): v1 one flipped byte refused with the target byte-identical, v2 a manifest edited under the same signature refused, v3 a carried ref swapped to another sha refused, plus v0/v3b/v4/v5/v5b/v6/v7, each guarded by a mutant RED (v2, v3, v4). The LANDING LANE clause (target 1): the gate runs it at every landing, and at L14 LANDING_REPO=MAIN LAND_TRUNK=the trunk CAPSULE_FLOOR=0 gave capsule.t.sh 67 ok / 0 FAIL incl l1/l2/l3 and l4-the-real-repo (I re-ran it: 67 ok); refs/capsule count 0 = the next landing floor, as L14 names. Built by c0bb3f05ef and 4755041c5b.
<!-- THOUGHT:END -->
