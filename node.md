---
id: hyp:chain-engine-r3
mint_id: 1848c9bfda8849f7b34ae8bf7dd68f4d
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
  - R3
testable_claim: Longest-Chain Attractor
thought_session: season
title: "chain-engine/R3: Longest-Chain Attractor"
---
**Description:** Among current chains, longer chains are preferred but not exclusive. Attractiveness is a weighted score and short chains may still be selected if their score is competitive.

**Acceptance Criteria:**
- [ ] When asked to rank chains, the engine returns them sorted by attractiveness with ties broken deterministically
- [ ] The longest chain is among the top-ranked results when no other factor dominates
- [ ] Short chains can rank above longer chains when their non-length scores are sufficiently higher
- [ ] The ranking function is pure: equal inputs produce equal outputs across runs

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r3-by-citation` citing `build:src-chain-engine-ranking`: `ranking.py` is longest-chain ranking with a deterministic tie-break.
<!-- THOUGHT:END -->