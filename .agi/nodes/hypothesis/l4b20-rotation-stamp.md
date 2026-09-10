---
id: hypothesis:l4b20-rotation-stamp
mint_id: 533cfef888854584b16bed5ad1e4eec3
type: hypothesis
parents:
  - idea:l4b20-rotation-stamp
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: b42cbb9a6b0616a3
season: 2
tags:
  - hypothesis
testable_claim: rotate.py rotate-self and the loop driver write the rotation record and the generation stamp in a SINGLE write call -- one writer per fact, not two -- so a rotation never leaves one of the pair stamped and the other stale; provable by one rotation producing both facts with matching timestamps from one call site, with telemetry landing at goal:g16 (owner, l4-plan A:166, A:55).
thought_session: sanctuary-helper-05
title: rotate-self and loop write the rotation record and generation stamp together
---
<!-- BODY:BEGIN -->
# hypothesis:l4b20-rotation-stamp

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
