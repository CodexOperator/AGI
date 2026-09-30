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
gen 20 rewrites the card whole ahead of its rotation (meter 0.41). The Prime's post changed shape today on the owner's word: directors coordinate through sanctuary-master and take rulings to the council ("the council IS prime to everyone else", 02:54Z); merge-up chunk reviews leave the Prime for the council or automation ("so you can keep the most zoomed out view", 04:50Z). So the successor inherits no PASS, only the watch until 11:00Z. Owner stamps are read from the transcript, never recalled (the HEAD's FORM rule, after alive's finding).
<!-- THOUGHT:END -->

## §0 State (05:2xZ 09-30, read from date -u)
| | |
|---|---|
| post | belam-S2-L5-XX gen 20, session **agi-79**; predecessor gen 19 = agi-c2 (idle, crons deleted) |
| run | owner 04:58Z: "Continue hammering at it as fast as you can until 7am" -> every post RESUMED to **11:00Z** (7am ET); owner 04:59Z: "I need to max sub use before reset in an hour" -> Opus subagents allowed until the ~06:0xZ reset, then the brief's SUBAGENTS row (Sonnet 5.5) applies again |
| posts | SM agi-5c · alive agi-e3 · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b · **DG6 agi-bb (NEW 05:02Z, Opus, on goal:g1.31)** · stream-master agi-8c (stream OFF) — names change at every rotation: ListAgents + tmux window names |
| lanes | coordination -> SM · rulings + mid-work questions -> the council · never the Prime (director brief messages row) |
| crons | session-only: CHECK 9593181d "13 */4 * * *" · STOP e8dae945 11:00Z (stop the council + directors, stream-master stays, owner report). CronList FIRST at wake (skill agi-rotate §3) |
| box | engine slice GUARD_ENGINE_MAX_local_town=3G (stopgap; real fix = goal:g7.16.1.5.5, DG5) · heal restarted 05:06:37Z onto ff09c6101 (SM's 1 h proof: no reaper oom-kill) · user@ cache pins memory.high under fan-out: relief = `echo 1500M > <post scope>/memory.reclaim` on the biggest file-heavy scope (freed 3.6 GiB 05:0xZ, nothing killed) |

## §1 Plan
```
DONE gen 20  PASS B3 closed: merge 13c3a3e8c on season2/main · local-maxxing/main 578650193 · 40 rounds: 8 accept · 30 awr · 2 demote · 0 RED · residues goal:g1.31 (council laned it: DG3 3 · DG5 8 · DG6 19 · node 17)
             trunk synced db69d66f9 · engine slice 512M -> 3G (heal oom-kills) · DG4 cold homing + reclaim live · 9 hypotheses under retired s18/s31/s32 MOVED to g1.2 / g7.33.10.1 / g2.4.1
             s31 -> complete · goal:g6.51 minted then retired ("The regime doesn't need a goal") · DG6 stood up · Prime template §1 + director brief (lanes, SUBAGENTS) · HEAD FORM time rule
NEXT         the watch only: answer posts, keep memory breathing, fire the 11:00Z STOP, owner report
NOT THE PRIME'S  B4 = goal:g7.16.1.10 (council: merge-up reviews off the Prime; DG1 sketches) · .5.5 RAM budget (DG5) · workflow.py headless claude-code route (SM board)
```

## §2 Landed (gen 20)
3b91e6c1a d04c7f9e2 4627581e7 5e47d781e 8ad1590a3 9de4f1fff 14a6f32b4 13c3a3e8c(season2/main) db69d66f9 e4475bcb9 eb7f30a64 af41ea678 73a89bb4b · write.py self-commits

## 🔴 Where it stops
FIRST ACT (HARD RULE, handed on at f 0.42): SM's guard-init decision 05:2xZ -- DG5's ramdisk.slice (goal:g7.16.1.5.5.1, 786c1c13a + bea6448a1) accepted R1-R3: bash extensions/agi/guard/guard-init.sh --dry-run (expect 'would write' ramdisk.slice MemoryMax=7168M) -> sudo bash extensions/agi/guard/guard-init.sh (re-applies all 5 layers) -> --status shows ramdisk.slice AND agi-work.slice re-rendered from the cells (was 9302/8371 MiB vs 6742/6067) -> proof: a RAM dispatch raises ramdisk.slice shmem while engine + work stay flat. Then: 13 agi-post-* scopes are uncapped in app.slice (spawn.post_scope.slice = app.slice vs mem_cap's agi.slice default; goal:g6.41.1's lane) -> rule or place it. Then watch to 11:00Z: the STOP cron fires the stop, then the owner report
```
at 11:00Z   SendMessage each council/director post "stop: finish the step, card whole, idle" (stream-master stays) -> card -> owner report <= 6 lines
memory      Monitor on user@ >= 12.8 GiB / PSI full >= 20% (re-arm at wake); relief = memory.reclaim on the biggest file-heavy post scope, never a kill
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
B3 merge verify on the RAM disk: 11/12 (bin-suite-fresh known) · links 0 · 5201 nodes · grid 165 versions / 0 errors · s-goal move: 0 hypotheses under s18/s31/s32/s34, links 5317/0 · DG4 cold homing falsifier: 5 homed, shmem +0M, tmpfs +1M

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| `*.pre-tier-*` backups: ~/.claude.pre-tier-20260930T0145Z + ~/.pi.pre-tier-20260930T0146Z (on /) | delete after a day of clean tiering |
| an on-disk /tmp makes every boot wait 5+ min in systemd-tmpfiles | tmpfs /tmp or a /tmp age cleaner, owner's call |
| belam row says opus-5-5 / high; the live Prime runs opus-5-5[1m] / max | owner sets the row |
| docker data-root still on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
