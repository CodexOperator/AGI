---
id: task:t-088
mint_id: 0bc1df14bc894abba325a6cc65548f0d
type: task
parents:
  - hyp:autoresearch-tree-skill-r1
acceptance_criteria:
  - (supporting task; criteria fully covered under T-076 via the install-skill payload structure)
blocked_by: []
cavekit_req: autoresearch-tree-skill/R1
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-088: Skill repository scaffolding (forked autoresearch skills layout)"
---
**Description:** Pre-create the directory tree under `agi-tree/skills/autoresearch-tree/` so T-076's installer has files to install. This is a structural-only task that prepares the payload; the criteria coverage is validated under T-076.

**Files:** `agi-tree/skills/autoresearch-tree/.gitkeep`, `agi-tree/skills/autoresearch-tree/scripts/.gitkeep`, `agi-tree/skills/autoresearch-tree/references/.gitkeep`

**Test Strategy:** Directory existence test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R1` under `hyp:autoresearch-tree-skill-r1`, whose disposition is already closed by `verdict:autoresearch-tree-skill-r1` before this pass -- a closure §F R1 calls hollow (self-asserted, `evidence_runs: []`, demoted from proved), so it is not treated as evidence; deprecated with its domain (`idea:domain-autoresearch-tree-skill`).
<!-- THOUGHT:END -->
