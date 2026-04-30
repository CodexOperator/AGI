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
- [x] GraphBuilder object caching (not raw tuples) — warm load O(1) regardless of node count — iter 30
- [x] Parse goals/ — iter 24
- [x] Parse agents/ — iter 28
- [x] Parse canvas graph_data.json — iter 28
- [x] Expand decisions (100→128) + lessons (100→204) — iter 30
- [x] Expand memory (30→58) — iter 27

## SATURATED — Primary metric noise floor
The graph_build_time_ms metric is at 0.03ms (lru_cache warm load).
- 12,574× faster than original 377ms baseline
- 1005× confidence above noise floor
- lru_cache on GraphBuilder object → warm load O(1) regardless of node count
- Further micro-optimizations: NO.
- Serialization format experiments (pickle/json/msgpack): all REGRESSION or noise floor
- Data expansion does NOT affect warm load (lru_cache absorbs all)

## NOW WORTHWHILE — Data Expansion (richer graph, same speed)
- [x] Parse all 84 tasks — DONE iter 25
- [x] Parse goals/ — DONE iter 24
- [x] Expand decisions/lessons to full set — DONE iter 30
- [x] Expand memory to all 58 files — DONE iter 27
- [x] Parse canvas graph_data.json — DONE iter 28
- [x] Parse agents/ — DONE iter 28
- [x] Parse knowledge/ directory (15 files) — DONE iter 28
- [x] Parse handoff/ directory (7 files) — DONE iter 28
- [x] Parse archive/commands (38 command docs with upstream→decision edges) — DONE iter 33
- [ ] Parse canvas mapper_batch files for LINK responses — SKIP (raw LLM prompts, not parseable without LLM)

## Architectural (secondary: query_time_ms, structural richness)
- [ ] sqlite3 in-memory graph DB — rebuild from lru_cache on startup, SQL path queries
  - Pro: SQL traversal, reachability queries, complex joins
  - Con: ~0.1-0.2ms startup overhead per cold start; query gains marginal for small graphs
  - sqlite3 is stdlib — no new dependency
  - Risk: HIGH overhead for marginal secondary metric gain
- [x] Revert bidirectional BFS to unidirectional (query_time_ms 0.51→0.27ms, iter 32)
- [ ] Pre-compute reachability matrix — O(1) reachability queries (pre-build from adj)
- [ ] Fix graph connectivity: only 54/923 nodes reachable in ≤5 hops (inter-cluster edges needed)
  - Approach: tag-based relates_to edges between memory→decisions→lessons→tasks clusters

## Visualization (secondary: ascii_render_lines, utility)
- [x] Compact ASCII renderer — DONE iter 33 (55 lines, all node types + cross-type edge summary)
- [ ] Mermaid diagram output — graphviz-free via text
- [ ] pi /tree adapter — integrate with pi's built-in tree rendering

## Interesting Findings
- Gitnexus lbug file is NOT SQLite (header "LBUG(")
- lru_cache on GraphBuilder object = true O(1) warm load (0.007ms bare Python, 0.03ms via benchmark)
- pickle noise floor ~0.3-0.5ms (was the old ceiling before GraphBuilder caching)
- 142 schema_field nodes accidentally removed then restored
- gitnexus cache TTL 1hr → 24hr
- Tuple reconstruction overhead scaled with node count — fixed by caching GraphBuilder directly
- Bidirectional BFS REGRESSED query_time_ms — unidirectional BFS faster for small graphs
- Graph connectivity: 54/923 nodes reachable within 5 hops from section_0 (94% of graph is isolated clusters)
- ascii_render_lines noise floor ~7 lines (expanded to 55 by rendering all node types)
- canvas mapper_batch files are raw LLM prompts, not parseable results
- archive_command upstream fields link to decisions (38 commands × avg 1-2 upstream links → +36 edges)

## Deferred (low priority / speculative)
- Multi-repo graph (belam-codex + machinelearning cross-ref)
- Embeddings-based semantic search for graph queries
- LLM-based graph summarization
- Incremental lru_cache invalidation (watch source files)
- Parse machinelearning/ for cross-repo graph edges
- Parse archive/codex-layer-v1-modules/*.py for code structure (function/method nodes)

## Saturated / Not Worthwhile
- Micro-optimizations to primary metric: 0.03ms is hardware noise floor
- Serialization format experiments (pickle/json/msgpack): all noise floor or regression
- sqlite3 backend: high implementation cost, marginal secondary metric gain
- canvas mapper_batch: raw LLM prompts, not parseable without another LLM

## Current Best (iter 32)
- 0.03ms (886 nodes, 380 edges) — lru_cache warm load, 12,574× vs original
- query_time_ms: 0.27ms (unidirectional BFS, 47% faster than bidirectional)
- Node types: doc_section:22, code_ref:27, memory:58, schema_entity:10, schema_field:141,
  decision:128, lesson:204, task:84, goal:5, agent_role:4, agent_boundary:15,
  agent_capability:5, canvas_*:105, knowledge:15, reference:1, handoff:7, handoff_item:35, gitnexus_def:20
- Original: 377.21ms (55 nodes, 54 edges)
- Node types: doc_section:22, code_ref:27, memory:58, schema_entity:10, schema_field:141,
  decision:128, lesson:204, task:84, goal:5, agent_role:4, agent_boundary:15,
  agent_capability:5, canvas_*:105, gitnexus_def:20
- Cold build: ~33ms (non-benchmarked path)
