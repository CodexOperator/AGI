---
id: doc:card-director-general-5
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-5
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

## §0 State (09-30 05:5xZ, meter ~0.15 of 0.47 · RESUMED on the owner's order until 11:00Z, full speed)
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · CC Opus 5.5 high |
| goal | goal:g1.31 leaves (.4.1 · .4.2.1 · .4.6.2) · goal:g7.16.1.5.5 (.5.5.1 LIVE, .5.5.6 active, .5.5.7 horizon) · goal:g7.16.1.5.4 closes at the .4.1 harvest · 7a goal:g7.16.1.7.1 |
| lanes (owner 03:0xZ) | coordination, queue, SHAs -> sanctuary-master (agi-5c) · rulings -> council: alive agi-b3 · all-is-one agi-8f · self-perpetuating agi-53 · never the Prime |
| spend | Opus subagents ended at the ~06:0xZ reset -> pi-free / Sonnet 5.5 only |
| split of record | rotate.py WHOLLY DG5 · dispatch.py launch resolvers · heal.py key path. DG3 = write.py/node_writer · DG4 = every non-rotate writer |
| skills | agi-goal · agi-node-write · agi-verify · agi-rotate · agi-post · agi-memory-guard · agi-dispatch · agi-corrective · agi-workflow |

## §1 Plan
```
SM order 05:3xZ: (1) ONE commit: 158b key order + stand-up 4-mode keys (DG2 fork) + R4 node text + .7.1.1 F2 pin  <- IN TEST (nb0544)
                 (2) harvest a00-1c745a92 (.4.1) in place -> mur pi-free -> merge -> [merge-up]  (3) .4.2.1  (4) .4.6.2
  then build goal:g7.16.1.5.5.7 (per-post MemoryHigh cell; Prime ruling: scopes STAY in app.slice) and .5.5.6 (writers + recharge)
7a   .1.3 left: .3.2 bullet 2 (spawn.harness + workflows.*.provider flip = its own tested change) · .3.3 aliases = season 3
     self-perpetuating gaps (/tmp/sp-g717-gaps.md): .7.1.5-.7.1.7 · .7.2.6-.7.2.8 (not minted)
```

## 🔴 Where it stops
```
Uncommitted in MAIN (mine, commit by exact path once nb0544 is green, ~/dg5/nbhd.out DONE):
  extensions/agi/bin/rotate.py · extensions/agi/tests/test_stand_up.py · extensions/agi/tests/test_ram_worktrees.py
  .agi/nodes/goal/g7.16.1.5.5.1.md (RAM proof line) · g7.16.1.5.5.6.md · g7.16.1.5.5.7.md (minted, lock refused the commit)
LIVE ROUNDS (reconcile: python3 extensions/agi/bin/spawn_budget.py status):
  a00-1c745a92 DG5.01 goal:g1.31.4.1 -- kid a00-da06914d proved; 2nd kid a00-829ed05f live; RAM worktree /mnt/agi-ram/worktrees/a00-1c745a92
  a00-33e0c858 DG5.02 goal:g1.31.4.2.1 (#40 #42 #31; orders /tmp/dg5/orders-g1.31.4.2.1.md) branch season2/loops/goal-g1.31.4.2.1-a00-33e0c858
  a00-3014f810 DG5.03 goal:g1.31.4.6.2 (#15, test_rotate.py only) branch season2/loops/goal-g1.31.4.6.2-a00-3014f810
goal:g7.16.1.5.4: CLOSE once a00-1c745a92 is harvested and its RAM worktree removed (git worktree list | grep -c agi-ram == 0).
Next command: `tail -3 ~/dg5/nbhd.out`
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock: every runner holds it per file | write.py commits refuse while ANY runner holds it: commit by exact path after; pytest inside it ERRORs at setup -> retry loop |
| systemd user manager sets TMPDIR=/data/tmp | runner scripts pin `env -u TMUX -u TMUX_PANE TMPDIR=/tmp` |
| write.py sub counts | its "N match(es)" line is cumulative over the script's subs |
| stand_up signature | stand_up(..., mode, keyed_in_body=False): a test fake must take **kw |
| systemd slice names: a dash nests | the RAM slice is ramdisk.slice, never agi-ram.slice |
| one scope-argv builder | any systemd-run argv goes through mem_cap.scope_argv (pinned: test_ram_worktrees) |
| config:guard, config:key-authority fields | Prime/owner-only: send the exact line via SM |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · ~/dg5/dg5-nbhd5.sh (rotate/heal/send/seatsig/stand_up/session_start) · ~/dg5/dg5-nbhd6.sh (dispatch/cli/heal_watch/boxkit/locations) via `systemd-run --user --unit=agi-director-general-5-<key> --working-directory=/data/work/agi -p MemoryMax=6G -p MemorySwapMax=0 bash <script>` -> ~/dg5/nbhd.out (DONE line) · RAM proof: bash /tmp/dg5/ramprobe.sh

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
