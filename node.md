---
id: hyp:graph-core-r4
mint_id: f4973464177f4017be7a09080bedec55
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - graph-core
  - R4
testable_claim: Frontmatter File Persistence
thought_session: season
title: "graph-core/R4: Frontmatter File Persistence"
---
**Description:** Each node persists as a standalone file with a structured frontmatter header and a free-form body. Bodies are not loaded into memory until a node is visited.

**Acceptance Criteria:**
- [ ] Loading the graph reads only frontmatter; body content is fetched on first access to that node's body
- [ ] A node file round-trips: load then save produces a byte-for-byte equivalent file modulo whitespace normalization
- [ ] Either Markdown-with-YAML-frontmatter or pure structured-data files (such as JSON) are accepted as node containers
- [ ] A malformed frontmatter block produces a structured error naming the offending file and does not abort the rest of the load

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r4-by-citation` citing `build:src-graph-core-persistence-frontmatter`, `build:src-graph-core-persistence-lazy-body`, `build:tests-graph-core-test-frontmatter`, `build:tests-graph-core-test-frontmatter-errors`, `build:tests-graph-core-test-lazy-body`: `persistence/frontmatter.py` is the round-tripping reader/writer with one failure class (`FrontmatterError`) and `lazy_body.py` the lazy body read; the three suites cover round-trip, error isolation and laziness.
<!-- THOUGHT:END -->