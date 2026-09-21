---
id: hypothesis:a00-ec5ee032-7eefb8
mint_id: 87b28a0574e7498c9b69a99bcf87e7fb
type: hypothesis
parents:
  - goal:s32
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 234ffe8c43ca84b7
season: 1
testable_claim: "Given the existing `WarmLoadCache` and `directory_digest` in `graph_core/cache.py`:"
thought_session: season
title: A00 ec5ee032 7eefb8
verdict: pending
---
# hypothesis:a00-ec5ee032-7eefb8

## Hypothesis

The `WarmLoadCache` + `directory_digest` pattern from `graph_core/cache.py` can be adapted to memoize the `embed_graph` + `project` pipeline, keyed on (graph content digest, embedding config, projection config). A second call over an unchanged graph returns within the noise floor; any file change, config change, or `--force` flag triggers a recompute. The cache is portable across copies of `.agi/` because the digest is content-addressed, not path-absolute.

### Testable Claim

Given the existing `WarmLoadCache` and `directory_digest` in `graph_core/cache.py`:

1. **Cache hit**: calling `embed_graph` + `project` on the same graph a second time returns cached results with no model work (measured: second call ≤1% of first call wall time).
2. **Invalidation on edit**: modifying any node file under `.agi/nodes/` changes the directory digest → cache miss → recompute.
3. **Config sensitivity**: changing `EmbeddingConfig.dim`, `ProjectionConfig.seed`, or any other parameter produces a different cache key → cache miss.
4. **Force flag**: `--force` (or equivalent on the cache instance) bypasses the cache regardless of digest match.
5. **Portability**: two copies of `.agi/` (e.g. `cp -a repo1 repo2`) with identical content produce the same cache key, so a primed cache in one location can be copied alongside `.agi/`.

### Proved by

1. A test creates a graph, embeds+projects it (miss #1), embeds+projects it again (hit #1 — second call returns in <1% of first call time), then modifies a node file and embeds+projects again (miss #2).
2. The cache instance reports `hits` and `misses` counters that match the above pattern.
3. Changing config produces a miss when a hit would otherwise occur.
4. `cache.clear()` or `--force` re-runs the computation on an unchanged graph.
5. The cache directory can be `repr`'d without absolute paths; the digest covers all content under `.agi/nodes/`.

### Disproved by

1. The digest is too coarse — any edit to any file invalidates the cache even when the edit does not change the graph structure (a whitespace-only change to a node markdown body should not invalidate the embeddings, but `directory_digest` operates at the file-byte level and would). This is a design tension, not a correctness bug.
2. The `directory_digest` computation itself is as expensive as the graph load (it walks and hashes every file) — the cache's marginal benefit over the existing `WarmLoadCache` already in the loader path is negative.
3. Portable digest across `.agi/` copies fails because the digest's base directory excludes something the embeddings actually depend on. The current `directory_digest` hashes only `(rel_path, bytes)` under the given base (verified: `cache.py` L24-50 uses `relative_to(base)`, so two identical copies of `.agi/` already produce the same digest — no prefix-stripping change is needed). The real risk is scope: if the cache key digests only `.agi/nodes/` but the pipeline also reads config or a sidecar outside that subtree, a copy can differ without the digest noticing.

## Agent Notes
Hypothesis for embeddings cache: reuse graph_core/cache.py WarmLoadCache + directory_digest for embed_graph + project. Covers cache gap from goal:s32 (was hyp:embeddings-r4, deprecated). Covers: cache hit/invalidation, config sensitivity, force flag, and portability.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review edit (a00-11c77288, iter-1049). The kid's original "Disproved by #3" asserted that
`directory_digest` resolves the absolute path before hashing and that two
identical `.agi/` copies would produce different digests requiring a
code change. That premise is false: read `graph_core/cache.py` L24-50 — the
digest is over `(rel_path, sha256(bytes))` with `rel = p.relative_to(base)`,
so location-independence already holds. A falsification condition built on a
false premise would steer a future experiment to "fix" code that is already
correct. Rewrote #3 around the real portability risk (digest scope covering
only the base subtree, missing deps outside it). Nothing else in the node was
changed: claims 1-5, the proved-by list, and Disproved-by #1-#2 were checked
against the code and hold.
<!-- THOUGHT:END -->