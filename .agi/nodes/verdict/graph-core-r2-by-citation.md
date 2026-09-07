---
id: verdict:graph-core-r2-by-citation
mint_id: 4fe661793128489aac05a058df8ee6d9
type: verdict
parents:
  - hyp:graph-core-r2
next_edges: []
confidence: 0.8
edited_by: season.py
evidence_runs:
  - build:src-graph-core-edge
  - build:src-graph-core-graph
  - build:tests-graph-core-test-graph-dag
  - build:tests-graph-core-test-edge
  - build:tests-graph-core-test-node-invariants
scaffold_hash: 4f5453359e19bf9b
season: 1
supports:
  - hyp:graph-core-r2
tags:
  - graph-core
  - R2
  - l1.09
  - by-citation
thought_session: season
title: "graph-core/R2: closed by citation"
verdict: inconclusive_lean_proved:80
---
# verdict:graph-core-r2-by-citation

## Verdict

`inconclusive_lean_proved:80` — **closed by citation, not by a run** (L1.09, 2026-09-03).

## Evidence

`hyp:graph-core-r2` — *Generic Edge Primitive* — was specified by the cavekit build-site and never reached a verdict there. The real, non-build-site tree already carries what it asked for:

- `build:src-graph-core-edge` → `extensions/agi/src/graph_core/edge.py`
- `build:src-graph-core-graph` → `extensions/agi/src/graph_core/graph.py`
- `build:tests-graph-core-test-graph-dag` → `extensions/agi/tests/graph_core/test_graph_dag.py`
- `build:tests-graph-core-test-edge` → `extensions/agi/tests/graph_core/test_edge.py`
- `build:tests-graph-core-test-node-invariants` → `extensions/agi/tests/graph_core/test_node_invariants.py`

Grounds: `edge.py`/`graph.py` carry `add_edge`/`remove_edge` and `_cycle_path`; the DAG, edge and node-invariant suites exercise cycle rejection, idempotent insert and no dangling references -- the same evidence pattern `verdict:graph-core-r1` was closed on (16 real test files).

Survey: `.agi/sessions/L1.09-mining/report.md` §C. Nothing was executed for this verdict; the suites named above are the ones `commands.py run tests` already runs.

## Confidence

0.8 — the citations are real files with real test suites, but this verdict cites them rather than running them, which is why it is `inconclusive_lean_proved:80` and not `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written 2026-09-03 in L1.09 to close `hyp:graph-core-r2` by citation per the build-site survey (§C); the hypothesis is deprecated in the same pass with its `origin: build-site` cohort (goal:s18), and this verdict is the live record of where its claim is actually satisfied.
<!-- THOUGHT:END -->