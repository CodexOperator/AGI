---
confidence: 0.5
id: "hyp:environment-indexers-r7"
mint_id: e77e9c58204d409aa004a835a536a31f
origin: build-site
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R7
testable_claim: One-File-Per-Indexer Layout
title: "environment-indexers/R7: One-File-Per-Indexer Layout"
type: hypothesis
---

**Description:** Each indexer is a single self-contained file with documented internals and registers or references at least one schema.

**Acceptance Criteria:**
- [ ] Each indexer lives in its own file under the indexers directory
- [ ] Each indexer either registers a new schema with the schema-registry or references an existing built-in schema
- [ ] Each indexer file documents its inputs, outputs, and known limitations in a header comment block
- [ ] Removing an indexer file removes only that indexer's command without affecting others

**Dependencies:** schema-registry (R1, R8)
