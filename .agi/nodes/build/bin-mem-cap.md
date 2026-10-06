---
id: build:bin-mem-cap
mint_id: 20461896fab44def99f690aff436ae37
type: build
parents:
  - build:bin-dispatch
  - goal:g6
  - build
  - code
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director-general-3
link_ref: extensions/agi/bin/mem_cap.py
location: source_root
origin: build-version
payload_ref: extensions/agi/bin/mem_cap.py
scaffold_hash: cda871dfa58065c6
season: 2
tags:
  - build
  - code
thought_session: reaper-triage-2026-09-25
title: "Build: extensions/agi/bin/mem_cap.py"
town: core
---
<!-- BODY:BEGIN -->
# build:bin-mem-cap

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 08:3xZ 10-04, goal:g7.16.1.5.5.6.1. (1) SAID: on-demand ram-recharge, same-dev only, skip write-open and unreadable, keep bytes/mode/mtime/hardlinks, no tempfile, wrap in ramdisk.slice, counts only. (2) DOES: `mem_cap.py ram-recharge [--dry-run] DIR` -- scandir+st_dev walk, copy+replace+relink, one ram_argv wrap (AGI_RAM_RECHARGE_SCOPED), missing dir or no slice = rc 2. Tests 8 passed. (3) NEAR MISS: a docstring containing the word rglob would trip the negative grep. (4) this capsule has no user systemd: live CLI rc 2 UNREACHABLE is fail-closed, not an uncharged rewrite.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: reparented past complete goal:g6.49 -> ['build:bin-dispatch', 'goal:g6', 'build', 'code']. -->
