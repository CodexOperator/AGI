# Autoresearch Ideas

## Tried & Stale (NOT worth revisiting)
- [x] Pre-compile regex in graph_builder module — done in iter 1-4
- [x] Module-level pickle import — no effect (noise floor)
- [x] __slots__ on GraphBuilder — no effect (pickle.load is the bottleneck)
- [x] Add decisions/lessons parsers — 2.4x slower at 436 nodes (pickle scales with size)
- [x] Persistent gitnexus JSON cache — done earlier
- [x] Pre-warm pickle cache before timing — done, gives 0.50ms
- [x] json instead of pickle — REGRESSION: 1.67ms vs 0.50ms
- [x] Pre-build node index — no effect
- [x] Skip adj from pickle cache — REGRESSION: 1.16ms vs 0.50ms
- [x] Skip `_node_ids` reconstruction — noise floor
- [x] Compact node representation (tuples) — 0.50ms→0.45ms at 225 nodes (10% faster). Noise floor ~0.3-0.5ms. DONE.
- [x] msgpack instead of pickle — REGRESSION: 1.77ms vs 0.45ms. Pickle faster for Python tuples/lists.

## Promising (not tried)
- [ ] Incremental pickle updates via file watcher — delta patching vs full rebuild
- [ ] duckdb backend — persistent graph DB, fast SQL queries, avoids pickle entirely

## Data Source Expansion (secondary metric: node richness, ~225→400+ nodes)
- [ ] Parse tasks/ directory for task state nodes
- [ ] Parse state/ directory for runtime state nodes
- [ ] Parse belam-codex decisions/ for decision nodes (limit to 10)
- [ ] Parse belam-codex lessons/ for lesson nodes (limit to 10)

## Query Optimizations (secondary metric: query_time_ms)
- [ ] Bidirectional BFS — faster path finding for disconnected graphs
- [ ] Pre-compute reachability matrix for common query pairs

## Visualization
- [ ] Add mermaid diagram output
- [ ] Compact ASCII renderer (pack more nodes per line)

## Interesting Findings
- Gitnexus lbug file is NOT SQLite (despite .db-like header "LBUG(")
- npx gitnexus call takes ~1.9s but is cacheable
- **Noise floor confirmed**: ~0.3-0.5ms for pickle.load at 225 nodes
- Pickle load time scales linearly with node count (~0.5ms/225 nodes = ~2.2µs/node)
- 142 schema_field nodes were accidentally removed in earlier optimization; restored
- gitnexus cache TTL was 1hr (too short); extended to 24hr

## Deferred Ideas
- Multi-repo graph building (belam-codex + machinelearning cross-ref)
- Embeddings-based semantic search for graph queries
- LLM-based graph summarization
- pi /tree adapter integration for graph viz

## Current Best
- 0.45ms (225 nodes, 189 edges) — tuple nodes + pickle cache + schema_field nodes restored
- 0.32ms (84 nodes) — shorter TTL, fewer nodes, NOT comparable
- Original baseline: 377.21ms (55 nodes, 54 edges) — 838x faster
