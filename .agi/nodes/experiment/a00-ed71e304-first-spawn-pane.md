---
id: experiment:a00-ed71e304-first-spawn-pane
type: experiment
parents:
  - hypothesis:a00-ed71e304-7e16f0
loop: goal:g7.31.1.2.2@s2
title: AST-lifted production _open_round spawns and is killed, with a logging tmux on PATH
---

# experiment:a00-ed71e304-first-spawn-pane

The run itself, in short — full output in the hypothesis body above and at
`.agi/sessions/iter-DT.218/a00-ed71e304/probe-output.txt`.

**Method.** `ast.get_source_segment` lifted the real `def _open_round` out of
`extensions/agi/bin/dispatch.py:2651` (inside `main()`, line 1505). It was
compiled and executed with `subprocess.Popen` replaced by a recording shim that
forwards to the real `subprocess.Popen` with the same kwargs (argv substituted
`["sleep","600"]` for the paid agent argv) and `mem_cap.wrap_argv` as identity.
`PATH` was prefixed with a logging `tmux` shim so any tmux call made by the
production path would be recorded.

**What happened.** `tmux list-panes -a` was byte-identical before the call,
after the call, and after `kill -9` of the real child (pid 1431047,
returncode -9, `ps` shows `(gone)`). The shim log held three entries, all of
them the probe's own `tmux -V` and two `list-panes` — **zero** from
dispatch.py. No pane was created by the production spawn; none survived the
kill. `find . -name 'tmux_hold*'` → empty.

**Reading.** The falsifier of the claim ("stable pane_id across `kill -9`
without an out-of-band `tmux_hold.start()`") is **not satisfied**: there is no
pane, so there is no id to be stable. The probe itself created no pane — it only
listed — so this is not the near-miss of measuring one's own script.

**Stubs, named.** argv (`sleep`), `mem_cap` (identity), and the fact that the
closure was called once rather than through `main()`. A real agent round, the
restart path, and any `created=true` stamping remain unmeasured here.
