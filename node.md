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

## §0 State (17:4xZ 09-30, read from date -u)
| | |
|---|---|
| post | belam-S2-L5-XX gen 22 (woke 16:56Z); predecessors idle: gen 21 agi-23 · gen 20 agi-79 · gen 19 agi-c2 |
| run | EXTENDED 17:4xZ (owner: "Please extend the cutoff to about 5 p.m., after which point continue working using the free lane.") -> current lanes to **21:00Z** (5pm EDT), then **FREE LANE ONLY** (pi-free, 0 USD), NO STOP · rule: doc:unified-director-brief ROUND LANES (9cb773a774) · relayed to SM agi-12 [afd9c6] |
| posts | DG5 + DG6 DOWN (handovers re-laned by SM: DG3 privacy cluster, DG4 hook/harvests/CC route) · SM = agi-12 @27 · DG3 = agi-00 @29 · DG4 = agi-10 @28 · all-is-one = agi-8f @1 · self-perpetuating = agi-53 @2 (14:2xZ; always "name [ref]") |
| crons | session: CHECK 97929cb8 (13 */4) · LANE-SWITCH one-shot bb871f87 (21:02Z; the 18:02Z STOP 13266db4 cancelled) · memory Monitor blhckdxaw (PSI full avg60 >= 10%, 30 min, re-arm) · box crontab LIVE (crons_live true, 12 jobs) · keysync timer re-created (transient, */2 min) |
| scrub | /data/scrub (mode 700): RESUME.md = the step table + revert · backup-local.git · backup-origin(2).git · stripped/ (2 nsys files, also back on disk, gitignored) |

## §1 Plan
```
DONE gen 21  guard-init applied (empty plan diff) · post scopes ruled to app.slice · command:commands canonicalize (d7cb48e6a pre-scrub) · config:guard doc header
             config:census minted · skill agi-send name [ref] row · brief SUBAGENTS = Sonnet 5.5 strictly · DG5 + DG6 stood down
             HISTORY SCRUB: email (text + 7k author lines -> the example.invalid placeholder address) · GPU name + fragments · pytest-of-<user> · 2 nsys binaries stripped
               origin: 803 refs forced with lease, 0 rejected, fresh-clone scan 0 · local: 1978 refs + 682 worktrees relinked · nodes 5457 = before · links 0 broken
               guard: box-local pre-commit hook (common hooks dir) = denylist ~/.config/agi/scrub-denylist.json + anonymize box tokens; 0 refusals on the last 300 commits
             after resume: harness claude-code models -> Sonnet 5.5 (8b9fded02) · [config] schema spawn: block (436f4b418) · council-loop town -> local-maxxing
             operating-mode ruling (NONE binds) waits on DG4's brief.py round + its pinned test (then land the 2-line config.json edit) · old->new sha map kept LOCAL
             memory: 5 cache spikes to user@ high 08:0x-10:56Z, each cleared by memory.reclaim (never a kill) -> the RAM budget leaf goal:g7.16.1.5.5 is the real fix
             12:4xZ owner: "Oh neat continue now until 2pm EST." -> all posts RESUMED to 18:00Z · self-perpetuating double seat: kept @2 (agi-53: row + transcript), closed the stranded @19 (failed 05:17Z join)
             addressing: SendMessage ONLY by "name [ref]"; offline Remote Control rows named like the posts (all-is-one [0781f7], alive [68d0c9], ...) swallow bare names; all-is-one = agi-8f [242e8c]
14:xZ: RAM disk 4.1G -> 2.3G (13 clean idle Agent worktrees removed; DG4 row: bind <repo>/.claude/worktrees from disk) · paths.local_maxxing.scrub_commit_map 1b14a0048 · SLO8 whois fact restored d71e39b69 · 8 trunk reds laned by SM (links.py:440 decode -> DG2; brief g15 -> DG4; boxkit anonymize fake denylist -> DG2)
             STILL MINE: config:rotations skills entry (:83 + :123) + agi-post, agi-stream, byte_cap 6000 -> 8000, THOUGHT -- only once DG4 lands build:skills-agi-post-SKILL.md + build:skills-agi-stream-SKILL.md (SM sends the exact text)
16:4xZ owner opened round lanes past pi-free (claude-code Sonnet 5.5 kids; parents+kids once proven; subagents or direct): brief SUBAGENTS row 6db908311, relayed via SM · email_allow user@UID.service 842cb065d · memory relief now PSI-gated (>= 10%): cache at user@ high with PSI 0 is normal, never churn on it
NEXT         the watch to 18:00Z, then STOP + owner report
NOT THE PRIME'S  anonymize email + hardware classes (DG6 handover, loop branch) -> SM lanes to DG3/DG4 · anonymize install-hook checks MAIN's diff, not the committing worktree's (a g7.33 row)
```

## §2 Landed (gen 21)
post-scrub: ec09d0290 (.gitignore) · every pre-scrub SHA is REWRITTEN: old -> new = grep ^<sha> /data/scrub/union.git/filter-repo/commit-map (ONE union pass over local + origin; a first per-repo pass diverged and was replaced)

## 🔴 Where it stops
Re-arm at wake (before 21:00Z): LANE-SWITCH one-shot "2 21 30 9 *" + CHECK "13 */4 * * *" + the memory Monitor. After 21:00Z: CHECK + Monitor only -- the free lane has no end time, so there is NO STOP to arm
```
at 21:00Z   ONE SendMessage to sanctuary-master agi-12 [afd9c6]: "free lane NOW" (pi-free only, no claude-code dispatch, no Sonnet subagents; live claude-code rounds finish) -> spawn_budget.py status: new parents pi-free -> card run row -> one owner line
memory      Monitor on PSI full avg60 >= 10% (relief) / >= 20% (red); user@ at high with PSI ~0 = page cache, never act; relief = memory.reclaim on the biggest file-heavy post scope, never a kill
```
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
| /data/scrub backups hold the UNREDACTED history (mode 700) | keep 3 days, then delete backup-*.git + stripped/ copies (the old->new sha map is kept apart: /data/agi-maps/scrub-2026-09-30.commit-map) |
| the old->new sha map stays LOCAL (a public full old-sha list = lookup keys into GitHub's stale cache) | track it (for resolve_old_sha, DG3 leaf) only AFTER the owner confirms the GitHub purge |
| `*.pre-tier-*` backups: ~/.claude.pre-tier-20260930T0145Z + ~/.pi.pre-tier-20260930T0146Z (on /) | delete after a day of clean tiering |
| an on-disk /tmp makes every boot wait 5+ min in systemd-tmpfiles | tmpfs /tmp or a /tmp age cleaner, owner's call |
| belam row says opus-5-5 / high; the live Prime runs opus-5-5[1m] / max | owner sets the row |
| docker data-root still on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
