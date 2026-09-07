---
id: hyp:graph-core-r11
mint_id: d150cfab6a12409e9653ad179585dce3
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - graph-core
  - R11
testable_claim: Traversal and Query API
thought_session: season
title: "graph-core/R11: Traversal and Query API"
---
**Description:** The graph exposes traversal primitives and a query API over the loaded node set, returning lazy iterators so a caller never pays for a full materialization it does not use.

**Acceptance Criteria:**
- [ ] R11.1 — `traverse_bfs(start_id)` yields node ids in breadth-first order as a lazy generator
- [ ] R11.2 — `traverse_dfs(start_id)` yields node ids in depth-first order as a lazy generator
- [ ] R11.3 — `find_paths(source_id, target_id)` returns all simple paths via DFS backtracking
- [ ] R11.4 — `find_ancestors(node_id)` returns the transitive parent closure via BFS
- [ ] R11.5 — `find_descendants(node_id)` returns the transitive child closure via BFS
- [ ] R11.6 — `query(type=None, tags=None, has_parent=None, has_child=None)` filters nodes without loading bodies
- [ ] R11.7 — every traversal and query entry point returns a lazy iterator, not a materialized list
- [ ] R11.8 — `detect_cycle(node_id)` runs DFS from that node and reports any cycle path it finds

## Out of Scope

- Autoresearch-specific node types such as `idea`, `hypothesis`, `experiment`, `verdict`, `mvp`, `outcome`, `bigger_outcome`, `app_purpose` — these are schema definitions, not graph-core concerns
- Chain mechanics, longest-chain attraction, fork or hop logic — see chain-engine
- ASCII, Mermaid, or git-shaped rendering — see renderers
- Vector embeddings or similarity APIs — see embeddings
- Specific source indexers (filesystem trees, code symbols, dependency graphs) — see environment-indexers

## Cross-References

- See also: cavekit-schema-registry.md (folder-name to node-type resolution, schemas as meta-nodes)
- See also: cavekit-environment-indexers.md (consumes graph-core to write nodes)
- See also: cavekit-chain-engine.md (computes chains over graph-core nodes)
- See also: cavekit-renderers.md (renders graph-core nodes)
- See also: cavekit-embeddings.md (vectorizes graph-core nodes)
- See also: cavekit-autoresearch-tree-skill.md (drives the loop on top of graph-core)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-SMALL-EXPERIMENT, not run: `graph.py` exposes none of BFS/DFS/find_paths/ancestors/descendants publicly, but `chain_engine/query_api.py` already carries a private `_bfs_descendants`; promoting it into `graph_core` with a thin test file is small -- no existing goal obviously covers it, so this THOUGHT is the record.
<!-- THOUGHT:END -->