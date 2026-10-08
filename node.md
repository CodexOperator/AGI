---
id: task:t-058
mint_id: 1c286c886c784be9befcfb940bdb83b6
type: task
parents:
  - hyp:chain-engine-r9
acceptance_criteria:
  - R9.3 (mid_chain_candidates accepts min chain length and max recency
  - returns join targets matching both)
blocked_by:
  - task:t-050
cavekit_req: chain-engine/R9
edited_by: season.py
effort: S
origin: build-site
season: 1
status: deprecated
tags:
  - S
  - tier--1
thought_session: season
tier: -1
title: "T-058: mid_chain_candidates query"
---
**Description:** Implement `mid_chain_candidates(graph, min_length, max_recency)` returning a list of `(node_id, chain, position)` triples meeting both filters.

**Files:** `agi-tree/src/chain_engine/queries.py`, `agi-tree/tests/chain_engine/test_query_mid_chain.py`

**Test Strategy:** Fixture with chains of varying length and recency; assert filter intersection is correct.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R9` under `hyp:chain-engine-r9`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r9-by-citation` citing `build:src-chain-engine-queries`: `queries.py` has `longest_n`, `branching_factor` and `mid_chain_candidates` by name, plus `all_chain_queries_pure`.
<!-- THOUGHT:END -->