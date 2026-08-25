---
acceptance_criteria:
  - R1.1 (chain = ordered sequence of node ids whose types appear in documented order)
  - R1.2 (multiple consecutive hypothesis or experiment nodes between idea and verdict allowed)
  - R1.3 (path skipping a required type → not a chain)
  - R1.4 (two chains may share any prefix; not deduplicated)
blocked_by:
  - task:t-031
  - task:t-004
cavekit_req: chain-engine/R1
effort: M
id: "task:t-047"
mint_id: b219a3919809438cb6b881ce89754bb9
origin: build-site
parents:
  - hyp:chain-engine-r1
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-047: Chain definition and ordered-type traversal"
type: task
---

**Description:** Define `Chain` as `list[str]` (node ids). Implement `find_chains(graph)` that traverses from idea nodes following `next` edges, collecting paths whose type sequence matches the regex `idea hypothesis+ experiment+ verdict mvp outcome bigger_outcome app_purpose`. Multiple-of-same-type consecutive runs allowed. Skipping any required type → path is rejected. Shared prefixes preserved as separate chains.

**Files:** `agi-tree/src/chain_engine/chains.py`, `agi-tree/src/chain_engine/types.py`, `agi-tree/tests/chain_engine/test_chain_definition.py`

**Test Strategy:** Fixture graphs covering each criterion: one full chain, one with two hypotheses, one missing experiment (rejected), and a graph with shared prefix yielding two chains.
