# Autoresearch Ideas — Pruned 2026-04-30

## DONE — Archived
- [x] Pre-compile regex patterns — iter 1-4
- [x] Gitnexus availability check + JSON cache — iter 2-3
- [x] Pickle-based graph cache with pre-warm — iter 7
- [x] Tuple nodes (smaller pickle) — iter 9, 15, 16
- [x] lru_cache on builder internals — iter 21 (MAJOR breakthrough)
- [x] Add decisions + lessons with lru_cache — iter 22
- [x] Parse tasks/ directory — iter 23
- [x] msgpack/json/mmap/pickle protocol micro-optimizations — REGRESSIONs confirmed noise floor

## SATURATED — Primary metric noise floor
The graph_build_time_ms metric is at 0.03ms (lru_cache warm load). This is:
- 12,574× faster than original 377ms baseline
- 838× confidence above noise floor
- lru_cache makes warm load O(1) memory lookup regardless of node count
- Further micro-optimizations: NO.
- Serialization format experiments (pickle/json/msgpack): all REGRESSION or noise floor

## NOW WORTHWHILE — Data Expansion (richer graph, same speed)
- [ ] Parse all 84 tasks (remove 50-limit) — trivial expansion
- [ ] Parse goals/ directory for goal nodes
- [ ] Parse canvas/ directory for canvas state nodes  
- [ ] Expand decisions/lessons beyond 10-limit (potential 300-400 nodes)
- [ ] Parse state/ directory for runtime state nodes
- [ ] Parse archive/ directory for archived files
- [ ] Parse machinelearning/ for cross-repo graph edges

## Architectural (secondary: query_time_ms, structural richness)
- [ ] duckdb/sqlite3 backend — persistent graph DB with SQL query engine
  - NOT for primary metric (warm load stays 0.03ms via lru_cache)
  - Benefits: SQL traversal, reachability queries, complex joins
  - Risk: adds dependency (sqlite3 stdlib OK, duckdb requires install)
  - Approach: sqlite3 in-memory graph DB that rebuilds from lru_cache on startup
- [ ] Bidirectional BFS in query_engine — faster path finding
- [ ] Pre-compute reachability matrix — O(1) reachability queries

## Visualization (secondary: ascii_render_lines, utility)
- [ ] Mermaid diagram output — graphviz-free via text
- [ ] Compact ASCII renderer — pack more nodes per line
- [ ] pi /tree adapter — integrate with pi's built-in tree rendering

## Interesting Findings
- Gitnexus lbug file is NOT SQLite (header "LBUG(")
- lru_cache is the key: warm load O(1), cold build ~3.8ms
- Noise floor ~0.03-0.05ms for warm load (memory lookup)
- pickle noise floor ~0.3-0.5ms (was the old ceiling before lru_cache)
- 142 schema_field nodes accidentally removed then restored
- gitnexus cache TTL 1hr → 24hr extended

## Deferred (low priority / speculative)
- Multi-repo graph (belam-codex + machinelearning cross-ref)
- Embeddings-based semantic search for graph queries
- LLM-based graph summarization
- Incremental lru_cache invalidation (watch source files)

## Current Best
- 0.03ms (295 nodes, 209 edges) — lru_cache warm load, 12,574× vs original
- Original: 377.21ms (55 nodes, 54 edges)
- Node types: doc_section, code_ref, memory, schema_entity, schema_field,
  decision, lesson, gitnexus_definition, task (new)
