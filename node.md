---
id: hyp:schema-registry-r1
mint_id: adea558d09a24134a14a27d4cd234d9b
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
  - R1
testable_claim: Schema as File
thought_session: season
title: "schema-registry/R1: Schema as File"
---
**Description:** Each schema is a single file in a known directory of the project's context. Adding, editing, or removing a schema requires only file operations.

**Acceptance Criteria:**
- [ ] A schema file lives at a known path under the context directory and follows a documented naming convention
- [ ] Adding a new schema file makes its node type available without code changes or process restart
- [ ] Removing a schema file makes the corresponding type unavailable on next load and existing nodes of that type fall back to generic handling with a warning
- [ ] Either Markdown-with-frontmatter or a structured-data file format is accepted as a schema container

**Dependencies:** graph-core (R4 frontmatter persistence)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); already closed by `verdict:schema-registry-r1` before this pass; deprecated with its domain (`idea:domain-schema-registry`).
<!-- THOUGHT:END -->