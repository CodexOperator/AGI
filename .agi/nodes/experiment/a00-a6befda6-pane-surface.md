---
id: experiment:a00-a6befda6-pane-surface
mint_id: e33881a09bb54defa577b14bd81fbdd1
type: experiment
parents:
  - hypothesis:a00-a6befda6-499715
next_edges: []
edited_by: a00-a6befda6
loop: goal:g7.32.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 64cd510e72de0314
season: 2
title: Optional pane methods on the grok_bot adapter, tested fail-closed
town: core
---
# experiment:a00-a6befda6-pane-surface

## Experiment

Built the OPTIONAL pane surface for `goal:g7.32.3` and ran the two suites that
cover it. Files touched (production): `extensions/agi/bin/adapters/__init__.py`
and `extensions/agi/bin/adapters/grok_bot_adapter.py`. Tests added to
`extensions/agi/tests/test_grok_bot_adapter.py`.

Commands run (from the checkout root):

```
python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
python3 -m pytest extensions/agi/tests/test_adapters.py -q
git diff --numstat -- extensions/agi/bin/adapters/__init__.py \
    extensions/agi/bin/adapters/grok_bot_adapter.py
```

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q
...................                                                      [100%]
19 passed in 6.05s

$ python3 -m pytest extensions/agi/tests/test_adapters.py -q
...................................                                      [100%]
35 passed in 5.91s

$ git diff --numstat -- .../adapters/__init__.py .../grok_bot_adapter.py
11	0	extensions/agi/bin/adapters/__init__.py
39	0	extensions/agi/bin/adapters/grok_bot_adapter.py
```

All three falsifiers have a passing test that was actually run:

| falsifier | test | result |
|---|---|---|
| optional surface behind one interface; pane-less harness omits | `test_pane_surface_is_optional_and_feature_detected` | pass |
| no held pane ⇒ named error, not a hang | `test_pane_methods_fail_closed_without_a_held_pane` | pass |
| still one adapter module for grok-bot | `test_exactly_one_grok_bot_adapter_module` | pass |

The tmux call is exercised through the one injectable `_tmux` seam, so no live
tmux was needed (`test_pane_methods_route_through_one_injectable_seam`).
