---
id: hyp:a00-695d830c-499a8b
mint_id: 5684c3c736b5416db9565cbdd7eb90be
type: hypothesis
parents:
  - idea:domain-vector-embedding-isomorphism
confidence: 0.5
domain: vector-embedding-isomorphism
edited_by: season.py
season: 1
spawns: []
status: pending
tags:
  - embeddings
  - umap
  - isomorphism
  - neighborhood
  - render
thought_session: season
title: UMAP 2D projection enables graph↔render coordinate isomorphism
verdict: pending
---
# hyp:a00-695d830c-499a8b

## Hypothesis

**Claim**: UMAP 2D projection of Node2Vec embeddings produces (x,y) coordinates that preserve local neighborhood structure, enabling graph↔render coordinate isomorphism even though PCA was disproved (R1 Spearman = -0.18).

**Key distinction from R1**: R1 used PCA which is linear dimensionality reduction. UMAP is a manifold-learning method designed to preserve local structure. The UMAP projection was already validated separately at 98.3% neighbor preservation (embeddings R3). This hypothesis tests whether that neighborhood preservation translates to coordinate isomorphism with ASCII render token positions.

**Test**:
1. Extract Node2Vec embeddings from the loaded graph (walk_length=40, walks_per_node=5)
2. Project to 2D using UMAP (from embeddings.projection, not PCA)
3. For each node, find k=5 nearest neighbors in UMAP 2D space
4. Compare: what fraction of UMAP neighbors are also graph-edge neighbors?
5. Measure: Jaccard-like neighborhood overlap score

**Prove**: Neighborhood overlap >60% between UMAP space and graph space
**Disprove**: Overlap ≤30% (similar to PCA's -0.18 Spearman failure)

**Why this matters**: The capillary DAG needs graph↔render duality for semantic zoom and cross-domain queries. If UMAP works, the renderers can use UMAP coordinates as canonical (x,y) positions, achieving isomorphic mapping between the embedding layer and the ASCII rendering layer.

## Proving it

Run experiment: `exp-vector-embedding-isomorphism-r2-umap-neighborhood.py`
- Load graph with GraphLoader
- Extract or reuse existing embeddings
- Apply UMAP 2D projection
- Compute neighborhood overlap between UMAP space and graph edges
- Score: fraction of UMAP k-nearest-neighbor pairs that share a graph edge

## Disproving it

UMAP neighborhood overlap ≤30%, similar to PCA failure — then force-directed layout (d3-force, Graphviz neato) becomes the recommended alternative per R1 next steps.

## Relationship to existing chains

- embeddings R3 already proved UMAP 2D projection works (98.3% preservation)
- renderers R1 proved RenderToken has x,y fields
- This hypothesis bridges them: UMAP 2D → RenderToken.x,y with >60% neighborhood match
- If proved: complete 8-hop chain for idea:domain-vector-embedding-isomorphism (verdict exists, needs exp→verdict→mvp→outcome→bigger_outcome→app_purpose)
- If disproved: document force-directed alternative, still create chain nodes with disproved status