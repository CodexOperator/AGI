---
id: hyp:autoresearch-tree-skill-r6
mint_id: 0c26d88ca65548f98a1caef7e347b587
type: hypothesis
parents:
  - idea:domain-autoresearch-tree-skill
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - autoresearch-tree-skill
  - R6
testable_claim: Benchmark Harness Extension
thought_session: L1.09
title: "autoresearch-tree-skill/R6: Benchmark Harness Extension"
---
**Description:** A benchmark harness extends the predecessor project's harness with new chain-shaped metrics. The new metrics are measured per run.

**Acceptance Criteria:**
- [ ] The harness produces, per run, the metrics `longest_chain_length`, `avg_chain_depth`, `mvp_count`, `outcome_coverage`, and `chain_branching_factor`
- [ ] `outcome_coverage` is defined as the fraction of `bigger_outcome` nodes traceable to at least one `mvp` node and is reported as a number between 0.0 and 1.0
- [ ] Each metric value is recorded with a timestamp and the iteration number
- [ ] Re-running the harness on the same graph produces the same metric values (within documented tolerance for any seeded randomness)

**Dependencies:** chain-engine (R9 chain query API)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-SMALL-EXPERIMENT, not run: `bin/benchmark.py` exists (`idea:engine-benchmark`) but was not confirmed to emit these five metric names; the small experiment is diffing its output fields against the criteria.
<!-- THOUGHT:END -->
