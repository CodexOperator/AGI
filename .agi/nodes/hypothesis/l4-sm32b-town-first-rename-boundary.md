---
id: hypothesis:l4-sm32b-town-first-rename-boundary
mint_id: 70ee744c61564cbb8c6ad8c4be776fbf
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: adebad8f6a6cc85a
season: 2
testable_claim: "SM.32b (SM review 08:3xZ on the town-cell merge-up, mur wf_9cedfafb-a6e): claims (1)/(2) of hypothesis:l4-the-keep-and-director-rows-carry-their-real-town-cell-and-a-live-cell-change-is-a-measured-rename-at-the-posts-boundary, FALSIFIED by kid2 (experiment:a00-5cf0cbf4-7f911b) and left for a follow-on round. MEASURED (kid2, live probes): rotate.py rename-post sanctuary-helper ... --dry-run still emits the legacy town-less branch spelling season2/posts/sanctuary-helper -> season2/posts/sanctuary-helper-zzz, and refs/heads/season2/posts has ZERO refs (live branches are core/season2/posts/<post>/main, town-first already in the PATH, not town-aware in the rename LOGIC); rotate.py contains no row_town/accepted_towns/town-cell read anywhere -- no rotation boundary consults the config:posts town cell added by claim (3)/(4). CLAIM: (1) the rename boundary (rotate.py rename-post and any rotate-self self-rename path) reads the row town cell via the same config_town_cell/_is_nonprime_row-style helper claims 3/4 already established (never re-derive), and a rename that would move a post OUT of its declared town is a NAMED refusal, never silent; (2) the branch-naming scheme itself already carries the town in the path (core/season2/posts/<post>/main) so claim (2) narrows to: rename tooling ASSERTS the town segment matches the row town cell before renaming, rather than inventing a new town-first branch scheme. FALSIFIERS: a rename that changes a post row town cell without a refusal path; a rename tool that still has zero town-cell reads after this lands; a branch created whose town path segment disagrees with the row town cell. PRECONDITIONS (real, not yet both met): SM.29 (viewport theme sanctuary->keep) is on MAIN already; the SM.25 real-mirror-mechanism work (SM.250, live as of gen24) is NOT yet landed -- do not dispatch this node until SM.250 lands, since the rename path this touches is adjacent to what SM.25 changes. TESTS: extend test_rotate.py + test_town_rows_readers.py (rename-post dry-run against a mismatched town cell refuses named; matching cell proceeds; branch path segment assertion). FILE SCOPE: rotate.py (rename-post + self-rename paths only), test_rotate.py, test_town_rows_readers.py. CEILING: <=60 production lines, ONE kid."
title: L4 sm32b town first rename boundary
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sm32b-town-first-rename-boundary

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: rename-post still emits `branches.post_branch(2, old/new)` and `origin/<season-first>` surfaces (rotate.py:3464-3467, MEASURED sed) while rotate.py has 0 hits for row_town EVIDENCE: config_town_cell Never rounded at close (owner 14:1xZ).
