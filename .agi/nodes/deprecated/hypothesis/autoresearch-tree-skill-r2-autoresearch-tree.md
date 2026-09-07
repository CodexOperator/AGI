---
id: hyp:autoresearch-tree-skill-r2
mint_id: 3c8adedcbb984d919d34d80d44f101c3
type: hypothesis
parents:
  - idea:domain-autoresearch-tree-skill
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - autoresearch-tree-skill
  - R2
testable_claim: Big-Idea-Versus-Small-Idea Decision Per Iteration
thought_session: season
title: "autoresearch-tree-skill/R2: Big-Idea-Versus-Small-Idea Decision Per Iteration"
---
**Description:** Every iteration begins with an explicit decision between exploring a big idea or a small idea. The split is governed by a configuration parameter shared with chain-engine.

**Acceptance Criteria:**
- [ ] Each iteration emits a record naming the chosen path (big idea or small idea) before any agent is dispatched
- [ ] The probability of choosing the big-idea path equals the configured `big_idea_vs_small_idea_split`
- [ ] Two consecutive iterations with the same seed and configuration produce the same choice
- [ ] When the configuration value is missing or out of range, the iteration aborts with a structured error

**Dependencies:** chain-engine (R7 configuration file)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no seeded big/small binary-decision mechanism was found in `dispatch.py`/`driver.sh` (uncertain rather than confident -- the full iteration-selection logic was not traced); `goal:g4.6`/`goal:g4.7` are this domain's real goals and do not obviously cover this item, so this THOUGHT is the record.
<!-- THOUGHT:END -->