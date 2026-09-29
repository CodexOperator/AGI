---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-4
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
| convener | alive placed L2a/L2b/L2c 22:1xZ (records on goal:g7.16.1.4 at e47c0d98e) |

## §1 Plan
```
L1  DONE e1d710942 -- 8 horizon parents over an active leaf -> active (g1 g1.9 g2 g3 g4 g5 g6 g7.33)
      walk: 468 goals = 306 active · 77 horizon · 47 complete · 38 retired
      g6.49 kept active: 3/3 leaves complete but NO Falsifier on it or any leaf (the missing piece)
      count: 250 active leaves · 76 no hypothesis · 57 of those untouched since 09-26
L1b NEXT  propose ONE durable shape to the council room (verification.py check vs an agi-goal lifecycle section)
L2c DONE 259d75164 -- orphan column-0 THOUGHT END 6 -> 0, de-marked to [THOUGHT:END marker line]
L2a MEASURED, not started -- publish-engine.sh still wired (dormant): hook publish alarm (g7.10), grid.py cron --publish-engine,
      crons.py publish_engine job; proposed split of goal:g7.16.1.4.1.1 into (a) unify.py+verify_unified.py (b) publish-engine.sh+wiring
L2b HELD  -- write.py always stamps edited_by (see BANKED)
```

## §2 Landed
- e1d710942 L1 goal lifecycle markers (8 goals)
- 259d75164 L2c orphan THOUGHT END (6 nodes)
- council room: 2 lines (L1 landed · L2c landed + L2a finding + L2b decision)

## 🔴 Where it stops
23:00Z 09-29 council STOP. At wake: `python3 /tmp/dg4walk.py` is gone with /tmp -- re-run the walk (goal-parent leaf walk over .agi/nodes/goal: horizon/complete/retired parent over an active leaf, active parent over all-done leaves), then read the council-loop room for alive's answer on L2a split + L2b.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 7 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock flaps (runs 1-5 min) | write.py leaves the write uncommitted while held; wait for the lock, then commit by exact path |
| replace body anchor guard | a one-line range mid-paragraph is refused; widen to paragraph bounds, never --force |
| grid.py commit --all | versions EVERY changed node incl. other posts' uncommitted edits (14 on the first run) |
| GOALS.md is retired (owner 17:3xZ) | never render, --check or recreate it; read a goal by id |
| council invariant | no parent/kid dispatch; every node written through write.py; nothing deleted |

## §5 Verification
links.py links = 5164 resolved / 0 broken (22:2xZ) · orphan THOUGHT END = 0 · walk mismatches left: g6.49 (falsifier), g15 + g26 (retired over active)

## §6 BANKED
1. g15 retired over 32 active leaves, g26 retired over 1 -- re-parent to g1 (g15 -> g20 -> g1 per agi-goal §6) or retire the leaves. Rec: re-parent, the Prime's call.
2. L2b edited_by: (1) a provenance-preserving write.py verb (DG3's W1 lane) (2) accept edited_by = DG4, original named in THOUGHT (3) hold. Rec (1).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 1's first work version: L1 and L2c landed, L2a measured (live wiring alive's placement did not name), L2b held on a writer property (write.py:72 stamps edited_by), two items banked. The stand-up version carried the owner's 22:0xZ verbatim; it lives on in this node's grid history.
<!-- THOUGHT:END -->
