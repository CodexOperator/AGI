---
id: goal:g3
mint_id: 3df6dabc1aa4449aa506e3f158512f21
type: goal
confidence: 1.0
edited_by: season.py
goal_id: G3
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - goal:g3.1
  - idea:engine-benchmark
  - idea:engine-chain-engine
  - idea:engine-metrics
status: active
tags:
  - goal
  - root
thought_session: season
title: "G3: Scoring that added motion cannot move"
---
The graph is measured by goals reached, never by motion spent. This goal exists
because the opposite was tried and it worked: 9 chains × 2000 hops via shortcut
cycles, carrying no signal, and the resulting structure then broke the render
path outright.

**Invariants:**
- No primary metric that appending hops can shift. `longest_chain_length` is a
  descriptive statistic, never a target.
- A decisive verdict (`proved` / `disproved`) requires `evidence_runs >= 1`.
  Unevidenced claims are demoted, not discarded — the expensive artifact is kept,
  only the overclaim is dropped.
- `unevidenced_decisive_verdicts` reads `0`. Nonzero means a bypass or a
  hand-edited node.

Banked: **H3** (metric computation out of the driver heredoc into `metrics.py`;
`evidence_fraction`, `evidence_weighted_depth`; gameable-primary warning) and
**H4** (the gate in code, on both writer paths). This project's own config
migrated off `longest_chain_length` on 2026-08-21.

Still open, and the reason this stays active: **L4** — `outcome_coverage` is a
*proxy* that counts chains reaching an outcome, not their **attribution to a
specific goal**. True goal-fulfilment scoring is unbuilt. The goal nodes it
needs exist as of L15.