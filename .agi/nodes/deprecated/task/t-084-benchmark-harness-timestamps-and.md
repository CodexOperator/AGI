---
id: task:t-084
mint_id: 8c8710b8b0c34aa99a55ac271980ab83
type: task
parents:
  - hyp:autoresearch-tree-skill-r6
acceptance_criteria:
  - R6.3 (each metric value recorded with timestamp and iteration number)
blocked_by:
  - task:t-082
cavekit_req: autoresearch-tree-skill/R6
edited_by: season.py
effort: S
origin: build-site
season: 1
status: deprecated
tags:
  - S
  - tier--1
thought_session: season
tier: -1
title: "T-084: Benchmark harness — timestamps and iteration recording"
---
**Description:** Persist per-iteration metrics at `context/bench/<iteration>.json` with `timestamp`, `iteration`, and the metric dict.

**Files:** `agi-tree/src/skill/bench_recorder.py`, `agi-tree/tests/skill/test_bench_record.py`

**Test Strategy:** Run two iterations; assert two files; each carries the right iteration number and a parseable ISO-8601 timestamp.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R6` under `hyp:autoresearch-tree-skill-r6`, whose disposition is disposition CLOSE-BY-SMALL-EXPERIMENT, not run: `bin/benchmark.py` exists (`idea:engine-benchmark`) but was not confirmed to emit these five metric names; the small experiment is diffing its output fields against the criteria.
<!-- THOUGHT:END -->