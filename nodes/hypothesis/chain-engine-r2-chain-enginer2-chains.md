---
confidence: 0.5
id: "hyp:chain-engine-r2"
mint_id: ea55e55622604a4999ea9e10da3c447e
origin: build-site
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R2
testable_claim: Chains Are Virtual
title: "chain-engine/R2: Chains Are Virtual"
type: hypothesis
---

**Description:** Chains are computed by traversing the graph; they are not stored as separate persistent records.

**Acceptance Criteria:**
- [ ] No chain object is written to disk as part of normal operation
- [ ] Adding a node that completes a new chain makes that chain queryable without a graph rebuild
- [ ] Removing a node that participated in a chain makes that chain disappear from queries on next traversal
- [ ] A chain query produces the same result whether or not earlier chain queries were run in the same session
