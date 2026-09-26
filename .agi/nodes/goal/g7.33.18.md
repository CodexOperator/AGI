---
id: goal:g7.33.18
mint_id: dbaf082ba61243e3a5a01f6fe1ecf214
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.7
edited_by: thought-master
goal_id: G7.33.18
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 232a1b029b951f26
season: 2
seeds: []
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
tags:
  - local-maxxing
  - engine
title: "G7.33.18: ONE BOX MEMORY-GUARD KIT -- every box that runs seats carries local-town's memory-watch stack, sized to its own RAM, installed from the repo (the owner's other-box ask; assigned director-engine)"
town: core
---
# goal:g7.33.18

WORLD-AFTER: every box that runs seats carries the SAME memory-watch stack, sized to its OWN RAM, installed from ONE kit in the repo -- never a hand copy from another box. Today the box-level pieces live only on local-town (`/usr/local/sbin`, `/etc/systemd`, `~/.config/systemd/user`); none is in git, so encryption-town (sanctuary's box, where the stream is moving) cannot install them from its checkout.

| layer | local-town as measured 21:3xZ 09-26 (15932 MiB RAM, 4095 MiB swap) | the kit ships |
|---|---|---|
| user@<uid> caps | `user@1000.service.d/50-sanctuary-guard.conf`: MemoryHigh 6628M · MemoryMax 7365M · MemorySwapMax 2047M · MemoryLow 1024M · TasksMax 16384 · ManagedOOMMemoryPressure=kill at 50% | the drop-in, sized by SIZING |
| oomd | `oomd.conf.d/50-sanctuary-guard.conf`: SwapUsedLimit 90% · DefaultMemoryPressureLimit 60% · DefaultMemoryPressureDurationSec 20s | the drop-in |
| slices | `user.slice.d` + `user-1000.slice.d` MemoryLow 1024M · `system.slice.d` MemoryMin 128M | the drop-ins |
| agi.slice (user) | MemoryHigh 4639 MiB · MemoryMax 5155 MiB | the unit, sized |
| memguard | `/usr/local/sbin/agi-memguard.py` + `agi-memguard.service` (Restart=always, OOMScoreAdjust=-1000, Nice=-10) | the script + the unit |
| no cascade | `10-agi-survival.conf` OOMPolicy=continue on claude-remote-control, streamer-stub, streamer-stub-watch | the drop-ins |
| watchdog | `/etc/watchdog.conf` (timeout 60, interval 10, test-binary `/usr/local/sbin/sanctuary-health`, repair-maximum 1) | the conf + the health script |
| memory_alarm | `config:crons` job memory_alarm (every minute, `--notify belam`) | already graph-declared: `crons.py apply` |
| per-spawn caps | `spawn.memory_max` 2G + `spawn.tasks_max` 150 (the Prime's [decision] 20:13Z, OWNER 19:5xZ); a model round dispatches `--memory <GB>` under model_slot | config cells |
| mem_cap probe | `mem_cap.systemd_run_usable(cfg)` is True | the read-back |
| model gate | the `--no-model` fence (DH.415) + model_slot the only lift (director-thought, TMM.259) | rides director-thought's merge-up |

SIZING, per box: user@ MemoryMax = MemTotal - every budget held outside user@ (container caps; the stream when it runs outside user@) - 2 GiB system reserve · MemoryHigh = 0.9 x MemoryMax · MemorySwapMax = 0.5 x swap · agi.slice MemoryHigh / MemoryMax = 0.63 / 0.70 x user@ MemoryMax (local-town's ratios).

ACCEPTANCE: one idempotent installer (dry-run by default; records every before-value; restores them on failure; sudo only for the system pieces) + one read-back probe that prints this table for the box it runs on -- green on local-town AND on encryption-town, the latter run by that box's own seat.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by thought-master 21:4xZ 09-26 for the owner's ask, relayed verbatim by belam 21:28:58Z -- OWNER 20:4xZ 09-26 (Prime pane): "Yeah sanctuary master may be not fully set up properly. Can we have thought master make sure the other box is fully set up with all the proper updated memory watch fixes." Why a kit and not a copy: local-town's guard pieces (memguard, the watchdog health test, the 50-sanctuary-guard drop-ins, the no-cascade drop-ins) exist only in its /usr/local/sbin and /etc -- none is in git -- and local-town has no ssh route to encryption-town, so that box's own seat must install them, and it can only install what its checkout carries. Local-town's values are the measured baseline; SIZING turns them into ratios so a box with other RAM gets its own numbers. The per-spawn caps follow the Prime's owner-approved [decision] 20:13Z (2G + TasksMax 150), which supersedes the master's 3G (10925dba7, VOID, corrected in f28493d5b).
<!-- THOUGHT:END -->
