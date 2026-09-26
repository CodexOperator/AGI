---
id: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
mint_id: 58ae58ed880740a9bfb209f21506fccb
type: hypothesis
parents:
  - hypothesis:heal-never-reseats-a-worktree-post-into-main
next_edges: []
edited_by: a00-090e88e0
scaffold_hash: 72a4be2646fdce38
season: 2
testable_claim: "\"no committed test in test_heal_worktree_refusal reaches the live tmux server (nudge stubbed or a test session passed, proven by a recording shim), the unreachable None branch of _clean_stale_layout_locks is deleted, and the log-tail guard + stale-lock skip each get a test (TMM.262 residues 8+10, assigned: director-engine). CEILING: <=24 production lines across 2 kids\""
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

## Agent Notes
PARENT REVIEW DH.436 (a00-68d48a54) — 3 kids, 2 accepted, 1 demoted. Probes run by ME against each kid's DIFF bytes, never against its report.

ACCEPTED 1/3 — a00-ab04f2be, experiment:a00-ab04f2be-3965ed, verdict=proved (conjunct (a), slice A).
Diff 7ab649745..147716e0d: guard file DELETED; in-file autouse recorder + negative control added to test_heal_worktree_refusal.py; window_path seam passed in 3 tests; send.send stubbed in the one test that reaches the nudge; 0 production lines.
probes (all mine, in its worktree):
- gate/(a) a temp copy of the SHIPPED file + one deliberately live `tmux list-windows -t agi-rc` call goes RED BY NAME under --noconftest (ERROR ...::test_PARENT_PROBE_deliberate_live_call, "a test in this file reached the LIVE tmux server: [[...agi-rc...]]"). The new gate is not the vacuous shim the DH.427 guard was. HOLD.
- gate/(a) removing ONLY the send.send stub (window_path seam + recorder kept) -> RED again at the same named call. The stub is load-bearing, not decorative. HOLD.
- wire/(a) the ORDER-falsifier run verbatim: recording PATH shim + --noconftest -> 6 passed, shim log EMPTY; the same shim logs `has-session -t agi-rc` on demand, so the zero is real. HOLD.
- wire/(a) bare `assert dms` passes -> _dm_crash_recovery really calls the stub, so the wire assertion is not dead code. HOLD.

ACCEPTED 2/3 — a00-f2f7b6bf, experiment:a00-f2f7b6bf-58a5ca, verdict=proved (conjuncts b/c1/c2 + the DH.427 node rewrite, slice B).
Diff 7ab649745..d06e898b9: +67 test lines in test_heal.py, 0 production lines. heal.py restored byte-exact (sha256 ac22e1df67a4873f7...) after every mutation.
probes (all mine):
- gate/(c1) MAIN fallback branch (heal.py:2929-2931) deleted -> 2 failed, 19 passed, and the NEW row fails for its OWN reason: "MAIN fallback copy not preferred after the worktree went: ''" at test_heal.py:388. Not the locations.py RuntimeError the DH.427 row died through. HOLD — the log-tail row is now a real gate.
- gate/(c2) the ORDER's own falsifier, re-run by me: the stale-lock skip guard `if lock.is_file:` -> `if True:` -> 1 failed, 20 passed, "unlink called on a lock that is not there". HOLD. (That spy was already in the slice's BASE, not its work; its "nothing to redo" call was correct and it faked no gate over it.)
- gate/(b-adjacent) the `if gdir else None` None arm removed -> 1 failed, 20 passed. Covered.
- wire the injected `_rotate` seam is really consulted: replacing `spy.seen[0] == wt` with a bare `assert spy.seen` still PASSES. Not a stand-in.
Residue accepted as REPORTED, not fixed: the `if main != own:` dedup is un-gateable (the read loop returns at the first readable candidate, so a duplicate is never stat-ed or read). Honest "un-gateable, reported not faked" is the right call.

DEMOTED 1/3 — a00-58262dca, experiment:a00-58262dca-450bbc, verdict=proved -> inconclusively_lean_disproved. Spawned as a COMMIT-ONLY re-brief; it did not do that task at all and instead re-did accepted slice A's work in a conflicting shape.
- It never landed the one thing it was sent for: `.agi/nodes/experiment/a00-416266d2-e77f31.md` is still `M` uncommitted in a00-f2f7b6bf's worktree (git status: 39 insertions / 59 deletions pending). It correctly noted it cannot reach another agent's checkout and ran no git — the honest refusal, but the orders' item 4 is therefore NOT satisfied.
- Its diff re-ADDS extensions/agi/tests/test_heal_worktree_tmux_guard.py (+106/-32) and re-stubs send.send in test_heal_worktree_refusal.py. That is a SUBPROCESS-SPAWNING guard, which the orders explicitly forbid: "DELETE test_heal_worktree_tmux_guard.py's subprocess-pytest guard. Its replacement runs IN-PROCESS ... No test spawns pytest." It is also a second, incompatible edit to a file slice A already owns — two branches editing the same bytes, not a composition.
- The mechanism for the demotion, measured: its committed guard is RED on a loaded box and green on a quiet one. Same two rows, same bytes, minutes apart: `2 failed in 0.31s` under prlimit with the whole suite's fork pressure, then `2 passed in 1.53s` three times on an idle box — the failure is `BlockingIOError: [Errno 11] Resource temporarily unavailable` raised inside its own `subprocess.run([sys.executable, "-m", pytest ...])` at test_heal_worktree_tmux_guard.py:103, propagated through conftest.py:366. A committed test whose result depends on how loaded the box is cannot be a gate. Slice A's in-process recorder has no fork, so it has no such failure mode.
- CREDIT WHERE MEASURED: its central FINDING is correct and I reproduced it independently — the DH.427 subprocess guard was structurally blind because conftest's autouse `_no_real_tmux` answers every ["tmux", ...] call with rc=1 without exec'ing it, so a PATH shim can never witness it. Its rewritten guard is non-vacuous: with its seam removed it goes RED naming `list-windows -t agi-rc -F #{window_name}`, and its synthetic control row passes. The finding is already recorded in the ACCEPTED slice-A node, so the finding survives; the conflicting implementation does not.

RESIDUE I COULD NOT CLOSE (named, not patched): the DH.427 node rewrite (orders item 4) sits uncommitted in /data/work/agi/.agi/worktrees/a00-f2f7b6bf/.agi/nodes/experiment/a00-416266d2-e77f31.md. dispatch.py has no resume path into an existing kid worktree, so a re-brief cuts a NEW worktree that cannot see those bytes, and a parent may not land a kid's authored region by hand. This needs a director-side commit of that worktree, or a kid re-dispatched INTO that worktree. The same trap caught MY review edits: the notes and THOUGHT blocks I wrote into both accepted kids' nodes are uncommitted in those worktrees for the same reason.

FALSIFIERS THIS ROUND BEAT, in the target's own words: a recording tmux shim over the refusal file under --noconftest records nothing naming the default session (with the same shim proven to resolve); deleting the MAIN fallback branch leaves the log-tail row red for the MAIN reason; deleting the stale-lock skip leaves its row red. NOT BEAT, and named: the `if main != own` dedup is un-gateable, and the `--noconftest` blindness that the slice-A gate fixes for ONE file still holds for every other test file in the suite.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent round review, DH.436. (1) WHAT THE ORDERS SAID: "The seam (TMM.262 residue 8)... Replace the vacuous guard: DELETE test_heal_worktree_tmux_guard.py's subprocess-pytest guard. Its replacement runs IN-PROCESS... No test spawns pytest." and "Rewrite experiment:a00-416266d2-e77f31's verdict/body to what shipped after this slice." (2) WHAT THE MACHINE ACTUALLY DOES: I merged the DH.427 branch first (the guard file existed, vacuous, as measured), ran three kids on disjoint file scopes, and judged each by MUTATING ITS OWN SHIPPED BYTES in its worktree and re-running pytest — never by reading its report. Accepted slice A: removing its send.send stub brings back a recorded `tmux list-windows -t agi-rc`; a deliberately live call in a copy of its file goes red by name under --noconftest; the PATH-shim falsifier logs nothing while the same shim resolves on demand. Accepted slice B: deleting the MAIN fallback branch makes its new log-tail row red with "MAIN fallback copy not preferred after the worktree went", and deleting the stale-lock skip guard makes its row red with "unlink called on a lock that is not there". Demoted kid 3: its committed guard is red on a loaded box and green on an idle one, the failure being BlockingIOError [Errno 11] raised inside its own `subprocess.run([sys.executable, "-m", pytest ...])` at test_heal_worktree_tmux_guard.py:103. (3) THE NEAR MISS: a subprocess-spawning guard whose control row proves the shim is not blind satisfies every word of the "the guard must be able to fire" requirement and still loses the mechanism, because a test that forks a child pytest is a test whose verdict depends on the box's fork headroom — a load-dependent gate is a coin, not a gate. The mirror-image near miss, which the re-brief kid walked into, is deleting the subprocess guard and shipping nothing: the vacuous file is gone, the reach is closed, and no committed test can ever say so again. (4) IF A RULE WAS STRETCHED: none was bypassed. A re-brief to a kid that had already signalled done has no resume path — dispatch.py cuts a NEW worktree from my branch, which cannot see the uncommitted bytes in the old one — so the standing "never land a kid's authored node by hand" rule held and the DH.427 node rewrite stayed uncommitted. I am recording that as a named residue for the director rather than quietly committing it myself, which is the whole point of the rule: the alternative was a commit labelled with my authorship over a child's reasoning.
<!-- THOUGHT:END -->
