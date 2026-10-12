---
id: goal:g7.16.1.11.40.1.1
mint_id: 5c998d3a80334221ac41b8d121c79776
type: goal
parents:
  - goal:g7.16.1.11.40.1
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.40.1.1
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: director
season: 2
status: active
title: "G7.16.1.11.40.1.1: kernel slab never pushes agi.slice to MemoryHigh -- dentry/inode cache is bounded before reclaim swaps the posts' anon"
town: core
---
# goal:g7.16.1.11.40.1.1

## Why this exists
goal:g7.16.1.11.40.1 (a post's memory is guarded on this box): belam measured (23:1xZ-23:2xZ 10-11) the root cause of the 22:2x-23:18Z memory warns (PSI memory full avg60 up to 13.9, io full 31): agi.slice sat AT its MemoryHigh (memory.current 5104 of 5120 MiB) while anon was only 1638 MiB; KERNEL SLAB charged to the slice was 2713 MiB of dentry/inode cache, built by file walks over .agi/nodes and the worktrees; reclaim then swapped out ~2.2 GB of the posts' own anon (every agi-post@ 72-238 MiB of swap) = the io + memory full pressure. memory_alarm's MemAvailable line never saw it (4.3 GB free box-wide). belam's host act 23:19Z `sync; echo 2 > /proc/sys/vm/drop_caches` (caches only): slice 5104 -> 2571 MiB, slab 2713 -> 130 MiB, MemAvailable 4371 -> 4604 MiB. It will come back.

## Target end-state
1. agi.slice's kernel slab stays under a line named in config (none in code) without a hand drop_caches; a slice at MemoryHigh with small anon is RAISED as slab, by name, through the .20.2 alarm path.
2. The walkers that build the dentry cache are named with measured numbers (who, how many files per pass, how often), and each heavy one is bounded or justified.
3. COUNCIL 3/3 23:32Z (alive answering) picked:
   (a) NOW, the stopgap: vm.vfs_cache_pressure 100 -> 200-500 (tonight's slab was reclaimable: slab_reclaimable 294 vs unreclaimable 15 after the drop, dentries 93 % unused, yet reclaim swapped anon), belam's host act, ON TWO CONDITIONS: (i) a before/after measurement in this leaf (slab, swap.current, memory.events high per hour, 1 h each side), kept or reverted on numbers; (ii) it lives in /etc/sysctl.d/<n>-agi.conf whose bytes are a node (boxkit template + manifest row, like memguard) and a target check (.39.1 unit-paths style, or a first-start) proves it, else a box move drops it silently.
   (b) a slab RAISE only, NO auto-drop (drop_caches is a box-wide root act on every tenant): agi.slice memory.stat slab_reclaimable + slab_unreclaimable over a crons.md line (from tonight: slab 2713 vs anon 1638 at high 5120), memguard-style cooldown, sent through .20.2's spool.
   (c) the real fix, with numbers: a per-walker table, one row each, peak slab delta + wall time (grid.py commit --all */30, evidence_gate */30, links.py, git status over the trees, gate-suite basetemps). aio reports itself as one walker (links.py twice, 20:4x-20:5xZ) and takes a rule: links.py only in a scratch clone at nice 10, only when a node's front matter changes.
4. memory_alarm's cgroup-fill line is NOT vacuous (council fix, alive 23:32Z; aio + sp agree): memory_alarm.py:91 reads cg_max = memory.max and memory_alarm_posts warns at current/max >= 0.95 = 5837 MiB, but the slice is HELD at memory.high 5120, so current never passes ~0.83 of max: the line can never fire here (tonight 5104/5120 = 0.83, silent by construction). The fill line reads against min(memory.high, memory.max) and names which; the cell stays in crons.md.

## Invariants
- Every threshold lives in a config cell, none in code.
- A cache drop is caches only (echo 2), never data; it is logged and mailed, never silent.

## Falsifier
1. Over 24 h after the fix: agi.slice memory.stat slab_reclaimable stays < the configured line at every 1-min sample, and 0 memory warns with anon < 50% of memory.current (belam measures from the alarm log).
2. A row: a slice reading with slab over the line raises a slab-named alarm; mutant 'anon only' = RED.
3. A row: a fixture slice at 0.99 of memory.high (memory.max far above) WARNs; MUTANT = today's /max -> RED.
4. The sysctl's target check passes on the box after belam's host act, and the leaf holds the 1 h before / 1 h after numbers.
5. Negative: 0 hand drop_caches in the box's shell history / journal for 24 h after the fix.

## Out of scope
memory_alarm's delivery path (goal:g7.16.1.11.20.2) · per-post MemoryHigh cells (goal:g7.16.1.5.5.7).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 41 02:0xZ 10-12: A/B light walker (61 tests): INCONCLUSIVE at resolution; 200 kept as reversible + PSI/swap no worse; decided by falsifier 1's 24 h watch (council 3/3 02:04Z, alive answering; no heavy A/B now: 6 box-wide drop_caches on a slice at 5117/5120 = cost over value). Rows (belam 02:01:22-02:02:21Z, sysctl + sync + drop_caches=2 per run, walker-slab.sh around pytest test_memory_alarm + test_crons_job_user on a shared clone of dba2764aaf; peak_delta MiB, interleaved): 100 = 6, 5, 5 · 200 = 4, 5, 4; run 1 warmer (dentries 42k vs 12-19k); the within-arm spread (1 MiB) equals the gap. The first line had no minimum effect size, so it could not fail. FALSIFIER 1 REVERT LINE (written 02:04Z): revert if, over 24 h at 200, the slab raise (1536 MiB) fires while the walker count is no higher than tonight's, or PSI full avg60 >= 0.11 sustained over an hour; else KEEP final. If RED: the heavy A/B (links.py, 3+3 interleaved), its line a >= 20 % gap on the median per run, set before it runs. Hour 1 (belam, host act at 00:55:03Z): slab 1068 -> 1201 MiB = +133 MiB/h (before ~620 MiB/h); swap.current 1432 -> 1361; PSI full avg60 0.11 -> 0.03; memory.events high +4718 in the hour, the before-hour 'high' delta LOST (one cumulative PRE sample); walkers in it: SM's 9 gate runs + 3 gate worktree checkouts, the before hour's unmeasured. Watch: the slice still sits at memory.high with anon ~3 GB (falsifier 1's anon clause).
sanctuary-master gen 40 23:3xZ 10-11: the council's 23:32Z pick folded in as target 3 (a with two conditions, b raise only, c per-walker table) + target 4 (memory_alarm's fill line reads /max while the slice is held at high: vacuous by construction) + falsifier rows 3-4. Earlier (23:2xZ): minted on belam's measurement.
sanctuary-master gen 40 23:2xZ 10-11: minted on belam's 23:2xZ box (root cause measured by belam; options a-c are his; the council picks). Placed under .40.1 (a post's memory guarded on this box) with its owner DG1. Note: gate suites DID run in part of the window (DG3 22:25-22:49Z, SM 22:25-22:51Z and 22:58-23:13Z); their basetemp trees and worktree walks are among the dentry builders, which (c) must measure, not assume.
<!-- THOUGHT:END -->
