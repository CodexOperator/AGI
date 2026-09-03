---
id: task:t-057
mint_id: 1a19457b9c034e79bb442638ba5415cd
type: task
parents:
  - hyp:chain-engine-r9
acceptance_criteria:
  - R9.2 (branching_factor returns avg + per-node count of out-edges across chain participants)
blocked_by:
  - task:t-051
cavekit_req: chain-engine/R9
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-057: branching_factor query"
---
**Description:** Implement `branching_factor(graph)` returning `{avg: float, per_node: {id: count}}`.

**Files:** `agi-tree/src/chain_engine/queries.py`, `agi-tree/tests/chain_engine/test_query_branching.py`

**Test Strategy:** Fixture chain participants with known fork counts; assert avg and per-node values.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R9` under `hyp:chain-engine-r9`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r9-by-citation` citing `build:src-chain-engine-queries`: `queries.py` has `longest_n`, `branching_factor` and `mid_chain_candidates` by name, plus `all_chain_queries_pure`.
<!-- THOUGHT:END -->
