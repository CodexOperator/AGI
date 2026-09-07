---
id: task:t-062
mint_id: 3c891e92203041eba8d572825688fde2
type: task
parents:
  - hyp:renderers-r2
acceptance_criteria:
  - R2.3 (output includes per-type count and edge summary)
blocked_by:
  - task:t-061
cavekit_req: renderers/R2
edited_by: season.py
effort: S
origin: build-site
season: 1
status: deprecated
tags:
  - S
  - tier--1
thought_session: season
tier: -1
title: "T-062: ASCII renderer — type counts and edge summary"
---
**Description:** Append a footer block with `Types: {type: count}` and `Edges: {relation: count}` lines.

**Files:** `agi-tree/src/renderers/ascii.py`, `agi-tree/tests/renderers/test_ascii_summary.py`

**Test Strategy:** Fixture with known type and edge mix; assert footer counts match.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R2` under `hyp:renderers-r2`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:renderers-r2-by-citation` citing `build:src-renderers-ascii`, `build:tests-renderers-test-ascii`, `build:tests-renderers-test-ascii-summary`: `ascii.py` is the bounded ASCII renderer with a type/edge summary; `test_ascii.py` and `test_ascii_summary.py` pin byte-equal output.
<!-- THOUGHT:END -->