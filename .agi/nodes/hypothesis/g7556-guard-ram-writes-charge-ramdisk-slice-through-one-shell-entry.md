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
testable_claim: mem_cap.py ram-exec wraps argv via locations.ram_write_argv; every RAM-bound write in ram-main.sh and session-sweep.sh goes through it and no disk-bound write does; mem_cap.py ram-recharge rewrites files as copy+rename inside the same scope, bytes and mode kept
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
config-max: none -- RAM_SLICE and GUARD_RAM_DIR already live in config:guard; no new cell / template-max: none / code: the `ram-exec` + `ram-recharge` verbs (the trigger a shell script lacks) and the two scripts' call sites.

## FALSIFIERS
- F1: a test runs ram-main.sh's RAM-bound rsync and session-sweep.sh's move into a RAM-dir fixture with a FAKE `systemd-run` first on PATH (records its argv, then runs the tail): any write into the fixture RAM dir without the ramdisk.slice scope argv = false.
- F2: the same fake shows a DISK-bound write wrapped = false (only RAM-bound writes are charged there).
- F3: `ram-recharge` on a dummy tree changes any file's bytes or mode, or runs outside the scope argv = false.
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

## CORRECTIVE DH.DG3.48 -- closes mur-season2-loops-hypothesis-g7556-guard-ram-write-a00-60331ee3 g7556 (demote: 11 upheld + 3 missed)
BASE      CUT FROM season2/loops/hypothesis-g7556-guard-ram-write-a00-60331ee3 tip 157112b53e (worktree under the RAM-disk cell). No merge. Never rebase.
SPLIT     the recharge is OUT of this round: remove the `ram-recharge` verb and _RECHARGE_SRC; goal:g7.16.1.5.5.6.1 carries it (mount crossing, open writes, mtime, hardlinks, tempfile, fail-open exit). CLAIM (3) moves there.
1. ONE rule for "this path is on the tmpfs" -- ram-main.sh ramw is unconditional, session-sweep.sh keys on "$RAM_DIR"/* which never matches the real RAM tree (MAIN is overmounted) -- one shell function, defined once (a sourced snippet or the mem_cap entry deciding it), that asks the FILESYSTEM (findmnt/stat -f: tmpfs) for the destination's mount, never a path prefix; both scripts call it.
2. every write INTO the tmpfs in ram-main.sh goes through it -- bind_in's mkdir/touch into $RAM and `mkdir -p "$RAM"` included; a disk-bound write is untouched by rule, not by call-site luck.
3. the cutover never aborts on the scope -- ram-main.sh `up` runs in a unit ordered before the user manager: when `systemd-run --user` is unreachable, mem_cap's entry runs argv UNWRAPPED (exit code = argv's) and says so once on stderr; a row drives the entry with a failing fake systemd-run and sees argv run.
4. tests that can fail -- F1b places src on disk and dest on the tmpfs stand-in (and the reverse); the snippet loader cannot fall through into the whole script (extract by an explicit end marker, or source a split-out function file); a row drives ram-main.sh `up`'s RAM-bound writes with fakes for mount/sudo/findmnt/systemd-run (never real ones).
5. `ram-exec` with no `--` or an empty argv exits 2 by name; the dead `return 127` goes.
6. evidence at YOUR final tip, pasted, plus a labelled two-operand numstat 157112b53e..<tip before the paste commit>: python3 -m pytest extensions/agi/tests/test_ram_write_charge.py extensions/agi/tests/test_ram_worktrees.py extensions/agi/tests/test_box_guard.py extensions/agi/tests/test_guard_init_cells.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/dh348
DEMOTED (no work): ram-tier.sh (out of claim wording, refuted) · two-spellings (refuted; item 1 makes it one anyway) · the parent's kids=[] harvest line (refuted as a node defect; engine row on goal:g7.33.19)
SAFETY    NEVER run ram-main.sh, session-sweep.sh or guard-init.sh for real; never the live RAM dir, a real mount, sudo, a real systemd unit or crontab -- fakes on PATH in tmp dirs only
ANON      no user name, home or repo path value, host, IP or hardware name in any output, node, test, commit or dm
FILE SCOPE extensions/agi/bin/mem_cap.py · extensions/agi/guard/ram-main.sh · extensions/agi/guard/session-sweep.sh · extensions/agi/tests/test_ram_write_charge.py · the kid's own experiment node. NEVER guard-init.sh.
CEILING   HARD CAP, WHOLE CHAIN vs the round base 2b837f66b8: 1 kid · mem_cap.py <= 35 added lines (the recharge removal pays for items 3 + 5) · the two scripts <= 16 changed lines together · tests <= 200 · comments count · pi-free tier-0 · 0 USD -- over it = the round is cut
PARENT    paste FILE SCOPE, SAFETY, ANON and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.DG3.50 -- closes the DG3.48 parent review (a00-4be37f6b: kid a00-46137558 demoted to inconclusive_lean_proved:70)
BASE      CUT FROM season2/loops/hypothesis-g7556-guard-ram-write-a00-4be37f6b tip 1e8e34c555 (worktree under the RAM-disk cell). No merge. Never rebase.
1. the cutover never aborts on the scope -- REFUTED by parent probe P4: mem_cap.py ram-exec os.execvp's the scoped argv, so a failing systemd-run --user means argv NEVER runs (rc 1) -- decide reachability BEFORE wrapping (the user manager's bus/socket for this uid, one check, in mem_cap.py): unreachable -> exec argv UNWRAPPED with ONE stderr line; reachable -> the scope. A row drives a FAILING fake systemd-run on PATH with the user manager reported unreachable and sees argv run (its output + rc), never a forced flag.
2. fstype_at never raises -- a mountinfo line without the ` - ` separator raises ValueError -- skip malformed lines; a row with one.
3. tests to size -- test_ram_write_charge.py is 332 lines vs the chain cap 200 -- fold duplicated fixtures and parametrize; the file ends <= 220 lines with every falsifier row kept.
4. evidence at YOUR final tip, pasted, + a labelled numstat 1e8e34c555..<tip before the paste commit>: python3 -m pytest extensions/agi/tests/test_ram_write_charge.py extensions/agi/tests/test_ram_worktrees.py extensions/agi/tests/test_box_guard.py extensions/agi/tests/test_guard_init_cells.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/dh350
SAFETY    NEVER run ram-main.sh, session-sweep.sh or guard-init.sh for real; never the live RAM dir, a real mount, sudo, a real systemd unit or crontab -- fakes on PATH in tmp dirs only
ANON      no user name, home or repo path value, host, IP or hardware name in any output, node, test, commit or dm
FILE SCOPE extensions/agi/bin/mem_cap.py · extensions/agi/tests/test_ram_write_charge.py · the kid's own experiment node
CEILING   HARD CAP for THIS round (cut..tip): 1 kid · mem_cap.py NET <= +6 lines · the test file ends <= 220 lines · pi-free tier-0 · 0 USD -- over it = the round is cut
PARENT    paste FILE SCOPE, SAFETY, ANON and CEILING verbatim into every kid brief; COMMIT every kid edit AND merge the kid branch into the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.DG3.48: mur g7556 demote -- the recharge split to goal:g7.16.1.5.5.6.1 (unsafe: mount crossing, lost open writes); ONE filesystem-asked tmpfs rule for both scripts; every RAM-bound write wrapped; the cutover never aborts on an unreachable user manager; tests that can fail
<!-- THOUGHT:END -->
