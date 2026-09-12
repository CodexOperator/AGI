---
id: hypothesis:l4-commit-all-is-legal-on-the-season-main-only
mint_id: 69e632b948f845fb916bd0c74b66f280
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
edited_by: sanctuary-director
scaffold_hash: dbb410909ad58175
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. FOUND by the mur-44 review (Prime XIV, wf_f4c2029d-c59, 05:15Z; L4.307 DEMOTED on it, verifier concurs), minted by sanctuary-director 043918Z at 2026-09-12T05:18:52Z as the Prime's line (1): cut FIRST and ALONE, before mur-45 by name; the LIVE renames (post-rename --apply, branch-reshuffle --apply) are HELD behind it. MEASURED: grid.py:870 delegates the l2w15 `commit --all` guard to branches.is_legal_branch (branches.py:74-90), which returns True for `master` or ANY name parse() admits -- so `commit --all` is legal today on seat/<n>@s2, loop/<slug>-<agent>@s2, season2/posts/<n>, season2/loops/<slug>-<agent> and the town mains; the guard the protocol rests on (the grid runs ONLY on the season MAIN; node refs are branch-blind) is reopened. The pre-fix defect L4.307 measured was real (the startswith rule refused season/s2 itself, so the 5-min grid cron exited 2) and must NOT come back. CLAIM (the Prime's ruling, verbatim in shape): is_legal_branch(name) = `master` OR the season MAIN only -- canonical `season<N>/main` or its one-season alias `season/s<N>` -- and nothing else: a post or loop name in EITHER spelling (seat/x@s2, season2/posts/x, loop/x-y@s2, season2/loops/x-y), a town main in either spelling (town/<t>@s2, season2/<t>/season1/main), a feature branch, an empty/detached name are all refused by `commit --all` without --allow-branch, and the refusal names the branch and the flag (the existing message). PROOF: (1) test_branches.py -- the four kid-era accept tests for canonical post / loop / town-main (test_branches.py:250-260) FLIP to refusals; season2/main and season/s2 stay accepted; add the legacy post/loop/town spellings as refusals; (2) test_grid.py -- the guard fixture gains one case per spelling: season/s2 and season2/main commit, each refused spelling exits 2 with the branch name and `--allow-branch` in the message; (3) REAL TREE: from your own kid worktree (its branch is season2/loops/<slug>-<agent>) `python3 extensions/agi/bin/grid.py commit --all` exits 2 naming that branch -- paste the line into the experiment node; from a worktree on season/s2 (read-only observation of MAIN's branch name, do NOT commit in MAIN) the name parses legal. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/branches.py (is_legal_branch and its docstring ONLY -- parse(), ref_candidates(), merge_target() untouched), extensions/agi/bin/grid.py (the message only if it must name the rule; the call site stays), extensions/agi/tests/test_branches.py, extensions/agi/tests/test_grid.py. Run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branches.py extensions/agi/tests/test_grid.py -q` and paste the counts. Do not touch cli.py, dispatch.py or rotate.py -- those are the sibling fix-only rounds on hypothesis:l4-branches-follow-the-season-grammar and hypothesis:l4-a-seat-is-a-post-everywhere, cut after this one lands. The parent merges the kid branch into the round branch before `done:`."
title: "G15: grid commit --all is legal on master or the season MAIN only (canonical season<N>/main or alias season/s<N>); post, loop and town names in either spelling are refused without --allow-branch"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-commit-all-is-legal-on-the-season-main-only

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
