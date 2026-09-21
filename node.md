---
id: idea:domain-autoresearch-tree-skill
mint_id: 864d54affd61407188e6cc3c042c45f2
type: idea
next_edges:
  - hyp:autoresearch-tree-skill-r1
confidence: 1.0
edited_by: season.py
origin: build-site
scale: big
season: 1
status: deprecated
tags:
  - domain
  - seed
thought_session: season
title: "Domain: autoresearch-tree-skill"
---
The agent skill that drives the autoresearch loop on top of the rest of the system. It forks an existing autoresearch skill family rather than modifying it, picks between big-idea and small-idea exploration each iteration, dispatches parallel builder agents, accepts their experiment results as verdict emissions, and runs a benchmark harness that extends the predecessor harness with new chain-shaped metrics. The skill must be drop-in portable: it should run in any repository where the project context directory has been added.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §B/§D/§E): the domain is built as `extensions/agi/bin/dispatch.py`, `bin/heal.py` and `driver.sh`, and `goal:g4.6`/`goal:g4.7` are its goals under different vocabulary; no new goal (§B).
<!-- THOUGHT:END -->