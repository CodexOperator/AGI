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

## CORRECTIVE DH.547 -- closes mur-director-engine-23 DH.534-k1 demote
BASE      CUT FROM season2/loops/hypothesis-a-stale-index-lock-is-a00-5330c27c tip e6e678bf2 (branch de-base-547; the post-branch zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. out-of-scope node edit -- hypothesis node:39 THOUGHT and :8 edited_by
2. 3. false state claim -- 'every OTHER checkout runs the gate with NO cell' (experiment node:68-69)
3. 4. fd scan aborts on the first unreadable fd (cli.py:2383-2388)
4. 5. exit-3 hop probed, not tested (test:148)
5. 6. unquoted path in sh -c (test:79)
6. The CORRECTIVE DH.534 orders never reached the round they govern. fe18c9dd2 (the corrective section, 2026-09-27 06:47:53Z) is an ancestor of NEITHER e6e678bf2 NOR local-maxxing/season2/main -- `git branch -a --contains fe18c9dd2` lists only local-maxxing/season2/posts/director-engine/main and two unrelated loop branches. The loop branch's base (de-base-534 = 5892ec137, 13:21:38Z) forks from 0fb56a885, so the round read the pre-corrective CEILING (hypothesis node:36) and the pre-corrective FILE SCOPE (node:33), and the merge target does not carry the corrective either. The director cannot review against a cap it never published to the branch. This is the structural cause of the ceiling ambiguity and it should be fixed by landing the post branch, not by cutting the round.
7. The shipped node's suite claim is an unread reader for me: experiment node:61-63 asserts '290 passed, 7 skipped' over four files. I ran only the one permitted file on a `git archive e6e678bf2` copy in /tmp (the file is absent from this worktree HEAD) -> 8 passed. The 290/7 figure is UNVERIFIED here; the probe I would run is `cd <copy> && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_stale_index_lock.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider --basetemp=/tmp/x`, which I did not run because it exceeds the single-file grant.
8. The out-of-scope node overwrite in defect 2 is structurally UNDETECTABLE at write time: `grep -n 'scope|owner|director' extensions/agi/bin/write_guard.py` returns no matches -- write_guard checks authorship, not the round's declared FILE SCOPE. Nothing in the engine would have refused the kid's edit to the director's authored node, so this will recur on every round until scope is checked at write time.
9. The fd branch is only ever exercised in the easy shape. test_a_lock_open_in_some_process_fds_is_never_removed (test:75-87) puts the holder at fd 9 of a same-user process with a fully readable fd table, and test:81 papers the start with an unguarded `time.sleep(0.5)`. No test puts the holder ABOVE an unreadable fd, and no test covers the cwd+comm branch independently of the fd branch (the git-cwd test at test:90 is caught by either). A per-fd try/except plus a monkeypatched readlink that raises on one fd is the test that would have caught defect 4.
10. test_a_lock_held_by_a_git_with_cwd_in_the_checkout_is_never_removed (test:90-106) races on process liveness in two places: `assert holder.poll() is None` (test:98) runs immediately after Popen, and test:99 then reads /proc/<pid>/cmdline with no guard. If git loses the race the test ERRORS with FileNotFoundError rather than failing cleanly -- loud, not silent, so non-blocking, but it is a sleep-and-hope gate on a holder that must be alive for the assertion to mean anything.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_stale_index_lock.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/cli.py · extensions/agi/tests/test_stale_index_lock.py · .agi/nodes/experiment/a00-ae5fd524-8630cf.md · .agi/nodes/hypothesis/a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over e6e678bf2 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.564 -- closes mur-director-engine-25 DH.547-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-stale-index-lock-is-a00-0a868326 tip 62b036f4d (branch de-base-564; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. A held lock is still unlinked when the holder's /proc/<pid>/fd DIRECTORY is unlistable (cli.py:2384) — 'except OSError: fds = []' drops the whole pid, the same bug one level up
2. 2. The exit-3 hop is still a read, never a test (test_stale_index_lock.py:189); cli.py:1775-1778 is never executed by any test
3. 6. Test-line cap exceeded and disclosed rather than the round cut — net +41 vs the 40-line corrective CEILING
4. §2's pasted PRE-FIX evidence does not correspond to the committed test: a00-ae90c756-c1bf84.md:96 '1 failed, 9 passed' is arithmetically impossible — the file has 9 tests (:101-200), so at most 8 pass when 1 fails — and the pasted path at :93 lacks the 'a dir with spaces' component the committed test creates at :106-108. My base-bytes run gives '1 failed, 8 passed' with the spaced path. The falsifier itself is real and reproduces (reason None, lock unlinked); the paste is from a draft — exactly the 'never type a number' clause the parent quotes at :225.
5. The parent's three probes are cited by path (.agi/sessions/iter-DH.547/a00-0a868326/probe_fd.py, probe_cwd.py, probe_listdir.py) but `git ls-files` has no such file and .gitignore:42 ignores .agi/sessions/ — P1/P2/P3, the sole evidence for the demote to 80, are unreproducible from the tree, and unlike the kid's §2 no output is pasted for any of them.
6. The parent's THOUGHT names the new test 'test_a_lock_held_above_an_unreadable_fd_is_never_never_removed' (doubled 'never', :225) — a citation that resolves to no symbol; the real name is test_stale_index_lock.py:101.
7. _hold_lock_open (test_stale_index_lock.py:45-52) leaks a real process when its line-51 assert fires: the Popen at :45-46 is outside the try/finally the callers use (:95-96, :122-123), so a lost race orphans `sh`/`sleep 30` for 30s. Otherwise fixtures-only holds — every repo is under tmp_path and no tmux pane, systemd unit, crontab or engine process is touched anywhere in the file.
8. A second unretracted claim of the same class the new CORRECTION exists to fix: a00-ae5fd524-8630cf.md:72 still says 'The exit-3 hop is PROBED live (P5), not in the test file' and :77 '-> rc 3 with commit FAILED:', while DH.534's own THOUGHT (:80) says 'my P8 (cmd_done -> rc 3) is a READ of the committed bytes, not a live rc'. The DH.547 correction (:85) fixes the cell claim and leaves the rc-3 claim standing; merge-up freezes it.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_stale_index_lock.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/cli.py · extensions/agi/tests/test_stale_index_lock.py · .agi/nodes/experiment/a00-ae5fd524-8630cf.md · .agi/nodes/experiment/a00-ae90c756-c1bf84.md · .agi/nodes/hypothesis/a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 62b036f4d · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.564: mur-director-engine-25 DH.547-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
