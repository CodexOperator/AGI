---
id: hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent
mint_id: c28f9cd88b834d99b463d9e1735c1323
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: a00-d506aa2a
push_further: "DH.594: the item 4/6/8 node-text corrections ARE landed -- verified against the commit, not the sentence: bf1d12489 (\"land DH.564 logged node edits left uncommitted in the parent worktree\") carries all three nodes plus this one, so the old \"not in commit b5b6b9e64\" clause was stale and is retired. What is actually LEFT: (1) conjunct 1 -- a non-git, unreadable holder still loses its lock (P-B, pasted on a00-76c416dd-0bb9b2); the comm-allowlist trade is now MEASURED (4 same-uid uninspectable pids per commit walk on this host, 0 of them git) and the measurement sides with the allowlist, so the remaining work is not \"decide the allowlist\" but \"close the non-git unreadable holder or state it as accepted risk in the claim\". (2) the exit-3 test monkeypatches the dm BUILDER away, so the dm TEXT carrying commit FAILED is still a read, not a run (named in ROUND NOTES). (3) the exit-3 finding is now on this node, so do not rebuild it."
scaffold_hash: 22edeb67ab7bcbef
season: 2
testable_claim: a stale index.lock (older than values.core.stale_index_lock_s, no live git holder) is removed with a named line before the round commit; a fresh or held one refuses by name; a failed round commit exits non-zero and the harvest dm names it
title: "A stale index.lock is cleared or named, and a failed round commit is never silent (g7.33.19 row 18; assigned: director-engine)"
town: local-maxxing
---
# hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent

## Measured
goal:g7.33.19 row 18: DH.503's round worktree held a 0-byte `.git/.../index.lock` (04:01:16Z, no holder); the parent's round commit failed and the parent exited with the kid's work uncommitted and unreviewed; 4 more kid worktrees held one at 04:24Z. No engine code handles index.lock (`grep -n index.lock extensions/agi/bin/*.py` = 0 hits). The round commit (cli.py:2511-2520) prints `ERR: worktree commit failed` to stderr and returns None; the harvest line the director receives does not say the commit failed.

## CLAIM
(1) Before the round commit, a STALE index.lock -- older than the cell values.core.stale_index_lock_s AND no live git process working in that checkout -- is removed with ONE named line, and the commit proceeds; a lock that is fresh or held is never removed: the commit refuses BY NAME. (2) A failed round commit is never silent: the done path exits non-zero and the parent's harvest dm to its director carries `commit FAILED: <reason>`.

## Dispatch line
config-max: values.core.stale_index_lock_s in .agi/config.json (the staleness threshold) / template-max: the harvest-dm line gains the commit-failed field in its template, if one exists / code: the stale-lock check before the commit + the non-zero exit (the trigger that does not exist)

## FALSIFIERS
a held or fresh lock removed · a stale lock left and the commit failing silently · a failed commit with exit 0 · the threshold a literal in code

## TESTS
one new test file, tmp git repos only: a stale 0-byte index.lock older than the cell -> removed, named, commit lands; a fresh lock -> refused by name, exit non-zero, lock untouched; a commit that fails for another reason -> non-zero + the failure named; plus test_cli.py test_dispatch.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp)

## FILE SCOPE
extensions/agi/bin/cli.py (the round commit + cmd_done's exit only) · extensions/agi/tests/test_stale_index_lock.py · the two experiment nodes a00-ae5fd524-8630cf / a00-ae90c756-c1bf84 (write.py only) · the kid's own node. Anon: no user/home/repo/host value in the prose.

## CEILING (GOVERNING -- the cap DH.564 was actually held to, DH.594 a00-d506aa2a)

    HARD CAP: 1 kid · <= 15 production lines net over 62b036f4d · <= 40 test lines · pi-free tier-0 · 0 USD

Commit range this governs: `62b036f4d..b5b6b9e64` (the kid's `done`), landed as
`bf1d12489`. Read it here, at the top of the node, because a merge-up reader of
this branch alone otherwise cannot see the cap at all -- the corrective's brief
never reached the branch.

**The round REWROTE the rule it was measured by, and that is now visible here.**
This node's own original CEILING said `<= 20 production lines · <= 70 test
lines`; the corrective's brief said `<= 15 / <= 40`; the kid read a THIRD number
(40) and wrote "production net +33 (cap 40) -- inside". Measured against the
cap that actually applied: `39 added / 6 deleted` on cli.py = **net +33 against
15 = 18 lines OVER, undisclosed** (the +76 test overage against 40 WAS
disclosed, with the numstat pasted). One heading, one ceiling: the 20/70 clause
and the inserted duplicate are retired -- the duplicate's history is kept in
ROUND NOTES below -- and this block is the only ceiling that governs here.

## ROUND NOTES (kid a00-76c416dd, DH.564) -- the two corrections, and the scope of the fix

**The `fds = []` bug is fixed, with a scope decision that was NAMED but NOT
MEASURED (DH.594, a00-d506aa2a: the decision is now measured, and the count
corrected).** `except OSError: fds = []` on the fd DIRECTORY dropped the whole
pid and unlinked a HELD lock. The bytes now refuse to conclude "no holder" from
an incomplete walk -- but only for a pid that could plausibly BE the holder, and
`/proc/<pid>/comm` (always readable) is the same signal the cwd+comm branch
already trusts. A `git` whose table we cannot read returns a NAMED refusal
string; `_lock_is_held` now returns `bool | str` and `_clear_stale_index_lock`
returns that string instead of clearing.

**THE COUNT, MEASURED (was an unmeasured paste, and it was WRONG).** The
paragraph this replaces read "Measured on this host ... five live pids here
(a user's `systemd`, `sd-pam`, `ssh-agent`, `gpg-agent`) are permanently
unreadable" -- a FIVE against a list of FOUR, presented as a measurement with no
command on the node. It is now a real count, with the command and its output,
run in the DH.594 session dir (script `probe_uninspectable.py`, comm only, no
pid, no path, no user name):

    $ python3 .agi/sessions/iter-DH.594/a00-d506aa2a/probe_uninspectable.py
    pids walked: 578   same-uid: 211
    same-uid pids uninspectable in at least one way: 4
      comm=(sd-pam)     fd-dir errno=13  cwd errno=13  -> allowlist refusal fires: False
      comm=gpg-agent    fd-dir errno=13  cwd errno=13  -> allowlist refusal fires: False
      comm=ssh-agent    fd-dir errno=13  cwd errno=13  -> allowlist refusal fires: False
      comm=systemd      fd-dir errno=None  cwd errno=13  -> allowlist refusal fires: False
    refusals a refuse-on-EVERY-uninspectable-pid rule would raise per commit walk: 4
    of which comm in the git allowlist (refused today): 0

Read it as the decision-maker should: on this host, EVERY commit walk would
raise **4** refusals under the strict rule, and **0** of them are `git` -- so
the strict rule is not merely inconvenient, it is *unconditionally fatal* to
every commit on an ordinary desktop, while the comm allowlist refuses nothing
here. That is the measurement the allowlist trade was missing. ONE CAVEAT I
will not hide: the count MOVES between runs -- a second run a minute earlier in
the same session saw 5, the extra pid being a transient `python3` -- so the
number is a per-walk reading, not a constant, and a rule keyed on a count would
be a rule keyed on a race. The comm of the offenders, not their number, is the
stable part, and that is what the allowlist keys on.

**THE RESIDUAL, still named and still open:** a NON-git process (an editor, a
backup, a scanner) that holds the lock open while being unreadable is still
cleared over. Unreadable and non-git is a far smaller hole than the one it
replaces, and it is the one a future round should measure next.

**The exit-3 hop is executed by a test -- and here is exactly what that test
does NOT execute (DH.594, a00-d506aa2a, so the next round does not rebuild it).**
`cmd_done` itself is now driven in
`test_a_failed_round_commit_exits_3_and_names_itself_in_the_dm`, so
`if commit_fail: ... return 3` runs on every suite run instead of being a
grep. THE FINDING, already visible in a00-ae5fd524-8630cf's own correction
block: that test builds a tmp linked worktree with a pre-commit hook that
exits 1 and **monkeypatches the dm BUILDER `_alarm_dispatcher_on_done` away**,
capturing the `commit_failed` reason it is handed. So the test proves
`cmd_done` returns 3 AND hands the reason to the dm builder; it does NOT prove
the dm TEXT the director reads carries `commit FAILED: <reason>` -- that link
is still a read of the builder's format string, and it is the link to close
next, not a link to rebuild.
**The retired SECOND `## CEILING` copy (DH.594 correction, a00-d506aa2a).** The
block that stood here repeated `1 kid / <= 20 production / <= 70 test` and added
`-- a byte or kid over it = the round is cut`, with a `## ROUND NOTES` block
wedged between it and the `## CEILING` above -- and the two copies named
DIFFERENT caps (20/70 here, 15/40 in the corrective's brief), so no reader could
tell which governed. One heading, one ceiling: the 20/70 clause is HISTORY from
this point, kept here in words only, and `## CEILING (GOVERNING)` above is the
cap this round was measured against.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.564 parent state after the ONE corrective kid allowed by the ceiling (experiment:a00-76c416dd-0bb9b2, DEMOTED to inconclusive_lean_disproved:25 on my own probes, not on its suite). Conjunct 2 is now closed in the bytes and at the live exit code: cmd_done ITSELF is driven by a test, and my independent probe -- a FRESH index.lock in a linked worktree, a shape no test in the file builds -- prints "ERR: round commit FAILED: index.lock ... age=5s stale_after=900s held=no -- NOT removed" and returns 3 with the reason handed to the dm verbatim. Conjunct 1 is NOT closed. The fix is real (an uninspectable git fd table now refuses by name instead of reading as no-holder) and it is not a no-op (a genuinely stale, unheld lock still clears), but it refuses only for comm in {git,index-pack,gc,rebase}: my P-B, the SAME shape as my P1 on the base with the holder's comm changed to sleep, still unlinks a lock verifiably open in a live process's fd. THE NEAR MISS this round shipped, named so the next one does not rebuild it: an allowlist scoped to git satisfies the kid test (which deliberately builds an as_git=True holder) and the git half of the claim while except OSError: fds = [] -- the exact line the corrective named -- survives for every other process. The ceiling also bit: cli.py net +33 against a <= 15 production cap, read by the kid as "cap 40, inside", so that overage went undisclosed. THE UNCLOSED QUESTION, now the whole of the remaining work here: is "refuse on every uninspectable pid" really unusable? The only evidence against it is a pasted reading of four same-uid uninspectable pids on one host, and a safety claim decided by an allowlist is decided by nothing. Measure it -- how many refusals per round on a real host -- rather than inheriting it.
<!-- THOUGHT:END -->
