---
id: hyp:chain-engine-r1
mint_id: 94e64a12573543b1873c30ebc912f456
type: hypothesis
parents:
  - idea:domain-chain-engine
next_edges:
  - exp:chain-engine-r1
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - chain-engine
  - R1
testable_claim: Chain Definition
thought_session: season
title: "chain-engine/R1: Chain Definition"
---
**Description:** A chain is an ordered path through the autoresearch node types: idea, hypothesis (one or more), experiment (one or more), verdict, mvp, outcome, bigger_outcome, app_purpose.

**Acceptance Criteria:**
- [ ] A chain is defined as an ordered sequence of node ids whose types appear in the documented order
- [ ] A chain may include multiple consecutive hypothesis or experiment nodes between an idea and a verdict
- [ ] A path that skips a required type (for example reaching mvp without an experiment) is not recognized as a chain
- [ ] Two chains may share any prefix, and shared-prefix chains are not deduplicated

**Dependencies:** schema-registry (R8 built-in schemas), graph-core (R1, R2)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); already closed by `verdict:chain-engine-r1` before this pass; deprecated with its domain (`idea:domain-chain-engine`).
<!-- THOUGHT:END -->