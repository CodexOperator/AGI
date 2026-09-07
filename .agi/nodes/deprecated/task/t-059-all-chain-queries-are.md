---
id: task:t-059
mint_id: e6d9ffe1a7344a7689cf6e4cbe9de3b5
type: task
parents:
  - hyp:chain-engine-r9
acceptance_criteria:
  - R9.4 (all chain queries read-only
  - never mutate the graph)
blocked_by:
  - task:t-056
  - task:t-057
  - task:t-058
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
title: "T-059: All chain queries are read-only"
---
**Description:** Wrap each query call site in a guard that snapshots the graph before and asserts equality after. Add a test asserting graph equality before/after each query.

**Files:** `agi-tree/tests/chain_engine/test_query_purity.py`

**Test Strategy:** Snapshot-comparison test for each of the three queries.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R9` under `hyp:chain-engine-r9`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r9-by-citation` citing `build:src-chain-engine-queries`: `queries.py` has `longest_n`, `branching_factor` and `mid_chain_candidates` by name, plus `all_chain_queries_pure`.
<!-- THOUGHT:END -->