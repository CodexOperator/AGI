---
id: experiment:tmux-pane-hold-kill-restart
mint_id: 8d70d47527804fcd98283ecbd8d7047c
type: experiment
parents:
  - hypothesis:a00-65c858a3-3ebc30
next_edges: []
edited_by: a00-65c858a3
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: bdd8443f1a80d1f5
season: 2
testable_claim: "A real tmux named pane keeps its window name and #{pane_id} across seat process death and the adapter restart re-enters it."
title: Real-tmux kill then adapter restart keeps the named pane
town: core
---
<!-- BODY:BEGIN -->
# experiment:tmux-pane-hold-kill-restart

## Experiment

Run the adapter's pane-backed restart against REAL tmux in a private session
and check the pane identity before/after a kill.

`extensions/agi/bin/adapters/tmux_hold.py` (new) provides `start` (create the
named pane only if absent) and `reattach` (`tmux respawn-pane -k -t
<session>:<name>`, never a second `new-window`). `remain-on-exit on` keeps a
dead pane listed so its `#{pane_id}` survives. `grok_bot_adapter.restart`
routes through `reattach` when `harness["tmux"]` is set; unset keeps the
direct-`Popen` path untouched.

Standalone script (not pytest — the conftest `_no_real_tmux` fixture replaces
`tmux` with an rc-1 stub), own uniquely-named session
`agi-hold-measure-a0065c`, never `agi-rc`:

```
$ python3 .agi/sessions/iter-DT.24/a00-65c858a3/measure_pane_hold.py
--- list-panes before-kill: [('seat-5b76ee7da59d', '%11', '2253656')]
start() pid=2253656
--- list-panes after-kill: [('seat-5b76ee7da59d', '%11', '2253656')]
--- pane_dead after kill: 1
--- capture after kill (tail): ['Pane is dead (signal 9, Mon Sep 21 04:40:08 2026)']
--- list-panes after-restart: [('seat-5b76ee7da59d', '%11', '2253693')]
restart() pid=2253693
--- pane_dead after restart: 0
--- output.log MOCK-SEAT-ALIVE lines: ['MOCK-SEAT-ALIVE pid=2253656', 'MOCK-SEAT-ALIVE pid=2253693']
--- checks: {
  "same window name": true,
  "same pane_id": true,
  "exactly one pane with that name": true,
  "new pid differs (process really died)": true,
  "pane_dead cleared after restart": true,
  "seat ran again in the same pane (fresh marker)": true,
  "restart pid == pane pid": true
}
--- VERDICT: PASS
```

Repo suite on the changed surface:
`python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_adapters.py -q`
→ **50 passed**.

## Evidence

Pane-identity predicate: `window_name == pane_name(agent_id)` AND exactly one
pane carries that window name AND `#{pane_id}` after == before AND
`pane_dead == 0` after. All true: same `%11`, one pane named
`seat-5b76ee7da59d`, fresh `MOCK-SEAT-ALIVE` marker after restart.

## Evidence

Raw output, screenshots, logs.
