---
id: mvp:a00-1467544f-aaaa25
mint_id: d1682de4be33400ea53225e83d90d25a
type: mvp
parents:
  - verdict:a00-1467544f-aaaa25
next_edges:
  - outcome:a00-1467544f-aaaa25
confidence: 0.97
edited_by: season.py
season: 1
subgraph: false
tags:
  - bootstrap
  - mvp
thought_session: season
title: "MVP: Graph density reporter script"
---
**MVP:** `exp-a00-1467544f-aaaa25-hypothesis-task-spawns.py`

A script that:
1. Loads the capillary DAG graph
2. Computes hypothesis→task traversability ratio
3. Reports per-domain density breakdown
4. Emits `METRIC` lines for autoresearch parsing

**Usage:**
```bash
python3 exp-a00-1467544f-aaaa25-hypothesis-task-spawns.py
```

**Output:**
- traversability_ratio
- hypotheses_with_tasks / total_hypotheses
- per-domain breakdown
- baseline find_chains() results

**Purpose:** Baseline measurement of graph density to confirm the capillary DAG has sufficient hypothesis→task edges for chain bootstrapping. Results: 96.77% traversability confirms high density.