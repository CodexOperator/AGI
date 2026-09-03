---
id: task:t-086
mint_id: ccdbc0d6416c48598bbe943497fc370a
type: task
parents:
  - hyp:autoresearch-tree-skill-r7
acceptance_criteria:
  - R7.2 (driver exits non-zero when iteration fails to record metrics)
  - R7.3 (driver writes per-iteration summary to documented location inside context dir)
blocked_by:
  - task:t-085
cavekit_req: autoresearch-tree-skill/R7
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-086: Driver — error handling and per-iteration summary"
---
**Description:** Driver writes summary at `context/iterations/<n>/summary.md` with the decision, action counts, verdicts emitted, and metrics. On metric-record failure, exit with code 2.

**Files:** `agi-tree/src/skill/driver.py`, `agi-tree/tests/skill/test_driver_summary.py`

**Test Strategy:** Force the bench recorder to fail; assert exit code 2 and an error line in stderr. Successful run produces summary.md.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `autoresearch-tree-skill/R7` under `hyp:autoresearch-tree-skill-r7`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r7-by-citation` citing `build:driver.sh`: `driver.sh` is the single-command end-to-end driver.
<!-- THOUGHT:END -->
