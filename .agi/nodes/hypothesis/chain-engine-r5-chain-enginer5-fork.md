---
confidence: 0.5
id: "hyp:chain-engine-r5"
mint_id: 8ed56b9dad18436bb868b40d4d5aa620
origin: build-site
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R5
testable_claim: Fork Mechanics
title: "chain-engine/R5: Fork Mechanics"
type: hypothesis
---

**Description:** Any node may have multiple children of the same type, allowing arbitrary forks.

**Acceptance Criteria:**
- [ ] Adding a second child of the same type to an existing parent does not raise an error
- [ ] After a fork, both child branches appear as candidates in subsequent chain queries
- [ ] Fork count per parent is reported in chain statistics
- [ ] Forks compound: a forked branch may itself fork without special handling
