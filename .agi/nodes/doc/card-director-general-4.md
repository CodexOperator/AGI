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

## §0 State (10-12 04:3xZ) — IDLE, owner order: "We're about outta usage ... everyone goes into idle for a clean resume in a few days"
| | |
|---|---|
| post | director-general-4 under sanctuary-master (SM); builder for DG1/SM; DG2 writes my falsifier lanes first, DG3 is the other builder |
| running | NOTHING: no suite, no runner, no dispatch, no build, no review. Do NOT box belam until the owner resumes us (SM 04:3xZ); no reply to SM needed |
| skills | agi-rotate · agi-send · agi-verify · agi-goal · agi-post (+ agi-review / agi-dispatch only if SM dispatches) |
| worktrees | /var/lib/agi/director-general-4/: t (mine, detached = posts/director-general-4) + LIVE locked: w-boardlog (dg4-boardlog 63b21a5b90) · w-pins (dg4-pins 5b6e7b00cb) · w-ownrow (d37799e298) · w-fixrunner (3deb115c1e) · w-capsule3 (23924e296f) · w-board3 (7a96f67619). SUPERSEDED, safe to `git worktree remove <path>` BY PATH: w-board2 (dbbfb2e2a6), w-capsule (a0a86ef159), w-capsule2 (c0bb3f05ef). Every dg4-* branch is kept |
| scratch | pytest --basetemp, TMPDIR, lane temp, gate trees: ONLY /data/work/gate-director-general-4 (700, my uid); home and /tmp are on the ROOT disk. One heavy lane at a time, niced, only above 3 GiB MemAvailable |

## §1 Plan (nothing in flight)
```
WAIT    SM's stack 13 (gate tree g397): my board_job log commit 63b21a5b90 (every line UTC-stamped incl. the writer's; [raced] names old -> seen sha12) with DG5 7970370e55 + DG2 e52540c669; and DG3's i10 fix.
        My pin commits 1ecd97928f (.13 C1/C7 + N7) + 4f1009ca58 (N7 = `in` is a TRANSPORT writer) + 5b6e7b00cb (capsule.t.sh GRID=TRANSPORT g4a/g4b) are in posts/sanctuary-master, council-approved 04:05Z, riding L12.
NEXT    (on SM's word only, never invented) box-move.sh becomes the CALLER of `sect capsule | sh -s -- pack|out|verify|in` (council ruling 01:56Z: design section 6 replaces box-move.sh :32-:45; NOT a capsule verb; the piece keeps its 8,192 bar).
        GATE on that caller (council 04:05Z, my deferred (c) accepted): the PRE-STOP scratch on the target holds MAIN's refs/grid as a MIRROR (not a plain clone), so the dry `in`'s own CAS ancestor check is row 5c: a non-ff refs/grid line -> PRE-STOP rc 6, the post still on FROM. 0 piece bytes.
EXTRAS  on SM's word (not placed): geometry_config.resolved_seat_env v4-rows-only; cc-session-start.sh BOOTSTRAP_SEAT=${AGI_POST:-${AGI_SEAT:-}}; skills-truth CUT/TIP defaults. HELD: .20 retire-the-inbox-write; .20.1 items 2+3. NOT MINE: box-wake.t.sh (DG2).
```

## §2 Landed / boxed (one line each; DG1 judges, SM gates and lands)
```
ON THE TRUNK b71fbe86d5 (checked 04:3xZ)  .42 E + its fix-forwards (b1d83acb51, eb944f41c9, ae0237b3d3 renderer, a5c53f47d1 the .42.1 leaf cap/mkdir/sudo-pending, 7a96f67619 commands.md caps) · .44.1-.6 capsule (c0bb3f05ef in L7; FF1 4755041c5b + FF2 23924e296f: behind-base refs ride as ref lines, thin bundle, ONE update-ref transaction; engine-sizes b7) · 3deb115c1e runner-uid pin · d37799e298 own-block row.
        earlier: .36 tui · .20 v5 alert · .37 · fresh-blob · .13.2 · .35 · kid AGI_POST=$k
NOT YET ON THE TRUNK  1ecd97928f 4f1009ca58 5b6e7b00cb (SM's branch, L12) · 63b21a5b90 (stack 13)
```

## 🔴 Where it stops
```
Idle by the owner's order. Nothing is mid-step; no lane, runner or gate slot is held.
FIRST ACT on resume: read mail ONCE, whole: AGI_POST=director-general-4 box read | fold -s -w 200  (messages are also commits: git log -1 --format=%B <tip of refs/box/<sender>/director-general-4>).
THEN: wait for SM's word. A RETURN on a cut = ONE new signed commit ON the sent sha in the matching worktree (never a rebase, F26/F14), commit with plain `git commit` there (a worktree on a dg4-* branch signs: commit.gpgsign) and `agi-at <path>` ONLY in ~/t (the card, a node).
Capsule lane: env -u AGI_TRUNK -u AGI_POST sh extensions/agi/tests/capsule.t.sh (66 ok); landing mode: LANDING_REPO=<repo> LAND_TRUNK=<ref> CAPSULE_FLOOR=<n> sh capsule.t.sh.
```

## §4 Traps (this generation's only; at the next rotation each moves to the skill that owns its flow)
| trap | rule |
|---|---|
| bare prune | NEVER `git worktree prune` on MAIN's shared .git: it drops every entry whose path my uid cannot stat = every other post's 700 gate dir. Remove my OWN tree by path; lock a long-lived one (`git worktree add --lock`) |
| runner fall-through | a background lane runner that waits on MemAvailable must STOP, not run anyway, when the wait ends |
| pkill -f | matches my own command line and kills the shell: find the pid with `pgrep -x sh -a`, kill by pid |
| mail (owner 10-11) | NEVER box belam; to SM one message per finished thing, no [ack]/[thanks]/[landed]; only [red] or a BLOCKING owner-ruling ask at once |
| the sha in a box message | `git rev-parse HEAD` FIRST, then compose the heredoc with it inline (I sent two [cut]s with "the sha is below" and no sha) |
| home literals | belam's guard knows EVERY seat's home: grep the added lines AND the message for /var/lib/agi/<name>, /home/, /data/home (anonymize.HOME_PATH_RE itself, in python; allowed_signers is not a home); a crons row writes `~/...` |
| new CLI verb | a subparser added to a bin needs a commands.md entry (manifest: or excluded: + reason): run test_commands_manifest.py (4m48s) before sending |
| scanned sites | a new engine piece/bin line with update-ref / commit-tree / mktree / hash-object -w / fetch moves test_grid_writers C1/C7 (goal:g7.16.1.11.13 pins): run it before sending; re-cut the blocks with the test's own norm/run, classify each site in a row |
| ambient uid | a test must pin its runner (monkeypatch crons._invoking_user), never assert on the uid running pytest (belam's slab A/B found it) |
| capsule lane | env -u AGI_TRUNK first; a shell function's last command is its status (a trailing rm made a mutant row pass) |
| committer email | git verifies an ssh signature against the COMMITTER EMAIL: a machine job signing as the seat commits as `belam <belam@agi>`, never `agi-belam` |

## §5 Verification
Last green (bare env -i, niced, one at a time): test_board_job 29 · test_crons_job_user 20 · test_crons 103 · test_crons_apply_cell 19 · test_crons_log_cap_declared_scope 17 · test_grid_writers 27 · test_thought_hygiene 17 · test_bin_help_smoke 76 · test_commands_manifest 182 · capsule.t.sh 66 ok / 0 FAIL · engine-sizes 0 FAIL (engine-capsule.md fenced 8,117 B = 75 B under its bar) · graph-metrics / metrics-cell / mail-alert-retired 0 FAIL.

## §6 BANKED
- `capsule move` is box-move.sh's caller work, not a verb (council 01:56Z); its gate (c) is above. `list` selector stays (SM: do not cut).
- RESIDUES named, not fixed: a cron row's custom `log:` outside `~/logs/` is neither capped nor mkdir'd; `in` transports refs/grid verbatim when a packer passes `--ref 'refs/grid/*'` (council 03:25Z (b), ruled, not a refusal).
- UNEXPLAINED: belam's first live `apply --sudo` (00:32Z) printed `pending` for both foreign users although their crontabs read back == desired; my reproduction (a stateful fake `sudo crontab -u`) showed the old path installs NOTHING for a user with no crontab, so something else installed them. Fixed the path (a5c53f47d1); the mystery is SM's/belam's to look at.
- SM banked with belam: a machine identity in the box ring (heal / memory-alarm senders), the owner's call for S3.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
