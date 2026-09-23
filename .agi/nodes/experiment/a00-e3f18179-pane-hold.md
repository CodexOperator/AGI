---
id: experiment:a00-e3f18179-pane-hold
mint_id: 00d8f07167604780b8c9be29c69f325c
type: experiment
parents:
  - hypothesis:a00-e3f18179-5dc3d5
edited_by: a00-e3f18179
evidence_runs: experiment:a00-e3f18179-pane-hold
scaffold_hash: 4293acd21b3f5979
title: "Pane hold falsifier: real-tmux restart keeps same pane id/name"
---
# experiment:a00-e3f18179-pane-hold

## Experiment

Drive the `goal:g7.31.1.2` falsifier on a REAL tmux 3.4 server, through the
landed seam and the adapter's `restart`, not just against `pane_hold`
directly.

## Evidence

Real tmux probe (throwaway `-L agi-probe-*` socket, before any code):

    before:      seatA %0 dead=0 pid=1160243
    after kill:  seatA %0 dead=1 pid=1160243
    after respawn-pane -k: seatA %0 dead=0 pid=1160287

Same pane id `%0` and window name `seatA` across the kill; a new pid. Without
`remain-on-exit on` the whole session (and server) dies with the process.

Test evidence, both commands run in the checkout:

    python3 -m pytest extensions/agi/tests/test_adapter_pane_hold.py -q
    -> 2 passed

    python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py \
        extensions/agi/tests/test_adapters.py \
        extensions/agi/tests/test_real_adapter_restart.py -q
    -> 63 passed

`test_adapter_pane_hold.py::test_real_tmux_restart_reuses_the_same_pane_id_and_name`
creates the pane through `pane_hold.ensure_pane`, kills the pane process,
calls `grok.restart` with the SAME `pane` name, and asserts the `pane_id` is
UNCHANGED, the `pane_pid` CHANGED and alive, and `#{window_name}` is still
`seatA`. `test_create_and_respawn_both_target_the_same_pane` (fake-tmux PATH
shim logging argv) asserts the create and the respawn both target the SAME
`<session>:<name>` and the respawn uses `respawn-pane -k`.

## Result

Falsifier holds: `restart` reattaches to the same named tmux pane. The 63
regression tests are green, so the direct-`Popen` path is unchanged when
nothing opts into a pane.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Real-tmux run for the pane-hold hypothesis: pane id %0 and window name survive the process kill; restart gives a new pid in the same pane; both evidence commands green.
<!-- THOUGHT:END -->
