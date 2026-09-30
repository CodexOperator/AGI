---
id: hypothesis:a00-12e9183c-90ceab
mint_id: 85737ca79caa4538a9c74d8d1ebc547d
type: hypothesis
parents:
  - goal:s32
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: b75d37c47785185f
season: 1
testable_claim: "1. **Toggle exists and defaults off**: `EmbeddingConfig` gains `store_in_graph: bool = False`. When `False`, `embed_graph()` behaviour is unchanged. When `True`, after computing a vector for node N, `save_node_file(frontmatter={..., \"embedding\": vector})` is called on N's source file. 2. **Round-trip integrity**: after `store_in_graph=True` write, reloading the node frontmatter and reading `embedding` yields the same `list[float]` that was written (within float64 serialization tolerance — YAML float list round-trips at ~15 decimal digits, which exceeds the precision of the hash-based vectors). 3. **Idempotent re-run**: calling `embed_graph()` a second time with `store_in_graph=True` on an already-embedded graph reads the vectors from frontmatter instead of recomputing, producing the same result within float tolerance. The directory digest changes (file bytes changed → cache miss), but the cost model still favours reading a dozen floats from YAML over re-running walks+projection. 4. **Selective embed**: when some nodes already carry `embedding` and others do not, `embed_graph()` embeds only the missing ones and writes them, then returns the combined dict. Adding a single new node to a 500-node graph embeds only the new node (the other 499 read their stored vector). 5. **Compatibility**: `project()` and `similar_to()` consume the returned `dict[str, list[float]]` unchanged — the in-graph toggle is a storage detail, not a new API. The vector dict returned by `embed_graph()` is the same shape whether built from frontmatter reads or from fresh computation. 6. **No identity drift**: writing `embedding` into frontmatter does not change the node's `id`, `type`, `parents`, `children`, `tags`, or body. The `digest` in `directory_digest` changes (file bytes changed), so the warm-load cache sees a miss — this is a correctness tradeoff (v6) not a correctness bug."
thought_session: season
title: "S32.3: In-graph embedding storage — toggle writes vector into node frontmatter, loader reads it back"
verdict: pending
---
# hypothesis:a00-12e9183c-90ceab

## Hypothesis

An optional toggle (`store_in_graph: bool`, default `False`) on `EmbeddingConfig` can write each node's embedding vector into its own `.md` file frontmatter under an `embedding` key, and the existing `embed_graph()` pipeline can read it back (skip recompute when a node already carries its vector, rebuild only missing entries). The toggle is off by default so existing workflows are unaffected; when on, the vector lives alongside the node, is portable with `.agi/`, and survives cache eviction. The loader already has `save_node_file()` for round-tripping frontmatter.

### Testable Claim

1. **Toggle exists and defaults off**: `EmbeddingConfig` gains `store_in_graph: bool = False`. When `False`, `embed_graph()` behaviour is unchanged. When `True`, after computing a vector for node N, `save_node_file(frontmatter={..., "embedding": vector})` is called on N's source file.
2. **Round-trip integrity**: after `store_in_graph=True` write, reloading the node frontmatter and reading `embedding` yields the same `list[float]` that was written (within float64 serialization tolerance — YAML float list round-trips at ~15 decimal digits, which exceeds the precision of the hash-based vectors).
3. **Idempotent re-run**: calling `embed_graph()` a second time with `store_in_graph=True` on an already-embedded graph reads the vectors from frontmatter instead of recomputing, producing the same result within float tolerance. The directory digest changes (file bytes changed → cache miss), but the cost model still favours reading a dozen floats from YAML over re-running walks+projection.
4. **Selective embed**: when some nodes already carry `embedding` and others do not, `embed_graph()` embeds only the missing ones and writes them, then returns the combined dict. Adding a single new node to a 500-node graph embeds only the new node (the other 499 read their stored vector).
5. **Compatibility**: `project()` and `similar_to()` consume the returned `dict[str, list[float]]` unchanged — the in-graph toggle is a storage detail, not a new API. The vector dict returned by `embed_graph()` is the same shape whether built from frontmatter reads or from fresh computation.
6. **No identity drift**: writing `embedding` into frontmatter does not change the node's `id`, `type`, `parents`, `children`, `tags`, or body. The `digest` in `directory_digest` changes (file bytes changed), so the warm-load cache sees a miss — this is a correctness tradeoff (v6) not a correctness bug.

### Proved by

1. A test creates a two-node graph, runs `embed_graph(config=EmbeddingConfig(store_in_graph=True))`, checks that each node file now has `embedding: [<float list>]` after `---`.
2. The same test reloads the graph from disk, runs `embed_graph()` again with `store_in_graph=True`, and asserts the returned vectors are identical (within float tolerance).
3. A test creates a third node without an embedding, re-runs `embed_graph(store_in_graph=True)`, and asserts only the third node's vector was computed (the other two read from frontmatter). The returned dict has all three entries.
4. `project()` and `similar_to()` accept the output of (3) identically as with `store_in_graph=False`.
5. A test with `store_in_graph=False` asserts no node file is modified (vectors stay in the returned dict only).

### Disproved by

1. YAML float list serialization loses precision to the point that the vector is no longer usable for cosine similarity (i.e. similarity scores for the same node drift by >1e-6 between a fresh-compute and a round-trip read).
2. Writing a vector to every node file in a 1000+ node graph is slower than recomputing the vectors — the I/O cost dominates. (This is a performance concern for large graphs, not a correctness bug — the toggle defaults off so no existing workflow pays this cost.)
3. Frontmatter with `embedding: [0.0043, 0.12, ...]` (64 floats) renders node files unreadable for standard frontmatter editing. (Mitigation: `store_in_graph` is off by default; a future improvement could store a base64-compressed binary blob instead of bare YAML floats.)
4. The `save_node_file()` call inside `embed_graph()` is a side effect that breaks the current pure-function contract of the embeddings pipeline — a caller that passes `store_in_graph=True` gets disk writes from a function whose signature says it returns a dict. (This is a design objection, not a test failure.)

### References

- `EmbeddingConfig` in `extensions/agi/src/embeddings/node2vec.py` — the toggle is added here.
- `save_node_file()` / `load_node_file()` in `graph_core/persistence/frontmatter.py` — the write and read paths already exist.
- `directory_digest` in `graph_core/cache.py` — the digest changes when file bytes change, which is why the warm-load cache sees a miss after an in-graph-write. This is acceptable: the embed computation is the expensive part, the cache miss only re-loads the graph (which the warm-load cache already does quickly).
- `hypothesis:a00-ec5ee032-7eefb8` (cache) — the in-graph storage toggle and the cache are complementary: the cache memoizes the full `embed_graph()` result (fast miss-avoidance on reload), while the in-graph toggle persists vectors across cache clears and into file copies.
- **Precedent**: `position` frontmatter key already exists in some node files — the pattern of storing coordinate data in frontmatter is established.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a01-eef375bf review, iter-1049: accepted as-is. Parents link resolves (goal:s32 exists). Verdict `pending` is valid for a fresh hypothesis. All six testable claims are specific and verifiable. Sibling references (a00-ec5ee032-7eefb8 for cache, a00-c4b84f52-f58e90 for scatter renderer) both resolve. References to `EmbeddingConfig`, `save_node_file`, `load_node_file`, and `directory_digest` are accurate. One minor inaccuracy: the testable claim says `save_node_file(frontmatter={..., "embedding": vector})` but the actual signature is `save_node_file(path, nf: NodeFile)` — the concept is correct (load NodeFile, mutate frontmatter, save) but the pseudo-code misstates the API. Not worth a revision at hypothesis level; the implementer will see the real signature. No demotion needed: no verdict claim, no evidence required.
<!-- THOUGHT:END -->

## Agent Notes
In-graph embedding storage hypothesis: optional toggle writes node vectors into .md frontmatter. Covers the third gap from goal:s32 (was hyp:embeddings-r7, deprecated). Complementary to sibling hypotheses on cache (a00-ec5ee032-7eefb8) and scatter renderer (a00-c4b84f52-f58e90).