---
id: hypothesis:l4-commit-guard-worktree-toplevel-bypass
mint_id: d69c93254d8c4f7cb77ba5d3e78ddd11
type: hypothesis
parents:
  - hypothesis:l3-commit-guard-inert-under-g11
  - goal:g15
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: cf449ccc309dc784
season: 2
testable_claim: "Under --branch dispatch, AGI_PROJECT_ROOT is exported as the kid's own worktree, so pre-commit's PROJECT_TOPLEVEL (git -C \"$AGI_PROJECT_ROOT\" rev-parse --show-toplevel) resolves to that worktree, not the main checkout. A commit run with CWD in the MAIN checkout under that env gets REAL_TOPLEVEL != REAL_PROJECT and is incorrectly ALLOWED. Falsifiable: reproduce that exact env/CWD combination live and observe the hook's exit code (0 = confirmed) before a fix, and confirm it refuses (non-zero, named message) after. Disproved if the current hook already refuses in that combination."
thought_session: sanctuary-helper-cd
title: pre-commit's AGI_PROJECT_ROOT-derived toplevel check is bypassed when a --branch kid commits from the MAIN checkout instead of its worktree
---
<!-- BODY:BEGIN -->
# hypothesis:l4-commit-guard-worktree-toplevel-bypass

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.121 brief -- pre-commit's toplevel guard is bypassed from the MAIN checkout under --branch

Assigned by sanctuary-director (rotation/verification noted in THOUGHT).

ROOT-CAUSED before writing this, against extensions/agi/hooks/agent-git/pre-commit
as it stands now (direct read, not taken from the assignment): the hook
already carries the L3.17 fix from hypothesis:l3-commit-guard-inert-under-g11
(PROJECT_TOPLEVEL derived via `git -C "$AGI_PROJECT_ROOT" rev-parse
--show-toplevel`, compared against the CWD's own toplevel). That fix closed
the original gap (AGI_PROJECT_ROOT = graph root vs. git toplevel never
matching). The RESIDUAL gap is different and, by my own reading, real:
under --branch dispatch AGI_PROJECT_ROOT is exported as the KID'S OWN
WORKTREE, so PROJECT_TOPLEVEL resolves to that worktree's toplevel, not the
main checkout's. A process that ends up running `git commit` with CWD
inside the MAIN checkout instead of its assigned worktree gets
REAL_TOPLEVEL = main checkout, REAL_PROJECT = worktree -- they differ, so
`if [ "$REAL_TOPLEVEL" != "$REAL_PROJECT" ]; then exit 0; fi` ALLOWS the
commit, in the one place the guard was built to refuse it.

NOTE: I could not find the "closing note" the assignment referenced on
hypothesis:l3-commit-guard-inert-under-g11 -- read the whole node directly,
it ends at its original L3.17 brief, no THOUGHT block or later section.
Either it lives on a branch not yet synced to me, or the pointer was
mistaken; this brief stands on my own direct reading of the current
pre-commit logic, not on that citation.

FALSIFIER: with AGI_TIER=parent, AGI_ROLE=parent, AGI_PROJECT_ROOT set to
whatever value `dispatch.py --branch` actually exports (confirm exactly,
do not assume it is `<worktree>/.agi`), CWD set to the MAIN checkout,
`git commit` must be REFUSED. Today (verify red first) it is allowed. Fix
must not regress the L3.17 case (AGI_PROJECT_ROOT = graph root, CWD = main
checkout, still refused) or the loop/* branch commit parents are
authorised to make.

Files: extensions/agi/hooks/agent-git/pre-commit, extensions/agi/hooks/agent-git/pre-push
(check whether pre-push has the identical shape -- l3-commit-guard-inert-under-g11's
own brief fixed both together), extensions/agi/tests/test_git_commit_guard.py.
Do not touch dispatch.py or any adapter. Kid ceiling 2. No full-suite run.

REPORT: one experiment node with the live exit-code proof (before/after,
both hooks) and the test result.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Point rotated again this generation (sanctuary-director-11 [3d6888] ->
seat-sanctuary-director-16 [4a9edc], third rotation this session). Verified
independently, same as the prior two: tmux+ListAgents join (@245, busy,
matches) and config:seats read fresh at origin/season/s2 HEAD (sanctuary-
director row session_ref 4a9edc, matches). Proceeded on that basis. This
node's brief was root-caused against my own current tree before writing,
not transcribed from the assignment message.
<!-- THOUGHT:END -->
