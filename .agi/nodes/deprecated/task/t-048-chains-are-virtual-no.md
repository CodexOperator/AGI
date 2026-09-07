---
id: task:t-048
mint_id: 7829db7186554f59a1461375bb135fcd
type: task
parents:
  - hyp:chain-engine-r2
acceptance_criteria:
  - R2.1 (no chain object written to disk during normal operation)
  - R2.2 (adding node that completes new chain → queryable without rebuild)
  - R2.3 (removing node that participated in chain → chain disappears next traversal)
  - R2.4 (chain query result independent of earlier queries in same session)
blocked_by:
  - task:t-047
cavekit_req: chain-engine/R2
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
title: "T-048: Chains are virtual (no on-disk chain objects)"
---
**Description:** Audit code path: ensure `find_chains` is pure over the live graph, never persists. Add tests for the four criteria.

**Files:** `agi-tree/src/chain_engine/chains.py`, `agi-tree/tests/chain_engine/test_virtual.py`

**Test Strategy:** Run query, mutate graph, run again; assert difference. Audit that no file in `context/.cache/chains/` is created during a query.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R2` under `hyp:chain-engine-r2`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r2-by-citation` citing `build:src-chain-engine-chains`, `build:tests-chain-engine-test-chain-definition`: `chains.py` derives chains from the parent edges at query time -- no chain object on disk -- and `test_chain_definition.py` is its suite.
<!-- THOUGHT:END -->