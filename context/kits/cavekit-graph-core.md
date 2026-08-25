---
created: 2026-04-30
last_edited: 2026-04-30
---

# Cavekit: graph-core

## Scope

Generic, domain-agnostic graph primitives: nodes, edges, identity, persistence, recursive bodies, directory-walking auto-discovery, and a portable bootstrap path. This kit is the substrate every other domain stands on. It contains nothing autoresearch-specific; the same primitives could be reused for any DAG memory product.

## Requirements

### R1: Generic Node Primitive

**Description:** A node is a typed, identified record with an optional payload reference, parent and child links, and free-form tags. Node type does not constrain payload; payload meaning is delegated to the schema-registry.

**Acceptance Criteria:**
- [ ] A node exposes the fields `id`, `type`, `payload_ref`, `parents`, `children`, `tags` and nothing in graph-core requires additional mandatory fields
- [ ] A node with no parents is accepted as a valid root and a node with no children is accepted as a valid leaf
- [ ] `parents` and `children` are sets of node ids (no duplicates) and self-loops are rejected with a clear error
- [ ] `tags` is a set of strings and is independent of the typed parent/child links

**Dependencies:** none

### R2: Generic Edge Primitive

**Description:** Edges connect a parent node to a child node, carry a relation type, and may carry tag metadata. The graph is a DAG; cycles are rejected at insert time.

**Acceptance Criteria:**
- [ ] Inserting an edge that would create a cycle returns a structured error and leaves the graph unchanged
- [ ] An edge exposes `source_id`, `target_id`, `relation`, and an optional `tags` set
- [ ] Two edges with the same `(source_id, target_id, relation)` are treated as one (idempotent insert)
- [ ] Removing a node removes all incident edges and leaves no dangling references

### R3: Identity Scheme

**Description:** Node ids follow a stable, human-legible scheme that is compact enough to render in ASCII frames.

**Acceptance Criteria:**
- [ ] Each id matches the pattern `<type-prefix>:<short-slug>` where `short-slug` is kebab-case of two to five words
- [ ] When two nodes would otherwise collide, the second receives a `:n` numeric suffix starting at `:2`
- [ ] Ids exceeding 40 characters trigger a non-fatal warning but are still accepted
- [ ] Ids are stable across rebuilds: regenerating the graph from the same source files produces the same ids

### R4: Frontmatter File Persistence

**Description:** Each node persists as a standalone file with a structured frontmatter header and a free-form body. Bodies are not loaded into memory until a node is visited.

**Acceptance Criteria:**
- [ ] Loading the graph reads only frontmatter; body content is fetched on first access to that node's body
- [ ] A node file round-trips: load then save produces a byte-for-byte equivalent file modulo whitespace normalization
- [ ] Either Markdown-with-YAML-frontmatter or pure structured-data files (such as JSON) are accepted as node containers
- [ ] A malformed frontmatter block produces a structured error naming the offending file and does not abort the rest of the load

### R5: Recursive Node Bodies

**Description:** A node body may itself contain a subgraph. The same primitives and the same renderers handle top-level and recursive subgraphs.

**Acceptance Criteria:**
- [ ] A node whose frontmatter declares `subgraph: true` is treated as a container; its body is parsed as a graph using the same loader
- [ ] Recursive subgraphs may nest at least three levels deep without special-case code paths
- [ ] Renderers are invoked uniformly on a top-level graph and on a nested subgraph using the same input contract
- [ ] Querying a parent node exposes both its outer-graph children and an opaque handle to its inner subgraph

### R6: Directory-Walking Auto-Discovery

**Description:** A directory of node files is loaded by walking the filesystem. A folder is a subgraph; files inside are nodes; folder names map to node types via the schema-registry.

**Acceptance Criteria:**
- [ ] Pointing the loader at any directory yields a graph whose nodes correspond to the files under that directory
- [ ] A subdirectory is loaded as a subgraph node whose type is resolved through the schema-registry
- [ ] Files that do not match any known schema are loaded as generic nodes and a warning is emitted listing them
- [ ] Walking is deterministic: two runs against the same directory produce the same node set and id order

**Dependencies:** schema-registry (for folder-name → node-type resolution)

### R7: Warm-Load Caching

**Description:** Repeated loads of an unchanged graph return in constant time relative to first load. A memoization layer wraps the builder.

**Acceptance Criteria:**
- [ ] A second load of an unchanged source directory returns in time indistinguishable from a no-op (within the host's measurement noise floor)
- [ ] Modifying any node file invalidates the cache for at least that file's containing graph and triggers a rebuild on next load
- [ ] The cache key includes a content-addressed digest of the source set so renaming a file is detected
- [ ] Cache state lives inside the project's local context directory and never under absolute external paths

### R8: Pluggable Persistence Layer

**Description:** The default persistence backend is the filesystem. The graph-core exposes a backend contract so alternative backends (such as in-process databases) can be added without changing callers.

**Acceptance Criteria:**
- [ ] A backend implements a documented set of operations (load, save, list, watch) and graph-core depends only on that contract
- [ ] Swapping the file backend for a stub in-memory backend in tests changes no caller code
- [ ] The default install requires no external database, daemon, or network service to function
- [ ] A backend choice is selectable through configuration without code edits

### R9: Portability Contract

**Description:** All graph state lives inside a single project-local context directory. The graph is movable by copying that directory.

**Acceptance Criteria:**
- [ ] No node file, cache file, or configuration file references an absolute path outside the project root
- [ ] Copying the context directory to a fresh checkout reproduces the same graph on load
- [ ] The graph loads with no environment variables set beyond an optional model selector for downstream hooks
- [ ] A self-test command verifies portability by re-loading from a temporary copy and comparing node counts and ids

### R10: Bootstrap Command

**Description:** A command initializes a new project so a fresh directory becomes a valid graph root.

**Acceptance Criteria:**
- [ ] Running the bootstrap command in an empty directory produces a `context/` skeleton with subdirectories for schemas, kits, and node storage
- [ ] Running the bootstrap command twice on the same directory is a no-op and does not overwrite existing files
- [ ] The skeleton includes a minimal example node and a minimal example schema sufficient to load a one-node graph
- [ ] The bootstrap reports the created paths to the user in a single summary

### R11: Traversal and Query API

**Description:** The graph exposes traversal primitives and a query API over the loaded node set, returning lazy iterators so a caller never pays for a full materialization it does not use.

**Acceptance Criteria:**
- [ ] R11.1 — `traverse_bfs(start_id)` yields node ids in breadth-first order as a lazy generator
- [ ] R11.2 — `traverse_dfs(start_id)` yields node ids in depth-first order as a lazy generator
- [ ] R11.3 — `find_paths(source_id, target_id)` returns all simple paths via DFS backtracking
- [ ] R11.4 — `find_ancestors(node_id)` returns the transitive parent closure via BFS
- [ ] R11.5 — `find_descendants(node_id)` returns the transitive child closure via BFS
- [ ] R11.6 — `query(type=None, tags=None, has_parent=None, has_child=None)` filters nodes without loading bodies
- [ ] R11.7 — every traversal and query entry point returns a lazy iterator, not a materialized list
- [ ] R11.8 — `detect_cycle(node_id)` runs DFS from that node and reports any cycle path it finds

## Out of Scope

- Autoresearch-specific node types such as `idea`, `hypothesis`, `experiment`, `verdict`, `mvp`, `outcome`, `bigger_outcome`, `app_purpose` — these are schema definitions, not graph-core concerns
- Chain mechanics, longest-chain attraction, fork or hop logic — see chain-engine
- ASCII, Mermaid, or git-shaped rendering — see renderers
- Vector embeddings or similarity APIs — see embeddings
- Specific source indexers (filesystem trees, code symbols, dependency graphs) — see environment-indexers

## Cross-References

- See also: cavekit-schema-registry.md (folder-name to node-type resolution, schemas as meta-nodes)
- See also: cavekit-environment-indexers.md (consumes graph-core to write nodes)
- See also: cavekit-chain-engine.md (computes chains over graph-core nodes)
- See also: cavekit-renderers.md (renders graph-core nodes)
- See also: cavekit-embeddings.md (vectorizes graph-core nodes)
- See also: cavekit-autoresearch-tree-skill.md (drives the loop on top of graph-core)
