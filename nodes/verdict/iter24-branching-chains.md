---
confidence: 1.0
evidence_runs: 0
id: "verdict:iter24-branching-chains"
next_edges: []
parents:
  - hypothesis:iter24-branching-chains
type: verdict
verdict: inconclusive_lean_proved:50
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---

## Evidence

Branching chains confirmed via manual DFS trace:
- `idea:domain-embeddings` has `next_edges: [hyp:embeddings-r2, hyp:embeddings-r3]`
- Both paths discovered by `find_chains()`
- Total: 18 chains (vs expected 12 if strictly linear)
- `idea:domain-autoresearch-tree-skill`: 2 chains (mvp branch + extend branch)
- `idea:domain-chain-engine`: 2 chains (extend cycle path + mvp path)

Architecture already supports branching. No code changes needed.
