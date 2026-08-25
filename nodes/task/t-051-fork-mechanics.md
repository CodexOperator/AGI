---
acceptance_criteria:
  - R5.1 (adding second child of same type to existing parent does not raise)
  - R5.2 (after fork
  - both branches appear as candidates in chain queries)
  - R5.3 (fork count per parent reported in chain stats)
  - R5.4 (forks compound: forked branch may itself fork without special handling)
blocked_by:
  - task:t-047
cavekit_req: chain-engine/R5
effort: M
id: "task:t-051"
mint_id: ddfc743d51844f0882e32e0c8a4ab19c
origin: build-site
parents:
  - hyp:chain-engine-r5
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-051: Fork mechanics"
type: task
---

**Description:** Document and verify that the graph allows multiple children of the same type. Implement `fork_count(graph, node_id)` returning the number of out-edges to children of the same type. `chain_stats(graph)` returns a dict including `fork_counts`.

**Files:** `agi-tree/src/chain_engine/forks.py`, `agi-tree/src/chain_engine/stats.py`, `agi-tree/tests/chain_engine/test_forks.py`

**Test Strategy:** Graph with one node having two `hypothesis` children; assert chain query returns both. Stats reports fork_count=2. Compound test: fork the fork, assert deeper chains all returned.
