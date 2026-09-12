---
id: experiment:a00-1937f660-8c3362
mint_id: 2b14501f77374b3b9ce9ebdf72206b2d
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.85
edited_by: a00-e20a6d63
evidence_runs:
  - experiment:a00-1937f660-8c3362
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 66db4e221ea82a96
season: 2
title: A00 1937f660 8c3362
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1937f660-8c3362

# experiment:a00-1937f660-8c3362

## Experiment

Clause (2) of hypothesis:l4-branches-follow-the-season-grammar — the span
between "branches are grammar-admitted" and "the tools that gate/name them
still speak the old season/s literal". After the migration the canonical
spelling is `season2/main`, and readers that still test
`branch.startswith("season/")` or emit `season/s<new>` break on it. This run
fixed the three remaining sites and proved them on the built bytes.

**Pre-fix defect (measured):** the legal-branch rule in `grid.py:867`
```
if not branch or (branch != "master" and not branch.startswith("season/")):
```
rejects every canonical name — `"season2/main".startswith("season/")` is
False — so the 5-min grid cron's `commit --all` would exit 2 on
`season2/main`, `season2/posts/<x>`, `season2/loops/<s>-<a>`. One-liner proof
run before any edit:
```
'season2/main' old_pred= False  grammar_accept= True
'season2/posts/x' old_pred= False  grammar_accept= True
'season2/loops/a-b' old_pred= False  grammar_accept= True
```
(the grammar module already accepts them; only the grid predicate was stale).

## Changes

1. **branches.py** — added `branches.is_legal_branch(name)`: True for `master`
   or any name `parse()` admits (canonical + legacy aliases), else False via
   the ValueError parse raises on feature branches, malformed season names,
   and empty/detached-HEAD. Exported in `__all__`. Single reusable predicate
   so the grid gate and its tests share one source of truth.
2. **grid.py** — `import branches`; the commit--all guard now calls
   `branches.is_legal_branch(branch)` instead of the startswith rule. Comment
   rewritten to name the grammar. `--allow-branch` / session-commit handling
   unchanged; `master` still admitted.
3. **season.py** — the rollover `--branch` plan line emits
   `branches.season_main(new_season)` (= `season2/main`) instead of the legacy
   `season/s<new>` literal; stale help/doc at :14, :868-870, :1748 updated
   from `season/s<N>` to `season<N>/main`.
4. **verification.py** — prose only: stale docstring `season/s2` →
   `season2/main` (lookup itself already reads the ladder `town_branches`).
5. **tests** — test_branches.py: 8 new `is_legal_branch` cases (accept
   season2/main, season2/posts/x, season2/loops/a-b,
   season2/web-app-suite/season1/main, season/s2, master; refuse feature/x,
   season2/weird, "", None). test_season.py: the rollover tests updated to
   expect `season2/main`. test_grid.py: the old "nested season/* admitted"
   test replaced — canonical `season2/main` admitted, non-grammar
   `season/ideas/flock` now refused (that name codified the loose old rule the
   grammar deliberately tightens).

## Evidence

Predicate run, not read — accept + refuse list:
```
'season2/main'                             -> True  OK
'season2/posts/x'                          -> True  OK
'season2/loops/a-b'                        -> True  OK
'season2/web-app-suite/season1/main'       -> True  OK
'season/s2'                                -> True  OK
'master'                                   -> True  OK
'feature/x'                                -> False  OK
'season2/weird'                            -> False  OK
''                                         -> False  OK
'None'                                     -> False  OK
```

season.py branch seam: `season_main(2) = season2/main`;
`branch_name = branches.season_main(new_season)` at season.py:987.

Test suite (files changed / that cover the change, never the bare dir):
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_grid.py \
  extensions/agi/tests/test_branches.py extensions/agi/tests/test_season.py -q
203 passed in 38.03s
```
the last line verbatim.

## Caveats

The grid.py predicate is tested here through branches.py's is_legal_branch and
the two grid guard tests, not through an end-to-end `commit --all` on a
migrated tree (none exists yet); the grammar module is the authority both
sides share, so the seam is thin.

## Agent Notes
grid.py legal-branch rule now uses branches.is_legal_branch; season.py rollover emits season2/main; verification.py prose fixed; 8 is_legal_branch tests + rollover/grid guard tests updated. 203 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.307 (a00-e20a6d63): accepted as proved. (1) INSTRUCTION SAID: "grid.py legal-branch rule ... must accept every name the grammar module admits; season.py --branch emits branches.season_main(new_season); verification.py prose; tests". (2) WHAT THE MACHINE DOES, re-measured on the kid bytes, not read: grid.py:870 now calls branches.is_legal_branch(branch) and branches.py:74 defines it as master-or-parse-succeeds; season.py:987 is `branch_name = branches.season_main(new_season)`; the old `startswith("season/")` predicate returned False for season2/main (one-liner, pre-fix). I re-ran `env -u TMUX -u TMUX_PANE python3 -m pytest test_grid.py test_branches.py test_season.py -q` in the kid worktree: `203 passed in 41.70s`. (3) NEAR MISS: an is_legal_branch that returns True for any string starting with `season` would satisfy the words and silently re-admit the loose names the grammar deliberately rejects; the kid tightened instead -- test_commit_all_refuses_non_grammar_season_branch proves season/ideas/flock now exits 2, and I checked no live branch carries that spelling, so the tightening costs nothing. (4) DEVIATION: scope grew from 3 files to 4 by adding the predicate to branches.py rather than inlining a try/except in grid.py -- authorised because the claim demands ONE grammar module, and a second parse site in grid.py is exactly the drift the module exists to prevent. Caveat recorded on the node is honest: no end-to-end commit --all on a migrated tree exists yet; the fixture guard test is the closest proof.
<!-- THOUGHT:END -->
