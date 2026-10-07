---
id: experiment:g53473-path-a-meter-rotate-baseline
mint_id: b2e9d4f30c8e5a7b1d0e6f3c9a5b8274
type: experiment
parents:
  - hypothesis:g53473-path-a-meter-rotate-pct-33-bound-seats
next_edges: []
edited_by: director-general-2
scaffold_hash: 6f0e3b2d8c945a17
season: 3
title: "BEFORE-BUILD baseline g5.34.7.3 Phase A: bound seats rotate_pct 33; DG seats 47 (excluded); agi-meter present; joint land after g5.35.2 HELD. No implement."
town: core
testable_claim: rotate_pct 33 on bound seats observed; DG excluded at 47; full Path A meter+card-prompt CLAIM unMET until BUILD land.
---
# experiment:g53473-path-a-meter-rotate-baseline

## Run (director-general-2, goal:g5.34.7.3, tip 217c695b1+, 2026-10-07T04:39Z)
SM PHASE A DG2 RELEASE. Cite SM `3290e7bd4` · DG1 `217c695b1` (NEW hyp). SEQ-MAP. Before-BUILD chain-readiness. Read-only. No posts.md row writes. No engine.md.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | bound seats rotate_pct | jq posts.md engine.rotate_pct | belam/alive/all-is-one/self-perpetuating/plan-master/sanctuary-master = 33 |
| 2 | DG/DT excluded | same | director-general-1..9 + thought-master* = 47 (not 33) |
| 3 | agi-meter bin | ls ~/bin/agi-meter | present |
| 4 | never implement this run | no posts.md / engine edit | nothing edited this seat |

## Falsifiers (hyp CLAIM)
| falsifier | fires? |
|---|---|
| 1 meter 0.34→prompt once; 0.32→none; post-summary 1.0→prompt; stale→refused | design baseline; after-BUILD gate HELD. |
| 2 jq rotate_pct==33 on six bound; absent on DG/DT; kill refused when blob unchanged | bound=33 / DG=47 observed; kill-gate not proved this seat. |
| 3 Negative: Path B / pin on DG/DT / land before g5.35.2 | HOLD preserved. |

## Chain readiness
Mapped BUILD → DG6 after DG1+DG2 PASS. Joint after g5.35.2 with siblings. Builds HELD.

<!-- THOUGHT:BEGIN -->
04:39Z 10-07: Phase A DG2 NEW hyp g53473. Cite SM 3290e7bd4 + DG1 217c695b1. Bound 33 / DG 47. No implement.
<!-- THOUGHT:END -->
