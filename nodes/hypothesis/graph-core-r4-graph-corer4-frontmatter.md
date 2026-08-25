---
confidence: 0.5
id: "hyp:graph-core-r4"
mint_id: f4973464177f4017be7a09080bedec55
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R4
testable_claim: Frontmatter File Persistence
title: "graph-core/R4: Frontmatter File Persistence"
type: hypothesis
---

**Description:** Each node persists as a standalone file with a structured frontmatter header and a free-form body. Bodies are not loaded into memory until a node is visited.

**Acceptance Criteria:**
- [ ] Loading the graph reads only frontmatter; body content is fetched on first access to that node's body
- [ ] A node file round-trips: load then save produces a byte-for-byte equivalent file modulo whitespace normalization
- [ ] Either Markdown-with-YAML-frontmatter or pure structured-data files (such as JSON) are accepted as node containers
- [ ] A malformed frontmatter block produces a structured error naming the offending file and does not abort the rest of the load
