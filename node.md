---
id: outcome:a00-ddbe3410-outcome003-iterative-traversal
mint_id: 95cd99f655ab4216b0bff2cb570abcbc
type: outcome
parents:
  - mvp:a00-ddbe3410-mvp003-iterative-traversal
next_edges:
  - bigger_outcome:a00-ddbe3410-bo003-iterative-traversal
edited_by: season.py
judged_against: goal:g2.1
lens: goal:g2
season: 1
tags:
  - chain-engine
  - recursion-bug
thought_session: season
title: "OUTCOME003: chain traversal unbounded by recursion depth"
---
## Input
Recursive `_traverse_from` in `src/chain_engine/chains.py`.

## Output
Iterative `_traverse_iterative` with explicit stack — no recursion depth limit.

## Behavior
Stack-based DFS: push (node_id, path, successors) frames, pop and process. LIFO order preserves DFS semantics. Handles chains of any length.

## Edge Cases
- Zero-hop chains: handled (empty stack → no chains)
- Single-node ideas with no successors: dead-end (no chain)
- Very deep chains (10,000+ hops): stack memory vs recursion depth tradeoff — stack approach wins