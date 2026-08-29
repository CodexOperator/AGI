---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r4"
mint_id: 8df1769734894bf3849894b691314916
origin: build-site
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R4
testable_claim: Per-Agent Briefing Payload
title: "autoresearch-tree-skill/R4: Per-Agent Briefing Payload"
type: hypothesis
---

**Description:** Each builder agent receives a briefing that contains the current chain statistics, the attractiveness scores for candidate chains, and the menu of available actions (extend, fork, hop, fresh start).

**Acceptance Criteria:**
- [ ] The briefing names the current set of chains under consideration with their length, depth, recency, and mvp count
- [ ] The briefing names each candidate chain's attractiveness score from the chain-engine
- [ ] The briefing lists the available actions per chain (extend at tail, fork at named node, hop to a mid-chain candidate, start fresh)
- [ ] The briefing is generated from chain-engine queries only and does not include implementation details of the engine

**Dependencies:** chain-engine (R3, R4, R6, R9)
