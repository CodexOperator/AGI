---
acceptance_criteria:
  - R5.1 (renderer accepts exactly two run identifiers belonging to same chain; mismatched pairs rejected with structured error)
  - R5.2 (added/removed/changed fields appear with conventional diff markers)
  - R5.3 (identical runs → empty diff with one-line note rather than blank string)
  - R5.4 (only printable ASCII characters)
blocked_by:
  - task:t-060
cavekit_req: renderers/R5
effort: M
id: "task:t-065"
mint_id: 1c106b0b8962438b9ddece71191717c5
origin: build-site
parents:
  - hyp:renderers-r5
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-065: Git-diff renderer"
type: task
---

**Description:** Implement `GitDiffRenderer.render(rep, run_a_id, run_b_id) -> str`. Validate both runs exist on the same chain; otherwise raise `MismatchedRunsError`. Use `+`/`-`/`~` markers per field. Identical → "no differences" line.

**Files:** `agi-tree/src/renderers/git_diff.py`, `agi-tree/tests/renderers/test_git_diff.py`

**Test Strategy:** Three fixtures: same chain different runs (diff produced), different chains (error raised), identical runs (single-line note).
