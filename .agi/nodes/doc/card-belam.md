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
thought_session: belam-S2-L5-XIV
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 14 card: PASS 12 closed, series B next. Landed history moved to the board note + commit log (owner 06:4xZ 09-28: the board carries progress so cards stay trim) -- §2 keeps only this gen's one-liners.
<!-- THOUGHT:END -->

## §0 State (07:0xZ 09-28)
| | |
|---|---|
| post | belam-S2-L5-XIV gen 14 · woke 03:5xZ 09-28 · Opus 5.5 · owner ASLEEP from 06:5xZ (delegated authority) |
| box | local-town: MAIN `/data/work/agi` on `local-maxxing/season2/main` · prime-root `.agi/worktrees/prime-root` · stream DOWN (HELD) |
| disks | `/` 93% (6.6G) + `/data` = ONE USB SSD (LVM) · `/mnt/agi-flash` SanDisk ext4 112G, own io queue · nvme BROKEN (owner) |
| merge | **PASS 12 CLOSED 06:5xZ**: season2/main 774e0b912 · local-maxxing/main -> 72d8d565c · next BASE = 72d8d565ce · residues goal:g1.28 |
| crons | CHECK **372dc32f** "13 */4 * * *" (session-only: re-arm at wake; the 08:13Z fire never came -- ran by hand 08:4xZ) · PASS B1 one-shot **f3ff3dd0** "47 13 28 9 *" (notice to TM 08:4xZ; state notice_sent_at + run_at set; procedure = crons.md section 2) |
| spend | pi-free 0 USD this pass; paid paths closed (56c1156ab) |
| models | claude-code kid + parent = claude-opus-5-5 (44925a6b6, 288513229) · harnesses.claude-code.max_live 4 · seat rows unchanged |
| memory | crit/warn every ~30-60 min 02:01-05:50Z (PSI full peak 25.9%, each cleared < 3 min); 4 idle predecessor belam sessions (X-XIII) still alive -- §6 |

## §1 Plan
```
done   PASS 12 steps 0-8 · owner orders: models (kid+parent opus 5.5, max_live 4) · board rule (39b942824) · DH.499 per-role roots note (968d19ca1) · g7.32.6 nudge-loss measurement (321a99b29) · redesign order to DE (g4.18.1 -> g7.32.6 -> g7.31.3.3)
done   clean prune 08:35Z: 144 removed, 154 dirty kept, /data +13.2 GB (board b1aba8033) · TM [red] 06:3xZ town-note grant: option (a) accepted, skill row interim (abf58770f)
now    PASS B1 IN FLIGHT 13:48Z: TIP pinned ed34f49532, BASE 72d8d565ce, /tmp/belam-passB1 (monitor.sh = the ONE Monitor), 8 rounds / 4 chunks CAP 3, SAMPLED (credits 0.606 < 4: engine-delta x3 + 5 hyp incl. the p2 re-check; 6 unsampled in plan.json) -> 14:4xZ: 5 of 8 rounds have verdicts (all accept_with_residue, RED gate CLEAR: 0 node deletions, keyword hits = negations, 0 secrets / 18,662 added lines); 3 incomplete (p2 re-check verify, engine-delta-1 verify, engine-delta-2) because the free provider returns EMPTY responses since 14:40Z -> /tmp/belam-passB1/reretry.sh retries them every 20 min x6, stops an attempt on the first empty death -> then verdicts.py -v -> step 5 in prime-root (tag pb1chunk, /tmp/belam-passB1, BASE 72d8d565ce; carries EG.1 57debf3a2 + re-checks the p2 demote)
HELD   OWNER 21:1xZ 09-27: stream · encryption-town config · sanctuary-master activation -- until messaging is done
```

## §2 Landed (gen 14): b065c922c wake re-link · 44925a6b6 + 288513229 opus 5.5 kids/parents · 968d19ca1 DH.499 owner note · 321a99b29 g7.32.6 · 39b942824 skills board row · 3e356eb7f goal:g1.28 + 6 hypotheses · 774e0b912 PASS 12 merge (prime-root, pushed) · f91ae15f5 board note · b1aba8033 prune board · abf58770f board-row interim · a577c160a ladder roles[5] pi-free (TM option A) -- FACTS WINDOW owed on TM ping: F13 trim + cell facts_pointer_target_bytes 2000 + re-measure 2009 B + fix config:posts:102 and goal:g4.18.2:34 once EG.5 removes ultracode

## 🔴 Where it stops
13:5xZ 09-28 belam-S2-L5-XIV: PASS B1 in flight (/tmp/belam-passB1, TIP ed34f49532); verdicts + merge next
```
P. PRUNE DONE 08:35Z (board b1aba8033). The 154 dirty kid trees are DE's sweep (agi-dispatch 5 "worktree sweep"), never --force.
B. PASS B1 NOTICED 08:4xZ, fires 13:47Z (one-shot f3ff3dd0; if this session is gone, the successor runs it under CHECK case (d)): rebuild tooling from /tmp/belam-pass12 into /tmp/belam-passB1 (BASE 72d8d565ce, tag pb1 in build.py / launch.sh / monitor.sh TAG= / retry.sh PASS_TAG / verdicts.py glob). monitor.sh TAG was stale p10 in PASS 12 -- grep every tag after copying.
R. RENAME B LATER (owner): hostnamectl + guard.env _belam_gpu -> _local_town + /etc/hosts + guard-init --status, ONE window. NEVER a bare `systemctl --user import-environment`.
5. RAM + per-role worktree roots (owner 06:2xZ, on DH.499): kids tmpfs · DE + parents /data · belam + TM /mnt/agi-flash · mount check before any write · flash worktrees locked. tmpfs GO = TMM.313 (EG.9 sweep chain merged + 24 h no memory crit): then (a) guard.env GUARD_WORKTREE_TMPFS_belam_gpu=4G (backup) (b) sudo guard-init.sh + --status (c) set the cells after (b) is green (d) prove one kid there.
6. OWED: re-add the agi-corrective clause when build:skills-agi-corrective-SKILL.md reaches the trunk; F13 'Spend by hand, from any worktree:' after DH.501 merges up; `skills` first_turn entry from DE's doc:draft-skills-first-turn.
```
## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 3 | the grid cron versions an UNCOMMITTED node within minutes | a fresh node is retired + moved, never deleted |
| 13 | the stream is LIVE (when up) | never print a secret, key, address or host name |
| 15 | a retire+move with a changed body shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 24 | the trunk push is thought-master's alone | belam pushes only `season2/main` + `local-maxxing/main` |
| 28 | after a reboot the seat row keeps the dead pid | `rotate._successor_row_write(...)`, commit posts.md by exact path |
| 30 | after a reboot heal re-spawns SOME seats | `reseat.py` from MAIN |
| 40 | F13's home-path .env does not exist here | the MAIN .env is `/data/work/agi/.env` |
| 42 | `replace body N:M` refuses a range with no blank line around it | `--force` rides the SOURCE arg, after asserting the range |
| 43 | a send lands `pending=0` when parents dm at the same time: no nudge, `wake` says nothing-pending (g7.32.6) | check the addressee's inbox for a `# read up to here` after your block; its own file watcher usually catches it |
| 44 | `write.py create goal` without origin/seeds/heading_level is skipped by the render | set origin goals-doc, seeds [], heading_level 3 (as g1.27) |
| 45 | `du`/`find` over `.agi/worktrees` (660+ trees) is an io storm | never; count with `git worktree list` |

## §5 Verification: `links.py links` 0 broken · `snapshot-goals.py --render --check` · `commands.py run verify` (bin-suite-fresh FAIL known) · `~/work/.sanctuary/guard/guard-init.sh --status` + `tail ~/logs/memory-alarm-alerts.log | cut -d" " -f1,3-`

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| 4 idle predecessor belam sessions (L5-X, XI, XII, XIII: claude --remote-control) still alive, holding RAM while memory crits recur | reap them (owner chain rule: on the owner's word) |
| memory crits recur (PSI full > 20% ~hourly 02-06Z 09-28) | middle ground GUARD_DOCKER_BUDGET_belam_gpu=2048M, or seats into user@ via `systemd-run --user --scope` -- the owner's guard |
| seat rows in config:posts still claude-opus-5 (adv-*, masters) | move on the owner's word (dispatched parents already 5.5) |
| guard follow-ups (TM 09-26): model rounds vs user@ high; guard-init 'last alerts' path | model loads in own scope MemoryMax ~6G; repoint to ~/logs/memory-alarm-alerts.log |
| origin remote moved (every push prints it) | `git remote set-url origin <new>` -- the owner's call |
| engine-wide config/template maxxing pass (owner idea 09-23) | opening it is the owner's call |
| DISK LATENCY 07:0xZ 09-28: io PSI some avg60 83-90 with the runaways gone; sda (USB SSD, dm-crypt, / + /data) 57% busy at ~16 ops/s = ~35 ms per op; jbd2 + dmcrypt_write + flush kworkers in D; systemd-tmpfiles in D 2h49m (/tmp is on /); dmesg shows no reset/error to belam | `sudo smartctl -a /dev/sda` + `sudo dmesg -T \| grep -iE "usb\|sda\|reset"` + check the USB port/cable/heat; `du -sh /tmp` as root. The prune waits on io60 < 40 |
