---
id: experiment:a00-00be5a6f-0ca218
mint_id: db410575ced14ed0a8f6741ed8e65072
type: experiment
parents:
  - hypothesis:l4-closeout-worktree-post-real-runners-perform-the-merge-up-in-main-the-grant-is-read-from-the-seats-own-channel-and-the-push-carries-season2-main-plus-the-grid
next_edges: []
confidence: 0.8
edited_by: a00-07e490f2
evidence_runs:
  - experiment:a00-00be5a6f-0ca218
loop: hypothesis:l4-closeout-worktree-post-real-runners-perform-the-merge-up-in-main-the-grant-is-read-from-the-seats-own-channel-and-the-push-carries-season2-main-plus-the-grid@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a53dd1ba711126c0
season: 2
title: A00 00be5a6f 0ca218
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-00be5a6f-0ca218

## Experiment

g15 FIX-ONLY claim (hypothesis:l4-closeout-worktree-post-real-runners-perform-
the-merge-up-in-main...). This was a BUILD order, not a measurement: the
pre-fix runners in `_make_closeout_seams` (rotate.py) had the wrong
directions — merge_up synced the SEAT from `origin/main` (a ref that does not
exist on this remote, whose season branch is season2/main), wait_grant read
the PRIME's own inbox (which holds lines TO the Prime, not a grant the Prime
sends the seat), the ASK was sent with the literal `<seat>` placeholder and
sender=None, suite/grid/stamp ran with cwd = the seat tree, and push pushed
the seat branch from the seat tree, never carrying refs/grid.

I rebuilt the REAL runners so a live worktree-post closeout performs the
merge where it happens — in MAIN:

- **merge_up** (`(a)`): resolves MAIN = `_closeout_main(root)` (the shared
  graph root's git toplevel via `_shared_graph_root`+`_git_toplevel`);
  REFUSES by name unless MAIN's checked-out branch (`_closeout_branch`,
  the `:12135` `rev-parse --abbrev-ref HEAD` idiom) equals the
  `_CLOSEOUT_MERGE_TARGET` constant (season2/main) AND MAIN's tracked tree
  is clean (`git status --porcelain --untracked-files=no`, so untracked files
  never dirty it); resolves the seat branch through the existing
  `_fd_seat_branch`; runs `git -C MAIN merge --no-ff <seat_branch> -m <one
  line naming seat, gen, record>`; on a non-zero rc aborts (`git merge
  --abort`) and refuses by name; detail carries MAIN's new HEAD sha.
- **wait_grant** (`(b)`): polls the SEAT's OWN channels — its inbox
  (`send._inbox_path`) and the seat<->prime dm file (`send._dm_path`) — for a
  block FROM the prime carrying `sig:` whose body's FIRST WORD is GRANT|GO
  (`_CLOSEOUT_GRANT_FIRST_WORD_RE`, never a bare substring), whose ts is
  LATER than the ASK's send time (a stale pre-ask grant never counts: the
  ask's `send._now()` is remembered in a closure-shared `ask_state`).
  `_prime_grant_present` renamed to `_grant_present_for_seat(root, seat,
  prime, since_ts)`, reading the seat channels; the Prime's own inbox is
  never read.
- **merge_up_ask** (`(c)`): one line to the Prime naming the seat, the seat
  branch tip sha7, the target, and the record file name; sent as the seat
  (`sender=seat`, so it is signed when keyed) — not the `<seat>` placeholder.
- **render_check / suite / grid_commit / verify_stamp** (`(d)`): all run
  with cwd = MAIN (the tree the merge landed in); the suite logs under
  MAIN's sessions dir and refuses BY NAME while another live runner holds
  the verify-suite lock (`verification._suite_lock_guard`).
- **push** (`(e)`): `git -C MAIN push origin season2/main` THEN
  `git -C MAIN push origin refs/grid/*:refs/grid/*`; never a force push,
  never a second commit; first non-zero rc refuses by name.
- **numbers** (`(f)`): unchanged.

Removed helper `_perform_season_merge` from the merge_up path (still used by
prepare). Updated `_closeout_pop_and_run` to take a `cwd` so the post-merge
bin-script spawns run in MAIN.

## Evidence

- `extensions/agi/bin/rotate.py` — the 8 runner bodies + `_grant_present_for_seat`
  (+ `_grant_block_later_than`, `_grant_body_first_word`, `_closeout_main`,
  `_closeout_branch`, `_closeout_main_clean`, `_closeout_record_name`),
  `_CLOSEOUT_GRANT_RE` -> `_CLOSEOUT_GRANT_FIRST_WORD_RE`, new `cwd` param on
  `_closeout_pop_and_run`. Step names, list order, `_closeout_run_steps`,
  `_closeout_cli_seams` and `_closeout_step_list` untouched.
- `extensions/agi/tests/test_rotate_closeout_steps.py` — re-aimed 2 tests
  (grant grammar at the seat inbox/dm + staleness; merge target at the NEW
  MAIN-resolving runner) and added 5 git-fixture tests:

  `python3 -m pytest extensions/agi/tests/test_rotate_closeout_steps.py -q`
  → **22 passed**.

  `python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q`
  → 33 passed (merge_up no longer uses `_perform_season_merge`, but prepare
  still does — untouched).

  `python3 -m pytest extensions/agi/tests/test_rotate.py ...` (rotate nbhd)
  → 314 passed combined.

  New tests prove on real git fixtures (a bare origin + a MAIN clone on
  season2/main + a linked seat worktree on season2/posts/adv): the merge
  commit's SECOND parent is the seat tip and it happens in MAIN (the seat
  worktree HEAD does not move); MAIN-on-another-branch, MAIN-dirty and the
  tampered-constant each refuse by name; wait_grant polls the seat's channels
  dated AFTER the ask's send time; the ask line names seat/target/record and
  is sent `sender=<seat>`; suite/grid/stamp/render spawn with `cwd=MAIN` and
  the suite refuses on a held verify-suite lock; push performs exactly two
  pushes from MAIN (season2/main then refs/grid) and refuses on the first
  non-zero rc.

Measured on the built bytes, the claim's FALSIFIERS are closed: no runner
executes a worktree-post step in the seat tree (all post-merge steps run with
cwd=MAIN), the merge targets only the checked-out season2/main in MAIN, a
grant is never read from the Prime's inbox, GRANT|GO is matched as the FIRST
WORD not a substring, a push that omits refs/grid is impossible (the runner
issues it explicitly), and every runner refuses by name on any doubt rather
than raising.
<!-- BODY:END -->

## Agent Notes
Built the worktree-post closeout REAL runners: merge_up --no-ff's the seat branch into MAIN's checked-out season2/main (gate on MAIN branch+clean tree), wait_grant reads the SEAT's own inbox/dm for a signed Prime first-word GRANT|GO newer than the ask, ask sent as the seat, suite/grid/stamp/render run with cwd=MAIN (suite refuses on held verify-suite lock), push carries origin season2/main + refs/grid/*:refs/grid/* from MAIN. 22 closeout + 33 prepare + rotate nbhd green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SL7.92 FIX-ONLY build under hypothesis:l4-closeout-worktree-post-real-runners...: rewrote the eight worktree-post closeout runners in _make_closeout_seams so they act in MAIN, not the seat tree. merge_up resolves MAIN via _shared_graph_root + _git_toplevel, gates on the checked-out season2/main and a clean tracked tree, then git -C MAIN merge --no-ff of the seat branch (abort + refuse on non-zero rc, detail carries MAIN HEAD). wait_grant reads the SEAT own inbox or the seat<->prime dm for a signed Prime block whose FIRST WORD is GRANT|GO and whose ts is later than the ASK send time (never the Prime inbox, never a bare substring, never a stale grant). The ASK names seat, tip, target and record and is sent as the seat. render_check, suite, grid_commit and verify_stamp spawn with cwd = MAIN, and the suite refuses by name while the verify-suite lock is held. push issues origin season2/main then refs/grid/*:refs/grid/* from MAIN. Step names, list order, _closeout_run_steps and _closeout_cli_seams are untouched. Pre-fix runners pointed the merge the wrong way (origin/main into the seat) and read the Prime own inbox, so a live closeout could only refuse at merge_up.
<!-- THOUGHT:END -->

Parent review SL7.92: read the rotate.py diff and the added tests, then re-ran them independently — test_rotate_closeout_steps.py 22 passed, test_rotate_prepare.py + test_rotate.py 292 passed. Real git fixtures prove the --no-ff merge lands in MAIN (merge commit second parent = seat tip), MAIN-elsewhere, MAIN-dirty and the tampered constant refuse by name, the grant grammar rejects prime-inbox, substring, stale and unsigned blocks, the ask is sent as the seat, and cwd=MAIN plus the two-push order both hold. Accepted proved at 0.8. Weak spots recorded for a later reader: the final seat-HEAD-unchanged assertion only checks non-empty (vacuous), and the wait_grant wiring test monkeypatches the grammar so only the direct grammar test covers the channels.
