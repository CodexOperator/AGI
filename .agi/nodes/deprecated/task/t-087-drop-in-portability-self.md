---
id: task:t-087
mint_id: 434c7b467e5643078199c8d4bf582c80
type: task
parents:
  - hyp:autoresearch-tree-skill-r8
acceptance_criteria:
  - R8.1 (self-test runs skill in fresh empty repository where only context dir copied; first iteration completes)
  - R8.2 (no code path inside skill assumes repo name/host path/env beyond optional model selector)
  - R8.3 (removing context dir from repo removes all skill-managed state)
  - R8.4 (skill documentation states portability contract and self-test command)
blocked_by:
  - task:t-086
  - task:t-017
cavekit_req: autoresearch-tree-skill/R8
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-087: Drop-in portability self-test for the skill"
---
**Description:** Implement `agi-tree self-test skill-portability`: copy the project's `context/` to a tempdir, run a single skill iteration there, assert success. Audit the skill code for absolute paths or unauthorized env reads. Document the contract in SKILL.md.

**Files:** `agi-tree/src/skill/self_test.py`, `agi-tree/skills/autoresearch-tree/SKILL.md`, `agi-tree/tests/skill/test_skill_portability.py`

**Test Strategy:** Self-test in tempdir asserts exit 0. Static audit asserts no unauthorized environment reads. Removal test confirms no residual files outside `context/`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R8` under `hyp:autoresearch-tree-skill-r8`, whose disposition is disposition GENUINELY-OPEN, not run: no formal drop-in self-test, though the skill is symlink-portable by construction (`CLAUDE.md`: everything reachable globally by symlink) -- informally true, not testably proven; this THOUGHT is the record.
<!-- THOUGHT:END -->