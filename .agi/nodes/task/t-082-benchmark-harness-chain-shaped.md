---
acceptance_criteria:
  - R6.1 (per-run metrics: longest_chain_length
  - avg_chain_depth
  - mvp_count
  - outcome_coverage
  - chain_branching_factor)
blocked_by:
  - task:t-056
  - task:t-057
cavekit_req: autoresearch-tree-skill/R6
effort: M
id: "task:t-082"
mint_id: 543f8b6972f844eda225acfd3e9524d5
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r6
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-082: Benchmark harness — chain-shaped metrics"
type: task
---

**Description:** Implement `bench(graph) -> Metrics` that computes all five metrics. Use chain-engine queries. Add a documented tolerance constant (1e-6) for floating-point comparisons.

**Files:** `agi-tree/src/skill/bench.py`, `agi-tree/tests/skill/test_bench_metrics.py`

**Test Strategy:** Fixture with known-shape graph; assert each metric to expected value. Re-run twice; assert equal within tolerance.
