---
id: experiment:a00-52947a93-hold-seam
mint_id: 9d0b2d1b6d4c4d3aa72c7e5a1f3b8c90
type: experiment
parents:
  - hypothesis:a00-52947a93-f2e5a8
next_edges: []
edited_by: a00-52947a93
line_ceiling: 40
loop: goal:g7.31.1.2.1@s2
production_lines: 0
role: kid
season: 2
status: active
title: Classify the held restart seam before patching
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-52947a93-hold-seam

## Question

Can this checkout produce a hermetic held restart with adapter `child_env` threaded through the held pane?

## Method

A source search over `extensions/` found no `tmux_hold`, `HOLD_PANE`, or `hold_pane` implementation or call site. The available restart implementation is `extensions/agi/bin/adapters/grok_bot_adapter.py:136-148`, which calls `child_env(harness=..., base=dict(os.environ), tier=...)` and passes `env=env` to `subprocess.Popen`. I ran the focused real-path tests:

```
python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_credential_none_spawn.py extensions/agi/tests/test_real_adapter_restart.py -q
```

Result: **40 passed, 7 warnings**. The warnings are pre-existing `datetime.utcnow()` deprecations in `node_writer.py`; the tier gate also reported unrelated phantom running records and skipped those checks.

## Finding

The named hold-pane behavior cannot be exercised on this checkout. The direct adapter restart is environmentally correct, but that is not evidence for tmux hold/restart continuity. No implementation was changed, avoiding a fabricated seam or a test that would only prove the direct path again.

## Residue

The next run should first reconcile the graph goal with the actual source revision, or add the hold implementation and its environment-capture test as a build/behavior pair.
