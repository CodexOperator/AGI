---
id: doc:card-director-general-5
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: e13627c192e516b7
season: 2
tags:
  - card
  - director
  - director-general-5
thought_session: director-general-5
title: Card director general 5
town: core
---
# doc:card-director-general-5

Role = the director template + the HEAD (`doc:unified-head`) + the council protocol (`doc:council-loop`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (09-30 05:2xZ, gen 3, meter ~0.38 of 0.47, rotating · RESUMED 04:5xZ on the owner's order until 11:00Z, full speed)
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · CC Opus 5.5 high |
| goal | goal:g7.16.1.5.5 (RAM disk's own budget line; .5.5.1 built) · goal:g1.31 leaves (below) · goal:g7.16.1.5.4 ON, closes at the first live round · 7a goal:g7.16.1.7.1 · 7b after goal:g7.16.1.6 + goal:g4.18.6 |
| lanes (owner 03:0xZ) | coordination, queue order, SHAs -> sanctuary-master (agi-5c since its rotation; ListAgents) · rulings -> the council: alive agi-b3 · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 · never the Prime |
| spend | owner 05:0xZ: Opus subagents allowed until the reset (~06:0xZ), then back to pi / Sonnet 5.5 |
| split of record | rotate.py WHOLLY DG5 · dispatch.py launch resolvers · heal.py key path. DG3 = write.py/node_writer · DG4 = every non-rotate writer + .5.5.3.x (re-parented to .5.5 after alive ruled (a)) |
| skills | agi-goal · agi-node-write · agi-verify · agi-rotate · agi-post · agi-memory-guard · agi-dispatch |

## §1 Plan
```
SM order (05:4xZ): (1) 786c1c13a R1-R4 DONE bea6448a1 · (2) keys residues 158/160/161/159 DONE 4feed71aa · (3) g1.31 leaves  <- NEXT
  goal:g1.31.4.1    #8 #9 dispatch --branch dry run prints no worktree/branch/base; accepts a target the live path refuses
  goal:g1.31.4.2.1  #40 #42 harvest merge line uses the LLM label; first-decision duplicates the harvest reader
                    #31 #32 copilot hooks never registered + a false "no remote-control mode" message · #45 rotate.py status misses belam-* windows
  goal:g1.31.4.6.2  #15 posts one-writer test lacks a per-path call count (with DG3)
  SM: "dispatch parents in parallel where the files do not overlap"
.5.5  .5.5.1 BUILT: waits on SM's accept -> the Prime applies guard-init (sudo) + declares GUARD_RAM_BUDGET in config:guard
           left: route every other engine bulk RAM writer through locations.ram_write_argv; a recharge of pages already on agi-engine.slice
      .5.5.2 horizon: GUARD_ENGINE_MAX back from the 3G stopgap to a derived value
7a    .1.3: falsifier re-pointed (89ef864c3); left: .3.2 bullet 2 (spawn.harness + workflows.*.provider still pi-free -- flipping
      to pi sends workflow.py into its harness == pi branch: its own tested change) · .3.3 aliases retire = season 3
      self-perpetuating's coverage review (/tmp/sp-g717-gaps.md): mint .7.1.5 two render modes · .7.1.6 first turn = a render tool
      call · .7.1.7 no row claims a dead life · .7.2.6 adapter onto the 4 verbs · .7.2.7 post row links its context docs · .7.2.8 key row
      on every trunk + predecessor link
```

## §2 Landed (gen 3)
- 37d8a473d ONE pi template · 99250d4f0 manifest stand-up · 4abfee9d3 + c14815594 .1.4 keys (council ruling C) · 4feed71aa run-27 residues 158-161
- ce8a681ed / 6cfb8bdf7 .5.4.1 minted + retired · 6e171495d .5.5 leaves · 786c1c13a + bea6448a1 .5.5.1 ramdisk.slice (live probes: engine shmem unchanged)
- 46aee1e96 / f335e2003 / 9d1fec397 .5.5.3 retired (alive ruled (a); the brief un-retire crossed SM's hold) · 89ef864c3 .7.1.3 re-point
- gen 1-2: git history of this node

## 🔴 Where it stops
```
LIVE ROUND: parent a00-1c745a92 (iter DG5.01, pi-free, detached, pid 2096989) on goal:g1.31.4.1 (#8 #9 dispatch --branch dry run),
  branch season2/loops/goal-g1.31.4.1-a00-1c745a92, worktree /mnt/agi-ram/worktrees/a00-1c745a92 (.agi/worktrees/<id> = symlink).
  Reconcile at wake: `python3 extensions/agi/bin/spawn_budget.py status`; harvest IN PLACE + mur (--harness pi-free) per the director template.
goal:g7.16.1.5.4: falsifiers 1+2 HOLD on that round (1 agi-ram worktree, symlink only); ramdisk.slice took its checkout (144 MiB).
  CLOSE .5.4 once the round is harvested and its RAM worktree removed (the Prime's condition): git worktree list | grep -c agi-ram == 0 after.
Successor leaves (SM): goal:g1.31.4.2.1 (#40 #42 #31 #32 #45: rotate.py -- #32 = rotate.py:2631 says "copilot has no remote-control
  mode" but templates/harness/copilot-cli.toml ships --remote; #45 = cmd_status filter rotate.py:3797 drops DEFAULT_TMUX_SESSION agi-rc)
  · goal:g1.31.4.6.2 (#15, with DG3). Dispatch parents where files do not overlap.
In review via SM (Opus): bea6448a1 (R1-R4) · 4feed71aa (158-161). After SM accepts bea6448a1 the Prime applies guard-init + the R3 line.
Next command: `python3 extensions/agi/bin/spawn_budget.py status`
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock: every runner holds it per file | write.py commits refuse while ANY runner holds it: commit by exact path after; pytest inside it ERRORs at setup -> retry loop |
| systemd user manager sets TMPDIR=/data/tmp | runner scripts pin `env -u TMUX -u TMUX_PANE TMPDIR=/tmp` (env's -u BEFORE the assignment) |
| python heredoc carrying shell text with EOF | a distinct delimiter (PYEOF) |
| write.py replace body guards paragraphs | replace from a heading through the block's closing fence |
| node_writer indexes a root once | a test that reads a node it writes later needs its own root |
| systemd slice names: a dash nests | the RAM slice is ramdisk.slice, never agi-ram.slice |
| one scope-argv builder (goal:g7.16.1.7.1.1) | any systemd-run argv goes through mem_cap.scope_argv / wrap_argv |
| config:guard, config:key-authority fields | Prime/owner-only: send the exact line via SM |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · runners ~/dg5/dg5-nbhd5.sh (62 rotate/heal/send/seatsig/stand_up/session_start files) · ~/dg5/dg5-nbhd6.sh (18 dispatch/cli/heal_watch/boxkit/locations files) via `systemd-run --user --unit=agi-director-general-5-<key> --working-directory=/data/work/agi -p MemoryMax=6G -p MemorySwapMax=0 bash <script>` -> ~/dg5/nbhd.out (DONE line)

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
