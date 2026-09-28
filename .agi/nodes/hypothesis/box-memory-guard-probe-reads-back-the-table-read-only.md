---
id: hypothesis:box-memory-guard-probe-reads-back-the-table-read-only
mint_id: 5e3a6807daa74b168e958d91a41dc361
type: hypothesis
parents:
  - goal:g7.33.18.3
next_edges: []
edited_by: director-engine
scaffold_hash: 1574804fe93d69df
season: 2
testable_claim: "boxkit probe.py prints g7.33.18's table (this box vs SIZING, ok|drift) using only file reads and systemctl show, never a write, and exits non-zero naming each drifting row (assigned: director-engine)"
title: Box memory guard probe reads back the table read only
town: core
---
# hypothesis:box-memory-guard-probe-reads-back-the-table-read-only

## Measured
- goal:g7.33.18 (TMM.265, OWNER 20:4xZ): the box-level memory-watch pieces live only on local-town, hand-installed; encryption-town must install the same stack sized to its RAM from ONE kit in the repo. The node's table lists every piece and its measured value on local-town (15932 MiB RAM, 4095 MiB swap).
- Config cells committed by the director at 3b42eb930: paths.boxkit.{templates_dir, install_root, sbin_dir, systemd_system_dir, systemd_conf_dir, user_systemd_dir, watchdog_conf}.

## CLAIM
extensions/agi/boxkit/probe.py is READ-ONLY: it prints goal:g7.33.18's table for the box it runs on (layer · value on this box · value SIZING wants · ok|drift), reading files under install_root and `systemctl show -p <prop>` (system and --user) -- never a write, never sudo, never a unit change -- and exits non-zero naming every drifting row; mem_cap.systemd_run_usable(cfg) is one row.

## Dispatch line
config-max: every path is a paths.boxkit cell, every sized knob a values.boxkit cell (the director commits them) / template-max: the pieces themselves ARE templates / code: probe.py (the reads + the table) reusing the SIZING function once g7.33.18.2 lands; until then a local sizing call the harvest will dedupe -- name it in THOUGHT.

## FALSIFIERS
- the probe writes any file or calls systemctl with anything but show / is-active;
- a drift in a fixture (e.g. MemoryHigh off by one) exits 0;
- run read-only on this box, a row the node's table measured is missing.

## TESTS
extensions/agi/tests/test_boxkit_probe.py: tmp install_root fixture + stubbed systemctl show; rows: clean table exit 0, one drift exits 1 naming the row, a recording shim proves only read verbs are called. The one LIVE read-only run on this box goes in the experiment node as evidence (no test runs live).

## FILE SCOPE
extensions/agi/boxkit/probe.py · extensions/agi/tests/test_boxkit_probe.py · extensions/agi/tests/fixtures/boxkit_probe/**. Never .agi/config.json.

## CEILING
<= 3 kids · <= 12 production lines per conjunct where code is new logic (template bytes do not count) · pi-free tier-0 · 0 USD.

## THE KIT CONTRACT (shared by g7.33.18.1/.2/.3 -- fixed by the director; a change is a [rule] line to the director, never a local edit)
- Templates live under the cell `paths.boxkit.templates_dir` (repo-relative), one file per live piece, `{{UPPER_SNAKE}}` placeholders for every SIZED value and every host-specific token.
- `<templates_dir>/manifest.json` = {"pieces": [{"name", "template" (relative to templates_dir), "dest_cell" (a key of paths.boxkit: sbin_dir | systemd_system_dir | systemd_conf_dir | user_systemd_dir | watchdog_conf), "dest_rel" (under that dir; "" when dest_cell names a file), "mode" (octal string), "sudo" (bool), "placeholders" [names], "reload" ("system" | "user" | "none")}]}.
- Every destination = install_root (cell paths.boxkit.install_root, "/" live, a tmp dir in every test) joined with the dest_cell value (`{home}` expanded) and dest_rel. NO literal path anywhere in code.
- SIZING (goal:g7.33.18): (g7.33.18 v2, 9b03554ac) user@ MemoryMax = MemTotal - held_outside_user - the box's MEASURED system reserve (an INPUT per box: local-town ~1.9 GiB, encryption-town 942 MiB -- never a fixed 2 GiB; the installer takes it as a flag/cell, the probe derives it from the installed MemoryMax) · MemoryHigh = 0.9 x MemoryMax · MemorySwapMax = 0.5 x swap · agi.slice MemoryHigh / MemoryMax = 0.63 / 0.70 x user@ MemoryMax (reproduces 4639/5155 MiB on local-town) -- the numeric knobs are cells under values.boxkit.* the director commits; name any you need in THOUGHT.
- FENCES (every round, every kid): NEVER run an install for real on this box -- no sudo, no systemctl start/stop/enable/daemon-reload, no write under /etc, /usr, ~/.config/systemd, no crontab write. Reading live files and `systemctl show` read-only is allowed. Every test uses a tmp install_root and a stubbed systemctl. Copied bytes pass `python3 extensions/agi/bin/anonymize.py check`: a host name, address, hardware name or key id becomes a placeholder. Every pytest `timeout 600 prlimit --nproc=300`, named files, --basetemp under /tmp; no test spawns pytest; kids never launch real claude.
- The director commits .agi/config.json cells; a round NEVER does (cli.py refuses it) -- write the cells you need in THOUGHT with their values.
