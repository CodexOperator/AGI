---
id: hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent
mint_id: c28f9cd88b834d99b463d9e1735c1323
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-engine
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
extensions/agi/bin/cli.py (the round commit + cmd_done's exit only) · .agi/config.json (the one cell; if the round gate refuses it, write the exact diff line on the kid node) · one new test file · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 20 production lines · <= 70 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. No test touches a live worktree.

## CORRECTIVE DH.534 -- closes the DH.532 parent review (a00-354f1396 demoted experiment:a00-e399b2d0-597da7 proved -> inconclusive_lean_disproved:35)
BASE      CUT FROM season2/loops/hypothesis-a-stale-index-lock-is-a00-354f1396 tip 4eb9be948 (worktree a00-354f1396; the director landed the config cell there). No merge. Never rebase.
1. HELD LOCK REMOVED (the parent's probe: a live `git update-index --index-info` with cwd = the checkout and no path in argv held .git/index.lock; `_clear_stale_index_lock` printed 'no git holder' and unlinked it) -- the holder test `pgrep -f git.*<checkout>` sees only argv -> a lock is HELD when any process has an open fd on that lock path (/proc/*/fd) OR any git process's cwd resolves inside the checkout; held = never removed, refused by name. One test that reproduces the parent's shape (a git child with cwd = the checkout, path NOT in argv) and asserts the lock survives.
2. The threshold is the literal 900.0 at cli.py:2380 -> read values.core.stale_index_lock_s (now in .agi/config.json at the base); a missing cell = never clear, refuse by name. No literal left.
3. cli.py is +70/-16 vs a 20-line cap -> trim to the mechanism; record the measured net on the kid node.
4. Exercise conjunct 2 end to end once: a real linked worktree (tmp) whose commit fails -> the done path exits non-zero and the harvest line carries `commit FAILED: <reason>`.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_stale_index_lock.py test_cli.py test_dispatch.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp); tmp repos only, never a live worktree
FILE SCOPE extensions/agi/bin/cli.py (the stale-lock check + the commit/exit path only) · extensions/agi/tests/test_stale_index_lock.py · the kid's own node
CEILING   HARD CAP: 1 kid · cli.py net <= 30 over the post branch (the base is +54: trimming pays) · <= 60 more test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.534 QUEUED (dispatch blocked: key mint, credits): the DH.532 parent probe removed a HELD lock (pgrep sees argv only; a git with cwd = the checkout is invisible), the threshold is still a literal 900.0 (the cell was refused in-round; director landed it 4eb9be948), cli.py +54 vs 20, conjunct 2 never run end to end. This round must not merge until 534 clears: a gate that deletes a held lock is worse than none.
<!-- THOUGHT:END -->
