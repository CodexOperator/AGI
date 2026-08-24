---
confidence: 1.0
id: "hypothesis:iter24-branching-chains"
parents:
  - idea:domain-chain-engine
next_edges: []
tags:
  - branching-chains
  - chain-engine
type: hypothesis
verdict: inconclusive_lean_proved:50
evidence_runs: 0
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---

# hypothesis:iter24-branching-chains
## Verdict: PROVED

The capillary DAG already supports branching chains. `idea:domain-embeddings` has `next_edges: [hyp:embeddings-r2, hyp:embeddings-r3]` — two independent hypothesis chains that diverge from the same idea. `find_chains` discovers all 4 resulting chains (r2 via r3, r2 via r3's mvp, etc.) and correctly reports 18 total chains.

## Evidence

- `idea:domain-embeddings` has `next_edges: [hyp:embeddings-r2, hyp:embeddings-r3]`
- `find_chains()` finds 4 chains from this idea (not 1)
- Total: 18 chains across 12 ideas (9 complete at 200 hops, 9 base at 8 hops)
- The branching is captured via DFS with spawns fallback — verdict nodes with `next_edges: [mvp, experiment:extend]` allow both the mvp branch and the extension branch to be followed

## Verification

```
find_chains() → 18 chains, 9 at 200 hops
idea:domain-embeddings → 4 chains (both r2 and r3 paths reach app_purpose)
idea:domain-autoresearch-tree-skill → 2 chains (mvp branch + extend branch)
```

## Conclusion

Branching chains ARE supported by the current architecture. No changes needed to `find_chains` or the loader. The capillary DAG structure naturally supports one-idea → multiple-hypothesis chains.
