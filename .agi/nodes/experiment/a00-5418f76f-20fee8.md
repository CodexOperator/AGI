---
id: experiment:a00-5418f76f-20fee8
mint_id: b3c4c894e8954be8832cd9bbd8156692
type: experiment
parents:
  - hypothesis:l4-merge-kids-resolves-the-parents-own-worktree
next_edges: []
confidence: 0.6
evidence_runs:
  - experiment:a00-5418f76f-20fee8
loop: hypothesis:l4-merge-kids-resolves-the-parents-own-worktree@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3d50165a8f75e981
season: 2
title: A00 5418f76f 20fee8
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-5418f76f-20fee8

## Experiment

Tested + fixed the PRIMARY falsifier of hypothesis:l4-merge-kids-resolves-the-
parents-own-worktree: merge-kids, run from a parent's linked git worktree,
must resolve the round branch from the CALLING worktree's own top, never
git_common_root (which walks to the MAIN checkout).

**Fixture** (throwaway temp repo, never this repo): `git init -b master`,
one node file + one source file, committed as `base`. A kid branch
`kid-A` cut from base carrying one commit. A REAL second linked worktree
`git worktree add -b loop/parent@s2 wt master`.

**REPRODUCED the defect (unmodified code):**
```
python3 season.py --root /tmp/mktest/wt merge-kids kid-A --suite true
kid-A is 1 commit(s) ahead of master
merged kid-A --no-ff into master        # WRONG
merge-kids complete; all 1 kid branches merged
```
`master` (MAIN's checked-out branch) got the merge; the parent's own
`loop/parent@s2` stayed at base. Exactly the hypothesized failure:
`git_common_root(wt)` = MAIN checkout, `_current_branch(main)` = `master`.

**FIX (extensions/agi/bin/season.py `cmd_merge_kids`):** replace
`git_root = locations.git_common_root(root)` with
`top = _git(root, "rev-parse", "--show-toplevel")`. `root` is the graph dir
(`.agi/`) inside whichever worktree invoked this; `--show-toplevel` names
that SAME worktree's checkout top. So `cur` is the parent's OWN round branch
and every git op (ahead/merge/suite/commit/`_resolve_conflicted`) runs in
that worktree onto that branch, with node/source paths staying
worktree-top-relative as `git diff` reports them. In a single checkout
(no worktree) show-toplevel == git_common_root, so bare-temp-repo behaviour
is unchanged (all prior merge-kids tests still pass).

**POST-FIX (same fixture, actor modelled as a parent: AGI_TIER=parent on a
`loop/*` branch, which the commit guard authorises):**
```
kid-A is 1 commit(s) ahead of loop/parent@s2
merged kid-A --no-ff into loop/parent@s2
exit 0
master still at base; loop/parent@s2 carries the merge; fresh-head (KIDA)
bytes present in the parent's worktree.
```

**Regression test added** (`extensions/agi/tests/test_season_merge_kids.py`:
`test_merge_kids_from_linked_worktree_never_touches_main`) using a REAL
`git worktree add` (temp repo, never this repo): asserts the merge lands on
`loop/parent@s2`, `round` (main's branch) HEAD is byte-unchanged, and main's
branch tree carries none of the kid's merged bytes. The suite runs with
the commit-guard tier vars (AGI_TIER/AGI_PROJECT_ROOT) stripped so the
`loop/*` merge is tested as pure git mechanics.

## Evidence

- Defect reproduced and fix proven by direct season.py runs against a real
  linked-worktree fixture (the git command traces above).
- `python3 -m pytest extensions/agi/tests/test_season_merge_kids.py
  extensions/agi/tests/test_git_commit_guard.py -q` -> **33 passed**.
- Full engine suite (env -u AGI_TIER -u AGI_PROJECT_ROOT)
  `python3 -m pytest extensions/agi/tests/ -q` -> **2858 passed, 1 skipped**.

SCOPE (honest bounds): this experiment proves the core round-branch
resolution + "never touch main's checked-out branch" falsifier. It does NOT
yet implement the hypothesis's other two parts: (a) the per-branch lease /
ownership check (refuse a foreign/unrelated branch), and (b) refusing a NODE
conflict outside Agent Notes/verdict, nor the brief.py timing gate (FIX 3).
Those remain open.

## Agent Notes
Fixed+proved core falsifier: merge-kids now resolves round branch from calling worktree's OWN top (git --show-toplevel), never git_common_root. Repro: pre-fix merged into main's master; post-fix lands on loop/parent@s2, main untouched. Regression test w/ real git worktree; 2858 passed.
