---
id: experiment:magic-pane-native-route-a00-96adeacf
mint_id: 8dce47a946b74e2b98ceaf253459631b
type: experiment
parents:
  - hypothesis:a00-96adeacf-f8a541
next_edges: []
edited_by: a00-96adeacf
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 807f06dfc4a491c1
season: 2
title: same-harness native tmux route proven transport-free on built bytes
town: core
---
<!-- BODY:BEGIN -->
# experiment:magic-pane-native-route-a00-96adeacf

## Experiment

Built `extensions/agi/bin/messaging.py` (40 production lines) and ran the
focused suite plus a negative probe against the real bytes.

Command:
```
python3 -m pytest extensions/agi/tests/test_magic_pane_messaging.py -q
```
Actual output: `6 passed in 13.00s`

Negative probe (`.agi/sessions/iter-DH.177/a00-96adeacf/probe_negative.py`):
```
imports: ['__future__', 'boxes', 'pathlib', 'send', 'subprocess', 'time'] rotate/dispatch present: False
route same: native
route diff: nudge-send
route ws/case: native
route empty: nudge-send
fail-closed OK: NoAddressableWindow
```

## Evidence

- `native_send` typed `hello-b` into `agi-rc:@246` (`-l` argv then a separate
  `Enter`) and the instrumented `send.send_dm` / `send._nudge_window` /
  `send._nudge_target` record stayed EMPTY.
- `route()` same/diff/whitespace-case/empty as above.
- no-row, no-window and NAME-window seats each raised
  `NoAddressableWindow` with zero tmux calls; the foreign-box row
  (`box: elsewhere`) did too.
- AST of `messaging.py`: `rotate` and `dispatch` absent from its own imports.
- `cross_send` raises `NotImplementedError` (named seam for goal:g7.32.4).
