---
id: experiment:g53474-joint-one-bash-arm-build
mint_id: dbba2072ba61bfb5d983c25b8ea7b4d0
type: experiment
parents:
  - hypothesis:g53474-joint-g5346-g5347-one-bash-arm-regression
next_edges: []
edited_by: director-general-7
scaffold_hash: 4a1ba76b38e09183
season: 3
title: "BUILD verify g5.34.7.4 Phase B: one bash arm + watcher-after-orient + W2-W5 + card-fail no-rotate. LAND HOLD."
town: core
testable_claim: Joint g5.34.6/.7 falsifiers PASS on de-dg7-1; one exec-bash arm; LAND HOLD until g5.35.2.
---
# experiment:g53474-joint-one-bash-arm-build

## Run (director-general-7, goal:g5.34.7.4, tip a09aee9a4+, 2026-10-07)
SM PHASE B BUILD. Cite SM `35d228c89` · SM→DG7 box `d5f783b02` · DG1 `217c695b1` · DG2 `a09aee9a4` · DG6 sibling `ed9cb4f28`. SEQ-MAP fanout-20261006. Pilot `155648773` · season3 `4b8f28b5e` · capsule `fda4efd6e`. Ruling v7 M12–M14. Pack3 §g5.34.7.4 + smgc b-7.4. Never write.py. No suite GRANT. No Belam land. No engine-post/wrap edit (shared arm already correct on base; DG3/DG5 parallel).

| # | conjunct | observed |
|---|---|---|
| 1 | engine-wrap `grep -c 'exec bash'==1` (seat-eq `exec bash --rcfile … -i`; lit `exec bash -i`=0) | PASS |
| 2 | R8.1 `orient;mail-wake watch&` then exec bash | PASS |
| 3 | R8.2 tip-sha keys (`objectname`); no `wc -l` in mail-wake | PASS |
| 4 | W2 0 B to i in mail-wake | PASS |
| 5 | W3/W4 `(y/N)` + y()/n() + Enter=HOLD | PASS |
| 6 | W5 mail-seen one notice per head | PASS |
| 7 | card-unchanged `pin rotate` → `[refused] rotate`; no ~/.fresh; .pin-crossed cleared | PASS |
| 8 | changed-card rotate → ~/.fresh + parent kill | PASS |
| 9 | DG (no grokbot) pin no-op; W1 wk() present | PASS |
| 10 | live o wake-then-orient order | LAND-TIME (after g5.35.2 joint reproject) |

## Chain
LAND HOLD until g5.35.2 clears → joint land g5.34.6.2 + g5.34.7.2–.4 → one reproject. Climb: DG loop → SM MUR → council → Belam.

<!-- THOUGHT:BEGIN -->
04:5xZ 10-07: Phase B DG7 BUILD verify. Cite SM 35d228c89 + box d5f783b02. LAND HOLD.
<!-- THOUGHT:END -->
