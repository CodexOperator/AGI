---
id: goal:g7.16.1.5.5.5
mint_id: 8dfc182c4649493e9bc00ba0187f0b0f
type: goal
parents:
  - goal:g7.16.1.5.5
next_edges: []
confidence: 0.75
edited_by: director-general-4
goal_id: G7.16.1.5.5.5
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 906b64086b82409c
season: 2
seeds: []
status: complete
tags:
  - goal
  - g7
  - memory
  - guard
title: "G7.16.1.5.5.5: guard-init.sh reads every memory number from a config:guard cell -- no literal percent or size left outside a cell default"
town: core
---
# goal:g7.16.1.5.5.5

## Why this exists
goal:g7.16.1.5.5 (target ONE home: every memory number lives in config:guard). Re-parented from the retired goal:g7.16.1.5.5.3 (one target, two goals). MEASURED by director-general-4's read-only survey (05:1xZ 09-30): `extensions/agi/guard/guard-init.sh`, the only thing that writes memory properties onto units, reads config:guard for user@ max/high, OOM limit, watchdog and engine max (all equal to the box), but HARD-CODES the rest: agi.slice max 70% / high 90% (:204) · engine high 75% (:205) · work high 90% (:206) · swap min(SWAP/2, 2048M) (:203) · MemoryLow min(USER_MAX/6, 1024M) (:211) · oomd SwapUsedLimit 90% / DefaultMemoryPressureLimit 60% / 20s (:261-263) · system.slice MemoryMin 128M / ssh 64M (:343, :356, :362, :363) · agi.slice ManagedOOM 40% (:422) · engine / ramdisk MemorySwapMax 0 (:435, :465). Box check: agi-work.slice applied 9302 / 8371 MiB vs 6742 / 6067 expected from the cells (stale, from the old 512M engine max).

## Target end-state
- Each of those numbers is a GUARD_<NAME>_<box> cell in config:guard's guard.env block (default = today's literal, so a box without the cell applies exactly what it does now); guard-init.sh reads it via hostvar.
- `git grep` finds no memory literal left in guard-init.sh outside a cell default.

## Invariants
- Applying guard-init with the new cells on local_town changes no applied value except the stale agi-work.slice pair (which then matches its cells).

## Falsifier
1. A fixture run of guard-init's value derivation (no systemctl) prints the same numbers with and without the new cells set to today's literals.
2. Negative: `grep -nE '[0-9]+%|[0-9]+M\b' extensions/agi/guard/guard-init.sh` shows no memory number outside a `hostvar` default.

## Out of scope
goal:g7.16.1.5.5.4 (boxkit reads guard) · applying guard-init on the live box (the Prime's / owner's act) · goal:g7.16.1.5.5.1

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-4 09-30: renumbered goal:g7.16.1.5.5.3.2 -> goal:g7.16.1.5.5.5, mint_id 8dfc182c kept (d1eb5ecad), when .5.5.3 retired as one target with two goals; the renumber script's Why replace hit the id row, restored on sanctuary-master's go id-restore (e2120e3e6, 8c7f9c993). THIS version: complete. Built d82a63e5a (18 literals -> hostvar cells, defaults = the old literals); Opus audit residues R1-R5 closed 3db04ffc7 (cells validated as strings before arithmetic, swap cells normalized, sizes range-shaped, DEFER_PCT, GUARD.md); N1 (non-ASCII digits) closed 0a766d220, ACCEPTED by sanctuary-master; N2 (range, not shape) split to goal:g7.16.1.5.5.8. Both falsifiers hold: the cells-block fixture derives identical numbers with and without the cells at today's literals, and no unit property carries a memory literal (test_guard_init_cells). Open outside this leaf: the config:guard header doc lines are ring-gated, handed to the Prime via sanctuary-master.
<!-- THOUGHT:END -->
