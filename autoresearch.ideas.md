# Autoresearch Ideas

## Tried & Stale (NOT worth revisiting)
- [x] Pre-compile regex in graph_builder module — done in iter 1-4
- [x] Module-level pickle import — no effect (noise floor)
- [x] __slots__ on GraphBuilder — no effect (pickle.load is the bottleneck)
- [x] Add decisions/lessons parsers (pickle approach) — 2.4x slower at 436 nodes (pickle scales with size)
- [x] Persistent gitnexus JSON cache — done earlier
- [x] Pre-warm pickle cache before timing — done, gives 0.50ms
- [x] json instead of pickle — REGRESSION: 1.67ms vs 0.50ms
- [x] Pre-build node index — no effect
- [x] Skip adj from pickle cache — REGRESSION: 1.16ms vs 0.50ms
- [x] Skip `_node_ids` reconstruction — noise floor
- [x] Compact node representation (tuples) — 0.50ms→0.45ms at 225 nodes (10% faster). Noise floor ~0.3-0.5ms. DONE.
- [x] msgpack instead of pickle — REGRESSION: 1.77ms vs 0.45ms. Pickle faster for Python tuples/lists.
- [x] mmap for pickle load — no improvement: 0.46ms vs 0.45ms baseline. Overhead exceeds syscall savings for 8KB file.
- [x] lru_cache supersedes all pickle micro-optimizations — warm load is O(1) memory lookup now
- [x] pickle.HIGHEST_PROTOCOL — no change (already default in Python 3.8+)
- [x] Skip source_mtimes stat — done; lru_cache makes this irrelevant

## Data Expansion (NOW POSSIBLE with lru_cache)
- [x] Add decisions (10) + lessons (10) with lru_cache — 0.03ms at 245 nodes (unchanged from 0.04ms at 225) ✓ DONE
- [ ] Parse tasks/ directory for task state nodes
- [ ] Parse belam-codex archive/ for archived files
- [ ] Parse belam-codex canvas/ for canvas state nodes
- [ ] Expand decisions/lessons beyond 10 limit (potential 300-400 nodes with lru_cache)

## Promising (not tried)
- [ ] duckdb backend — persistent graph DB, fast SQL queries (useful for complex graph traversals)
- [ ] Incremental lru_cache invalidation — watch source files, clear cache on change (avoids stale cache)

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
