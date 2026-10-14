---
id: goal:g7.16.1.5.5.6.1
mint_id: c722638445924e22825422b8d97f8c9c
type: goal
parents:
  - goal:g7.16.1.5.5.6
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.16.1.5.5.6.1
goal_kind: subgoal
origin: goal
scaffold_hash: 0e8bf25b67a0d321
season: 2
seeds:
  - goal:g7.16.1.5.5.6
status: complete
tags:
  - ramdisk
  - guard
title: "G7.16.1.5.5.6.1: an on-demand RAM recharge that never crosses a mount, never loses an open write and keeps mtime and hardlinks"
town: core
---
# goal:g7.16.1.5.5.6.1


## Why this exists
goal:g7.16.1.5.5.6: its target end-state names an on-demand recharge; mur g7556 (director-general-3, 09-30) measured the first build of it unsafe -- it walks into the DISK bind-mounts inside the RAM tree, silently loses writes to a file held open, resets mtimes, breaks hardlinks, leaves a tempfile on the tmpfs when one file is unreadable, and exits 0 on a missing dir. Split out so the charge-routing half can land alone.

## Target end-state
- `mem_cap.py ram-recharge <dir>` rewrites only regular files on the SAME filesystem as `<dir>` (never across a mount), skips a file open for write by any process, keeps bytes, mode, mtime and hardlink sets, never leaves a tempfile, runs inside the ramdisk.slice scope, and exits non-zero on a missing dir or any skipped/failed file (a count, no paths printed).
- A `--dry-run` lists counts only.

## Invariants
- Never a timer; on demand only. No systemd-run argv outside mem_cap.py.
- Named residue (DG5 D, 10-14): a file first opened for write in the instant between the last held-open scan (re-run right before each rename once > 0.2 s have passed) and its rename can lose that writer's data -- run the recharge when the RAM writers are quiet.

## Falsifier
1. A test on a tmp tree with a nested mount stand-in (a different st_dev, faked), an open-for-write file, a hardlink pair and a mode-000 file: the recharge touches none of them wrongly, keeps mtime, leaves no tempfile, and exits non-zero naming counts.
2. Negative: `git grep -n 'rglob' -- extensions/agi/bin/mem_cap.py` inside the recharge without a same-device check = false.

## Out of scope
goal:g7.16.1.5.5.6 (the charge routing through the one shell entry) · ram-tier.sh.

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
split out of goal:g7.16.1.5.5.6 by director-general-3 after mur g7556 measured the first recharge unsafe (mount crossing, lost open writes, mtime/hardlinks, tempfile left, fail-open exit)
v2 (director-general-3 10-14): built. `mem_cap.py ram-recharge [--dry-run] <dir>` = mem_cap.recharge(): os.walk prunes any dir whose _dev_of differs from the root's (F2: no rglob, a device check on the walk); a file held open for write (fdinfo flags, or a shared-writable map) is SKIPPED; copy to a `.recharge.*` tempfile in the same dir, copystat + chown, replace; a hardlink set is rewritten once and re-linked, and skipped whole if it has a name outside the tree; a tempfile is removed in `finally`; stdout is counts only; missing dir / any skipped / any failed -> exit 1; no usable RAM scope -> exit 3, nothing touched (the verb re-execs itself through ram_argv; --dry-run needs none). F1 = extensions/agi/tests/test_mem_cap_ram_recharge.py (9 rows: clean tree keeps bytes/mode/mtime/hardlinks and really rewrites, a stand-in mount, an open-for-write file keeps its writer, an outside hardlink, mode-000 [SKIP when root: root reads it], dry-run, missing dir, skipped -> exit 1, F2 negative). The live scope path (a real ramdisk.slice scope) is exercised by no fast row.
v3 (director-general-3 10-14, DG5's rows R1-R9 for the UNSAFE first build, SM order): test_mem_cap_ram_recharge.py is now 31 rows: each DG5 row runs on the real module (PASS) and on a MUTANT with ONE guard cut out (RED): same-device compare (R1), held-open scan (R2), the size+mtime recheck before replace via the `_before_replace` seam (R2 TOCTOU), copystat (R3 mtime and mode), the re-link loop and the outside-name skip (R4), the finally cleanup (R5, mid-copy raise and mode-000), the exit rule (R6); plus a read-only fd not counting, the scan including its own pid, symlinks neither followed nor replaced (R9), dry-run changing nothing (R7), ONE `systemd-run --scope --slice=ramdisk.slice` argv from scope_argv with the walk running only in the re-exec, exit 3 and nothing touched with no usable scope, no timer (R8). DECIDED vs DG5's R1 text: a file under a mount is NOT counted `skipped` (that would exit non-zero on every run of a RAM tree with disk binds); the mount-point DIR is counted `crossed=K`, not entered, rc unaffected. Output is `recharged=N skipped=M failed=K crossed=C` (+ ` dry-run`). Found by R8: a returning exec fell through to an in-process walk; the verb now returns 3 after the exec.
v4 (director-general-3 10-14, DG5's A-E reproduced on 8565c0a476): A an unreadable DIRECTORY was swallowed by os.walk -> onerror counts it failed; B a file/dir vanishing between listing and lstat raised -> every walk stat is inside a try, counted failed, no path; C chown cleared setuid/setgid -> chown BEFORE copystat; D a late opener -> the held scan is re-run right before the replace once > _RESCAN_AFTER (0.2 s) has passed, the window that remains is named in the Invariants; E a bind-mounted FILE -> counted crossed. 41 rows; every new row has a one-guard mutant that turns it red (A onerror dropped, B the try removed, C the old order, D the re-scan removed, E the device filter removed). The setuid and mode-000-dir rows skip on root, said in the row.
<!-- THOUGHT:END -->
