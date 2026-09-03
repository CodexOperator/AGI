---
id: idea:domain-chain-engine
mint_id: 60dfa5469cb1476cbc740e5957f16f7f
type: idea
next_edges:
  - hyp:chain-engine-r1
confidence: 1.0
edited_by: l1.09-execution-parent
origin: build-site
scale: big
status: deprecated
tags:
  - domain
  - seed
thought_session: L1.09
title: "Domain: chain-engine"
---
The autoresearch-specific layer that sits on top of graph-core. It defines what a chain is, how chains are scored and selected, how agents join, fork, or hop between them, and what verdicts look like. It contains all the autoresearch semantics so graph-core can remain a generic substrate. Chains are virtual: they are computed from the underlying graph rather than stored as separate first-class objects.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §B/§D/§E): the domain is built at `extensions/agi/src/chain_engine/` (`idea:engine-chain-engine` is the live counterpart) and `goal:g3`/`goal:g10.2`/`goal:g10.3` are its real descendants; no new goal (§B).
<!-- THOUGHT:END -->
