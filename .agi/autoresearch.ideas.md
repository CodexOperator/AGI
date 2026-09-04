# Deferred optimization ideas (autoresearch tree)

## Build time optimization

### Second-pass file re-reads in parsers
- parse_tasks second pass re-reads every task file (~84) to extract depends_on from frontmatter
- parse_skills second pass re-walks dir tree and re-reads SKILL.md files (~15-20)
- parse_agent_roles / parse_personas second passes re-read files (~5-10 each)
- All could cache frontmatter data in the first pass like build_tag_bridges _tag_store pattern
- Estimated impact: ~3-8ms (smaller than the 416 files in build_tag_bridges fix)

### Lazy _precompute_key_paths
- Currently eager in build_adjacency(). Could compute on first query instead.
- Smaller impact since it's only 1 BFS (vs 32 for reachability which was removed)

### add_node dedup optimization
- `while node_id in self._node_ids` does set lookup per increment; could use a counter-suffix instead of iterating

## Not related to build time

### _cache_ver bump convention
- `_cache_ver=13` is hardcoded in _cached_build_builder. If freqent code changes bump it, the lru_cache is cleared. Could derive from content hash of the module instead.