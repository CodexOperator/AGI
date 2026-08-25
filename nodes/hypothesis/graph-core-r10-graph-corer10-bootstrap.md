---
confidence: 0.5
id: "hyp:graph-core-r10"
mint_id: 3721a5b0b1ad481888ad4e54c3864a1f
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R10
testable_claim: Bootstrap Command
title: "graph-core/R10: Bootstrap Command"
type: hypothesis
---

**Description:** A command initializes a new project so a fresh directory becomes a valid graph root.

**Acceptance Criteria:**
- [ ] Running the bootstrap command in an empty directory produces a `context/` skeleton with subdirectories for schemas, kits, and node storage
- [ ] Running the bootstrap command twice on the same directory is a no-op and does not overwrite existing files
- [ ] The skeleton includes a minimal example node and a minimal example schema sufficient to load a one-node graph
- [ ] The bootstrap reports the created paths to the user in a single summary

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
