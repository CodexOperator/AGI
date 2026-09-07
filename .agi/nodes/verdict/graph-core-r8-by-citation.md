---
id: verdict:graph-core-r8-by-citation
mint_id: 696f1517daec44eaab39c6b3f4c5c6e9
type: verdict
parents:
  - hyp:graph-core-r8
next_edges: []
confidence: 0.8
edited_by: season.py
evidence_runs:
  - build:src-graph-core-persistence-backend
  - build:src-graph-core-persistence-filesystem
  - build:src-graph-core-persistence-in-memory
  - build:src-graph-core-persistence-sqlite-backend
  - build:tests-graph-core-test-backend-swap
scaffold_hash: 0a3d01f2ebe3ca6b
season: 1
supports:
  - hyp:graph-core-r8
tags:
  - graph-core
  - R8
  - l1.09
  - by-citation
thought_session: season
title: "graph-core/R8: closed by citation"
verdict: inconclusive_lean_proved:80
---
# verdict:graph-core-r8-by-citation

## Verdict

`inconclusive_lean_proved:80` — **closed by citation, not by a run** (L1.09, 2026-09-03).

## Evidence

`hyp:graph-core-r8` — *Pluggable Persistence Layer* — was specified by the cavekit build-site and never reached a verdict there. The real, non-build-site tree already carries what it asked for:

- `build:src-graph-core-persistence-backend` → `extensions/agi/src/graph_core/persistence/backend.py`
- `build:src-graph-core-persistence-filesystem` → `extensions/agi/src/graph_core/persistence/filesystem.py`
- `build:src-graph-core-persistence-in-memory` → `extensions/agi/src/graph_core/persistence/in_memory.py`
- `build:src-graph-core-persistence-sqlite-backend` → `extensions/agi/src/graph_core/persistence/sqlite_backend.py`
- `build:tests-graph-core-test-backend-swap` → `extensions/agi/tests/graph_core/test_backend_swap.py`

Grounds: `persistence/backend.py` is the protocol, with filesystem, in-memory and sqlite implementations, and `test_backend_swap.py` swaps them under one graph.

Survey: `.agi/sessions/L1.09-mining/report.md` §C. Nothing was executed for this verdict; the suites named above are the ones `commands.py run tests` already runs.

## Confidence

0.8 — the citations are real files with real test suites, but this verdict cites them rather than running them, which is why it is `inconclusive_lean_proved:80` and not `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written 2026-09-03 in L1.09 to close `hyp:graph-core-r8` by citation per the build-site survey (§C); the hypothesis is deprecated in the same pass with its `origin: build-site` cohort (goal:s18), and this verdict is the live record of where its claim is actually satisfied.
<!-- THOUGHT:END -->