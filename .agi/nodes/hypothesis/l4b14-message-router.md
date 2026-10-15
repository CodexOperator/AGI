---
id: hypothesis:l4b14-message-router
mint_id: 79776bf616c74011a4ea986d1d37a393
type: hypothesis
parents:
  - idea:l4b14-message-router
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: 5078dc2ea05591fd
season: 2
tags:
  - hypothesis
testable_claim: send.py resolves a send/session-send targeting a seat running on pi through ONE message router that translates it into that harness's message format automatically -- the sender never learns which harness answered; provable by sending to a pi-seat target and a CC-seat target through the same call and getting each delivered in its native format with no branch in the caller (owner, l4-plan A:322).
thought_session: sanctuary-helper-05
title: A single message router translates a seat-addressed send invisibly
---
<!-- BODY:BEGIN -->
# hypothesis:l4b14-message-router

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
