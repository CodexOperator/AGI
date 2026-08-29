---
acceptance_criteria:
  - R8.1 (self-test runs skill in fresh empty repository where only context dir copied; first iteration completes)
  - R8.2 (no code path inside skill assumes repo name/host path/env beyond optional model selector)
  - R8.3 (removing context dir from repo removes all skill-managed state)
  - R8.4 (skill documentation states portability contract and self-test command)
blocked_by:
  - task:t-086
  - task:t-017
cavekit_req: autoresearch-tree-skill/R8
effort: M
id: "task:t-087"
mint_id: 434c7b467e5643078199c8d4bf582c80
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r8
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-087: Drop-in portability self-test for the skill"
type: task
---

**Description:** Implement `agi-tree self-test skill-portability`: copy the project's `context/` to a tempdir, run a single skill iteration there, assert success. Audit the skill code for absolute paths or unauthorized env reads. Document the contract in SKILL.md.

**Files:** `agi-tree/src/skill/self_test.py`, `agi-tree/skills/autoresearch-tree/SKILL.md`, `agi-tree/tests/skill/test_skill_portability.py`

**Test Strategy:** Self-test in tempdir asserts exit 0. Static audit asserts no unauthorized environment reads. Removal test confirms no residual files outside `context/`.
