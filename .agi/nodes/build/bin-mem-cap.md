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
NOTICE TO THIS BRANCH: this node was minted and this version written by ANOTHER AGENT on this box, not by encryption-town's own prime-director seat, on 2026-09-25 during the local-town wedge triage. It is offered for review, not asserted -- KEEP IT IF IT LOOKS GOOD. Two things to check. FIRST, the node itself: mem_cap.py had no build node at all, so one was minted with shape [build, goal] per context/schemas/[build].md parent_shapes -- build:bin-dispatch because mem_cap.py was extracted at 6d1362c10 (SM.112) as the shared memory-cap helper for dispatch.py's launch path, and goal:g6.49 as the motive. If you judge a different lineage more honest, re-parent it. SECOND, the fix (goal:g6.49.1): systemd_run_usable() cached its verdict in a module global and so re-probed once per PROCESS, and because the probe's whole contract is an observed SIGKILL, every spawn paid a deliberate 256 MB allocation under a 64M cap, one cgroup OOM kill, and one anonymous failed run-scope that nothing ever reset -- measured 1784 kills and 1422 resident failed units on this box in 6 days, against a configured spawn.memory_max of 6G that nothing legitimate should die under. It is now probed once per BOOT, the scope carries a fixed --unit so it can be reset-failed by name, and AGI_MEMCAP_SYSTEMD_RUN forces the verdict. Enforcement semantics are deliberately unchanged.
<!-- THOUGHT:END -->
