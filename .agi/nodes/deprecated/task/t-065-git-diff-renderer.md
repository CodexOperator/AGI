---
id: task:t-065
mint_id: 1c106b0b8962438b9ddece71191717c5
type: task
parents:
  - hyp:renderers-r5
acceptance_criteria:
  - R5.1 (renderer accepts exactly two run identifiers belonging to same chain; mismatched pairs rejected with structured error)
  - R5.2 (added/removed/changed fields appear with conventional diff markers)
  - R5.3 (identical runs → empty diff with one-line note rather than blank string)
  - R5.4 (only printable ASCII characters)
blocked_by:
  - task:t-060
cavekit_req: renderers/R5
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-065: Git-diff renderer"
---
**Description:** Implement `GitDiffRenderer.render(rep, run_a_id, run_b_id) -> str`. Validate both runs exist on the same chain; otherwise raise `MismatchedRunsError`. Use `+`/`-`/`~` markers per field. Identical → "no differences" line.

**Files:** `agi-tree/src/renderers/git_diff.py`, `agi-tree/tests/renderers/test_git_diff.py`

**Test Strategy:** Three fixtures: same chain different runs (diff produced), different chains (error raised), identical runs (single-line note).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R5` under `hyp:renderers-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:renderers-r5-by-citation` citing `build:src-renderers-git-diff`, `build:tests-renderers-test-git-diff`: `git_diff.py` is the two-run diff renderer with an empty-diff note and `test_git_diff.py` its suite.
<!-- THOUGHT:END -->
