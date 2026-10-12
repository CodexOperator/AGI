---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-4
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
---
# doc:card-director-general-4

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines; rules live in skills, progress on the town board.

## §0 State (10-12 ~00:4xZ)
| | |
|---|---|
| post | director-general-4 under sanctuary-master (SM); builder for DG1/SM; DG2 writes my falsifier lanes first, DG3 is the other builder |
| running | NOTHING (no suite, no runner, no dispatch). ONE heavy lane at a time, niced, only above 3 GiB MemAvailable (cat /proc/meminfo); no scratch on /dev/shm while agi.slice > 4600 MiB |
| skills | agi-rotate · agi-review · agi-dispatch · agi-send · agi-verify · agi-goal · agi-post |
| worktrees | /var/lib/agi/director-general-4/: t (mine) + w-board3 (LIVE, locked: dg4-board3 = 7a96f67619 (commands.md: crons.py caps excluded) on a5c53f47d1 (the .42.1 leaf: cap + mkdir + sudo-pending, on ae0237b3d3) on ae0237b3d3 (renderer fix: a foreign user's default log is ~/logs) on eb944f41c9 (test fix) on b1d83acb51 (the .42 RE-CUT, ONE commit on 9b71aa6daa) + the test fix) + w-board2 (locked, SUPERSEDED: dbbfb2e2a6) + w-capsule3 (LIVE, locked: dg4-capsule3 = 23924e296f FF2 on 4755041c5b FF1 on L7 375139b329; c0bb3f05ef is in L7; w-capsule + w-capsule2 SUPERSEDED). Every other dg4-* branch kept, its worktree removed 17:1xZ |
| scratch | pytest --basetemp, TMPDIR, lane temp, gate trees: ONLY /data/work/gate-director-general-4 (700, my uid); home and /tmp are on the ROOT disk; remove each run's tree when done |

## §1 Plan
```
WAIT    (1) SM re-mints the stack on .42 E eb944f41c9 ON b1d83acb51 (council ACKed b1d83acb51 00:16Z; SM 00:17Z: the rendered-line test went RED in the stack, fixed in eb944f41c9; belam's guard had REFUSED the old three commits: a literal belam home in the crons row, its test and a message; alive acks the edit in one line). (2) SM's gate of the capsule cuts (a0a86ef159), after .41; the council gets the 4 deviations + 7,418 B. Do NOT cut `list`.
HOST    belam: `python3 extensions/agi/bin/crons.py apply --sudo` from MAIN in the SAME MINUTE as the ff of posts/belam; the FIRST live run is the proof.
CAPSULE goal:g7.16.1.11.44 (owner's one container, design doc:g716111-44-capsule-pack, `git show posts/sanctuary-master:.agi/nodes/doc/g716111-44-capsule-pack.md`). ALL SIX leaves .44.1-.6 built in w-capsule: ONE piece `capsule` in engine-capsule.md (pack out verify in regrow repoint) + lane extensions/agi/tests/capsule.t.sh (62 rows, mutants RED, incl. the landing lane). Boxed to SM 22:0xZ with FOUR deviations (fat bundle for a ref behind base; header prerequisite; scratch-repo verify; [moved]) and the size (7,418 B vs ~1.9 KB; I'd drop `list` first). runner-uid fix 3deb115c1e on L8 (dg4-fixrunner, w-fixrunner; belam slab A/B find: the rendered-board row pins a fixture runner). FF1+FF2 are in L8 1ead48f16d (council 01:56Z: FF1 MET). RULING 01:56Z: `capsule move` is NOT a capsule verb: box-move.sh becomes the CALLER of `sect capsule | sh -s -- pack|out|verify|in` (dry pack in a job clone + target verify + scratch pre-stop; real pack/out/carry/in post-stop; the recovery lines; replaces box-move.sh :32-:45). The piece keeps its 8,192 bar (75 B left). No leaf placed yet: only on SM's word.
EXTRAS  on SM's word (not placed): (1) geometry_config.resolved_seat_env v4-rows-only; (2) cc-session-start.sh BOOTSTRAP_SEAT=${AGI_POST:-${AGI_SEAT:-}}; skills-truth CUT/TIP defaults. HELD: .20 retire-the-inbox-write; .20.1 items 2+3. NOT MINE: box-wake.t.sh (DG2).
```

## §2 Landed / boxed (one line each; DG1 judges, SM gates and lands)
```
CAPSULE .44.1-.6 cut 1 b86473037c + cut 2 a0a86ef159 (dg4-capsule), boxed to SM, not yet gated
LANDED  .36 tui · .20 v5 alert · .37 (20a39210c4, C1 6c9d471bc8, next cut + CLOSE 4e38ecb36c, post-env LIVE fix afeec20cce, F6 re-read 72a2678064) · fresh-blob · .13.2 · .35 · kid AGI_POST=$k
REVIEW  .42 option E (SUPERSEDED by b1d83acb51, 00:4xZ): a155fb2792 (code half: crons.py `user:` + `apply --sudo`, board_job.py commit/land, crons.md rows) -> 16b368ad72 (grid_writers pins .13 C1/C5 + N6/P9, `-X theirs`, take-MAIN refusals to the notice) -> dbbfb2e2a6 (council 18:06Z conditions: every user any job names is reconciled; land checks %G?==G AND %GS==belam@agi itself with -c gpg.ssh.allowedSignersFile). APPROVED 3/3 with those two conditions.
ROOT    disk pass done 17:1xZ: home 3.4 GB -> 468 MB, df / 64%.
```

## 🔴 Where it stops
```
Everything of mine is boxed and idle: dbbfb2e2a6 (.42) and a0a86ef159 (.44) await SM; nothing is mid-step, no lane or runner is running.
FIRST ACT: read mail ONCE, whole: AGI_POST=director-general-4 box read | fold -s -w 200 (messages are also commits: git log -1 --format=%B <tip of refs/box/<sender>/director-general-4>).
THEN: a RETURN = ONE new signed commit ON the sent sha in the matching worktree (w-board2 / w-capsule; never a rebase, F26/F14). Gate dir for any run: /data/work/gate-director-general-4. Run the capsule lane: env -u AGI_TRUNK -u AGI_POST sh extensions/agi/tests/capsule.t.sh (AGI_TRUNK in a post's env leaks into the fixture otherwise). Extras only on SM's word.
```

## §4 Traps (this generation's only)
| trap | rule |
|---|---|
| bare prune | NEVER `git worktree prune` on MAIN's shared .git (SM 17:16Z; I ran it once 17:11Z): it drops every entry whose path my uid cannot stat = every other post's 700 gate dir. Remove my OWN tree by path (`git worktree remove <path>`); lock a long-lived one (`git worktree add --lock`) |
| runner fall-through | a background lane runner that waits on MemAvailable must STOP, not run anyway, when the wait ends (I stopped mine at 09:33Z after it was about to run beside SM's gate) |
| pkill -f | `pkill -f <script>` matches my own command line and kills the shell: find the pid with `pgrep -x sh -a` and kill by pid |
| mail (owner 10-11 20:2xZ, via SM) | NEVER box belam: anything for belam goes to SM (he folds it into the ONE ~4 h digest). To SM: one message per finished thing, no [ack]/[thanks]/[landed]. Only [red] or a BLOCKING owner-ruling ask is sent at once. Lands in skill agi-send |
| home literals | belam's landing guard knows EVERY seat's home (HOME_PATH_RE under a post uid knows only its own): grep the added lines AND the commit message for /var/lib/agi/<any name>, /home/, /data/home = 0 before sending; a crons row writes `~/...` (cron expands it as the row's user). Diff a re-cut against the commits' own net (merge-base), never a named sha SM typed |
| new CLI verb | adding a subparser to a bin (crons.py caps) needs a `commands.md` entry (manifest: or excluded: with a reason): run test_commands_manifest.py (4m48s, ~180 rows) before sending, not just the file's own tests |
| capsule lane | env -u AGI_TRUNK first (a post's AGI_TRUNK=<ref> made every fixture `at` read the wrong trunk); a function's last command is its status (a trailing rm made a mutant row pass). Both live in the lane's comments |
| committer email | git verifies an ssh signature against the COMMITTER EMAIL: a machine job signing as the seat commits as `belam <belam@agi>` (the ring principal), never `agi-belam` |

## §5 Verification
Last green (bare env -i, niced, one at a time, scratch on /data): on dbbfb2e2a6: test_board_job 25 · test_crons_job_user 11 · test_grid_writers 27 · test_crons 103 · test_crons_apply_cell 19 · test_thought_hygiene 17 · test_bin_help_smoke 75 · test_agi_bin_absent 17 · test_stand_up 54 · graph-metrics.t.sh / metrics-cell.t.sh / mail-alert-retired.t.sh 0 FAIL. Not mine, red on the trunk side too: test_snapshot_goals::test_wg_reader_lines_only_point_at_the_retirement (SM attributes it from the full suite). Baseline-red earlier: test_cli 1, test_season 11, test_commands 1.

## §6 BANKED
(none for me) · .42's HOST half is belam's ONE GO above · SM banked with belam: a machine identity in the box ring (heal / memory-alarm senders), the owner's call for S3.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
