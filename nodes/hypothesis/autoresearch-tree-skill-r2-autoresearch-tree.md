---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r2"
mint_id: 3c8adedcbb984d919d34d80d44f101c3
origin: build-site
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R2
testable_claim: Big-Idea-Versus-Small-Idea Decision Per Iteration
title: "autoresearch-tree-skill/R2: Big-Idea-Versus-Small-Idea Decision Per Iteration"
type: hypothesis
---

**Description:** Every iteration begins with an explicit decision between exploring a big idea or a small idea. The split is governed by a configuration parameter shared with chain-engine.

**Acceptance Criteria:**
- [ ] Each iteration emits a record naming the chosen path (big idea or small idea) before any agent is dispatched
- [ ] The probability of choosing the big-idea path equals the configured `big_idea_vs_small_idea_split`
- [ ] Two consecutive iterations with the same seed and configuration produce the same choice
- [ ] When the configuration value is missing or out of range, the iteration aborts with a structured error

**Dependencies:** chain-engine (R7 configuration file)
