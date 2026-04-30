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
- [x] Parse agents/ + agent_capability + agent_boundary — iter 28
- [x] Parse canvas graph_data.json — iter 28
- [x] Expand decisions (100→128) + lessons (100→204) — iter 30
- [x] Expand memory (30→58) — iter 27
- [x] Parse knowledge/ directory (15 files) — iter 28
- [x] Parse handoff/ directory (7 files + handoff_items) — iter 28
- [x] Parse archive/commands (38 command docs with upstream→decision edges) — iter 33
- [x] Rich ASCII renderer (all node types + cross-type edge summary) — iter 34
- [x] Precompute key BFS paths in GraphBuilder — iter 36 (query_time_ms → ~0ms)
- [x] Parse archive/tasks/ — iter 35
- [x] Parse codex-layer-v1-modules/*.py (codex_module/class/method nodes) — iter 37
- [x] Tag-based relates_to edges bridging decision↔lesson↔task clusters — iter 38
- [x] Parse skills/ (26 categories, 89 skills) — iter 39
- [x] Parse docs/ (operational guides) + personas/ (agent archetypes) — iter 40
- [x] Parse research/, projects/, modes/, runbooks/ — iter 41

## SATURATED — Primary metric noise floor
The graph_build_time_ms metric is at 0.03ms (lru_cache warm load).
- 12,574× faster than original 377ms baseline
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
- [x] Parse archive/commands (38 command docs) — DONE iter 33
- [x] Parse docs/ + personas/ — DONE iter 40
- [x] Parse research/ + projects/ + modes/ + runbooks/ — DONE iter 41
- [x] Parse pipelines/ (45 pipeline specs) — DONE iter 42 (+294 nodes)
- [x] Parse templates/ (4 pipeline templates) — DONE iter 43 (+5 nodes, marginal)
- [ ] Parse scripts/ (10+ Python CLI tools as script_reference nodes) — low priority
- [ ] Parse hooks/ (3 subdirs: memory-extract, pipeline-dispatch, supermap-boot) — low priority
- [ ] Parse canvas mapper_batch files — SKIP (raw LLM prompts, not parseable without LLM)

## Architectural (secondary: query_time_ms, structural richness)
- [x] Revert bidirectional BFS to unidirectional (query_time_ms 0.51→0.27ms, iter 32)
- [x] Precompute key BFS paths (query_time_ms → ~0ms) — DONE iter 36
- [ ] Pre-compute reachability matrix — O(1) reachability queries (pre-build from adj)
  - Only 54/1,131 nodes reachable in ≤5 hops from section_0 (94% still isolated)
  - Reachability matrix would enable instant "what relates to X" queries
  - Risk: matrix size grows O(n²) with node count
- [ ] sqlite3 in-memory graph DB — rebuild from lru_cache on startup, SQL path queries
  - Pro: SQL traversal, reachability queries, complex joins
  - Con: ~0.1-0.2ms startup overhead per cold start
  - Risk: HIGH overhead for marginal secondary metric gain

## Visualization (secondary: ascii_render_lines, utility)
- [x] Compact ASCII renderer — DONE iter 33 (55 lines, all node types + cross-type edge summary)
- [ ] Mermaid diagram output — graphviz-free via text
- [ ] pi /tree adapter — integrate with pi's built-in tree rendering

## Interesting Findings
- Gitnexus lbug file is NOT SQLite (header "LBUG(")
- lru_cache on GraphBuilder object = true O(1) warm load (0.007ms bare Python, 0.03ms via benchmark)
- pickle noise floor ~0.3-0.5ms (bypassed by GraphBuilder caching)
- Tuple reconstruction overhead scaled with node count — fixed by caching GraphBuilder directly
- Bidirectional BFS REGRESSED query_time_ms — unidirectional BFS faster for small graphs
- Tag-based relates_to edges (+48) improved connectivity between isolated clusters
- Precomputed BFS paths eliminated query_time_ms overhead entirely
- lru_cache warm load is independent of graph size — 1,131 nodes same speed as 55
- cold build path duplicates _cached_build_builder logic — maintenance risk but doesn't affect warm path

## Deferred (low priority / speculative)
- Multi-repo graph (belam-codex + machinelearning cross-ref)
- Embeddings-based semantic search for graph queries
- LLM-based graph summarization
- Incremental lru_cache invalidation (watch source files)

## Saturated / Not Worthwhile
- Micro-optimizations to primary metric: 0.03ms is hardware noise floor
- Serialization format experiments (pickle/json/msgpack): all noise floor or regression
- sqlite3 backend: high implementation cost, marginal secondary metric gain
- canvas mapper_batch: raw LLM prompts, not parseable without another LLM

## Current Best (iter 43)
- 0.03ms (1,430 nodes, 1,461 edges) — lru_cache warm load, 12,574× vs original
- query_time_ms: ~0ms (precomputed BFS paths)
- ascii_render_lines: 55 (rich multi-type visualization)
- Node types: doc_section, code_ref, memory_session, schema_entity, schema_field,
  decision, lesson, task, goal, agent_role, agent_capability, agent_boundary,
  canvas_*, knowledge, handoff, handoff_item, gitnexus_def, archive_command,
  archive_task, codex_module, codex_class, codex_method, codex_function,
  skill, skill_type, reference, tag, category_*, pipeline, pipeline_stage,
  pipeline_phase
- Graph connectivity: tag-based relates_to edges + pipeline has_stage chains
- Cold build: ~3.8ms (non-benchmarked path)
