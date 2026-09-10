---
id: experiment:a00-30d128c3-dd46d5
mint_id: e78ad23fd3284c5b8984c69838bd7a24
type: experiment
parents:
  - hypothesis:l4-commit-guard-worktree-toplevel-bypass
next_edges: []
confidence: 0.9
edited_by: a00-321c00b2
evidence_runs:
  - experiment:a00-30d128c3-dd46d5
loop: hypothesis:l4-commit-guard-worktree-toplevel-bypass@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1f0938d4f120ec48
season: 2
title: A00 30d128c3 dd46d5
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-30d128c3-dd46d5

## Experiment

Tested hypothesis:l4-commit-guard-worktree-toplevel-bypass on hooks/agent-git
pre-commit + pre-push, against the LIVE tree (no cherry-picked fixture): the
real main checkout `/home/ubuntu/work/agi` and a real `--branch` worktree at
`.agi/worktrees/a00-321c00b2` (that is THIS agent's own worktree). dispatch.py
was NOT modified; the round stayed in the two hooks + the guard test file.

**Setup confirmed first** (direct reads, then git calls):
- dispatch.py:1542 exports `AGI_PROJECT_ROOT = branch_root.resolve()`; under
  `--branch` (L1337-1363) `branch_root` = the kid's worktree checkout root.
- `git -C . rev-parse --show-toplevel` = `/home/ubuntu/work/agi` (main).
- `git -C .agi/worktrees/a00-321c00b2 rev-parse --show-toplevel` = that worktree.
  The two toplevels DIFFER; the worktree's `.git` is a file referencing
  `main/.git`.

The bypass's triggering condition is exactly that toplevel mismatch: the
hook's L3.17 logic (`if [ "$REAL_TOPLEVEL" != "$REAL_PROJECT" ]; then exit 0; fi`)
allows whenever the CWD's toplevel differs from the toplevel derived from
AGI_PROJECT_ROOT — so a process whose CWD is the MAIN checkout while
AGI_PROJECT_ROOT points at its worktree slips through as a "non-project repo".

**Repro (RED), both hooks, pre-fix** (invoking the hook script directly with the
env + CWD; no actual commit made — the hook reads only env + CWD):
```
cd /home/ubuntu/work/agi
AGI_TIER=kid AGI_PROJECT_ROOT=/home/ubuntu/work/agi/.agi/worktrees/a00-321c00b2 \
  bash extensions/agi/hooks/agent-git/pre-commit ; echo exit=$?
# -> (no refusal line) exit=0   <-- ALLOWED, the bug
AGI_TIER=kid AGI_PROJECT_ROOT=<same worktree> bash .../pre-push ; echo exit=$?
# -> exit=0   <-- also allowed
```
Controls (should hold, and did pre-fix):
- kid, CWD=worktree, root=worktree -> refuse (1)
- kid, CWD=main, root=main/.agi (L3.17 g11 case) -> refuse (1)
- kid, CWD=main, root=main -> refuse (1)

**Fix** — in BOTH hooks, the `different => allow` escape now distinguishes a
foreign repo from a different checkout of the SAME project by comparing the
resolved `git rev-parse --git-common-dir` of REAL_TOPLEVEL and REAL_PROJECT:
same common dir => same project, other checkout => refusesthe commit;
different/absent common dir => genuinely foreign scratch repo => allow. Manual
verification that both toplevels resolve their common-dir to the same
`/home/ubuntu/work/agi/.git` guided the discriminator choice.

**After fix (GREEN), both hooks** (same commands):
```
AGI_TIER=kid AGI_PROJECT_ROOT=<worktree> bash .../pre-commit ; echo exit=$?
# -> agi: tier kid may not commit — automation owns git (goal:s27) ; exit=1  REFUSED
AGI_TIER=kid AGI_PROJECT_ROOT=<worktree> bash .../pre-push ; echo exit=$?
# -> agi: tier kid may not push — automation owns git (goal:s27)   ; exit=1  REFUSED
```
Regression controls after fix, all still correct:
- kid in own worktree (equal toplevel) -> refuse (1)
- parent on `loop/hypothesis-l4-commit-guard-workt-a00-321c00b2@s2` in its own
  worktree -> ALLOW (0) — the one authorised parent commit survives
- parent, CWD=main, root=worktree, non-loop -> refuse (1)

**Test suite** — `python3 -m pytest extensions/agi/tests/test_git_commit_guard.py -q`
passed 20/20 before adding regression tests, then 22/22 with two new tests
`test_pre_commit_rejects_kid_from_main_into_same_repo_other_checkout` and
`test_pre_push_rejects_kid_from_main_into_same_repo_other_checkout`, each
creating a real two-checkout repo via `git worktree add` and asserting the
main-CWD commit/push is refused under AGI_PROJECT_ROOT = the sibling worktree.

## Evidence

- PRE-FIX bypass, pre-commit: `exit=0` (silently allowed).
- PRE-FIX bypass, pre-push: `exit=0`.
- POST-FIX, both hooks: `exit=1` with the named goal:s27 refusal line.
- Post-fix controls: kid worktree=1, parent loop worktree=0, parent main non-loop=1.
- `bash -n` clean on both modified hooks.
- pytest guard file: 20 passed (pre) -> 22 passed (post).
- No full-suite run: the brief capped this round at the guard test file
  (` No full-suite run`), and no engine file outside the hooks changed.
- Hypothesis PROVED: the worktree-root toplevel bypass existed and now both
  hooks refuse the main-checkout commit under a worktree AGI_PROJECT_ROOT.

## Agent Notes
Worktree-toplevel bypass proved and fixed in both agent-git hooks: recovered via agi/tools.git_commit_guard (blue road) because the earlier hooks now compare the CWD's resolved toplevel against the toplevel of AGI_PROJECT_ROOT (git fetch)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: read the artifact, re-ran the guard suite myself (22/22 pass in this worktree) and live-refired the main-checkout bypass repro under AGI_TIER=kid with a worktree AGI_PROJECT_ROOT — refused, exit=1 with the goal:s27 line. Both hooks carry the git-common-dir discriminator; no dispatch.py or adapter touched; no git run by the kid. verdict=proved accepted as written; evidence_runs self-cite is legitimate (experiment IS the run).
<!-- THOUGHT:END -->
