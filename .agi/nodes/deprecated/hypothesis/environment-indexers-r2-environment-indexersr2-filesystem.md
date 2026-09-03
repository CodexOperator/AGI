---
id: hyp:environment-indexers-r2
mint_id: 485900a5cbb24cc696169f13c3ece7dc
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
  - R2
testable_claim: Filesystem Tree Indexer
thought_session: L1.09
title: "environment-indexers/R2: Filesystem Tree Indexer"
---
**Description:** An indexer emits one node per directory and one node per file under a target path.

**Acceptance Criteria:**
- [ ] Running this indexer on any directory produces a node for the directory and one child node per file or subdirectory
- [ ] Each emitted node carries frontmatter that conforms to the registered filesystem-tree schema
- [ ] Symbolic links and unreadable entries are skipped with a per-entry warning rather than aborting the run
- [ ] Re-running the indexer on the same path produces the same node ids and the same parent-child links

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
