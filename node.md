---
id: task:t-056
mint_id: 42694b1544c643fe9885a608cb5e5534
type: task
parents:
  - hyp:chain-engine-r9
acceptance_criteria:
  - R9.1 (longest_n returns top-N chains ranked by attractiveness with score and length)
blocked_by:
  - task:t-049
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
title: "T-056: longest_n chain query"
---
**Description:** Implement `longest_n(graph, n)` returning `[(chain, score, length), ...]` of size up to n.

**Files:** `agi-tree/src/chain_engine/queries.py`, `agi-tree/tests/chain_engine/test_query_longest_n.py`

**Test Strategy:** Fixture with 5 chains; longest_n(3) returns 3 ordered correctly.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R9` under `hyp:chain-engine-r9`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r9-by-citation` citing `build:src-chain-engine-queries`: `queries.py` has `longest_n`, `branching_factor` and `mid_chain_candidates` by name, plus `all_chain_queries_pure`.
<!-- THOUGHT:END -->