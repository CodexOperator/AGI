# Autoresearch Ideas

## Potential Future Optimizations

### Low-hanging fruit
- [ ] Pre-compile regex in graph_builder module (currently re-compiled on each import)
- [ ] Cache schema file parsing results
- [ ] Use memory-mapped file for large caches

### Data Source Expansion
- [ ] Parse decisions/ directory for decision nodes
- [ ] Parse lessons/ directory for learning nodes
- [ ] Parse tasks/ directory for task state nodes
- [ ] Parse .hermes/agi/pi-agi.log for session data

### Query Optimizations
- [ ] Implement bidirectional BFS for faster path finding
- [ ] Pre-build node index by type for O(1) lookups
- [ ] Cache query results for repeated queries

### Visualization
- [ ] Add graphviz DOT output
- [ ] Add mermaid diagram output
- [ ] Add interactive HTML viewer

### DB Integration
- [ ] Implement duckdb backend for persistent graph storage
- [ ] Add full-text search using Postgres/duckdb FTS
- [ ] Implement incremental updates (not full rebuild)

### Interesting Findings
- Gitnexus lbug file is NOT SQLite (despite .db-like header "LBUG(")
- npx gitnexus call takes ~1.9s but is cacheable
- Module-level caching works well for repeated runs

### Deferred Ideas
- Multi-repo graph building (cross-reference belam-codex + machinelearning)
- Embeddings-based semantic search for graph queries
- LLM-based graph summarization
