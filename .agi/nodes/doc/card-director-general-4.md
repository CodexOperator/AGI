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

## §0 State (10-14 06:5xZ) — RESUMED by the owner (06:2xZ "go, let's re-enable all the automated things ... keep trucking along until all bundle goals are closed and we can do season rollover"); keepalive is IDLE-ONLY now. GOAL: close every goal:g7.16.1 bundle, then season rollover
| | |
|---|---|
| post | director-general-4 under sanctuary-master (SM); builder for DG1/SM; DG2 writes my falsifier lanes first, DG3 is the other builder |
| running | NOTHING: no suite, no runner, no dispatch, no build, no review, no council round. I own NO session cron (CronList empty). Quiet rule to the owner stands: ONE digest per ~4 h via belam; I NEVER box belam, only SM (one message per finished thing, `[red]` + blocking owner asks excepted) |
| skills | agi-rotate · agi-send · agi-verify · agi-goal · agi-post (+ agi-review / agi-dispatch only if SM dispatches) |
| worktrees | /var/lib/agi/director-general-4/: t (mine, detached = posts/director-general-4) + LIVE locked: w-boardlog (dg4-boardlog 63b21a5b90) · w-pins (dg4-pins 5b6e7b00cb) · w-ownrow (d37799e298) · w-fixrunner (3deb115c1e) · w-capsule3 (23924e296f) · w-board3 (7a96f67619). SUPERSEDED, safe to `git worktree remove <path>` BY PATH: w-board2 (dbbfb2e2a6), w-capsule (a0a86ef159), w-capsule2 (c0bb3f05ef). Every dg4-* branch is kept |
| scratch | pytest --basetemp, TMPDIR, lane temp, gate trees: ONLY /data/work/gate-director-general-4 (700, my uid); home and /tmp are on the ROOT disk. One heavy lane at a time, niced, only above 3 GiB MemAvailable |

## §1 Plan (nothing in flight)
```
BOARD   (SM 10-14 06:3xZ) live trunk 93df4efce0 (SM said a35328430e; check `git rev-parse origin/local-maxxing/season2/main` before any send). Stack 14 (DG2 .39.3+.39.4, DG5 .22+.41.1, SM 0ad0eb2e7d) re-gates; stack 15 = DG5 .41 cut 2 2ca8bbd4de. Owed by others: DG1 test_seat_alias_notice fix, DG5 the verify-v5-uid l3-credentials leaf under .43. All 14 of my shas are ON the trunk.
DONE    I answered SM's CLOSE/DEFER ask (06:4xZ). SM's reply 06:4xZ: bundle lines TAKEN. .44.7 (box-move.sh as the capsule CALLER) ALREADY EXISTS and is DG2's ("CLOSE .44.7 after stack 14 gates"): ONE owner, DO NOT cut a second .44.7.
DONE 06:5xZ  CLOSE commits boxed to SM: branch dg4-close2 tip 1aaf54c2bd (base trunk 93df4efce0): 7 signed write.py commits closing .42 .42.1 .44.1 .44.2 .44.4 .44.5 .44.6 (worktree w-close2, locked). HELD by SM: .44.3 (closes with the gate's landing-lane wiring, row l4) and .44 (closes AT the rollover run).
DONE 06:5xZ  gate-(c) row 5c + its mutant boxed to DG2 (one message) as a falsifier row for .44.7.
DONE 07:1xZ  REVIEWED DG2's .44.7 cut 2f990f92b8: ACCEPT, lane 70 ok/0 FAIL re-run (also with ambient AGI_TRUNK); 4 non-blocking residues boxed to DG2 for his re-cut onto the trunk; verdict boxed to SM. .11.20.1 target 1 = 128ae202c8 already on the trunk (boxed in CLOSE form). Nothing owed by me; wait for SM.
DONE 09:0xZ  CLOSE .44.3 = af0df494e8 (branch dg4-close3, worktree w-close3 locked, on L14 882517c523) boxed to SM in close form, rides stack 15. NEXT: review DG2's .44.7 re-cut delta when it comes (git diff 2f990f92b8 <new tip> -- extensions/agi/guard; re-run box-move-refs.t.sh, expect 70 ok; check his 4 residues). .44 parent closes only at the rollover run.
DONE 16:0xZ 10-14  SYNCED to L17 5ab8974ca8: posts/director-general-4 = 24c140beff (merge, trunk side for the 5 skills paths, byte-equal to the trunk); agi-sync prints nothing rc 0; [synced] boxed to SM. The [trunk-conflict] hook warning is gone. origin core/season3/main was overwritten (old tip kept as origin archive/core-season3-main-pre-20261014): never push to it from the old line.
DONE 19:1xZ 10-14  ROLLOVER STACK 20 = df7f93568a (ratified by the council 18:40Z) + RE-CUT 2fac120652 (R1 ancestor head = 2-parent merge, R2 --skip-fold owner-given, R3 core BEHIND = in-run ff + post-check, R4 half-rolled RECOVERY lines, (iv) align row; 104 targeted season tests green; each row + a mutant RED), branch dg4-roll2 / worktree w-roll2 (locked), boxed to SM. HOLD: no further cut, no re-dry, NEVER --apply until SM sends the PASS tip (owner-word PASS + belam's merge into season3/main); then RE-DRY with --judge-tip = the PASS tip (not ef9b043e68), paste WHOLE. Dry-run recipe: scratch-edit the 3 season-1 town cells to 2, `python3 -u extensions/agi/bin/season.py --root .agi rollover --global --judge-tip <PASS tip>`, `git checkout -- .agi/nodes/town`. A RETURN = ONE new signed commit ON 2fac120652 in w-roll2. Memory: only test_season* files while agi.slice is over.
EXTRAS  on SM's word (not placed): geometry_config.resolved_seat_env v4-rows-only; cc-session-start.sh BOOTSTRAP_SEAT=${AGI_POST:-${AGI_SEAT:-}}; skills-truth CUT/TIP defaults. HELD: .20 retire-the-inbox-write; .20.1 items 2+3. NOT MINE: box-wake.t.sh (DG2).
```

## §2 Landed / boxed (one line each; DG1 judges, SM gates and lands)
```
ON THE TRUNK b71fbe86d5 (checked 04:3xZ)  .42 E + its fix-forwards (b1d83acb51, eb944f41c9, ae0237b3d3 renderer, a5c53f47d1 the .42.1 leaf cap/mkdir/sudo-pending, 7a96f67619 commands.md caps) · .44.1-.6 capsule (c0bb3f05ef in L7; FF1 4755041c5b + FF2 23924e296f: behind-base refs ride as ref lines, thin bundle, ONE update-ref transaction; engine-sizes b7) · 3deb115c1e runner-uid pin · d37799e298 own-block row.
        earlier: .36 tui · .20 v5 alert · .37 · fresh-blob · .13.2 · .35 · kid AGI_POST=$k
IN L13 f632cd4854 (SM's line; origin trunk catches up)  63b21a5b90. The pins 1ecd97928f 4f1009ca58 5b6e7b00cb landed earlier (trunk 67730b8fb7)
```

## 🔴 Where it stops
```
10-15 07:4xZ  SEASON 3 IS ROLLED (apply rc 0 by belam as agi-belam, 06:21-06:24Z; I was the runner of record and checked every paste: dry == apply but the expected lines; origin read by me). season3/main 2a8056bcb5; live trunk core/season3/main (origin 420e00ae9c at 07:43Z); freeze ended 06:28:21Z; rotation LIFTED.
10-15 08:09Z SM: ALL 12 POSTS RESTARTED on AGI_TRUNK=core/season3/main (mine reads core/season3/main in env); BOX MOVES UNBLOCKED; landings still only through SM (LAND_TRUNK=refs/heads/core/season3/main). In flight, not mine: B-3 (belam), S26 (SM gate), DG2's Falsifier 1 on .44.7.
NOTHING owed by me. SM 07:45Z: .44 and .44.7 stay OPEN (HORIZON s3): Falsifier 1 needs the first real box move after belam's restart, measured by DG2, who cuts the .44.7 close; .44 closes after, with its own THOUGHT (the rollover never called box-move/capsule). Worktrees w-roll2 and w-align REMOVED 07:5xZ (clean, no --force); branches dg4-roll2 (4a219cab82) and dg4-align (522a842a0b) kept as history.
FIRST ACT on resume: AGI_POST=director-general-4 box read | fold -s -w 200 ; send only with a stdin heredoc (an arg-only send arrives EMPTY). A RETURN on a cut = ONE new signed commit ON the sent sha in the matching worktree; `agi-at <path>` ONLY in ~/t.
```

## §4 Traps (this generation's only; the 4 inherited ones moved to skills/agi-post + agi-memory-guard at this rotation; these move at the next)
| trap | rule |
|---|---|
| mail (owner 10-11) | NEVER box belam; to SM one message per finished thing, no [ack]/[thanks]/[landed]; only [red] or a BLOCKING owner-ruling ask at once |
| the sha in a box message | `git rev-parse HEAD` FIRST, then compose the heredoc with it inline (I sent two [cut]s with "the sha is below" and no sha) |
| home literals | belam's guard knows EVERY seat's home: grep the added lines AND the message for /var/lib/agi/<name>, /home/, /data/home (anonymize.HOME_PATH_RE itself, in python; allowed_signers is not a home); a crons row writes `~/...` |
| new CLI verb | a subparser added to a bin needs a commands.md entry (manifest: or excluded: + reason): run test_commands_manifest.py (4m48s) before sending |
| scanned sites | a new engine piece/bin line with update-ref / commit-tree / mktree / hash-object -w / fetch moves test_grid_writers C1/C7 (goal:g7.16.1.11.13 pins): run it before sending; re-cut the blocks with the test's own norm/run, classify each site in a row |
| ambient uid | a test must pin its runner (monkeypatch crons._invoking_user), never assert on the uid running pytest (belam's slab A/B found it) |
| capsule lane | env -u AGI_TRUNK first; a shell function's last command is its status (a trailing rm made a mutant row pass) |

## §5 Verification
Last green (bare env -i, niced, one at a time): test_board_job 29 · test_crons_job_user 20 · test_crons 103 · test_crons_apply_cell 19 · test_crons_log_cap_declared_scope 17 · test_grid_writers 27 · test_thought_hygiene 17 · test_bin_help_smoke 76 · test_commands_manifest 182 · capsule.t.sh 66 ok / 0 FAIL · engine-sizes 0 FAIL (engine-capsule.md fenced 8,117 B = 75 B under its bar) · graph-metrics / metrics-cell / mail-alert-retired 0 FAIL.

## §6 BANKED
- `capsule move` is box-move.sh's caller work, not a verb (council 01:56Z); its gate (c) is above. `list` selector stays (SM: do not cut).
- RESIDUES named, not fixed: a cron row's custom `log:` outside `~/logs/` is neither capped nor mkdir'd; `in` transports refs/grid verbatim when a packer passes `--ref 'refs/grid/*'` (council 03:25Z (b), ruled, not a refusal).
- UNEXPLAINED: belam's first live `apply --sudo` (00:32Z) printed `pending` for both foreign users although their crontabs read back == desired; my reproduction (a stateful fake `sudo crontab -u`) showed the old path installs NOTHING for a user with no crontab, so something else installed them. Fixed the path (a5c53f47d1); the mystery is SM's/belam's to look at.
- SM banked with belam: a machine identity in the box ring (heal / memory-alarm senders), the owner's call for S3.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
