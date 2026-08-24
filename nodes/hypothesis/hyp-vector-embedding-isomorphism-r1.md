---
id: hyp:vector-embedding-isomorphism-r1
title: "R1: Node2Vec 2D coordinates isomorphic to ASCII render token positions"
type: hypothesis
parent_idea: idea:domain-vector-embedding-isomorphism
domain: vector-embedding-isomorphism
tags:
  - embeddings
  - node2vec
  - umap
  - isomorphism
  - render
spawns:
  - task:t-093
status: pending
verdict: inconclusive_lean_disproved:50
confidence: 0.18
evidence_runs: 0
demoted_from: disproved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''disproved'''
---

## Hypothesis

**Claim**: Node2Vec embeddings projected to 2D via PCA produce (x,y) coordinates that are **topologically isomorphic** to ASCII render token positions.

**Test**: 
1. Train Node2Vec on graph (walk_length=40, walks_per_node=5)
2. Project to 2D via PCA (from embeddings.projection)
3. Compare embedding (x,y) with graph distance for reachable node pairs
4. Measure: Spearman correlation between graph distance and embedding distance

**Expected**: Nodes closer in graph should be closer in embedding space.

## Result (iter 19)
- **Spearman correlation: -0.18** (weak negative)
- Nodes farther in graph are actually slightly CLOSER in embedding space
- **VERDICT: DISPROVED**

## Analysis
The hash-based Node2Vec implementation doesn't preserve graph topology:
- Uses deterministic random walks + hash projection
- Hash-based vectors don't encode semantic similarity
- PCA projection of random-ish vectors produces random directions
- No reason to expect topology preservation

## Next Steps
- R2: Try true skip-gram Node2Vec (gensim) vs hash-based
- R3: Check if embedding similarity matches graph traversal neighbors
