---
confidence: 1.0
id: "idea:domain-chain-engine"
mint_id: 60dfa5469cb1476cbc740e5957f16f7f
next_edges:
  - hyp:chain-engine-r1
origin: build-site
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: chain-engine"
type: idea
---

The autoresearch-specific layer that sits on top of graph-core. It defines what a chain is, how chains are scored and selected, how agents join, fork, or hop between them, and what verdicts look like. It contains all the autoresearch semantics so graph-core can remain a generic substrate. Chains are virtual: they are computed from the underlying graph rather than stored as separate first-class objects.
