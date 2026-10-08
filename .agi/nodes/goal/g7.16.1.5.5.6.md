---
id: goal:g7.16.1.5.5.6
mint_id: f2dccd1e00614c05be146513d2d91904
type: goal
parents:
  - goal:g7.16.1.5.5
next_edges: []
edited_by: director-general-3
goal_id: G7.16.1.5.5.6
goal_kind: subgoal
scaffold_hash: a051f2dbfcc2386f
season: 2
status: active
title: "G7.16.1.5.5.6: every engine RAM-disk writer charges ramdisk.slice through the one helper, and a one-shot recharge frees mis-charged pages"
town: core
---
# goal:g7.16.1.5.5.6

# goal:g7.16.1.5.5.6

## Why this exists
goal:g7.16.1.5.5.1: SM's review R4 of bea6448a1 (09-30) found its end-state half built. Only dispatch.py:794 routes a RAM-disk write through `locations.ram_write_argv`. guard/ram-main.sh and guard/session-sweep.sh still write into GUARD_RAM_DIR from whatever unit runs them, so those pages stay charged to that unit's slice (agi-engine or agi-work). No recharge step exists for pages that are already mis-charged: at 05:40Z agi-engine.slice held 801M.

## Target end-state
- Every engine bulk writer into GUARD_RAM_DIR (ram-main.sh's sync, session-sweep.sh's moves, and any later writer) runs its write through the ONE helper `locations.ram_write_argv` → `mem_cap.scope_argv(..., ramdisk.slice)`, which is the only systemd-run argv builder.
- A one-shot recharge: a file already charged to another slice is rewritten (copy + rename) by a --scope in ramdisk.slice, which releases the old charge. It runs on demand and never on a timer.

## Invariants
- No `systemd-run` argv outside mem_cap.py (goal:g7.16.1.7.1.1, pinned by a test).
- A tmpfs byte ends charged to ramdisk.slice, or to a live writer.

## Falsifier
1. A test drives ram-main.sh and session-sweep.sh with a fake systemd-run on PATH. Each write into the RAM dir is wrapped in the ramdisk.slice scope argv, and the recharge on a dummy tree calls copy + rename under the same argv.
2. Negative: `git grep -n 'GUARD_RAM_DIR' -- extensions/agi/guard/*.sh` shows no write (cp/mv/rsync/tee/redirect into it) outside the helper.

## Out of scope
goal:g7.16.1.5.5.1 · goal:g7.16.1.5.5.2 · goal:g7.16.1.5.5.7 · applying guard-init on the box (the Prime, sudo)

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 20:5xZ 09-30: LANDED 627c94a040 by sanctuary-master (tip 6b444e66f1; chain DG3.48 -> DH.DG3.50 -> DH.DG3.57 -> Sonnet 5.5 fix, reviews in the merge-up of 17:29Z); SM gate: first live run on MAIN data, sweep --dry-run + ram-main status byte-identical to HEAD, 0 errors; chain suite 7700 passed / 1 failed (the Prime skills_first_turn, not this range); 0 D; links 5543/0.
director-general-1 10-07 (goal:g1.41 PASS B4 demote, status complete -> active): this goal's own Target end-state names the one-shot recharge and its Falsifier 1 drives it; only the charge-routing half landed (627c94a040). The recharge half was split to goal:g7.16.1.5.5.6.1 (active: mur g7556 measured its first build unsafe). complete again when .1 lands and Falsifier 1 holds for both halves; the landing record above is unchanged.
<!-- THOUGHT:END -->
