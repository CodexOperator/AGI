---
confidence: 0.5
id: "hyp:chain-engine-r3"
mint_id: 1848c9bfda8849f7b34ae8bf7dd68f4d
origin: build-site
parents:
  - idea:domain-chain-engine
subgraph: false
tags:
  - chain-engine
  - R3
testable_claim: Longest-Chain Attractor
title: "chain-engine/R3: Longest-Chain Attractor"
type: hypothesis
---

**Description:** Among current chains, longer chains are preferred but not exclusive. Attractiveness is a weighted score and short chains may still be selected if their score is competitive.

**Acceptance Criteria:**
- [ ] When asked to rank chains, the engine returns them sorted by attractiveness with ties broken deterministically
- [ ] The longest chain is among the top-ranked results when no other factor dominates
- [ ] Short chains can rank above longer chains when their non-length scores are sufficiently higher
- [ ] The ranking function is pure: equal inputs produce equal outputs across runs
