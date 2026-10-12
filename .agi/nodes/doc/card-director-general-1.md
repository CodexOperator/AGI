---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
tags: []
title: Card director general 1
town: core
# doc:card-director-general-1 — director-general-1's card: the ONE scratch, replaced whole, <= 100 lines

## OVERALL GOAL (owner 10-08): finish encapsulation of grid slices (E1), belam on the new engine (E3, DONE), then the season rollover (E5). Progress is read ONLY on town:local-maxxing 'Engine rework trajectory' E1-E5. E2 (grid retirement) is MINE to cut; E4 (g1.41) moves by SM's landings.

## §0 State (10-12 ~04:4xZ, gen 26, IDLE again 07:4xZ (owner: usage resets Wednesday; keepalive disabled); encryption-town; trunk local-maxxing/season2/main tip 7693feb76b)
| | |
|---|---|
| post | director-general-1: a director, claude-code, engine v5 · parent SM (sanctuary-master) · ~/t is DETACHED at posts/director-general-1: NEVER `git checkout` in it · card edits: `agi-wt pull doc:card-director-general-1` + agi-turn + agi-flush (the pull dir vanishes after agi-turn: pull again for each edit) · a clone pushes a sha to MAIN with `git push /data/work/agi SHA:refs/heads/NAME` (a NEW name; next is dg1-close75; a `gc.pid.lock Permission denied` line after the push is harmless, check with `git ls-remote`) |
| mail | `AGI_POST=director-general-1 /opt/agi/bin/box read` (send: `box send POST < FILE`, from ~/t, plain text WITHOUT backslashes). **OWNER RULE 20:2xZ: NEVER box belam**; I box SM only, ONE message per finished thing, NO acks. A "mail: box read" typed into my pane is my own wake unit: read the mail |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it · DG2 falsifier lanes (re-cuts box-wake.t.sh) · DG3 builder · DG4 builder (.42 C1) · SM gates + lands (council 3/3 first) · belam = host acts, one GO each |
| SCRATCH | **/data/work/gate-director-general-1/wip**: t401 (the working clone, --shared, alternates = /data/work/agi), mail-sm-*.txt, home401 (HOME for `env -i` runs), pt (basetemp). Gate trees: `git worktree add --lock` then `git worktree unlock` + `remove --force`. Plain `rm -rf <absolute path>` |
| BOX RULES | NO scratch on /dev/shm; basetemp on DISK, `nice -n 10`, ONE heavy run at a time (SM's gate first); read the trunk through t401 (`git fetch -q /data/work/agi local-maxxing/season2/main`), never ~/t |

## §1 Plan
```
IDLE since SM 07:4xZ (owner: "Be back next week once usage resets on Wednesday"; keepalive timer disabled). No gate, land, dispatch, build, council round, box send (every mail wakes a post), CronCreate. Do NOT box belam. Session crons: none (CronList empty).
MY OPEN RED (owner: me): test_seat_alias_notice, 2 failures on the trunk since L6 (alarm_spool.py drain --seat had no SeatAction). FIX BUILT, TESTED, NOT SENT: 1c72fe952b (branch dg1-close74), ONE signed G commit on trunk a2bfba031c (L13 f632cd4854 landed), 3 files: alarm_spool.py (guarded `import geometry_config` with a plain-store fallback because /opt/agi/bin/alarm_spool.py is a single file with no engine beside it; `drain --seat --post` through geometry_config.SeatAction), test_seat_alias_notice.py (pin 21 -> 22), test_alarm_spool.py (standalone-copy row + bare-import mutant). Run at the sha: seat_alias_notice + alarm_spool + quiet_watch_spool 48 passed; grid_writers + bin_help_smoke + commands 134 passed 16 skipped.
 NOTE for SM: the two cron rows (crons.md drain --seat ...) and alarm-first-start.sh still say --seat, so each minute's cron log gets one 'note: --seat is deprecated' stderr line until they move to --post (follow-up: crons.md x2, commands.md argv, alarm-first-start.sh, test_quiet_watch_spool.py:123 pin; installing the cron change is belam's host act).
LANDED: B f7b86a1229, D 0800de802f, .40.1, .40.1.1, 20ada969d6. AT SM / taken: .11.11.1 CLOSE 54d30b48ad was in stack 13c (check the trunk: `git merge-base --is-ancestor 54d30b48ad <trunk>`; if not landed, re-cut on the live trunk).
NOT MINE (waiting on the resume): stack 14 (b522328480), stack 15 = DG5 .41 cut 2, DG5 verify-v5-uid l3-credentials red.
PARKED: .12 .15 .13 (DG2 runs the 17 aa3 lanes, I close .13) - .17 ACTIVE (belam's host acts).
```
HOST ACTS (belam, never mine): install alarm_spool.py to /opt/agi/bin, re-install agi-quiet-watch, crons.py apply (needs .42 C1 `user:`), then `sh extensions/agi/guard/alarm-first-start.sh`; render+install /etc/sysctl.d/60-agi-vm.conf, sysctl --system, sysctl-check.sh, 1 h before/after numbers into the .40.1.1 leaf; a cold-cache `walker-slab.sh` pass; box-move.sh after-check (DG2's file, SM places the call).
PARKED: .12 .15 .13 (DG2 runs the 17 aa3 lanes, I close .13) · .17 ACTIVE (its falsifier-1 misses: no ring file/ckpt block, agi-land not installed: belam's host acts).
```

## 🔴 Where it stops + the exact next command
IDLE, tree clean, the one thing in hand is the UNSENT fix 1c72fe952b. ON RESUME (owner back, SM says so): 1) `AGI_POST=director-general-1 /opt/agi/bin/box read`; 2) `cd /data/work/gate-director-general-1/wip/t401 && git fetch -q /data/work/agi local-maxxing/season2/main`: if the trunk tip moved and touched alarm_spool.py / test_alarm_spool.py / test_seat_alias_notice.py, re-cut on it (`git worktree add --lock --detach ../gNN <tip>`, cherry-pick -S 1c72fe952b, push a NEW name dg1-close75), else the sha stands; 3) box SM ONE message: the sha + the counts above + the --seat cron-log note. Never a host act; never `grid.py checkout`; never invent goals.

## §2 Landed this generation (mine, via SM)
close32..close51 (memguard stack, .32 condition + CLOSE, .40.1 start-time/append/log fixes, .20.2 cut 1) · close52 flap hold (571f300635) · close53..58 the .20.2 spool stack (alarm_spool.py, memory_alarm appends, alarm_drain rows, quiet-watch, memguard append, first-start) · close59..62 the slab chain · close63..64 box-mail lane + leaf · close65 the sweep · close66..68 sysctl remark, /proc/sys read, fill line · close69 .40.1 CLOSE re-cut · close70 thrash row + case map · close71 boxwake fingerprint · close72 memguard remarks · close73 .11.11.1 close · close74 seat-alias red fix (UNSENT). Judged by running: dg3-40b ACCEPT.

## §4 Traps (this generation only; the older ones moved to agi-verify / agi-send in d3521e286f)
| trap | rule |
|---|---|
| a node edit made via agi-wt/agi-turn on the posts branch | NEVER mailed as a sha for landing: it drags the whole post history (a key blob, 10-01) into the range, SM returns it. Re-cut the final blob as ONE commit on a worktree of the live trunk (blob equals its base there = clean), push dg1-closeNN |
| a hysteresis/hold row | the hover input must outlast the hold or only the band mutant shows: derive the mutant x row matrix by reasoning, then assert it |
| test_commands::test_a_bare_first_word_runs_a_declared_command | times out (180 s `agi links`) on the BARE trunk too: not a regression signal |
| a root unit/script that touches a seat's key or `box send` | r1 (test_quiet_watch_spool.py) RED: root only APPENDS to the seat's spool by runuser; the seat's drain row signs |
| a crons.md why_box/prose with a literal seat home path | belam's landing guard (anonymize.HOME_PATH_RE over added lines) refuses it: write the seat's ~/alarm.spool |
| a crons.md THOUGHT whose FIRST 84 chars change | goal:g7.16.1.11.13's pinned C4 line breaks test_grid_writers (7 red): re-cut that node's block or keep the first words |
| plain YAML with `: ` inside a cron cell | an unquoted scalar breaks the whole node: no colon-space in why_box |
| a spool append that opens the file and writes later | the drain renames+unlinks under it: re-check fstat(fd).st_ino vs stat(path) after the write, put the SAME id in again |
| prose in a file INSTALLED under /usr/local/sbin or /opt/agi/bin | alarm-first-start.sh r1 greps it, comments skipped: never the word pair box+send in a docstring or help string |
| a template word list (memguard code row) | the rendered code may not contain the word `box` even in a comment: reword |
| `echo x 1>/dev/null` style redirects after a numeric arg | `1>` eats the argument: write `... 1 >/dev/null` (the lane pilot got NR empty) |

## §5 Verification: every return RUN at the sender's sha (bare `env -i PATH=$PATH HOME=<home401>`, tree and basetemp on DISK, nice 10), TARGETED while a gate runs. At the tip e8b68385a1: alarm_spool 21 + memory_alarm + quiet_watch 8 + first_start 5 + boxkit_templates + probe + grid_writers 27 + flip_successors = 467. Slab chain: boxkit + sysctl_check 352, walker_slab 3. box-mail.t.sh solo `ROOT=$PWD sh extensions/agi/tests/box-mail.t.sh` (2m39s). Engine shell lanes: `ROOT=$PWD sh extensions/agi/tests/<name>.t.sh`; with a SHA arg: agi-out-states, agi-out-stale. Read-only measurement of a live tree is fine; a signal, a write under /etc or /usr/local, or a root act is not mine. HOME_PATH_RE: `git diff BASE HEAD | grep "^+" | grep -E "/var/lib/agi/[A-Za-z]|/home/[a-z]|/data/work/"` = 0 before every send.

## §6 BANKED (to SM's digest; none blocks a build)
- user@-only memory thrash is logged but not noticed (memory_alarm_posts owns the notice): option 'the user@ job notifies only while its sibling is ok'.
- A jittered backoff between CAS tries in the box piece (unsent 2.3 percent of racing sends): the box owner's, the piece is at its 2005-byte ceiling; T1/T2 triggers are SM's.
- The council's claim that agi-sync's parent box stamps ~/.trunk-boxed: UNVERIFIED (no such writer found); asked SM.
- Branches I created that cannot be deleted from this uid (leave): the dg1-* ones (close32..close65).
