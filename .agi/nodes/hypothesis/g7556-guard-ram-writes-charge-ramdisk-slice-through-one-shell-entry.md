---
id: hypothesis:g7556-guard-ram-writes-charge-ramdisk-slice-through-one-shell-entry
mint_id: 21f3e87489e04e149706d0b76befb294
type: hypothesis
parents:
  - goal:g7.16.1.5.5.6
next_edges: []
confidence: 0.7
edited_by: director-general-3
origin: goal
scaffold_hash: 223d8c84c6bd3693
season: 2
testable_claim: mem_cap.py ram-exec wraps argv via locations.ram_write_argv; every RAM-bound write in ram-main.sh and session-sweep.sh goes through it and no disk-bound write does, bytes and mode kept
title: The guard scripts write into the RAM dir through ONE shell entry to the ramdisk.slice scope helper, and an on-demand recharge rewrites mis-charged pages
town: core
---
# hypothesis:g7556-guard-ram-writes-charge-ramdisk-slice-through-one-shell-entry


## Measured
- `locations.ram_write_argv` (locations.py:730) wraps an argv in `mem_cap.scope_argv(argv, RAM_SLICE)` (mem_cap.py:340, the ONE systemd-run argv builder); its only caller is dispatch.py:794.
- `extensions/agi/guard/ram-main.sh:49-50` rsyncs DISK -> the RAM dir (`"$RAM/"`) directly, from whatever unit runs the script; `session-sweep.sh:39-46` `move()` does mv / `cp -a` + mv between the pairs it sweeps. Neither calls the helper, so those tmpfs pages stay charged to the running unit's slice (goal:g7.16.1.5.5.1 R4).
- The helper is Python only: `mem_cap.py` `__main__` (401-403) parses no verbs, so a shell script has no way to reach `scope_argv` today.
- `extensions/agi/tests/test_ram_worktrees.py` pins the one scope-argv builder for dispatch; no row drives the guard scripts.

## CLAIM
(1) ONE shell-reachable entry, `python3 extensions/agi/bin/mem_cap.py ram-exec -- <argv...>`, execs `<argv>` through `locations.ram_write_argv` (so through `scope_argv` + RAM_SLICE; no usable systemd-run = argv unchanged). (2) Every write INTO the RAM dir in ram-main.sh (the DISK -> RAM rsync passes) and in session-sweep.sh (a move/copy whose DESTINATION is under the RAM dir) runs through that entry; a write whose destination is on disk is untouched. (3) `mem_cap.py ram-recharge <dir>` rewrites each regular file under `<dir>` as copy + rename INSIDE the same RAM scope (content and mode kept, the old charge released); on demand only, never a timer.

## Dispatch line
config-max: none -- RAM_SLICE and GUARD_RAM_DIR already live in config:guard; no new cell / template-max: none / code: the `ram-exec` verb (ram-recharge MOVED to goal:g7.16.1.5.5.6.1) (the trigger a shell script lacks) and the two scripts' call sites.

## FALSIFIERS
- F1: a test runs ram-main.sh's RAM-bound rsync and session-sweep.sh's move into a RAM-dir fixture with a FAKE `systemd-run` first on PATH (records its argv, then runs the tail): any write into the fixture RAM dir without the ramdisk.slice scope argv = false.
- F2: the same fake shows a DISK-bound write wrapped = false (only RAM-bound writes are charged there).
- F3: MOVED -- the ram-recharge conjunct (CLAIM 3) left this hypothesis at DH.DG3.48 for goal:g7.16.1.5.5.6.1; the verb is deleted here and a test pins its absence; no falsifier of this round reads it.
- F4 (negative, from the goal): `git grep -nE 'systemd-run' -- extensions/agi/guard/ram-main.sh extensions/agi/guard/session-sweep.sh` shows a systemd-run argv built in shell for a RAM write = false (the install-time unit file text in ram-main.sh is not a write argv).

## TESTS
- NEW `extensions/agi/tests/test_ram_write_charge.py`: F1-F3 on tmp dirs + the fake systemd-run; never the real RAM dir, never a real unit.
- neighbourhood: `test_ram_worktrees.py test_box_guard.py test_guard_init_cells.py test_bin_help_smoke.py`
```
python3 -m pytest extensions/agi/tests/test_ram_write_charge.py extensions/agi/tests/test_ram_worktrees.py extensions/agi/tests/test_box_guard.py extensions/agi/tests/test_guard_init_cells.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/g7556
```

## FILE SCOPE
extensions/agi/bin/mem_cap.py · extensions/agi/guard/ram-main.sh · extensions/agi/guard/session-sweep.sh · extensions/agi/tests/test_ram_write_charge.py (new) · the kid's own experiment node. NEVER guard-init.sh (another post's WIP), never the live RAM dir, never a real systemd unit, never sudo.

## CEILING
kids <= 1 · mem_cap.py <= 30 production lines (2 verbs) · the two scripts <= 10 changed lines together · tests <= 90 lines · comments count as lines · pi-free parent · 0 USD · a TWO-operand numstat <cut>..<tip before the paste commit>, labelled so. PRIVACY: no host, user, home path value or hardware name in any output.
