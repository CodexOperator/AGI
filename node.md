---
id: goal:g6.49.1
mint_id: 32fa1eb20b0f4143a627821fc268d500
type: goal
parents:
  - goal:g6.49
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G6.49.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 7f0499dad80ea201
season: 2
seeds: []
status: complete
tags:
  - goal
  - subgoal
thought_session: reaper-triage-2026-09-25
title: "G6.49.1: mem_cap's enforcement probe runs once per PROCESS, so every spawn costs one deliberate OOM kill and one leaked failed scope"
town: core
---
<!-- BODY:BEGIN -->
# goal:g6.49.1

## Agent Notes
DEFECT: mem_cap.systemd_run_usable() cached its verdict in a module global, so it re-probed once per PROCESS. The probe's contract is an observed SIGKILL -- it allocates 256 MB under a MemoryMax=64M scope and requires the kill -- so every dispatch.py, heal.py and cron invocation paid one deliberate 256 MB allocation, one cgroup OOM kill, and one anonymous failed run-<random>.scope that nothing ever reset. MEASURED on encryption-town: oom_kill 1784 since boot, 1422 failed run-*.scope units resident in systemd --user, 52 of the 55 surviving dmesg kill records being python3 at ~65,000kB (the 64M cap), against a configured spawn.memory_max of 6G that nothing legitimate should die under. FIX: probe once per BOOT, verdict cached in XDG_RUNTIME_DIR keyed on boot id; the scope carries a fixed --unit so it can be reset-failed by name; AGI_MEMCAP_SYSTEMD_RUN=0|1 skips the probe entirely. Enforcement semantics unchanged -- still a real allocation past a real cap, still requiring the observed SIGKILL. VERIFIED live: cold run took exactly one OOM kill (1793 to 1794), two subsequent fresh processes took none and left the failed-unit count flat. The 1430 accumulated units were cleared with systemctl --user reset-failed (1430 to 0; run-*.scope 1422 to 8).
