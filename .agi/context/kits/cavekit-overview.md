---
created: 2026-04-30
last_edited: 2026-04-30
---

# Cavekit: overview

## Purpose

Index and dependency map for the autoresearch-tree cavekit set. Read this first to understand which kit owns which concern and to choose a safe order for downstream design and implementation work.

## Domain Index

| Kit | One-Line Description |
|---|---|
| cavekit-graph-core.md | Generic, domain-agnostic node and edge primitives, identity scheme, frontmatter persistence, recursive bodies, directory-walking auto-discovery, warm-load caching, pluggable persistence, portability contract, bootstrap command. |
| cavekit-schema-registry.md | File-based schema registry with bracket-activation convention, schemas-as-meta-nodes, validation hooks, an auto-discovery cascade that ends in a language-model fallback, and a built-in schema set covering the autoresearch node types. |
| cavekit-environment-indexers.md | On-demand pluggable indexers for filesystem trees, code symbols, Python dependencies, OpenAPI specifications, and read-only container observation. Each indexer is one self-contained file with documented upgrade markers and per-path caching. |
| cavekit-chain-engine.md | Autoresearch-specific layer over graph-core: virtual chains, longest-chain attractor, mid-chain join, fork mechanics, attractiveness scoring, configuration file, verdict taxonomy, and chain query API. |
| cavekit-renderers.md | Multi-format renderers (ASCII primary, Mermaid, git-tree shape, git-diff between runs) over a shared internal representation, with a plugin contract, recursive rendering, and a pure-function guarantee. |
| cavekit-embeddings.md | Node2Vec vectors plus UMAP projection whose two-dimensional coordinates ARE the renderer-side coordinates, with cache invalidation on graph change, similarity query, scatter renderer plugin, and optional in-graph storage. |
| cavekit-autoresearch-tree-skill.md | The pi skill that drives the loop: forks the autoresearch skill repository, decides big-idea-versus-small-idea per iteration, dispatches up to five Claude builders in parallel (Ollama deferred), emits taxonomy-conformant verdicts, and runs an extended benchmark harness with new chain-shaped metrics. Drop-in portable. |

## Dependency Graph

```
                                 graph-core
                                /     |     \
                               /      |      \
              schema-registry         |       renderers
                  /  |                |          |
                 /   |                |          |
                /    |                |       embeddings
               /     |                |       /
              /      |                |      /
environment-indexers chain-engine    /      /
              \      |              /      /
               \     |             /      /
                \    |            /      /
                 \   |           /      /
                  \  |          /      /
                   autoresearch-tree-skill
```

Read in dependency order:

1. graph-core
2. schema-registry
3. environment-indexers (parallel with chain-engine, renderers, embeddings)
4. chain-engine (parallel with environment-indexers, renderers, embeddings)
5. renderers (parallel with environment-indexers, chain-engine; before embeddings)
6. embeddings (after renderers because it shares the renderer representation)
7. autoresearch-tree-skill (last — depends on all of the above)

## Cross-Reference Map

| Source Kit | Depends On |
|---|---|
| graph-core | (none) |
| schema-registry | graph-core |
| environment-indexers | graph-core, schema-registry |
| chain-engine | graph-core, schema-registry |
| renderers | graph-core |
| embeddings | graph-core, renderers |
| autoresearch-tree-skill | graph-core, schema-registry, environment-indexers, chain-engine, renderers, embeddings |

## Coverage Summary

| Kit | Requirements | Acceptance Criteria |
|---|---|---|
| cavekit-graph-core.md | 10 | 40 |
| cavekit-schema-registry.md | 8 | 32 |
| cavekit-environment-indexers.md | 9 | 36 |
| cavekit-chain-engine.md | 9 | 36 |
| cavekit-renderers.md | 8 | 32 |
| cavekit-embeddings.md | 7 | 28 |
| cavekit-autoresearch-tree-skill.md | 8 | 32 |
| Total | 59 | 236 |

## Notes for Downstream Plans

- The renderers kit and the embeddings kit jointly own the shared representation contract; any change to the render token shape requires updates in both.
- The schema-registry's built-in schema set is the contract surface that lets chain-engine and the skill rely on autoresearch types without depending on each other.
- environment-indexers is independent of chain-engine; both depend on graph-core and schema-registry but neither depends on the other.
- All persistence lives inside the project context directory. No kit declares external services, daemons, or absolute host paths.
- Ollama dispatch, in-memory database backend, and cross-repo orchestration are out of scope across the entire set.
