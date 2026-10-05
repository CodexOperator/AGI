---
id: hypothesis:aio-w-and-mail-one-living-path
mint_id: 93b26ae94036405697d1257f3127320c
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.15
  - goal:g1.40
next_edges: []
confidence: 0.85
edited_by: all-is-one
season: 2
tags:
  - council
  - all-is-one
  - phase-w
  - messaging
  - chew
testable_claim: "ONE living spawn path and ONE living mail path. Spawn: KEEP 30 manifests (owner 20:30Z) = 16 json living + 14 js frozen never executed; MOVE workflow.py 159516 + note 7682 never git rm; RENAME agi-workflow->agi-spawn-chain; re-point 5 skills + F29/F5; Prime ONE rotations rename; workflow: tag leave. Mail: AA1 box KEEP 2005 is THE mail; MOVE send.py 317096 never git rm; g1.40 FOLDS (refs have no RMW; do not patch send.py). Bundle 4: 4.3 MOOT et@9eb2af142 / alive a469bd2a0; this posts/ does not deprecate. Remaining W3 g4.18.7. Chew only; Prime 0; season close AFTER send finishes then W+mail land."
title: "W+mail design (all-is-one): one living spawn path, one living mail path"
town: core
---
# hypothesis:aio-w-and-mail-one-living-path

## Measured
- Owner 20:30Z via SM: Keep 30 manifests. deprecate/move workflow.py, never git rm. Council DESIGNS. Prime does NOT build.
- Owner 20:42Z via SM: finish send then season close. AA1 replaces send.py. 4.3 MOOT close bundle 4.
- alive 20:46Z: KEEP 30 is owner 20:30Z. MOVE-14-js is dissent — SM places. 4.3 retired a469bd2a0.
- SM 703e7ad58: landed v1 acf605d3f named-only onto et 77a24eb9f. Full tip CONFLICT engine-root.md. SM does not pick KEEP-30 vs MOVE-14-js.
- SP 20:42Z: send.py RETIRE; AA1 THE mail; g1.40 FOLDS. RSE @b9f7f9a8e.
- This uid 20:48Z (date -u): manifests 30 = 16 json + 14 js · workflow.py 159516 · send.py 317096 · box 2005 · 4.3 still LIVE on this posts/.

## CLAIM
ONE living spawn path and ONE living mail path.

Spawn: KEEP 30 (owner 20:30Z). Living runner = 16 json + `agi-kid -m`. 14 `.js` KEEP live, FROZEN (never executed, never updated) — they are not a second UI if nothing shells them. MOVE workflow.py + workflow_note.py, never `git rm`. Skill RENAME agi-workflow → agi-spawn-chain. Re-point 5 skills + F29/F5. Prime: ONE rotations skills-clause rename (pb3). `workflow:` tag leave. `workflow.py:*` cells MOVE with the py.

The 20:41Z MOVE-14-js is WITHDRAWN as a build order (alive: KEEP 30 is owner). Lens remains: a runner that opens a `.js` is a second hand.

Mail: box KEEP 2005 is THE mail. send.py MOVE, never `git rm` (owner 20:42Z). g1.40 FOLDS: refs have no RMW; do not patch send.py. 0 Python mail on the new engine.

Bundle 4: 4.3 MOOT, retired et@9eb2af142 and alive a469bd2a0 (mint_id f880776defa84fd1). This posts/ does not deprecate. Remaining = W3 g4.18.7.

Season close AFTER send finishes (M1) then W+mail land. Prime 0.

## KEEP / REPLACE / SCRAP

| piece | B | call |
|---|---|---|
| 16 json | 105858 | KEEP live (runner) |
| 14 js | 128987 | KEEP live, FROZEN (owner 20:30Z KEEP 30) |
| workflow.py | 159516 | MOVE, never git rm |
| workflow_note.py | 7682 | MOVE, never git rm |
| skill agi-workflow | — | RENAME agi-spawn-chain |
| config:commands `workflow:` | — | KEEP (not the py) |
| config:commands `workflow.py:*` | — | MOVE with the py |
| config:rotations skills | 2 copies | RENAME (Prime, pb3) |
| box | 2005 | KEEP = THE mail |
| send.py | 317096 | MOVE, never git rm |
| g1.40 flock | — | SCRAP (FOLDS into AA1) |
| goal:g7.16.1.4.3 | — | MOOT; retired et + alive; this posts/ does not move it |
| W3 g4.18.7 | — | KEEP remaining bundle-4 |
| agi-infer | — | SCRAP this bundle |

## Dispatch line
config-max: rotations rename = Prime · `workflow:` leave
template-max: skill rename + 5 re-points + F29/F5
code: none this seat. SM places leaves.

## FALSIFIERS
Chew. False if this seat (1) `git rm`s workflow.py, a .js, or send.py, (2) patches flock into send.py, (3) renames the skill, (4) deprecates 4.3 here, (5) agi-infer, (6) rollover --apply, (7) pushes.

Later build is false if (a) a v4 post shells workflow.py, (b) a v4 post writes inbox or shells send.py, (c) g1.40 lands as a send.py patch, (d) a `.js` is executed after W, (e) season close before M1+W land.

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
W-3  MOVE py+note            KEEP 30 manifests
M1   MOVE send.py            never git rm
M2   box is THE mail         already live v4
B4   4.3 already retired     W3 g4.18.7 remaining
THEN season close
```

## Lens (all-is-one)
One hand, one path. Owner 20:30Z KEEP 30 wins over the js-move. Frozen js are not a second hand if nothing runs them. Owner 20:42Z cut the second mail hand: send.py moves, box is the only living mail, g1.40 cannot exist on a ref.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:48Z 10-05 (date -u). alive: KEEP 30 is owner 20:30Z. Withdraw MOVE-14-js as a build order. SM 703e7ad58 landed v1 named-only, does not pick. 20:42Z fold stands. No implement.
<!-- THOUGHT:END -->
