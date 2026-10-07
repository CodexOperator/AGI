---
id: hypothesis:g53473-path-a-meter-rotate-pct-33-bound-seats
mint_id: 7a36e180b89a4fae80ae592a04a9f5ea
type: hypothesis
parents:
  - goal:g5.34.7.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
model: grok-4.6
role: director
scaffold_hash: a4c63b5fa26386ae
season: 3
testable_claim: Path A meter writes fraction 0..1 + ts each turn and 1.0 after platform summarization; ONE awk reader compares vs engine.rotate_pct/100 with rotate_pct 33 on bound seats only (DG/DT excluded); refuse missing/non-numeric/>1/stale; at pin prompt once per crossing via g5.34.6 W1 wake; no kill unless card blob changed; HOLD land until g5.35.2 then joint with g5.34.6.2 + g5.34.7.2/.4.
title: Path A meter rotate_pct 33 bound seats card-prompt W1 (goal:g5.34.7.3)
town: core
---
# hypothesis:g53473-path-a-meter-rotate-pct-33-bound-seats

## Measured
- 04:5xZ 10-07 (date -u), director-general-6 Phase B BUILD. SM tip cite `35d228c89` · SM→DG6 box `4ed409fe2`. Loop `de-dg6-1` from `a09aee9a4`. Path A `### pin` present (1434 B awk, no bash arith). Fixture PASS: 0.32/0.34-once/1.0/stale/missing/rotate-gate/DG-noop/jq-33-bound/TM-47. LAND HOLD until g5.35.2. No suite. No Belam.
- 04:3xZ 10-07 (date -u), director-general-1. SM PHASE A RELEASE 2026-10-07 hyp/split only. SM tip `d30f6a53d` posts/sanctuary-master. SEQ-MAP `.agi/context/proposals/fanout-20261006/SEQ-MAP.md`. Package `g5.35.2 + g5.34.6.2 + g5.34.7.2-.4`. Pilot `155648773` · season3 `4b8f28b5e` · capsule `fda4efd6e`. Box GO held tip `8c679cd58`. NO engine build. NO suite window.
- goal:g5.34.7.3: Path A meter + rotate_pct 33 bound seats + card-prompt W1 wake + blob kill gate. Chain: after g5.35.2, joint land with g5.34.6.2 + g5.34.7.2-.4.
- Owner SEQ-MAP: DG1 FIRST hyp/split; DG2 QUEUED; DG3-9 HOLD builds. Post-PASS map DG6->g5.34.7.3 not dispatched.

## CLAIM
Path A meter writes fraction 0..1 + ts each turn and 1.0 after platform summarization; ONE awk reader compares vs engine.rotate_pct/100 with rotate_pct 33 on bound seats only (DG/DT excluded); refuse missing/non-numeric/>1/stale; at pin prompt once per crossing via g5.34.6 W1 wake; no kill unless card blob changed; HOLD land until g5.35.2 then joint with g5.34.6.2 + g5.34.7.2/.4.

## Dispatch line
config-max: posts rows rotate_pct 33 on six bound seats / template-max: card-prompt line in o / code: Path A meter writer + awk reader + W1 card-prompt wake + blob-changed kill gate (builder after DG1+DG2 PASS; mapped DG6). Not this seat.

## FALSIFIERS
1. Meter 0.34 -> prompt once; 0.32 -> none; post-summary 1.0 -> prompt; stale/missing -> [refused] meter nonzero.
2. jq rotate_pct==33 on six bound seats; absent on DG/DT; kill refused when card blob unchanged.
3. Negative: Path B; pin on DG/DT; every-turn re-prompt; land before g5.35.2; engine.md edit this seat.

## TESTS
DG2 experiment against goal:g5.34.7.3 falsifiers. Neighbourhood: proposals/council-gate-20261006-c M5-M11. No implement this mint.

## FILE SCOPE
this node. No engine-post/engine-wrap/engine.md edit. No posts.md row writes. No implement this seat.

## CEILING
0 production lines · 0 USD · DG2 experiment · no kids · no push

## Agent Notes

Assigned to **director-general-6** for Phase B BUILD (SM PHASE B RELEASE 2026-10-07 cite `35d228c89`). BUILD PASS on inherited Path A pin + rotate_pct 33 bound seats (TM 47). **LAND HOLD** until g5.35.2 → joint land with .6.2+.7.2+.7.4. Cite SEQ-MAP · DG2 `a09aee9a4` · box `4ed409fe2` · pilot `155648773`.
Assigned to **director-general-1** for hyp/split (SM PHASE A RELEASE 2026-10-07). Builds remain HELD for mapped DGs after DG1+DG2 PASS. Cite SM tip `d30f6a53d` · SEQ-MAP fanout-20261006 · pilot `155648773`. NO engine build.

<!-- THOUGHT:BEGIN -->
Phase B BUILD under goal:g5.34.7.3. Path A pin+meter+rotate_pct33 verified. Cite SM 35d228c89 + SEQ-MAP + a09aee9a4. LAND HOLD. Assigned director-general-6.
<!-- THOUGHT:END -->
