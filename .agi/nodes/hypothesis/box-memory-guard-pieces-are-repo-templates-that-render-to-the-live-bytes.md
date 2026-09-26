---
id: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
mint_id: 8d3f4fbac3104be29da7e895a6c95a34
type: hypothesis
parents:
  - goal:g7.33.18.1
next_edges: []
edited_by: director-engine
scaffold_hash: d1bd18074c8a2550
season: 2
testable_claim: "every piece of goal:g7.33.18's table is a template + manifest entry under paths.boxkit.templates_dir that renders to the live local-town bytes, with no literal host/path and anonymize clean (assigned: director-engine)"
title: Box memory guard pieces are repo templates that render to the live bytes
town: core
---
# hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes

## Measured
- goal:g7.33.18 (TMM.265, OWNER 20:4xZ): the box-level memory-watch pieces live only on local-town, hand-installed; encryption-town must install the same stack sized to its RAM from ONE kit in the repo. The node's table lists every piece and its measured value on local-town (15932 MiB RAM, 4095 MiB swap).
- Config cells committed by the director at 3b42eb930: paths.boxkit.{templates_dir, install_root, sbin_dir, systemd_system_dir, systemd_conf_dir, user_systemd_dir, watchdog_conf}.

## CLAIM
Every piece in goal:g7.33.18's table (user@ / oomd / user.slice / user-UID.slice / system.slice drop-ins, agi.slice, agi-memguard.py + agi-memguard.service, the 10-agi-survival no-cascade drop-ins, watchdog.conf + sanctuary-health) is a template under paths.boxkit.templates_dir with manifest.json per the KIT CONTRACT; rendering each with local-town's measured values reproduces the live file byte-for-byte; no template carries a literal host, address, hardware name or path; anonymize check is clean.

## Dispatch line
config-max: every path is a paths.boxkit cell, every sized knob a values.boxkit cell (the director commits them) / template-max: the pieces themselves ARE templates / code: manifest.json + a tiny render helper (placeholder substitution, refuses an unfilled placeholder by name).

## FALSIFIERS
- a rendered template differs from the live file it was copied from (the test fixture holds the live bytes with host tokens already replaced);
- anonymize.py check flags a template;
- a template contains an unlisted placeholder, or a manifest placeholder the template never uses.

## TESTS
extensions/agi/tests/test_boxkit_templates.py: render every piece against a committed fixture of local-town's measured values and diff against a committed ANONYMIZED copy of the live bytes; manifest schema row; unfilled-placeholder refusal row. + test_anonymize*.py neighbourhood.

## FILE SCOPE
extensions/agi/boxkit/** (templates, manifest.json, render helper) · extensions/agi/tests/test_boxkit_templates.py · extensions/agi/tests/fixtures/boxkit/**. Never .agi/config.json.

## CEILING
<= 3 kids · <= 12 production lines per conjunct where code is new logic (template bytes do not count) · pi-free tier-0 · 0 USD.

## THE KIT CONTRACT (shared by g7.33.18.1/.2/.3 -- fixed by the director; a change is a [rule] line to the director, never a local edit)
- Templates live under the cell `paths.boxkit.templates_dir` (repo-relative), one file per live piece, `{{UPPER_SNAKE}}` placeholders for every SIZED value and every host-specific token.
- `<templates_dir>/manifest.json` = {"pieces": [{"name", "template" (relative to templates_dir), "dest_cell" (a key of paths.boxkit: sbin_dir | systemd_system_dir | systemd_conf_dir | user_systemd_dir | watchdog_conf), "dest_rel" (under that dir; "" when dest_cell names a file), "mode" (octal string), "sudo" (bool), "placeholders" [names], "reload" ("system" | "user" | "none")}]}.
- Every destination = install_root (cell paths.boxkit.install_root, "/" live, a tmp dir in every test) joined with the dest_cell value (`{home}` expanded) and dest_rel. NO literal path anywhere in code.
- SIZING (goal:g7.33.18): (g7.33.18 v2, 9b03554ac) user@ MemoryMax = MemTotal - held_outside_user - the box's MEASURED system reserve (an INPUT per box: local-town ~1.9 GiB, encryption-town 942 MiB -- never a fixed 2 GiB; the installer takes it as a flag/cell, the probe derives it from the installed MemoryMax) · MemoryHigh = 0.9 x MemoryMax · MemorySwapMax = 0.5 x swap · agi.slice MemoryHigh / MemoryMax = 0.63 / 0.70 x user@ MemoryMax (reproduces 4639/5155 MiB on local-town) -- the numeric knobs are cells under values.boxkit.* the director commits; name any you need in THOUGHT.
- FENCES (every round, every kid): NEVER run an install for real on this box -- no sudo, no systemctl start/stop/enable/daemon-reload, no write under /etc, /usr, ~/.config/systemd, no crontab write. Reading live files and `systemctl show` read-only is allowed. Every test uses a tmp install_root and a stubbed systemctl. Copied bytes pass `python3 extensions/agi/bin/anonymize.py check`: a host name, address, hardware name or key id becomes a placeholder. Every pytest `timeout 600 prlimit --nproc=300`, named files, --basetemp under /tmp; no test spawns pytest; kids never launch real claude.
- The director commits .agi/config.json cells; a round NEVER does (cli.py refuses it) -- write the cells you need in THOUGHT with their values.
