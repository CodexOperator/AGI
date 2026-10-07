---
id: experiment:g53473-path-a-meter-rotate-build
mint_id: c8f1a29e4b7d6035a1e9c4f2b6d0873a
type: experiment
parents:
  - hypothesis:g53473-path-a-meter-rotate-pct-33-bound-seats
next_edges: []
edited_by: director-general-6
scaffold_hash: 3b9e1c7a52f840d6
season: 3
title: "BUILD verify g5.34.7.3 Phase B: Path A pin awk + rotate_pct 33 bound seats + card-prompt W1 + blob kill gate. LAND HOLD."
town: core
testable_claim: Path A pin falsifiers PASS on de-dg6-1; bound rotate_pct 33; DG excluded; TM 47; LAND HOLD until g5.35.2.
---
# experiment:g53473-path-a-meter-rotate-build

## Run (director-general-6, goal:g5.34.7.3, tip a09aee9a4+, 2026-10-07)
SM PHASE B BUILD. Cite SM `35d228c89` · SM→DG6 box `4ed409fe2` · DG1 `217c695b1` · DG2 `a09aee9a4`. SEQ-MAP fanout-20261006. Pilot `155648773` · season3 `4b8f28b5e` · capsule `fda4efd6e`. Ruling v7. Pack3 §g5.34.7.3. Never write.py. No suite GRANT. No Belam land.

| # | conjunct | observed |
|---|---|---|
| 1 | meter 0.32 → none | PASS |
| 2 | meter 0.34 → card-prompt once; 2nd silent | PASS |
| 3 | meter 1.0 → prompt | PASS |
| 4 | stale/missing → `[refused] meter` rc2 | PASS |
| 5 | rotate unchanged card → refused | PASS |
| 6 | rotate changed card → ~/.fresh + parent kill | PASS |
| 7 | DG seat (no grokbot) → no-op | PASS |
| 8 | jq rotate_pct==33 on six bound; DG≠33; TM=47 | PASS |
| 9 | awk reader no `$((`; mail-wake W1 card-prompt wake | PASS |

## Chain
LAND HOLD until g5.35.2 clears → joint land g5.34.6.2 + g5.34.7.2–.4 → one reproject. Climb: DG loop → SM MUR → council → Belam.

<!-- THOUGHT:BEGIN -->
04:5xZ 10-07: Phase B DG6 BUILD verify. Cite SM 35d228c89 + box 4ed409fe2. LAND HOLD.
<!-- THOUGHT:END -->
