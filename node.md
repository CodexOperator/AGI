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

## CORRECTIVE DH.594 -- closes mur-director-engine-30 DH.564-k1 demote
BASE      CUT FROM season2/loops/hypothesis-a-stale-index-lock-is-a00-fd081745 tip bf1d12489 (branch de-base-594; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Held-lock clause still falsified in the shipped shape: the refusal is comm-ALLOWLISTED, so an uninspectable NON-git holder's lock is unlinked (cli.py:2388 with :2414).
2. 2. The demotion lives only in the node body; frontmatter still reads inconclusive_lean_proved:80 (node:21).
3. 3. The new safety test builds its holder as_git=True, the one comm the allowlist refuses, so it can only be green (test:248).
4. 4. A kid's failed round commit is named in no dm (tier=kid sends _completion_line, no commit_failed) (cli.py:1020).
5. 5. Agent record + manifest mirror are set status=done before the commit (cli.py:1603).
6. 6. lock-refusal -> rc 3 is joined only by a probe, never by a test (test:210).
7. 7. Production overage (+33) undisclosed in the round (node:21 / node:117).
8. 8. Duplicate `## CEILING` heading (:36 and :61) with ROUND NOTES wedged between (hypothesis node:36).
9. 9. push_further says the node corrections are unlanded, which bf1d12489 itself lands (hypothesis node:9).
10. 10. The refusal is host-global (any unreadable git-comm pid anywhere blocks every clear) (cli.py:2411).
11. 11. Malformed-config refusal path has no test (cli.py:2472).
12. The round edited the ceiling it is judged by, and the diff never shows the cap that governed it. b5b6b9e64 inserts a SECOND `## CEILING` into the director's hypothesis node and rewrites FILE SCOPE (:34), while the governing DH.564 CEILING ('<= 15 production lines net over 62b036f4d · <= 40 test lines', parent-branch hypothesis node:85) is NOT in this branch at all — the branch's node carries no CORRECTIVE section, so a merge-up reader of 62b036f4d..bf1d12489 alone cannot see the cap the round was held to. The inserted copy at node:37 also drops the enforcement clause node:62 still carries. That is the node-side shape of 'a round that fixes the gate it must pass through', and the first reviewer's item 7 cites only the miscount, not the edit.
13. The new exit-3 test monkeypatches `_alarm_dispatcher_on_done` itself (test:226), so the real dm builder — cli.py:1016-1047, the only code that turns `commit_failed` into a body anyone receives — never executes. The assertion at test:236 checks a captured kwarg, not a sent body. Paired with defect 4 (the kid branch builds `line` with no commit_failed), the suite is green while the shipped kid path silently drops the reason: a green test that can require a defect, distinct from the first reviewer's items 3/4/6.
14. The load-bearing ENOENT arm of `_uninspectable` (cli.py:2382-2383, 'the pid EXITED mid-walk: provably no holder') has no test, and neither does the comm-unreadable '?' arm (cli.py:2386-2387). The only monkeypatched listdir in the file (test:251-254) raises PermissionError, never FileNotFoundError, so the decision that keeps the gate usable is exercised by nothing — and it is the very decision node:62 rests its 'refusing on every pid would refuse every commit' argument on.
15. The host reading that justifies the comm allowlist is internally inconsistent and does not measure what it is used for. node:62 says 'five live pids are permanently unreadable' but the paste lists four (node:67-70; 2102 shows only a cwd failure, no fd failure), and the parent's own THOUGHT calls it 'four same-uid uninspectable pids' (hypothesis node:65). A safety decision rests on that paste rather than on a falsifier — which node:161 itself names as the next round's job.
16. Suite claims I could not verify inside the single-file grant. node:102-103 claims test_cli.py + test_brief.py '227 passed' — UNVERIFIED here. What I did run, on a `git archive bf1d12489` copy in /tmp: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_stale_index_lock.py -q -p no:cacheprovider --basetemp=/tmp/pt564` -> 11 passed, 70.02s, matching node:100's count (its 34.90s duration is machine-dependent, not a correctness claim). The probe I WOULD run and did not, because it exceeds the one-file grant: `cd /tmp/rev564 && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_brief.py -q -p no:cacheprovider --basetemp=/tmp/pt564b`.
17. Ownership checks I re-ran fresh, for the record. NO deletion or move under .agi/nodes: a00-76c416dd-0bb9b2.md is a pure addition (162 insertions, 0 deletions) and the other three node files are edits in place — no demotion, no git rm. NO test touches a real resource: every repo in the file is under tmp_path, the holders are `sh -c` children in those tmp repos (test:48-50, :172-174), there is no tmux/systemd/crontab/`ps` call anywhere in the diff, and the project's autouse tmux guard (extensions/agi/tests/conftest.py:329) is in force. The threshold is a real config cell, not a literal (cli.py:2445-2459; .agi/config.json values.core.stale_index_lock_s=900 present in both 62b036f4d and bf1d12489).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_stale_index_lock.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/cli.py · extensions/agi/tests/test_stale_index_lock.py · .agi/nodes/experiment/a00-76c416dd-0bb9b2.md · .agi/nodes/experiment/a00-ae5fd524-8630cf.md · .agi/nodes/experiment/a00-ae90c756-c1bf84.md · .agi/nodes/hypothesis/a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (k1 = cli.py + its tests, k2 = the node-text items) · <= 15 production lines net over bf1d12489 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.627 -- closes mur-director-engine-35 DH.594-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-stale-index-lock-is-a00-4ddd45d6 tip e85cd5388 (branch de-base-627; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. The new non-dumpable exit waives a refusal the base made, on an unmeasured safety claim — extensions/agi/bin/cli.py:2406
2. 2. Refuse-to-unlink holds at the fd-DIRECTORY arm only; a lock open on an individually unreadable fd still reads as 'no holder'; the cwd backstop was removed in the same diff — extensions/agi/bin/cli.py:2455
3. 3. push_further still carries the claim the same node calls false — .agi/nodes/hypothesis/a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent.md:9
4. 4. Pasted probe output that does not reproduce — .agi/nodes/experiment/a00-9dfef904-01bf3b.md:43 ('16 passed in 0.81s')
5. MISS 1 (the round's own claim is false in the code, and a green test sits on it): a00-9dfef904-01bf3b.md:38 and the hypothesis node's Agent Notes (:134) both assert the failed-commit restamp is 'mirrored into the manifest ... status=done at :1603 no longer survives a failed commit'. It does not. `cmd_done` already wrote status=done and mirrored it at cli.py:1678; the new block at cli.py:1775-1778 re-stamps the AGENT RECORD and then calls `_mirror_terminal_into_manifest` with rec['status']='failed' — and that function refuses to downgrade: `_AGENT_STATUS_RANK` (cli.py:3004-3011) ranks failed=3 below done=5, and the guard `if rec_rank >= _merge_status_rank(entry)` (cli.py:1101) leaves `target` None, so cli.py:1104 returns and manifest.json keeps reading `done`. The new test asserts only `(rec/"agent.json")["status"] == "failed"` (test file :328) and never opens manifest.json — a green test over a claim no code executes. Worth recording as the silver lining: had the manifest been restamped, `workflow.py:2225-2226` would take its FIRST branch (`if rec.get("status") in ("failed","timeout","stalled"): return 3, None`) and drop the round's entire harvest; the rank guard is the only thing standing between this diff and that.
6. MISS 2 (a new fail-closed flake, untested): the two new `os.stat` calls in `_uninspectable` (cli.py:2404, 2406) are wrapped by `except OSError: return "?"` at cli.py:2408-2409. A pid that exits between the SUCCESSFUL `os.listdir(f"{base}/fd")` at cli.py:2434 and the stat at :2404 is therefore returned as an UNKNOWN HOLDER and refuses the whole commit — the ENOENT arm at cli.py:2401 only covers an exc raised BY the listing itself, not a stat that fails after it. The branch's own count for this walk is 578 pids (a00-d506aa2a-5351fb.md:76) on a host where the loop spawns and reaps agents continuously, so the window is live. No test covers the stat arm. NOT RUN, reported as UNVERIFIED: I would monkeypatch `os.stat` to raise `FileNotFoundError(2, ...)` for one real same-uid pid in the current process's own table and assert `cli._clear_stale_index_lock(root, repo) is None` (a dead pid must not refuse) — a unit call on the two module functions, no dispatch/rotate/heal/send.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_stale_index_lock.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/cli.py · extensions/agi/tests/test_stale_index_lock.py · .agi/nodes/experiment/a00-76c416dd-0bb9b2.md · .agi/nodes/experiment/a00-9dfef904-01bf3b.md · .agi/nodes/experiment/a00-d506aa2a-5351fb.md · .agi/nodes/hypothesis/a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over e85cd5388 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.627: mur-director-engine-35 DH.594-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
