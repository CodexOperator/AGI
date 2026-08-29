---
id: "exp:a00-ddbe3410-exp003-iterative-traversal"
mint_id: 67b573e87e8f4a05adfda4aecf4a7b7f
next_edges:
  - verdict:a00-ddbe3410-verdict003-iterative-traversal
parents:
  - hyp:a00-ddbe3410-iterative-traversal
status: complete
tags:
  - chain-engine
  - recursion-bug
  - iterative
title: "EXP003: Iterative find_chains() — eliminate recursion limit"
type: experiment
---

## Experiment

Replace `_traverse_from` (recursive DFS) with `_traverse_iterative` (explicit stack) in `src/chain_engine/chains.py`.

## Results
- Before: RecursionError at 708-hop chains
- After: 9 chains at 708 hops (all domains), 22 total chains
- 274 tests pass
