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
- [x] Parse docs/ + personas/ — iter 40
- [x] Parse research/ + projects/ + modes/ + runbooks/ — iter 41
- [x] Pre-compute hub reachability matrix (32 hub nodes, O(1) reachability queries) — iter 44
- [x] Parse templates/ (4 pipeline templates + template_stage rich metadata) — iter 45
- [x] Parse hooks/ (3 hook defs: memory-extract, pipeline-dispatch, supermap-boot) — iter 46
- [x] Parse scripts/ (~40 Python CLI tools + script_function/class child nodes) — iter 46
- [x] ASCII renderer shows hook/script/pipeline nodes + script→pipeline bridges — iter 47

## SATURATED — Primary metric noise floor
The graph_build_time_ms metric is at 0.03-0.04ms (lru_cache warm load).
- ~9,400× faster than original 377ms baseline
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
- [x] Parse templates/ (4 pipeline templates + template_stage) — DONE iter 45
- [x] Parse hooks/ (3 hook defs) — DONE iter 46
- [x] Parse scripts/ (~40 Python CLI tools) — DONE iter 46
- [ ] Parse canvas mapper_batch files — SKIP (raw LLM prompts, not parseable without LLM)

## Architectural (secondary: query_time_ms, structural richness)
- [x] Revert bidirectional BFS to unidirectional (query_time_ms 0.51→0.27ms, iter 32)
- [x] Precompute key BFS paths (query_time_ms → ~0ms) — DONE iter 36
- [x] Pre-compute hub reachability matrix (32 hub nodes) — DONE iter 44
- [ ] sqlite3 in-memory graph DB — rebuild from lru_cache on startup, SQL path queries
  - Pro: SQL traversal, reachability queries, complex joins
  - Con: ~0.1-0.2ms startup overhead per cold start
  - Risk: HIGH overhead for marginal secondary metric gain
- [ ] Cold build as secondary metric — measure cold build time as separate benchmark

## Visualization (secondary: ascii_render_lines, utility)
- [x] Compact ASCII renderer — DONE iter 33 (55 lines)
- [x] ASCII renderer shows all node types (hook/script/pipeline/skill/reference) — DONE iter 47 (72 lines)
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
- script→pipeline operates_on bridges link CLI tools to pipeline ecosystem

## Small Wins (each <0.5ms, cumulative ~2-3ms)
- [ ] Move inline regex compilations to class level: parse_pipelines (4 patterns), parse_codex_modules (6 patterns), parse_templates (4 patterns), parse_scripts (4 patterns). Each compile is negligible but 18 patterns × compilation time adds ~1-2ms to cold build.

## Deferred (low priority / speculative)
- Multi-repo graph (belam-codex + machinelearning cross-ref)
- Embeddings-based semantic search for graph queries
- LLM-based graph summarization
- Incremental lru_cache invalidation (watch source files)
- hook_reference → decision edges (which decisions trigger which hooks)

## Saturated / Not Worthwhile
- Micro-optimizations to primary metric: 0.03ms is hardware noise floor
- Serialization format experiments (pickle/json/msgpack): all noise floor or regression
- sqlite3 backend: high implementation cost, marginal secondary metric gain
- canvas mapper_batch: raw LLM prompts, not parseable without another LLM

## Current Best (iter 1068)
- 0.03ms warm (1,681 nodes, 1,782 edges) — lru_cache, noise floor
- Cold build: ~130ms (benchmarked path via _benchmark.py)
- query_time_ms: ~0.08ms (BFS first→last section, unidirectional)
- ascii_render_lines: 106 (all node types)
- Cold build optimized: 146.33ms → 125.95ms (-13.9%) by eliminating build_tag_bridges double-read of 416 decision/lesson/task files. Tags are now collected in `_tag_store` during initial parse and reused rather than re-read from source files.
- 4.7× noise floor confidence

## Open (thoughtgraph)
- [ ] goal:s28 follow-up: manifest merge in dispatch.py is a non-atomic read-modify-write cycle. Process-level race test (8 concurrent workers, exact sequence) lost 1/8 entries in 3/6 runs, plus a FileNotFoundError crash from the shared fixed tmp name `.manifest.json.tmp` — in real dispatch that crash means a spawned-but-untracked agent (Popen ran, manifest entry never landed, heal cannot see it). Fix direction: flock on a lockfile around the read-merge-write, or per-agent manifest files. Measured 2026-09-02, iter 101, parent a00-dea93ac5.
- [ ] test_provisioning.py TTL failure: `test_a_minted_key_is_capped_and_expires_and_can_be_revoked` fails deterministically in isolation (17/18 pass); `test_mint_refuses_to_hand_out_a_key_with_no_ttl` fails intermittently (full suite 1379/1381 on 2026-09-03, iter 1006, parent a02-ccfcf794 review of kid a00-dc761315). One of the kid's notes claimed 1381/1381 — corrected. Looks like a real TTL/clock defect in provisioning, not flake.
- [ ] **L4 goal-coverage metric (the honest form of goal-fulfilment scoring).** Measured 2026-09-03, iter 1006, parent a03-2a508dc0 (re-audit of kids' `outcome_coverage` gap experiments under `hypothesis:a01-8e09cdf2-6c63ec`). Walk-up through each outcome's `parents:` on the real corpus: **19 of 23 outcome nodes terminate at an `idea:domain-*` node that has no `parents:` field, and none of the 14 `domain-*` ideas connects to any goal** — so `outcome_coverage` is measuring *outcome-reach*, not goal-fulfilment. Only 4/23 outcomes' chains reach a `goal:` node. The current `outcome_coverage` proxy (mvps/hypotheses) never asked "does this outcome's chain reach a goal?". Proposed metric: `goal_coverage` = fraction of outcomes whose parent chain resolves to a live goal. This is L4's real gap and is gameable-resistant (splicing hops between two goal-less halves changes nothing). A kid's sibling experiment overclaimed `proved` on a `0/23` number from a wrong-edge-direction method (looked for forward `next_edges` refs, ignored the outcome's own `parents:`) — demoted; see `experiment:a01-5a8f6fc8-3e72b6`.
- [ ] **dispatch.py `_node_type_for` keys the small-zoom step table on the full type name, but experiments are minted with the `exp:` id prefix.** So `--target exp:...` (68 corpus experiments use `exp:`) falls through to the `"hypothesis"` default instead of scaffolding a `verdict`. Confirmed 2026-09-03 (iter 1006, parent a03): `step.get('exp'...)` → `hypothesis`, not `verdict`. Fix: resolve the target's declared `type:` from frontmatter rather than the id prefix, or add `"exp" -> "verdict"` (and any other short prefixes) to the step table. Currently a parent aiming an experiment at an `exp:` node silently gets a hypothesis scaffold, which is why I had to aim at the `hypothesis:` node instead to get an experiment.
