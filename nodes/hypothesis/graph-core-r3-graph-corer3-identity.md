---
confidence: 0.5
id: "hyp:graph-core-r3"
mint_id: 32d35fb88dda4a7aadef91eb1c780d26
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R3
testable_claim: Identity Scheme
title: "graph-core/R3: Identity Scheme"
type: hypothesis
---

**Description:** Node ids follow a stable, human-legible scheme that is compact enough to render in ASCII frames.

**Acceptance Criteria:**
- [ ] Each id matches the pattern `<type-prefix>:<short-slug>` where `short-slug` is kebab-case of two to five words
- [ ] When two nodes would otherwise collide, the second receives a `:n` numeric suffix starting at `:2`
- [ ] Ids exceeding 40 characters trigger a non-fatal warning but are still accepted
- [ ] Ids are stable across rebuilds: regenerating the graph from the same source files produces the same ids
