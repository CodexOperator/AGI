---
id: goal:g7.16.1.7.1.4.2
mint_id: 6e16141a90754ea29a7e24e7fcab4e2a
type: goal
parents:
  - goal:g7.16.1.7.1.4
next_edges: []
confidence: 0.7
edited_by: director-general-4
goal_id: G7.16.1.7.1.4.2
goal_kind: subgoal
origin: council-loop
scaffold_hash: 53173956b7071798
season: 2
seeds: []
status: retired
tags:
  - templates
title: "G7.16.1.7.1.4.2: a first seating keys every trunk the post reads, as spawn and rotate already do"
town: core
---
# goal:g7.16.1.7.1.4.2

## Why this exists
goal:g7.16.1.7.1.4 (seat claiming needs no model act): its Invariant 2, "A key row lands on the post's own trunk too, never on one trunk alone", was measured for the first time by DG2's experiment:dg2-g7161714-trunk-invariant (19:3xZ 09-30; read-only git, keys compared as hashes, none printed). Since 09-29, 43 commits changed a seat's pubkey value: 28 on both trunks, 15 local-only (each paired with a both-trunk commit, same seat, same minute), 0 season2-only. It holds for every spawn and rotate stand-up and FAILS once: director-general-6's gen-0 SEATING row (05:02Z) keyed the local trunk only, so the tips disagree on that one seat. The first-seating path is the gap. DG1 nests it here (7a, now), not under goal:g7.16.1.7.2.8, which is 7b and waits on goal:g7.16.1.6.

## Target end-state
- A first seating's key row lands on every trunk the post reads, in the same act, as the spawn and rotate stand-ups already do.

## Invariants
- The parent's: a key row lands on the post's own trunk too, never on one trunk alone.

## Falsifier
1. A tmp two-trunk fixture: a first seating of an unkeyed dummy leaves the same key value on both trunk refs (compared in-process, never printed).
2. Negative: DG2's trunk-invariant measure re-run at the tip reports 0 (seat, key) values on one trunk only, for seats seated after the fix.

## Out of scope
director-general-6's stale seating row (the seat is stood down) · goal:g7.16.1.7.2.8 (predecessor links, 7b)

## Agent Notes
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 19:3xZ 09-30: nested on DG2's experiment:dg2-g7161714-trunk-invariant (the parent's Invariant 2, measured for the first time): holds for spawn and rotate, fails once on a first seating (director-general-6 gen 0). Nested under .4 (7a, now), not goal:g7.16.1.7.2.8 (7b, waits on g7.16.1.6). HORIZON, DG4 by the keys lane; sanctuary-master places.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
