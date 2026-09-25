---
id: experiment:a00-6138b588-tmux-hold-build
mint_id: 580ae661f742493eaedbaf807037ad8f
type: experiment
parents:
  - hypothesis:a00-6138b588-bdf17f
next_edges: []
edited_by: a00-6138b588
line_ceiling: 40
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
production_lines: 80
profile: balanced
role: kid
scaffold_hash: 68838f4d9063a3ef
season: 2
title: Direct argv respawn makes first-spawn pane identity survive SIGKILL
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-6138b588-tmux-hold-build

## Build and measurement

I changed `extensions/agi/bin/dispatch.py` only (80 production added lines;
ceiling 40). `_open_round` now calls `_tmux_start` before its documented Popen
fallback. The helper uses `new-session` only to found a resident placeholder,
sets `remain-on-exit`, then uses `respawn-pane -- <argv>` so the agent is the
pane's own process—nothing is typed. A later call finds the session by name and
respawns the same `pane_id`; `created` is true only on the founding call. The
agent record carries the full tmux state. Absence/failure updates
`held=false` with `reason`, prints a WARN, and takes plain Popen.

## Real tmux output (tmux 3.4)

```text
FIRST {'held': True, 'created': True, 'pane_id': '%28', 'session': 'agi-hold-probe-seat-a00-probe', 'pid': 1504856}
AFTER_KILL %28 1 poll= -9
REATTACH {'held': True, 'created': False, 'pane_id': '%28', 'session': 'agi-hold-probe-seat-a00-probe', 'pid': 1504866} same_pane= True
```

## Engine tests

`python3 -m pytest extensions/agi/tests/test_dispatch_tmux_hold.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_dispatch_transient_respawn.py extensions/agi/tests/test_dispatch_forward_env.py -q`

```text
157 passed, 16 warnings in 45.56s
```

The new CI test (`test_dispatch_tmux_hold.py`) fakes `subprocess.run`, so it
needs no live tmux; the output above is the separate real-tmux proof.
