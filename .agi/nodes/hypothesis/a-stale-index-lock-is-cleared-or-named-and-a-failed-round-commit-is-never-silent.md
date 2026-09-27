---
id: hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent
mint_id: c28f9cd88b834d99b463d9e1735c1323
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: a00-76c416dd
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

## CEILING
HARD CAP: 1 kid · <= 20 production lines · <= 70 test lines · pi-free tier-0 · 0 USD

## ROUND NOTES (kid a00-76c416dd, DH.564) -- the two corrections, and the scope of the fix

**The `fds = []` bug is fixed, with a scope decision I am naming rather than
hiding.** `except OSError: fds = []` on the fd DIRECTORY dropped the whole pid
and unlinked a HELD lock. The bytes now refuse to conclude "no holder" from an
incomplete walk -- but only for a pid that could plausibly BE the holder, and
`/proc/<pid>/comm` (always readable) is the same signal the cwd+comm branch
already trusts. A `git` whose table we cannot read returns a NAMED refusal
string; `_lock_is_held` now returns `bool | str` and `_clear_stale_index_lock`
returns that string instead of clearing. Measured on this host, refusing on
EVERY uninspectable pid is not an option: five live pids here (a user's
`systemd`, `sd-pam`, `ssh-agent`, `gpg-agent`) are permanently unreadable, so
the strict reading would refuse every commit on every ordinary desktop. The
RESIDUAL, named: a NON-git process (an editor, a backup, a scanner) that holds
the lock open while being unreadable is still cleared over. Unreadable and
non-git is a far smaller hole than the one it replaces, and it is the one a
future round should measure next.

**The exit-3 hop is executed by a test.** `cmd_done` itself is now driven in
`test_a_failed_round_commit_exits_3_and_names_itself_in_the_dm`, so
`if commit_fail: ... return 3` runs on every suite run instead of being a
grep. Only the dm transport is stubbed.
## CEILING
HARD CAP: 1 kid · <= 20 production lines · <= 70 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. No test touches a live worktree.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.547 parent state, after one corrective kid (a00-ae90c756, demoted to inconclusive_lean_proved:80 on my own P3). WHAT THE MACHINE DOES NOW, read in the diff e6e678bf2..2f54f71de: _lock_is_held scans /proc per fd with a per-fd OSError continue (cli.py:2383-2395), the test file proves the falsifier fails pre-fix and passes post-fix, the holder path is shlex-quoted with a bounded liveness poll, and the cwd+comm test asserts it holds no fd on the lock. WHAT IS STILL FALSE IN THE CLAIM, from my probe (probe_listdir.py, live, tmp repo): when the holders own /proc/<pid>/fd DIRECTORY is unlistable -- the real hidepid / other-user shape -- the except maps it to fds = [] and drops the WHOLE pid, so a lock demonstrably open at fd 9 is cleared with one named line. THE NEAR MISS that would satisfy every test in the file and lose the mechanism: the per-fd loop, whose source now reads as hardened while the same skip-one-pid decision survives one level up. THE FIX I DID NOT CUT, because CEILING says HARD CAP 1 kid: a refuse-to-unlink rule -- if the /proc walk was incomplete, return a NAMED refusal instead of clearing, the same principle the missing cell already follows. ALSO UNCLOSED: the exit-3 hop (cmd_done returning 3 given a live _auto_commit_worktree str) is still a READ, never a test; the DH.534 corrective fe18c9dd2 is still an ancestor of NEITHER this base NOR local-maxxing/season2/main, so the merge target carries no corrective; and nothing in the engine refuses an out-of-scope NODE edit at write time (write_guard checks authorship, not the rounds declared scope), so the item-1 out-of-scope edit recurs until write.py checks scope at its single funnel.
<!-- THOUGHT:END -->
