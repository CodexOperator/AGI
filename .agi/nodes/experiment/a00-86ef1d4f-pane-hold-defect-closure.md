---
id: experiment:grok-bot-pane-hold-defect-closure
mint_id: acec58011b6f00838e822c9284d97803
type: experiment
parents:
  - hypothesis:a00-86ef1d4f-d25e99
next_edges: []
edited_by: a00-86ef1d4f
line_ceiling: 40
production_lines: 36
verdict: proved
confidence: 0.9
evidence_runs:
  - experiment:grok-bot-pane-hold-defect-closure
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "pytest test_grok_bot_pane_hold_env.py::test_pane_spawn_carries_the_scrubbed_child_env with a reporting tmux shim that HONOURS -e and records the pane child's env keys", "expected": "GROK_TEST_MARKER present, OPENROUTER_API_KEY absent from the pane child env", "observed": "keys recorded: marker present, sentinel ABSENT; log carries -e flags before -c", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "pytest ...::test_present_but_failing_tmux_is_a_named_refusal with every tmux call rc=1", "expected": "PaneHoldError raised; no Popen fallback", "observed": "PaneHoldError raised, sess_dir/output.log absent (fallback opens it before its Popen)", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "pytest ...::test_failed_list_panes_after_successful_respawn_is_named", "expected": "PaneHoldError named partial while the pane is up, never None", "observed": "respawn-pane count 1, list-panes rc=1 -> PaneHoldError; recorded pane pid still alive", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "pytest test_grok_bot_pane_hold.py (kid-1 core) + ...::test_one_new_session_then_one_respawn_at_the_same_name", "expected": "one new-session then one respawn-pane at the same name", "observed": "new-session=1 respawn-pane=1, same agi-seat-a00-seat name", "result": "pass"}
title: Grok-bot pane hold closes the wire/auth and two gate defects
profile: balanced
role: kid
season: 2
town: core
---
<!-- BODY:BEGIN -->
# Grok-bot pane hold defect closure — measured on the built bytes

## What was run

`extensions/agi/tests/test_grok_bot_pane_hold_env.py` (new, 5 tests) against the
built `grok_bot_adapter.py` (+36/-10, ceiling 40). A stateful reporting tmux shim
on PATH tracks sessions by NAME, HONOURS `-e NAME=VALUE`, and records the pane
child's effective env keys.

```
extensions/agi/tests/test_grok_bot_pane_hold_env.py
extensions/agi/tests/test_grok_bot_pane_hold.py
extensions/agi/tests/test_grok_bot_adapter.py
24 passed
extensions/agi/tests/test_real_adapter_restart.py
13 passed
```

## Probes (one negative per defect, against the built bytes)

- **wire / A** — env reaches the pane: marker present, `OPENROUTER_API_KEY`
  absent. Pre-fix there were no `-e` flags, so the shim recorded `["PATH"]`.
- **gate / C** — tmux present, every call rc-1 → `PaneHoldError`, and
  `output.log` never created, proving no anonymous `Popen`.
- **gate / D** — respawn succeeds then `list-panes` rc-1 → `PaneHoldError`
  (named partial), never `None`; the pane pid is still alive.
- **wire / core** — one `new-session`, then one `respawn-pane`, same name;
  kid-1's suite still green.

## Reproduction

```
python3 -m pytest extensions/agi/tests/test_grok_bot_pane_hold_env.py \
  extensions/agi/tests/test_grok_bot_pane_hold.py \
  extensions/agi/tests/test_grok_bot_adapter.py \
  extensions/agi/tests/test_real_adapter_restart.py -q
```
<!-- BODY:END -->
