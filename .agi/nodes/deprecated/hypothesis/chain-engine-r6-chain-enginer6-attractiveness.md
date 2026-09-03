---
id: hyp:chain-engine-r6
mint_id: 6718ef01f5d248148b3f6ee2733c7c3b
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
  - R6
testable_claim: Attractiveness Function
thought_session: L1.09
title: "chain-engine/R6: Attractiveness Function"
---
**Description:** The score that ranks chains is a weighted combination of length, depth, recency, and mvp count.

**Acceptance Criteria:**
- [ ] The score is computed from exactly four documented inputs: chain length, chain depth, recency of the latest node, and count of mvp nodes reached
- [ ] Each weight is supplied through configuration, not hard-coded
- [ ] When all weights are zero, the function returns a stable constant rather than raising
- [ ] Two chains with identical inputs produce identical scores

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r6-by-citation` citing `build:src-chain-engine-attractiveness`, `build:tests-chain-engine-test-attractiveness-impact`: `attractiveness.py` is the pure attractiveness function and `test_attractiveness_impact.py` its suite.
<!-- THOUGHT:END -->
