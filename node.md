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

## CORRECTIVE DH.528 -- closes mur-director-engine-16 DH.485-k1 (review accept_with_residue; verify timed out twice at 3600 s, review residues stand)
BASE      CUT FROM season2/loops/hypothesis-heal-worktree-refusal-a00-bffe8866 tip ac2b2a4c3 (worktree a00-bffe8866). No merge. Never rebase. NEVER DH.476.
0 production lines, 0 test lines: node wording only, write.py only.
1. verdict:a00-033193ed-599c69 keeps demote_reason 'no experiment evidence (evidence_runs=0) for proved' (:9) and demoted_from: proved (:10) while verdict: proved (:23) -> clear both stale stamps (write.py set/unset), reason in its THOUGHT.
2. the same verdict's evidence_runs cites experiment:a00-651ab5e8-e70670 -- the node the DH.485 scrub edited, the OBJECT of the verdict, not independent backing (evidence_gate._is_self_citation accepts it, evidence_gate.py:322-340) -> cite the committed test run that proves the claim (test_heal_worktree_refusal.py, 6 passed at the base: RE-RUN, paste) or lower the verdict with the reason.
3. experiment:a00-651ab5e8-e70670 :80 and :99 record grep probes whose PATTERN contains the strings it searches for, so run over the node they match their own lines (rc=0), not 'no match' -> record a probe that cannot self-match (build the pattern from pieces at run time, or run it over the scrubbed files only), RE-RUN, paste the real output; the recorded pattern writes <user>, never the name.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE verdict:a00-033193ed-599c69 · experiment:a00-651ab5e8-e70670 (write.py only) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines · 0 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.528: mur-16 DH.485-k1 accept_with_residue (verify timed out twice) -- stale demote stamps on a proved verdict, circular evidence (the verdict cites its own object), self-matching grep probes recorded as no match. Demoted as notes: cli.py body-union (carried, goal:g7.33.19 row scope), the <user> literal (named on the verdict).
<!-- THOUGHT:END -->
