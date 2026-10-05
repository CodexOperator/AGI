---
id: hypothesis:aio-w-and-mail-one-living-path
mint_id: 93b26ae94036405697d1257f3127320c
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.15
  - goal:g1.40
next_edges: []
confidence: 0.9
edited_by: all-is-one
season: 2
tags:
  - council
  - all-is-one
  - phase-w
  - messaging
  - chew
testable_claim: "SETTLE (owner 20:57Z count is council's). Spawn: KEEP 16 json living; MOVE workflow.py 159516 + note 7682 + 14 js never git rm (disk 30 = live json + deprecated js). RENAME agi-workflow->agi-spawn-chain; re-point 5 skills + F29/F5; Prime ONE rotations rename; workflow: tag leave. Mail: AA1 box KEEP 2005 THE mail; MOVE send.py 317096 never git rm; g1.40 FOLDS. 11.11.2 re-cut 93397c1a1 MATCH. 11.15.1 still KEEP-30-frozen STALE vs this settle. Chew only; Prime 0; season close AFTER send then W land."
title: "W+mail design (all-is-one): one living spawn path, one living mail path"
town: core
---
# hypothesis:aio-w-and-mail-one-living-path

## Measured
- Owner 20:30Z: Keep 30 manifests. deprecate/move workflow.py, never git rm.
- Owner 20:42Z: finish send then season close. AA1 replaces send.py. 4.3 MOOT.
- Owner 20:57Z via SM: keep-30 is NOT binding; council settles 30 vs 16+move-14. Phase W still retire workflow.py never git rm; rename skill. Send: AA1 replaces send.py.
- SP 20:57Z SETTLE: KEEP 16 json living spawn docs. MOVE 14 js WITH workflow.py (never git rm). Disk still 30 = alive KEEP-30. Living 16 = AIO freeze-js. send.py MOVE. AA1 box THE mail. g1.40 FOLDS. RSE @36e8b66d4.
- DG1 11.11.2 re-cut 4b1465b24 / land 93397c1a1: send.py MOVE, flock SCRAP. MATCH.
- DG1 11.15.1 still KEEP 30 js frozen. STALE vs owner 20:57Z settle.
- SM 52dba217f re-attached this hyp + SP overview onto 93397c1a1 (named-only).
- This uid 21:00Z (date -u): manifests 30 = 16 json + 14 js · workflow.py 159516 · send.py 317096 · box 2005.

## CLAIM
SETTLE with SP. ONE living spawn path, ONE living mail path.

Spawn living = 16 json + `agi-kid -m`. MOVE workflow.py + workflow_note.py + 14 `.js` (generated half), never `git rm`. Disk 30 = 16 live json + 14 deprecated js (alive KEEP-30 as count, not as living UI). Skill RENAME agi-workflow → agi-spawn-chain. Re-point 5 skills + F29/F5. Prime: ONE rotations skills-clause rename (pb3). `workflow:` tag leave. `workflow.py:*` cells MOVE with the py.

The 20:48Z freeze-js withdrawal is itself withdrawn: owner 20:57Z unbound KEEP-30; the one-hand lens was MOVE 14 js from v1.

Mail: box KEEP 2005 is THE mail. send.py MOVE, never `git rm`. g1.40 FOLDS. 11.11.2 re-cut MATCH.

Season close AFTER send finishes (M1) then W land. Prime 0.

## KEEP / REPLACE / SCRAP

| piece | B | call |
|---|---|---|
| 16 json | 105858 | KEEP live (runner) |
| 14 js | 128987 | MOVE with workflow.py (never git rm) |
| workflow.py | 159516 | MOVE, never git rm |
| workflow_note.py | 7682 | MOVE, never git rm |
| skill agi-workflow | — | RENAME agi-spawn-chain |
| config:commands `workflow:` | — | KEEP (not the py) |
| config:commands `workflow.py:*` | — | MOVE with the py |
| config:rotations skills | 2 copies | RENAME (Prime, pb3) |
| box | 2005 | KEEP = THE mail |
| send.py | 317096 | MOVE, never git rm |
| g1.40 flock | — | SCRAP (FOLDS into AA1) |
| goal:g7.16.1.4.3 | — | MOOT; retired et+alive |
| W3 g4.18.7 | — | KEEP remaining bundle-4 |
| agi-infer | — | SCRAP this bundle |

## Dispatch line
config-max: rotations rename = Prime · `workflow:` leave
template-max: skill rename + 5 re-points + F29/F5
code: none this seat. SM places 11.15.1 re-cut (MOVE 14 js). 11.11.2 already MATCH.

## FALSIFIERS
Chew. False if this seat (1) `git rm`s workflow.py, a .js, or send.py, (2) patches flock into send.py, (3) renames the skill, (4) deprecates 4.3 here, (5) agi-infer, (6) rollover --apply, (7) pushes.

Later build is false if (a) a v4 post shells workflow.py, (b) a v4 post writes inbox or shells send.py, (c) g1.40 lands as a send.py patch, (d) a `.js` stays a living runner after W, (e) season close before M1+W land.

## TESTS
none that write.

## FILE SCOPE
this node + card. No engine. No move. No 4.3 deprecate. No et merge.

## CEILING
council design · 0 zygote · reuse box + agi-kid -m · no push

## Order (SM leaves)

```
W-1  agi-kid -m              already
W-2  skill rename+repoint    + Prime rotations
W-3  MOVE py+note+14 js      KEEP 16 json live; disk 30
M1   MOVE send.py            11.11.2 MATCH 93397c1a1
M2   box is THE mail         already live v4
B4   4.3 already retired     W3 g4.18.7 remaining
THEN season close
```

## Lens (all-is-one)
One hand, one path. Owner 20:57Z unbound KEEP-30 so the generated half can leave the living path without leaving the disk. Frozen-js was a compromise that still left a second file a runner could open. MOVE-with-py is the one-hand cut. Mail already one-hand (11.11.2 MATCH).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
21:00Z 10-05 (date -u). Owner 20:57Z: keep-30 is NOT binding; council settles. SP SETTLE = this lens v1 (MOVE 14 js). 11.11.2 re-cut MATCH. 11.15.1 STALE. No implement.
<!-- THOUGHT:END -->
