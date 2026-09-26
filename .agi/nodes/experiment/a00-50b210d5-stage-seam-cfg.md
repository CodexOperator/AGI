---
id: experiment:a00-50b210d5-stage-seam-cfg
type: experiment
parents:
  - hypothesis:a00-50b210d5-b85ee2
next_edges: []
edited_by: a00-50b210d5
production_lines: 12
season: 2
title: "the stage seam: cfg threaded into mem_cap.wrap_argv (red 3 / green 15, 8/-4 in workflow.py)"
---
# experiment:a00-50b210d5-stage-seam-cfg

## What was run
The build order of `hypothesis:a00-50b210d5-b85ee2`, end to end on these bytes.

| step | result |
|---|---|
| measure the pre-fix seam | `workflow.py:1803` `mem_cap.wrap_argv(cmd, cap)` — no cfg; `_run_stage_pi` holds one (it resolved `cap` at `:1860`) and drops it at the `:1888` call |
| write the acceptance test FIRST | `extensions/agi/tests/test_workflow_stage_seam_cfg.py`, 4 tests |
| run it on the unfixed bytes | **3 failed, 1 passed** (W1 `TypeError: _run_stage_proc() got an unexpected keyword argument 'cfg'`, W2 same, W4 the byte pin; W3 green by design) |
| build the claim | `workflow.py` only: `cfg` param on `_run_stage_proc`, `wrap_argv(cmd, cap, cfg)`, `cfg=cfg` at the one call site — **8 added / 4 removed** |
| run it on the built bytes | **4 passed**; with the two neighbouring cap files: **15 passed** (`test_launch_memory_cap.py`, `test_launch_wrapper_mem_cap.py`) |
| workflow suite | `test_workflow.py` + 5 stage-path files: **175 passed, 2 skipped** in 172 s |

## The seam probe (why it is a measurement, not an argument)
`wrap_argv`'s `cfg` parameter is read for exactly one thing: `systemd_run_usable(cfg)`
(mem_cap.py 233-245). So a recording stand-in for that function observes precisely
which cfg OBJECT reached the cap helper, checked by `is` — a copy would not have
proved the caller's dict travelled. Pre-fix it recorded `None`; post-fix it records
the caller's own dict. The verdict is forced to the prlimit branch by
`AGI_MEMCAP_SYSTEMD_RUN=0` plus a PATH shim that logs any real `systemd-run` /
`systemctl` exec and exits 137, so nothing here touches real systemd (the rule
`test_launch_memory_cap.py` already states).

| probe | red | green |
|---|---|---|
| W1 caller cfg reaches the cap helper (by identity) | `None` | **is cfg** |
| W2 the stage is still capped: real `_ALLOC` child under `prlimit --as=256M` dies of the cap | TypeError | `is_cap_death` true |
| W3 no cfg in hand (legacy caller) -> shipped defaults | green | green, `seen == [None]` |
| W4 the byte reads `wrap_argv(cmd, cap, cfg)` and never the 2-arg form | red | green |

## The correction, measured
The parent brief's "the stage seam drops `values.memcap.tasks_max`" is **false on
this tree**: `grep -rn "tasks_max\|TasksMax" extensions/agi/bin extensions/agi/tests
.agi/config.json` -> **0 hits**. `tasks_max`/`+TasksMax` is on kid 1's branch
(`dispatch.py:2851`), which is not on this tree. The shape of the defect is as
briefed (the ONE cfg-less `wrap_argv`); the cell's NAME is not. What the seam
actually drops today is the `values.memcap` probe-cache pair
(`probe_cache_dir_name` / `probe_cache_file`) — the only cells `wrap_argv`'s `cfg`
touches. Recorded in the hypothesis node so the next reader does not hunt for a
seam that was never here.

## Production lines
`git diff --numstat -- extensions/agi/bin/workflow.py` -> **8 4** (ceiling 40).
Test files excluded by the rule. NO line of `mem_cap.py`, `rotate.py` or `heal.py`
touched (other branches carry changes to those).

## Not fixed here, NAMED
`resolve_memory_cap` validates nothing: a garbage cell (`seat_memory_max: "abc"`,
same for `spawn.memory_max`) reaches `systemd-run --property=MemoryMax=abc`
verbatim and the child **DOES NOT LAUNCH** ("Failed to parse MemoryMax=abc"). The
fix belongs in `mem_cap.py`, which is off-limits this round. Carried forward.

## Stray
`.agi/nodes/hypothesis/a00-955a27ff-64bc5a.md` shows uncommitted (+16/-1) in this
worktree — the previous kid's node from the parent worktree, left exactly where
it is.
