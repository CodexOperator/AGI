---
id: hyp:embeddings-r1
mint_id: 86246cab298c4b7a8a3973546c73dbc4
type: hypothesis
parents:
  - idea:domain-embeddings
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - embeddings
  - R1
testable_claim: Per-Node Vector Generation
thought_session: season
title: "embeddings/R1: Per-Node Vector Generation"
---
**Description:** A vector is generated per node by running Node2Vec over the graph-core graph. The choice of Node2Vec is fixed for v1; alternative models are out of scope.

**Acceptance Criteria:**
- [ ] After embedding, every node in the input graph has exactly one associated vector
- [ ] Vector dimensionality is configurable and defaults to a documented value
- [ ] Two runs over the same graph and configuration produce identical vectors when the random seed is fixed
- [ ] When the graph contains zero nodes, the embedding step completes successfully and produces an empty vector set

**Dependencies:** graph-core (R1, R2)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:embeddings-r1-by-citation` citing `build:src-embeddings-node2vec`, `build:tests-embeddings-test-node2vec`: `node2vec.py` is per-node Node2Vec with a seed and `test_node2vec.py` pins determinism.
<!-- THOUGHT:END -->