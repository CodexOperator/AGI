---
id: hyp:graph-core-r6
mint_id: 59fdb7a61fb648409a283dcfe7ca0072
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
  - R6
testable_claim: Directory-Walking Auto-Discovery
thought_session: L1.09
title: "graph-core/R6: Directory-Walking Auto-Discovery"
---
**Description:** A directory of node files is loaded by walking the filesystem. A folder is a subgraph; files inside are nodes; folder names map to node types via the schema-registry.

**Acceptance Criteria:**
- [ ] Pointing the loader at any directory yields a graph whose nodes correspond to the files under that directory
- [ ] A subdirectory is loaded as a subgraph node whose type is resolved through the schema-registry
- [ ] Files that do not match any known schema are loaded as generic nodes and a warning is emitted listing them
- [ ] Walking is deterministic: two runs against the same directory produce the same node set and id order

**Dependencies:** schema-registry (for folder-name → node-type resolution)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r6-by-citation` citing `build:src-graph-core-loader`, `build:tests-graph-core-test-loader`, `build:tests-graph-core-test-walk-determinism`: `loader.py` is the directory walk with schema-resolved subgraphs and `test_walk_determinism.py` pins the walk order.
<!-- THOUGHT:END -->
