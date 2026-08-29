---
created: 2026-04-30
last_edited: 2026-04-30
---

# Cavekit: schema-registry

## Scope

A registry of schemas that define what node types exist, what their frontmatter must contain, and how directories of files are interpreted as nodes. Schemas are themselves graph nodes, so the registry is observable from inside the graph. New schemas can be added by dropping a file. When data is encountered that no schema explains, a hook can ask a language model to propose a new schema. This kit is how the autoresearch domain (and any future domain) plugs in without touching graph-core.

## Requirements

### R1: Schema as File

**Description:** Each schema is a single file in a known directory of the project's context. Adding, editing, or removing a schema requires only file operations.

**Acceptance Criteria:**
- [ ] A schema file lives at a known path under the context directory and follows a documented naming convention
- [ ] Adding a new schema file makes its node type available without code changes or process restart
- [ ] Removing a schema file makes the corresponding type unavailable on next load and existing nodes of that type fall back to generic handling with a warning
- [ ] Either Markdown-with-frontmatter or a structured-data file format is accepted as a schema container

**Dependencies:** graph-core (R4 frontmatter persistence)

### R2: Bracket Convention for Active Schemas

**Description:** A schema file whose name is wrapped in brackets is treated as the active schema for the directory tree it lives in. Bracketing is the user's signal of approval.

**Acceptance Criteria:**
- [ ] A schema file whose name is wrapped in brackets is loaded into the active set
- [ ] A schema file without brackets is loaded into the registry but marked inactive and excluded from auto-discovery matching
- [ ] Activating a schema is achieved by renaming the file to add brackets; no other action is required
- [ ] When two bracketed schemas claim the same name, loading fails with a structured error naming both files

### R3: Schemas as Meta-Nodes

**Description:** Every registered schema appears in the graph as a node of type `meta_node` so the graph can describe its own structure.

**Acceptance Criteria:**
- [ ] After load, the graph contains one `meta_node` per registered schema and its id is derived from the schema's name
- [ ] A meta-node's frontmatter exposes the schema's declared fields, defaults, and validation rules
- [ ] Edges from `meta_node` instances to ordinary nodes record which schema validated which node
- [ ] Removing a schema removes its meta-node and the validating edges on next load

**Dependencies:** graph-core (R1 nodes, R2 edges)

### R4: Optional Validation Hooks

**Description:** A schema may declare a validation rule. When set, the rule checks node frontmatter on load.

**Acceptance Criteria:**
- [ ] A schema without a validation rule loads its nodes without per-field checks
- [ ] A schema with a validation rule rejects nodes whose frontmatter violates the rule and emits a structured error per offending node
- [ ] Validation errors do not abort the rest of the load
- [ ] The set of validation results is queryable after load (for example, count of failures per schema)

### R5: Auto-Discovery Cascade

**Description:** When a directory of files is encountered, the registry resolves its node type using a documented cascade: bracketed schema match, then fingerprint similarity against registered schemas, then language-model fallback to propose a new schema, then a generic fallback with a warning.

**Acceptance Criteria:**
- [ ] When a bracketed schema matches the directory by name, that schema is selected and later steps are skipped
- [ ] When no name match exists, the registry compares observed frontmatter shape against registered schemas and selects the best match if its similarity score is at least 0.7
- [ ] When similarity is below the threshold and a language-model hook is available, the hook proposes a schema and the proposal is written without brackets pending user review
- [ ] When all earlier steps fail, the directory is loaded under a generic schema and a warning lists each unmatched file

### R6: Pluggable Language-Model Hook

**Description:** The schema-proposal hook is selected by configuration and degrades gracefully when no model is available.

**Acceptance Criteria:**
- [ ] The hook target is selectable through configuration or environment, not hard-coded
- [ ] When no hook target is configured or reachable, the cascade proceeds to the generic fallback without raising
- [ ] A hook failure (timeout, error response, malformed output) is logged with the offending input and does not abort the load
- [ ] Hook outputs are validated before being written as schema files

### R7: Generated Schemas Land Inactive

**Description:** Schemas produced by the language-model hook are written to the schemas directory without brackets so the user must explicitly activate them.

**Acceptance Criteria:**
- [ ] A hook-generated schema file is written without brackets and is not added to the active set on the same load
- [ ] On subsequent load after a user adds brackets, the schema becomes active
- [ ] A hook-generated schema file carries provenance metadata (timestamp, source directory, hook target) in its frontmatter
- [ ] Two consecutive runs that both invoke the hook for the same directory do not produce duplicate proposal files

### R8: Built-In Schemas for Autoresearch Types

**Description:** A baseline set of schemas ships with the registry to define the autoresearch node types so chain-engine, renderers, and the skill can rely on them.

**Acceptance Criteria:**
- [ ] After bootstrap, the registry contains active schemas named `idea`, `hypothesis`, `experiment`, `verdict`, `mvp`, `outcome`, `bigger_outcome`, and `app_purpose`
- [ ] Each built-in schema declares the fields its corresponding node type must carry, including verdict taxonomy fields where applicable
- [ ] Built-in schemas can be overridden by a user-supplied bracketed schema of the same name without code changes
- [ ] Removing a built-in schema makes downstream features that depend on it report a clear missing-schema error rather than crashing

**Dependencies:** none (consumed by chain-engine, which uses the autoresearch types defined here)

## Out of Scope

- Storage of node data — see graph-core
- Indexing of external sources (code, filesystem trees, OpenAPI specs) — see environment-indexers
- Chain-shaped logic over autoresearch nodes — see chain-engine
- Rendering of meta-nodes alongside ordinary nodes — see renderers

## Cross-References

- See also: cavekit-graph-core.md (R4 frontmatter persistence, R6 directory walking)
- See also: cavekit-environment-indexers.md (each indexer registers or references a schema)
- See also: cavekit-chain-engine.md (uses built-in autoresearch schemas)
- See also: cavekit-renderers.md (may render meta-nodes)
- See also: cavekit-autoresearch-tree-skill.md (relies on built-in schemas to emit verdicts and chain nodes)
