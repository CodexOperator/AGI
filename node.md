---
id: hyp:environment-indexers-r6
mint_id: 913637130a4d4b8fbc327d243f8b1f34
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
  - R6
testable_claim: Container Observation Indexer
thought_session: season
title: "environment-indexers/R6: Container Observation Indexer"
---
**Description:** An indexer emits nodes describing a running container observed read-only from the outside, with no modification of the container.

**Acceptance Criteria:**
- [ ] Running this indexer against an accessible container produces a node for the container plus child nodes for each observable surface (image, ports, mounts, environment keys with values redacted)
- [ ] No write operation is issued against the container or its host
- [ ] When the target container is unreachable, the indexer returns a structured error and emits no nodes
- [ ] Sensitive values (secrets, tokens) are redacted before being written into node frontmatter

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->