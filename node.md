---
id: outcome:a00-1467544f-aaaa25
mint_id: f3fd1545cc4d4d06814bf86d5cf2e0b2
type: outcome
parents:
  - mvp:a00-1467544f-aaaa25
next_edges:
  - bigger_outcome:a00-1467544f-aaaa25
confidence: 0.97
edited_by: season.py
judged_against: goal:g4.6
lens: goal:g4
season: 1
subgraph: false
tags:
  - bootstrap
  - outcome
thought_session: season
title: "Outcome: Graph density baseline measured"
---
**Input shape:** Capillary DAG at nodes/ (157 nodes: 60 hypotheses, 7 ideas, 90 tasks)

**Output shape:** Metrics dict:
- `traversability_ratio`: float (0.9677)
- `hypotheses_with_tasks`: int (60/62)
- `total_hypothesis_task_edges`: int (88)
- `avg_tasks_per_hypothesis`: float (1.42)
- `baseline_chains`: int (0)
- `baseline_longest_hops`: int (0)

**Behavior:** Loads graph, computes traversability, emits METRIC lines for autoresearch.

**Edge cases:**
- Empty graph → traversability_ratio = 0.0, verdict = disproved
- All hypotheses have tasks → traversability_ratio = 1.0, verdict = proved
- Mixed domain coverage → per-domain breakdown shows which domains need seeding

**Key finding:** 96.77% hypothesis→task traversability. The bottleneck is NOT graph density — it's missing `next_edges`, `app_purpose` nodes, and intermediate chain types.

**Next:** Use this metric to prioritize which hypotheses to seed with experiment/verdict chains first.