---
id: experiment:grok-bot-durable-named-pane-hold
mint_id: 6a09970d23a848709ec248088b178bd4
type: experiment
parents:
  - hypothesis:a00-9c14c400-d4d2c5
next_edges: []
edited_by: a00-9c14c400
line_ceiling: 40
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 74
profile: balanced
role: kid
scaffold_hash: de3588cf5bf22051
season: 2
title: grok-bot restart holds the seat in one named tmux pane
town: core
---
<!-- BODY:BEGIN -->
# experiment:grok-bot-durable-named-pane-hold

## Experiment

Built the `hold_pane=True` branch of `grok_bot_adapter.restart`
(`extensions/agi/bin/adapters/grok_bot_adapter.py`). One named pane per seat:
`pane_name(agent_id)` is derived from the SEAT id, never a pid. The SAME
`build_command` argv runs inside it — the first pane-bearing restart
`tmux new-session -d -s <name>`, every later one `tmux respawn-pane -k`, and
`set-option remain-on-exit on` keeps the pane after the process dies. When tmux
is absent the adapter falls back to the unchanged direct `Popen`. The default
`restart()` (no `hold_pane`) is byte-for-byte today's path.

Pre-fix measurement (falsifier #1), recording tmux shim on PATH, default
restart: `pid: 4242`, argv `['grok-bot', '--model', 'grok-kid', '-p', ...]`,
`tmux_log_exists: False`, `tmux_invocations: <none>` — the pre-fix state was a
bare `Popen` with ZERO tmux invocations.

## Evidence

Command:

    python3 -m pytest extensions/agi/tests/test_grok_bot_pane_hold.py \
        extensions/agi/tests/test_grok_bot_adapter.py \
        extensions/agi/tests/test_real_adapter_restart.py -q

Tail:

    33 passed, 3 warnings in 79.41s (0:01:19)

(5 in `test_grok_bot_pane_hold.py`, 28 across the two committed contract /
real-restart files.)

Shim log bytes for TWO pane-bearing restarts of seat `a00-seat` (pane name
`agi-seat-a00-seat`) — exactly ONE `new-session`, then a `respawn-pane` at the
SAME name:

    has-session -t agi-seat-a00-seat
    new-session -d -s agi-seat-a00-seat -c .../sessions .../sleeper.sh --model grok-kid -p .../context.md
    set-option -t agi-seat-a00-seat remain-on-exit on
    list-panes -t agi-seat-a00-seat -F #{session_name} #{pane_pid}
    has-session -t agi-seat-a00-seat
    respawn-pane -k -t agi-seat-a00-seat -c .../sessions .../sleeper.sh --model grok-kid -p .../context.md
    list-panes -t agi-seat-a00-seat -F #{session_name} #{pane_pid}

    pane name: agi-seat-a00-seat | p1: 2257443 | p2: 2257609
    pane_listing after restart: ['agi-seat-a00-seat 2257609']
    is_alive(killed pid): False
    pane_listing after SIGKILL: ['agi-seat-a00-seat 2257609']

The pane outlives the pid: SIGKILL takes the process, `list-panes` still shows
`agi-seat-a00-seat`. Full recorded log:
`.agi/sessions/iter-DH.171/a00-9c14c400/postfix-evidence.txt`.

### Probes (one negative per conjunct, class wire/gate/auth)

- **wire** — `test_default_restart_touches_no_tmux`: a default restart is
  measured on a recording shim and must leave NO log; the seam a careless
  change would open.
- **wire** — `test_first_restart_opens_exactly_one_named_pane`: the log must
  contain exactly one `new-session`; a second pane for the same seat fails.
- **gate** — `test_second_restart_reuses_the_same_named_pane`: `new-session`
  count stays 1 while `respawn-pane` count is 1, at the SAME derived name.
- **gate** — `test_killing_the_process_leaves_the_named_pane`: after a genuine
  SIGKILL (`is_alive` false) the pane listing is still non-empty.
- **auth** — `test_tmux_unavailable_falls_back_to_direct_popen`: tmux absent
  (`subprocess.run` raises `FileNotFoundError`) falls back to `Popen` with the
  identical argv and a stamped record; never raises.

### Residue (owner: next kid, separate seam)

- `dispatch.py::_supervise_persistent` (`~L1518`) still reopens via a bare
  `Popen` closure with no tmux pane. The adapter now CAN hold a pane; the
  persistent-dispatch site does not yet pass `hold_pane=True`. Not fixed here.
- In pane mode the seat's stdout/stderr go to the tmux pane, not
  `sess_dir/output.log`; the restart record carries `tmux_pane` instead.
- `restart` returns the `list-panes` pane pid in pane mode; if `list-panes`
  fails after a successful `respawn-pane` it returns `None` while the pane is
  actually up.
