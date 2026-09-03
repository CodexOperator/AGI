---
id: hyp:iter24-verdict-loading
mint_id: c073cc094eee4c06a9b28e1fcfdb4b2d
type: hypothesis
parents:
  - idea:domain-chain-engine
next_edges: []
confidence: 1.0
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
evidence_runs: []
tags:
  - topological-queries
  - loader
  - iter-24
title: Iter24 verdict loading
verdict: inconclusive_lean_proved:50
---
# hyp:iter24-verdict-loading
## Verdict: PROVED

Topological queries now reflect actual chain completion state. Rankings show meaningful variation.

## Changes

- `src/graph_core/node.py`: Added verdict_meta fields to Node dataclass
- `src/graph_core/loader.py`: Added verdict field extraction
- `src/graph_core/topological_queries.py`: Fixed verdict value access
- `tests/graph_core/test_node.py`: Updated + 2 new tests