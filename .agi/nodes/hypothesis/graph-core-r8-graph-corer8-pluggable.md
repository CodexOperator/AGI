---
confidence: 0.5
id: "hyp:graph-core-r8"
mint_id: 9087f46fdca145ddbb2b6684ff5da2d2
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R8
testable_claim: Pluggable Persistence Layer
title: "graph-core/R8: Pluggable Persistence Layer"
type: hypothesis
---

**Description:** The default persistence backend is the filesystem. The graph-core exposes a backend contract so alternative backends (such as in-process databases) can be added without changing callers.

**Acceptance Criteria:**
- [ ] A backend implements a documented set of operations (load, save, list, watch) and graph-core depends only on that contract
- [ ] Swapping the file backend for a stub in-memory backend in tests changes no caller code
- [ ] The default install requires no external database, daemon, or network service to function
- [ ] A backend choice is selectable through configuration without code edits
