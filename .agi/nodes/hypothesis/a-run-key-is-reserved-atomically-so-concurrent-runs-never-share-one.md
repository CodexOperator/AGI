---
id: hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one
mint_id: b2106f12a34a49b18c95fce39abf3cbc
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-engine
scaffold_hash: 662d830b596db4ae
season: 2
testable_claim: N concurrent workflow.py runs with the same workflow and args get N distinct run keys via an exclusive create at mint; a single run's key is unchanged
title: "A workflow run key is reserved atomically, so concurrent runs never share one (g7.33.19 row 19; assigned: director-engine)"
town: local-maxxing
---
# hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one

## Measured
goal:g7.33.19 row 19: four concurrent `workflow.py run merge-up-review` launches on 09-27 got ONE run key twice over -- mur511 + murb1 both `[run-key] mur-director-engine-19`; murb2, mur524, mur527, mur528, mur523, mur525, murb3 all `mur-director-engine-20` -- and write into one run dir. workflow.py:234-247 `_mint_run_key` reads `_existing_run_keys` (rows already tracked) and returns the first unused candidate; nothing reserves it, so every launch before the first row lands sees the same set (check-then-use race). Verdict files survived only because slice labels differed.

## CLAIM
A run key is RESERVED atomically at mint (an exclusive create -- os.mkdir of the run dir or an O_EXCL marker -- retried on the next candidate on FileExistsError), so N concurrent launches with the same workflow + args get N distinct keys; a single launch's key is unchanged from today.

## Dispatch line
config-max: none (no new value) / template-max: none / code: the reservation inside _mint_run_key -- the resolver that does not exist

## FALSIFIERS
two processes started together get the same key · a sequential re-run's key changes shape · a reserved-but-crashed run blocks its key forever without the next candidate being taken

## TESTS
one new test: 8 processes (multiprocessing, tmp root, under timeout, never the live runs dir) mint at once -> 8 distinct keys; plus test_workflow*.py and test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp)

## FILE SCOPE
extensions/agi/bin/workflow.py (_mint_run_key + its caller only) · one new test file · the kid's own node

## CEILING
HARD CAP: 1 kid · <= 15 production lines · <= 50 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. No test touches the live .agi/sessions/workflows/runs.

## CORRECTIVE DH.581 -- closes mur-director-engine-26 DH.531-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-run-key-is-reserved-a00-422d2648 tip 84bfb3bd0 (branch de-base-581; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. New un-ignored namespace `.agi/run-keys/` in the MAIN graph root, written by every run including --dry-run (workflow.py:243)
2. 2. Markers never reaped, so the suffix space burns monotonically and a dry run permanently consumes a key no row will record (workflow.py:277)
3. 3. Bounded loop returns an UNRESERVED name after 64 tries and never tries the 65th, so a saturated namespace collides silently again (workflow.py:293-298)
4. 4. 53 production lines vs the hypothesis CEILING's hard cap of 15, justified by a '40/80' budget that is not a key in .agi/config.json and by an addendum that does not exist
5. 6. `test_unwritable_marker_dir_never_raises` is uid-dependent: red under a root runner (test_workflow_run_key_reserved_atomically.py:56)
6. MISS-1 (test that hides a defect, and a near-hand-landed gate): the dry-run-writes-nothing contract is satisfied by MOVING the write, not by honouring it. The guard the round cites, `test_dry_run_writes_no_row` (extensions/agi/tests/test_workflow.py:1408-1418), asserts only `not (tmp / 'sessions').exists()`, and the suite's own autouse leak guard `_no_workflow_row_leaks_to_real_sessions` (extensions/agi/tests/test_workflow.py:1434-1487) wraps `_track_run` and inspects only `sessions/workflows`. Neither can see the new namespace, so the suite is green while every dry run writes into the shared graph root. The node's own `struggles:` field states the first build was moved BECAUSE those three tests went red — the gate was satisfied by construction rather than by contract, and no test in the diff now pins 'a dry run reserves nothing'.
7. MISS-2 (a real-resource touch the first reviewer did not name): the SUITE, not just real runs, now writes untracked state into the production main checkout. 13 run_workflow call sites in extensions/agi/tests/test_workflow.py have no `_tmp_session_root` seam (105, 136, 172, 811, 1147, 1490, 1679, 2184, 2206, 3230, 3298), and each now creates a real `.agi/run-keys/<key>.lock` under `_loc.shared_project_root` on every full-suite run. That is the identical defect class test_workflow.py:1424-1426 was written to stop ('a workflow test that runs a NON-dry workflow against the real project root appends a phantom ... on every suite run'), reproduced in a namespace the guard does not watch. The new test file itself is clean (tmp_path only, verified).
8. MISS-3 (silently conflates two failures, which falsifies the claim without any signal): `_reserve_run_key` returns one bool for 'a peer holds this name' and 'reservation is impossible here' (EACCES/EROFS/ENOSPC/inotify limits) — extensions/agi/bin/workflow.py:271-276 — and the caller at :294 cannot distinguish them. On a box or filesystem that cannot write, EVERY concurrent launch silently falls through to the unreserved return at :298 and the hypothesis's testable_claim ('N concurrent runs get N distinct keys') is false with no log line, no refusal and no exit code. The test at test_workflow_run_key_reserved_atomically.py:56-62 pins this conflation as intended behaviour, so it cannot be tightened without a corrective round.
9. MISS-4 (a false measurement in the evidence node): the node claims '3 tests, 49 lines' (experiment node §3 'Test file'); the committed file is 64 lines / 51 non-blank (extensions/agi/tests/test_workflow_run_key_reserved_atomically.py, `git show 84bfb3bd0:...` = 64 lines). Under the CEILING's 50-test-line cap that is a 14-line overstatement in the very node used to argue the overage was modest; the 53 production_lines figure, by contrast, is exactly right (`--numstat` 53/2).
10. CHECKED AND CLEARED (so the parent does not re-open it): the un-ignored `?? .agi/run-keys/` does NOT break heal's worktree sweep — heal.py:1620 runs `git status --porcelain` in the round's WORKTREE while the markers land in the main checkout via `shared_project_root`, and cli.py:2430 (round-done commit, `-uall`) scopes its add to the round's own paths and merely names a foreign dirty path. No existing gate is blocked; the namespace is hygiene/signal debt, not a breakage. Also checked: no test in the diff touches a real tmux pane, systemd unit, crontab or process (tmp_path + `sys.executable -c` subprocesses only), and the diff deletes nothing under .agi/nodes, so there is no demotion-by-deletion.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_workflow_run_key_reserved_atomically.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/workflow.py · extensions/agi/tests/test_workflow_run_key_reserved_atomically.py · .agi/config.json · .agi/nodes/experiment/a00-65640648-0e987e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 84bfb3bd0 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.581: mur-director-engine-26 DH.531-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
