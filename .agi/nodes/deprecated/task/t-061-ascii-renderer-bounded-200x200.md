---
id: task:t-061
mint_id: fdc08817119748c3aab46ad1aa515310
type: task
parents:
  - hyp:renderers-r2
acceptance_criteria:
  - R2.1 (output ≤ 200 lines
  - ≤ 200 columns)
  - R2.2 (oversize → compress or truncate with visible marker
  - no overflow)
  - R2.4 (two runs on same graph → byte-equal output)
blocked_by:
  - task:t-060
cavekit_req: renderers/R2
edited_by: l1.09-execution-parent
effort: L
origin: build-site
status: deprecated
tags:
  - L
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-061: ASCII renderer — bounded 200x200 with truncation marker"
---
**Description:** Implement `AsciiRenderer.render(rep) -> str`. Hierarchical layout (depth-driven indent). Bounded by 200 lines and 200 cols; on overflow, emit `... [truncated, N more nodes]` and `... [line cut at column 200]` markers. Byte-equal across runs (driven by deterministic representation).

**Files:** `agi-tree/src/renderers/ascii.py`, `agi-tree/tests/renderers/test_ascii.py`

**Test Strategy:** Run against a 1000-node fixture; assert max line length and total lines. Byte-equality test on two consecutive runs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R2` under `hyp:renderers-r2`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:renderers-r2-by-citation` citing `build:src-renderers-ascii`, `build:tests-renderers-test-ascii`, `build:tests-renderers-test-ascii-summary`: `ascii.py` is the bounded ASCII renderer with a type/edge summary; `test_ascii.py` and `test_ascii_summary.py` pin byte-equal output.
<!-- THOUGHT:END -->
