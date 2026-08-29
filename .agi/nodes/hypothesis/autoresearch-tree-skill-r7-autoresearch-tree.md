---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r7"
mint_id: e7e1705e912f44bd958e9ed4397cd8d0
origin: build-site
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R7
testable_claim: Driver Script
title: "autoresearch-tree-skill/R7: Driver Script"
type: hypothesis
---

**Description:** A driver script orchestrates one or more loop iterations analogously to the predecessor project's driver.

**Acceptance Criteria:**
- [ ] A single command starts the driver and runs at least one full iteration end-to-end
- [ ] The driver exits with a non-zero status when any iteration fails to record metrics
- [ ] The driver writes a per-iteration summary to a documented location inside the project context directory
- [ ] The driver respects the configuration file's parameters without code changes
