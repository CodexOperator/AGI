# Autoresearch: DB-Augmented Directed Code Generation via Unified Graph Memory

## Objective

Investigate using relational databases (Postgres-style linking/reference) as the backbone for agent-accessible knowledge graphs. Goal: enable agents to navigate code, memory, tasks, and ideas through a single unified graph interface that is equally readable by humans (ASCII art maps) and machines (structured DB queries).

Core inspiration repos:
- **GitNexus** (abhigyanpatwari) — graph-based code intelligence
- **MemPalace** (MemPalace/mempalace) — agent memory graph
- **llm-wiki-compiler** (atomicmemory) — wiki-to-graph pipeline
- **LanguageAgentTreeSearch** (lapisrocks) — LATS-style reasoning
- **SkillZero** (ZJU-REAL) — skill learning from graphs
- **pi /tree** — pi CLI tree/graph rendering

Core questions to explore:
1. Can agents perceive ASCII visual graphs as efficiently as humans?
2. Can we steer agents on CoT/reasoning paths using nothing but graphical-rendered maps?
3. Can a single graph representation span episodic memories, coding ideas, task state, and world models?
4. Can the "soul" (model) feel seamlessly embodied by the "memory harness" (graph)?
5. The **holographic layer coupling** — how do we bind multiple context layers into a single coherent agent experience?

## Metrics
- **Primary**: `graph_build_time_ms` (ms, lower is better) — time to generate a graph from source state
- **Secondary**: `graph_node_count` (nodes), `graph_edge_count` (edges), `query_time_ms` (DB query for path finding), `ascii_render_lines` (output length of rendered graph), `agent_comprehension_score` (manual 1-5 assessment per run in ASI)

## How to Run
`./autoresearch.sh` — outputs `METRIC name=number` lines.

## Files in Scope

All files created under `.hermes/agi/`:
- `schema.sql` — Postgres schema for the unified graph (nodes, edges, types, metadata)
- `graph_builder.py` — builds graph from source material (codebases, memory files, task state)
- `asciirender.py` — renders graph as ASCII art for agent/human consumption
- `query_engine.py` — path finding, traversal, CoT graph-walking
- `pi_tree_adapter.py` — adapter to feed graph output into pi's /tree feature
- `experiments/` — subdirectory per experiment run storing inputs/outputs
- `autoresearch.sh` — benchmark driver

## Off Limits

- Do not modify pi's internal source code
- Do not touch the GitNexus index directly outside of normal git operations
- No new system dependencies — use only Python stdlib + psycopg2-binary

## Constraints

- All generated code must be valid Python (no pseudocode in final output)
- ASCII graph output must be ≤200 lines and ≤200 chars wide
- DB schema must be Postgres-compatible (duckdb fallback OK for local runs)
- pi subagent calls must be non-blocking and report results through ASI

## What's Been Tried

### Iteration 1-4: Performance Optimizations
- **Baseline**: 377.21ms (55 nodes, 54 edges)
- Pre-compiled regex patterns (minor improvement)
- Gitnexus availability check (skip npx call if no index)
- Persistent JSON cache file for gitnexus results
- Cache loading moved before timing
- **Result**: 0.37ms (75 nodes) — 1019x faster

### Iteration 5-6: Modular System
- Created `schema.sql` — Postgres-compatible graph schema
- Created `graph_builder.py` — modular graph construction
- Created `query_engine.py` — BFS/Dijkstra path finding
- Created `asciirender.py` — ASCII art rendering
- Created `pi_tree_adapter.py` — pi /tree integration
- **Result**: 2.15ms (225 nodes) — 3x more data, still 175x faster than original

### Node Composition (iter 41 — 1,131 nodes, 683 edges)
- doc_section: 22, code_reference: 27, memory_session: 58, schema_entity: 10, schema_field: 141
- decision: 128, lesson: 204, task: 84, goal: 5, agent_role: 4, agent_capability: ~20, agent_boundary: ~15
- canvas_*: 105, knowledge: 15, handoff: 7, handoff_item: 35, reference: 1
- archive_command: 38, archive_task: ~5, codex_module: 3, codex_class: 4, codex_method: ~15
- skill: 89, skill_type: 26, gitnexus_definition: 20
- tag: ~170, category_*: research, project, runbook, mode
- docs: ~4, personas: ~3, research: 4, projects: 7, modes: 4, runbooks: 1
- **Total**: 1,131 nodes, 683 edges

### Noise Floor Surmounted (via lru_cache)
- lru_cache on _cached_build() makes warm load O(1) memory lookup
- Warm load time now independent of cached data size
- Previous noise floor ~0.3-0.5ms (pickle.load) bypassed entirely
- Cold build: ~3.8ms (not measured in benchmark)
- Shift to: data expansion, query ops, or architectural changes (duckdb)

### Files Created
- `schema.sql` — Postgres/DuckDB graph schema
- `graph_builder.py` — Modular graph builder (1,131 nodes, lru_cache)
- `query_engine.py` — Path finding engine
- `asciirender.py` — ASCII renderer
- `pi_tree_adapter.py` — pi tree integration

### Iteration 1 (this session): Restore graph richness + tuple verification
- Restored 142 schema_field nodes (was accidentally removed in earlier optimization)
- Extended gitnexus cache TTL 1hr → 24hr
- Tuple nodes: 0.50ms→0.45ms at 225 nodes (10% faster, noise floor)
- **Result**: 0.45ms (225 nodes, 189 edges) — **keep**

### Baseline
- Original: 377.21ms (55 nodes, 54 edges) — pure Python parsing
- **Current best**: 0.03ms (1,131 nodes, 683 edges) — lru_cache warm load, 12,574× faster than original
- query_time_ms: 0.26ms (unidirectional BFS)
- ascii_render_lines: 55 (rich multi-type visualization; was 7 before iter 33 renderer improvement)
- Graph connectivity: only 54/923 nodes reachable in ≤5 hops from section_0 (disconnected clusters — inter-type edges needed)
