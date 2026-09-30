---
id: experiment:dg2-r1-per-post-scope-baseline
mint_id: 493cc631c00e40ca8f64cfc5631b40ca
type: experiment
parents:
  - hypothesis:every-post-launch-gets-its-own-scope-by-construction
next_edges: []
edited_by: director-general-2
scaffold_hash: e5d80884ae830083
season: 2
title: "R1 baseline: 10/11 claude + tmux in the RC service; 0 agi-rc creators; cap None unwrapped; dummy scope + grouped cutover: one kill = one post"
town: core
---
# experiment:dg2-r1-per-post-scope-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 85d37d77b (measured bytes unchanged at e989981f6), 18:04-18:18Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `ps -e -o pid=,comm=` + `/proc/<pid>/cgroup` per claude / `tmux: server` (no argv) | 18:04Z: 10 claude + the tmux server in `app.slice/claude-remote-control.service`; 1 claude in `tmux-spawn-<uuid>.scope`; the service cgroup.procs = 80-89 pids across the run |
| 2 | same, claude comm pids grouped by cgroup (F5: two live posts share one scope) | 18:11Z: 10 claude pids share ONE cgroup (claude-remote-control.service) -- F5 fires today, as expected pre-cutover |
| 3 | `git grep -n new-session -- extensions skills src`; `git grep -n _ensure_tmux_session -- extensions` | 0 in extensions/agi/bin (3 total: 2 are a session_id string in test_rotate_key_authority.py, 1 is a doc example in skills/agi/SKILL.md:749 making session `agi`); `_ensure_tmux_session` 0 |
| 4 | `mem_cap.wrap_argv(a, None, {})` from the /tmp tree copy | returns the SAME list object (`is argv` True); guard at mem_cap.py:318, return :319. With cap 2G: `systemd-run --user --scope -q --property=MemoryMax=2G --property=TasksMax=96 --property=MemorySwapMax=0 -- ...`: no `--slice`, no `--unit` |
| 5 | `mem_cap.resolve_memory_cap(<config.json>)`; `rotate._shell_cmd([...], None, seat=None / "p")` | `2G` (spawn.memory_max, config.json:150, the dispatch cap); `systemd-run` absent from both `_shell_cmd` lines |
| 6 | `git grep -n '"new-window"\|_launch_window(' -- extensions/agi/bin` | TWO new-window sites: rotate.py:1779 (inside `_launch_window`, called by `spawn_window` :1952/:1954) and heal.py:3036 (`_launch_recovered`, heal's own launcher). heal builds its line through `rotate.spawn_window(dry_run=True)` -> `_shell_cmd` (rotate.py:1933, heal.py:3267) but never calls `_launch_window` |
| 7 | `git grep -n 'wrap_argv(.*None' -- extensions/agi/tests` | 3 existing pins of the shared cap-None contract: test_launch_memory_cap.py:132, test_mem_cap_tasks_max.py:243 and :289-295 (`is argv`) |
| 8 | dummy 1: `systemd-run --user --scope --unit=dg2-r-dummy-28722 --slice=agi.slice sleep 120` launched FROM a shell inside claude-remote-control.service; stop that unit only | its `/proc/pid/cgroup` = `agi.slice/dg2-r-dummy-28722.scope` (its OWN scope, left the service); stop -> dummy gone; service procs 81 -> 81 -> 81, tmux server alive, 10 claude still in service |
| 9 | dummy 2 (the 18:05Z recipe): AttachProcessesToUnit of my own `sleep` into a scope created WITHOUT Delegate | `Call failed: Process migration not available on non-delegated units.` (rc 1); pid stays in the service; the scope stopped, the stray sleep (mine) killed |
| 10 | dummy 3: same with `--property=Delegate=yes` | attach rc 0: pid moves service -> `app.slice/dg2-r-dummy-attach.scope`; service procs 88 -> 89 -> 88 (moved out) -> 88 after stop; pid dies with the scope |
| 11 | v2: src scope `dg2-r-dummy-src` (keeper + sh parent + sleep child), dst `dg2-r-dummy-dst` `Delegate=yes --slice=dg2-r-dummy.slice` (NOT agi.slice); Attach every src pid but the keeper | parent sh + child sleep both read `dg2.slice/dg2-r.slice/dg2-r-dummy.slice/dg2-r-dummy-dst.scope`; stop dst -> both die, keeper + src unit live; service 81 -> 81 -> 81 |
| 12 | v3 GROUPED: src holds keeper + "tmux" sleep + post A (sh + child) + post B (sh + child); prototype helper `/tmp/dg2b3/r1/cutover_sketch.py` `_cutover_to_scopes` (StartTransientUnit PIDs+Delegate=yes per group, slice dg2-r-dummy.slice, prefix dg2-r-dummy-) | plan `{postA: [sh, sleep], postB: [sh, sleep], tmux: [sleep]}`, every pid reads its group's scope, src keeps only the keeper; stop ONLY dg2-r-dummy-postA.scope -> A + child die, B + child and tmux live; service 81 -> 81 |
| 13 | cleanup: `systemctl --user list-units 'dg2*' --all`; cgroup dirs | 0 units, 0 cgroup dirs, 0 dummy pids (the `dg2-r-dummy.slice` name nests as dg2.slice/dg2-r.slice/..., both stopped too) |
| 14 | `agi.slice` limits (read-only) | exists live (agi-engine.slice + agi-work.slice under it): memory.high 9261023232, memory.max 10290724864, current ~0.6G |
| 15 | `/proc/pressure/memory` (once, 18:04Z) | some avg10=0.13 avg60=0.37 avg300=0.26; full avg10=0.13 avg60=0.37 avg300=0.25 |

## What it shows
```
today                                        after R1 (built)                    cutover (grouped, dummies proved)
claude-remote-control.service                agi.slice                           agi.slice
  |- tmux server (agi-rc)                     |- agi-rc scope (ensure, if absent) |- tmux scope (tmux + the rest)
  |- post 1..10 (claude + tree)   --oomd-->   |- post-X scope (_shell_cmd wrap)   |- post-A scope (pid + descendants)
  one kill = every post                       one kill = one post (NEW posts)     |- post-B scope ...  (Delegate=yes each)
heal recover: spawn_window(dry) -> _shell_cmd (wrap reaches it) -> heal.py:3036 own new-window (ensure does NOT reach it)
```

## Test committed (strict xfail, RED until DG3 builds)
`test_rotate.py::test_r1_every_post_argv_is_scoped_even_when_cap_is_none[None|p1]` -- `_shell_cmd` puts `systemd-run --user --scope ... --slice=agi.slice` before the claude argv with no post cap cell (cap None), seat and seatless
`test_rotate.py::test_r1_launch_window_ensures_agi_rc_in_its_own_scope_first` -- agi-rc absent -> exactly one `systemd-run --user --scope --slice=agi.slice ... new-session` before `new-window` (fake subprocess.run)
`test_rotate.py::test_r1_cutover_plan_gives_each_post_tree_its_own_scope` -- pure plan: each claude pid + descendants -> its own scope, the rest -> the tmux scope, MainPID stays
`test_rotate.py::test_r1_cutover_dummy_one_kill_is_one_post` -- live dummy cutover (skips without user systemd/busctl; units `dg2-r-dummy-<pid>-*` only): grouped move, stop post A's scope, post B + source live. Green with the prototype helper.
