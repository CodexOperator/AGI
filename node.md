---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
---
# doc:card-director-general-4

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (22:2xZ 09-29) — gen 1, stood up by belam-S2-L5-XVIII on the owner's word
| | |
|---|---|
| post | director-general-4 · the LEFTOVERS lane: graph growth the bundles left behind, disjoint from the live bundle |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN /data/work/agi on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-workflow |
| never | a bundle-4 row (goal:g7.16.1.4: DG1 -> DG2 -> DG3 -> SM own it) · write.py · node_writer.py · loader.py · links.py · viewport.py · rotate.py's posts paths |
| route up | to belam: merge-up · decision · rotation · red · rule only. Council: ONE council-loop room line per landing |

## §1 Plan
```
L1  GOAL LIFECYCLE MARKERS by a recursive leaf walk (owner 22:0xZ). Measured by belam 22:0xZ over .agi/nodes/goal:
      467 goals = 298 active · 84 horizon · 47 complete · 38 retired
      8 horizon parents over an ACTIVE leaf: g1 g1.9 g2 g3 g4 g5 g6 g7.33  -> active
      1 active parent, every leaf complete/retired: g6.49                  -> complete ONLY if its own falsifier holds, else name what is missing
    re-measure first (the numbers move) · each fix = write.py goal:<id> 'set status <s> && thought <why>' (skill agi-goal)
    then COUNT (numbers only, never demote): active leaves with no hypothesis and no commit touching them since 09-26
L1b the walk as a durable check: propose ONE shape to the council room (a verification.py check vs an agi-goal lifecycle section);
    the owner is unifying skills on core, so the trunk edit stays one section / one check, never a new skill
L2  leftovers the council places (ask alive, the convener; never self-place over a bundle row):
      goal:g7.16.1.4.1.1 retire unify.py · verify_unified.py · publish-engine.sh (horizon, placed in bundle 5)
      DG2 §6 findings: 87 nodes carry the repo path · the writer stamps town: core for local-town posts · 8 nodes carry a surplus THOUGHT END
```

## §2 Landed
(none yet)

## 🔴 Where it stops
23:00Z 09-29 = the council STOP (owner: "Keep working till 7pm"): finish the step, card whole, idle. Next command at wake: re-run the L1 walk.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 7 posts | commit by exact path; never commit, reset or stash another post's file |
| PASS B3 runs 23:33Z on this box | tests ONE file at a time; no MAIN commit while .agi/sessions/verify-suite.lock exists |
| GOALS.md is retired (owner 17:3xZ) | never render, --check or recreate it; read a goal by id |
| council invariant | no parent/kid dispatch; every node written through write.py; nothing deleted |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · `python3 extensions/agi/bin/links.py schema` · the L1 walk re-run shows 0 mismatches

## §6 BANKED
(none)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner's 22:0xZ order, verbatim: "Can we spin up another director-general to tackle more of the leftover graph growth from the bundle? The goals should have proper active markers since the lifecycle skill should include recursive leaf walking from the core/season2/main branch." Then: "It may be in the director briefs in that branch" and "I'm still working on unifying things. That branch is working on the magic pane system". The Prime searched core/season2/main (briefs, skills, bin): no leaf walk exists there yet, so L1 measures and fixes the markers here and L1b only proposes the durable shape. The lane stays disjoint from bundle 4 because the council invariant is one director per bundle.
<!-- THOUGHT:END -->
