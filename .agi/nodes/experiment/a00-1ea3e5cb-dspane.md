---
id: experiment:a00-1ea3e5cb-dspane
mint_id: 7afb51715c124666bb055a2b09d8f5ba
type: experiment
parents:
  - hypothesis:a00-1ea3e5cb-5d75a8
next_edges: []
edited_by: a00-1ea3e5cb
line_ceiling: 40
production_lines: 76
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
season: 2
title: Dispatch's real persistent spawn path births a named pane and reattaches the same %N
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-1ea3e5cb-dspane

## Experiment

Close the residual named by `experiment:a00-spawn-pane-hold` (and
`experiment:a00-e3f18179-pane-hold` before it): the adapter's pane seam
existed but NOTHING in production called it. `dispatch._open_round` built a
raw `subprocess.Popen`, and `.agi/config.json`'s `grok-bot` row had no
generic `pane` cell, so a real `--persistent` round was fire-and-forget and
there was no pane for `restart` to reattach to.

This round wires the real dispatch spawn path to the generic adapter
lifecycle entry and proves the falsifier end-to-end through `dispatch.main()`
(not through the adapter directly):

1. `dispatch._open_round` now prefers `adapter.spawn(...)` when the adapter
   exposes one, handing it THIS round's already-rendered
   `argv`/`env`/`cwd`/`log_file`. No harness literal appears in dispatch;
   adapters without `spawn` (every other harness) keep the byte-identical
   `Popen` branch.
2. The returned handle is `pane_hold.PaneProc`, an `int` subclass (so
   pid-shaped callers keep working) carrying `.pid` / `.poll()` /
   `.returncode`. `mem_cap.wrap_argv` still wraps the argv before the
   adapter sees it. The persistent supervisor and reaper are unchanged.
3. `.agi/config.json` grows the generic `"pane": true` cell on `grok-bot`
   (a generic cell, not a grok-named key or branch).

The pane-name stamp lives in a per-slot `_pane_stamp` dict that survives
every reopen, so the SAME pane name is *re-read*, not re-derived.

Production change: `pane_hold.py` `PaneProc` (+34), `grok_bot_adapter.py`
`spawn` gains prebuilt-round kwargs and returns `PaneProc` (+17/-12),
`dispatch.py` `_open_round` + debug-brief `project_root` (+25), config (2).
76 added / 13 deleted, under 2x the 40-line ceiling.

## Probes (one per falsifier conjunct)

1. **`restart`/`reopen` reattaches the SAME name and %N after a kill.** The
   end-to-end dispatch test SIGKILLs the pane's pid and asserts the
   supervisor's `reopen` returns a NEW `pane_pid` with the SAME `%N` and
   window name, `pane_dead=0` again.
2. **A live NAMED pane exists from the first spawn.** The test reads the
   window name out of `tmux list-windows` on the throwaway `-L` socket and
   `pane_hold.pane_id` returns a non-empty `%N`.
3. **The record carries the occupation.** The manifest's agent record has
   `pane == <window name>`, `pane_id == %N`, `pane_session == <session>`.
4. **Harness-agnostic seam.** `grep -ic grok dispatch.py rotate.py` -> 0/0;
   an adapter with no `spawn` still spawns via `Popen` (negative control =
   the untouched `test_dispatch_persistent.py` pi cases).

## Evidence

All command tails on this tree (throwaway tmux `-L` socket, never `agi-rc`):

```
$ python3 -m pytest extensions/agi/tests/test_dispatch_pane_hold.py -q
1 passed, 1 warning in 17.75s

$ python3 -m pytest extensions/agi/tests/test_dispatch_persistent.py \
    extensions/agi/tests/test_adapter_pane_spawn_hold.py \
    extensions/agi/tests/test_adapter_pane_hold.py \
    extensions/agi/tests/test_grok_bot_adapter.py \
    extensions/agi/tests/test_adapters.py \
    extensions/agi/tests/test_real_adapter_restart.py -q
70 passed, 6 warnings in 42.02s

$ grep -ic grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py
extensions/agi/bin/dispatch.py:0
extensions/agi/bin/rotate.py:0

$ git diff --numstat -- <production paths>
2	1	.agi/config.json
17	12	extensions/agi/bin/adapters/grok_bot_adapter.py
34	0	extensions/agi/bin/adapters/pane_hold.py
25	0	extensions/agi/bin/dispatch.py
```

The end-to-end dispatch test (new file
`extensions/agi/tests/test_dispatch_pane_hold.py`) drives the REAL
`dispatch.main()` with `--persistent`, a sleeping fake harness bin, and a
config with `"pane": true` + a throwaway `pane_session`. It asserts, in
order: a named window appears on the socket; `%N` is non-empty; SIGKILL of
`pane_pid` is followed by the supervisor's restart to a different pane pid
on the SAME `%N`; the manifest record carries `pane`/`pane_id`/`pane_session`;
and dispatch returns 0 once `AGI_PERSISTENT_STOP` is set.

## Residual (named, not papered over)

The live pane session is `pane_hold.DEFAULT_TMUX_SESSION` ("agi-rc") unless
a harness `pane_session` cell overrides it, so the FIRST real grok-bot
dispatch after this commit will create its window in the live `agi-rc`
session. That is the goal's intent (the seat visible where the operator
looks) but it is a behaviour change on a live session and is called out
here rather than discovered later. No pane↔post/pin linkage and no
magic-pane chrome — both out of scope.

The debug-brief `project_root=root` fix is a one-line divergence: the
spawn.json artifact previously resolved its line ceiling from brief.py's
OWN graph (scanning it for a foreign node id), not the dispatched project's.
Without it the test above could not complete in reasonable time.
