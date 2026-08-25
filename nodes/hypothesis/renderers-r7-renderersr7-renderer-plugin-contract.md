---
confidence: 0.5
id: "hyp:renderers-r7"
mint_id: ebbe1f1f33ef451c868a9be4154936d1
origin: build-site
parents:
  - idea:domain-renderers
subgraph: false
tags:
  - renderers
  - R7
testable_claim: Renderer Plugin Contract
title: "renderers/R7: Renderer Plugin Contract"
type: hypothesis
---

**Description:** Adding a new renderer is one new class that implements a single method taking the shared representation and returning a string.

**Acceptance Criteria:**
- [ ] The renderer interface declares exactly one required method that accepts the shared representation and returns a string
- [ ] A new renderer implementation is loadable without modifying existing renderers
- [ ] An invalid renderer (raises during render or returns a non-string) is reported with a structured error and does not affect other renderers
- [ ] A self-test command runs every registered renderer over a fixture graph and reports pass or fail per renderer
