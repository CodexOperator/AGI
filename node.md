---
id: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
mint_id: 58ae58ed880740a9bfb209f21506fccb
type: hypothesis
parents:
  - hypothesis:heal-never-reseats-a-worktree-post-into-main
next_edges: []
edited_by: director-engine
scaffold_hash: 72a4be2646fdce38
season: 2
testable_claim: "no committed test in test_heal_worktree_refusal reaches the live tmux server (nudge stubbed or a test session passed, proven by a recording shim), the unreachable None branch of _clean_stale_layout_locks is deleted, and the log-tail guard + stale-lock skip each get a test (TMM.262 residues 8+10, assigned: director-engine)"
title: Heal worktree refusal tests never reach live tmux and dead branches go
town: core
---
# hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go

## Measured
- TMM.262 (8): extensions/agi/tests/test_heal_worktree_refusal.py:186-192 reaches the LIVE tmux server: send.py:2208-2209 defaults the session to rotate.DEFAULT_TMUX_SESSION (the test root governs rows + inbox only). Its fixture window @777 is absent today, so no pane was hit -- by luck.
- (10) heal.py:3082-3087, the None branch of _clean_stale_layout_locks, is UNREACHABLE: its caller at :3221 runs after the early return at :3166-3174. The log-tail guard and the stale-lock skip have no test of their own.

## CLAIM
(a) No committed test in test_heal_worktree_refusal.py reaches the live tmux server: the nudge is stubbed or a test session is passed, and a guard test proves it (tmux invocations recorded, none targets the default session); (b) the unreachable None branch is deleted (or a comment states why it stays, with the caller line), and the log-tail guard and the stale-lock skip each get their own test.

## Dispatch line
config-max: none / template-max: none / code: the stub/test-session seam, the branch deletion, 2 tests.

## FALSIFIERS
- running the file with a recording `tmux` shim on PATH shows any call carrying the default session name;
- coverage of heal.py:3082-3087 still possible after the change with the branch present and no comment;
- deleting the log-tail guard or the stale-lock skip leaves the suite green.

## TESTS
extensions/agi/tests/test_heal_worktree_refusal.py + neighbourhood test_cli.py test_heal_watch.py test_dispatch.py test_heal.py. Never a real tmux server: a PATH shim only.

## FILE SCOPE
extensions/agi/bin/heal.py · extensions/agi/tests/test_heal_worktree_refusal.py · extensions/agi/tests/test_heal.py (new rows only).

## CEILING
<= 2 kids · <= 12 production lines per conjunct · pi parents (tier-0) · 0 USD. Every test that spawns python/pytest runs under `timeout` + a process cap; never a pytest that re-collects its own dir; kids never launch real claude or touch a live tmux pane.
