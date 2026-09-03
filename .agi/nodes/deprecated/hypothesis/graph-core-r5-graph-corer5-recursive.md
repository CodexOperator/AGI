---
id: hyp:graph-core-r5
mint_id: 2c8b63ef7b3845fd93578cfbae98aac6
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - graph-core
  - R5
testable_claim: Recursive Node Bodies
thought_session: L1.09
title: "graph-core/R5: Recursive Node Bodies"
---
**Description:** A node body may itself contain a subgraph. The same primitives and the same renderers handle top-level and recursive subgraphs.

**Acceptance Criteria:**
- [ ] A node whose frontmatter declares `subgraph: true` is treated as a container; its body is parsed as a graph using the same loader
- [ ] Recursive subgraphs may nest at least three levels deep without special-case code paths
- [ ] Renderers are invoked uniformly on a top-level graph and on a nested subgraph using the same input contract
- [ ] Querying a parent node exposes both its outer-graph children and an opaque handle to its inner subgraph

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r5-by-citation` citing `build:tests-graph-core-test-recursive-bodies`, `build:tests-graph-core-test-uniform-contract`: `test_recursive_bodies.py` loads nested subgraphs three levels deep and `test_uniform_contract.py` asserts node and subgraph share one contract.
<!-- THOUGHT:END -->
