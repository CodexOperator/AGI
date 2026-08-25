---
acceptance_criteria:
  - R1.1 (new skill at documented path inside existing autoresearch skill repository)
  - R1.2 (no file under autoresearch-create or autoresearch-finalize modified or removed)
  - R1.3 (adding the skill is one new directory of files
  - not a patch)
  - R1.4 (after installation
blocked_by:
  - task:t-088
cavekit_req: autoresearch-tree-skill/R1
effort: M
id: "task:t-076"
mint_id: 2ebf321e638e44f3a6f4fd15cf1bed18
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r1
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-076: Skill installation in forked skill repository"
type: task
---

**Description:** Place the new skill at `agi-tree/skills/autoresearch-tree/` with its own SKILL.md, scripts/, and references/. Document the installation path and confirm the layout doesn't touch existing skills. Provide an `install-skill.sh` that copies the directory into a target skill repo without modifying anything else.

**Files:** `agi-tree/skills/autoresearch-tree/SKILL.md`, `agi-tree/skills/autoresearch-tree/scripts/`, `agi-tree/skills/autoresearch-tree/references/`, `agi-tree/skills/autoresearch-tree/install-skill.sh`, `agi-tree/tests/skill/test_skill_installation.py`

**Test Strategy:** Test installs into a tempdir mirroring an existing skill repo with create/finalize subdirs; asserts those are byte-equal before and after install and the new skill appears in `find skills/ -name SKILL.md` enumeration.
