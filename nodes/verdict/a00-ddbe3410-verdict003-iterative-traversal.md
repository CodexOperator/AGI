---
confidence: 0.95
evidence_runs:
  - experiment:a00-ddbe3410-exp003-iterative-traversal
id: "verdict:a00-ddbe3410-verdict003-iterative-traversal"
mint_id: b273d901747d43daa23cbb29c843015b
next_edges:
  - mvp:a00-ddbe3410-mvp003-iterative-traversal
parent_hypothesis: "hypothesis:a00-ddbe3410-iterative-traversal"
parents:
  - experiment:a00-ddbe3410-exp003-iterative-traversal
status: proved
synthetic: false
tags:
  - chain-engine
  - recursion-bug
  - iterative
title: "V003: iterative traversal PROVED — 9 chains at 708 hops"
type: verdict
---

**Verdict**: PROVED (confidence: 0.95)

## Metric
- 22 chains found (was 0 before fix due to RecursionError)
- 9 chains at 708 hops (all domain ideas at cycle 350)
- 1 chain at 300 hops (embeddings r3)
- 12 chains at 8 hops (base chains)
- 274 tests pass

## Evidence
- Replaced recursive `_traverse_from` with iterative `_traverse_iterative` using explicit stack
- Stack frame: `(node_id, current_path, successors_remaining)`
- LIFO pop order preserves DFS semantics
- No RecursionError at any chain length

## Interpretation
Recursive DFS limit was masking true chain lengths. All 9 domain chains are at 708 hops (cycle 350). Primary metric `longest_chain_length` is confirmed at 708.
