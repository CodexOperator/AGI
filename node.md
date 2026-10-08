---
id: hypothesis:l5-relative-worktree-cell-resolution-has-no-committed-test-coverage
mint_id: bd26f1b8c6664911befbbd89f7646ba5
type: hypothesis
parents:
  - hypothesis:l5-rename-surfaces-and-the-successor-brief-resolve-from-the-rotating-worktree-root
next_edges: []
edited_by: director-belam
scaffold_hash: 095e9f819e9bf484
season: 2
testable_claim: "mur-l5-11's 11 committed tests pin rotate.py's _own_sessions_dir (rotate.py:3554) and _own_card_path (rotate.py:7586) only against ABSOLUTE worktree cells -- none constructs a seat row with a RELATIVE worktree cell (e.g. \".agi/worktrees/post-sensei-director\"), which is the shape live seat rows actually carry (mur-l5-11 review defect 2). belam proved the relative case once, by hand, in-process at the L5.11 merge (_own_sessions_dir resolves the relative cell to that worktree's own sessions dir; the template brief re-roots to .../post-sensei-director/.agi/sessions/quorum/director-sanctuary.md) -- an uncommitted manual proof pins nothing against regression. Fix: add a committed test constructing a seat row with a RELATIVE worktree cell and asserting _own_sessions_dir / _own_card_path resolve it identically to the existing absolute-cell tests. Dispatch held until sensei-director's live rotation (belam-ordered, merge-main-then-rotate) reports back -- that live run is the first real proof and the test should pin what it demonstrates, not a guess ahead of it (belam ruling 22:11:40Z)."
title: L5 relative worktree cell resolution has no committed test coverage
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-relative-worktree-cell-resolution-has-no-committed-test-coverage

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
