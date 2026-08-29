---
created: 2026-04-30
last_edited: 2026-04-30
---

# Cavekit: embeddings

## Scope

Vector embeddings of the graph that share their two-dimensional projection with the renderers' shared representation. The same coordinate values that drive a scatter rendering also drive similarity queries: visualization and embedding are isomorphic by construction. Node2Vec is the embedding model and UMAP is the projection method for v1. Other models and projections are documented as upgrade paths but not required.

## Requirements

### R1: Per-Node Vector Generation

**Description:** A vector is generated per node by running Node2Vec over the graph-core graph. The choice of Node2Vec is fixed for v1; alternative models are out of scope.

**Acceptance Criteria:**
- [ ] After embedding, every node in the input graph has exactly one associated vector
- [ ] Vector dimensionality is configurable and defaults to a documented value
- [ ] Two runs over the same graph and configuration produce identical vectors when the random seed is fixed
- [ ] When the graph contains zero nodes, the embedding step completes successfully and produces an empty vector set

**Dependencies:** graph-core (R1, R2)

### R2: UMAP Projection to 2D

**Description:** Per-node vectors are projected to two dimensions using UMAP. Three-dimensional projection is supported via configuration but is not required by default.

**Acceptance Criteria:**
- [ ] After projection, every embedded node has an `(x, y)` coordinate pair
- [ ] Projection dimensionality is configurable to either 2 or 3, with 2 as the default
- [ ] Two projection runs over the same vectors and configuration produce identical coordinates when the random seed is fixed
- [ ] When fewer than two nodes are embedded, projection completes with a documented degenerate result rather than raising

### R3: Coordinate Isomorphism with Renderers

**Description:** The `(x, y)` coordinates produced by projection are exactly the `x` and `y` values used by the renderers' shared representation. There is one source of truth.

**Acceptance Criteria:**
- [ ] The renderer's shared representation derives `x` and `y` for each token from the embedding output for the same node id
- [ ] When embeddings are recomputed, the renderer's coordinates change accordingly without separate update steps
- [ ] No alternative coordinate source is permitted for nodes that have an embedding
- [ ] An integration check confirms that for every node, the renderer-side and embedding-side coordinates are equal

**Dependencies:** renderers (R1)

### R4: Cache Invalidation on Graph Change

**Description:** Embedding state is invalidated when the underlying graph changes. UMAP coordinates remain stable across rebuilds when the graph is unchanged and the seed is fixed.

**Acceptance Criteria:**
- [ ] Adding, removing, or modifying a node invalidates that node's vector and triggers recomputation on next embed
- [ ] When neither the graph nor the configuration change, two consecutive runs produce the same vectors and the same coordinates
- [ ] Cached embedding state lives inside the project context directory and is portable along with it
- [ ] A documented flag forces a full re-embed regardless of cache state

**Dependencies:** graph-core (R7 warm-load caching, R9 portability)

### R5: Similarity Query API

**Description:** A query returns the `k` most similar nodes to a given node id, ranked by similarity score.

**Acceptance Criteria:**
- [ ] The query accepts a node id and an integer `k` and returns up to `k` `(node_id, score)` pairs ordered by descending score
- [ ] When the requested node has no embedding, the query returns an empty list and emits a warning rather than raising
- [ ] Scores are real numbers in a documented range
- [ ] Two queries with the same arguments over the same embedding state produce identical results

### R6: Scatter Rendering Plugin

**Description:** A renderer plugin produces an ASCII scatter view directly from UMAP coordinates, sharing the renderer plugin contract.

**Acceptance Criteria:**
- [ ] The plugin is registered through the same renderer plugin contract used by the renderers kit
- [ ] The plugin places each node at coordinates derived from its UMAP `(x, y)` without re-projecting
- [ ] Output respects the ASCII renderer's bounds (at most 200 lines and 200 columns) and degrades visibly when bounds are exceeded
- [ ] When two nodes overlap at the same character cell, the cell shows a documented overlap marker

**Dependencies:** renderers (R7)

### R7: Optional In-Graph Embedding Storage

**Description:** Per-node vectors may optionally be stored as a payload field on the node itself so the embedding is persisted alongside the graph.

**Acceptance Criteria:**
- [ ] When in-graph storage is enabled, each node carries a `embedding_vector` payload field after embedding
- [ ] When in-graph storage is disabled (default), node files do not carry the field and embeddings live only in the cache
- [ ] Toggling the option does not invalidate previously stored vectors
- [ ] When the option is enabled and a node lacks the field, the embedding step backfills it without rewriting unrelated fields

## Out of Scope

- Alternative embedding models such as transformer-based encoders (documented as a future upgrade path but not required in v1)
- Specific workflows that consume similarity scores (for example "always extend the chain whose tail is most similar to X") — see autoresearch-tree-skill
- Visualization of three-dimensional projections beyond toggling the projection target — out of scope for renderers in v1
- Cross-graph or cross-repo embeddings — saved for later

## Cross-References

- See also: cavekit-graph-core.md (R1 nodes, R7 caching, R9 portability)
- See also: cavekit-renderers.md (R1 shared representation, R7 plugin contract)
- See also: cavekit-autoresearch-tree-skill.md (may consume similarity for agent dispatch)
