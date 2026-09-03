---
id: task:t-064
mint_id: 0b043384d0e64957b206b3eb265d0da3
type: task
parents:
  - hyp:renderers-r4
acceptance_criteria:
  - R4.1 (each chain → one branch-shaped lane)
  - R4.2 (lane order deterministic
  - rooted in highest-scoring chain)
  - R4.3 (merge points → visible junction)
  - R4.4 (only printable ASCII characters)
blocked_by:
  - task:t-060
  - task:t-049
cavekit_req: renderers/R4
edited_by: l1.09-execution-parent
effort: L
origin: build-site
status: deprecated
tags:
  - L
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-064: Git-tree renderer"
---
**Description:** Implement `GitTreeRenderer.render(rep, chains) -> str`. Lays out chains as parallel lanes using ASCII glyphs `|/\*`. Lane 0 is the highest-scoring chain. Merge junctions render as `*`. Restrict character set to printable ASCII via assertion.

**Files:** `agi-tree/src/renderers/git_tree.py`, `agi-tree/tests/renderers/test_git_tree.py`

**Test Strategy:** Three-chain fixture: assert lane order, merge symbol presence, ASCII-only via `output.isascii()`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R4` under `hyp:renderers-r4`, whose disposition is disposition GENUINELY-OPEN, not run: no `git_tree.py` anywhere in the tree; no existing goal obviously covers a git-tree renderer with lanes and merge junctions, so this THOUGHT is the record.
<!-- THOUGHT:END -->
