---
acceptance_criteria:
  - (supporting task; criteria fully covered under T-076 via the install-skill payload structure)
blocked_by: []
cavekit_req: autoresearch-tree-skill/R1
effort: S
id: "task:t-088"
mint_id: 0bc1df14bc894abba325a6cc65548f0d
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r1
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-088: Skill repository scaffolding (forked autoresearch skills layout)"
type: task
---

**Description:** Pre-create the directory tree under `agi-tree/skills/autoresearch-tree/` so T-076's installer has files to install. This is a structural-only task that prepares the payload; the criteria coverage is validated under T-076.

**Files:** `agi-tree/skills/autoresearch-tree/.gitkeep`, `agi-tree/skills/autoresearch-tree/scripts/.gitkeep`, `agi-tree/skills/autoresearch-tree/references/.gitkeep`

**Test Strategy:** Directory existence test.
