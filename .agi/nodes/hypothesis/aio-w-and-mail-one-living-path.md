---
id: hypothesis:aio-w-and-mail-one-living-path
mint_id: 93b26ae94036405697d1257f3127320c
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.15
  - goal:g1.40
next_edges: []
confidence: 0.8
edited_by: all-is-one
season: 2
tags:
  - council
  - all-is-one
  - phase-w
  - messaging
  - chew
testable_claim: "ONE living spawn path and ONE living mail path. Spawn: 16 json manifests live; agi-kid -m is the runner; workflow.py 159516 + workflow_note 7682 + 14 js MOVE (never git rm); skill agi-workflow RENAME agi-spawn-chain; re-point agi,corrective,master-gate,merge-pass,dispatch + F29/F5; ONE rotations skills rename (Prime); config:commands workflow: tag is NOT workflow.py (leave); workflow.py:* cells MOVE with the py. Mail: AA1 box KEEP 2005; send.py stays old-setup only; g1.40 flock on inbox RMW only while send.py still writes (pattern already at _foreign_memo_lock), never a second mail. Chew only; Prime does not build; season close AFTER these land."
title: "W+mail design (all-is-one): one living spawn path, one living mail path"
town: core
---
# hypothesis:aio-w-and-mail-one-living-path

## Measured
- Owner 20:30Z via SM: Council DESIGNS. Prime does NOT build. Land Phase W (g7.16.1.11.15 UNHELD) + messaging (g1.40 + AA1) before season close. Skip agi-infer. SM gates. No push.
- Prime hyp:phase-w-and-messaging-council-designs-then-dg-sm on et 2cc3e4e0e (50 lines), not this HEAD. Not copied.
- SP @de7dbcd09 / 99202ea6d: KEEP 30 (16 json+14 js) · MOVE workflow.py 159516 + note 7682 never git rm · RENAME agi-workflow→agi-spawn-chain · re-point · `workflow:` tag ≠ workflow.py · AA1 KEEP · g1.40 flock only while send.py writes.
- alive e1db70125: this v5 seat already boxes; send.py PermissionError; same KEEP 30.
- This uid 20:41Z (date -u): manifests 30 = 16 json (105858) + 14 js (128987) · workflow.py 159516 · note 7682 · send.py 317096 · box 2005 · skills/agi-workflow present, agi-spawn-chain absent · rotations skills: two copies of one `build:skills-agi-workflow-SKILL.md` clause · send.py `open(inbox,"a")` :3337 unlocked vs `inbox.write_text` :4312 · flock exists only on pending-count + foreign-memo, not inbox · this seat: `box read` drained alive W+mail chew; `send.py read` PermissionError on MAIN dm state.

## CLAIM
ONE living spawn path and ONE living mail path.

Spawn living = json manifest + graph slice + `agi-kid -m` (W-1 already). The 14 `.js` are workflow.py:author's generated half — a second hand. MOVE them WITH workflow.py + workflow_note.py (deprecate+move, never `git rm`); 16 json KEEP live; 14 js KEEP as deprecated (sum never drops). Skill RENAME agi-workflow → agi-spawn-chain (owner 17:4xZ). Re-point skills agi / agi-corrective / agi-master-gate / agi-merge-pass / agi-dispatch + rotations facts F29/F5. Prime: ONE rotations skills-clause rename (two copies, pb3). `config:commands` `workflow:` tag on smoke/tests/… is NOT workflow.py — leave. `workflow.py:*` cells MOVE with the py.

Mail living = `box` (AA1 KEEP, 2005 B, 0 zygote). send.py is the old-setup hand until those posts move. g1.40 flock is a bandage on THAT hand only: one `<inbox>.lock` around append AND mark-read rewrite (copy `_foreign_memo_lock` :2423, never a new primitive). AA1 needs no flock (update-ref is the lock). This uid already boxes.

Season close (outcomes → bigger_outcomes → overviews) only AFTER W + g1.40-or-AA1 land. Prime does not implement.

## KEEP / REPLACE / SCRAP

| piece | B | call |
|---|---|---|
| 16 json manifests | 105858 | KEEP live (spawn docs) |
| 14 js | 128987 | MOVE with workflow.py (generated half; never git rm) |
| workflow.py | 159516 | MOVE, never git rm |
| workflow_note.py | 7682 | MOVE, never git rm |
| skill agi-workflow | — | RENAME agi-spawn-chain |
| build:skills-agi-workflow-SKILL.md | — | retire; new build id for renamed skill |
| config:commands `workflow:` | — | KEEP (not the py) |
| config:commands `workflow.py:*` | — | MOVE with the py |
| config:rotations skills clause | 2 copies | RENAME (Prime, pb3) |
| box | 2005 | KEEP (AA1 living mail) |
| send.py | 317096 | KEEP until last old-setup post moves |
| g1.40 flock | ~40 | REPLACE-BY existing flock pattern, old-setup inbox only |
| agi-infer | — | SCRAP this bundle (owner skip) |
| season.py rollover --apply | — | SCRAP until SM.113/114 |

SP/alive KEEP-30-live (js stay in `extensions/agi/workflows/`). Dissent: a live `.js` beside a live `.json` is two hands; a runner that never opens `.js` still leaves a second UI. SM picks. If KEEP-30-live wins: freeze js (never executed, never updated) — still not the living path.

## Dispatch line
config-max: rotations skills rename = Prime at merge-up · `workflow:` tag leave · `workflow.py:*` cells move with py
template-max: skill rename + 5 re-points + F29/F5
code: none this seat. W-3 MOVE. g1.40 flock only in send.py inbox RMW, old-setup. AA1 no new piece.
Council does not dispatch. SM places leaves. DG inner loops. mur. land. THEN season close.

## FALSIFIERS
Chew. False if this seat (1) `git rm`s workflow.py or a .js, (2) writes flock into send.py, (3) renames the skill, (4) runs agi-infer, (5) `season.py rollover --apply`, (6) copies Prime's hyp onto this tree, (7) pushes.

Later build is false if (a) a v4 post's review still shells workflow.py, (b) `workflow:` tag cells are deleted, (c) a v4 post writes `.agi/sessions/inbox`, (d) season close starts before W+mail land.

## TESTS
none that write. Neighbourhood: `ls extensions/agi/workflows \| wc -l` = 30 · `wc -c` box = 2005 · `AGI_POST=all-is-one box n` empty after this read · send.py inbox flock grep = 0 today.

## FILE SCOPE
this node + card. No engine. No workflow.py move. No skill rename. No send.py edit. No et merge.

## CEILING
council design · 0 zygote bytes · reuse box + agi-kid -m · no push

## Order (SM leaves)

```
W-1  agi-kid -m          already (DG3 10-03)
W-2  skill rename+repoint + Prime rotations sub
W-3  MOVE py+note+14 js  after Z4.e 24h (0 workflow.py in ~/track)
g1.40 flock              parallel, old-setup send.py only; closes when last old-setup moves
AA1                      KEEP; host acts stay Prime GO, not this bundle
THEN season close
```

## Lens (all-is-one)
One hand, one path. Spawn and mail each have one living route; every other file is a retired twin, not a second UI. A bandage (flock) on a dying hand is allowed; a new mail primitive beside box is not. Derived copies (the .js) are not a second source of truth.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:41Z 10-05 (date -u). Owner 20:30Z via SM: council DESIGNS, Prime does not build. Dissent from SP/alive KEEP-30-live is the .js: generated half, two hands. Mail agrees (box KEEP, flock only while send.py writes). No implement.
<!-- THOUGHT:END -->
