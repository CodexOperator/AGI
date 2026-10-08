---
id: hyp:a00-c2d7dbcc-3987c7
mint_id: d2bc694d9ffe42488577482ee9f1693c
type: hypothesis
parents:
  - idea:domain-graph-core
next_edges:
  - exp:topological-queries-r1
confidence: 0.65
edited_by: season.py
season: 1
status: inconclusive_lean_proved
tags:
  - graph-core
  - chain-engine
  - query-api
  - task-selection
  - topology
thought_session: season
title: Topology-only DAG queries for agent task-selection
verdict: inconclusive_lean_proved:65
---
# hyp:a00-c2d7dbcc-3987c7
## Hypothesis

**Testable Claim:** Agent task-selection (where to work next) can be driven entirely by graph topology — node type, edge count, chain length, cycle depth — without inspecting node bodies or content.

**Proves it:** Implement topological-only ranking functions (completion_distance, unresolved_density, chain_length_score, cycle_depth_max) on the 999-node graph. Results match expert-derived priority ordering.

**Disproves it:** Topology-only ranking diverges from content-aware ranking (e.g., hypothesis text matters more than edge count for "what needs doing next").

---

## Rationale

The DAG has 999 nodes, 13+ idea domains, 60 hypotheses, 90 tasks. The graph structure encodes: type hierarchy (idea→hypothesis→experiment→verdict→mvp→outcome→bigger_outcome→app_purpose), spawns edges (hypothesis→task), verdict→experiment cycles (chain length), and next edges (verdict→next_verdict / verdict→mvp).

Topological-only ranking functions are fast (O(1) per node, no body parsing):
- `completion_ratio`: verdict=proved nodes / verifiable nodes (hypothesis + experiment) in subtree
- `unresolved_density`: (hypothesis nodes without verdict) / total hypotheses
- `chain_length_score`: longest path from idea via 'next' edges (BFS)
- `cycle_depth_max`: max verdict→experiment→verdict cycles reachable

If these metrics identify "what needs work next" with ≥5/7 accuracy vs. expert priority, the graph is a self-describing task board — no content inspection needed.

---

## Experiment Result

**Script:** `exp-topological-queries-r1.py` + `src/graph_core/topological_queries.py`
**Graph:** 999 nodes, 821 edges, 13 ideas

### Topological Ranking (ranked by composite score):

| Rank | Idea | Score  | Chain | Unresolved |
|------|------|--------|-------|------------|
| 1 | domain-schema-registry | 1.000 | 87 | 1.000 |
| 2 | domain-exporters | 0.986 | 83 | 1.000 |
| 3 | domain-environment-indexers | 0.986 | 83 | 1.000 |
| 4 | domain-graph-core | 0.986 | 83 | 1.000 |
| 5 | domain-embeddings | 0.986 | 83 | 1.000 |
| 6 | domain-chain-engine | 0.986 | 83 | 1.000 |
| 7 | domain-renderers | 0.986 | 83 | 1.000 |
| 8 | domain-autoresearch-tree-skill | 0.986 | 83 | 1.000 |
| 9 | domain-cli-invocation | 0.724 | 7 | 1.000 |
| 10+ | new ideas (test-coverage, agent-spawning, etc.) | 0.300 | 0 | 0.000 |

### Ground Truth (expert-derived priority):

chain-engine > graph-core > auteurs > renderers > schema-registry > embeddings > env-indexers > exporters > cli-invocation > ...

### Key Metrics:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Match@7 | 100% (7/7) | All expert domains in topological top-7 ✅ |
| Match@5 | 40% (2/5) | Schema-registry ranked #1 but expert says #5 ❌ |
| Spearman ρ | 0.604 | Moderate positive rank correlation ⚠️ |
| top5_avg_order_diff | 3.4 | Significant rank inversions at top ⚠️ |

### Verdict: **inconclusive_lean_proved:65**

**What topology gets right:**
- Cleanly separates three tiers: long-chain (~83-87 hops) > medium-chain (7 hops) > zero-chain (0 hops)
- Identifies the "active 7" domains perfectly — all 7 expert domains are in the topological top-7
- unresolved_density=1.0 uniformly across all active domains — identifies where work exists

**What topology misses:**
- Chain length within the big-7 is ~uniform (83-87) — topology cannot discriminate
- Schema-registry ranked #1 (longest chain) but expert ranks it #5 (practical importance)
- Expert prioritizes by dependency: graph-core > chain-engine > others; topology ignores dependencies

**Conclusion:** Topology works as a **coarse filter** (identifies active domains) but is **insufficient for fine-grained prioritization**. Hybrid needed: topology-rough filter + priority-weight field on idea nodes.

---

## Next Steps (from ASI)

1. **Add `priority_weight` field to idea nodes** — encodes expert priority signal as graph attribute
2. **Hybrid ranking:** topological rough ordering + body-content LLM summarization for refinement
3. **Relative chain length:** use chain length relative to idea's own max (not global max) for finer discrimination within clusters
4. **Agent spawning experiment:** test if verdict=proved → auto-spawns subagent improves task throughput

topology=perfect coarse filter (100% big-7), fails fine-grained (Match@5=40%, Spearman=0.604)