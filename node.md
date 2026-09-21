---
id: experiment:a00-ed255cc3-a0ee73
mint_id: ae2a4ac4840846be9621129598de8521
type: experiment
parents:
  - hypothesis:l4-commit-all-is-legal-on-the-season-main-only
next_edges: []
confidence: 0.85
edited_by: a00-de6c51f7
evidence_runs:
  - experiment:a00-ed255cc3-a0ee73
loop: hypothesis:l4-commit-all-is-legal-on-the-season-main-only@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 049b22009957b2a5
season: 2
title: A00 ed255cc3 a0ee73
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ed255cc3-a0ee73
## Experiment

Pre-fix state measured: `grid.py:870`'s commit --all guard delegated to
`branches.is_legal_branch` (branches.py), which returned True for `master` OR
any name `parse()` admits — so `commit --all` was legal on every live branch
(loop/post/town, canonical and legacy spellings). The hypothesis's pre-fix
defect (L4.307 demoted) was the opposite error: the old `startswith("season/")`
rule *rejected* season/s2 itself, so the 5-min grid cron exited 2. The claim
is a BUILD: name exactly what commit --all may run on.

WHAT I BUILT:
- `branches.py is_legal_branch` (function + docstring ONLY): True for `master`
  or the season MAIN — canonical `season<N>/main` or its one-season alias
  `season/s<N>`; recurses on an alias and accepts it only when its canonical
  parses kind == "main" (so town aliases that canonicalise to a town_main, and
  post/loop aliases to a post/loop, stay refused). Refuses every post, loop and
  town MAIn branch in BOTH spellings, feature branches, malformed names, empty/
  detached HEAD.
- `test_branches.py`: the four kid-era accept tests for canonical post / loop /
  town-main FLIP to refusals; season/s2 + master stay accepted; legacy
  spellings (seat/x@s2, loop/a-b@s2, town/x/season/s1, town/x@s2) are new
  refusals.
- `test_grid.py`: `season_live_branch` fixture, 9 cases (canonical post/loop/
  town-main, legacy post/loop/town-main/town, loose season/ideas/flock, feature
  branch) — each must exit 2 naming the branch AND `--allow-branch`.

## Evidence

UNIT (branches + grid suites):
    env -u TMUX -u TMUX_PANE python3 -m pytest \
      extensions/agi/tests/test_branches.py extensions/agi/tests/test_grid.py -q
    => 161 passed in 19.90s
  (knew one parametrize-as-fixture false start; fixed by pytest.fixture(params=...))

REAL TREE (proof 3, first half): from my own kid worktree, branch
`season2/loops/hypothesis-l4-commit-all-is-lega-a00-de6c51f7`:
    python3 extensions/agi/bin/grid.py commit --all
    => grid: refusing commit --all on 'season2/loops/hypothesis-l4-commit-all-is-lega-a00-de6c51f7', node refs are branch-blind; merge to master first or pass --allow-branch
    => EXIT=2   (refusal names the branch and the flag; nothing committed)

REAL TREE (proof 3, second half, read-only — MAIN's branch name parses legal):
    is_legal_branch("season/s2")  => True   (alias -> season2/main)
    is_legal_branch("season2/main") => True
    is_legal_branch("seat/x@s2")  => False ; len("loop/a-b@s2")/town/x@s2 => False

## Agent Notes
g15 build: is_legal_branch admits ONLY master + season MAIN (season<N>/main | season/s<N>); post/loop/town in both spellings, feature, loose season(season/ideas/flock), empty all refused; 161 unit tests pass; real tree commit --all on season2/loops/... exits 2 naming branch + --allow-branch; season/s2 and season2/main confirmed legal

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.311: accepted as proved. Claim is a BUILD (is_legal_branch = master or the season MAIN only), and the kid implemented it, not merely reproduced the defect. Verified independently: (1) branches.py:is_legal_branch now recurses on aliases and admits only parse(kind)=="main"; (2) my own probe returns True for master/season2/main/season/s2 and False for season2/posts/x, season2/loops/x-a, seat/x@s2, loop/a-b@s2, season2/core/season1/main, town/core@s2, feature/x, "", season/ideas/flock — exactly the CLAIM; (3) 161 passed in 17.82s under the claim command, re-run by me, not pasted from the kid; (4) grid.py is untouched (git status shows no grid.py), so the guard call site and message are unchanged and only the predicate moved. The four kid-era accept tests really flipped to refusals and the legacy spellings are new refusals, so the build is not vacuous.
<!-- THOUGHT:END -->
