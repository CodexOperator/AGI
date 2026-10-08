---
id: hyp:graph-core-r8
mint_id: 9087f46fdca145ddbb2b6684ff5da2d2
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - graph-core
  - R8
testable_claim: Pluggable Persistence Layer
thought_session: season
title: "graph-core/R8: Pluggable Persistence Layer"
---
**Description:** The default persistence backend is the filesystem. The graph-core exposes a backend contract so alternative backends (such as in-process databases) can be added without changing callers.

**Acceptance Criteria:**
- [ ] A backend implements a documented set of operations (load, save, list, watch) and graph-core depends only on that contract
- [ ] Swapping the file backend for a stub in-memory backend in tests changes no caller code
- [ ] The default install requires no external database, daemon, or network service to function
- [ ] A backend choice is selectable through configuration without code edits

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r8-by-citation` citing `build:src-graph-core-persistence-backend`, `build:src-graph-core-persistence-filesystem`, `build:src-graph-core-persistence-in-memory`, `build:src-graph-core-persistence-sqlite-backend`, `build:tests-graph-core-test-backend-swap`: `persistence/backend.py` is the protocol, with filesystem, in-memory and sqlite implementations, and `test_backend_swap.py` swaps them under one graph.
<!-- THOUGHT:END -->