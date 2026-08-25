---
confidence: 0.5
id: "hyp:graph-core-r10"
mint_id: 3721a5b0b1ad481888ad4e54c3864a1f
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R10
testable_claim: Bootstrap Command
title: "graph-core/R10: Bootstrap Command"
type: hypothesis
---

**Description:** A command initializes a new project so a fresh directory becomes a valid graph root.

**Acceptance Criteria:**
- [ ] Running the bootstrap command in an empty directory produces a `context/` skeleton with subdirectories for schemas, kits, and node storage
- [ ] Running the bootstrap command twice on the same directory is a no-op and does not overwrite existing files
- [ ] The skeleton includes a minimal example node and a minimal example schema sufficient to load a one-node graph
- [ ] The bootstrap reports the created paths to the user in a single summary
