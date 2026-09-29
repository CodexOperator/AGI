---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-S2-L5-XV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 15, resumed after the 04:50Z 09-29 reboot: the reboot wiped /tmp and every PASS tool with it. Rebuilt from transcript 76166d75 (the PASS 10 dump, 09-27 01:32Z) + 9c691d8d (B1's SAMPLE/MUST patch); the rebuilt build.py reproduced B2's 12-round set exactly. Moved DURABLE (/data/home-belam/passB2 + /data/home-belam/prime-merge-tools/trunk-sync): the near miss is rebuilding into /tmp again, which satisfies the skill's path and loses the tooling at the next reboot. resolve.py re-authored to its recorded rule (trunk rows + season2/main director model cells; refuse on a differing pubkey or row set); the 09:00Z conflict was 3 director rows whose trunk side is the newer crash-respawn (gen 46/35/34), pubkeys + model cells equal -> tree delta 0. Run tag pb2b so the relaunch never reads the dead 01:44-03:59Z pb2 runs.
<!-- THOUGHT:END -->

## §0 State (09:1xZ 09-29)
| | |
|---|---|
| post | belam-S2-L5-XV gen 15 · woke 22:1xZ 09-28 · killed 04:48Z (oomd), --resume'd by the owner 08:4xZ 09-29 · Opus 5.5 (1M) · delegated authority |
| box | local-town · MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `/mnt/agi-flash/worktrees/prime-root` · reboot 04:50Z (§6) · TM/DT/DE crash-respawned 08:55Z (704ee55c9, gens 34/35/46) · stream DOWN (HELD) |
| DISK | `/` 63 GB free (the reboot emptied /tmp) · **`/data` 34.6 GB free 08:50Z** (54 at 22:3xZ): 1040 worktrees + .agi/sessions 24.6 GB (340 iter-*) -> [red] to DE 09:1xZ · flash 114 GB |
| moved | ~/logs, ~/.cache/{uv,pip}, 41 closed project dirs -> /data/home-belam/* · TMPDIR=/data/tmp (systemd --user env still set after the reboot) · prime-root -> flash |
| merge | **PASS B2 RELAUNCHED 09:01Z** (restart stamped 08:59:29Z; try 1 held 03:59Z, lane dead): BASE ed34f49532 · TIP 922ff3f48 (sync #2: origin fed5f06449) · 12 rounds (5 hyp SAMPLED + 7 engine-delta), tag pb2b · RED clean: 0 D · 0 secret hits / 24,228 added lines · 0 broken |
| crons | CHECK da6f2ed6 "13 */4 * * *" came back with the --resume (CronList 08:5xZ); a FRESH process must re-arm it |
| spend | credits 0.606 USD -> SAMPLED on --harness pi-free (the lane was back by 04:34Z: DE's mur-eg reviews landed) |

## §1 Plan
```
now    PASS B2 (🔴 P): chunks -> verdicts -> step 5 in prime-root -> residues leaf goal -> state + board note -> [merge-up] to TM -> owner
next   CHECK 12:13Z · skill agi-merge-pass §3: tooling path /tmp -> /data/home-belam/passN (after the PASS closes)
owed   M3b ~/.pi -> /data/home-belam/pi when NO pi runs · M4b live seats' ~/.claude/projects dirs after they rotate
owed   FACTS WINDOW on TM's ping (🔴 F) · TM (a) counting rule -> skills/agi-merge-pass 4 · town note grant lines (🔴 G)
HELD   OWNER 21:1xZ 09-27: stream · encryption-town config · sanctuary-master activation -- until messaging is done
```

## §2 Landed (gen 15): 6e31f798a re-link · 8f891b8cd path move · 0628fb4af sync #1 · 599cf3b07 rotations clause · e26fbabea card (held) · 922ff3f48 sync #2

## 🔴 Where it stops
09:1xZ 09-29 belam-S2-L5-XV: PASS B2 relaunched after the reboot (tag pb2b, durable tooling on /data); watch the chunks, then verdicts
```
P. PASS B2: D=/data/home-belam/passB2 · `tail $D/events.log` · `python3 $D/verdicts.py | grep ATTN` · Monitor: `bash $D/monitor.sh` (re-arm on expiry).
   All 6 chunk exits -> MISSING rounds: `setsid nohup bash $D/reretry.sh &` (paced, one at a time). Verdicts -> step 5 in prime-root (flash):
   pull --ff-only · merge-tree preview · merge --no-ff $(cat $D/TIP) · commands.py run verify · push season2/main · ff local-maxxing/main · grid.py commit --all.
   Trunk sync next time: /data/home-belam/prime-merge-tools/trunk-sync/{sync.sh,resolve.py,target,msg}. Transcript dump = recovered/ (same dir).
D. /data: < 10 GB free -> no PASS launch. [red] to DE 09:1xZ: prune finished rounds' trees (1040 worktrees, 340 iter-* dirs); never delete another post's tree.
M3b. ~/.pi (935 MB): ONLY while no `pi` comm runs: cp -a to /data/home-belam/pi, mv ~/.pi ~/.pi.old-on-root, ln -s, smoke, rm the old.
M4b. live seats' project dirs: after each seat rotates; `ln -s --` (names start with '-').
F. FACTS WINDOW -- PREP DONE: branch belam/facts-window @ a1ccc2dee (worktree .agi/worktrees/belam-facts). When TM pings with the chain tip, in ONE window land a1ccc2dee with it, then: F13 line -> 'Spend by hand, from any worktree:' · cell templates.director.startup.facts_pointer_target_bytes = 2000 · RE-MEASURE the 2009 B region · config:posts:102 + goal:g4.18.2:34 drop the DEFAULT_CC_ROLES ultracode residue ONLY once EG.5 removes it from rotate.py:120.
G. TOWN NOTE GRANT (TM option a): DE builds a verb-scoped actor_rows note grant (goal:g7.33 round); at landing add ONE [town] schema grant line per post (DE, TM, DT) and drop the interim clause from agi-dispatch 5.
R. RENAME B LATER (owner): hostnamectl + guard.env _belam_gpu -> _local_town + /etc/hosts + guard-init --status, ONE window. NEVER a bare `systemctl --user import-environment`.
5. RAM + per-role roots (owner 06:2xZ, DH.499): kids tmpfs · DE + parents /data · belam + TM /mnt/agi-flash · tmpfs GO = TMM.313.
```
## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 24 | the trunk push is thought-master's alone | belam pushes only `season2/main` + `local-maxxing/main` |
| 28 | after a reboot the seat row keeps the dead pid | `rotate._successor_row_write(...)`, commit posts.md by exact path |
| 40 | F13's home-path .env does not exist here | the MAIN .env is `/data/work/agi/.env` |
| 43 | `send.py read` shows EMPTY while blocks sit in `.agi/sessions/inbox/belam.md` | read the inbox FILE by ts at every CHECK |
| 44 | `write.py create goal` without origin/seeds/heading_level is skipped by the render | set origin goals-doc, seeds [], heading_level 3 |
| 45 | `du`/`find` over `.agi/worktrees` or `/tmp` is an io storm; `du --max-depth=1 .agi/sessions` > 120 s | `git worktree list`; `find -maxdepth 1` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 47 | a seat key row can carry a pubkey whose seed was never written | prove by sign+verify before any re-key |
| 48 | `~/.claude/projects/*` names start with '-': `ln`/`du` read them as options | always `--` or a `./` prefix |
| 49 | a systemd `append:` log holder keeps its fd across a move | restart the unit after the symlink swap |
| 50 | a reboot empties /tmp (PASS tooling lost 04:50Z 09-29) | tooling lives on /data/home-belam only; copy the previous pass dir |
| 51 | watchdog "test binary ... returned 2 = 'No such file or directory'" | = sanctuary-health EXIT 2 (PSI full avg60 >= 40%), rendered as errno 2; the binary exists |
| 52 | after a --resume, `send.py read belam` refuses ("you are 'unknown'") | always `--from belam` |

## §5 Verification: `links.py links` 0 broken (09:0xZ) · `snapshot-goals.py --render --check` · `df -B1M / /data` · `tail ~/logs/memory-alarm-alerts.log | cut -d" " -f1,3-`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| REBOOT 04:50Z 09-29: systemd-oomd (user@1000: 50% memory PRESSURE for 20 s) made 67 kills in that boot -- reaper, alarms, sanctuary-watch, remote-control (8.5 MB), DE's timers -- the units with the most reclaim, never the load; then sanctuary-health failed its PSI-full >= 40% test past retry-timeout 300 s and the watchdog rebooted BY DESIGN | (a) keep both guards (recommended: the reboot is the designed repair of a wedge) · (b) exempt seat infrastructure (remote-control, reaper, alarms) from oomd -- root config · (c) cap the load: DE's parallel murs + kids (some worktrees on /dev/shm = RAM, 03:15Z) preceded every crit -- unmeasured |
| docker data-root still on / (owner: -> /data or flash when models are redownloaded) | a stop-the-daemon window; owner's word |
| DISK LATENCY: sda (USB SSD, dm-crypt, / + /data) ~35 ms/op | `sudo smartctl -a /dev/sda` · `sudo dmesg -T` for usb/reset |
| seat rows in config:posts still claude-opus-5 (adv-*, masters) | move on the owner's word |
| origin remote moved (every push prints it) | `git remote set-url origin <new>` |
