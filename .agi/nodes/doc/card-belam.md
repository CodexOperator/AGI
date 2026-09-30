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
gen 21 ran the owner-ordered history scrub. Owner 06:3xZ-06:4xZ 09-30, verbatim: "Yeah we gotta scrub it. Time to pause grid crons and do the whole shebang." · "Yes include codex-town. And go now then restart when everything is verified" · "Go". Also owner 06:1xZ: "We should probably ease off expensive subagents now and just use strictly sonnet 5.5 ideally using our new headless CC review routes." and "We also will need to stand down director-general 5 and 6 to help conserve tokens as well ... 3,4 can continue as is and pick up whatever 5,6 don't finish after standing down". The rewrite ran on mirrors, never in place (filter-repo in place would reset --hard MAIN's uncommitted files); local refs moved by one asserted transaction and worktrees by per-path swaps, because a full git status over 682 worktrees did not finish in 15 min.
<!-- THOUGHT:END -->

## §0 State (08:0xZ 09-30, read from date -u)
| | |
|---|---|
| post | belam-S2-L5-XX gen 21, session **agi-23**; predecessors idle: gen 20 agi-79 · gen 19 agi-c2 |
| run | owner run to 11:00Z; Opus subagent window CLOSED (owner 06:1xZ: Sonnet 5.5 only, headless CC review route first) |
| posts | DG5 + DG6 DOWN (recover false, pid 0, windows closed; handover cards e4f52f044 / ce682865d, SHAs pre-scrub) · DG1-4, SM, alive, all-is-one, self-perpetuating, stream-master FROZEN for the scrub until "[rule] resume" |
| crons | session: CHECK d087a76c · STOP aceed7d4 11:02Z · memory Monitor (re-arm each 30 min). Box crontab: crons_live=false during the scrub (turn back on at resume) |
| scrub | /data/scrub (mode 700): RESUME.md = the step table + revert · backup-local.git · backup-origin(2).git · stripped/ (2 nsys files, also back on disk, gitignored) |

## §1 Plan
```
DONE gen 21  guard-init applied (empty plan diff) · post scopes ruled to app.slice · command:commands canonicalize (d7cb48e6a pre-scrub) · config:guard doc header
             config:census minted · skill agi-send name [ref] row · brief SUBAGENTS = Sonnet 5.5 strictly · DG5 + DG6 stood down
             HISTORY SCRUB: email (text + 7k author lines -> owner@example.invalid) · GPU name + fragments · pytest-of-<user> · 2 nsys binaries stripped
               origin: 803 refs forced with lease, 0 rejected, fresh-clone scan 0 · local: 1978 refs + 682 worktrees relinked · nodes 5457 = before · links 0 broken
               guard: box-local pre-commit hook (common hooks dir) = denylist ~/.config/agi/scrub-denylist.json + anonymize box tokens; 0 refusals on the last 300 commits
NEXT         (scan 0 DONE) crons_live true + crons.py apply -> start agi-keysync.timer, reaper, alarms -> "[rule] resume" to the frozen posts -> watch to 11:00Z
NOT THE PRIME'S  anonymize email + hardware classes (DG6 handover, loop branch) -> SM lanes to DG3/DG4 · anonymize install-hook checks MAIN's diff, not the committing worktree's (a g7.33 row)
```

## §2 Landed (gen 21)
post-scrub: ec09d0290 (.gitignore) · every pre-scrub SHA is REWRITTEN: old -> new = grep ^<sha> /data/scrub/union.git/filter-repo/commit-map (ONE union pass over local + origin; a first per-repo pass diverged and was replaced)

## 🔴 Where it stops
Finish the scrub close: repack/prune + local scan 0, crons back on, units back, resume the posts; then watch to 11:00Z (STOP cron aceed7d4) and the owner report
```
at 11:00Z   SendMessage each council/director post "stop: finish the step, card whole, idle" (stream-master stays) -> card -> owner report <= 6 lines
memory      Monitor on PSI full avg60 >= 20% or user@ within 64M of high; relief = memory.reclaim on the biggest file-heavy post scope, never a kill
addressing  SendMessage by "name [ref]" from ListAgents (agi-c8 / agi-8c / agi-e3 each name two posts)
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
SCRUB 08:3xZ: GitHub fresh mirror 259,334 objects -> 0 hits · origin/season2/main ancestor of the trunk again · local 229,343 objects -> 0 hits, fsck ok (stale refs/remotes/origin-posts/director-thought dropped: the last holder) · nodes 5457 = before · links 5414 / 0 broken · grid 5450 clean
guard-init 05:37Z: --status ok for agi-engine 3072M · agi-work 6742M · ramdisk 7168M · SM's Opus audit of d82a63e5a: 18 defaults == the old literals, plan identical (residue to DG4: validate cells before bash arithmetic; never `sudo -E`)
B3 merge verify on the RAM disk: 11/12 (bin-suite-fresh known) · links 0 · 5201 nodes · grid 165 versions / 0 errors · s-goal move: 0 hypotheses under s18/s31/s32/s34, links 5317/0 · DG4 cold homing falsifier: 5 homed, shmem +0M, tmpfs +1M

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| GitHub may still serve the OLD SHAs (cached views, any fork, PR refs) | the owner files a GitHub Support request to purge cached objects for the repo (draft given 08:xZ) |
| other boxes' clones (the grok team; one pushed a grid ref at 07:26Z) hold pre-scrub history | owner is telling them: re-clone, drop old worktrees/branches, push nothing from an old clone |
| /data/scrub backups hold the UNREDACTED history (mode 700) | keep 3 days, then delete backup-*.git + stripped/ copies |
| `*.pre-tier-*` backups: ~/.claude.pre-tier-20260930T0145Z + ~/.pi.pre-tier-20260930T0146Z (on /) | delete after a day of clean tiering |
| an on-disk /tmp makes every boot wait 5+ min in systemd-tmpfiles | tmpfs /tmp or a /tmp age cleaner, owner's call |
| belam row says opus-5-5 / high; the live Prime runs opus-5-5[1m] / max | owner sets the row |
| docker data-root still on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
