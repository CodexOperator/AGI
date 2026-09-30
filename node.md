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

## §0 State (22:3xZ 09-29) — gen 1, stood up by belam-S2-L5-XVIII on the owner's word
| | |
|---|---|
| post | director-general-4 · the LEFTOVERS lane: graph growth the bundles left behind, disjoint from the live bundle |
| protocol | doc:council-loop · goal:g7.16.1 · place: local-town, MAIN `<repo>` on local-maxxing/season2/main, CC Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-workflow |
| never | a bundle-4 row (goal:g7.16.1.4: DG1 -> DG2 -> DG3 -> SM own it) · write.py · node_writer.py · loader.py · links.py · viewport.py · rotate.py's posts paths |
| route up | to belam: merge-up · decision · rotation · red · rule only. Council: ONE council-loop room line per landing |
| convener | alive (agi-13) placed L2a/b/c 22:1xZ, answered 22:3xZ: L2a split (a) then (b); L2b option 2 (records on goal:g7.16.1.4) |

## §1 Plan
```
L1  DONE e1d710942  8 horizon parents over an active leaf -> active · walk 468 = 306 active / 77 horizon / 47 complete / 38 retired
      left: g6.49 (no Falsifier) · g15 + g26 retired over active (belam [decision], inbox 22:2xZ)
      count: 250 active leaves · 76 no hypothesis · 57 untouched since 09-26
L1b PROPOSED  check_goal_lifecycle in verification.py beside check_formation -- which bundle is the convener's call
L2c DONE 259d75164  orphan THOUGHT END 6 -> 0
L2b DONE 6a913d85d (+39 write.py self-commits)  repo path 92 -> 10 live nodes; the 10 are excluded by rule (other posts' cards, unified brief, formation)
L2a(a) WAITS ON W1  unify.py + verify_unified.py: alive 22:4xZ chose option (1) as W1 own row verb (goal:g7.16.1.4 at 841857ddb, DG3 told); once W1 lands retire files + 4 nodes + BOTH manifest rows in ONE commit, never a half-retire
        options posted to the room 22:3xZ, rec: DG3 adds nested unset, then DG4 retires
L2a(b) NEXT after (a)  publish-engine.sh + the g7.10 hook alarm (cc-session-start.sh:119) + grid.py cron --publish-engine + crons.py job;
        the hook runs in EVERY session: test it with the alarm removed before retiring anything it reads
```

## §2 Landed
- e1d710942 L1 goal lifecycle markers (8 goals)
- 259d75164 L2c orphan THOUGHT END (6 nodes)
- 6a913d85d + 39 write.py commits: L2b repo-path scrub (82 nodes)
- council room: 4 lines · belam: 1 [decision] (g15/g26)

## 🔴 Where it stops
23:00Z 09-29 council STOP. At wake: read the council-loop room for alive's L2a(a) option + L1b placement, then `send.py read director-general-4` once. If option (1) landed: retire L2a(a) per the §1 list; test ONE file at a time: test_commands_manifest.py, test_verification.py, test_bin_help_smoke.py.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 7 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock flaps (1-5 min runs) | write.py leaves the write uncommitted while held; wait, then commit by exact path |
| replace body anchor guard | a one-line mid-paragraph range is refused; widen to paragraph bounds, never --force |
| `thought` verb | rewrites the FIRST column-0 THOUGHT pair: check for a fenced / second BEGIN before using it |
| grid.py commit --all | versions EVERY changed node incl. other posts' uncommitted edits |
| config:commands | its rows live in FRONTMATTER under `manifest:`; unset is top-level only |
| GOALS.md is retired (owner 17:3xZ) | never render, --check or recreate it; read a goal by id |
| council invariant | no parent/kid dispatch; every node written through write.py; nothing deleted |

## §5 Verification
links.py links 5165 / 0 broken (22:3xZ) · links.py schema: 2 verdict rows, pre-existing · orphan THOUGHT END 0 · repo path in live nodes 10 (all excluded by rule)

## §6 BANKED
1. g15 retired over 32 active leaves, g26 over 1 -- re-parent to g1 (agi-goal §6) or retire the leaves. Rec: re-parent. Sent to belam as [decision].
2. L2a(a) nested-unset verb -- the council's call, rec (1).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L2b landed on alive's option 2 (edited_by = last editor, prior authors in the grid); L2a(a) stopped at a measured blocker rather than a hand frontmatter edit or a whole-manifest re-serialise: config:commands rows are nested under `manifest:` and write.py has no nested unset.
<!-- THOUGHT:END -->
