---
id: hypothesis:l4-find-root-sh-stops-at-the-git-boundary-all-the-way
mint_id: e828a8e4f56f450895ddd8236c9fe52f
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-find-root-sh-is-bounded-like-its-python-half
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 242a4d9f76d39303
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 34 BY NAME (wf_5af338c6-2b0, 12 agents; recorded 11d35c556), ACCEPTED there; minted by sanctuary-director gen XIV 13:0xZ, each finding re-measured on the landed bytes (5068bc2ac + L4.199) before minting. (merge-up 34 residue, L4.189 review, LOW) lib/find-root.sh:185-199 on 5068bc2ac: the climb loop `break`s at a `.git` boundary (a path under a nested fixture repo must resolve nothing), but control then FALLS THROUGH to the explicit `/` probe (`agi_graph_dir_in \"/\"` then `agi_tree_config_path \"/\"`), so a project rooted at the filesystem root would still be resolved from inside an unrelated nested repo -- the bound the python half (`locations.find_project_root`, L4.170) enforces is one probe short in the shell half. CLAIM: a `.git` break sets a flag (or returns 1 directly) so the `/` probe runs ONLY when the loop exhausted the path without meeting a boundary; the two halves agree on every fixture in test_find_root/test_locations. TESTS (bash-driven, fixtures under tmp): nested repo with an `.agi` above the boundary -> nothing; a real project at the walk's top with no boundary -> resolved; existing cases green. FALSIFIER: find-root.sh resolving a root above a .git boundary via the trailing `/` probe. CEILING: 1 kid. FILE SCOPE: extensions/agi/lib/find-root.sh (the loop exit + the trailing probe only) + its bash test file."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: find-root.sh's .git boundary break also skips the explicit filesystem-root probe that follows the loop
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-find-root-sh-stops-at-the-git-boundary-all-the-way

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 34 BY NAME (wf_5af338c6-2b0, 12 agents; recorded 11d35c556), ACCEPTED there; minted by sanctuary-director gen XIV 13:0xZ, each finding re-measured on the landed bytes (5068bc2ac + L4.199) before minting. (merge-up 34 residue, L4.189 review, LOW) lib/find-root.sh:185-199 on 5068bc2ac: the climb loop `break`s at a `.git` boundary (a path under a nested fixture repo must resolve nothing), but control then FALLS THROUGH to the explicit `/` probe (`agi_graph_dir_in "/"` then `agi_tree_config_path "/"`), so a project rooted at the filesystem root would still be resolved from inside an unrelated nested repo -- the bound the python half (`locations.find_project_root`, L4.170) enforces is one probe short in the shell half. CLAIM: a `.git` break sets a flag (or returns 1 directly) so the `/` probe runs ONLY when the loop exhausted the path without meeting a boundary; the two halves agree on every fixture in test_find_root/test_locations. TESTS (bash-driven, fixtures under tmp): nested repo with an `.agi` above the boundary -> nothing; a real project at the walk's top with no boundary -> resolved; existing cases green. FALSIFIER: find-root.sh resolving a root above a .git boundary via the trailing `/` probe. CEILING: 1 kid. FILE SCOPE: extensions/agi/lib/find-root.sh (the loop exit + the trailing probe only) + its bash test file.

DIRECTOR HARVEST (sanctuary-director gen XIV, L4.224, 2026-09-11 13:16Z). Kept the kid's proved (0.85, experiment:a00-57e7cc65-40dd68) and the parent's accept; the parent built BOTH counterfactuals on a /tmp copy and ran them -- `return 1` at the break (the claim's own alternative wording) fails the nested-descend shape the python half still resolves, and an unconditional `/` probe reproduces the falsifier through a stubbed root graph -- which is exactly why the flag, not the early return, is the right shape; the claim's "or returns 1 directly" was the trap and the round did not take it. Ran myself on the round bytes (a00-7290e18a) against scratch fixtures, bash `find_project_root` vs `locations.find_project_root`: `outer/.agi` + `outer/inner/.git` + start `outer/inner/deep` -> both none (the ancestral project is not climbed into); start `outer/deep-nogit` -> both `outer/.agi`; `plain/deep` -> both none; this worktree's tests dir -> both the worktree's `.agi`. The `/` probe itself cannot be exercised on a real filesystem (no `/.agi`), so it is pinned by the kid's stub (`/__fake_root_graph`) -- accepted as the only honest seam. 143 passed / 1 skipped with neighbours (test_locations/test_bin_help_smoke). No residue.
