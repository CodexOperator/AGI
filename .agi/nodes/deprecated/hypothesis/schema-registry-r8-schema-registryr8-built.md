---
id: hyp:schema-registry-r8
mint_id: c15b12ebc5594c4c985075fea10dd0ba
type: hypothesis
parents:
  - idea:domain-schema-registry
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - schema-registry
  - R8
testable_claim: Built-In Schemas for Autoresearch Types
thought_session: season
title: "schema-registry/R8: Built-In Schemas for Autoresearch Types"
---
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r8-by-citation` citing `build:src-schema-registry-active-set`, `build:src-schema-registry-loader`, `build:tests-schema-registry-test-brackets`, `build:tests-schema-registry-test-schema-files`: `.agi/context/schemas/[*].md` is the real built-in schema set (a superset of the fictional eight, adapted to this project's taxonomy); bracket override is `active_set.py` and `loader.py::_generic_schema()` is the fallback for a missing schema.
<!-- THOUGHT:END -->