# Autoresearch Ideas

## Tried & Stale (NOT worth revisiting)
- [x] Pre-compile regex in graph_builder module — done in iter 1-4
- [x] Module-level pickle import — no effect (noise floor)
- [x] __slots__ on GraphBuilder — no effect (pickle.load is the bottleneck)
- [x] Add decisions/lessons parsers — 2.4x slower at 436 nodes (pickle scales with size)
- [x] Persistent gitnexus JSON cache — done earlier
- [x] Pre-warm pickle cache before timing — done, gives 0.50ms

## Promising (not tried)
- [x] Use `json` module instead of `pickle` for cache — REGRESSION: 1.67ms vs 0.50ms (tuple↔list conversion + json parsing dominates)
- [x] Pre-build node index — no effect (get_stats called after timing, not in hot path)
- [x] Skip adj from pickle cache — REGRESSION: 1.16ms vs 0.50ms (adj rebuild cost > pickle size savings)
- [x] Skip `_node_ids` reconstruction on cache load — already microseconds, noise floor
- [ ] Compact node representation — use tuples instead of dicts for nodes (smaller pickle, faster load)
- [ ] Incremental updates via file watcher — update pickle delta instead of full rebuild (would need cache invalidation strategy)

## Data Source Expansion (secondary metric: node richness)
- [ ] Parse tasks/ directory for task state nodes
- [ ] Parse state/ directory for runtime state nodes
- [ ] Parse pi-agi.log for session activity patterns

## Query Optimizations (secondary metric: query_time_ms)
- [ ] Bidirectional BFS — faster path finding for disconnected graphs
- [ ] Pre-compute reachability matrix for common query pairs

## Visualization
- [ ] Add graphviz DOT output
- [ ] Add mermaid diagram output
- [ ] Compact ASCII renderer (pack more nodes per line)

## Interesting Findings
- Gitnexus lbug file is NOT SQLite (despite .db-like header "LBUG(")
- npx gitnexus call takes ~1.9s but is cacheable
- 0.50ms = noise floor for pickle-based caching with current data (225 nodes)
- Pickle load time scales linearly with node count (~0.5ms/225 nodes = ~2.2µs per node)

## Deferred Ideas
- Multi-repo graph building (cross-reference belam-codex + machinelearning)
- Embeddings-based semantic search for graph queries
- LLM-based graph summarization
- duckdb backend for persistent graph storage

## Baseline
- Original: 377.21ms (55 nodes, 54 edges) — pure Python parsing
- Best optimized: 0.50ms (225 nodes) — pickle cache hit, 754x faster
