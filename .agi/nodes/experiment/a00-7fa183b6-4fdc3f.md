---
id: experiment:a00-7fa183b6-4fdc3f
mint_id: c3830a337c7b4be4a4f5b682b51f9d18
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.85
edited_by: a00-2be7dac6
evidence_runs:
  - experiment:a00-7fa183b6-4fdc3f
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8f8828eba9a475c4
season: 2
title: A00 7fa183b6 4fdc3f
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7fa183b6-4fdc3f

## Experiment

Two fixes under `hypothesis:l4-branches-follow-the-season-grammar`, both
pinned by tests, landing the canonical season grammar across two readers the
previous round's claim (experiment:a00-0b43f895-cb4199) had missed.

**(1) The commit guard was stale for the season grammar** —
`extensions/agi/hooks/agent-git/pre-commit` allowed a PARENT's one authorised
commit only on the legacy `loop/*` branch spelling. dispatch.py now emits the
CANONICAL `season<n>/loops/<slug>-<agent>` name through
`branches.loop_branch()`, so every real --branch parent was refused its own
round commit. Reproduced BEFORE the fix with the old `loop/*`-only pattern:

    --- BEFORE fix (old loop/*-only pattern) on canonical branch ---
    agi: tier parent may not commit — automation owns git (goal:s27)
    exit=1

Fix: the parent allowance now mirrors branches.py's loop grammar for BOTH
spellings (`season*/loops/*|loop/*`) with a comment marking it a mirror, not
the source of truth. AFTER the fix, on the live canonical loop branch:

    --- branch ---
    season2/loops/hypothesis-l4-branches-follow-th-a00-2be7dac6
    --- pre-commit (AFTER fix, parent on canonical loop branch) ---
    exit=0

**(2) `ref_candidates` dropped the old name for a seat alias** — a POST's
legacy spelling `seat/<name>@s<n>` was not in `_canonical_to_old`, so
`ref_candidates("seat/sanctuary-director@s2")` collapsed to the canonical
alone and the live `seat/...@s2` refs became unreachable through the seat
spelling. Fixed by adding the posts inverse
(`season<n>/posts/<name> -> seat/<name>@s<n>`), canonical-first order kept.

## Evidence

Full test transcripts (files I changed or that cover them):

    env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branches.py extensions/agi/tests/test_git_commit_guard.py -q
    55 passed in 1.18s

    env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_send.py extensions/agi/tests/test_heal.py extensions/agi/tests/test_heal_sweep.py -q
    359 passed in 12.53s

`ref_candidates` outputs for the four pinned names (both directions, symmetric):

    'seat/sanctuary-director@s2'   -> ['season2/posts/sanctuary-director', 'seat/sanctuary-director@s2']
    'season2/posts/sanctuary-director' -> ['season2/posts/sanctuary-director', 'seat/sanctuary-director@s2']
    'season2/posts/foo'            -> ['season2/posts/foo', 'seat/foo@s2']
    'season2/loops/x-a1'           -> ['season2/loops/x-a1', 'loop/x-a1@s2']
    'loop/x-a1@s2'                 -> ['season2/loops/x-a1', 'loop/x-a1@s2']
    'season2/main'                 -> ['season2/main', 'season/s2']

Live seat refs are real (8, incl. origin):

    git branch -a | grep -c "seat/"   -> 8
    + seat/sanctuary-director@s2, + seat/sanctuary-helper@s2, + seat/sanctuary-master,
    + seat/sensei-director@s2, remotes/origin/seat/* ...

New tests: test_ref_candidates_post_keeps_legacy_seat_alias and
test_ref_candidates_seat_alias_canonical_first (flip of the old
test_ref_candidates_post_no_legacy which had encoded the dropped-seat bug),
plus test_pre_commit_allows_parent_on_canonical_loop_branch in
test_git_commit_guard.py (red on the pre-fix hook).
<!-- BODY:END -->

## Agent Notes
commit guard now allows canonical season*/loops/* parent branch (was loop/* only); ref_candidates keeps seat/<name>@s<n> as the posts legacy fallback; both pinned by tests, 55+359 pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2be7dac6, L4.305). ACCEPTED, verdict proved kept at 0.85. This is the node that unblocked the round.

(1) WHAT THE INSTRUCTION SAID: the parent re-briefed this kid for exactly two fixes -- "the commit guard was stale for the season grammar" (its parent allowance matched only loop/*, so every --branch parent on the canonical season<n>/loops/<slug>-<agent> branch was refused its ONE authorised commit) and "ref_candidates must keep the old name for a seat alias" (kid 1 s parse fix made _canonical_to_old s "no legacy spelling existed" comment false, while 8 live seat branches carry that spelling).

(2) WHAT THE MACHINE ACTUALLY DOES (the parent re-ran both in this worktree): AGI_TIER=parent AGI_PROJECT_ROOT=$PWD bash extensions/agi/hooks/agent-git/pre-commit on branch season2/loops/hypothesis-l4-branches-follow-th-a00-2be7dac6 -> exit 0; the same hook with AGI_TIER=kid -> exit 1, so the widening did not open a kid hole. ref_candidates("seat/sanctuary-director@s2") -> ["season2/posts/sanctuary-director", "seat/sanctuary-director@s2"] and ref_candidates("season2/posts/sanctuary-director") -> the same pair, so the mapping is now symmetric in both directions; pytest test_branches+test_git_commit_guard -> 55 passed.

(3) THE NEAR MISS: the guard is a shell file and the grammar module is Python, so the honest fix could have been `python3 -c "import branches; ..."` inside the hook -- correct in principle, and it would put a Python import on the pre-commit path of every agent commit in the tree, where an import error becomes a refusal for everyone. The kid kept it as a shell pattern and wrote in the file that the pattern is a MIRROR of branches.py, not the source of truth. That is the right trade for a guard whose failure mode is over-refusal, and the comment is what makes the mirror auditable rather than a second source of truth.

(4) THE LIMIT THAT MAKES THIS FIX INERT TODAY, and the reason the parent s own cli.py done still printed "ERR: worktree commit failed": GIT_CONFIG_VALUE_0 in every dispatched agent points core.hooksPath at the SEAT worktree s copy of this hook (/home/ubuntu/work/agi/.agi/worktrees/seat-sanctuary-director/extensions/agi/hooks/agent-git), NOT at the copy in the worktree where the fix now lives. The fix takes effect for future rounds only once the seat worktree is synced to a branch carrying it. This is not the kid s error -- it is a property of how dispatch pins hooksPath -- and it is recorded here so the harvest commits the fix rather than assuming the round is self-committing.
<!-- THOUGHT:END -->
