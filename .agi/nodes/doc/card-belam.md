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
thought_session: belam-S2-L5-XVIII
title: "doc:card-belam -- the Prime's card: the one scratch (state · plan · landed · where it stops · traps · verification · BANKED)"
town: core
---
# doc:card-belam — the Prime's card (local-town): the ONE scratch

Owner 09-23: the card is the handoff scratch space and a doc node — `HANDOFF.md` and `.agi/sessions/quorum/belam.md` are symlinks to this file. Role = the Prime template (`build:briefs-prime-director-successor`) + the HEAD (`doc:unified-head`). Replaced whole; ≤ 100 lines; rules live in skills + role docs, never here; progress lives on the town board.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 21 closes the first act gen 20 handed on. SM asked for a hold until its [accept] on d82a63e5a, OR an empty diff between HEAD's --dry-run plan and d82a63e5a^'s. The plans diffed empty (only a live reading and the script path differed), so the apply went ahead without waiting. The post scopes stay in app.slice: moving 7.9G of posts into agi.slice's 9814M would starve the rounds, and P6's slice was the owner's go.
<!-- THOUGHT:END -->

## §0 State (05:4xZ 09-30, read from date -u)
| | |
|---|---|
| post | belam-S2-L5-XX gen 21, session **agi-23**; predecessor gen 20 = agi-79 (idle, no crons) |
| run | owner 04:58Z: "Continue hammering at it as fast as you can until 7am" -> every post RESUMED to **11:00Z** (7am ET); owner 04:59Z: "I need to max sub use before reset in an hour" -> Opus subagents allowed until the ~06:0xZ reset, then the brief's SUBAGENTS row (Sonnet 5.5) applies again |
| posts | SM agi-5c · alive agi-e3 · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b · **DG6 agi-bb (NEW 05:02Z, Opus, on goal:g1.31)** · stream-master agi-8c (stream OFF) — names change at every rotation: ListAgents + tmux window names |
| lanes | coordination -> SM · rulings + mid-work questions -> the council · never the Prime (director brief messages row) |
| crons | session-only: CHECK d087a76c "13 */4 * * *" · STOP aceed7d4 11:02Z · Monitor b8xm4v8wi (memory, 30 min, re-arm) (stop the council + directors, stream-master stays, owner report). CronList FIRST at wake (skill agi-rotate §3) |
| box | engine slice GUARD_ENGINE_MAX_local_town=3G (stopgap; real fix = goal:g7.16.1.5.5, DG5) · heal restarted 05:06:37Z onto ff09c6101 (SM's 1 h proof: no reaper oom-kill) · user@ cache pins memory.high under fan-out: relief = `echo 1500M > <post scope>/memory.reclaim` on the biggest file-heavy scope (freed 3.6 GiB 05:0xZ, nothing killed) |

## §1 Plan
```
DONE gen 21  quorum card re-linked f07838011 · keysync 8c391237d already landed f3c31278e (SM's red closed) · crons re-armed
             guard-init APPLIED 05:37Z after an EMPTY plan diff HEAD vs d82a63e5a^: agi-work 8371/9302 -> 6067/6742M · engine file 384/512 -> 2304/3072M · ramdisk.slice max 7168M
             RULED: the 16 agi-post-* scopes (7.9G) stay in app.slice under user@ high 13319M; a per-post high cell = goal:g7.16.1.5.5 (SM boards)
             reclaim 1000M on the SM scope: user@ 13290 -> 12165M, nothing killed
DONE gen 20  PASS B3 closed (13c3a3e8c) · residues goal:g1.31 · DG6 stood up · Prime template §1 + director brief
NEXT         the watch only: answer posts, keep memory breathing, fire the 11:00Z STOP, owner report · DG5 owes the ramdisk proof (baseline 05:40Z: ramdisk shmem 578M · engine 801M · work 281M)
NOT THE PRIME'S  B4 = goal:g7.16.1.10 (council: merge-up reviews off the Prime; DG1 sketches) · .5.5 RAM budget (DG5) · workflow.py headless claude-code route (SM board)
```

## §2 Landed (gen 21 · gen 20)
f07838011 · guard-init apply (box, no commit) || gen 20: 3b91e6c1a d04c7f9e2 4627581e7 5e47d781e 8ad1590a3 9de4f1fff 14a6f32b4 13c3a3e8c(season2/main) db69d66f9 e4475bcb9 eb7f30a64 af41ea678 73a89bb4b · write.py self-commits

## 🔴 Where it stops
Watch to 11:00Z: the STOP cron aceed7d4 fires the stop, then the owner report. No Prime act is open; the ramdisk proof is DG5's
```
at 11:00Z   SendMessage each council/director post "stop: finish the step, card whole, idle" (stream-master stays) -> card -> owner report <= 6 lines
memory      Monitor on user@ >= 12.8 GiB / PSI full avg60 >= 20%, edge-triggered 10 min (re-arm at wake + at each 30-min expiry); relief = memory.reclaim on the biggest file-heavy post scope, never a kill
asks        heal restarts on a clean SM verdict: git merge-base --is-ancestor <sha> HEAD · heal.py dirty = comments only? · heal_sweep green (retry while "suite window refused") · systemctl --user restart agi-agi-reaper-3fbc6951.service
```

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 15 | a retire+move shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 45 | `du`/`find` over `.agi/worktrees` is an io storm; a glob into `.agi/` hands du the bind-mounted worktrees | `git worktree list`; never glob into `.agi/` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 57 | write.py lands UNCOMMITTED while verify-suite.lock is held | wait for the lock, then commit by exact path (`git add` a new file first) |
| 61 | `workflow.py --harness claude-code` runs NOTHING headless | `<home>/passB3/ccrun.py` (CC_MODEL, default Sonnet 5.5) |
| 63 | a gate that greps pytest's LAST line reads tier-gate noise or the suite-lock refusal as red | grep `(passed|failed|errors?) in`; retry on "suite window refused" |
| 64 | RAM MAIN: tmpfs pages are charged to the FIRST writer's slice and stay there | heal's writes land on agi-engine.slice as shmem; the budget line is goal:g7.16.1.5.5 |
| 65 | `rm -rf $VAR/$X` is refused by the safety check | literal absolute paths, or `"${S:?}"/"${d:?}"` |

## §5 Verification
guard-init 05:37Z: --status ok for agi-engine 3072M · agi-work 6742M · ramdisk 7168M · SM's Opus audit of d82a63e5a: 18 defaults == the old literals, plan identical (residue to DG4: validate cells before bash arithmetic; never `sudo -E`)
B3 merge verify on the RAM disk: 11/12 (bin-suite-fresh known) · links 0 · 5201 nodes · grid 165 versions / 0 errors · s-goal move: 0 hypotheses under s18/s31/s32/s34, links 5317/0 · DG4 cold homing falsifier: 5 homed, shmem +0M, tmpfs +1M

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| `*.pre-tier-*` backups: ~/.claude.pre-tier-20260930T0145Z + ~/.pi.pre-tier-20260930T0146Z (on /) | delete after a day of clean tiering |
| an on-disk /tmp makes every boot wait 5+ min in systemd-tmpfiles | tmpfs /tmp or a /tmp age cleaner, owner's call |
| belam row says opus-5-5 / high; the live Prime runs opus-5-5[1m] / max | owner sets the row |
| docker data-root still on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
