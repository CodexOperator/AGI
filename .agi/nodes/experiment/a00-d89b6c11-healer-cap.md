---
id: experiment:a00-d89b6c11-healer-cap
mint_id: 41d0b6c9a1e5f2049c7b3ad9e0f51c62
type: experiment
parents:
  - hypothesis:a00-d89b6c11-b6e73f
next_edges: []
edited_by: a00-d89b6c11
loop: goal:g7.33.17@s2
production_lines: 12
season: 2
title: the healer Popen measured uncapped, then wrapped -- 4/4 green, 104 in the heal suites
town: core
---
# experiment:a00-d89b6c11-healer-cap

## What was measured (the pre-fix state, honestly)

The previous kid (a00-1ff9316d) named, unexamined, that only `wrap_argv`'s TWO
call sites had been looked at. An audit of the engine's agent spawns:

| site | spawns | wrapped? |
|---|---|---|
| `dispatch.py:2851` (`_open_round`) | the round's kid | yes (`wrap_argv(..., cfg)`) |
| `workflow.py:1803` | a workflow stage | yes (`wrap_argv(cmd, cap)`) |
| `heal.py:3768` (`_heal`) | **the healer agent** | **NO — raw `pi` argv** |
| `rotate.py:1652` (`launch-wrapper`) | the seat relaunch child | no — NAMED RESIDUAL, below |
| `rotate.py:7375` (`_spawn_master_rotate`) | `rotate.py` itself | n/a — engine-internal, not an agent |

The gap is the healer, and it is the worst-placed one: a healer is spawned
*precisely when a round has already gone wrong*, which is when a runaway is
most likely, and it is the one spawn with no `env=`-scrub audit trail of a cap.

## The build (a g15 claim is behaviour to build, so it was built)

`heal.py`, +12/-2 production lines:
- `import mem_cap` beside `import locations`;
- after the `pi_args` list is built: `heal_cfg = locations.load_config(_main_graph_root(root))`
  (the same config resolver heal.py already uses at :486), then
  `heal_argv = mem_cap.wrap_argv(pi_args, mem_cap.resolve_memory_cap(heal_cfg), heal_cfg)`;
- the `Popen` and the recorded `healer.command` both take `heal_argv`, so
  `agent.json` names the command ACTUALLY launched, cap included.

## Pre-fix bytes, measured (not asserted)

`.agi/sessions/iter-DH.421/a00-d89b6c11/prefix_probe.py` re-runs `_heal` with
the wrap seam stubbed back to identity:

```
PRE-FIX argv: ['pi', '-p', '--append-system-prompt', '@.../healer-.../context.md']
... has MemoryMax: False
```

## Post-fix, the suite

`extensions/agi/tests/test_heal_mem_cap.py` (new, 4 tests, all against the argv
the Popen seam is handed — the box's fork bound forbids a real fan-out, as the
previous kid recorded):

| test | asserts |
|---|---|
| `test_healer_argv_carries_the_configured_cap` | `argv[0] == "systemd-run"`, `--property=MemoryMax=1G` present, the prompt still last |
| `test_healer_record_names_the_command_actually_launched` | `agent.json`'s `healer.command` == the shlex-joined launched argv, cap included |
| `test_a_capped_off_cell_leaves_the_healer_unwrapped` | `spawn.memory_max: null` -> raw pi argv, no `MemoryMax` anywhere (the escape hatch stays one) |
| `test_an_absent_cell_still_caps_the_healer` | no `spawn` cell -> the shipped `4G`; a missing config is not the one uncapped case |

```
4 passed
104 passed  (test_heal_watch.py test_dispatch_alarms.py test_heal_mem_cap.py
             test_mem_cap_cache_config.py test_mem_cap_override.py)
```

## Named residual, NOT fixed (one line, no silent gap)

`rotate.py:1652` `launch-wrapper` still spawns its child unwrapped. It is
deliberately left alone this round: the wrapper's contract is a
`sigwaitinfo(SIGCHLD)` loop that forwards signals to `child.pid` by number, and
`systemd-run --scope` would put a second process between the wrapper and the
agent, changing the pid the forward targets. Capping it needs its own
hypothesis (a scope-aware signal forward), not a one-line wrap.

## What this does NOT prove

- Not a live cgroup kill: the argv is proven, the refusal is not (fork-bound,
  as the previous kid recorded).
- `wrap_argv`'s **prlimit** fallback gives no per-tree process bound
  (`RLIMIT_NPROC` is per-user) — the previous kid's named residual, unchanged
  here.
- The auditor is my own grep, not a lint: a future spawn path added outside
  `wrap_argv` would not be caught by these tests.
