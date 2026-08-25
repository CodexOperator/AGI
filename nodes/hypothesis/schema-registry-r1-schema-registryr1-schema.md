---
confidence: 0.5
id: "hyp:schema-registry-r1"
mint_id: adea558d09a24134a14a27d4cd234d9b
origin: build-site
parents:
  - idea:domain-schema-registry
subgraph: false
tags:
  - schema-registry
  - R1
testable_claim: Schema as File
title: "schema-registry/R1: Schema as File"
type: hypothesis
---

**Description:** Each schema is a single file in a known directory of the project's context. Adding, editing, or removing a schema requires only file operations.

**Acceptance Criteria:**
- [ ] A schema file lives at a known path under the context directory and follows a documented naming convention
- [ ] Adding a new schema file makes its node type available without code changes or process restart
- [ ] Removing a schema file makes the corresponding type unavailable on next load and existing nodes of that type fall back to generic handling with a warning
- [ ] Either Markdown-with-frontmatter or a structured-data file format is accepted as a schema container

**Dependencies:** graph-core (R4 frontmatter persistence)
