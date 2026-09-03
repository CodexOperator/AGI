---
id: task:t-085
mint_id: 491cfbb6665d4046857050adf8f27535
type: task
parents:
  - hyp:autoresearch-tree-skill-r7
acceptance_criteria:
  - R7.1 (single command runs at least one full iteration end-to-end)
  - R7.4 (driver respects config without code changes)
blocked_by:
  - task:t-077
  - task:t-078
  - task:t-080
  - task:t-081
  - task:t-084
cavekit_req: autoresearch-tree-skill/R7
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-085: Driver script — single iteration end-to-end"
---
**Description:** Implement `agi-tree run` CLI invoking decision → dispatch → verdict-emission → benchmark → record, all reading `context/config/`.

**Files:** `agi-tree/src/skill/driver.py`, `agi-tree/src/skill/cli.py`, `agi-tree/tests/skill/test_driver_iteration.py`

**Test Strategy:** End-to-end fixture with stub builder; assert the iteration completes, records exist, and editing config affects behavior.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R7` under `hyp:autoresearch-tree-skill-r7`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r7-by-citation` citing `build:driver.sh`: `driver.sh` is the single-command end-to-end driver.
<!-- THOUGHT:END -->
