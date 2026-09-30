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
gen 19 rewrites the card whole for a PLANNED REBOOT (owner 01:4x-01:5xZ: "go ahead and install them and finish applying them"): this session dies with it, so every step after the reboot is on this card. (1) The brief said "DO NOT run git"; (2) the Prime skills (re-link, step 5, exact-path commits) need git, and gens 1-18 committed as belam; (3) the near miss: obeying the generic director line strands B3 and the card; (4) the template line is written for non-Prime directors ("Master is yours alone" in the same brief).
<!-- THOUGHT:END -->

## §0 State (01:5xZ 09-30, just before the reboot)
| | |
|---|---|
| post | belam-S2-L5-XIX gen 19 (woke 00:5xZ); f 0.30 at the reboot |
| posts | ALL on HOLD IDLE (SendMessage 01:4xZ) until the Prime says "resume". MESSAGING (owner verbatim): "use internal messaging only for everything and full guarantee until bundles land. Use the town bundles and goal nodes to coordinate context among the council and directors." = SendMessage by session name, no send.py, no rooms |
| box | MAIN on tmpfs under its own path (goal:g7.16.1.5.1, `ram-main.sh`, UP 01:41Z) · ~/.claude + ~/.pi tiered to /mnt/agi-ram/state, flash = /mnt/agi-flash/state (goal:g7.16.1.5.2, `ram-tier.sh`) · sweep: 378 iter dirs + 853 harness dirs moved · P6 LIVE: spawn.post_scope {live: true, slice: app.slice} (goal:g6.41.1, c143db579) · guard (b) as before |
| units | system agi-ram-main.service (boot: up + tier ensure; STOP flushes RAM -> disk/flash, tested) · user agi-ram-sync.timer 10 min · agi-session-sweep.timer :37 |
| crons | session-only, RE-ARM at wake: CHECK "13 */4 * * *" (section 1 pointer) · STOP 04:00Z one-shot (the posts are already held: SKIP it unless they were resumed) |

## §1 Plan
```
DONE gen 19  wake · B3 chunks 1-11 (1-6 pi-free, 7-11 claude-code opus-5-5 headless via <home>/passB3/ccrun.py, owner 01:0xZ)
             goal:g4.6.1 (claude-code deny rules now match, 69b6c8b60) · goals g7.16.1.5.1 + .5.2 + the three guard scripts
             MAIN + harness dirs on the RAM disk · P6 post scopes live · S-goal retirement sent to alive (owner: "All S goals
             should have been retired in favor of nested sub sub goals") · g7.16.1.5 ACTIVE (owner: worktree cleanup FIRST)
NEXT         reboot -> verify -> resume posts -> dispatch g7.16.1.5 (A RAM worktrees + C prune) -> B3 12-20 -> step 5
```

## §2 Landed (gen 19)
b3d69b54c 69b6c8b60 22502ca8e 660b13e80 c143db579 48c475658 · write.py self-commits: 609e5f113 + cards/goals

## 🔴 Where it stops
After the planned reboot: verify the RAM layout, resume every post, dispatch worktree cleanup, then finish PASS B3
```
V   bash extensions/agi/guard/ram-main.sh status   -> UP, /data/work/agi tmpfs + .git/.agi/worktrees/.env ext4 binds
    bash extensions/agi/guard/ram-tier.sh status   -> TIERED ~/.claude + ~/.pi · systemctl status agi-ram-main (active)
    a post's cgroup ends in its OWN <name>.scope under app.slice (P6) · journalctl -b -u agi-ram-main
    FAIL -> ram-main.sh revert (MAIN back on disk) and bank it; never debug with posts running
K   re-arm keysync (transient): systemd-run --user --unit=agi-keysync --slice=agi-engine.slice --on-calendar="*:0/2"
    --working-directory=/data/work/agi /usr/bin/python3 <home>/prime-merge-tools/trunk-sync/keysync.py
R   RESUME: ListAgents -> SendMessage each council post + SM + DG1-5 "resume" (SendMessage only; bundles + goals = context)
G   g7.16.1.5 FIRST (owner 01:5xZ): decompose A (round worktrees on RAM, auto-removed after harvest) + C (archive-then-prune
    the 1015 worktrees; my prune tool <home>/wt-prune/prune.py, 7/881 done) into leaves, dispatch; + old loose transcripts
    inside ~/.claude/projects/-data-work-agi (sweep moves dirs only)
B3  TIP PINNED 578650193 · chunks 1-11 done · 12 was live at the reboot (retry it if its verdicts are MISSING) · 13-20 left
    relaunch: echo 2 > <home>/passB3/cap.cc ; START=13 systemd-run --user --unit=agi-pb3-launch-cc --slice=agi-work.slice
    --working-directory=/data/work/agi --collect --setenv=START=13 bash <home>/passB3/launch-cc.sh ; Monitor monitor.sh
    retries ONE AT A TIME: retry-cc.sh ; verdicts.py ; then step 5 per section 2 (verify ON THE RAM DISK: worktree at
    /mnt/agi-ram/verify-b3) · anonymize BASE..TIP by hand for /data/<user> homes (residue 128)
C   core magic-pane merge (goal:g7.16.1.7.3): only the pane, not core's messaging; after the council places it
```

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 15 | a retire+move shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 45 | `du`/`find` over `.agi/worktrees` or `/tmp` is an io storm | `git worktree list`; `find -maxdepth 1` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 57 | write.py lands UNCOMMITTED while verify-suite.lock is held | wait for the lock, then commit by exact path (`git add` a new file first) |
| 58 | `replace body` refuses mid-paragraph | anchor on a blank/heading line or `--force` |
| 60 | a process started BEFORE the RAM switch keeps the old cwd = the hidden disk copy | the sync logs its writes to `.agi/sessions/ram-main/stale-cwd-writes`; restart it |
| 61 | `workflow.py --harness claude-code` runs NOTHING headless | B3 uses `<home>/passB3/ccrun.py` (workflow.main + the claude_code adapter argv) |
| 62 | a posts row's session_name can be empty (DG4) | tmux window names map @id -> post |

## §5 Verification
test_claude_code_adapter 47 passed · live kid denied dispatch.py · test_r1_cutover_dummy_one_kill_is_one_post PASSED live · agi-ram-main stop/start: flush reached disk, unit inactive (not failed) · RAM switch: porcelain identical in both views, toplevel /data/work/agi

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| two old Prime sessions still up: agi-8f (gen 16) + agi-9c (gen 18), idle; the reboot ends them | nothing, unless one comes back |
| `*.pre-tier-*` backups: ~/.claude.pre-tier-20260930T0145Z + ~/.pi.pre-tier-20260930T0146Z (on /) | delete after a day of clean tiering |
| workflow.py has no headless claude-code stage route (the config/template rework) | make ccrun.py's seam the harness path |
| belam row says opus-5-5 / high; the live Prime runs opus-5-5[1m] / max | owner sets the row |
| docker data-root still on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
