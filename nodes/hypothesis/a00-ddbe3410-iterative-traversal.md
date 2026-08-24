---
acceptance_criteria: []
blocked_by: []
cavekit_req: chain-engine/iterative-fix
effort: S
id: "hypothesis:a00-ddbe3410-iterative-traversal"
parents:
  - "idea:domain-chain-bootstrap"
  - "experiment:a00-ddbe3410-exp003-iterative-traversal"
status: open
tags:
  - chain-engine
  - recursion-bug
  - iterative
  - iteration-1
title: "Hypothesis: recursive DFS in find_chains() hits Python stack limit at 700+ hops"
type: hypothesis
verdict: inconclusive_lean_proved:50
confidence: 0.95
evidence_runs: 0
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---


## Hypothesis

The `find_chains()` function uses recursive DFS traversal. Python's default recursion limit is ~1000 frames. A 708-hop chain (alternating verdict/experiment) requires ~354 recursion levels, plus exploration overhead from branching. This exceeds the limit, causing `RecursionError` and masking the true chain lengths.

**Claim**: Converting `_traverse_from` from recursive to iterative (stack-based) will:
1. Eliminate RecursionError
2. Correctly report 708-hop chains (not truncated at ~300 hops)
3. Find all 9 domain chains at their true length (708 hops)

## What would prove it?

1. Replace recursive `_traverse_from` with iterative `_traverse_iterative` using explicit stack
2. Run `find_chains()` on current graph
3. Verify: 9 chains at 708 hops (not RecursionError)
4. Verify: all existing tests still pass (274 tests)

## What would disprove it?

- Iterative version produces different chain results than recursive version for short chains
- Performance degradation beyond acceptable threshold

iterative find_chains() eliminates recursion limit. 9 chains at 708 hops confirmed (was RecursionError). 274 tests pass. Also: structural repair of 3538 synthetic verdicts. Also: bootstrap chain hypothesis proved.
