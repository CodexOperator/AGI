---
confidence: 0.5
id: "hyp:environment-indexers-r1"
mint_id: 9d942ac4bc864f4b8d15141672a75741
next_edges:
  - exp:environment-indexers-r1
origin: build-site
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R1
testable_claim: Indexer Invocation Command
title: "environment-indexers/R1: Indexer Invocation Command"
type: hypothesis
---

**Description:** A single command runs a chosen indexer over a chosen path and writes results into the graph.

**Acceptance Criteria:**
- [ ] The command accepts a target path and an indexer name and runs only that indexer
- [ ] Listing available indexers without invoking one produces a summary with each indexer's name and one-line description
- [ ] An unknown indexer name returns a structured error and does not run anything
- [ ] The command exits with a non-zero status when the indexer reports any failure that prevented node emission

**Dependencies:** graph-core (R10 bootstrap), schema-registry (R1 schema-as-file)
