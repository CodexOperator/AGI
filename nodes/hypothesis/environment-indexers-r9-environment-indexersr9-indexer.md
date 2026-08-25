---
confidence: 0.5
id: "hyp:environment-indexers-r9"
mint_id: 106a6365f70644bead2028d672df7ee9
origin: build-site
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R9
testable_claim: Indexer Documentation and Upgrade Markers
title: "environment-indexers/R9: Indexer Documentation and Upgrade Markers"
type: hypothesis
---

**Description:** Each indexer's source documents its own internals well enough that a future contributor can replace the parsing or scanning core without re-deriving the schema mapping.

**Acceptance Criteria:**
- [ ] Each indexer file contains comments explaining at least its parsing strategy, its schema mapping, and its caching behavior
- [ ] Each indexer file contains at least one comment block tagged as an upgrade marker, naming the section eligible for replacement
- [ ] Upgrade markers are discoverable by a single grep over the indexers directory
- [ ] A documentation self-check command lists each indexer and reports whether it has at least one upgrade marker

## Out of Scope

- Chain-specific autoresearch node types (idea, hypothesis, experiment, verdict, mvp, outcome, bigger_outcome, app_purpose) — see chain-engine
- Rendering of indexed graphs — see renderers
- The autoresearch agent loop that decides what to index when — see autoresearch-tree-skill
- Mutating indexers that change source repositories or running containers — explicitly out of bounds

## Cross-References

- See also: cavekit-graph-core.md (R1 nodes, R2 edges, R7 caching, R9 portability)
- See also: cavekit-schema-registry.md (each indexer registers or references a schema)
- See also: cavekit-renderers.md (consumes nodes the indexers produce)
- See also: cavekit-autoresearch-tree-skill.md (invokes indexers as part of the loop)
