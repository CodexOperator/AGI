---
id: hyp:environment-indexers-r5
mint_id: a4d5f36c846a467a8f4c538d0c0595ee
type: hypothesis
parents:
  - idea:domain-environment-indexers
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - environment-indexers
  - R5
testable_claim: API Dependency Indexer
thought_session: L1.09
title: "environment-indexers/R5: API Dependency Indexer"
---
**Description:** An indexer emits nodes describing endpoints and their relationships from an OpenAPI or Swagger specification.

**Acceptance Criteria:**
- [ ] Running this indexer on a valid specification file emits one node per endpoint
- [ ] Each endpoint node carries method, path, and summary fields in its frontmatter
- [ ] Edges record which endpoints share schemas or reference each other
- [ ] An invalid specification file produces a structured error naming the offending file and emits no nodes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
