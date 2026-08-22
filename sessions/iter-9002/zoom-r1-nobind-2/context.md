# autoresearch-tree iteration 9002 — agent zoom-r1-nobind-2

## Zoom Level: 2 — Sub-systems
Level 2 is sub-systems and their relationships: one census node per engine module/entry-point (nodes/idea/engine-*.md), each carrying a unit_path pointing at the real file it describes and a parent goal that motivates it. This is the layer between 'what we want' (level 1) and 'the file that does it' (level 3). Non-census idea nodes (research chains, domain groupings) are deliberately excluded — they are not sub-systems.

26 level-2 (idea) node(s) across the whole corpus (no --target given).

### Sub-systems in scope
-   `idea:engine-agi-algos` — Engine surface: extensions/agi/src/agi_algos
    file: extensions/agi/src/agi_algos
    parents: goal:g2.1
    children: level3:src-agi-algos-asciirender, level3:src-agi-algos-benchmark, level3:src-agi-algos-graph-builder
-   `idea:engine-agi-bridge-index` — Engine surface: extensions/agi-bridge/index.ts
    file: extensions/agi-bridge/index.ts
    parents: goal:g4
-   `idea:engine-benchmark` — Engine surface: extensions/agi/bin/benchmark.py
    file: extensions/agi/bin/benchmark.py
    parents: goal:g3
    children: level3:bin-benchmark
-   `idea:engine-cc-session-start` — Engine surface: extensions/agi/hooks/cc-session-start.sh
    file: extensions/agi/hooks/cc-session-start.sh
    parents: goal:g9
-   `idea:engine-chain-engine` — Engine surface: extensions/agi/src/chain_engine
    file: extensions/agi/src/chain_engine
    parents: goal:g3
    children: level3:src-chain-engine-attractiveness, level3:src-chain-engine-chains, level3:src-chain-engine-init
-   `idea:engine-cli` — Engine surface: extensions/agi/bin/cli.py
    file: extensions/agi/bin/cli.py
    parents: goal:g1
    children: level3:bin-cli
-   `idea:engine-dashboard` — Engine surface: extensions/agi/bin/dashboard.py
    file: extensions/agi/bin/dashboard.py
    parents: goal:g9.1
    children: level3:bin-dashboard
-   `idea:engine-decompose-engine` — Engine surface: extensions/agi/bin/decompose-engine.py
    file: extensions/agi/bin/decompose-engine.py
    parents: goal:g6.1
    children: level3:bin-decompose-engine
-   `idea:engine-dispatch` — Engine surface: extensions/agi/bin/dispatch.py
    file: extensions/agi/bin/dispatch.py
    parents: goal:g4
    children: level3:bin-dispatch
-   `idea:engine-driver-sh` — Engine surface: extensions/agi/driver.sh
    file: extensions/agi/driver.sh
    parents: goal:g1
-   `idea:engine-embeddings` — Engine surface: extensions/agi/src/embeddings
    file: extensions/agi/src/embeddings
    parents: goal:g2
    children: level3:src-embeddings-init, level3:src-embeddings-node2vec, level3:src-embeddings-projection
-   `idea:engine-evidence-gate` — Engine surface: extensions/agi/bin/evidence_gate.py
    file: extensions/agi/bin/evidence_gate.py
    parents: goal:g3.1
    children: level3:bin-evidence-gate
-   `idea:engine-find-root` — Engine surface: extensions/agi/lib/find-root.sh
    file: extensions/agi/lib/find-root.sh
    parents: goal:g1
-   `idea:engine-graph-core` — Engine surface: extensions/agi/src/graph_core
    file: extensions/agi/src/graph_core
    parents: goal:g7
    children: level3:src-graph-core-cache, level3:src-graph-core-db-loader, level3:src-graph-core-edge
-   `idea:engine-grid` — Engine surface: extensions/agi/bin/grid.py
    file: extensions/agi/bin/grid.py
    parents: goal:g7
    children: level3:bin-grid
-   `idea:engine-heal` — Engine surface: extensions/agi/bin/heal.py
    file: extensions/agi/bin/heal.py
    parents: goal:g4
    children: level3:bin-heal
-   `idea:engine-level3` — Engine surface: extensions/agi/bin/level3.py
    file: extensions/agi/bin/level3.py
    parents: goal:g2.1
    children: level3:bin-level3
-   `idea:engine-metrics` — Engine surface: extensions/agi/bin/metrics.py
    file: extensions/agi/bin/metrics.py
    parents: goal:g3
    children: level3:bin-metrics
-   `idea:engine-migrate-to-sqlite` — Engine surface: extensions/agi/scripts/migrate_to_sqlite.py
    file: extensions/agi/scripts/migrate_to_sqlite.py
    parents: goal:g7
-   `idea:engine-post-wire` — Engine surface: extensions/agi/bin/post_wire.py
    file: extensions/agi/bin/post_wire.py
    parents: goal:g3.1
    children: level3:bin-post-wire
-   `idea:engine-render-context` — Engine surface: extensions/agi/bin/render-context.py
    file: extensions/agi/bin/render-context.py
    parents: goal:g9
    children: level3:bin-render-context
-   `idea:engine-renderers` — Engine surface: extensions/agi/src/renderers
    file: extensions/agi/src/renderers
    parents: goal:g9
    children: level3:src-renderers-ascii, level3:src-renderers-git-diff, level3:src-renderers-init
-   `idea:engine-schema-registry` — Engine surface: extensions/agi/src/schema_registry
    file: extensions/agi/src/schema_registry
    parents: goal:g5
    children: level3:src-schema-registry-active-set, level3:src-schema-registry-cascade, level3:src-schema-registry-dsl
-   `idea:engine-snapshot-build-site` — Engine surface: extensions/agi/bin/snapshot-build-site.py
    file: extensions/agi/bin/snapshot-build-site.py
    parents: goal:g5
    children: level3:bin-snapshot-build-site
-   `idea:engine-snapshot-goals` — Engine surface: extensions/agi/bin/snapshot-goals.py
    file: extensions/agi/bin/snapshot-goals.py
    parents: goal:g5
    children: level3:bin-snapshot-goals
-   `idea:engine-zoom` — Engine surface: extensions/agi/bin/zoom.py
    file: extensions/agi/bin/zoom.py
    parents: goal:g2
    children: level3:bin-zoom

## Your Task
Pick one `idea` node above to extend, fork, or seed a new chain from.
Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).
When done, signal completion:
```
python3 <plugin>/bin/cli.py done 9002 zoom-r1-nobind-2 \
  --verdict <verdict_state> --confidence <0.0-1.0> \
  --node-id <new_node_id> \
  --notes "<one-line>"
```

If stuck >2 attempts → write `pending` verdict and stop.
