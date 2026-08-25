---
confidence: 0.5
id: "hyp:graph-core-r9"
mint_id: 2ca2807126e14fe6a5f208048e113f94
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R9
testable_claim: Portability Contract
title: "graph-core/R9: Portability Contract"
type: hypothesis
---

**Description:** All graph state lives inside a single project-local context directory. The graph is movable by copying that directory.

**Acceptance Criteria:**
- [ ] No node file, cache file, or configuration file references an absolute path outside the project root
- [ ] Copying the context directory to a fresh checkout reproduces the same graph on load
- [ ] The graph loads with no environment variables set beyond an optional model selector for downstream hooks
- [ ] A self-test command verifies portability by re-loading from a temporary copy and comparing node counts and ids
