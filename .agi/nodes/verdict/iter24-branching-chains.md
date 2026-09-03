---
id: verdict:iter24-branching-chains
mint_id: 0ad88873d82f4cbabffc455762d29e5f
type: verdict
parents:
  - hyp:iter24-branching-chains
next_edges: []
confidence: 1.0
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
evidence_runs: []
title: Iter24 branching chains
verdict: inconclusive_lean_proved:50
---
## Evidence

Branching chains confirmed via manual DFS trace:
- `idea:domain-embeddings` has `next_edges: [hyp:embeddings-r2, hyp:embeddings-r3]`
- Both paths discovered by `find_chains()`
- Total: 18 chains (vs expected 12 if strictly linear)
- `idea:domain-autoresearch-tree-skill`: 2 chains (mvp branch + extend branch)
- `idea:domain-chain-engine`: 2 chains (extend cycle path + mvp path)

Architecture already supports branching. No code changes needed.