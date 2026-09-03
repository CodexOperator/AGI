---
id: hyp:chain-engine-r5
mint_id: 8ed56b9dad18436bb868b40d4d5aa620
type: hypothesis
parents:
  - idea:domain-chain-engine
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - chain-engine
  - R5
testable_claim: Fork Mechanics
thought_session: L1.09
title: "chain-engine/R5: Fork Mechanics"
---
**Description:** Any node may have multiple children of the same type, allowing arbitrary forks.

**Acceptance Criteria:**
- [ ] Adding a second child of the same type to an existing parent does not raise an error
- [ ] After a fork, both child branches appear as candidates in subsequent chain queries
- [ ] Fork count per parent is reported in chain statistics
- [ ] Forks compound: a forked branch may itself fork without special handling

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r5-by-citation` citing `build:src-chain-engine-queries`, `build:tests-chain-engine-test-chain-definition`: `test_fork_after_hypothesis` (in `test_chain_definition.py`) is the real fork test, and `queries.py::branching_factor`'s `per_node` dict realises the per-parent fork count under a different name.
<!-- THOUGHT:END -->
