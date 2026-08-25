---
confidence: 0.5
id: "hyp:schema-registry-r8"
mint_id: c15b12ebc5594c4c985075fea10dd0ba
origin: build-site
parents:
  - idea:domain-schema-registry
subgraph: false
tags:
  - schema-registry
  - R8
testable_claim: Built-In Schemas for Autoresearch Types
title: "schema-registry/R8: Built-In Schemas for Autoresearch Types"
type: hypothesis
---

**Description:** A baseline set of schemas ships with the registry to define the autoresearch node types so chain-engine, renderers, and the skill can rely on them.

**Acceptance Criteria:**
- [ ] After bootstrap, the registry contains active schemas named `idea`, `hypothesis`, `experiment`, `verdict`, `mvp`, `outcome`, `bigger_outcome`, and `app_purpose`
- [ ] Each built-in schema declares the fields its corresponding node type must carry, including verdict taxonomy fields where applicable
- [ ] Built-in schemas can be overridden by a user-supplied bracketed schema of the same name without code changes
- [ ] Removing a built-in schema makes downstream features that depend on it report a clear missing-schema error rather than crashing

**Dependencies:** none (consumed by chain-engine, which uses the autoresearch types defined here)

## Out of Scope

- Storage of node data — see graph-core
- Indexing of external sources (code, filesystem trees, OpenAPI specs) — see environment-indexers
- Chain-shaped logic over autoresearch nodes — see chain-engine
- Rendering of meta-nodes alongside ordinary nodes — see renderers

## Cross-References

- See also: cavekit-graph-core.md (R4 frontmatter persistence, R6 directory walking)
- See also: cavekit-environment-indexers.md (each indexer registers or references a schema)
- See also: cavekit-chain-engine.md (uses built-in autoresearch schemas)
- See also: cavekit-renderers.md (may render meta-nodes)
- See also: cavekit-autoresearch-tree-skill.md (relies on built-in schemas to emit verdicts and chain nodes)
