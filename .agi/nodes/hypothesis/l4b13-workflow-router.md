---
id: hypothesis:l4b13-workflow-router
mint_id: 9c6cf3ef5c1e4ea7abb88327ae5b8076
type: hypothesis
parents:
  - idea:l4b13-workflow-router
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: 9bef96f39da1250a
season: 2
tags:
  - hypothesis
testable_claim: workflow.py exposes ONE router that every workflow dispatches through -- the parent/kid loop, brief drafting, round review, and any future Master workflow -- and a workflow started the Claude Code way still lands a row in graph workflow-tracking; provable by one workflow of each kind showing up in the same tracked-workflow log (owner, l4-plan A:320).
thought_session: sanctuary-helper-05
title: A single workflow router dispatches every workflow
---
<!-- BODY:BEGIN -->
# hypothesis:l4b13-workflow-router

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?