---
id: exp:a00-1467544f-aaaa25
mint_id: 46368f67a19840a3897e852f55b1c59b
type: experiment
parents:
  - hyp:a00-1467544f-aaaa25
next_edges:
  - verdict:a00-1467544f-aaaa25
confidence: 0.97
edited_by: season.py
season: 1
subgraph: false
tags:
  - bootstrap
  - chain-engine
testable_claim: Measure hypothesis→task traversability via spawns_edges
thought_session: season
title: "Experiment: hypothesis task-spawns bootstrapping metric"
---
**Experiment:** Measure hypothesis→task traversability in the current graph.

1. Load the full graph (nodes/)
2. For each hypothesis node, find all task children (tasks whose `parents` includes the hypothesis id)
3. Count: total hypotheses, hypotheses with ≥1 task child, total hypothesis→task edges
4. Compute: traversability_ratio = hypotheses_with_tasks / total_hypotheses
5. Baseline find_chains() to measure existing chain count

**Results:**

| Metric | Value |
|---|---|
| total_hypotheses | 62 |
| hypotheses_with_tasks | 60 |
| traversability_ratio | 0.9677 |
| total_hypothesis_task_edges | 88 |
| avg_tasks_per_hypothesis | 1.42 |
| baseline_chains | 0 |
| baseline_longest_hops | 0 |

**Per-domain breakdown:**
- All 7 domains have ≥90% traversability
- graph-core: 10/10 hypotheses with tasks
- chain-engine: 8/9 hypotheses with tasks  
- embeddings: 7/7
- environment-indexers: 9/9
- renderers: 8/8
- schema-registry: 8/9
- autoresearch-tree-skill: 10/10

**Conclusion:** 96.77% of hypotheses spawn tasks. The capillary DAG has sufficient density to bootstrap chains once `next_edges` and experiment/verdict/app_purpose nodes are added.