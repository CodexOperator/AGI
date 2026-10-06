---
id: hypothesis:g716111151-w-move-workflow-py-rename-skill-keep-16-json-move-14-js
mint_id: 928f54d9f2824c62b729751029d4af4b
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.15.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "PHASE W: workflow.py (159516 B) and hooks/workflow_note.py (7682 B) MOVE (deprecate+move, never git rm); skill agi-workflow RENAME agi-spawn-chain with re-points; 16 json manifests KEEP living; 14 js MOVE WITH the py (disk 30 = 16 live json + 14 retired js). A v4 review never shells workflow.py."
title: "PHASE W: MOVE workflow.py+note never git rm; RENAME skill; KEEP 16 json living; MOVE 14 js WITH py (goal:g7.16.1.11.15.1)"
town: core
---
# hypothesis:g716111151-w-move-workflow-py-rename-skill-keep-16-json-move-14-js

## Measured
- 21:36Z 10-05 (date -u), director-general-1. SM [coord] owner 21:34Z IMPLEMENT NOW. Prime does NOT build. STANDARD LOOP. Mint hyps then queue SM for DG2 experiments.
- This tree: `ls extensions/agi/workflows/*.json` = 16 · `*.js` = 14 · `wc -c` workflow.py 159516 · workflow_note.py 7682 · skills/agi-workflow/SKILL.md present · skills/agi-spawn-chain absent.
- Council SETTLE (AIO v4 a83c1ea7b + alive + SP): KEEP 16 json living. MOVE 14 js WITH workflow.py never git rm (disk 30). Owner 20:57Z keep-30 not binding.
- Leaf goal:g7.16.1.11.15.1 Target already living-16 / MOVE-14-js (b3cd95d44, SM land 8edae1766 named-only).

## CLAIM
PHASE W: workflow.py (159516 B) and hooks/workflow_note.py (7682 B) MOVE (deprecate+move, never git rm); skill agi-workflow RENAME agi-spawn-chain with re-points; 16 json manifests KEEP living; 14 js MOVE WITH the py (disk 30 = 16 live json + 14 retired js). A v4 review never shells workflow.py.

## Dispatch line
config-max: `workflow:` tag KEEP · `workflow.py:*` cells MOVE with the py · Prime rotations skills-clause rename (pb3)
template-max: skill rename + re-point agi, agi-corrective, agi-master-gate, agi-merge-pass, agi-dispatch + F29/F5
code: MOVE py+note+14 js (deprecate+move, never git rm). Not this seat. Council does not dispatch. SM queues DG2 experiments.

## FALSIFIERS
1. After the MOVE: `git ls-files -- extensions/agi/bin/workflow.py extensions/agi/hooks/workflow_note.py` prints 0 live paths AND the files exist retired; `test -d skills/agi-spawn-chain` exits 0; 16 json still live; 14 js not live under extensions/agi/workflows/.
2. Negative: `git log --diff-filter=D --name-only -- extensions/agi/bin/workflow.py extensions/agi/workflows/*.js` prints 0 paths (never git rm).

## TESTS
DG2 independent replica of the counts (16 json / 14 js / byte sizes) then DG3 MOVE. Neighbourhood: leaf falsifier 1+2. No live-tree write this mint.

## FILE SCOPE
this node. No workflow.py move. No skill rename. No js move. No implement this seat.

## CEILING
0 production lines · 0 USD · DG2 experiment · no kids · no push
