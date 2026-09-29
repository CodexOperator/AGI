---
edited_by: a00-1ff9316d
id: "experiment:a00-1ff9316d-tasksmax"
loop: "goal:g7.33.17@s2"
mint_id: eb9a85d9e8c246ad98083dcffce3309f
next_edges: []
parents:
  - hypothesis:a00-1ff9316d-177aae
title: "TasksMax on the round scope: an 18-process fan-out is refused, the unwrapped path is not"
town: core
type: experiment
---

<!-- BODY:BEGIN -->
# experiment:a00-1ff9316d-tasksmax

## What was built

`wrap_argv` (extensions/agi/bin/mem_cap.py) now carries a SECOND bound on the SAME
systemd scope it already built: `--property=TasksMax=<n>`, read from the config cell
**`values.memcap.tasks_max`** with the shipped default **`mem_cap._DEFAULT_TASKS_MAX = 96`**
(a round may never commit `.agi/config.json`, so the default lives in code and the cell is
read when present). 33 production lines, one file; the probe is untouched.

| piece | where | what |
|---|---|---|
| cell resolver | `mem_cap.resolve_tasks_max(cfg)` | absent / non-numeric / `<1` -> the shipped default, never "no bound"; `AGI_TASKS_MAX` overrides for tests |
| the bound | `wrap_argv` systemd branch | `--property=TasksMax=N` beside `MemoryMax` and `MemorySwapMax` |
| the residual | `wrap_argv` prlimit branch | NAMED IN CODE: the fallback bounds address space per process and nothing about tree width -- `RLIMIT_NPROC` is per-USER, so a per-tree process cap has no prlimit spelling. A box without a usable systemd-run still fans out unbounded. |
| tests | `extensions/agi/tests/test_mem_cap_tasks_max.py` (new, 9 tests) | cell/default/garbage, both argv branches, the fallback's *named absence*, and the real fan-out |

Why 96: one round's own tree is the round process plus its tools (a `pytest -n8` run is
~15 procs), so 96 is ~6x headroom on a normal round; the DH.419 fan-out that pushed user@
over `memory.high` was 127 forks, so a default BELOW that number catches the incident that
happened, and it is far under the box's user@ `pids.max` (16384) so the SCOPE refuses the
fork rather than the whole user slice growing.

## Red-on-old / green-on-new (the real thing, not a stand-in)

`bash` + `sleep` only -- no python child, no pytest recursion, every subprocess under
`timeout`, at most 18 processes on the uncapped path. 18 `sleep` fan-out under the WRAPPED
argv with `AGI_TASKS_MAX=8`:

```
p.returncode = 254,  markers = 8        (fork: Resource temporarily unavailable x N)
cap is None  ->  argv is the SAME object,  markers = 18,  rc 0
```

Before the edit (no `TasksMax` on the scope) the same script started all 30 in a manual
`systemd-run` without the property -- the old argv could not have refused.

## Real-path probe (not a hand-typed argv)

`realpath_probe.py` runs the three lines `dispatch.py` itself runs -- `adapters.load(...)`
-> `adapter.build_command(...)` (dispatch.py L2642) -> `mem_cap.resolve_memory_cap(cfg)`
(L2846) -> `mem_cap.wrap_argv(spawn_args, cap, cfg)` (L2851) -- with the LIVE config, and
prints the argv it would hand `Popen`:

```
harness=pi-free  cap(spawn.memory_max)=6G   tasks_max cell -> 96 (shipped default 96)
systemd-run --user --scope -q --property=MemoryMax=6G --property=TasksMax=96 \
    --property=MemorySwapMax=0 -- <pi argv>
spawn_args is untouched by the wrap: True
```

`systemd_run_usable()` was NOT forced here: the box's own probe verdict is True, so this is
the argv a real round gets.

## (b) The memory ordering -- MEASURED, not edited

`mem_order.py` (read-only) prints the per-round cap against user@'s own cgroup limits:

| bound | value |
|---|---|
| round scope / `spawn.memory_max` | 6,442,450,944 B (6.000 GiB) |
| user slice / `memory.high` | 5,500,829,696 B (5.123 GiB) |
| user slice / `memory.max` | 6,112,149,504 B (5.692 GiB) |
| user slice / `pids.max` | 16,384 |
| user slice / `pids.current` | 316 |

**The brief's ordering is CONFIRMED:** 6.000 GiB per round > 5.123 GiB user@ `memory.high`
AND > 5.692 GiB user@ `memory.max`, so the per-round `MemoryMax` can never bind first --
the user slice reclaims and then dies before the round's cap is reached. Not changed here
(reported only, as briefed). The TasksMax bound is the one that bites first, which is
precisely why it had to be added: process width, not bytes, was the unbound axis.

## Suite

* `extensions/agi/tests/test_mem_cap_tasks_max.py` -- 9 passed
* `extensions/agi/tests/test_launch_memory_cap.py extensions/agi/tests/test_mem_cap_cache_config.py` -- 19 passed
* `extensions/agi/tests/test_dispatch.py` -- 139 passed

Production lines (git diff --numstat, `extensions/agi/bin/`): 33 added, 0 removed.

## Residual, named

A box where `systemd_run_usable()` is False keeps the memory cap and gains NO process
bound. That is a real hole on such a box and it is a property of the box, not of this
code: the only spelling is a cgroup with a `pids` controller, which is what
`systemd_run_usable()` already tests for when it probes `MemoryMax`.
