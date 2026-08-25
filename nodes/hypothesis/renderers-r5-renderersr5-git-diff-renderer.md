---
confidence: 0.5
id: "hyp:renderers-r5"
mint_id: 57ebda5a4768406c862274666d23b32a
origin: build-site
parents:
  - idea:domain-renderers
subgraph: false
tags:
  - renderers
  - R5
testable_claim: Git-Diff Renderer
title: "renderers/R5: Git-Diff Renderer"
type: hypothesis
---

**Description:** A renderer produces a diff view between two experiment runs along the same chain so progression and regression are visible side by side.

**Acceptance Criteria:**
- [ ] The renderer accepts exactly two run identifiers belonging to the same chain and rejects mismatched pairs with a structured error
- [ ] Added, removed, and changed fields appear with conventional diff markers
- [ ] When two runs are identical, the output is an empty diff with a one-line note rather than a blank string
- [ ] The output uses only printable ASCII characters
