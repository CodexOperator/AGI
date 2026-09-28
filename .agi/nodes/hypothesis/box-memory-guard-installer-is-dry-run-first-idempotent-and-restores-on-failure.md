---
id: hypothesis:box-memory-guard-installer-is-dry-run-first-idempotent-and-restores-on-failure
mint_id: be7ec50dac3c4696bae5b80dd57b2569
type: hypothesis
parents:
  - goal:g7.33.18.2
next_edges: []
edited_by: director-engine
scaffold_hash: c37b45768dbf9a51
season: 2
testable_claim: "boxkit install.py is dry-run by default, sizes from /proc/meminfo per g7.33.18 SIZING (reproducing local-town's measured numbers), records and restores every before-value on failure, and a second apply is a no-op; tested only under a tmp install_root (assigned: director-engine)"
title: Box memory guard installer is dry run first idempotent and restores on failure
town: core
---
# hypothesis:box-memory-guard-installer-is-dry-run-first-idempotent-and-restores-on-failure

## Measured
- goal:g7.33.18 (TMM.265, OWNER 20:4xZ): the box-level memory-watch pieces live only on local-town, hand-installed; encryption-town must install the same stack sized to its RAM from ONE kit in the repo. The node's table lists every piece and its measured value on local-town (15932 MiB RAM, 4095 MiB swap).
- Config cells committed by the director at 3b42eb930: paths.boxkit.{templates_dir, install_root, sbin_dir, systemd_system_dir, systemd_conf_dir, user_systemd_dir, watchdog_conf}.

## CLAIM
extensions/agi/boxkit/install.py renders the manifest's pieces sized by SIZING from the box's own /proc/meminfo (MemTotal, SwapTotal), DRY-RUN BY DEFAULT (prints path · before · after per piece, writes nothing); with --apply writes every piece under install_root, records every before-value first, restores ALL of them byte-for-byte on any failure, and a second --apply changes nothing; the sudo pieces are named and refused without privilege rather than half-installed.

## Dispatch line
config-max: every path is a paths.boxkit cell, every sized knob a values.boxkit cell (the director commits them) / template-max: the pieces themselves ARE templates / code: install.py (plan, apply, restore) and the SIZING function.

## FALSIFIERS
- dry-run writes any byte under the tmp root;
- a second --apply reports or writes a change;
- an injected failure after piece k leaves any earlier piece changed;
- SIZING over local-town's MemTotal/swap does not reproduce the node's measured numbers (7365/6628/2047 MiB user@; 5155/4639 MiB agi.slice).

## TESTS
extensions/agi/tests/test_boxkit_install.py: tmp install_root + a FIXTURE manifest and templates (this round does not wait on g7.33.18.1's real templates -- build against the contract), a fake /proc/meminfo, a stubbed systemctl recording calls; rows: dry-run no-write, apply, idempotent re-apply, injected-failure restore, sizing reproduces the measured numbers, sudo piece refused unprivileged.

## FILE SCOPE
extensions/agi/boxkit/install.py · extensions/agi/boxkit/sizing.py (if split) · extensions/agi/tests/test_boxkit_install.py · extensions/agi/tests/fixtures/boxkit_install/**. Never .agi/config.json, never the real templates dir (g7.33.18.1's scope).

## CEILING
<= 3 kids · <= 12 production lines per conjunct where code is new logic (template bytes do not count) · pi-free tier-0 · 0 USD.

## THE KIT CONTRACT (shared by g7.33.18.1/.2/.3 -- fixed by the director; a change is a [rule] line to the director, never a local edit)
- Templates live under the cell `paths.boxkit.templates_dir` (repo-relative), one file per live piece, `{{UPPER_SNAKE}}` placeholders for every SIZED value and every host-specific token.
- `<templates_dir>/manifest.json` = {"pieces": [{"name", "template" (relative to templates_dir), "dest_cell" (a key of paths.boxkit: sbin_dir | systemd_system_dir | systemd_conf_dir | user_systemd_dir | watchdog_conf), "dest_rel" (under that dir; "" when dest_cell names a file), "mode" (octal string), "sudo" (bool), "placeholders" [names], "reload" ("system" | "user" | "none")}]}.
- Every destination = install_root (cell paths.boxkit.install_root, "/" live, a tmp dir in every test) joined with the dest_cell value (`{home}` expanded) and dest_rel. NO literal path anywhere in code.
- SIZING (goal:g7.33.18): (g7.33.18 v2, 9b03554ac) user@ MemoryMax = MemTotal - held_outside_user - the box's MEASURED system reserve (an INPUT per box: local-town ~1.9 GiB, encryption-town 942 MiB -- never a fixed 2 GiB; the installer takes it as a flag/cell, the probe derives it from the installed MemoryMax) · MemoryHigh = 0.9 x MemoryMax · MemorySwapMax = 0.5 x swap · agi.slice MemoryHigh / MemoryMax = 0.63 / 0.70 x user@ MemoryMax (reproduces 4639/5155 MiB on local-town) -- the numeric knobs are cells under values.boxkit.* the director commits; name any you need in THOUGHT.
- FENCES (every round, every kid): NEVER run an install for real on this box -- no sudo, no systemctl start/stop/enable/daemon-reload, no write under /etc, /usr, ~/.config/systemd, no crontab write. Reading live files and `systemctl show` read-only is allowed. Every test uses a tmp install_root and a stubbed systemctl. Copied bytes pass `python3 extensions/agi/bin/anonymize.py check`: a host name, address, hardware name or key id becomes a placeholder. Every pytest `timeout 600 prlimit --nproc=300`, named files, --basetemp under /tmp; no test spawns pytest; kids never launch real claude.
- The director commits .agi/config.json cells; a round NEVER does (cli.py refuses it) -- write the cells you need in THOUGHT with their values.
