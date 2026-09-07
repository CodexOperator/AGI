---
id: exp:a00-ddbe3410-exp003-iterative-traversal
mint_id: 67b573e87e8f4a05adfda4aecf4a7b7f
type: experiment
parents:
  - hyp:a00-ddbe3410-iterative-traversal
next_edges:
  - verdict:a00-ddbe3410-verdict003-iterative-traversal
edited_by: season.py
season: 1
status: complete
tags:
  - chain-engine
  - recursion-bug
  - iterative
thought_session: season
title: "EXP003: Iterative find_chains() — eliminate recursion limit"
---
## Experiment

Replace `_traverse_from` (recursive DFS) with `_traverse_iterative` (explicit stack) in `src/chain_engine/chains.py`.

## Results
- Before: RecursionError at 708-hop chains
- After: 9 chains at 708 hops (all domains), 22 total chains
- 274 tests pass