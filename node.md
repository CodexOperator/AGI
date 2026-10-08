---
id: hyp:chain-engine-r2
mint_id: ea55e55622604a4999ea9e10da3c447e
type: hypothesis
parents:
  - idea:domain-chain-engine
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - chain-engine
  - R2
testable_claim: Chains Are Virtual
thought_session: season
title: "chain-engine/R2: Chains Are Virtual"
---
**Description:** Chains are computed by traversing the graph; they are not stored as separate persistent records.

**Acceptance Criteria:**
- [ ] No chain object is written to disk as part of normal operation
- [ ] Adding a node that completes a new chain makes that chain queryable without a graph rebuild
- [ ] Removing a node that participated in a chain makes that chain disappear from queries on next traversal
- [ ] A chain query produces the same result whether or not earlier chain queries were run in the same session

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r2-by-citation` citing `build:src-chain-engine-chains`, `build:tests-chain-engine-test-chain-definition`: `chains.py` derives chains from the parent edges at query time -- no chain object on disk -- and `test_chain_definition.py` is its suite.
<!-- THOUGHT:END -->