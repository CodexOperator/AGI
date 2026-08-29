---
confidence: 0.5
id: "hyp:graph-core-r6"
mint_id: 59fdb7a61fb648409a283dcfe7ca0072
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R6
testable_claim: Directory-Walking Auto-Discovery
title: "graph-core/R6: Directory-Walking Auto-Discovery"
type: hypothesis
---

**Description:** A directory of node files is loaded by walking the filesystem. A folder is a subgraph; files inside are nodes; folder names map to node types via the schema-registry.

**Acceptance Criteria:**
- [ ] Pointing the loader at any directory yields a graph whose nodes correspond to the files under that directory
- [ ] A subdirectory is loaded as a subgraph node whose type is resolved through the schema-registry
- [ ] Files that do not match any known schema are loaded as generic nodes and a warning is emitted listing them
- [ ] Walking is deterministic: two runs against the same directory produce the same node set and id order

**Dependencies:** schema-registry (for folder-name → node-type resolution)
