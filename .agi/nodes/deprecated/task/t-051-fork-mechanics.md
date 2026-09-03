---
id: task:t-051
mint_id: ddfc743d51844f0882e32e0c8a4ab19c
type: task
parents:
  - hyp:chain-engine-r5
acceptance_criteria:
  - R5.1 (adding second child of same type to existing parent does not raise)
  - R5.2 (after fork
  - both branches appear as candidates in chain queries)
  - R5.3 (fork count per parent reported in chain stats)
  - {"R5.4 (forks compound": "forked branch may itself fork without special handling)"}
blocked_by:
  - task:t-047
cavekit_req: chain-engine/R5
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-051: Fork mechanics"
---
**Description:** Document and verify that the graph allows multiple children of the same type. Implement `fork_count(graph, node_id)` returning the number of out-edges to children of the same type. `chain_stats(graph)` returns a dict including `fork_counts`.

**Files:** `agi-tree/src/chain_engine/forks.py`, `agi-tree/src/chain_engine/stats.py`, `agi-tree/tests/chain_engine/test_forks.py`

**Test Strategy:** Graph with one node having two `hypothesis` children; assert chain query returns both. Stats reports fork_count=2. Compound test: fork the fork, assert deeper chains all returned.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R5` under `hyp:chain-engine-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r5-by-citation` citing `build:src-chain-engine-queries`, `build:tests-chain-engine-test-chain-definition`: `test_fork_after_hypothesis` (in `test_chain_definition.py`) is the real fork test, and `queries.py::branching_factor`'s `per_node` dict realises the per-parent fork count under a different name.
<!-- THOUGHT:END -->
