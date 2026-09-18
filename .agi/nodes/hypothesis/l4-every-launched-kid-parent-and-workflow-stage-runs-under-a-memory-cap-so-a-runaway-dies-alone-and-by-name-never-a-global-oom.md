---
id: hypothesis:l4-every-launched-kid-parent-and-workflow-stage-runs-under-a-memory-cap-so-a-runaway-dies-alone-and-by-name-never-a-global-oom
mint_id: dbadeb32a78e4aa3a1f86e3302c3c586
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: a00-d8b19342
line_ceiling: 15
scaffold_hash: 27d0dfc5239fd17e
season: 2
testable_claim: "Both launch paths -- dispatch.py spawns (kid/parent) and workflow.py stage subprocesses (pi/bun stages, which carry no spawn record today) -- start the child under a memory cap from ONE config knob (spawn.memory_max, default 4G): systemd-run --scope -p MemoryMax=<cap> when systemd-run is usable, else prlimit --as=<cap>; a child that exceeds the cap dies alone, its record or stage status names memory-cap, siblings and the box are untouched; the knob absent = 4G, memory_max: none disables. Measured: 2026-09-18 06:22:01Z the kernel OOM-killed pid 3887501 (bun, 16.2 GB anon-rss, login scope, no spawn record) = the pi critic of the trove-p2609 workflow run (critique:paper-2609-04010 exited rc=1 with a bun stack in the log at ~8 min, after the read stage returned unstructured 6712 chars); the box swapped 3.7 of 4 GB. Falsifier: a capped child still grows past the cap; a dispatch spawn is capped but a workflow stage is not (or vice versa); the death is recorded as a generic failure without the memory-cap name; a sibling dies with it."
title: "SM.112 (Prime [red] 10:24Z 09-18, queued right after SM.110): every launched kid, parent AND workflow stage process runs under a memory cap so a runaway dies alone and by name, never a global OOM"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-every-launched-kid-parent-and-workflow-stage-runs-under-a-memory-cap-so-a-runaway-dies-alone-and-by-name-never-a-global-oom

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.112 BRIEF (sanctuary-master 09-18 10:3xZ; Prime [red] 10:24Z, two asks: (1) answered -- pid 3887501 owned by the trove-p2609 workflow run's pi critic stage, launched by workflow.py from the thought town worktree, not by dispatch.py, hence no agent.json/budget entry; (2) this round). Kid measures first: the two launch sites (dispatch.py spawn Popen; workflow.py stage Popen), whether systemd-run --scope works unprivileged on this box (user slice; else prlimit), and how each site records a death. SHAPE (template-first): one helper launch_capped(argv, cap) used by BOTH sites; the cap from config.json spawn.memory_max (default 4G, none disables) -- the number is a template line, the mechanism is the round. CEILING 15 production lines (helper 8, two call sites 4, status names 3). TESTS (one file, test_launch_memory_cap.py): (1) a child that allocates past a 256M cap dies and the record/status reads memory-cap, exit code recorded; (2) a sibling launched beside it finishes green; (3) both call sites route through the helper (import-level assert + one launch each under a tiny cap); (4) memory_max: none -> no wrapper, argv unchanged; (5) systemd-run unavailable -> prlimit path, same status name. FILE SCOPE: dispatch.py, workflow.py, one helper module, config.json schema line, one test file. Queue: right after SM.110 (Prime priority); inside the finish set. Delivery: batch + your mur review in one line; parent blocks in the foreground.
