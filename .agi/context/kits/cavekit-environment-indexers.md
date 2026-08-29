---
created: 2026-04-30
last_edited: 2026-04-30
---

# Cavekit: environment-indexers

## Scope

Pluggable indexers that consume an external source (a directory tree, a code repository, a Python project, an OpenAPI specification, a running container) and emit nodes into the graph through graph-core and the schema-registry. Indexers are on-demand: nothing scans automatically until invoked. Each indexer is one self-contained file with documented internals so future replacements can be made surgically.

## Requirements

### R1: Indexer Invocation Command

**Description:** A single command runs a chosen indexer over a chosen path and writes results into the graph.

**Acceptance Criteria:**
- [ ] The command accepts a target path and an indexer name and runs only that indexer
- [ ] Listing available indexers without invoking one produces a summary with each indexer's name and one-line description
- [ ] An unknown indexer name returns a structured error and does not run anything
- [ ] The command exits with a non-zero status when the indexer reports any failure that prevented node emission

**Dependencies:** graph-core (R10 bootstrap), schema-registry (R1 schema-as-file)

### R2: Filesystem Tree Indexer

**Description:** An indexer emits one node per directory and one node per file under a target path.

**Acceptance Criteria:**
- [ ] Running this indexer on any directory produces a node for the directory and one child node per file or subdirectory
- [ ] Each emitted node carries frontmatter that conforms to the registered filesystem-tree schema
- [ ] Symbolic links and unreadable entries are skipped with a per-entry warning rather than aborting the run
- [ ] Re-running the indexer on the same path produces the same node ids and the same parent-child links

### R3: Code Symbol Indexer

**Description:** An indexer emits nodes for code symbols (functions, classes, methods, modules) and edges for the relationships between them. The internals carry forward the lessons of the predecessor project (warm-load caching, tag-based bridging edges, precomputed traversal paths) but are re-implemented against this kit's contracts rather than copied.

**Acceptance Criteria:**
- [ ] Running this indexer on a code repository emits at minimum function, class, method, and module nodes for the supported language
- [ ] The emitted graph contains relationship edges sufficient to answer "callers of X" and "callees of X" queries
- [ ] The indexer warm-loads in time indistinguishable from a no-op on a previously-indexed unchanged repository
- [ ] Inline comments inside the indexer's source flag at least one upgrade point per major parsing stage (for example "this regex parser could be replaced by a tree-based parser later")

### R4: Python Dependency Indexer

**Description:** An indexer emits nodes for Python packages a project depends on, plus internal-import edges between modules.

**Acceptance Criteria:**
- [ ] Running this indexer on a Python project emits one node per declared package dependency
- [ ] Edges record which internal module imports which other internal module
- [ ] Both `requirements.txt`-style and `pyproject.toml`-style dependency declarations are supported
- [ ] When neither declaration file exists, the indexer reports a structured error and emits no nodes

### R5: API Dependency Indexer

**Description:** An indexer emits nodes describing endpoints and their relationships from an OpenAPI or Swagger specification.

**Acceptance Criteria:**
- [ ] Running this indexer on a valid specification file emits one node per endpoint
- [ ] Each endpoint node carries method, path, and summary fields in its frontmatter
- [ ] Edges record which endpoints share schemas or reference each other
- [ ] An invalid specification file produces a structured error naming the offending file and emits no nodes

### R6: Container Observation Indexer

**Description:** An indexer emits nodes describing a running container observed read-only from the outside, with no modification of the container.

**Acceptance Criteria:**
- [ ] Running this indexer against an accessible container produces a node for the container plus child nodes for each observable surface (image, ports, mounts, environment keys with values redacted)
- [ ] No write operation is issued against the container or its host
- [ ] When the target container is unreachable, the indexer returns a structured error and emits no nodes
- [ ] Sensitive values (secrets, tokens) are redacted before being written into node frontmatter

### R7: One-File-Per-Indexer Layout

**Description:** Each indexer is a single self-contained file with documented internals and registers or references at least one schema.

**Acceptance Criteria:**
- [ ] Each indexer lives in its own file under the indexers directory
- [ ] Each indexer either registers a new schema with the schema-registry or references an existing built-in schema
- [ ] Each indexer file documents its inputs, outputs, and known limitations in a header comment block
- [ ] Removing an indexer file removes only that indexer's command without affecting others

**Dependencies:** schema-registry (R1, R8)

### R8: Per-Path Result Caching

**Description:** Indexer results are cached per-path so repeated invocations on the same unchanged source skip recomputation.

**Acceptance Criteria:**
- [ ] A second invocation on the same unchanged path returns in time indistinguishable from a no-op
- [ ] Modifying any source file under the target path invalidates the cache for at least that path's run
- [ ] Cache state is stored under the project context directory and is portable along with it
- [ ] Forcing a fresh re-run is available via a documented flag

**Dependencies:** graph-core (R7 warm-load caching, R9 portability)

### R9: Indexer Documentation and Upgrade Markers

**Description:** Each indexer's source documents its own internals well enough that a future contributor can replace the parsing or scanning core without re-deriving the schema mapping.

**Acceptance Criteria:**
- [ ] Each indexer file contains comments explaining at least its parsing strategy, its schema mapping, and its caching behavior
- [ ] Each indexer file contains at least one comment block tagged as an upgrade marker, naming the section eligible for replacement
- [ ] Upgrade markers are discoverable by a single grep over the indexers directory
- [ ] A documentation self-check command lists each indexer and reports whether it has at least one upgrade marker

## Out of Scope

- Chain-specific autoresearch node types (idea, hypothesis, experiment, verdict, mvp, outcome, bigger_outcome, app_purpose) — see chain-engine
- Rendering of indexed graphs — see renderers
- The autoresearch agent loop that decides what to index when — see autoresearch-tree-skill
- Mutating indexers that change source repositories or running containers — explicitly out of bounds

## Cross-References

- See also: cavekit-graph-core.md (R1 nodes, R2 edges, R7 caching, R9 portability)
- See also: cavekit-schema-registry.md (each indexer registers or references a schema)
- See also: cavekit-renderers.md (consumes nodes the indexers produce)
- See also: cavekit-autoresearch-tree-skill.md (invokes indexers as part of the loop)
