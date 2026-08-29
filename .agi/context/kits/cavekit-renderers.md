---
created: 2026-04-30
last_edited: 2026-04-30
---

# Cavekit: renderers

## Scope

Multi-format renderers that turn a graph into human-readable views. All renderers consume a single shared internal representation, so a new renderer is one class implementing a single method. The same representation is also consumed by the embeddings kit, which is what keeps visualization and embedding isomorphic. Renderers are pure functions: same input, same output, no side effects.

## Requirements

### R1: Shared Internal Representation

**Description:** All renderers operate over a uniform representation: a sequence of render tokens, where each token carries identity, label, type, depth, two-dimensional coordinates, and outgoing edges.

**Acceptance Criteria:**
- [ ] A render token exposes the fields `id`, `label`, `type`, `depth`, `x`, `y`, and `edges`
- [ ] Building the representation from a graph is deterministic: identical input graphs produce identical token sequences
- [ ] The same representation is accepted by every renderer in this kit without conversion shims
- [ ] The representation is documented as a contract so external consumers (notably embeddings) can rely on it

**Dependencies:** graph-core (R1, R2)

### R2: ASCII Renderer (Primary)

**Description:** A primary renderer produces a compact text view bounded by 200 lines and 200 columns. The view is hierarchical and includes a summary of edges and a count of node types.

**Acceptance Criteria:**
- [ ] Rendering any graph produces output of at most 200 lines and at most 200 columns
- [ ] When the graph is too large for the bounds, the renderer compresses or truncates with a clearly visible marker rather than overflowing
- [ ] The output includes a per-type count and a summary of edges
- [ ] Two runs against the same graph produce byte-equal output

### R3: Mermaid Renderer

**Description:** A renderer produces a valid Mermaid diagram source string usable as a graph or flowchart.

**Acceptance Criteria:**
- [ ] The output begins with a recognized Mermaid diagram directive (for example `graph TD` or `flowchart`)
- [ ] The output parses without error in Mermaid version 10 or later
- [ ] Every node and edge in the input representation appears at most once in the output
- [ ] Two runs against the same representation produce byte-equal output

### R4: Git-Tree Renderer

**Description:** A renderer produces a view shaped like the output of a graph-style git log, where each chain corresponds to one branch shape.

**Acceptance Criteria:**
- [ ] Each chain in the input appears as one branch-shaped lane in the output
- [ ] Lane order is deterministic and rooted in the highest-scoring chain
- [ ] Merge points (where two chains share a node) render as a visible junction
- [ ] The output uses only printable ASCII characters

### R5: Git-Diff Renderer

**Description:** A renderer produces a diff view between two experiment runs along the same chain so progression and regression are visible side by side.

**Acceptance Criteria:**
- [ ] The renderer accepts exactly two run identifiers belonging to the same chain and rejects mismatched pairs with a structured error
- [ ] Added, removed, and changed fields appear with conventional diff markers
- [ ] When two runs are identical, the output is an empty diff with a one-line note rather than a blank string
- [ ] The output uses only printable ASCII characters

### R6: Recursive Rendering

**Description:** When a node's body is itself a subgraph, renderers may render it as a nested view bounded in depth.

**Acceptance Criteria:**
- [ ] A node flagged as containing a subgraph is rendered with a visible nested view in renderers that support nesting
- [ ] The ASCII renderer renders nested subgraphs to a maximum depth of two levels
- [ ] Renderers that do not support nesting render only a single placeholder line per nested subgraph
- [ ] Nesting depth is configurable and respects a documented maximum

**Dependencies:** graph-core (R5 recursive node bodies)

### R7: Renderer Plugin Contract

**Description:** Adding a new renderer is one new class that implements a single method taking the shared representation and returning a string.

**Acceptance Criteria:**
- [ ] The renderer interface declares exactly one required method that accepts the shared representation and returns a string
- [ ] A new renderer implementation is loadable without modifying existing renderers
- [ ] An invalid renderer (raises during render or returns a non-string) is reported with a structured error and does not affect other renderers
- [ ] A self-test command runs every registered renderer over a fixture graph and reports pass or fail per renderer

### R8: Pure Function Guarantee

**Description:** Every renderer is a pure function over the representation: it never mutates input, never reads external state, and never writes outside the returned string.

**Acceptance Criteria:**
- [ ] A renderer invoked twice with the same representation produces equal outputs
- [ ] A renderer's input representation is unchanged after the call
- [ ] No renderer reads environment variables, files, or network resources during render
- [ ] No renderer writes any file or process state during render

## Out of Scope

- Generating the embedding vectors that drive coordinates in the shared representation — see embeddings (note: coordinates produced there flow into this kit's representation)
- Building the graph from sources — see graph-core and environment-indexers
- Choosing which renderer to invoke at which moment of the autoresearch loop — see autoresearch-tree-skill
- Interactive or animated renderers — only static text outputs are required by this kit

## Cross-References

- See also: cavekit-graph-core.md (R1 nodes, R2 edges, R5 recursive bodies)
- See also: cavekit-embeddings.md (provides the coordinate values consumed in R1 tokens)
- See also: cavekit-chain-engine.md (chain shapes consumed by R4 and R5)
- See also: cavekit-autoresearch-tree-skill.md (selects renderers per iteration)
