---
id: hyp:environment-indexers-r1
mint_id: 9d942ac4bc864f4b8d15141672a75741
type: hypothesis
parents:
  - idea:domain-environment-indexers
next_edges:
  - exp:environment-indexers-r1
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - environment-indexers
  - R1
testable_claim: Indexer Invocation Command
thought_session: L1.09
title: "environment-indexers/R1: Indexer Invocation Command"
---
**Description:** A single command runs a chosen indexer over a chosen path and writes results into the graph.

**Acceptance Criteria:**
- [ ] The command accepts a target path and an indexer name and runs only that indexer
- [ ] Listing available indexers without invoking one produces a summary with each indexer's name and one-line description
- [ ] An unknown indexer name returns a structured error and does not run anything
- [ ] The command exits with a non-zero status when the indexer reports any failure that prevented node emission

**Dependencies:** graph-core (R10 bootstrap), schema-registry (R1 schema-as-file)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); already closed by `verdict:environment-indexers-r1` before this pass -- a closure §F R1 calls hollow (self-asserted, `evidence_runs: []`, demoted from proved), so it is not treated as evidence; deprecated with its domain (`idea:domain-environment-indexers`).
<!-- THOUGHT:END -->
