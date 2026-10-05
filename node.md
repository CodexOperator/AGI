---
id: hypothesis:aa1-v4-wake-still-shells-send-py
mint_id: 726d526853f843f9b630955d7cf37fcf
type: hypothesis
parents:
  - goal:g7.16.1.11.11.2
next_edges: []
confidence: 0.8
edited_by: director-thought-2
model: grok-4.6
role: director
season: 2
tags:
  - aa1
  - mail
  - encryption-town
testable_claim: "On encryption-town, box is 2005 B with 0 sessions/inbox hits; the v4 agi-run wake line still names send.py and .agi/sessions/inbox — so goal:g7.16.1.11.11.2 falsifier 1 (inbox grep on wake) and falsifier 2 (send.py grep on wake) are NOT met."
title: v4 agi-run wake still shells send.py; box itself has no inbox path
town: core
---
# hypothesis:aa1-v4-wake-still-shells-send-py

## Measured
- Owner [owner] 21:35Z IMPLEMENT NOW: send.py MOVE never git rm; AA1 box THE mail; standard loop; DT2 in the idle-DG list.
- goal:g7.16.1.11.11.2 on trunk (DG1 mint, SM placed). Falsifier 1: box cap AND `git grep sessions/inbox` on box + v4 agi-run wake = 0. Falsifier 2: v4 wake never opens send.py.
- This uid 21:39Z: `wc -c` box = 2005. `rg sessions/inbox` on box = 0. agi-run line 2–4: `f=$O/.agi/sessions/inbox/$AGI_SEAT.md` and `printf "mail: send.py read $AGI_SEAT"`. send.py still live 317680. `box n` empty.

## CLAIM
C1. box bytes = 2005 (AA1 cap).
C2. box script has 0 `sessions/inbox` hits.
C3. v4 agi-run wake names `.agi/sessions/inbox`.
C4. v4 agi-run wake names `send.py`.
C1 AND C2 AND C3 AND C4 → proved that 11.11.2 F1/F2 are not met (box is clean; wake is not). Any C1/C2 fail → void the "box KEEP" half. C3 or C4 false → the goal's F2 already holds.

## Dispatch line
config-max: none this round. template-max: agi-run wake should become `box n` (capsule piece, not this file). code: none this round (MOVE send.py is the NEXT leaf after this measurement). Measurement only.

## FALSIFIERS
- C1 ≠ 2005 → disproved
- C2 finds inbox in box → disproved
- C3 or C4 absent → the goal's F2 already holds (this hyp void)
- load of box / agi-run fails → void

## TESTS
No new test file. Commands on the experiment node.

## FILE SCOPE
this hypothesis, its experiment, its verdict, 11.11.2 thought/seeds. Not send.py. Not agi-run. Not git rm.

## CEILING
0 production lines, one builder, CPU, 0 USD. Wall cap 5 min. No billed spawn. No push.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 21:39Z 10-05 (date -u): owner IMPLEMENT NOW. Nested under 11.11.2 rather than waiting on SM board row (owner named DT2). Did not MOVE send.py this round (measure first). Did not git rm. Did not implement mint.
<!-- THOUGHT:END -->
