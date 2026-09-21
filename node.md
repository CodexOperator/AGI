---
id: hypothesis:l3w4-quorum-request-path
mint_id: edef0b67d5f44140975ad680cd468d5e
type: hypothesis
parents:
  - goal:g17
next_edges: []
scaffold_hash: 67f7abd006829ca4
season: 2
testable_claim: After the change, send.py audience quorum --reason TEXT posts an [ask]-tagged message into room quorum-requests from any caller, and send.py report --room quorum-requests --ref TS TEXT posts the ruling into the same thread but only succeeds when the caller is a tier-3 parent (AGI_ROLE=parent, AGI_LADDER_TIER=3); a non-quorum caller attempting the report half is refused. Proved by tests exercising both the ask and the gated report, plus a full green suite.
title: A non-quorum caller can request a quorum ruling without entering the quorum room
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-quorum-request-path

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

