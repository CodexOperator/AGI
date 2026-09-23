---
id: experiment:a00-f1c9295b-pane-methods
mint_id: 41aaf48d9f494f06ade92fe05f857d02
type: experiment
parents:
  - hypothesis:a00-f1c9295b-c773ea
next_edges: []
edited_by: a00-f1c9295b
line_ceiling: 40
loop: goal:g7.32.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 75
profile: balanced
role: kid
scaffold_hash: ca5808005a292d58
season: 2
title: build grok pane methods with dead-target fail-closed and runner seam
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-f1c9295b-pane-methods

## Experiment

BUILD round (goal:g7.32.3): ported the canonical unmerged design from
worktree `a00-f09b3a86` — `adapters.OPTIONAL_PANE`, `adapters.PaneNotHeld`,
`adapters.pane_interface(mod)`, and the `pane_attach` / `pane_send` /
`pane_read` methods on `grok_bot_adapter` — and FIXED its known DT.99 defect:
that version ignored the tmux returncode, so a DEAD target returned silently
(`pane_attach` -> `{"live": False}`; `pane_send`/`pane_read` -> a value).

**The fix.** One helper `_run_pane(args, pane, runner)` gates all three
methods. It calls `_require_pane(pane)` FIRST (so a missing/malformed hold
refuses before any subprocess) and then refuses by name on an injected
`runner` whose `returncode != 0`, on `OSError`, and on
`subprocess.TimeoutExpired`. The default `_tmux` carries `timeout=5`, so a
wedged tmux cannot hang. `pane_attach` now returns `{"pane": ..., "live":
True}` only after a zero-rc probe; dead targets raise. `runner=` is the ONE
tmux seam, so no live tmux is needed.

Production change (test excluded): `git diff --numstat` = 22 added lines in
`extensions/agi/bin/adapters/__init__.py` + 53 in
`extensions/agi/bin/adapters/grok_bot_adapter.py` = **75 lines**. Ceiling 40;
75 is under the 2x (80) stop threshold, so the round continues with the
overage recorded below rather than a re-brief.

## Evidence

New test file `extensions/agi/tests/test_adapter_pane_methods.py` asserts the
three conjuncts of the hypothesis, with the tmux seam injected:

- feature detection: `pane_interface(grok) == OPTIONAL_PANE`, and
  `pane_interface(mod) == ()` + `hasattr(mod, "pane_send") is False` for pi,
  claude_code, copilot_cli; `REQUIRED` unchanged; exactly one
  `*grok*_adapter.py`.
- fail closed, no hold: all three methods x {None, "", "   "} raise
  `PaneNotHeld` with a `runner` that fails if reached (proves pre-subprocess).
- fail closed, dead target: rc=1, `OSError`, `subprocess.TimeoutExpired` each
  raise `PaneNotHeld` for all three methods — never a value.
- success path: `send-keys -t %3 ping Enter` argv captured; `capture-pane`
  stdout returned; `display-message` -> `{"pane": "%3", "live": True}`.

Command and output:

```
python3 -m pytest extensions/agi/tests/test_adapter_pane_methods.py \
  extensions/agi/tests/test_grok_bot_adapter.py \
  extensions/agi/tests/test_adapters.py -q
78 passed in 30.90s
```

`grep -n grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py` ->
no matches (zero harness-name special-case).
