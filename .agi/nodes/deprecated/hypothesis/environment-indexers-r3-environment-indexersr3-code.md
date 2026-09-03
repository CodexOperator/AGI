---
id: hyp:environment-indexers-r3
mint_id: 26068eb634be4e21865cabe7c651049a
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
  - R3
testable_claim: Code Symbol Indexer
thought_session: L1.09
title: "environment-indexers/R3: Code Symbol Indexer"
---
**Description:** An indexer emits nodes for code symbols (functions, classes, methods, modules) and edges for the relationships between them. The internals carry forward the lessons of the predecessor project (warm-load caching, tag-based bridging edges, precomputed traversal paths) but are re-implemented against this kit's contracts rather than copied.

**Acceptance Criteria:**
- [ ] Running this indexer on a code repository emits at minimum function, class, method, and module nodes for the supported language
- [ ] The emitted graph contains relationship edges sufficient to answer "callers of X" and "callees of X" queries
- [ ] The indexer warm-loads in time indistinguishable from a no-op on a previously-indexed unchanged repository
- [ ] Inline comments inside the indexer's source flag at least one upgrade point per major parsing stage (for example "this regex parser could be replaced by a tree-based parser later")

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
