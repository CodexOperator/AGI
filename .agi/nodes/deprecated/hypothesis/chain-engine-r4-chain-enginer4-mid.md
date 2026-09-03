---
id: hyp:chain-engine-r4
mint_id: 31743e6c4767483a8c47986f6ae2fc8e
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
  - R4
testable_claim: Mid-Chain Join
thought_session: L1.09
title: "chain-engine/R4: Mid-Chain Join"
---
**Description:** An agent may attach to any node mid-chain rather than at the end. The probability of joining mid-chain is a tunable parameter.

**Acceptance Criteria:**
- [ ] A query for join candidates returns nodes from anywhere along candidate chains, not only chain tails
- [ ] The engine applies the configured mid-chain join probability when sampling a join target
- [ ] A minimum-chain-length parameter prevents joining chains shorter than the configured threshold
- [ ] Disabling mid-chain join (probability zero) produces only tail nodes as join candidates

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r4-by-citation` citing `build:src-chain-engine-mid-chain`: `mid_chain.py`'s docstring enumerates R4.1-R4.4 and implements each (`MidChainConfig`: join probability, minimum chain length).
<!-- THOUGHT:END -->
