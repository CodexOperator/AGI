---
id: task:t-047
mint_id: b219a3919809438cb6b881ce89754bb9
type: task
parents:
  - hyp:chain-engine-r1
acceptance_criteria:
  - R1.1 (chain = ordered sequence of node ids whose types appear in documented order)
  - R1.2 (multiple consecutive hypothesis or experiment nodes between idea and verdict allowed)
  - R1.3 (path skipping a required type → not a chain)
  - R1.4 (two chains may share any prefix; not deduplicated)
blocked_by:
  - task:t-031
  - task:t-004
cavekit_req: chain-engine/R1
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-047: Chain definition and ordered-type traversal"
---
**Description:** Define `Chain` as `list[str]` (node ids). Implement `find_chains(graph)` that traverses from idea nodes following `next` edges, collecting paths whose type sequence matches the regex `idea hypothesis+ experiment+ verdict mvp outcome bigger_outcome app_purpose`. Multiple-of-same-type consecutive runs allowed. Skipping any required type → path is rejected. Shared prefixes preserved as separate chains.

**Files:** `agi-tree/src/chain_engine/chains.py`, `agi-tree/src/chain_engine/types.py`, `agi-tree/tests/chain_engine/test_chain_definition.py`

**Test Strategy:** Fixture graphs covering each criterion: one full chain, one with two hypotheses, one missing experiment (rejected), and a graph with shared prefix yielding two chains.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R1` under `hyp:chain-engine-r1`, whose disposition is already closed by `verdict:chain-engine-r1` before this pass; deprecated with its domain (`idea:domain-chain-engine`).
<!-- THOUGHT:END -->