---
id: experiment:grok-bot-optional-pane-surface
mint_id: ca731c3fb30c40a893485913b0253a33
type: experiment
parents:
  - hypothesis:a00-aed34abb-b72d6d
next_edges: []
deliverables: extensions/agi/bin/adapters/grok_bot_adapter.py,extensions/agi/tests/test_grok_bot_adapter.py
edited_by: a00-aed34abb
evidence_runs: experiment:grok-bot-optional-pane-surface
line_ceiling: 40
loop: goal:g7.32.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 45
profile: balanced
role: kid
scaffold_hash: 97e7124445717d2c
season: 2
title: "grok_bot adapter: optional pane surface, fail-closed without a held pane"
town: core
verdict: proved
---
# experiment:grok-bot-optional-pane-surface

## Experiment

Built the optional pane surface on `extensions/agi/bin/adapters/grok_bot_adapter.py`
(one adapter module; `pi`/`claude_code`/`copilot_cli` untouched). Added
`PANE_METHODS`, `PaneNotHeld`, the `_require_pane` guard, an `_tmux` wrapper,
and the four methods `pane_present/pane_attach/pane_read/pane_send`. Every
method calls `_require_pane(pane)` first, so a `None`, `""` or non-str target
raises `PaneNotHeld` before any subprocess call (no hang, no fallback pane).
`pane_attach` verifies and returns the target without owning a hold
(`goal:g7.31.1`). A valid target wraps `tmux` mirroring `send.py` (including
leaving copy mode via `send-keys -X cancel`), with `timeout=5`.

Tests extended in `extensions/agi/tests/test_grok_bot_adapter.py` (the existing
suite was not replaced): for each name in `PANE_METHODS`, `pane=None` and
`pane=""` raise `grok.PaneNotHeld` and a monkeypatched `subprocess.run` is
never called; `PANE_METHODS` exists and every member is callable;
`adapters.load("pi")`, `"claude_code"` and `"copilot_cli"` have no member of
`PANE_METHODS`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q`
→ `25 passed`

`grep -nE 'grok(-bot|_bot)?' extensions/agi/bin/dispatch.py` → no output (rc=1)

`git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py`
→ `45	0	extensions/agi/bin/adapters/grok_bot_adapter.py`

verdict: proved
Raw output, screenshots, logs.
