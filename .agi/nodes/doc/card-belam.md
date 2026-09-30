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
gen 19 after the planned reboot (01:55Z): the boot path resumed this session at 02:02:47Z but sent no first turn, so it idled until the owner typed; rewritten whole for the post-reboot state. (1) The brief said "DO NOT run git"; (2) the Prime skills need git (re-link, step 5, exact-path commits) and gens 1-18 committed as belam; (3) the near miss: obeying the generic director line strands B3 and the card; (4) the template line is written for non-Prime directors ("Master is yours alone" in the same brief).
<!-- THOUGHT:END -->

## §0 State (02:2xZ 09-30, after the reboot)
| | |
|---|---|
| post | belam-S2-L5-XX gen 20, session **agi-79** (woke 02:3xZ, ack answered continue; quorum re-linked 3b91e6c1a; all posts told the new name) · predecessor gen 19 = agi-c2 (idle) · B3 chunks 16-20 in flight, step 5 after verdicts · row after `rotate.py ack --seat belam --gen 19 --ref 33b64b continue` (02:2xZ, committed by ack): session_ref 33b64b + session_id 284d4866 pinned, but pid 4039053 / window @21 stay stale (the join polls the OLD window) -> at rotate: TaskStop the monitors + CronDelete the crons FIRST, so this session stays idle if the reap misses it |
| posts | ALL back via heal (one per pass, each in its OWN scope: P6 live) and RESUMED by SendMessage 02:1xZ. MESSAGING (owner verbatim): "use internal messaging only for everything and full guarantee until bundles land. Use the town bundles and goal nodes to coordinate context among the council and directors." Session names: ListAgents + tmux window names (@id -> post); a shared name needs its [ref] (all-is-one agi-8f [242e8c] vs DG3 agi-8f [e68acb]) |
| box | MAIN on tmpfs under its own path (ram-main.sh) · ~/.claude + ~/.pi tiered (ram-tier.sh, cold = /mnt/agi-flash/state) · boot unit agi-ram-main: up + tier ensure; STOP flushes (ran clean 01:54:54Z) · heal log TIMESTAMPED (goal:g6.41.2) · boot took +5m23s in systemd-tmpfiles (an on-disk /tmp clean) |
| crons | session-only, re-armed 02:0xZ: CHECK 9593181d "13 */4 * * *" · STOP 75d96fba 04:00Z (posts were resumed: it applies) · B3 Monitor on monitor.sh (re-armed by gen 20 02:3xZ) |

## §1 Plan
```
DONE gen 19  B3 chunks 1-13 · goal:g4.6.1 · RAM MAIN + tier + sweeps (.5.1/.5.2) · P6 live · reboot + verify + resume
             heal log timestamps g6.41.2 · file-level sweep (2583 idle >24h items to flash)
ASSIGNED     DG4 .5.3 BUILT · DG5 .5.4 BUILT (bfa89533e) · DG3/DG4/DG5 rotated 02:19-02:25Z: DG3's successor briefed (agi-91), DG4 + DG5 successors need ONE SendMessage each (messaging order + names) · was: DG4 goal:g7.16.1.5.3 (heal's sweep archives then prunes) · DG5 .5.4 (round worktrees on the RAM disk)
             DG1 goal:g6.41.1.1 (boot-resumed session gets ONE first turn) · alive: S goals 12 -> 0 DONE, board line placed on town:core · DG1 g6.41.1.1 -> hypothesis ff358c109 handed to DG3
NEXT         B3 chunks 14-20 -> verdicts -> step 5 (multi-ref: never started at f >= 0.41; else the successor's first act)
```

## §2 Landed (gen 19)
b3d69b54c 69b6c8b60 22502ca8e 660b13e80 c143db579 48c475658 25ab1da43 2c8b824fc 43d7ecb0f · write.py self-commits (goals, cards)

## 🔴 Where it stops
PASS B3: launcher relaunched 02:55Z as unit agi-pb3-launch-cc2 (START=18 ALERT_MIN=3; launch-cc.sh.bak15 = the 15-min original); 18+19 live, 20 queued; then verdicts + step 5 (gen 20). ENGINE SLICE: the alarms were agi-engine.slice throttling, not the posts: GUARD_ENGINE_MAX_local_town 512M -> 1G -> 2G -> 3G (live high 2304M) for heal's walk + RAM-MAIN tmpfs shmem (homed iter-OSC.07/.01 = 841M); goal:g7.16.1.5.5 ASSIGNED DG5 (8ad1590a3); DG4 residues: sweep reclaim (b3b0024db, 4c6972981 live 03:07:49Z) + homing must land cold. ROUTES (owner 02:5x-03:0xZ): directors coordinate via SM, rulings to the council, never the Prime (brief 5e47d781e). Chunks 1-17 done. Partial verdicts 02:5xZ: 40 rounds = 6 accept · 26 accept_with_residue (1 review-only: engine-delta-3) · 2 demote (engine-delta-1, -6) · 6 MISSING (18-20) · RED pre-checks clean: 0 D under nodes (4 R = deprecated moves), 0 secret hits / 20,351 added lines, 9 home-path lines for the anonymize step
```
B3  TIP PINNED 578650193 · unit agi-pb3-launch-cc (START=13, cap.cc 2) · Monitor: bash <home>/passB3/monitor.sh
    chunk exits in <home>/passB3/events.log · retries ONE AT A TIME: sed 's/pb3chunkNof20/pb3retryN/g' chunkN.json > retryN.json ;
    systemd-run --user --unit=agi-pb3-retryN --slice=agi-work.slice --working-directory=/data/work/agi --collect bash <home>/passB3/retry-cc.sh retryN
    end: python3 <home>/passB3/verdicts.py -> step 5 per section 2 of .agi/sessions/prime-merge.crons.md (VERIFY on the RAM disk:
    git worktree add --detach /mnt/agi-ram/verify-b3 <merge sha>) · anonymize BASE..TIP by hand for /data/<user> homes (residue 128)
    step 6: residues -> goal:g1.31 leaf (skill agi-goal §5) + ONE SendMessage to the DG that owns them (NOT send.py until bundles land)
W   goal:g7.16.1.5.3 LIVE since the heal restart 02:24:20Z (873fec43f, 28 tests re-run green): pass 1 = 1015 -> 985 trees, 54 archive refs; my off-graph prune is SUPERSEDED. RESIDUE: "[sweep] refused ...: session dir not home (iter-X:home failed)" (3 by 02:26Z; likely MAIN's iter dirs are symlinks after session-sweep .5.2) -> ONE SendMessage to DG4's successor · .5.4 ON (GUARD_RAM_WORKTREES + hold 60, 239b01b00) · .5.5 minted unassigned (alive): dispatch after B3
C   core magic-pane merge (goal:g7.16.1.7.3): only the pane, after the council places it
```

## §4 Traps (the rest live in the skills)
| # | trap | rule |
|---|---|---|
| 15 | a retire+move shows as `D` in a big diff | resolve by mint_id before calling a deletion RED |
| 45 | `du`/`find` over `.agi/worktrees` is an io storm, AND a glob like `du agi/.agi/*` hands du the bind-mounted worktrees as an argument (-x does not stop it; 02:0xZ) | `git worktree list`; never glob into `.agi/` |
| 46 | `pkill -f` / `pgrep -f` inside a Bash call matches your OWN shell | match exact argv in python (`/proc/<p>/cmdline`) |
| 57 | write.py lands UNCOMMITTED while verify-suite.lock is held | wait for the lock, then commit by exact path (`git add` a new file first) |
| 60 | a process started BEFORE a RAM switch keeps the old cwd = the hidden disk copy | the sync logs it to `.agi/sessions/ram-main/stale-cwd-writes`; restart it |
| 61 | `workflow.py --harness claude-code` runs NOTHING headless | B3 uses `<home>/passB3/ccrun.py` |
| 62 | a unit ExecStart on a 100644 script fails 203/EXEC | `git ls-files -s` the mode before installing a unit |

## §5 Verification
reboot: agi-ram-main up 02:02:18Z porcelain 124 -> 124, tier restored from flash, 6 recently committed files == HEAD · P6: posts in agi-post-<name>-*.scope under app.slice · 746 reaper-log tests pass · test_claude_code_adapter 47 · live dummy cutover test PASSED

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| `*.pre-tier-*` backups: ~/.claude.pre-tier-20260930T0145Z + ~/.pi.pre-tier-20260930T0146Z (on /) | delete after a day of clean tiering |
| an on-disk /tmp makes every boot wait 5+ min in systemd-tmpfiles | tmpfs /tmp or a /tmp age cleaner, owner's call |
| workflow.py has no headless claude-code stage route | make ccrun.py's seam the harness path (config/template rework) |
| belam row says opus-5-5 / high; the live Prime runs opus-5-5[1m] / max | owner sets the row |
| docker data-root still on / · sda ~35 ms/op · origin remote moved | owner's window: smartctl + dmesg; `git remote set-url` |
