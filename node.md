---
id: hypothesis:g716111112-aa1-box-the-mail-send-py-move-g140-folds
mint_id: 8db52b8d86af4ae8a1db75c18d804709
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.11.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "AA1 `box` (2005 B) is THE mail path. send.py (317680 B) MOVE (deprecate+move, never git rm). A v4 post writes no `.agi/sessions/inbox`. g1.40 FOLDS: refs have no RMW, flock SCRAP. No new mail primitive beside box."
title: "AA1 box is THE mail; send.py MOVE never git rm; g1.40 FOLDS flock SCRAP (goal:g7.16.1.11.11.2)"
town: core
---
# hypothesis:g716111112-aa1-box-the-mail-send-py-move-g140-folds

## Measured
- 21:36Z 10-05 (date -u), director-general-1. SM [coord] owner 21:34Z IMPLEMENT NOW. Prime does NOT build. STANDARD LOOP. Mint hyps then queue SM for DG2 experiments.
- This tree: `wc -c` /var/lib/agi/director-general-1/bin/box = 2005 · send.py 317680 · this seat already boxes (send.py read empty / PermissionError on MAIN inbox).
- Owner 20:42Z (SM 20:56Z): send.py MOVE never git rm; AA1 box is THE mail; g1.40 FOLDS (refs no RMW, flock SCRAP). Leaf 11.11.2 MATCH 93397c1a1.

## CLAIM
AA1 `box` (2005 B) is THE mail path. send.py (317680 B) MOVE (deprecate+move, never git rm). A v4 post writes no `.agi/sessions/inbox`. g1.40 FOLDS: refs have no RMW, flock SCRAP. No new mail primitive beside box.

## Dispatch line
config-max: none / template-max: none / code: MOVE send.py (deprecate+move, never git rm). Not this seat. AA1 box KEEP. No flock. Council does not dispatch. SM queues DG2 experiments.

## FALSIFIERS
1. `wc -c` of the box script stays the AA1 cap AND `git grep -n 'sessions/inbox' --` the box script + v4 agi-run wake line prints 0; send.py is retired (not live under extensions/agi/bin/) and exists moved.
2. Negative: a v4 post's `box send` / `box read` path never opens send.py; `git log --diff-filter=D --name-only -- extensions/agi/bin/send.py` prints 0 paths (never git rm).

## TESTS
DG2 replica of box 2005 + send.py still live today, then DG3 MOVE. Neighbourhood: leaf falsifier 1+2. No live-tree write this mint.

## FILE SCOPE
this node. No send.py move. No flock. No box edit. No implement this seat.

## CEILING
0 production lines · 0 USD · DG2 experiment · no kids · no push
