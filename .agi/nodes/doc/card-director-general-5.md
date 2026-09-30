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

## §0 State (09-30 06:2xZ · STOOD DOWN on the owner's order 06:1xZ via belam, verbatim: "We also will need to stand down director-general 5 and 6 to help conserve tokens as well. Just let them arrive at a stopping point and have them stop and take down the posts to free up resources. 3,4 can continue as is and pick up whatever 5,6 don't finish after standing down")
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · DOWN: recover false + pid 0 (belam) |
| pickup | DG3 / DG4 via SM's board: the HANDOVER table below is the whole state |
| split of record | rotate.py WHOLLY DG5 (now: whoever SM names) · dispatch.py launch resolvers · heal.py key path |
| skills | agi-dispatch · agi-corrective · agi-workflow · agi-master-gate · agi-goal · agi-node-write · agi-verify · agi-memory-guard |

## §1 HANDOVER (every unfinished leaf / row)
| goal / row | state | next command |
|---|---|---|
| goal:g1.31.4.2.1 (#40 #42 #31) | round a00-33e0c858 DONE, both kids proved; loop tip e5c338ffe, merge-base 324df95ec. Harvest tests on the tip (worktree .agi/worktrees/de-h-dg5-421): 18/19 files green; test_bin_help_smoke 1 fail = [snapshot-build-site.py] help, a file the round never touched: confirm on trunk. mur unit agi-director-general-5-mur4210609 RUNNING (pi-free, 2 slices: -fd, -copilot). MY READ: #40 #42 good; #31 likely a residue: hook_lines only PRINTS event+argv on every build_command (a stdout side effect on dispatch) and writes no copilot hooks config, so "registered" is named, not met | `python3 extensions/agi/bin/workflow.py status` -> read runs/<key>/{review,verify}_g1-31-4-2-1-*.json; #31 residue -> skill agi-corrective; land via skill agi-master-gate (merge-tree + commit-tree + ff-only); then `git worktree remove .agi/worktrees/de-h-dg5-421` |
| goal:g1.31.4.6.2 (#15) | parent a00-3014f810 FINISHED (not live); loop branch season2/loops/goal-g1.31.4.6.2-a00-3014f810 tip 7868fc91f: test_rotate.py +219, 2 hypothesis nodes. NOT harvested, NOT reviewed | harvest in place + mur pi-free (skill agi-workflow) |
| goal:g1.31.4.1 (#8 #9) | parent a00-1c745a92 (DG5.01) STILL LIVE, detached; 3 kids so far (da06914d proved, 829ed05f, 160ddb8a inconclusive_lean_proved); branch season2/loops/goal-g1.31.4.1-a00-1c745a92; RAM worktree /mnt/agi-ram/worktrees/a00-1c745a92 | `python3 extensions/agi/bin/spawn_budget.py status`; on exit: harvest + mur |
| goal:g7.16.1.5.4 | falsifiers 1+2 HOLD on DG5.01; closes when DG5.01 is harvested and its RAM worktree removed | `git worktree list | grep -c agi-ram` == 0, then set status complete |
| goal:g1.31.5.3 (n33 129 130 139 76 107) | NOT dispatched: n129/n130 overlap .4.2.1's first-decision edits, n107 overlaps .4.6.2's test_rotate.py xfail -> dispatch AFTER both land | dispatch.py . <ITER> --target goal:g1.31.5.3 --level small --tier parent --role parent --ladder-tier 0 --branch --detach |
| goal:g4.18.5.6 (horizon) | council go via SM 06:1xZ: rotate-out commit carries the RESOLVED doc:card-<post> or refuses by name; quorum path stays a symlink (no flatten at rotate.py:18885/18893) | claim, then dispatch after g1.31.5.3 |
| goal:g7.16.1.5.5.7 (horizon) | minted 1f81dbdbd: per-post MemoryHigh cell, scopes STAY in app.slice (Prime ruling) | build after the above |
| goal:g7.16.1.5.5.6 (active) | minted 1f81dbdbd: ram-main.sh + session-sweep.sh through locations.ram_write_argv + a one-shot recharge | dispatch a parent |
| goal:g7.16.1.5.5.1 | the proof is DONE, recorded on the node: 64 MiB via the helper after the 05:37Z apply, ramdisk shmem 675->739->675, engine 0->0, work 11->11 (baseline 05:40Z ramdisk 578M · engine 801M · work 281M) | none; SM reviews 1f81dbdbd |
| 1f81dbdbd (158b + stand-up 4-mode + R4 + F2 pin) | landed on the trunk; SM review queued | SM's verdict -> residues to the pickup post |

## 🔴 Where it stops
```
STOOD DOWN. Live and detached: parent a00-1c745a92 (DG5.01, goal:g1.31.4.1) · mur unit agi-director-general-5-mur4210609.
Next command (pickup post): python3 extensions/agi/bin/spawn_budget.py status
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock: every runner holds it per file | write.py commits refuse while ANY runner holds it: commit by exact path after; pytest inside it ERRORs at setup -> retry loop |
| systemd user manager sets TMPDIR=/data/tmp | runner scripts pin `env -u TMUX -u TMUX_PANE TMPDIR=/tmp` |
| a watch grepping "failed" | matches "xfailed": grep "[0-9]+ failed" |
| stand_up signature | stand_up(..., mode, keyed_in_body=False): a test fake must take **kw |
| replace body on this card | start at line 3 (never the H1), end on a blank line before the paid-for line |
| one scope-argv builder | any systemd-run argv goes through mem_cap.scope_argv (pinned: test_ram_worktrees) |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · ~/dg5/dg5-nbhd5.sh (60 files, 1877 passed at 1f81dbdbd) · RAM probe: bash /tmp/dg5/ramprobe.sh

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
