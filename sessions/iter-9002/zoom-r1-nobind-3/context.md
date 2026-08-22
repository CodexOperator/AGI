# autoresearch-tree iteration 9002 — agent zoom-r1-nobind-3

## Zoom Level: 3 — Code nodes
Level 3 is actual code: one level3 node per source file (nodes/level3/*.md), each with a payload_ref to the real file and a mechanically-generated IO contract (inputs/outputs — harness-owned, never authored by a summarising model). goal:g2.1 calls this the level that makes the graph an executable artifact rather than a description of one, and it is the only level with a real index behind it today.

73 level-3 (level3) node(s) across the whole corpus (no --target given).

### Code nodes in scope
-   `level3:bin-benchmark` — Level-3: extensions/agi/bin/benchmark.py
    file: extensions/agi/bin/benchmark.py
    parents: idea:engine-benchmark
-   `level3:bin-cli` — Level-3: extensions/agi/bin/cli.py
    file: extensions/agi/bin/cli.py
    parents: idea:engine-cli
-   `level3:bin-dashboard` — Level-3: extensions/agi/bin/dashboard.py
    file: extensions/agi/bin/dashboard.py
    parents: idea:engine-dashboard
-   `level3:bin-decompose-engine` — Level-3: extensions/agi/bin/decompose-engine.py
    file: extensions/agi/bin/decompose-engine.py
    parents: idea:engine-decompose-engine
-   `level3:bin-dispatch` — Level-3: extensions/agi/bin/dispatch.py
    file: extensions/agi/bin/dispatch.py
    parents: idea:engine-dispatch
-   `level3:bin-evidence-gate` — Level-3: extensions/agi/bin/evidence_gate.py
    file: extensions/agi/bin/evidence_gate.py
    parents: idea:engine-evidence-gate
-   `level3:bin-grid` — Level-3: extensions/agi/bin/grid.py
    file: extensions/agi/bin/grid.py
    parents: idea:engine-grid
-   `level3:bin-heal` — Level-3: extensions/agi/bin/heal.py
    file: extensions/agi/bin/heal.py
    parents: idea:engine-heal
-   `level3:bin-level3` — Level-3: extensions/agi/bin/level3.py
    file: extensions/agi/bin/level3.py
    parents: idea:engine-level3
-   `level3:bin-metrics` — Level-3: extensions/agi/bin/metrics.py
    file: extensions/agi/bin/metrics.py
    parents: idea:engine-metrics
-   `level3:bin-post-wire` — Level-3: extensions/agi/bin/post_wire.py
    file: extensions/agi/bin/post_wire.py
    parents: idea:engine-post-wire
-   `level3:bin-render-context` — Level-3: extensions/agi/bin/render-context.py
    file: extensions/agi/bin/render-context.py
    parents: idea:engine-render-context
-   `level3:bin-snapshot-build-site` — Level-3: extensions/agi/bin/snapshot-build-site.py
    file: extensions/agi/bin/snapshot-build-site.py
    parents: idea:engine-snapshot-build-site
-   `level3:bin-snapshot-goals` — Level-3: extensions/agi/bin/snapshot-goals.py
    file: extensions/agi/bin/snapshot-goals.py
    parents: idea:engine-snapshot-goals
-   `level3:bin-zoom` — Level-3: extensions/agi/bin/zoom.py
    file: extensions/agi/bin/zoom.py
    parents: idea:engine-zoom
-   `level3:src-agi-algos-asciirender` — Level-3: extensions/agi/src/agi_algos/asciirender.py
    file: extensions/agi/src/agi_algos/asciirender.py
    parents: idea:engine-agi-algos
-   `level3:src-agi-algos-benchmark` — Level-3: extensions/agi/src/agi_algos/benchmark.py
    file: extensions/agi/src/agi_algos/benchmark.py
    parents: idea:engine-agi-algos
-   `level3:src-agi-algos-graph-builder` — Level-3: extensions/agi/src/agi_algos/graph_builder.py
    file: extensions/agi/src/agi_algos/graph_builder.py
    parents: idea:engine-agi-algos
-   `level3:src-agi-algos-init` — Level-3: extensions/agi/src/agi_algos/__init__.py
    file: extensions/agi/src/agi_algos/__init__.py
    parents: idea:engine-agi-algos
-   `level3:src-agi-algos-pi-tree-adapter` — Level-3: extensions/agi/src/agi_algos/pi_tree_adapter.py
    file: extensions/agi/src/agi_algos/pi_tree_adapter.py
    parents: idea:engine-agi-algos
-   `level3:src-agi-algos-query-engine` — Level-3: extensions/agi/src/agi_algos/query_engine.py
    file: extensions/agi/src/agi_algos/query_engine.py
    parents: idea:engine-agi-algos
-   `level3:src-chain-engine-attractiveness` — Level-3: extensions/agi/src/chain_engine/attractiveness.py
    file: extensions/agi/src/chain_engine/attractiveness.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-chains` — Level-3: extensions/agi/src/chain_engine/chains.py
    file: extensions/agi/src/chain_engine/chains.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-init` — Level-3: extensions/agi/src/chain_engine/__init__.py
    file: extensions/agi/src/chain_engine/__init__.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-mid-chain` — Level-3: extensions/agi/src/chain_engine/mid_chain.py
    file: extensions/agi/src/chain_engine/mid_chain.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-queries` — Level-3: extensions/agi/src/chain_engine/queries.py
    file: extensions/agi/src/chain_engine/queries.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-query-api` — Level-3: extensions/agi/src/chain_engine/query_api.py
    file: extensions/agi/src/chain_engine/query_api.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-ranking` — Level-3: extensions/agi/src/chain_engine/ranking.py
    file: extensions/agi/src/chain_engine/ranking.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-renderers-init` — Level-3: extensions/agi/src/chain_engine/renderers/__init__.py
    file: extensions/agi/src/chain_engine/renderers/__init__.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-renderers-mermaid` — Level-3: extensions/agi/src/chain_engine/renderers/mermaid.py
    file: extensions/agi/src/chain_engine/renderers/mermaid.py
    parents: idea:engine-chain-engine
-   `level3:src-chain-engine-types` — Level-3: extensions/agi/src/chain_engine/types.py
    file: extensions/agi/src/chain_engine/types.py
    parents: idea:engine-chain-engine
-   `level3:src-embeddings-init` — Level-3: extensions/agi/src/embeddings/__init__.py
    file: extensions/agi/src/embeddings/__init__.py
    parents: idea:engine-embeddings
-   `level3:src-embeddings-node2vec` — Level-3: extensions/agi/src/embeddings/node2vec.py
    file: extensions/agi/src/embeddings/node2vec.py
    parents: idea:engine-embeddings
-   `level3:src-embeddings-projection` — Level-3: extensions/agi/src/embeddings/projection.py
    file: extensions/agi/src/embeddings/projection.py
    parents: idea:engine-embeddings
-   `level3:src-embeddings-similarity` — Level-3: extensions/agi/src/embeddings/similarity.py
    file: extensions/agi/src/embeddings/similarity.py
    parents: idea:engine-embeddings
-   `level3:src-graph-core-cache` — Level-3: extensions/agi/src/graph_core/cache.py
    file: extensions/agi/src/graph_core/cache.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-db-loader` — Level-3: extensions/agi/src/graph_core/db_loader.py
    file: extensions/agi/src/graph_core/db_loader.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-edge` — Level-3: extensions/agi/src/graph_core/edge.py
    file: extensions/agi/src/graph_core/edge.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-errors` — Level-3: extensions/agi/src/graph_core/errors.py
    file: extensions/agi/src/graph_core/errors.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-graph` — Level-3: extensions/agi/src/graph_core/graph.py
    file: extensions/agi/src/graph_core/graph.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-identity` — Level-3: extensions/agi/src/graph_core/identity.py
    file: extensions/agi/src/graph_core/identity.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-init` — Level-3: extensions/agi/src/graph_core/__init__.py
    file: extensions/agi/src/graph_core/__init__.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-loader` — Level-3: extensions/agi/src/graph_core/loader.py
    file: extensions/agi/src/graph_core/loader.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-node` — Level-3: extensions/agi/src/graph_core/node.py
    file: extensions/agi/src/graph_core/node.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-persistence-backend` — Level-3: extensions/agi/src/graph_core/persistence/backend.py
    file: extensions/agi/src/graph_core/persistence/backend.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-persistence-filesystem` — Level-3: extensions/agi/src/graph_core/persistence/filesystem.py
    file: extensions/agi/src/graph_core/persistence/filesystem.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-persistence-frontmatter` — Level-3: extensions/agi/src/graph_core/persistence/frontmatter.py
    file: extensions/agi/src/graph_core/persistence/frontmatter.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-persistence-in-memory` — Level-3: extensions/agi/src/graph_core/persistence/in_memory.py
    file: extensions/agi/src/graph_core/persistence/in_memory.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-persistence-init` — Level-3: extensions/agi/src/graph_core/persistence/__init__.py
    file: extensions/agi/src/graph_core/persistence/__init__.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-persistence-lazy-body` — Level-3: extensions/agi/src/graph_core/persistence/lazy_body.py
    file: extensions/agi/src/graph_core/persistence/lazy_body.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-persistence-sqlite-backend` — Level-3: extensions/agi/src/graph_core/persistence/sqlite_backend.py
    file: extensions/agi/src/graph_core/persistence/sqlite_backend.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-templates-init` — Level-3: extensions/agi/src/graph_core/templates/__init__.py
    file: extensions/agi/src/graph_core/templates/__init__.py
    parents: idea:engine-graph-core
-   `level3:src-graph-core-types` — Level-3: extensions/agi/src/graph_core/types.py
    file: extensions/agi/src/graph_core/types.py
    parents: idea:engine-graph-core
-   `level3:src-init` — Level-3: extensions/agi/src/__init__.py
    file: extensions/agi/src/__init__.py
-   `level3:src-renderers-ascii` — Level-3: extensions/agi/src/renderers/ascii.py
    file: extensions/agi/src/renderers/ascii.py
    parents: idea:engine-renderers
-   `level3:src-renderers-git-diff` — Level-3: extensions/agi/src/renderers/git_diff.py
    file: extensions/agi/src/renderers/git_diff.py
    parents: idea:engine-renderers
-   `level3:src-renderers-init` — Level-3: extensions/agi/src/renderers/__init__.py
    file: extensions/agi/src/renderers/__init__.py
    parents: idea:engine-renderers
-   `level3:src-renderers-mermaid` — Level-3: extensions/agi/src/renderers/mermaid.py
    file: extensions/agi/src/renderers/mermaid.py
    parents: idea:engine-renderers
-   `level3:src-renderers-representation` — Level-3: extensions/agi/src/renderers/representation.py
    file: extensions/agi/src/renderers/representation.py
    parents: idea:engine-renderers
-   `level3:src-schema-registry-active-set` — Level-3: extensions/agi/src/schema_registry/active_set.py
    file: extensions/agi/src/schema_registry/active_set.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-cascade` — Level-3: extensions/agi/src/schema_registry/cascade.py
    file: extensions/agi/src/schema_registry/cascade.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-dsl` — Level-3: extensions/agi/src/schema_registry/dsl.py
    file: extensions/agi/src/schema_registry/dsl.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-fingerprint` — Level-3: extensions/agi/src/schema_registry/fingerprint.py
    file: extensions/agi/src/schema_registry/fingerprint.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-hooks-cascade-step` — Level-3: extensions/agi/src/schema_registry/hooks/cascade_step.py
    file: extensions/agi/src/schema_registry/hooks/cascade_step.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-hooks-claude-hook` — Level-3: extensions/agi/src/schema_registry/hooks/claude_hook.py
    file: extensions/agi/src/schema_registry/hooks/claude_hook.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-hooks-init` — Level-3: extensions/agi/src/schema_registry/hooks/__init__.py
    file: extensions/agi/src/schema_registry/hooks/__init__.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-hooks-none-hook` — Level-3: extensions/agi/src/schema_registry/hooks/none_hook.py
    file: extensions/agi/src/schema_registry/hooks/none_hook.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-hooks-ollama-hook` — Level-3: extensions/agi/src/schema_registry/hooks/ollama_hook.py
    file: extensions/agi/src/schema_registry/hooks/ollama_hook.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-hooks-protocol` — Level-3: extensions/agi/src/schema_registry/hooks/protocol.py
    file: extensions/agi/src/schema_registry/hooks/protocol.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-init` — Level-3: extensions/agi/src/schema_registry/__init__.py
    file: extensions/agi/src/schema_registry/__init__.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-loader` — Level-3: extensions/agi/src/schema_registry/loader.py
    file: extensions/agi/src/schema_registry/loader.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-meta-nodes` — Level-3: extensions/agi/src/schema_registry/meta_nodes.py
    file: extensions/agi/src/schema_registry/meta_nodes.py
    parents: idea:engine-schema-registry
-   `level3:src-schema-registry-validation` — Level-3: extensions/agi/src/schema_registry/validation.py
    file: extensions/agi/src/schema_registry/validation.py
    parents: idea:engine-schema-registry

## Your Task
Pick one `level3` node above to extend, fork, or seed a new chain from.
Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).
When done, signal completion:
```
python3 <plugin>/bin/cli.py done 9002 zoom-r1-nobind-3 \
  --verdict <verdict_state> --confidence <0.0-1.0> \
  --node-id <new_node_id> \
  --notes "<one-line>"
```

If stuck >2 attempts → write `pending` verdict and stop.
