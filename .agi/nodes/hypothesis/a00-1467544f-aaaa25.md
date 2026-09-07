---
id: hyp:a00-1467544f-aaaa25
mint_id: 9409e1c309b04e569a20f3cfb7f76181
type: hypothesis
parents:
  - idea:domain-bootstrap-discovery
next_edges:
  - exp:a00-1467544f-aaaa25
confidence: 0.7
edited_by: season.py
season: 1
subgraph: false
tags:
  - bootstrap
  - chain-engine
  - graph-core
thought_session: season
title: Hypothesis task-spawns chain bootstrapping
---
**Hypothesis:** Hypothesis nodes that spawn task nodes via the `spawns` relationship create traversable graph paths. Quantifying the hypothesis→task traversability via `spawns_edges` provides a baseline chain-bootstrapping metric. If ≥70% of hypotheses spawn ≥1 task, the graph has sufficient density to bootstrap chains once `next_edges` and experiment/verdict/app_purpose nodes are added.

**What would prove it:** ≥70% of hypothesis nodes have at least one task child via `spawns` (task.parents → hypothesis). This means the capillary DAG has dense enough branching to support multi-hop chains after experiment nodes are added.

**What would disprove it:** <30% of hypothesis nodes have task children. The graph is too sparse — chain bootstrapping requires seeding experiments manually rather than deriving them from tasks.

---

**Experiment:** Measure hypothesis→task traversability in the current graph.

1. Load the full graph (nodes/)
2. For each hypothesis node, find all task children (tasks whose `parents` includes the hypothesis id)
3. Count: total hypotheses, hypotheses with ≥1 task child, total hypothesis→task edges
4. Compute: traversability_ratio = hypotheses_with_tasks / total_hypotheses
5. Create `next_edges` from each hypothesis to its first task child (simulating experiment node addition)
6. Re-measure find_chains() longest chain length

**Metric:** `hypothesis_task_traversability_ratio` (fraction of hypotheses that spawn tasks)

**Pass threshold:** ≥ 0.70 (70% of hypotheses have task children)