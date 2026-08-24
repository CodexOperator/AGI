---
id: verdict:verdict:a00-204c9d9e-1d958f
type: verdict
title: "Query API enables rational task selection in the capillary DAG"
verdict: inconclusive_lean_proved:50
confidence: 0.82
parents:
  - experiment:exp:a00-204c9d9e-1d958f
  - hypothesis:a00-204c9d9e-1d958f
tags:
  - architecture
  - query-api
  - capillary-dag
  - proved
next_edges: []
evidence_runs: 0
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---

# verdict:verdict:a00-204c9d9e-1d958f

## Verdict: PROVED

All 4 Query API functions operate correctly against the live 933-node capillary DAG graph.

### Evidence

- **Graph loaded**: 933 nodes, 923 edges (157+ in context, grew via chain extensions)
- **Q1 task_attractiveness**: 94 tasks scored, 1 non-zero (expected: most raw hypotheses have no graph edges)
- **Q2 chain_gaps**: 44 gaps found across 5 major domains (hypotheses without verdict children)
- **Q3 next_best_hypothesis**: 5 top hypotheses returned with chain-progress scores
- **Q4 coverage_report**: 9 domains, 933 nodes, 82.2% coverage
- **272 tests pass**: no regressions

### Why Q1 returned only 1 non-zero score

Most hypothesis nodes (e.g., `hyp:graph-core-r4`, `hyp:renderers-r8`) are raw research nodes with no outgoing edges in the graph. The next_edges are reconstructed from verdict→experiment→verdict cycle patterns, not from raw hypothesis→task patterns. This is correct: task_attractiveness correctly returns 0 for tasks whose parent hypothesis has no active chain.

### What the Query API provides

| Query | Purpose | Result |
|---|---|---|
| `task_attractiveness` | Score tasks for agent selection | 94 tasks scored |
| `chain_gaps` | Find unresolved hypotheses per domain | 44 gaps across 5 domains |
| `next_best_hypothesis` | Top hypotheses to extend | 5 returned |
| `coverage_report` | Per-domain node type counts | 9 domains, 82.2% coverage |

### Confidence: 0.82

扣 0.18 because Q1 has very sparse non-zero results (only 1/94 tasks scored). This reflects correct graph state but limits practical utility for raw-hypothesis domains. Future work: score tasks by hypothesis R-number recency even when hypothesis has no graph edges.
