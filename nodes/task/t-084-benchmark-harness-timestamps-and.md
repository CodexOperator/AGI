---
acceptance_criteria:
  - R6.3 (each metric value recorded with timestamp and iteration number)
blocked_by:
  - task:t-082
cavekit_req: autoresearch-tree-skill/R6
effort: S
id: "task:t-084"
mint_id: 8c8710b8b0c34aa99a55ac271980ab83
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r6
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-084: Benchmark harness — timestamps and iteration recording"
type: task
---

**Description:** Persist per-iteration metrics at `context/bench/<iteration>.json` with `timestamp`, `iteration`, and the metric dict.

**Files:** `agi-tree/src/skill/bench_recorder.py`, `agi-tree/tests/skill/test_bench_record.py`

**Test Strategy:** Run two iterations; assert two files; each carries the right iteration number and a parseable ISO-8601 timestamp.
