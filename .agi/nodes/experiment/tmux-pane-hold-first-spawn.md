---
id: experiment:tmux-pane-hold-first-spawn
mint_id: 68edf120ce364d26bb18cf9a967ca9f3
type: experiment
parents:
  - hypothesis:a00-e9e22ed7-63f7a7
next_edges: []
edited_by: a00-e9e22ed7
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"class": "wire", "probe": "panes()/list-panes WITHOUT -s sees only the current window, so a non-current seat window is invisible and a second window is fabricated", "status": "refuted_by_test"}
  - {"class": "gate", "probe": "an explicit tmux:False on a harness must win over HOLD_PANE and keep the direct-Popen path", "status": "held"}
  - {"class": "wire", "probe": "remain-on-exit set AFTER the command races a fast-failing argv that closes the window and loses the pane", "status": "refuted_by_fix"}
  - {"class": "auth", "probe": "the real-tmux proof must never touch the live agi-rc session (scratch session only, killed at teardown)", "status": "held"}
production_lines: 71
profile: balanced
role: kid
scaffold_hash: 1c42a0e41fb74f0a
season: 2
thought_session: iter-DT.67
title: Tmux pane hold first spawn
town: core
---
<!-- BODY:BEGIN -->
# experiment:tmux-pane-hold-first-spawn

## Experiment

Build order (`goal:g7.31.1.2`): make a grok-bot seat's durable named tmux pane
exist at the FIRST spawn, then prove `restart` re-enters the SAME immutable
pane. Base is `14970838a` (the dispatch order's requested reset to `51ae16535`
never happened, so the DT.34–DT.47 pane bytes are absent here); prior art was
read from the stranded branch and verified on real tmux before adapting.

Built (production lines, `git diff --numstat`, tracked files only):
- `extensions/agi/bin/adapters/tmux_hold.py` (NEW): `pane_name(agent_id)`,
  `start()` founds the named window/pane, `reattach()` uses
  `respawn-pane -k -t <pane_id>` (immutable id, never the dotted name),
  `panes()` passes `-s`, `spawn()` is the FIRST-SPAWN entry dispatch calls, and
  `HeldProc` gives dispatch's startup-grace loop its `poll()/pid/returncode`.
  `remain-on-exit` is set on the pane BEFORE the real argv is respawned into
  it — setting it after raced a fast-failing command and lost the pane.
- `extensions/agi/bin/adapters/grok_bot_adapter.py`: `HOLD_PANE = True` +
  `hold_harness()` (adapter's own declaration; explicit `tmux: False` wins),
  and `restart` routes through `tmux_hold.reattach(..., created=...)`.
- `extensions/agi/bin/adapters/__init__.py`: `_box_tmux_session` carried onto
  the resolved harness (`tmux_session`), the ONE source of the session name.
- `extensions/agi/bin/dispatch.py` `_open_round`: when the resolved adapter
  declares a hold, the first spawn calls `tmux_hold.spawn(...)` instead of
  `Popen`, with NO harness name special-cased.

Measurements against a REAL tmux server (tmux 3.4), scratch session
`agi-dt67-probe-<pid>`, killed at teardown; never the live `agi-rc`:

- first spawn: `tmux list-panes -s -t <session>` shows
  `seat-a4527bd01360 %52 <pid>` BEFORE any restart.
- kill the pane process; `restart`: `created == {"created": False,
  "pane_id": "%52"}` — the SAME immutable pane id, new pid.
- kill the WINDOW (genuinely gone); `restart`: `created["created"] is True`
  and exactly ONE seat window exists afterwards.

## Evidence

`python3 -m pytest extensions/agi/tests/test_tmux_hold.py -q` → 9 passed
(6 FakeTmux fixtures + 3 real-tmux integration tests; the real tests skip BY
NAME when `tmux` is absent). The real tests capture the real stdlib
`subprocess.run` at import to step over the suite's autouse `_no_real_tmux`
guard, which exists to protect the LIVE `agi-rc` session.

Regression: `test_grok_bot_adapter.py` + `test_adapters.py` +
`test_real_adapter_restart.py` → 63 passed; `test_dispatch_dry_run.py` +
`test_dispatch_forward_env.py` + `test_dispatch_model_allowlist.py` → 43
passed. `grep -n 'grok' extensions/agi/bin/dispatch.py` → no hits.
