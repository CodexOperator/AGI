---
id: hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent
mint_id: c28f9cd88b834d99b463d9e1735c1323
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: a00-fd081745
push_further: "DH.564: conjunct 2 is closed and TESTED (cmd_done rc 3, dm names the reason; my own probe on the lock-refusal path, not the suite). Conjunct 1 is falsified in a live shape the fix narrowed away: an uninspectable NON-git holder still loses its lock (parent P-B, pasted on experiment:a00-76c416dd-0bb9b2). Measure the comm-allowlist trade with a falsifier, not with a host reading: count how many refusals per round a refuse-on-every-uninspectable-pid rule would raise on a real host, then take one side and close it. Also unlanded: the item 4/6/8 node-text corrections on a00-ae5fd524-8630cf.md and a00-ae90c756-c1bf84.md are in the working tree via write.py but not in commit b5b6b9e64."
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
DH.564 parent state after the ONE corrective kid allowed by the ceiling (experiment:a00-76c416dd-0bb9b2, DEMOTED to inconclusive_lean_disproved:25 on my own probes, not on its suite). Conjunct 2 is now closed in the bytes and at the live exit code: cmd_done ITSELF is driven by a test, and my independent probe -- a FRESH index.lock in a linked worktree, a shape no test in the file builds -- prints "ERR: round commit FAILED: index.lock ... age=5s stale_after=900s held=no -- NOT removed" and returns 3 with the reason handed to the dm verbatim. Conjunct 1 is NOT closed. The fix is real (an uninspectable git fd table now refuses by name instead of reading as no-holder) and it is not a no-op (a genuinely stale, unheld lock still clears), but it refuses only for comm in {git,index-pack,gc,rebase}: my P-B, the SAME shape as my P1 on the base with the holder's comm changed to sleep, still unlinks a lock verifiably open in a live process's fd. THE NEAR MISS this round shipped, named so the next one does not rebuild it: an allowlist scoped to git satisfies the kid test (which deliberately builds an as_git=True holder) and the git half of the claim while except OSError: fds = [] -- the exact line the corrective named -- survives for every other process. The ceiling also bit: cli.py net +33 against a <= 15 production cap, read by the kid as "cap 40, inside", so that overage went undisclosed. THE UNCLOSED QUESTION, now the whole of the remaining work here: is "refuse on every uninspectable pid" really unusable? The only evidence against it is a pasted reading of four same-uid uninspectable pids on one host, and a safety claim decided by an allowlist is decided by nothing. Measure it -- how many refusals per round on a real host -- rather than inheriting it.
<!-- THOUGHT:END -->
