---
id: "outcome:environment-indexers-r1"
mint_id: 5c464e2b5448400ba53a43c8311138e4
next_edges:
  - bigger_outcome:environment-indexers-r1
parents:
  - mvp:environment-indexers-r1
  - verdict:environment-indexers-r1
tags:
  - environment-indexers
  - R1
title: "Outcome: environment-indexers R1"
type: outcome
---

**Outcome:** Indexer invocation command available and working.

**Input:** Target path + indexer name
**Output:** Graph nodes emitted for indexed resources
**Behavior:** Runs only the specified indexer on the specified path
**Edge cases:** Unknown indexer returns structured error, non-zero exit on failure
