---
id: build:bin-mem-cap
mint_id: 20461896fab44def99f690aff436ae37
type: build
parents:
  - build:bin-dispatch
  - goal:g6.49
next_edges: []
build_kind: code
confidence: 1.0
edited_by: belam
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
Minted 2026-09-25 as the node this file should always have had, in the same act as the goal:g6.49 fix that made its absence matter. Shape is [build, goal] per context/schemas/[build].md -- build:bin-dispatch because mem_cap.py was extracted at 6d1362c10 (SM.112) as the shared memory-cap helper for dispatch.py's launch path (workflow.py is the second caller), and goal:g6.49 because that is why THIS version differs. The fix, goal:g6.49.1: systemd_run_usable() cached its verdict in a module global and so re-probed once per PROCESS, and since the probe's contract is an observed SIGKILL, every spawn paid one deliberate 256 MB allocation under a 64M cap, one cgroup OOM kill, and one anonymous failed run-<random>.scope nothing ever reset -- 1784 kills and 1422 resident failed units on encryption-town in 6 days. Now probed once per BOOT (cached in XDG_RUNTIME_DIR keyed on boot id), the scope carries a fixed --unit so it can be reset-failed by name, and AGI_MEMCAP_SYSTEMD_RUN forces the verdict outright. Enforcement semantics are deliberately unchanged.
<!-- THOUGHT:END -->
