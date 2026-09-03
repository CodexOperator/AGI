---
id: hyp:autoresearch-tree-skill-r4
mint_id: 8df1769734894bf3849894b691314916
type: hypothesis
parents:
  - idea:domain-autoresearch-tree-skill
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - autoresearch-tree-skill
  - R4
testable_claim: Per-Agent Briefing Payload
thought_session: L1.09
title: "autoresearch-tree-skill/R4: Per-Agent Briefing Payload"
---
**Description:** Each builder agent receives a briefing that contains the current chain statistics, the attractiveness scores for candidate chains, and the menu of available actions (extend, fork, hop, fresh start).

**Acceptance Criteria:**
- [ ] The briefing names the current set of chains under consideration with their length, depth, recency, and mvp count
- [ ] The briefing names each candidate chain's attractiveness score from the chain-engine
- [ ] The briefing lists the available actions per chain (extend at tail, fork at named node, hop to a mid-chain candidate, start fresh)
- [ ] The briefing is generated from chain-engine queries only and does not include implementation details of the engine

**Dependencies:** chain-engine (R3, R4, R6, R9)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r4-by-citation` citing `build:src-chain-engine-query-api`, `build:bin-dispatch`: `chain_engine/query_api.py` (`task_attractiveness`, `chain_gaps`, `next_best_hypothesis`, `coverage_report`) is the briefing data and `dispatch.py` assembles the kid brief.
<!-- THOUGHT:END -->
