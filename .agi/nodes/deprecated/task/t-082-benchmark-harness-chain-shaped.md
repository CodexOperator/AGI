---
id: task:t-082
mint_id: 543f8b6972f844eda225acfd3e9524d5
type: task
parents:
  - hyp:autoresearch-tree-skill-r6
acceptance_criteria:
  - {"R6.1 (per-run metrics": "longest_chain_length"}
  - avg_chain_depth
  - mvp_count
  - outcome_coverage
  - chain_branching_factor)
blocked_by:
  - task:t-056
  - task:t-057
cavekit_req: autoresearch-tree-skill/R6
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-082: Benchmark harness — chain-shaped metrics"
---
**Description:** Implement `bench(graph) -> Metrics` that computes all five metrics. Use chain-engine queries. Add a documented tolerance constant (1e-6) for floating-point comparisons.

**Files:** `agi-tree/src/skill/bench.py`, `agi-tree/tests/skill/test_bench_metrics.py`

**Test Strategy:** Fixture with known-shape graph; assert each metric to expected value. Re-run twice; assert equal within tolerance.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R6` under `hyp:autoresearch-tree-skill-r6`, whose disposition is disposition CLOSE-BY-SMALL-EXPERIMENT, not run: `bin/benchmark.py` exists (`idea:engine-benchmark`) but was not confirmed to emit these five metric names; the small experiment is diffing its output fields against the criteria.
<!-- THOUGHT:END -->
