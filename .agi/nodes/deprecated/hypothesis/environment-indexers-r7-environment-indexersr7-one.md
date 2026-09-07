---
id: hyp:environment-indexers-r7
mint_id: e77e9c58204d409aa004a835a536a31f
type: hypothesis
parents:
  - idea:domain-environment-indexers
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - environment-indexers
  - R7
testable_claim: One-File-Per-Indexer Layout
thought_session: season
title: "environment-indexers/R7: One-File-Per-Indexer Layout"
---
**Description:** Each indexer is a single self-contained file with documented internals and registers or references at least one schema.

**Acceptance Criteria:**
- [ ] Each indexer lives in its own file under the indexers directory
- [ ] Each indexer either registers a new schema with the schema-registry or references an existing built-in schema
- [ ] Each indexer file documents its inputs, outputs, and known limitations in a header comment block
- [ ] Removing an indexer file removes only that indexer's command without affecting others

**Dependencies:** schema-registry (R1, R8)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->