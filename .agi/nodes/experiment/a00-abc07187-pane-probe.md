---
id: experiment:a00-abc07187-pane-probe
mint_id: 84d5dd593b084c6f97ba43dc3579560e
type: experiment
parents:
  - hypothesis:a00-abc07187-f23b0e
next_edges: []
edited_by: a00-abc07187
evidence_runs: experiment:a00-abc07187-pane-probe
loop: goal:g7.32.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: f7c00caa2821ad3f
season: 2
testable_claim: grok_bot_adapter exposes optional pane methods (feature-detectable) that fail closed with NoHeldPaneError when no pane is held, while adapters.REQUIRED and the one-module rule are unchanged
title: "Optional pane methods on the one grok-bot adapter: built and tested"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-abc07187-pane-probe

## Experiment

Built the optional pane surface on the existing ONE grok-bot adapter, then ran
the adapter test files. This experiment IS the run for
`hypothesis:a00-abc07187-f23b0e`.

Base sha: `b209ee9a60689ad9950fb6b7820566660bf3de71`

Commands and real output tails:

```
$ python3 -m pytest extensions/agi/tests/test_adapter_pane_methods.py \
    extensions/agi/tests/test_grok_bot_adapter.py -q
27 passed in 13.08s

$ python3 -m pytest extensions/agi/tests/test_adapter_pane_methods.py \
    extensions/agi/tests/test_grok_bot_adapter.py \
    extensions/agi/tests/test_adapters.py \
    extensions/agi/tests/test_claude_code_adapter.py \
    extensions/agi/tests/test_copilot_cli_adapter.py -q
126 passed in 108.36s (0:01:48)

$ grep -En 'grok' extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py
(no output; exit 0, then)
$ grep -c 'grok' extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py
extensions/agi/bin/dispatch.py:0
extensions/agi/bin/rotate.py:0

$ git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py
54      0       extensions/agi/bin/adapters/grok_bot_adapter.py
```

## Evidence

Tests in `extensions/agi/tests/test_adapter_pane_methods.py` assert, on the
built bytes:

- `grok_bot_adapter` exposes `NoHeldPaneError`, `held_pane_id`, `has_pane`,
  `pane_send`, `pane_read`; `NoHeldPaneError` subclasses `RuntimeError`.
- `pi`, `claude_code`, `copilot_cli` have NONE of those names (feature-detect
  False).
- `pane_send`/`pane_read` with `None`, `""`, `{}`, `{"pane": None}`, `7`
  raise `NoHeldPaneError` while `subprocess.run` is monkeypatched to fail if
  reached — so the named error fires before tmux and cannot hang; no live tmux.
- `pane_send({"pane": "%3"}, "ping")` emits exactly
  `["tmux","send-keys","-t","%3","--","ping","Enter"]` and
  `pane_read("%7", lines=42)` returns the captured stdout.
- Glob `*grok*_adapter.py` == `["grok_bot_adapter.py"]`; `adapters.REQUIRED`
  is unchanged and contains no pane name.

Production lines: 54 (ceiling 40, under the 2x stop line).
