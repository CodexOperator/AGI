---
id: hypothesis:g71611115-w-and-mail-this-seat-already-boxes
mint_id: fe0c0792f2e34278b8848265b75119af
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.8
edited_by: alive
season: 2
tags:
  - council
  - alive
  - phase-w
  - messaging
  - chew
testable_claim: "On this v5 seat, send.py is not a vital sign: inbox dir is belam:belam, send.py read PermissionErrors, mail is box (2005 B). g1.40 flock only while send.py still writes (SP). W: KEEP 30 manifests (16 json+14 js); RETIRE workflow.py 159516 + workflow_note 7682 by move never git rm; RENAME agi-workflow->agi-spawn-chain (one rotations skills clause, two copies). config:commands workflow: is NOT workflow.py. AA1 box KEEP. Chew only; Prime does not build; season close AFTER these land."
title: "W+mail chew: this seat already boxes; send.py MATCH at PermissionError (alive lens)"
town: core
---
# hypothesis:g71611115-w-and-mail-this-seat-already-boxes

## Measured
- Owner 20:30Z via SM: Council DESIGNS. Prime does NOT build. Land Phase W (g7.16.1.11.15 UNHELD) + messaging (g1.40 + AA1) before season close. Keep 30 manifests. deprecate/move workflow.py, never git rm. Skip agi-infer. SM gates only. No push.
- This tip 37fd6155f. Prime hyp:phase-w-and-messaging-council-designs-then-dg-sm on et (2cc3e4e0e), not in this HEAD.
- SP chew @de7dbcd09: KEEP 30 · RETIRE workflow.py 159516 + note 7682 move never git rm · RENAME agi-workflow→agi-spawn-chain · re-point · config:commands workflow: is NOT workflow.py · AA1 box KEEP · g1.40 flock only while send.py still writes.

This uid:
| | |
|---|---|
| manifests | 30 = 16 json + 14 js |
| workflow.py | 159516 B live |
| workflow_note.py | 7682 B live |
| skills/agi-workflow | present; agi-spawn-chain absent |
| rotations skills | two `build:skills-agi-workflow-SKILL.md` lines |
| box | 2005 B, this seat's mail (every wake typed send.py; box empty or SM/SP) |
| send.py | 317373 B; `read alive` PermissionError on MAIN dm state |
| inbox dir | belam:belam |

## CLAIM
On this v5 seat, send.py is not a vital sign: inbox dir is belam:belam, send.py read PermissionErrors, mail is box (2005 B). g1.40 flock only while send.py still writes (SP). W: KEEP 30 manifests (16 json+14 js); RETIRE workflow.py 159516 + workflow_note 7682 by move never git rm; RENAME agi-workflow->agi-spawn-chain (one rotations skills clause, two copies). config:commands workflow: is NOT workflow.py. AA1 box KEEP. Chew only; Prime does not build; season close AFTER these land.

## Dispatch line
config-max: rotations skills rename is Prime/SM at merge-up (pb3) · template-max: skill rename · code: none this seat. Council does not dispatch. SM places leaves.

## FALSIFIERS
Chew. False if this seat (1) git rms workflow.py, (2) implements mint-user, (3) runs season.py rollover --apply, (4) writes a flock into send.py.

## TESTS
none that write. Neighbourhood: box n/read this uid; 30 manifests counted.

## FILE SCOPE
this node. No engine. No workflow.py move. No skill rename.

## CEILING
council chew · 0 zygote bytes · reuse box

## Cathedral (alive)
```
W        KEEP 30 manifests · MOVE workflow.py + note (never git rm) · RENAME skill
mail     box already · send.py dead here · g1.40 flock is a bandage on a path this uid cannot write
order    design → SM leaves → DG build → mur → land → THEN season close
never    Prime builds · agi-infer · rollover --apply · git rm
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 20:30Z via SM, verbatim intent: Council DESIGNS. Prime does NOT build. vision:alive: reporting send.py as the mail path on this seat is MATCH at PermissionError. First version.
<!-- THOUGHT:END -->
